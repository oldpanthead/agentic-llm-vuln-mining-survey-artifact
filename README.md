# Public Audit Artifact

This repository contains the non-sensitive artifact for a mapping-oriented scoping review of Agentic LLM systems for vulnerability discovery and validation. It supports audit of the integrated multi-source search, study/version reconciliation, corpus stratification, study-level coding, extended synthesis, independent second-coder review, and source-located supplementary extractions. It is not an exploit-reproduction package.

## Start Here

1. Read `SECURITY_BOUNDARY.md`.
2. Run `python reproduce_tables.py`.
3. Use `docs/coding/data_dictionary.md` for field definitions.

This is the compact public release. It contains directly readable core audit files plus three function-based ZIP bundles that preserve the remaining final audit records under their original relative paths. Run `python reproduce_tables.py` to validate the full artifact; it expands the bundles only in a temporary directory. To inspect a bundled record manually, extract the relevant archive without changing the release directory.

The repository is organized by function: protocol, coding, and review documentation are under `docs/`; search, corpus, coding, adjudication, synthesis, and derived data occupy separate `data/` subdirectories. The root retains only the files needed to identify, cite, secure, and validate the artifact; internal release-builder scripts and superseded manifests are kept in repository history, not in this submission snapshot.

The synchronized submission snapshot is identified by `csur-submission-2026-08-final-v16`. The preceding `csur-submission-2026-08-final-v15`, `csur-submission-2026-08-final-v14`, and earlier tags remain immutable historical snapshots.

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

## Compact File Map

| Location | Role |
|---|---|
| `README.md` | Orientation, counts, audit paths, and release use |
| `SECURITY_BOUNDARY.md` | Public-disclosure boundary |
| `reproduce_tables.py` | Standalone validation entry point |
| `data/search/` | Search, screening, retrieval, and deduplication records |
| `data/corpus/` | Source ledger, version crosswalk, publication/reference audit |
| `data/coding/` | Preserved and final study-level matrices |
| `data/adjudication/` | Independent comparison, OY rereview, and decision log |
| `data/synthesis/` | Source-located study synthesis and representative extractions |
| `data/derived/` | Derived tables and adjudication completion metadata |
| `docs/` | Coding documentation directly; protocol and review documentation are in the function bundles |
| `references/` | BibTeX metadata |

## Main Audit Paths

### Search, screening, and reconciliation

- `docs/protocol/FINAL_MULTISOURCE_SEARCH_AND_PRISMA_20260730.md` (in `bundles/search.zip`): integrated PRISMA account, source-specific provenance, and unified search protocol.
- `data/search/final_multisource_search_20260730_access_log.csv`: query-level access and export log.
- `data/search/final_multisource_search_20260730_results.csv`: saved multi-source search occurrences.
- `data/search/final_multisource_search_20260730_screening_audit.csv`: deterministic title/abstract triage for the 1,642 unique interface records.
- `data/search/final_multisource_search_20260730_fulltext_assessment.csv`: retrieval and assessment evidence retained from the eligibility workflow.
- `data/search/final_multisource_search_20260730_complete_screening.csv`: frozen final screening stage, analytical allocation, and decision basis for all 1,642 records.
- `data/derived/derived_summary_tables.json`: consolidated machine-readable derived summaries, including exclusion, publication-status, primitive, domain, artifact, sensitivity, mapping, and adjudicated-statistics tables.
- `data/search/final_multisource_search_20260730_prisma_counts.csv`: manuscript-facing integrated PRISMA-ScR allocation plus source-specific acquisition provenance.
- `data/search/final_multisource_search_20260730_dedup_resolutions.csv`: same-study/version decisions.
- `data/corpus/corpus.csv`: integrated 1,785-source-record ledger.
- `data/corpus/study_version_crosswalk.csv`: 1,785 source records mapped to 1,772 studies.
- `data/synthesis/study_synthesis_199.csv`: one 199-row, source-prefixed view joining publication status, technical primitives, target domain, public-artifact checks, denominator sensitivity membership, and training-overlap reporting. The component fields are retained as prefixed columns and use `matrix_id` as the join key.

### Study-level and extended synthesis

- `data/coding/adjudicated_study_level_coding_matrix_199.csv`: final 199-row target-software matrix used for all descriptive distributions after third-review adjudication.
- `data/coding/current_study_level_coding_matrix_harmonized.csv` (in `bundles/corpus_and_synthesis.zip`): preserved primary author matrix retained for pre-adjudication provenance.
- `data/coding/extended_synthesis_audit.csv` (in `bundles/corpus_and_synthesis.zip`): record-level audit for 154 adjacent records, comprising 92 records with detailed public material for substantive synthesis and 62 records supporting contextual coverage mapping; AgentFuzz supplies cross-cutting governance context.
- `data/synthesis/traditional_security_primitives_by_use_role.csv` (in `bundles/corpus_and_synthesis.zip`): source-located study--primitive role assignments at their native pair-level granularity.
- The component study-level views formerly stored as separate files are joined in `data/synthesis/study_synthesis_199.csv`; their derived cross-tabs and counts are in `data/derived/derived_summary_tables.json`.
- `data/synthesis/public_trigger_replay_evidence_index.csv` (in `bundles/corpus_and_synthesis.zip`): reviewed trigger/replay candidates. The strict column is restricted to public, system-generated, item-level material; repositories and benchmark inputs alone are excluded. No independent artifact execution is claimed.
- Controlled-task membership fields are in `data/synthesis/study_synthesis_199.csv`; the derived 199-versus-164 sensitivity table is in `data/derived/derived_summary_tables.json`.
- `data/synthesis/public_alignment_evidence_index.csv` (in `bundles/corpus_and_synthesis.zip`): the local evidence chains for all four publicly aligned external-trace cases, including QRS.
- Training-overlap reporting fields are in `data/synthesis/study_synthesis_199.csv`; their counts are in `data/derived/derived_summary_tables.json`.
- Historical cohort-stability calculations and other superseded transition tables are retained in repository history; they do not define manuscript cohorts or denominators.
- `data/synthesis/representative_system_mechanisms.csv` (in `bundles/corpus_and_synthesis.zip`): source-located mechanism extraction used by the representative system comparison.
- `data/derived/empirical_reporting_completeness.csv` (in `bundles/corpus_and_synthesis.zip`): source-located reporting completeness counts for the 67-study extraction subset.
- `data/synthesis/mechanism_cost_ablation_synthesis.csv` (in `bundles/corpus_and_synthesis.zip`): source-located cost, ablation, and failure-recovery observations.
- `data/synthesis/representative_reported_results.csv` (in `bundles/corpus_and_synthesis.zip`): source-located rows used by the representative reported-results table.
- `data/adjudication/final_matrix_reapplication_check_tasks_60.csv` and `data/adjudication/final_matrix_reapplication_check_public_material_60.csv` (in `bundles/reliability_and_rereview.zip`): completed 300-task rule-application diagnostic and its 60-row public-material descriptors.
- `data/derived/final_matrix_reapplication_check_summary.csv` (in `bundles/reliability_and_rereview.zip`): field-level diagnostic metrics for the 60-study check; these are not independent accuracy or reliability estimates.
- `references/references_merged_manuscript.bib`: the complete BibTeX file used by the synchronized manuscript; it contains the newly integrated study references.

### Independent second-coder review

- `data/search/final_multisource_search_20260730_all_coder_comparison.csv`: author/coder2 comparison for the newly reviewed records.
- `data/adjudication/integrated_199_second_coder_comparison_20260730.csv`: complete comparison for all 199 target-software studies.
- `data/adjudication/integrated_199_per_label_reliability_20260730.csv`: lifecycle and capability label-level agreement, including Gwet's AC1.
- `data/adjudication/integrated_199_reporting_audit_disagreement_review.csv`: source-linked direction and boundary basis for reporting/audit disagreements.
- Per-label agreement and the remaining sensitivity inputs are in `data/adjudication/integrated_199_per_label_reliability_20260730.csv` and `data/adjudication/integrated_199_second_coder_comparison_20260730.csv`.
- Integrated pre-adjudication reliability is included in `docs/review/ADJUDICATION_COMPLETION_20260812.md`.
- `data/adjudication/third_party_rereview_decisions_20260824.csv`: OY decisions for the 410 independent-coding disagreements; historical completed-form fields remain merged in this file.
- `data/adjudication/adjudication_log_199_all_fields.csv` and `data/derived/derived_summary_tables.json`: final external-rereview log plus consolidated descriptive statistics and embedded adjudication completion metadata. The integrated decision export also carries five `prior_form_*` columns, so earlier completed-form values are preserved without a second 410-row file.
- `data/adjudication/claim_alignment_reconciled_199.csv`: 199-row auxiliary wording audit retaining Fang/Zhao/Rong/final labels, evidence location, material availability, and current-matrix crosswalk fields. The 190 aligned and nine overclaim labels describe wording alignment only, not study quality, truth, or independent reproducibility.
- `data/adjudication/rong_external_interpretability_check_50.csv` (in `bundles/reliability_and_rereview.zip`): record-level results for Rong Zhoujie's fixed 50-study, four-field external interpretability check, including the 49 comparable records per field and the CP209 unresolved rows.
- `docs/review/ADJUDICATION_COMPLETION_20260812.md` and `docs/review/ADJUDICATION_RULES_20260812.md` (in `bundles/reliability_and_rereview.zip`): adjudication closure record, reporting boundary, and operational rules.

The complete review uses the same controlled fields across all 199 target-software studies. The two coders initially agreed on 585 of the 995 study--field units. Two U17 (FunFuzz) agreements were later corrected through targeted evidence checks, leaving 583 agreement rows unchanged. OY externally rereviewed the 410 independent-coding disagreements; 409 OY decisions were retained and one C11 (MALF) external-traceability decision was later corrected through an official-record check. The field log therefore contains 583 `agreed_assignment` rows, 409 `third_party_external_rereview` rows, and three `post_adjudication_evidence_correction` rows; these corrections add no study or independent coding round. For multi-label fields, OY reread the complete label set and could apply a stricter source-located rule, including `no qualifying label observed`, rather than mechanically selecting one coder. The first- and second-coder files are preserved unchanged, and raw agreement, Cohen's kappa, AC1, and substitution results remain pre-adjudication reliability records. The subsequent 60-study check was completed by Dou Xingwang as an independent post-adjudication rule-application diagnostic; it is not a gold-standard accuracy test or post-adjudication reliability estimate. Rong Zhoujie's separate 50-study check is an external interpretability diagnostic against the preserved pre-adjudication harmonized matrix, not a final-matrix accuracy estimate.

## Historical Provenance

The tagged source repository retains files concerning earlier 31-record, 41-record, 67-study, July 15 arXiv, and July 16 official-source checks, as well as release-builder scripts and superseded manifests. They document codebook development and prior submission snapshots; they are not the current corpus denominators or reliability result. The clean public export omits these historical build files.

## Evidence and Security Boundaries

The manuscript synthesis uses workflow position, cross-stage capability, primary system shape, principal reported evidence output, external traceability, and structured claim-boundary notes. The CSV field `strongest_evidence_output` remains as a historical schema name for compatibility.

The public artifact excludes undisclosed PoCs, exploit payloads, sensitive crash inputs, private targets, credentials, live reproduction steps, local document-library paths, private databases, full-text PDFs, and vendor-private or bug-bounty communications.

## License

- Data and documentation: CC BY 4.0, see `LICENSE-DATA`.
- Code: MIT License, see `LICENSE-CODE`.

Repository: `https://github.com/oldpanthead/agentic-llm-vuln-mining-survey-artifact`.
