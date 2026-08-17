# Third-Review Adjudication Completion Record

## Scope

- Study-level denominator: 199 target-software studies.
- Independent field-level disagreements: 410.
- Completed third-review decisions: 410.
- Pending decisions: 0.
- Unresolved decisions: 0.

## Procedure

Two coders independently assigned lifecycle coverage, cross-stage capability, primary system shape, principal reported evidence output, and external traceability. A third reviewer resolved every disagreement against the prespecified codebook and the cited source evidence. The reviewer used anonymized coder X and coder Y labels and did not use aggregate manuscript results to determine individual records.

The review applied the rules in `adjudication/ADJUDICATION_RULES_20260812.md`: operational definitions control; benchmark ground truth is not external confirmation; author-reported CVE, CNVD, vendor, maintainer, or bounty material is an external clue unless a concrete system result aligns with a concrete public external record; multi-label fields retain only explicitly shown labels; and evidence-insufficient cases would have been recorded as unresolved. No unresolved case remained after review.

## Outputs And Reporting Boundary

- `adjudication/adjudication_form_199_all_disagreements_20260812.completed_human_review.csv` is the completed anonymized decision record.
- `data/adjudicated_study_level_coding_matrix_199.csv` is the sole source for final descriptive distributions.
- `data/adjudication_log_199_all_fields.csv` preserves the decision path for all 995 controlled study-field assignments.
- `data/adjudicated_synthesis_statistics_199.csv` provides the final counts and shares.
- `data/current_study_level_coding_matrix_harmonized.csv` and `data/integrated_199_second_coder_comparison_20260730.csv` remain preserved pre-adjudication sources.

Agreement statistics, including raw agreement, Cohen's kappa, and AC1, describe the independent assignments before adjudication. The adjudicated matrix is not a new reliability test.

## Final Key Counts

- Reporting and audit: 78/199.
- Validation organization / evidence packaging: 147/199.
- Externally traceable material as principal output: 6/199.
- Publicly aligned external trace: 7/199.
