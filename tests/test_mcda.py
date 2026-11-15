from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.mcda import (
    minmax_normalize,
    one_way_sensitivity,
    proportional_reweight,
    rank_scores,
    sample_weights,
    summarize_ranks,
    topsis,
    validate_problem,
    weighted_sum,
)


@pytest.fixture
def simple_problem():
    data = pd.DataFrame(
        {"Cost": [10.0, 20.0, 15.0], "Quality": [70.0, 90.0, 80.0]},
        index=["A", "B", "C"],
    )
    criteria = ["Cost", "Quality"]
    directions = {"Cost": "cost", "Quality": "benefit"}
    weights = {"Cost": 0.4, "Quality": 0.6}
    return data, criteria, directions, weights


def test_minmax_normalization_handles_cost_and_benefit(simple_problem):
    data, criteria, directions, _ = simple_problem
    result = minmax_normalize(data, criteria, directions)
    expected = pd.DataFrame(
        {"Cost": [1.0, 0.0, 0.5], "Quality": [0.0, 1.0, 0.5]},
        index=data.index,
    )
    pd.testing.assert_frame_equal(result, expected)


def test_constant_criterion_gives_equal_normalized_values():
    data = pd.DataFrame({"Constant": [5.0, 5.0], "Benefit": [1.0, 2.0]})
    result = minmax_normalize(data, list(data.columns), {"Constant": "cost", "Benefit": "benefit"})
    assert result["Constant"].tolist() == [1.0, 1.0]


def test_validation_rejects_bad_weight_sum(simple_problem):
    data, criteria, directions, weights = simple_problem
    weights["Quality"] = 0.5
    with pytest.raises(ValueError, match="sum to 1"):
        validate_problem(data, criteria, directions, weights)


def test_weighted_sum_matches_manual_dot_product(simple_problem):
    data, criteria, directions, weights = simple_problem
    normalized = minmax_normalize(data, criteria, directions)
    result = weighted_sum(normalized, weights)
    np.testing.assert_allclose(result.to_numpy(), normalized.to_numpy() @ np.array([0.4, 0.6]))
    assert result.between(0, 1).all()


def test_topsis_closeness_and_rank_are_valid(simple_problem):
    data, criteria, directions, weights = simple_problem
    result = topsis(data, criteria, directions, weights)
    assert result["TOPSIS Closeness"].between(0, 1).all()
    ranks = rank_scores(result["TOPSIS Closeness"])
    assert set(ranks) <= {1, 2, 3}


def test_topsis_rejects_all_zero_criterion():
    data = pd.DataFrame({"Zero": [0.0, 0.0], "Benefit": [1.0, 2.0]}, index=["A", "B"])
    with pytest.raises(ValueError, match="all-zero"):
        topsis(
            data,
            ["Zero", "Benefit"],
            {"Zero": "cost", "Benefit": "benefit"},
            {"Zero": 0.5, "Benefit": 0.5},
        )


def test_proportional_reweight_preserves_sum_and_ratios():
    base = {"A": 0.5, "B": 0.3, "C": 0.2}
    changed = proportional_reweight(base, "A", 0.25)
    assert sum(changed.values()) == pytest.approx(1.0)
    assert changed["A"] == pytest.approx(0.25)
    assert changed["B"] / changed["C"] == pytest.approx(0.3 / 0.2)


def test_one_way_sensitivity_returns_all_suppliers_and_values(simple_problem):
    data, criteria, directions, weights = simple_problem
    normalized = minmax_normalize(data, criteria, directions)
    result = one_way_sensitivity(normalized, weights, "Cost", [0.2, 0.4, 0.6])
    assert len(result) == len(data) * 3
    assert result.groupby("Target weight")["Winner"].nunique().eq(1).all()


def test_weight_sampling_is_reproducible_and_sums_to_one():
    base = {"A": 0.5, "B": 0.3, "C": 0.2}
    first = sample_weights(base, samples=25, seed=7)
    second = sample_weights(base, samples=25, seed=7)
    pd.testing.assert_frame_equal(first, second)
    np.testing.assert_allclose(first.sum(axis=1), 1.0)


def test_rank_summary_frequencies_sum_to_one():
    scores = pd.DataFrame({"A": [0.9, 0.2, 0.8], "B": [0.8, 0.7, 0.1]})
    summary = summarize_ranks(scores)
    assert summary["Win frequency"].sum() == pytest.approx(1.0)
    assert summary["Average rank"].between(1, 2).all()
