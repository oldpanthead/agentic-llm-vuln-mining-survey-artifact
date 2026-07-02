# Public Audit Artifact

This repository contains the non-sensitive public artifact for a Chinese mapping-oriented scoping review on Agentic LLM systems for vulnerability mining. It supports reviewer audit of corpus construction, Core coding, second-coder checks, mapping counts, reference verification, product-ecosystem boundary materials, and reproducibility notes. It is not an exploit-reproduction package.

## Start Here

1. Read `SECURITY_BOUNDARY.md`.
2. Run `D:\Anaconda3\python.exe reproduce_tables.py` on Windows, or `python reproduce_tables.py` with a working Python installation.
3. Use `ARTIFACT_INDEX.md` as the compact file map.
4. Use `data_dictionary.md` for field-level definitions.

Expected validation highlights:

- Candidate records: 212
- Core studies: 31
- Supporting studies: 66
- Background references: 95
- Excluded records: 20
- Product/system boundary snapshot rows: 23
- Source-specific search ledger date: 2026-06-30
- Product-ecosystem snapshot date: 2026-06-29

## Main Entry Points

- `SEARCH_PROTOCOL.md`: source-specific search protocol.
- `data/source_search_log.csv`: source-level search ledger.
- `data/source_screening_audit.csv`: record-level screening audit for all 212 candidate records.
- `data/corpus.csv`: corpus metadata and final analysis layer.
- `data/v13_core_synthesis_matrix.csv`: current manuscript-facing Core synthesis matrix; filename retained from a prior restructuring stage.
- `data/v13_synthesis_statistics.csv`: checked synthesis statistics used by the manuscript.
- `data/mapping_snapshot_counts.csv`: descriptive mapping views for the manuscript corpus.
- `data/product_ecosystem_snapshot.csv`: product-ecosystem boundary snapshot, maintained outside the 212-record corpus.
- `evidence_output_codebook.md`: current evidence-output label definitions.
- `data_dictionary.md`: complete field dictionary.
- `reproduce_tables.py`: validation and count-check script.

## Second-Coder Status

The formal strongest-evidence-output second-coder pass covers all 31 Core studies. Results are in `data/core31_second_coder_formal_results.csv`, with agreement reported in `reports/FORMAL_SECOND_CODER_AGREEMENT_REPORT.md`.

A separate extension check covers Agent-increment / cross-stage capability and external traceability. Results are in `data/core31_second_coder_capability_traceability_results.csv`, with set-style agreement reported in `reports/SECOND_CODER_CAPABILITY_TRACEABILITY_AGREEMENT_REPORT.md`.

The pilot second-coder round is archived under `archive/pilot_second_coder_round_1/` for codebook calibration only and should not be cited as formal reliability.

## Evidence Boundary

Product pages, help pages, official blogs, model pages, project pages, and disclosure policies are recorded as dated boundary materials. They support ecosystem discussion and do not expand the 31-Core set. The product ecosystem snapshot is independent of the 212 candidate records; row-level roles and caveats are recorded in `data/product_ecosystem_snapshot.csv` and `data/reference_audit.csv`.

Legacy A/E fields are retained for historical traceability. The current manuscript synthesis uses natural-language workflow, capability, strongest evidence output, external audit material, and claim-boundary fields.

## Security Boundary

The public artifact excludes undisclosed PoCs, exploit payloads, sensitive crash inputs, private targets, credentials, live reproduction steps, local Zotero paths, SQLite databases, PDFs, and private vendor or bug-bounty communication.

## Archive

- `archive/v13_restructuring_audits/`: historical v13 restructuring audit notes.
- `archive/pilot_second_coder_round_1/`: pilot second-coder calibration archive.
- `local_private_working/`: ignored local workspace, not part of the public artifact.

## License

- Data and documentation: CC BY 4.0, see `LICENSE-DATA`.
- Code scripts: MIT License, see `LICENSE-CODE`.

Current public repository URL: `https://github.com/oldpanthead/agentic-llm-vuln-mining-survey-artifact`. Prepare a separate anonymized artifact package or anonymized repository link before anonymous peer review.
