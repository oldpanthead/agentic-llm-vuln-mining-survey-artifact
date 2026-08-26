# Artifact Index

## Validation Entry Point

- `reproduce_tables.py`: standalone validation of the integrated search, reconciliation, analytical layers, study-level distributions, primitive extraction, and complete second-coder files.
- `manuscript_artifact_paths.txt`: repository-relative paths promised by the manuscript.

Expected current counts: 1,785 source records; 1,772 studies after version reconciliation; 199 target-software studies; 154 adjacent records retained for evidence or contextual mapping; 668 background/reference studies; 751 exclusions; and 13 alternate versions or source variants. AgentFuzz is retained in the adjacent evidence layer as governance and agent-safety context rather than as a separate analytical stratum.

## Integrated Search

- `FINAL_MULTISOURCE_SEARCH_PROTOCOL_20260730.md`: protocol and source-access boundaries.
- `FINAL_MULTISOURCE_SEARCH_AND_PRISMA_20260730.md`: manuscript-facing integrated PRISMA-ScR allocation with source-specific acquisition provenance.
- `data/final_multisource_search_20260730_access_log.csv`: query attempts, interfaces, timestamps, status, and raw export paths.
- `data/final_multisource_search_20260730_results.csv`: 12,090 saved source occurrences.
- `data/final_multisource_search_20260730_source_counts.csv`: source-interface occurrence totals.
- `data/final_multisource_search_20260730_screening_audit.csv`: deterministic triage for 1,642 unique interface records.
- `data/final_multisource_search_20260730_fulltext_assessment.csv`: retrieval and assessment evidence from the eligibility workflow.
- `data/final_multisource_search_20260730_complete_screening.csv`: frozen final screening and analytical-allocation audit for all 1,642 records.
- `data/final_multisource_exclusion_summary.csv`: stage-level closure of the 751 excluded studies.
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
- `data/publication_status_distribution_by_layer.csv`: publication-status-stratified evidence and shape counts.
- `unified_second_coder_codebook.md`: controlled coding definitions and boundary rules.
- `evidence_output_codebook.md`: principal evidence-output labels.

## Complete Independent Review

- `data/integrated_199_second_coder_comparison_20260730.csv`: complete field comparison.
- `data/integrated_199_per_label_reliability_20260730.csv`: lifecycle and capability label-level reliability, including Gwet's AC1.
- `data/integrated_199_reporting_audit_disagreement_review.csv`: reporting/audit disagreement directions and boundary basis.
- `data/integrated_199_label_substitution_sensitivity_20260730.csv`: full-label substitution counts.
- `INTEGRATED_199_SECOND_CODER_AGREEMENT_20260730.md`: report used by the manuscript.
- `data/final_multisource_search_20260730_all_coder_comparison.csv`: detailed comparison for newly reviewed records.
- `third_party_rereview_oy_20260824.csv`: raw OY export for 410 disagreement and 50 QC tasks.
- `data/third_party_rereview_decisions_20260824.csv` and `data/third_party_rereview_qc_20260824.csv`: final decision and separate QC layers; these supersede the earlier completed form.
- `data/adjudication_log_199_all_fields.csv`: final audit log covering 995 study-field assignments.
- `data/adjudicated_synthesis_statistics_199.csv` and `data/adjudication_completion_manifest.json`: final descriptive statistics and completion metadata.
- `ADJUDICATION_COMPLETION_20260812.md`: fixed rules and reporting boundary.

## Supplementary Extractions

- `data/traditional_security_primitives.csv`: 199-study RQ1 extraction with source locations.
- `data/traditional_security_primitives_by_use_role.csv`, `data/traditional_security_primitive_use_role_counts.csv`, and `data/traditional_security_primitive_by_output.csv`: workflow-active/evaluation role split and output co-occurrence.
- `data/target_domain_extraction.csv`, `data/target_domain_by_principal_output.csv`, and `data/publication_year_by_primary_shape.csv`: target-domain and year cross-tabs used in the study-level figure.
- `data/public_artifact_availability.csv` and `data/principal_output_by_public_artifact_availability.csv`: located public artifact indicators by output.
- `data/training_data_overlap_control.csv` and `data/training_data_overlap_control_counts.csv`: training-overlap control reporting audit.
- `data/mapping_snapshot_counts.csv`: source-record composition and current study-level distribution snapshot referenced by the manuscript.
- `data/publication_status_sensitivity_analysis.csv`: publication-status robustness counts for the 199-study set.
- `data/controlled_task_only_membership.csv` and `data/controlled_task_only_sensitivity.csv`: the 199 row-level inclusion decisions and mechanically derived 199-versus-164 denominator sensitivity.
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
- `FINAL_HARMONIZATION_AND_ARTIFACT_CLOSURE_REPORT.md`: current closure record.

## Historical Files

Earlier corpus snapshots, July 15/16 search files, 31-record and 41-record coding checks, and 67-study review files remain in the tagged source repository for provenance. The clean public export retains only the frozen pre-final matrix required by the current validator. Historical files must not be interpreted as current counts or current manuscript-facing results.
