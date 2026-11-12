# Fictional Supplier Data Dictionary

All alternatives, values, and scenarios are invented for this project.

| Field | Type | Unit / scale | Direction | Meaning |
|---|---|---|---|---|
| `Supplier` | text | name | identifier | Fictional alternative label |
| `Unit Price (EUR)` | number | EUR per unit | cost | Lower quoted price is preferred |
| `Delivery Time (days)` | number | calendar days | cost | Lower expected lead time is preferred |
| `Quality Score (%)` | number | percent | benefit | Higher accepted-quality estimate is preferred |
| `On-Time Delivery (%)` | number | percent | benefit | Higher reliability estimate is preferred |
| `Sustainability Score` | number | 0-100 points | benefit | Higher fictional composite score is preferred |
| `Risk Score` | number | 1-5 points | cost | Lower fictional risk estimate is preferred |

## Baseline weights

| Criterion | Weight |
|---|---:|
| Unit Price (EUR) | 0.25 |
| Delivery Time (days) | 0.15 |
| Quality Score (%) | 0.25 |
| On-Time Delivery (%) | 0.15 |
| Sustainability Score | 0.10 |
| Risk Score | 0.10 |
| **Total** | **1.00** |

The weights are illustrative preference inputs only.

## Assumptions

- Every criterion is numerical, finite, and available for every supplier.
- Higher normalized performance is always preferred.
- WSM allows compensation among criteria.
- No hard qualification threshold is modeled.
- Criteria are treated as independent.
- The comparison set contains six suppliers unless the outlier experiment states otherwise.

## Data provenance

The dataset was constructed specifically for this course project. It contains no personal data, confidential commercial information, or copied supplier records.
