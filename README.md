# Public Audit Artifact

This repository contains the non-sensitive artifact for a mapping-oriented scoping review of Agentic LLM systems for vulnerability discovery and validation. It supports audit of the integrated multi-source search, study/version reconciliation, corpus stratification, study-level coding, extended synthesis, independent second-coder review, and source-located supplementary extractions. It is not an exploit-reproduction package.

## Start Here

1. Read `SECURITY_BOUNDARY.md`.
2. Run `python reproduce_tables.py`.
3. Use `ARTIFACT_INDEX.md` as the compact file map.
4. Use `data_dictionary.md` for field definitions.

For a public archive, run `python build_public_release.py <new-output-directory>`. The builder copies only the release allowlist and manuscript-facing manifest, then validates the exported copy. Do not archive the source working tree directly.

The synchronized submission snapshot is identified by `csur-submission-2026-08-final-v10`. Earlier tags, including `csur-submission-2026-08-final-v9` and `csur-submission-2026-07-final-v8`, remain immutable historical snapshots.

## Current Integrated Snapshot

The review integrates database and supplementary searches conducted through 2026-07-30.

- Integrated source records: 1,785
- Studies after version reconciliation: 1,772
- Target-software studies with study-level coding: 199
- Extended-synthesis studies: 154, including governance and agent-safety context outside the target-software denominator
- Background/reference studies: 668
- Excluded studies: 751
- Alternate versions or source variants retained without separate counting: 13

The search used arXiv, OpenAlex, Crossref-backed publisher queries for ACM, IEEE, Springer, and Elsevier records, and supplementary checks of official conference, indexing, benchmark, project, seed, and citation sources. The access log distinguishes exportable interfaces from source-restricted web checks and records unavailable subscription services without claiming access.

## Main Audit Paths

### Search, screening, and reconciliation

- `FINAL_MULTISOURCE_SEARCH_PROTOCOL_20260730.md`: unified protocol, date range, query groups, and source-access boundaries.
- `data/final_multisource_search_20260730_access_log.csv`: query-level access and export log.
- `data/final_multisource_search_20260730_results.csv`: saved multi-source search occurrences.
- `data/final_multisource_search_20260730_screening_audit.csv`: deterministic title/abstract triage for the 1,642 unique interface records.
- `data/final_multisource_search_20260730_fulltext_assessment.csv`: retrieval and assessment evidence retained from the eligibility workflow.
- `data/final_multisource_search_20260730_complete_screening.csv`: frozen final screening stage, analytical allocation, and decision basis for all 1,642 records.
- `data/final_multisource_exclusion_summary.csv`: high-level account of the 751 exclusions by screening stage and basis.
- `data/final_multisource_search_20260730_prisma_counts.csv`: manuscript-facing integrated PRISMA-ScR allocation plus source-specific acquisition provenance.
- `data/final_multisource_search_20260730_source_counts.csv`: source-interface occurrence counts.
- `data/final_multisource_search_20260730_dedup_resolutions.csv`: same-study/version decisions.
- `data/corpus.csv`: integrated 1,785-source-record ledger.
- `data/study_version_crosswalk.csv`: 1,785 source records mapped to 1,772 studies.
- `data/publication_status_standardized.csv`: study-level publication-status assignments.
- `data/publication_status_distribution_by_layer.csv`: publication-status-stratified evidence and shape counts used in the manuscript.

### Study-level and extended synthesis

- `data/adjudicated_study_level_coding_matrix_199.csv`: final 199-row target-software matrix used for all descriptive distributions after third-review adjudication.
- `data/current_study_level_coding_matrix_harmonized.csv`: preserved primary author matrix retained for pre-adjudication provenance.
- `data/extended_synthesis_audit.csv`: record-level audit for 154 adjacent records, comprising 92 records with detailed public material for substantive synthesis and 62 records supporting contextual coverage mapping; AgentFuzz supplies cross-cutting governance context.
- `data/traditional_security_primitives.csv`: source-located, multi-label author extraction for the 199 target-software studies.
- `data/traditional_security_primitives_by_use_role.csv` and `data/traditional_security_primitive_use_role_counts.csv`: study--primitive rows and counts separated into workflow-active and evaluation/support use.
- `data/traditional_security_primitive_by_output.csv`: primitive-family by principal-output co-occurrence counts.
- `data/target_domain_extraction.csv`, `data/target_domain_by_principal_output.csv`, and `data/publication_year_by_primary_shape.csv`: source-located target-domain and descriptive year cross-tabs.
- `data/public_artifact_availability.csv`, `data/public_trigger_replay_evidence_index.csv`, and `data/principal_output_by_public_artifact_availability.csv`: public artifact indicators. The trigger/replay column is restricted to public, system-generated, item-level material; repositories and benchmark inputs alone are excluded. No independent artifact execution is claimed.
- `data/controlled_task_only_membership.csv` and `data/controlled_task_only_sensitivity.csv`: all 199 row-level denominator decisions and the mechanically derived 199-versus-164 sensitivity results.
- `data/public_alignment_evidence_index.csv`: the local evidence chains for all four publicly aligned external-trace cases, including QRS.
- `data/training_data_overlap_control.csv` and `data/training_data_overlap_control_counts.csv`: source-located reporting status for explicit training-overlap controls, discussion only, or no statement located.
- `data/publication_status_sensitivity_analysis.csv`: 199-study shape and output distributions by publication-status group.
- `data/final_multisource_cohort_stability.csv`: provenance-only comparison of historical acquisition groups under the final schema; it does not define manuscript cohorts or denominators.
- `data/representative_system_mechanisms.csv`: source-located mechanism extraction used by the representative system comparison.
- `data/mechanism_cost_ablation_synthesis.csv`: source-located cost, ablation, and failure-recovery observations.
- `data/representative_reported_results.csv`: source-located rows used by the representative reported-results table.
- `references_final_multisource_new_studies_20260730.bib`: reference metadata for newly integrated study-level records.

### Independent second-coder review

- `data/final_multisource_search_20260730_all_coder_comparison.csv`: author/coder2 comparison for the newly reviewed records.
- `data/integrated_199_second_coder_comparison_20260730.csv`: complete comparison for all 199 target-software studies.
- `data/integrated_199_per_label_reliability_20260730.csv`: lifecycle and capability label-level agreement, including Gwet's AC1.
- `data/integrated_199_reporting_audit_disagreement_review.csv`: source-linked direction and boundary basis for reporting/audit disagreements.
- `data/integrated_199_label_substitution_sensitivity_20260730.csv`: complete coder2 substitution counts.
- `INTEGRATED_199_SECOND_CODER_AGREEMENT_20260730.md`: integrated pre-adjudication reliability summary.
- `third_party_rereview_oy_20260824.csv`: raw 460-row OY rereview export (410 disagreements plus 50 QC rows).
- `data/third_party_rereview_decisions_20260824.csv` and `data/third_party_rereview_qc_20260824.csv`: integrated disagreement decisions and separately retained QC results.
- `data/adjudication_log_199_all_fields.csv`, `data/adjudicated_synthesis_statistics_199.csv`, and `data/adjudication_completion_manifest.json`: final external-rereview log, descriptive statistics, and completion manifest. The integrated decision export also carries five `prior_form_*` columns, so the earlier completed-form values are preserved without a second 410-row file.
- `ADJUDICATION_COMPLETION_20260812.md`: adjudication rules, closure status, and reporting boundary.

The complete review uses the same controlled fields across all 199 target-software studies. OY performed an external rereview of all 410 independent-coding disagreements plus 50 hidden-reference QC rows using the prespecified codebook and source evidence. Only disagreement decisions enter the final matrix; QC remains separate. The first- and second-coder files are preserved unchanged, and raw agreement, Cohen's kappa, AC1, and substitution results remain pre-adjudication reliability records. No post-adjudication reliability statistic is claimed.

## Historical Provenance

The tagged source repository retains files concerning the earlier 31-record, 41-record, 67-study, July 15 arXiv, and July 16 official-source checks. They document codebook development, earlier search stages, and prior submission snapshots; they are not the current corpus denominators or the current reliability result. The clean public export omits these historical build files.

## Evidence and Security Boundaries

The manuscript synthesis uses workflow position, cross-stage capability, primary system shape, principal reported evidence output, external traceability, and structured claim-boundary notes. The CSV field `strongest_evidence_output` remains as a historical schema name for compatibility.

The public artifact excludes undisclosed PoCs, exploit payloads, sensitive crash inputs, private targets, credentials, live reproduction steps, local document-library paths, private databases, full-text PDFs, and vendor-private or bug-bounty communications.

## License

- Data and documentation: CC BY 4.0, see `LICENSE-DATA`.
- Code: MIT License, see `LICENSE-CODE`.

Repository: `https://github.com/oldpanthead/agentic-llm-vuln-mining-survey-artifact`.
