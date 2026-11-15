# Choosing the Best Supplier with Mathematics: *Weighted Scoring, TOPSIS, and Sensitivity Analysis in Python*

This project for the SoftUni *Math Concepts for Developers* course turns a fictional supplier-selection problem into an auditable multi-criteria decision analysis (MCDA). All suppliers and values are fictional; the results are educational and are not procurement advice.

## Research question

> How can normalization, weights, and distance from ideal solutions turn conflicting supplier criteria into a transparent recommendation, and how stable is that recommendation when assumptions change?

## Main result

Under the baseline weights, **Borealis Industries** ranks first with a WSM score of **0.7243**, narrowly ahead of **Evergreen Manufacturing** at **0.7182**. TOPSIS gives the same complete baseline order. The small WSM margin (**0.0061**) and the sensitivity experiments show that the recommendation is provisional rather than universal.

## Repository structure

```text
├── config/decision_problem.json       # Criteria, directions, weights, valid ranges
├── data/fictional_suppliers.csv       # Synthetic input data
├── docs/DATA_DICTIONARY.md            # Units, meanings, assumptions, provenance
├── notebooks/supplier_selection.ipynb # Complete executed mathematical analysis
├── outputs/                           # Six notebook-generated result CSV files
│   └── figures/                       # Optional rendered notebook figures
├── scripts/verify_project.py          # Clean notebook execution helper
├── src/__init__.py
├── src/mcda.py                        # Validated reusable MCDA functions
├── tests/test_mcda.py                 # Automated pytest suite
├── VALIDATION_REPORT.md
└── requirements.txt
```

## Methods

- direction-aware min-max normalization for cost and benefit criteria;
- Weighted Sum Model (WSM) as a matrix-vector product;
- TOPSIS with vector normalization and ideal/anti-ideal distances;
- scenario analysis;
- one-way price-weight sensitivity;
- 5,000-sample Monte Carlo weight-robustness analysis;
- leave-one-criterion-out and outlier checks;
- Kendall rank correlation and automated tests.

## Reproduce the project

### 1. Create and activate a virtual environment

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate
```

### 2. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The project was verified with Python 3.12. The bounded dependency ranges in `requirements.txt` permit compatible updates.

### 3. Run the tests

```bash
python -m pytest -q
```

### 4. Run the notebook

```bash
jupyter notebook notebooks/supplier_selection.ipynb
```

In Jupyter, use **Kernel → Restart Kernel and Run All Cells**. The first code cell searches upward for the repository root, so the notebook works when launched from either the repository root or `notebooks/`.

### 5. Regenerate outputs

The final notebook cells write:

- `outputs/baseline_rankings.csv`
- `outputs/scenario_winners.csv`
- `outputs/price_weight_transitions.csv`
- `outputs/wsm_random_weight_summary.csv`
- `outputs/topsis_random_weight_summary.csv`
- `outputs/leave_one_criterion_out.csv`

## Quality and reproducibility controls

- unique supplier names, numeric finite values, criterion domain ranges, directions, and weights are validated;
- all weights must be non-negative and sum to one;
- the random-weight experiment uses seed `2026`;
- the test suite covers normal and edge cases;
- the notebook contains comments explaining imports, formulas, code purpose, and interpretation;
- citations use a numbered IEEE-style format and trace methods to sources.

## Academic integrity and AI assistance

AI tools were used for language improvement, code suggestions, and review. The author reviewed, executed, and validated the submitted content, takes responsibility for it.

## References
See section *References* in the end of the notebook.
