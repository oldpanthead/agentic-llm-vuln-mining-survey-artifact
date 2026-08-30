# Data Dictionary

This dictionary covers the current clean public export. Historical build files retained in the tagged source repository are intentionally excluded.

## Conventions

- CSV files are UTF-8 encoded and contain one header row.
- Blank values mean not reported, not applicable, or not located according to the field context; they must not automatically be interpreted as a negative finding.
- Multi-label lifecycle and capability fields use semicolon-separated controlled labels.
- `record_id` identifies a source record; `canonical_study_id` identifies a version-reconciled study; `matrix_id` identifies a target-software coding row.
- `strongest_evidence_output` is the historical column name for the current principal reported evidence output.
- Counts are descriptive study or source-record counts. They are not pooled causal estimates.

## Controlled Fields

### Primary system shape

- `candidate-analysis system`
- `feedback-driven fuzzing agent`
- `reproduction-, validation-, and repair-centered agent`
- `long-horizon pentest and CRS agent`

### Principal reported evidence output

- `candidate judgment`
- `controlled task completion`
- `runtime safety signal`
- `reproducible validation`
- `externally traceable material`

### External traceability

- `no external trace reported`
- `author-reported external clue`
- `benchmark ground truth / public material`
- `publicly aligned external trace`

### Lifecycle coverage

- `candidate analysis`
- `path and input exploration`
- `execution observation`
- `reproduction and validation`
- `patch validation`
- `reporting and audit`

### Cross-stage capability

- `context aggregation / rule extraction`
- `tool routing / strategy routing`
- `feedback interpretation / loop adjustment`
- `validation organization / evidence packaging`
- `long-horizon state management`
- `failure reuse / strategy update`
- `governance / human gates / disclosure control`

Detailed coding boundaries are defined in `docs/coding/codebook.md`.

## Search And Screening Files

| File | Unit | Purpose and key fields |
|---|---|---|
| `data/search/final_multisource_search_20260730_access_log.csv` | Query attempt | Source/interface, query, timestamp, status, raw-file identifier, and returned count. |
| `data/search/final_multisource_search_20260730_results.csv` | Saved source occurrence | Query provenance plus title, authors, abstract, venue, DOI, arXiv ID, URL, and record type. |
| `data/derived/derived_summary_tables.json` | Derived table bundle | Machine-readable derived summaries listed below, retained with original table names, columns, and rows. |
| `data/search/final_multisource_search_20260730_screening_audit.csv` | Deduplicated discovery record | Title/abstract triage, existing-record match, full-text status, final layer, canonical study, and notes. |
| `data/search/final_multisource_search_20260730_complete_screening.csv` | Frozen screened record | Screening stage, final analytical layer, decision basis, counting status, and coder provenance. |
| `data/search/final_multisource_search_20260730_fulltext_assessment.csv` | Report sought | Access, assessment, version, author decision, and confirmation status. |
| `data/search/final_multisource_search_20260730_prisma_counts.csv` | Flow metric | Manuscript-facing integrated flow and source-specific provenance counts. |
| `data/search/final_multisource_search_20260730_dedup_resolutions.csv` | Candidate record pair | Match basis, title similarity, audit decision, and provenance. |

## Corpus And Coding Files

| File | Unit | Purpose and key fields |
|---|---|---|
| `data/corpus/corpus.csv` | Source record | Bibliographic ledger with legacy corpus layer, task category, exclusion reason, and note. |
| `data/corpus/study_version_crosswalk.csv` | Source record | Mapping to canonical study and record, version type, counting status, and deduplication basis. |
| `data/coding/adjudicated_study_level_coding_matrix_199.csv` | Target-software study | Final 199-row third-review adjudicated matrix used for descriptive distributions. |
| `data/coding/current_study_level_coding_matrix_harmonized.csv` | Target-software study | Preserved primary author matrix covering lifecycle, output, traceability, claim boundary, shape, and capabilities before adjudication. |
| `data/coding/extended_synthesis_audit.csv` | Extended-synthesis study | Material basis, synthesis role, RQ contribution, manuscript use, and reason for not entering study-level coding. |
| `data/corpus/reference_audit.csv` | Reference record | Canonical title, publication status, venue, verified URL, DOI/arXiv ID, citation key, and `new__*` fields for the 132 newly integrated records. |
| `references/references_merged_manuscript.bib` | BibTeX entry | Complete BibTeX file used by the synchronized manuscript, including newly integrated study-level records. |

Legacy `Core`, `Supporting`, `Background`, and `Excluded` values remain in `corpus.csv` for source-record provenance. Current manuscript denominators are determined from the version crosswalk and harmonized study-level/extended-synthesis files.

## Descriptive And Supplementary Extractions

| File | Unit | Purpose and key fields |
|---|---|---|
| `data/synthesis/study_synthesis_199.csv` | Target-software study | One 199-row join keyed by `matrix_id`. Source prefixes preserve the former component views: `pub__` (publication status), `prim__` (primitive extraction), `domain__` (target domain), `artifact__` (public-artifact checks), `task__` (controlled-task membership), and `overlap__` (training-overlap reporting). |
| `data/synthesis/traditional_security_primitives_by_use_role.csv` | Study--primitive pair | Workflow-active/evaluation-support role and assignment basis. |
| `data/synthesis/public_trigger_replay_evidence_index.csv` | Reviewed trigger/replay candidate | The 14 initially located candidates, their inclusion decision, local PDF locator, and reason. Only an item recorded as included enters Table 10's trigger/replay column. |
| `data/synthesis/public_alignment_evidence_index.csv` | Public-alignment case | Local evidence chain for all four publicly aligned external-trace cases, including QRS. |
| `data/derived/derived_summary_tables.json` | Derived table bundle | Includes source counts, exclusion summary, adjudicated statistics, publication-status distributions and sensitivity, primitive role/output tables, unspecified-primitive closure rows, domain/output and year/shape cross-tabs, artifact summaries, controlled-task sensitivity, training-overlap counts, mapping snapshots, and embedded adjudication completion metadata. |
| `data/synthesis/representative_system_mechanisms.csv` | Representative system | Model, runtime, state/feedback, workflow endpoint, source location, and note. |
| `data/synthesis/mechanism_cost_ablation_synthesis.csv` | Reported observation | Cost, ablation, or recovery observation with original unit/comparison and source location. |
| `data/synthesis/representative_reported_results.csv` | Representative system | Evaluation setting, reported result, validation material, and source location. |

## Independent Coding Files

| File | Unit | Purpose and key fields |
|---|---|---|
| `data/search/final_multisource_search_20260730_all_coder_comparison.csv` | Newly reviewed record | First/second assignments for eligibility, shape, output, traceability, lifecycle, and capabilities. |
| `data/adjudication/integrated_199_second_coder_comparison_20260730.csv` | Target-software study | Complete first/second assignment comparison for all controlled fields. |
| `data/adjudication/integrated_199_per_label_reliability_20260730.csv` | Controlled label | Positive counts, raw agreement, Cohen's kappa, Gwet's AC1, and interpretation note. |
| `data/adjudication/integrated_199_reporting_audit_disagreement_review.csv` | Reporting/audit disagreement | Direction, assignments, and source-linked boundary basis. |
| `data/adjudication/third_party_rereview_oy_20260824.csv` | Rereview task | Raw OY export for 410 disagreement tasks and 50 hidden-reference QC tasks. |
| `data/adjudication/third_party_rereview_decisions_20260824.csv` | Disagreement | OY decision, rationale, locator, task/case/study/field identity, material path and SHA-256, integration provenance, and five `prior_form_*` columns carrying the corresponding historical completed-form values for all 410 disagreements. This is the consolidated decision/provenance file; the historical form is not distributed as a second copy. |
| `data/adjudication/third_party_rereview_qc_20260824.csv` | QC task | Fifty rule-application checks with the same task/material identity fields, retained separately from final decisions and reliability statistics. |
| `data/adjudication/third_party_rereview_material_crosswalk_20260824.csv` | Corrected case material | Identity correction and SHA-256 record for A104, A139, A011, and A137. |
| `data/adjudication/adjudication_log_199_all_fields.csv` | Study-field assignment | Full adjudication audit log for all 995 controlled study-field assignments. |
| `data/derived/derived_summary_tables.json` | Adjudication metadata | The `metadata.adjudication_completion_manifest` object records inputs, outputs, disagreement count, unresolved count, and field reportability. |
| `data/adjudication/final_matrix_reapplication_check_tasks_60.csv` | Post-adjudication diagnostic task | OY's completed 300-task reapplication of the five frozen fields on 60 sampled studies, with source locators and excerpts; not an independent replication or accuracy estimate. |
| `data/adjudication/final_matrix_reapplication_check_public_material_60.csv` | Post-adjudication diagnostic descriptor | Binary public-material descriptors for the 60 sampled studies, retained separately from task labels. |
| `data/derived/final_matrix_reapplication_check_summary.csv` | Post-adjudication diagnostic summary | Field-level agreement metrics for the 60-study/300-task check; exact-set agreement, Jaccard, and micro-F1 are descriptive diagnostics only. |
| `docs/review/final_matrix_reapplication_check_README.md` | Diagnostic protocol | Scope, source basis, and interpretation limits for the post-adjudication check. |
| `docs/review/final_matrix_reapplication_check_RULES.md` | Diagnostic rules | Versioned empirical rules used for the completed check. |
| `docs/review/final_matrix_reapplication_check_FREEZE_RECORD.md` | Diagnostic freeze record | Payload freeze and completion record. |
| `docs/review/final_matrix_reapplication_check_SHA256.txt` | Diagnostic integrity record | SHA-256 values for the completed diagnostic payload. |

Final descriptive distributions use the adjudicated matrix. Independent assignments and per-label agreement remain separate as pre-adjudication reliability records; the adjudicated matrix is not a new reliability test.

## Validation

`reproduce_tables.py` verifies compact-manifest completeness, the completed 410-row adjudication record, the final matrix and statistics, unique headers, expected denominators, controlled distributions, search/reconciliation arithmetic, supplementary extraction closure, publication-status stratification, and complete pre-adjudication second-coder statistics. It exits with `VALIDATION_OK` only when all checks pass.
