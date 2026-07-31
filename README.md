# Public Audit Artifact

This repository contains the non-sensitive artifact for a mapping-oriented scoping review of Agentic LLM systems for vulnerability discovery and validation. It supports audit of the integrated multi-source search, study/version reconciliation, corpus stratification, study-level coding, extended synthesis, independent second-coder review, and source-located supplementary extractions. It is not an exploit-reproduction package.

## Start Here

1. Read `SECURITY_BOUNDARY.md`.
2. Run `python reproduce_tables.py`.
3. Use `ARTIFACT_INDEX.md` as the compact file map.
4. Use `data_dictionary.md` for field definitions.

The submission snapshot tag will be recorded after the synchronized manuscript and artifact commit is approved. Earlier tags, including `csur-submission-2026-07-final-v6`, remain immutable historical snapshots.

## Current Integrated Snapshot

The review integrates database and supplementary searches conducted through 2026-07-30.

- Exported source occurrences: 12,090
- Occurrences entering source-level deduplication: 2,289
- Unique interface records screened: 1,642
- Reports sought: 274
- Reports assessed at full text: 239
- Integrated source records: 1,785
- Studies after version reconciliation: 1,772
- Target-software studies with study-level coding: 199
- Governance boundary case: 1, outside target-software distributions
- Extended-synthesis studies: 149
- Background/reference studies: 670
- Excluded studies: 753
- Alternate versions or source variants retained without separate counting: 13

The search used arXiv, OpenAlex, Crossref-backed publisher queries for ACM, IEEE, Springer, and Elsevier records, and supplementary checks of official conference, indexing, benchmark, project, seed, and citation sources. The access log distinguishes exportable interfaces from source-restricted web checks and records unavailable subscription services without claiming access.

## Main Audit Paths

### Search, screening, and reconciliation

- `FINAL_MULTISOURCE_SEARCH_PROTOCOL_20260730.md`: unified protocol, date range, query groups, and source-access boundaries.
- `data/final_multisource_search_20260730_access_log.csv`: query-level access and export log.
- `data/final_multisource_search_20260730_results.csv`: saved multi-source search occurrences.
- `data/final_multisource_search_20260730_screening_audit.csv`: title/abstract and retrieval decisions for the 1,642 unique interface records.
- `data/final_multisource_search_20260730_fulltext_assessment.csv`: full-text eligibility and analytical-layer decisions.
- `data/final_multisource_search_20260730_prisma_counts.csv`: directly recomputable PRISMA-ScR counts.
- `data/final_multisource_search_20260730_source_counts.csv`: source-interface occurrence counts.
- `data/final_multisource_search_20260730_dedup_resolutions.csv`: same-study/version decisions.
- `data/corpus.csv`: integrated 1,785-source-record ledger.
- `data/study_version_crosswalk.csv`: 1,785 source records mapped to 1,772 studies.
- `data/publication_status_standardized.csv`: study-level publication-status assignments.
- `data/publication_status_distribution_by_layer.csv`: publication-status-stratified evidence and shape counts used in the manuscript.

### Study-level and extended synthesis

- `data/current_study_level_coding_matrix_harmonized.csv`: final 200-row matrix: 199 target-software studies and one governance boundary case.
- `data/extended_synthesis_audit.csv`: record-level audit for 149 extended-synthesis studies.
- `data/traditional_security_primitives.csv`: source-located, multi-label author extraction for the 199 target-software studies.
- `data/representative_system_mechanisms.csv`: source-located mechanism extraction used by the representative system comparison.
- `data/mechanism_cost_ablation_synthesis.csv`: source-located cost, ablation, and failure-recovery observations.
- `data/representative_reported_results.csv`: source-located rows used by the representative reported-results table.
- `references_final_multisource_new_studies_20260730.bib`: reference metadata for newly integrated study-level records.

### Independent second-coder review

- `data/final_multisource_search_20260730_all_coder_comparison.csv`: author/coder2 comparison for the newly reviewed records.
- `data/integrated_199_second_coder_comparison_20260730.csv`: complete comparison for all 199 target-software studies.
- `data/integrated_199_per_label_reliability_20260730.csv`: lifecycle and capability label-level agreement.
- `data/integrated_199_label_substitution_sensitivity_20260730.csv`: complete coder2 substitution counts.
- `INTEGRATED_199_SECOND_CODER_AGREEMENT_20260730.md`: integrated reliability summary.

The complete review uses the same controlled fields across all 199 target-software studies. Final descriptive distributions use the final author matrix; independent labels and substitution results remain separate. No consensus or post-adjudication reliability is claimed.

## Historical Provenance

Files concerning the earlier 31-record, 41-record, 67-study, July 15 arXiv, and July 16 official-source checks are retained as provenance. They document codebook development, earlier search stages, and prior submission snapshots; they are not the current corpus denominators or the current reliability result. Files with legacy values such as `Core`, `Supporting`, `core31`, or `v13_` remain only where needed for traceability or script compatibility.

## Evidence and Security Boundaries

The manuscript synthesis uses workflow position, cross-stage capability, primary system shape, principal reported evidence output, external traceability, and structured claim-boundary notes. The CSV field `strongest_evidence_output` remains as a historical schema name for compatibility.

The public artifact excludes undisclosed PoCs, exploit payloads, sensitive crash inputs, private targets, credentials, live reproduction steps, local document-library paths, private databases, full-text PDFs, and vendor-private or bug-bounty communications.

## License

- Data and documentation: CC BY 4.0, see `LICENSE-DATA`.
- Code: MIT License, see `LICENSE-CODE`.

Repository: `https://github.com/oldpanthead/agentic-llm-vuln-mining-survey-artifact`.
