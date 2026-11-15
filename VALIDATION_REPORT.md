# Validation Report

## Verification scope

The project was rebuilt from the supplied dataset, configuration, source module, executed HTML report, and saved results. The verification process checks code, mathematics, reproducibility, notebook execution, outputs, documentation, and the previously identified audit findings.

## Implemented audit corrections

- repository-root search works from `notebooks/`;
- raw-data horizontal charts invert the y-axis so the preferred value appears at the top;
- a real pytest suite replaces the unsupported testing claim;
- notebook code generates all six output CSV files;
- bounded dependencies and end-to-end execution instructions are documented;
- `SELF_ASSESSMENT.md` is included;
- numbered in-text citations and an AI-assistance disclosure are included;
- “Global sensitivity” is renamed “Monte Carlo weight-robustness analysis” and explicitly distinguished from Sobol-style sensitivity indices;
- `Viisualization` and other wording issues are corrected;
- the quality criterion is described as a fictional estimated acceptance/composite quality percentage;
- WSM and TOPSIS are compared in an advantages/limitations table;
- supplier-name uniqueness and domain ranges are validated;
- `src/__init__.py` provides explicit package structure;
- the output scenario table has a `Scenario` index heading.

## Expected numerical checks

- WSM winner: Borealis Industries, score approximately 0.7243056.
- WSM runner-up: Evergreen Manufacturing, score approximately 0.7182065.
- TOPSIS winner: Borealis Industries, closeness approximately 0.7945948.
- Price-weight transitions on the 0.01 grid: Evergreen at 0.05, Borealis at 0.23, Falcon at 0.48.
- WSM random-weight winner frequencies: Borealis 59.04%, Evergreen 40.78%.
- TOPSIS random-weight winner frequencies: Borealis 69.44%, Evergreen 30.10%.
- Method winner agreement: 77.38%.

## External submission checks

The archive cannot establish GitHub commit history. Before submission, confirm that the public repository contains the actual notebook and at least 10 genuine, meaningful commits, then run the notebook from a clean kernel in the submitted repository.

## Final build verification

- 13 automated tests passed.
- All 23 notebook code cells executed sequentially from the `notebooks/` working directory.
- The executed notebook contains 0 error outputs and 6 embedded visualizations.
- All six regenerated CSV files match the supplied numerical results (the scenario index heading is now explicitly `Scenario`).
- A standalone HTML report and six PNG figure exports were generated from the executed notebook.
