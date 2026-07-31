# Artifact Index

## Validation Entry Point

- `reproduce_tables.py`: standalone validation of the integrated search, reconciliation, analytical layers, study-level distributions, primitive extraction, and complete second-coder files.
- `manuscript_artifact_paths.txt`: repository-relative paths promised by the manuscript.

Expected current counts: 1,785 source records; 1,772 studies after version reconciliation; 199 target-software studies; 150 extended-synthesis studies; 670 background/reference studies; 753 exclusions; and 13 alternate versions or source variants. AgentFuzz is retained in extended synthesis as governance and agent-safety context rather than as a separate analytical stratum.

## Integrated Search

- `FINAL_MULTISOURCE_SEARCH_PROTOCOL_20260730.md`: protocol and source-access boundaries.
- `FINAL_MULTISOURCE_SEARCH_AND_PRISMA_20260730.md`: search and PRISMA-ScR summary.
- `data/final_multisource_search_20260730_access_log.csv`: query attempts, interfaces, timestamps, status, and raw export paths.
- `data/final_multisource_search_20260730_results.csv`: 12,090 saved source occurrences.
- `data/final_multisource_search_20260730_source_counts.csv`: source-interface occurrence totals.
- `data/final_multisource_search_20260730_screening_audit.csv`: deterministic triage for 1,642 unique interface records.
- `data/final_multisource_search_20260730_fulltext_assessment.csv`: retrieval and assessment evidence from the eligibility workflow.
- `data/final_multisource_search_20260730_complete_screening.csv`: frozen final screening and analytical-allocation audit for all 1,642 records.
- `data/final_multisource_exclusion_summary.csv`: stage-level closure of the 753 excluded studies.
- `data/final_multisource_search_20260730_prisma_counts.csv`: flow counts regenerated from the frozen final audit and pre-integration baselines.
- `data/final_multisource_search_20260730_dedup_resolutions.csv`: same-study/version resolutions.

## Corpus and Coding

- `data/corpus.csv`: integrated source-record ledger.
- `data/study_version_crosswalk.csv`: source record to study/version mapping.
- `data/current_study_level_coding_matrix_harmonized.csv`: 199 target-software rows.
- `data/extended_synthesis_audit.csv`: 150-study thematic-use audit: 89 full-text-supported and 61 title/abstract-metadata-supported records, including cross-cutting governance context.
- `data/reference_audit.csv`: citation and source-role audit.
- `data/publication_status_standardized.csv`: study-level publication-status assignments.
- `data/publication_status_distribution_by_layer.csv`: publication-status-stratified evidence and shape counts.
- `unified_second_coder_codebook.md`: controlled coding definitions and boundary rules.
- `evidence_output_codebook.md`: principal evidence-output labels.

## Complete Independent Review

- `data/integrated_199_second_coder_comparison_20260730.csv`: complete field comparison.
- `data/integrated_199_per_label_reliability_20260730.csv`: lifecycle and capability label-level reliability.
- `data/integrated_199_label_substitution_sensitivity_20260730.csv`: full-label substitution counts.
- `INTEGRATED_199_SECOND_CODER_AGREEMENT_20260730.md`: report used by the manuscript.
- `data/final_multisource_search_20260730_all_coder_comparison.csv`: detailed comparison for newly reviewed records.

## Supplementary Extractions

- `data/traditional_security_primitives.csv`: 199-study RQ1 extraction with source locations.
- `data/final_multisource_cohort_stability.csv`: shape, evidence-output, and capability distributions for the retained 67-study baseline and 132 new target-software studies.
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

Earlier corpus snapshots, July 15/16 search files, 31-record and 41-record coding checks, and 67-study review files remain in the repository for provenance. Filenames containing `pre_final_multisource_20260730` are frozen inputs to the integrated build. They must not be interpreted as current counts or current manuscript-facing results.

`archive/final_multisource_preintegration_20260730/` contains the superseded pending-status checklist and integration precheck created before the final corpus was closed.
