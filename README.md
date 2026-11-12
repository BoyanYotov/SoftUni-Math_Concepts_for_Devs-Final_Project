# Choosing the Best Supplier with Mathematics: Weighted Scoring, TOPSIS, and Sensitivity Analysis #

This project serves as the final submission for the *Math Concepts for Developers* course at *SoftUni*. It illustrates how a supplier selection problem can be transformed into a decision matrix, followed by normalization, weighting, ranking, and stress testing using Python. 

The project includes a technical report, a tutorial, a reusable module, automated tests, and an executed Jupyter notebook. Please note that all supplier names and values presented are fictional.

## Research question ##
> How can normalization, weights, and distance from ideal solutions turn several conflicting supplier criteria into a transparent recommendation - and how stable is that recommendation when assumptions change?

## Main findings from the fictional dataset ##
- **Weighted Sum Model (WSM):** Borealis Industries ranks first with a score of **0.7243**, narrowly ahead of Evergreen Manufacturing at **0.7182**.
- **TOPSIS:** Borealis also ranks first; the complete baseline ordering is identical to WSM.
- **Small baseline margin:** the WSM first-second gap is only **0.0061**, so the result should be treated as provisional.
- **Scenario dependence:** a quality-and-reliability scenario and an equal-weight scenario select Evergreen.
- **Price sensitivity:** the WSM winner changes from Evergreen to Borealis around a price weight of **0.23**, then to Falcon around **0.48** (0.01 grid resolution).
- **Random-weight robustness:** across 5,000 reproducible near-baseline weight samples, Borealis wins **59.04%** of WSM runs and Evergreen wins **40.78%**. WSM and TOPSIS choose the same winner in **77.38%** of runs.

*These are educational results, not procurement advice.*

## Repository structure ##
```text
SoftUni-Math_Concepts_for_Devs-Final_Project
├── config/
│   └── decision_problem.json       
├── data/
│   ├── DATA_DICTIONARY.md          
│   └── fictional_suppliers.csv     
├── notebooks/
│   └── supplier_selection.ipynb               
├── src/
│   └── mcda.py                     
└── README.md
```

## Mathematics covered ##
1. Decision matrices
2. Cost and benefit criteria
3. Direction-aware min-max normalization
4. Weight constraints and weighted averages
5. Vectors, dot products, and matrix-vector multiplication
6. Weighted Sum Model
7. Euclidean distance
8. TOPSIS ideal and anti-ideal solutions
9. Kendall rank correlation
10. Scenario, one-way, random-weight, leave-one-criterion-out, and outlier sensitivity analysis

## Limitations ##
- Synthetic data cannot predict real supplier performance.
- Weights are subjective and must be agreed before use.
- WSM is compensatory; real sourcing often needs mandatory gates.
- Correlated criteria can double-count performance.
- Min-max normalization is sensitive to outliers and the comparison set.
- TOPSIS and other relative methods can exhibit rank reversal.
- The experiment varies preference weights but does not model measurement uncertainty.
  
## References ##
*See Section **'References'** in the end of the notebook for full reference list.*
