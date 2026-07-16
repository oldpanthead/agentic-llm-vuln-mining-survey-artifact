# Final Harmonization and Artifact Closure Report

## Scope

This closure pass synchronizes the public artifact with the current ACM CSUR manuscript after canonical-study deduplication, recall-recovery integration, coding-round harmonization, and the 2026-07-16 official-source follow-up check. The literature set, frozen author/coder2 files, round-specific reliability reports, and human-coder boundaries are preserved for auditability.

## Public Release Pointer

- Repository: `oldpanthead/agentic-llm-vuln-mining-survey-artifact`
- Official-source follow-up: 2026-07-16; no corpus-count changes
- Submission tag: `csur-submission-2026-07-final`.
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

Frozen-label reliability and harmonized-label descriptive synthesis are intentionally separated.

1. Frozen initial-round labels and independent-coder labels remain preserved in the `core31_*` files and associated reports.
2. The frozen initial strongest-evidence-output check remains 28/31 agreements, raw agreement = 0.903, Cohen's kappa = 0.860.
3. The frozen initial capability/traceability extension remains reported with set-style metrics: capability exact = 0.645, mean Jaccard = 0.772, micro F1 = 0.857; external traceability exact/Jaccard = 0.839.
4. The adopted tightened-boundary 41-record recall-recovery blind rerun is reported by field: layer 40/41, kappa = 0.844; primary shape 26/41, kappa = 0.513; strongest evidence 28/41, kappa = 0.551; external traceability 28/41, kappa = 0.420; lifecycle exact 7/41, mean Jaccard = 0.666, micro F1 = 0.783; capability exact 11/41, mean Jaccard = 0.772, micro F1 = 0.872.
5. Harmonized lifecycle, capability, and shape labels are author-confirmed descriptive recodings with round-specific reliability provenance.
6. No AI output is treated as an independent human coding decision.
7. Reliability remains reported by coding round.

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

- state the frozen-label versus harmonized-label reliability boundary;
- use four dominant comparison shapes rather than a three-shape-plus-cross-cutting formulation;
- use the formal reproduction-, validation-, and repair-centered shape name;
- keep Table 7 legend text as a table note rather than a data cell; the recompiled PDF no longer contains the bad `Reproducible validation, not external confirmation Legend.` string;
- place Table 14 after a complete introduction sentence and keep the `Trustworthy Agentic...` paragraph after the table; the recompiled PDF no longer contains the split `reporting requirements. Trustworthy` string;
- update the conclusion to use recall-recovery and author-confirmed harmonized-label wording.

## Artifact Closure

The public artifact now includes and validates:

- `data/current_study_level_coding_matrix_harmonized.csv`
- `data/coding_round_harmonization_audit.csv`
- `data/current_synthesis_statistics_by_round.csv`
- `CODING_ROUND_HARMONIZATION_REPORT.md`
- `README.md`, `ARTIFACT_INDEX.md`, `RELEASE_MANIFEST.md`, `SEARCH_PROTOCOL.md`, `data_dictionary.md`, `public_release_checklist.md`, and `reproduce_tables.py`

The search protocol records the submission-time arXiv recall-recovery search and records that the historical ledger was multi-source and narrower, the recall-recovery pass was broader and arXiv-only, 432 unique records were screened, 41 reached full-text review, 37 entered study-level coding, four entered extended synthesis, no new evidence-output category was required, and the four dominant comparison shapes remained stable. The artifact also includes `OFFICIAL_SOURCE_FOLLOWUP_REPORT.md`, `data/official_source_followup_20260716_search_log.csv`, and `data/official_source_followup_20260716_screening_audit.csv`; these files record that official-source follow-up checks matched PANGOLIN and FirmAgent to already integrated canonical records and introduced no corpus-count changes.

## Validation Result

`D:\Anaconda3\python.exe reproduce_tables.py` exits with code 0 in standalone public-artifact mode. The script remains public-clone compatible: `python reproduce_tables.py` requires only that `python` resolve to a real Python interpreter. `python reproduce_tables.py --manuscript <path-to-main_acm_csur.tex>` additionally validates manuscript `\path{}` entries when the manuscript source is available. The script checks canonical counts, source/canonical separation, no cross-layer canonical overlap, official-source follow-up closure files, second-coder reports, recall-recovery agreement values, harmonized matrix size and controlled vocabulary, round-specific shape and evidence counts, harmonization evidence bases, repository-local artifact-path manifest entries, optional manuscript `\path{}` entries, and tracked-file security boundaries.

The current PDF compiles to 36 pages after adding the representative Appendix B reported-results table. The LaTeX log reports no undefined citations, no undefined references, no overfull boxes, and no rerun request after the final local compile. Remaining warnings are underfull box/caption warnings typical of dense survey tables. Rendered-page checks covered pages 14, 15, 18, 19, 22, 23, and 28; no large internal whitespace bands were detected on those pages after the float-placement repairs.

## Public-Artifact Sync Requirements

After this report is committed and pushed, public main should expose the current artifact files. The final handoff should record the pushed main commit SHA, the `csur-submission-2026-07-final` tag status, and the standalone artifact validation exit code.


