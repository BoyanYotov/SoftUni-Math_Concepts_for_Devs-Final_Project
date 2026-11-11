from __future__ import annotations
from collections.abc import Mapping, Sequence

import numpy as np
import pandas as pd

VALID_DIRECTIONS = {"cost", "benefit"}

def validate_problem(
    data: pd.DataFrame,
    criteria: Sequence[str],
    directions: Mapping[str, str],
    weights: Mapping[str, float],
) -> None:
    """Validate an MCDA decision problem and raise ``ValueError`` if invalid."""
    if not isinstance(data, pd.DataFrame) or data.empty:
        raise ValueError("data must be a non-empty pandas DataFrame")
    if not criteria:
        raise ValueError("at least one criterion is required")
    if len(set(criteria)) != len(criteria):
        raise ValueError("criteria must be unique")

    missing = [criterion for criterion in criteria if criterion not in data.columns]
    if missing:
        raise ValueError(f"missing criteria columns: {missing}")

    non_numeric = [criterion for criterion in criteria if not pd.api.types.is_numeric_dtype(data[criterion])]
    if non_numeric:
        raise ValueError(f"criteria must be numeric: {non_numeric}")
    if data[list(criteria)].isna().any().any():
        raise ValueError("criteria contain missing values")
    if not np.isfinite(data[list(criteria)].to_numpy(dtype=float)).all():
        raise ValueError("criteria contain non-finite values")

    if set(directions) != set(criteria):
        raise ValueError("directions must contain exactly the criteria")
    invalid_directions = {key: value for key, value in directions.items() if value not in VALID_DIRECTIONS}
    if invalid_directions:
        raise ValueError(f"directions must be 'cost' or 'benefit': {invalid_directions}")

    if set(weights) != set(criteria):
        raise ValueError("weights must contain exactly the criteria")
    weight_values = np.array([weights[criterion] for criterion in criteria], dtype=float)
    if not np.isfinite(weight_values).all() or (weight_values < 0).any():
        raise ValueError("weights must be finite and non-negative")
    if not np.isclose(weight_values.sum(), 1.0, atol=1e-9):
        raise ValueError(f"weights must sum to 1; received {weight_values.sum():.12f}")

def minmax_normalize(
    data: pd.DataFrame,
    criteria: Sequence[str],
    directions: Mapping[str, str],
) -> pd.DataFrame:
    """Normalize all criteria to [0, 1], where a larger value is always better.

    For a constant criterion all alternatives receive 1.0. This criterion then
    contributes the same amount to every WSM score and cannot change the ranking.
    """
    result = pd.DataFrame(index=data.index)
    for criterion in criteria:
        values = data[criterion].astype(float)
        minimum, maximum = values.min(), values.max()
        value_range = maximum - minimum
        if np.isclose(value_range, 0.0):
            result[criterion] = 1.0
        elif directions[criterion] == "benefit":
            result[criterion] = (values - minimum) / value_range
        else:
            result[criterion] = (maximum - values) / value_range
    return result


def weighted_sum(
    normalized: pd.DataFrame,
    weights: Mapping[str, float],
) -> pd.Series:
    """Calculate WSM scores as the matrix-vector product ``R @ w``."""
    criteria = list(weights)
    if list(normalized.columns) != criteria:
        normalized = normalized.loc[:, criteria]
    weight_vector = np.array([weights[criterion] for criterion in criteria], dtype=float)
    scores = normalized.to_numpy(dtype=float) @ weight_vector
    return pd.Series(scores, index=normalized.index, name="WSM Score")


def topsis(
    data: pd.DataFrame,
    criteria: Sequence[str],
    directions: Mapping[str, str],
    weights: Mapping[str, float],
) -> pd.DataFrame:
    """Run TOPSIS and return distances and closeness coefficients.

    The method uses vector normalization. For a benefit criterion, the ideal is
    the maximum weighted-normalized value; for a cost criterion it is the minimum.
    The closeness coefficient is D- / (D+ + D-), so larger values are preferred.
    """
    validate_problem(data, criteria, directions, weights)
    matrix = data.loc[:, criteria].to_numpy(dtype=float)
    denominators = np.sqrt((matrix**2).sum(axis=0))
    if np.isclose(denominators, 0.0).any():
        zero_columns = [criteria[i] for i, value in enumerate(denominators) if np.isclose(value, 0.0)]
        raise ValueError(f"TOPSIS cannot vector-normalize all-zero criteria: {zero_columns}")

    normalized = matrix / denominators
    weight_vector = np.array([weights[criterion] for criterion in criteria], dtype=float)
    weighted = normalized * weight_vector

    ideal = np.empty(len(criteria))
    anti_ideal = np.empty(len(criteria))
    for position, criterion in enumerate(criteria):
        column = weighted[:, position]
        if directions[criterion] == "benefit":
            ideal[position], anti_ideal[position] = column.max(), column.min()
        else:
            ideal[position], anti_ideal[position] = column.min(), column.max()

    distance_to_ideal = np.linalg.norm(weighted - ideal, axis=1)
    distance_to_anti = np.linalg.norm(weighted - anti_ideal, axis=1)
    denominator = distance_to_ideal + distance_to_anti
    closeness = np.divide(
        distance_to_anti,
        denominator,
        out=np.full_like(distance_to_anti, 0.5),
        where=~np.isclose(denominator, 0.0),
    )
    return pd.DataFrame(
        {
            "Distance to ideal": distance_to_ideal,
            "Distance to anti-ideal": distance_to_anti,
            "TOPSIS Closeness": closeness,
        },
        index=data.index,
    )

def rank_scores(scores: pd.Series, higher_is_better: bool = True) -> pd.Series:
    """Convert scores to dense integer ranks; tied values receive the same rank."""
    return scores.rank(method="dense", ascending=not higher_is_better).astype(int).rename("Rank")

def proportional_reweight(
    base_weights: Mapping[str, float],
    target_criterion: str,
    target_weight: float,
) -> dict[str, float]:
    """Change one weight and redistribute the remainder proportionally."""
    if target_criterion not in base_weights:
        raise ValueError(f"unknown target criterion: {target_criterion}")
    if not 0 <= target_weight <= 1:
        raise ValueError("target_weight must be between 0 and 1")

    others = [criterion for criterion in base_weights if criterion != target_criterion]
    other_total = sum(base_weights[criterion] for criterion in others)
    if np.isclose(other_total, 0.0) and target_weight < 1:
        raise ValueError("cannot redistribute weight because all other base weights are zero")

    adjusted = {target_criterion: float(target_weight)}
    remaining = 1.0 - target_weight
    for criterion in others:
        adjusted[criterion] = remaining * base_weights[criterion] / other_total
    return {criterion: adjusted[criterion] for criterion in base_weights}


def one_way_sensitivity(
    normalized: pd.DataFrame,
    base_weights: Mapping[str, float],
    target_criterion: str,
    target_values: Sequence[float],
) -> pd.DataFrame:
    """Sweep one WSM weight and record every supplier score, rank, and winner."""
    records: list[dict[str, float | int | str]] = []
    for target_value in target_values:
        weights = proportional_reweight(base_weights, target_criterion, float(target_value))
        scores = weighted_sum(normalized, weights)
        ranks = rank_scores(scores)
        winner = str(scores.idxmax())
        ordered = scores.sort_values(ascending=False)
        margin = float(ordered.iloc[0] - ordered.iloc[1]) if len(ordered) > 1 else np.nan
        for supplier in scores.index:
            records.append(
                {
                    "Target weight": float(target_value),
                    "Supplier": str(supplier),
                    "Score": float(scores.loc[supplier]),
                    "Rank": int(ranks.loc[supplier]),
                    "Winner": winner,
                    "Winning margin": margin,
                }
            )
    return pd.DataFrame.from_records(records)

def sample_weights(
    base_weights: Mapping[str, float],
    samples: int,
    concentration: float = 40.0,
    seed: int = 42,
) -> pd.DataFrame:
    """Draw plausible weight vectors from a Dirichlet distribution.

    The expected value equals ``base_weights``. Larger concentration means less
    variation around that baseline. A fixed seed makes the experiment reproducible.
    """
    if samples <= 0:
        raise ValueError("samples must be positive")
    if concentration <= 0:
        raise ValueError("concentration must be positive")
    criteria = list(base_weights)
    base = np.array([base_weights[criterion] for criterion in criteria], dtype=float)
    if (base <= 0).any() or not np.isclose(base.sum(), 1.0):
        raise ValueError("Dirichlet sampling requires positive weights summing to 1")
    rng = np.random.default_rng(seed)
    draws = rng.dirichlet(base * concentration, size=samples)
    return pd.DataFrame(draws, columns=criteria)


def summarize_ranks(score_table: pd.DataFrame) -> pd.DataFrame:
    """Summarize winner frequency and average rank from simulations.

    ``score_table`` must have one row per simulation and one column per supplier.
    """
    ranks = score_table.rank(axis=1, method="min", ascending=False)
    winners = score_table.idxmax(axis=1).value_counts(normalize=True)
    return (
        pd.DataFrame(
            {
                "Win frequency": winners.reindex(score_table.columns, fill_value=0.0),
                "Average rank": ranks.mean(axis=0),
                "Rank std. dev.": ranks.std(axis=0),
            }
        )
        .sort_values(["Win frequency", "Average rank"], ascending=[False, True])
    )
