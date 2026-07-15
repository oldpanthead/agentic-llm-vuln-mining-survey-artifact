# Final Harmonization and Artifact Closure Report

## Scope

This closure pass synchronizes the public artifact with the current ACM CSUR manuscript after canonical-study deduplication, recall-recovery integration, and coding-round harmonization. It does not add literature, rerun search, overwrite frozen author/coder2 files, create a synthetic combined kappa, or treat AI-assisted tools as an independent human coder.

## Public Release Pointer

- Repository: `oldpanthead/agentic-llm-vuln-mining-survey-artifact`
- Submission tag: `csur-submission-2026-07`
- Public-main final commit SHA: reported in the submission handoff/final response after this closure report is committed and pushed. A commit cannot embed its own final SHA without changing that SHA.
- Tag status: `csur-submission-2026-07` marks the prior synchronized submission baseline; this repair pass does not move the tag unless explicitly retagged.

## Corpus Counts

- Source records: 253
- Canonical candidate studies: 248
- Study-level coded records: 68, consisting of 67 target-software studies plus one governance boundary case
- Extended-synthesis studies: 65
- Background/reference records: 95
- Canonical excluded near-neighbor studies: 20
- Product-ecosystem snapshot rows: 23, maintained as an independent boundary layer

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
4. The 41-record recall-recovery blind pass remains reported by field: layer 40/41, kappa = 0.844; primary shape 27/41, kappa = 0.514; strongest evidence 28/41, kappa = 0.566; external traceability 25/41, kappa = 0.320; lifecycle exact 4/41, mean Jaccard = 0.667, micro F1 = 0.794; capability exact 9/41, mean Jaccard = 0.760, micro F1 = 0.865.
5. Harmonized lifecycle, capability, and shape labels are author-confirmed descriptive recodings and were not independently re-coded in a change-only human reliability pass.
6. No AI output is treated as an independent human coding decision.
7. No synthetic combined kappa is generated or claimed.

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

The search protocol is titled around the `Submission-Time arXiv Sensitivity and Recall-Recovery Search` and records that the historical ledger was multi-source and narrower, the recall-recovery pass was broader and arXiv-only, 432 unique records were screened, 41 reached full-text review, 37 entered study-level coding, four entered extended synthesis, no new evidence-output category was required, and the four dominant comparison shapes remained stable.

## Validation Result

`python reproduce_tables.py` exits with code 0 in standalone public-artifact mode. A GitHub fresh clone of public `main` after this repair pass also ran `python reproduce_tables.py` with exit code 0; the exact final pushed SHA is reported in the submission handoff/final response. `python reproduce_tables.py --manuscript <path-to-main_acm_csur.tex>` exits with code 0 when the manuscript source is available. The script checks canonical counts, source/canonical separation, no cross-layer canonical overlap, second-coder reports, recall-recovery agreement values, harmonized matrix size and controlled vocabulary, round-specific shape and evidence counts, harmonization evidence bases, repository-local artifact-path manifest entries, optional manuscript `\path{}` entries, and tracked-file security boundaries.

The current PDF compiles to 33 pages. The LaTeX log reports no undefined citations, no undefined references, no overfull boxes, and no rerun request. Remaining warnings are underfull box/caption warnings typical of dense survey tables. Rendered-page checks covered pages 14, 15, 18, 19, 22, 23, and 28; no large internal whitespace bands were detected on those pages after the float-placement repairs.

## Public-Artifact Sync Requirements

After this report is committed and pushed, public main should expose the current artifact files. The final handoff should record the pushed main commit SHA, the `csur-submission-2026-07` tag status, and the public fresh-clone `python reproduce_tables.py` exit code.
