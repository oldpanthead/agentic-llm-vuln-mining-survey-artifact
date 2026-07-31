# Final Multi-Source Search: All Independent-Coder Batches

Eligibility agreement is calculated over every reviewed candidate. Analytical coding agreement is calculated only for records that both coders included at study level. Claim-boundary prose is not assigned a synthetic exact-agreement statistic.

## Coverage

| Batch | Reviewed | Eligibility exact | Jointly included |
|---|---:|---:|---:|
| main | 86 | 86/86 | 86 |
| addendum | 9 | 9/9 | 9 |
| remaining | 41 | 37/41 | 37 |
| **All** | **136** | **132/136** | **132** |

## Eligibility

| Raw agreement | Cohen's kappa |
|---:|---:|
| 0.971 | 0.000 |

## Single-Label Fields Among Jointly Included Records

| Field | Raw agreement | Cohen's kappa |
|---|---:|---:|
| primary_shape | 0.932 | 0.906 |
| principal_evidence | 0.758 | 0.658 |
| external_traceability | 0.773 | 0.262 |

## Multi-Label Fields Among Jointly Included Records

| Field | Row exact | Mean row Jaccard | Micro F1 |
|---|---:|---:|---:|
| lifecycle | 0.258 | 0.716 | 0.821 |
| capability | 0.280 | 0.776 | 0.873 |

## Files

- `data/final_multisource_search_20260730_all_coder_comparison.csv` preserves eligibility and label differences.
- `data/final_multisource_search_20260730_all_per_label_reliability.csv` reports binary per-label agreement among jointly included records.

No disagreement is automatically resolved by this script.
