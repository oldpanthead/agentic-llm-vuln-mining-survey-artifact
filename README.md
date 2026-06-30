# Public Audit Artifact

This repository contains the non-sensitive public artifact for a Chinese mapping-oriented scoping review on Agentic LLM systems for vulnerability mining. It is designed for reviewer auditability, not exploit reproduction.

## What To Check First

1. Run `python reproduce_tables.py`.
2. Inspect `data/corpus.csv`, `data/core_coding.csv`, and `data/corpus_layer_audit.csv` for corpus layering and Core coding.
3. Inspect `SEARCH_PROTOCOL.md`, `data/source_search_log.csv`, and `data/source_screening_audit.csv` for the source-specific search ledger.
4. Inspect `data/v13_synthesis_statistics.csv`, `data/v13_reproducibility_audit.csv`, and `data/mapping_snapshot_counts.csv` for manuscript-facing synthesis and mapping counts.
5. Inspect `data/product_ecosystem_snapshot.csv` for the 2026-06-29 product-ecosystem boundary snapshot.
6. Read `SECURITY_BOUNDARY.md` before using any security-related rows.

## Scope

- Candidate records: 212
- Analytical Core studies: 31
- Supporting studies: 66
- Background references: 95
- Excluded records: 20
- Product/system boundary snapshot rows: 23
- Source-specific search ledger date: 2026-06-30

The manuscript reference list may cite a subset of already-audited Supporting or Background rows more densely than earlier drafts. Reference-list size is therefore not the same as corpus-record size. The 2026-06-19 reference expansion drew only on rows already present in `data/corpus.csv` and `data/reference_audit.csv`; it did not change the 212 / 31 / 66 / 95 / 20 corpus statistics.

Product pages, help pages, official blogs, model pages, project pages, and disclosure policies are recorded as dated boundary material. These public vendor/project materials are not independently validated by this artifact, do not automatically enter Core statistics, and are not treated as independent reproduction evidence.

The product ecosystem snapshot is an independent boundary data layer. It is not part of the 212 candidate records; when a product item also supports background or supporting discussion, its use is recorded separately in `data/reference_audit.csv`.

The current manuscript synthesis is based on natural-language workflow, capability, and evidence-output fields. Legacy A/E fields are retained only for historical reproducibility and cross-version traceability.

The product ecosystem snapshot is date-bounded as of 2026-06-29 and should be refreshed before each manuscript release. Product changes do not automatically alter Core statistics. Row-level `access_date` values record when individual public sources were checked.

## Historical Traceability

The public artifact still includes legacy A-profile and E-level columns because earlier manuscript versions used them for reproducibility checks. They should be read as historical traceability fields. The current manuscript-facing synthesis uses workflow position, Agent capability, strongest evidence output, external audit material, and claim-boundary notes.

## Second-Coder Status

After the pilot calibration round, the clarified codebook was used for a formal second-coder pass on the strongest-evidence-output field for all 31 Core studies. Formal results are stored in `data/core31_second_coder_formal_results.csv`, and agreement statistics are reported in `reports/FORMAL_SECOND_CODER_AGREEMENT_REPORT.md`. The pilot round remains archived for calibration only. A separate formal extension check was completed for Agent-increment / cross-stage capability and external-traceability fields using `data/core31_second_coder_capability_traceability_blind_template.csv` as the blank input template. Completed extension results are stored in `data/core31_second_coder_capability_traceability_results.csv`, and multi-label/set-style agreement statistics are reported in `reports/SECOND_CODER_CAPABILITY_TRACEABILITY_AGREEMENT_REPORT.md`.

## Main Files

- `SEARCH_PROTOCOL.md`: source-specific search protocol for the current mapping-oriented scoping review corpus.
- `data/source_search_log.csv`: source-level search ledger and post-deduplication candidate counts.
- `data/source_screening_audit.csv`: record-level source assignment, screening decision, and layer outcome for all 212 candidate records.
- `data/corpus.csv`: corpus metadata and analysis-use layers.
- `data/core_coding.csv`: legacy A/E coding for the 31 Core studies, retained for historical traceability.
- `data/corpus_layer_audit.csv`: layer audit fields for Core / Supporting / Background / Excluded records.
- `data/reference_audit.csv`: bibliographic audit table.
- `data/doi_remaining_manual_status.csv`: DOI-less or DOI-not-applicable status notes.
- `data/v13_core_synthesis_matrix.csv`: natural-language Core synthesis matrix used by the current manuscript.
- `data/v13_synthesis_statistics.csv`: checked synthesis counts used by the manuscript.

Files with `v13_` prefixes are retained filenames from the prior restructuring stage but are used by the current v14 manuscript synthesis unless superseded.
- `data/mapping_snapshot_counts.csv`: descriptive mapping views for year, source type, and task facet; these counts describe the manuscript corpus only and are not field-level prevalence estimates.
- `data/core_reproducibility_audit.csv`: public-material reproducibility audit for 30 vulnerability-mining Core studies; C27 is excluded as a governance boundary case.
- `data/product_ecosystem_snapshot.csv`: public coding-agent and security-agent product snapshot as of 2026-06-29.
- `evidence_output_codebook.md`, `codebook.md`, and `data_dictionary.md`: current evidence-output labels, legacy coding definitions, and field descriptions.
- `ZOTERO_PDF_RESOLUTION_REPORT.md`: path-redacted public Zotero/PDF resolution summary.

Second-coder files include `data/core31_second_coder_formal_blind_template.csv` as a blank template for future strongest-evidence-output reruns, `data/core31_second_coder_formal_results.csv` as the completed formal strongest-evidence-output second-coder pass, `reports/FORMAL_SECOND_CODER_AGREEMENT_REPORT.md` for pre-adjudication agreement statistics, and `data/core31_second_coder_adjudication_template.csv` for comparison/adjudication. `data/core31_second_coder_capability_traceability_blind_template.csv` remains the blank extension template for future reruns, while `data/core31_second_coder_capability_traceability_results.csv` stores the completed Agent-increment / external-traceability coder2 decisions. `reports/SECOND_CODER_CAPABILITY_TRACEABILITY_AGREEMENT_REPORT.md` reports set-style and per-label agreement for those fields. The archived pilot files are under `archive/pilot_second_coder_round_1/` and remain calibration-only. Auxiliary sampled-review worksheets include `data/intercoder_sample_blind.csv`, `data/intercoder_check_template.csv`, and `data/disagreement_resolution_template.csv`.

## Security Boundary

This artifact excludes undisclosed PoCs, exploit payloads, private targets, credentials, live vulnerability reproduction instructions, sensitive crash inputs, local Zotero paths, SQLite databases, PDFs, and private vendor or bug-bounty communication.

## Reproduce Checks

Run from this directory:

```bash
python reproduce_tables.py
```

Expected result: all schema, source-search ledger, corpus count, Core count, product-snapshot, mapping-snapshot, formal strongest-evidence-output second-coder template/results, formal agreement report, capability/traceability extension template/results/report, legacy A/E, classification, and reproducibility-audit checks pass. Missing DOI rows remain documented warnings.

## License

- Data and documentation: CC BY 4.0, see `LICENSE-DATA`.
- Code scripts: MIT License, see `LICENSE-CODE`.

The current public repository URL is `https://github.com/oldpanthead/agentic-llm-vuln-mining-survey-artifact`. An archival DOI is not yet assigned. For anonymous review, prepare a separate anonymized artifact package or anonymized repository link before submission.


