# Unified Second-Coder Pre-Adjudication Report

## Scope

The unified review covers all 67 target-software studies plus the governance boundary case under one frozen codebook. Reliability metrics below use the 67 target-software studies; the governance boundary case was reviewed where applicable but remains outside target-software distribution denominators. Claim-boundary text was reviewed for all 68 records but is not assigned an artificial exact-match statistic.

## Field-Specific Agreement Before Adjudication

| Field | Scope | Result |
|---|---:|---|
| Lifecycle coverage | 67 | exact = 18/67 = 0.269; mean row Jaccard = 0.746; micro F1 = 0.848 |
| Cross-stage capability | 67 | exact = 25/67 = 0.373; mean row Jaccard = 0.793; micro F1 = 0.877 |
| Primary system shape | 67 | raw agreement = 53/67 = 0.791; Cohen's kappa = 0.720 |
| Strongest evidence output | 67 | raw agreement = 51/67 = 0.761; Cohen's kappa = 0.665 |
| External traceability | 67 | raw agreement = 41/67 = 0.612; Cohen's kappa = 0.463 |

## Review Actions

| Field | Confirm | Revise | Newly code |
|---|---:|---:|---:|
| Lifecycle coverage | 37 | 0 | 31 |
| Cross-stage capability | 41 | 26 | 1 |
| Primary system shape | 33 | 4 | 31 |
| Strongest evidence output | 58 | 10 | 0 |
| External traceability | 43 | 25 | 0 |
| Claim boundary | 34 | 3 | 31 |

The disagreement file contains 147 field-level rows. These are pre-adjudication differences; no consensus or post-adjudication reliability is claimed.

## Label-Substitution Sensitivity

The complete count comparison is available in `data/unified_second_coder_label_substitution_sensitivity.csv`. Reproducible validation (31/67), candidate judgment (6/67), controlled task completion (13/67), and the feedback-driven fuzzing shape (17/67) are unchanged under second-coder substitution. Feedback interpretation and validation organization remain common, and governance control remains uncommon. Exact counts for external traceability, failure reuse, reporting/audit coverage, and tool routing are more boundary-sensitive and are therefore interpreted directionally in the manuscript.

## Provenance

The second coder was allowed to reuse and reconsider their own earlier labels, but did not receive author or harmonized row-level labels before completing the unified review. Every row records reviewed material and a decision note. Original historical second-coder files remain unchanged.
