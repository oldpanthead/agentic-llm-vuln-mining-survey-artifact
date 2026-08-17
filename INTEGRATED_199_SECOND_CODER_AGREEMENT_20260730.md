# Integrated 199-Study Independent-Coder Agreement

The calculation combines the released 67-study review with 132 studies jointly included from the final multi-source search. Both cohorts use the same controlled label vocabulary. This report records independent assignments before adjudication; source assignments remain separate, and it does not score claim-boundary prose by exact textual agreement. Final descriptive distributions are reported separately from the adjudicated matrix.

## Coverage

| Cohort | Target-software studies |
|---|---:|
| Released study set | 67 |
| Final multi-source search | 132 |
| **Integrated set** | **199** |

## Single-Label Fields

| Field | Raw agreement | Cohen's kappa |
|---|---:|---:|
| primary shape | 0.884 | 0.843 |
| principal evidence | 0.759 | 0.665 |
| external traceability | 0.724 | 0.448 |

## Multi-Label Fields

| Field | Row exact | Mean row Jaccard | Micro F1 |
|---|---:|---:|---:|
| lifecycle | 0.261 | 0.726 | 0.831 |
| capability | 0.312 | 0.782 | 0.874 |

## Interpretation Boundary

Eligibility agreement for the new search is reported separately because the released 67-study set had already passed inclusion before its unified second-coder review. The integrated reliability result therefore covers analytical coding fields only.

## Audit Files

- `data/integrated_199_second_coder_comparison_20260730.csv`
- `data/integrated_199_per_label_reliability_20260730.csv`
- `data/integrated_199_label_substitution_sensitivity_20260730.csv`
- `adjudication/adjudication_form_199_all_disagreements_20260812.completed_human_review.csv`
- `data/adjudication_log_199_all_fields.csv`
- `data/adjudicated_study_level_coding_matrix_199.csv`
