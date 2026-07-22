# Final Harmonization and Artifact Closure Report

## Scope

This closure pass synchronizes the public artifact with the current ACM CSUR manuscript after canonical-study deduplication, recall-recovery integration, coding-round harmonization, and the 2026-07-16 official-source follow-up check. The literature set, frozen author/coder2 files, round-specific reliability reports, and human-coder boundaries are preserved for auditability.

## Public Release Pointer

- Repository: `oldpanthead/agentic-llm-vuln-mining-survey-artifact`
- Official-source follow-up: 2026-07-16, with final metadata verification on 2026-07-22; no corpus-count changes
- Submission tag: `csur-submission-2026-07-final-v3`.
- Final artifact sync adds the representative reported-results audit file, the target-only sensitivity scopes, and official-source follow-up naming without changing corpus counts or coding metrics.

## Corpus Counts

- Source records: 253
- Canonical candidate studies: 248
- Study-level coded records: 68, consisting of 67 target-software studies plus one governance boundary case
- Extended-synthesis studies: 65
- Background/reference records: 95
- Canonical excluded near-neighbor studies: 20
- Product-ecosystem snapshot rows: 23, maintained as an independent boundary layer
- Official-source follow-up: no new canonical candidate, study-level coded, extended-synthesis, background, or excluded records

## Harmonization Changes

The author-confirmed harmonization audit contains 408 field rows for 68 study-level coded records. Substantive harmonization changed 25 records and 39 field entries:

- `lifecycle_coverage`: 15 changed field entries
- `cross_stage_capabilities`: 24 changed field entries
- `primary_system_shape`: no substantive label changes; schema normalization separates primary shape from overlay tags
- `strongest_evidence_output`: no substantive changes in the harmonization pass
- `external_traceability`: no substantive changes in the harmonization pass

Label-level changes computed from `data/coding_round_harmonization_audit.csv`:

- Lifecycle additions: candidate analysis +7, execution observation +7, path and input exploration +1, reporting and audit +1
- Lifecycle removals: none
- Capability additions: context aggregation / rule extraction +17, tool routing / strategy routing +14, feedback interpretation / loop adjustment +9, validation organization / evidence packaging +5, long-horizon state management +1
- Capability removals: role discussion / textual reflection -1, preserved only as legacy notes where applicable
- Unresolved harmonization fields: 0

Every substantive change has a recorded evidence basis and author-confirmed status.

## Reliability Boundary

The current reliability result applies one frozen codebook to the complete study-level set, while the harmonized matrix remains the source of descriptive manuscript counts.

1. The unified independent review covers all 67 target-software studies plus the governance boundary case; target-software reliability uses the 67-study denominator.
2. Lifecycle coverage reached exact agreement 18/67 = 0.269, mean row Jaccard = 0.746, and micro F1 = 0.848.
3. Cross-stage capability reached exact agreement 25/67 = 0.373, mean row Jaccard = 0.793, and micro F1 = 0.877.
4. Primary system shape reached raw agreement 53/67 = 0.791 and Cohen's kappa = 0.720; strongest evidence output reached 51/67 = 0.761 and kappa = 0.665; external traceability reached 41/67 = 0.612 and kappa = 0.463.
5. The harmonized matrix supplies descriptive counts, and the complete independent label-substitution table supplies the sensitivity view. No consensus labels, synthetic combined kappa, or post-adjudication reliability are claimed.
6. Historical 31-record and 41-record files remain preserved as codebook-development and provenance records.
7. No AI output is treated as an independent human coding decision.

## Controlled System-Shape Vocabulary

The current controlled primary-shape vocabulary is:

- Candidate-analysis systems
- Feedback-driven fuzzing agents
- Reproduction-, validation-, and repair-centered agents
- Long-horizon pentest and CRS agents
- Governance boundary case, excluded from target-software denominators

Conceptual overlaps remain possible, but each target-software coded study receives one dominant primary shape for descriptive counting. Overlay tags preserve additional characteristics such as multi-agent orchestration, iterative optimization, failure-memory reuse, and governance control without entering the primary-shape denominator.

## Manuscript Closure

The manuscript has been updated to:

- report one complete-study-set independent review and its label-substitution sensitivity;
- use four dominant comparison shapes rather than a three-shape-plus-cross-cutting formulation;
- use the formal reproduction-, validation-, and repair-centered shape name;
- keep table legends as notes rather than data cells; the recompiled PDF no longer contains the bad `Reproducible validation, not external confirmation Legend.` string;
- place the research-agenda table after a complete introduction sentence and keep the `Trustworthy Agentic...` paragraph after the table; the recompiled PDF no longer contains the split `reporting requirements. Trustworthy` string;
- update the conclusion to use recall-recovery and author-confirmed harmonized-label wording.

## Artifact Closure

The public artifact now includes and validates:

- `data/current_study_level_coding_matrix_harmonized.csv`
- `data/coding_round_harmonization_audit.csv`
- `data/current_synthesis_statistics_by_round.csv`
- `CODING_ROUND_HARMONIZATION_REPORT.md`
- `unified_second_coder_codebook.md`
- `data/unified_second_coder_final_blind_template.csv`
- `data/unified_second_coder_final_results.csv`
- `data/unified_second_coder_pre_adjudication_disagreements.csv`
- `data/unified_second_coder_label_substitution_sensitivity.csv`
- `reports/UNIFIED_SECOND_CODER_PRE_ADJUDICATION_REPORT.md`
- `data/empirical_reporting_extraction.csv`
- `data/empirical_reporting_completeness.csv`
- `data/publication_status_sensitivity_analysis.csv`
- `data/representative_reported_results.csv`
- `README.md`, `ARTIFACT_INDEX.md`, `RELEASE_MANIFEST.md`, `SEARCH_PROTOCOL.md`, `data_dictionary.md`, `public_release_checklist.md`, and `reproduce_tables.py`

The search protocol records the submission-time arXiv recall-recovery search and records that the historical ledger was multi-source and narrower, the recall-recovery pass was broader and arXiv-only, 432 unique records were screened, 41 reached full-text review, 37 entered study-level coding, four entered extended synthesis, no new evidence-output category was required, and the four dominant comparison shapes remained stable. The artifact also includes `OFFICIAL_SOURCE_FOLLOWUP_REPORT.md`, `data/official_source_followup_20260716_search_log.csv`, and `data/official_source_followup_20260716_screening_audit.csv`; these files record that official-source follow-up checks matched PANGOLIN and FirmAgent to already integrated canonical records and introduced no corpus-count changes.

## Validation Result

`python reproduce_tables.py` exits with code 0 in standalone public-artifact mode. `python reproduce_tables.py --manuscript <path-to-main_acm_csur.tex>` additionally validates manuscript `\path{}` entries when the manuscript source is available. The script checks canonical counts, source/canonical separation, no cross-layer canonical overlap, official-source follow-up files, historical provenance, unified second-coder completion and agreement values, label-substitution sensitivity, harmonized matrix size and controlled vocabulary, repository-local artifact-path entries, optional manuscript paths, and tracked-file security boundaries.

The current PDF compiles to 33 pages. The LaTeX log reports no undefined citations, no undefined references, no overfull boxes, and no rerun request after the final local compile. Remaining warnings are underfull box/caption warnings typical of dense survey tables. Tables 1--13 remain in the manuscript, and Table 13 preserves all four system-shape groups. Final metadata verification reconciled PANGOLIN with its official USENIX Security 2026 publication page without changing analytical counts or evidence coding.

## Public-Artifact Snapshot

The synchronized public snapshot is identified by the `csur-submission-2026-07-final-v3` tag. Standalone artifact validation and optional manuscript-path validation are recorded above.
