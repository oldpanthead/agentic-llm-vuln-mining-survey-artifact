# Submission Update Canonical Integration Report

## Scope

This report compares the 41 author-confirmed update-search records with the current source-record corpus and canonical study/version crosswalk. It uses exact arXiv IDs, DOI identifiers, normalized titles, and conservative title-similarity review. The assessment does not modify the frozen corpus or manuscript.

## Match Outcome

- Update records assessed: 41
- New canonical studies: 41
- Existing-study or alternate-version matches: 0
- Manual-review matches: 0
- New study-level coded candidates after this pass: 37
- New extended-synthesis studies after this pass: 4

No exact arXiv-ID, DOI, URL-derived arXiv-ID, or normalized-title match was found against the existing 212 source records. The highest title similarities are retained in `data/submission_update_20260715_canonical_integration_crosswalk.csv` for inspection; similarities below 0.80 are treated as topical naming overlap rather than version identity.

## Current and Projected Counts

| Analytical view | Current frozen count | Projected after canonical integration |
|---|---:|---:|
| Source records | 212 | 253 |
| Canonical candidate studies | 207 | 248 |
| Study-level coded records, including the governance boundary case | 31 | 68 |
| Extended-synthesis studies | 61 | 65 |
| Background/reference studies | 95 | 95 |
| Excluded near-neighbor studies | 20 | 20 |

The projected study-level total is 67 target-software studies plus the existing governance boundary case. These projected counts must not be used in the manuscript until corpus rows, canonical crosswalks, coding matrices, descriptive distributions, and manuscript tables are updated together.

## Manual Review

No unresolved canonical-identity match exceeded the 0.80 manual-review threshold.


## Integration Boundary

The 37/4 analytical-layer decision is final for the update cohort, but canonical corpus integration remains a separate release operation. The existing 31-record second-coder statistics continue to describe the frozen 30-target-study-plus-one-governance set; the update cohort has its own pre-adjudication agreement report. No combined reliability statistic is inferred from the two rounds.
