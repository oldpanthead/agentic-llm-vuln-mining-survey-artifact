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

Detailed coding boundaries are defined in `codebook.md`.

## Search And Screening Files

| File | Unit | Purpose and key fields |
|---|---|---|
| `data/final_multisource_search_20260730_access_log.csv` | Query attempt | Source/interface, query, timestamp, status, raw-file identifier, and returned count. |
| `data/final_multisource_search_20260730_results.csv` | Saved source occurrence | Query provenance plus title, authors, abstract, venue, DOI, arXiv ID, URL, and record type. |
| `data/derived_summary_tables.json` | Derived table bundle | Machine-readable derived summaries listed below, retained with original table names, columns, and rows. |
| `data/final_multisource_search_20260730_screening_audit.csv` | Deduplicated discovery record | Title/abstract triage, existing-record match, full-text status, final layer, canonical study, and notes. |
| `data/final_multisource_search_20260730_complete_screening.csv` | Frozen screened record | Screening stage, final analytical layer, decision basis, counting status, and coder provenance. |
| `data/final_multisource_search_20260730_fulltext_assessment.csv` | Report sought | Access, assessment, version, author decision, and confirmation status. |
| `data/final_multisource_search_20260730_prisma_counts.csv` | Flow metric | Manuscript-facing integrated flow and source-specific provenance counts. |
| `data/final_multisource_search_20260730_dedup_resolutions.csv` | Candidate record pair | Match basis, title similarity, audit decision, and provenance. |

## Corpus And Coding Files

| File | Unit | Purpose and key fields |
|---|---|---|
| `data/corpus.csv` | Source record | Bibliographic ledger with legacy corpus layer, task category, exclusion reason, and note. |
| `data/study_version_crosswalk.csv` | Source record | Mapping to canonical study and record, version type, counting status, and deduplication basis. |
| `data/adjudicated_study_level_coding_matrix_199.csv` | Target-software study | Final 199-row third-review adjudicated matrix used for descriptive distributions. |
| `data/current_study_level_coding_matrix_harmonized.csv` | Target-software study | Preserved primary author matrix covering lifecycle, output, traceability, claim boundary, shape, and capabilities before adjudication. |
| `data/current_study_level_coding_matrix_harmonized_pre_final_multisource_20260730.csv` | Historical target-software study | Frozen pre-final matrix used only for provenance and cohort-stability checks. |
| `data/extended_synthesis_audit.csv` | Extended-synthesis study | Material basis, synthesis role, RQ contribution, manuscript use, and reason for not entering study-level coding. |
| `data/reference_audit.csv` | Reference record | Canonical title, publication status, venue, verified URL, DOI/arXiv ID, and citation key. |
| `data/final_multisource_new_study_reference_metadata_20260730.csv` | Newly integrated reference | Selected source metadata and selection basis for the 132 newly integrated study-level records. |
| `references_final_multisource_new_studies_20260730.bib` | BibTeX entry | Bibliographic export corresponding to newly integrated study-level records. |

Legacy `Core`, `Supporting`, `Background`, and `Excluded` values remain in `corpus.csv` for source-record provenance. Current manuscript denominators are determined from the version crosswalk and harmonized study-level/extended-synthesis files.

## Descriptive And Supplementary Extractions

| File | Unit | Purpose and key fields |
|---|---|---|
| `data/publication_status_standardized.csv` | Target-software study | Standardized publication status with output, shape, capabilities, and traceability. |
| `data/traditional_security_primitives.csv` | Target-software study | Controlled primitive tags, named tools, source location, and extraction note. |
| `data/traditional_security_primitives_by_use_role.csv` | Study--primitive pair | Workflow-active/evaluation-support role and assignment basis. |
| `data/target_domain_extraction.csv` | Target-software study | Source-located target domain, shape, output, year, and extraction basis. |
| `data/public_artifact_availability.csv` | Target-software study | Located implementation, build, strict system-generated public trigger/replay, trace, and patch indicators. A repository or benchmark input is not itself a trigger/replay artifact. |
| `data/public_trigger_replay_evidence_index.csv` | Reviewed trigger/replay candidate | The 14 initially located candidates, their inclusion decision, local PDF locator, and reason. Only an item recorded as included enters Table 10's trigger/replay column. |
| `data/controlled_task_only_membership.csv` | Target-software study | Reproducible 199-row membership decision, reason, and source-located domain basis for the 35-study denominator sensitivity cohort. |
| `data/public_alignment_evidence_index.csv` | Public-alignment case | Local evidence chain for all four publicly aligned external-trace cases, including QRS. |
| `data/training_data_overlap_control.csv` | Target-software study | Reporting status, source location, evidence note, and audit scope. |
| `data/derived_summary_tables.json` | Derived table bundle | Includes source counts, exclusion summary, adjudicated statistics, publication-status distributions and sensitivity, primitive role/output tables, unspecified-primitive closure rows, domain/output and year/shape cross-tabs, artifact summaries, controlled-task sensitivity, training-overlap counts, and mapping snapshots. |
| `data/final_multisource_cohort_stability.csv` | Cohort-by-label row | Provenance-only count and share across historical acquisition groups. |
| `data/representative_system_mechanisms.csv` | Representative system | Model, runtime, state/feedback, workflow endpoint, source location, and note. |
| `data/mechanism_cost_ablation_synthesis.csv` | Reported observation | Cost, ablation, or recovery observation with original unit/comparison and source location. |
| `data/representative_reported_results.csv` | Representative system | Evaluation setting, reported result, validation material, and source location. |
| `data/product_ecosystem_snapshot.csv` | Public product material | Independent product-ecosystem context outside research-study denominators. |

## Independent Coding Files

| File | Unit | Purpose and key fields |
|---|---|---|
| `data/final_multisource_search_20260730_all_coder_comparison.csv` | Newly reviewed record | First/second assignments for eligibility, shape, output, traceability, lifecycle, and capabilities. |
| `data/integrated_199_second_coder_comparison_20260730.csv` | Target-software study | Complete first/second assignment comparison for all controlled fields. |
| `data/integrated_199_per_label_reliability_20260730.csv` | Controlled label | Positive counts, raw agreement, Cohen's kappa, Gwet's AC1, and interpretation note. |
| `data/integrated_199_reporting_audit_disagreement_review.csv` | Reporting/audit disagreement | Direction, assignments, and source-linked boundary basis. |
| `data/integrated_199_label_substitution_sensitivity_20260730.csv` | Controlled label | First-coder and complete coder-substitution counts and difference. |
| `third_party_rereview_oy_20260824.csv` | Rereview task | Raw OY export for 410 disagreement tasks and 50 hidden-reference QC tasks. |
| `data/third_party_rereview_decisions_20260824.csv` | Disagreement | OY decision, rationale, locator, task/case/study/field identity, material path and SHA-256, integration provenance, and five `prior_form_*` columns carrying the corresponding historical completed-form values for all 410 disagreements. This is the consolidated decision/provenance file; the historical form is not distributed as a second copy. |
| `data/third_party_rereview_qc_20260824.csv` | QC task | Fifty rule-application checks with the same task/material identity fields, retained separately from final decisions and reliability statistics. |
| `data/third_party_rereview_material_crosswalk_20260824.csv` | Corrected case material | Identity correction and SHA-256 record for A104, A139, A011, and A137. |
| `data/adjudication_log_199_all_fields.csv` | Study-field assignment | Full adjudication audit log for all 995 controlled study-field assignments. |
| `data/adjudication_completion_manifest.json` | Adjudication run | Inputs, outputs, disagreement count, unresolved count, and field reportability. |

Final descriptive distributions use the adjudicated matrix. Independent assignments and substitution results remain separate as pre-adjudication reliability and sensitivity records; the adjudicated matrix is not a new reliability test.

## Validation

`reproduce_tables.py` verifies manifest completeness, the completed 410-row adjudication record, the final matrix and statistics, unique headers, expected denominators, controlled distributions, search/reconciliation arithmetic, supplementary extraction closure, publication-status stratification, and complete pre-adjudication second-coder statistics. It exits with `VALIDATION_OK` only when all checks pass.
