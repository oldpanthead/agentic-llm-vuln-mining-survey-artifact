# Artifact Index

## Validation Entry Point

- `reproduce_tables.py`: standalone validation of the integrated search, reconciliation, analytical layers, study-level distributions, primitive extraction, and complete second-coder files.
- `manuscript_artifact_paths.txt`: repository-relative paths promised by the manuscript.

Expected current counts: 1,785 source records; 1,772 studies after version reconciliation; 199 target-software studies; 154 adjacent records retained for evidence or contextual mapping; 668 background/reference studies; 751 exclusions; and 13 alternate versions or source variants. AgentFuzz is retained in the adjacent evidence layer as governance and agent-safety context rather than as a separate analytical stratum.

## Integrated Search

- `FINAL_MULTISOURCE_SEARCH_AND_PRISMA_20260730.md`: integrated PRISMA-ScR allocation, source-specific acquisition provenance, and the final search protocol.
- `data/final_multisource_search_20260730_access_log.csv`: query attempts, interfaces, timestamps, status, and raw export paths.
- `data/final_multisource_search_20260730_results.csv`: 12,090 saved source occurrences.
- `data/derived_summary_tables.json`: consolidated derived summaries, including source-interface and exclusion counts.
- `data/final_multisource_search_20260730_screening_audit.csv`: deterministic triage for 1,642 unique interface records.
- `data/final_multisource_search_20260730_fulltext_assessment.csv`: retrieval and assessment evidence from the eligibility workflow.
- `data/final_multisource_search_20260730_complete_screening.csv`: frozen final screening and analytical-allocation audit for all 1,642 records.
- `data/final_multisource_search_20260730_prisma_counts.csv`: integrated flow counts and source-specific provenance regenerated from frozen audit files.
- `data/final_multisource_search_20260730_dedup_resolutions.csv`: same-study/version resolutions.

## Corpus and Coding

- `data/corpus.csv`: integrated source-record ledger.
- `data/study_version_crosswalk.csv`: source record to study/version mapping.
- `data/adjudicated_study_level_coding_matrix_199.csv`: final 199-row adjudicated matrix used for descriptive distributions.
- `data/current_study_level_coding_matrix_harmonized.csv`: preserved primary author matrix.
- `data/current_study_level_coding_matrix_harmonized_pre_final_multisource_20260730.csv`: frozen pre-final matrix used for provenance checks.
- `data/extended_synthesis_audit.csv`: 154-study thematic-use audit: 92 records with detailed public material for substantive synthesis and 62 records supporting contextual coverage mapping, including cross-cutting governance context.
- `data/reference_audit.csv`: citation and source-role audit.
- `data/publication_status_standardized.csv`: study-level publication-status assignments.
- `data/derived_summary_tables.json`: publication-status distributions and sensitivity tables.
- `codebook.md`: unified lifecycle, capability, system-shape, principal-output, external-traceability, review, and historical-crosswalk rules.

## Complete Independent Review

- `data/integrated_199_second_coder_comparison_20260730.csv`: complete field comparison.
- `data/integrated_199_per_label_reliability_20260730.csv`: lifecycle and capability label-level reliability, including Gwet's AC1.
- `data/integrated_199_reporting_audit_disagreement_review.csv`: reporting/audit disagreement directions and boundary basis.
- `data/integrated_199_label_substitution_sensitivity_20260730.csv`: full-label substitution counts.
- Integrated independent-coder agreement is included in `ADJUDICATION_COMPLETION_20260812.md`.
- `data/final_multisource_search_20260730_all_coder_comparison.csv`: detailed comparison for newly reviewed records.
- `third_party_rereview_oy_20260824.csv`: raw OY export for 410 disagreement and 50 QC tasks.
- `data/third_party_rereview_decisions_20260824.csv`: consolidated 410-row OY decision layer, including five `prior_form_*` columns that preserve the earlier completed-form values without a duplicate file.
- `data/third_party_rereview_qc_20260824.csv`: separate 50-row QC layer.
- `data/adjudication_log_199_all_fields.csv`: final audit log covering 995 study-field assignments.
- `data/derived_summary_tables.json` and `data/adjudication_completion_manifest.json`: final descriptive statistics and completion metadata.
- `ADJUDICATION_COMPLETION_20260812.md`: fixed rules and reporting boundary.

## Supplementary Extractions

- `data/traditional_security_primitives.csv`: 199-study RQ1 extraction with source locations.
- `data/traditional_security_primitives_by_use_role.csv`: row-level workflow-active/evaluation-support assignments; derived role counts and output co-occurrence are in `data/derived_summary_tables.json`.
- `data/target_domain_extraction.csv`: source-located target-domain extraction; domain-output and year-shape cross-tabs are in `data/derived_summary_tables.json`.
- `data/public_artifact_availability.csv`: row-level located public-artifact indicators; output summaries are in `data/derived_summary_tables.json`.
- `data/training_data_overlap_control.csv`: row-level training-overlap control reporting audit; counts are in `data/derived_summary_tables.json`.
- Mapping snapshots and publication-status sensitivity counts are in `data/derived_summary_tables.json`.
- `data/controlled_task_only_membership.csv`: the 199 row-level inclusion decisions; the mechanically derived 199-versus-164 sensitivity is in `data/derived_summary_tables.json`.
- `data/public_alignment_evidence_index.csv`: item-level local evidence chains for all four publicly aligned external-trace cases, including QRS.
- `data/final_multisource_cohort_stability.csv`: provenance-only comparison of historical acquisition groups under the final schema.
- `data/representative_system_mechanisms.csv`: representative mechanism cases.
- `data/mechanism_cost_ablation_synthesis.csv`: source-located cost, ablation, and recovery observations.
- `data/representative_reported_results.csv`: representative result rows.
- `references_final_multisource_new_studies_20260730.bib`: metadata for newly integrated study-level studies.

## Boundary and Release Files

- `data/product_ecosystem_snapshot.csv`: independent product-ecosystem context.
- `SECURITY_BOUNDARY.md`: excluded sensitive material.
- `RELEASE_MANIFEST.md`: release scope and validation status.
- `data_dictionary.md`: field definitions and historical/current status.
- Closure record is included in `RELEASE_MANIFEST.md`.

## Historical Files

Earlier corpus snapshots, July 15/16 search files, 31-record and 41-record coding checks, and 67-study review files remain in the tagged source repository for provenance. The clean public export retains only the frozen pre-final matrix required by the current validator. Historical files must not be interpreted as current counts or current manuscript-facing results.
