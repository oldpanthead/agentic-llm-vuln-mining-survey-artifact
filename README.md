# Public Audit Artifact

This repository contains the non-sensitive public artifact for a Chinese survey on Agentic LLM systems for vulnerability mining. It is designed for reviewer auditability, not exploit reproduction.

## What To Check First

1. Run `python reproduce_tables.py`.
2. Inspect `data/corpus.csv`, `data/core_coding.csv`, and `data/corpus_layer_audit.csv` for corpus layering and Core coding.
3. Inspect `data/v13_synthesis_statistics.csv` and `data/v13_reproducibility_audit.csv` for manuscript-facing synthesis counts.
4. Inspect `data/product_ecosystem_snapshot.csv` for the 2026-06-13 product-ecosystem boundary snapshot.
5. Read `SECURITY_BOUNDARY.md` before using any security-related rows.

## Scope

- Candidate records: 212
- Analytical Core studies: 31
- Supporting studies: 66
- Background references: 95
- Excluded records: 20
- Last incremental manuscript search date: 2026-05-20

The manuscript reference list may cite a subset of already-audited Supporting or Background rows more densely than earlier drafts. Reference-list size is therefore not the same as corpus-record size. The 2026-06-19 reference expansion drew only on rows already present in `data/corpus.csv` and `data/reference_audit.csv`; it did not change the 212 / 31 / 66 / 95 / 20 corpus statistics.

Product pages, help pages, official blogs, model pages, and disclosure policies are recorded as dated boundary material. They do not automatically enter Core statistics and are not treated as independent reproduction evidence.

The product ecosystem snapshot is an independent boundary data layer. It is not part of the 212 candidate records; when a product item also supports background or supporting discussion, its use is recorded separately in `data/reference_audit.csv`.

The current manuscript synthesis is based on natural-language workflow, capability, and evidence-output fields. Legacy A/E fields are retained only for historical reproducibility and cross-version traceability.

The product ecosystem snapshot is date-bounded and should be refreshed before each manuscript release. Product changes do not automatically alter Core statistics.

## Historical Traceability

The public artifact still includes legacy A-profile and E-level columns because earlier manuscript versions used them for reproducibility checks. They should be read as historical traceability fields. The current manuscript-facing synthesis uses workflow position, Agent capability, strongest evidence output, external audit material, and claim-boundary notes.

## Second-Coder Status

The independent second-coder pass for strongest evidence output has been completed for all 31 Core studies. `data/core31_second_coder_blind.csv` remains the blind input table and intentionally hides original labels; `data/core31_second_coder_results.csv` records the completed coder2 decisions. `reports/SECOND_CODER_AGREEMENT_REPORT.md` reports pre-adjudication raw agreement and Cohen's kappa computed from real coder2 decisions. `data/core31_second_coder_adjudication_template.csv` copies coder2 decisions for comparison with `original_strongest_evidence_output`; adjudication is still pending, and `adjudication_result` remains blank. A future adjudicated output should use `data/core31_second_coder_adjudicated.csv` only after disagreement review is complete.

## Main Files

- `data/corpus.csv`: corpus metadata and analysis-use layers.
- `data/core_coding.csv`: legacy A/E coding for the 31 Core studies, retained for historical traceability.
- `data/corpus_layer_audit.csv`: layer audit fields for Core / Supporting / Background / Excluded records.
- `data/reference_audit.csv`: bibliographic audit table.
- `data/doi_remaining_manual_status.csv`: DOI-less or DOI-not-applicable status notes.
- `data/v13_core_synthesis_matrix.csv`: natural-language Core synthesis matrix used by the current manuscript.
- `data/v13_synthesis_statistics.csv`: checked synthesis counts used by the manuscript.
- `data/core_reproducibility_audit.csv`: public-material reproducibility audit for 30 vulnerability-mining Core studies; C27 is excluded as a governance boundary case.
- `data/product_ecosystem_snapshot.csv`: public coding-agent and security-agent product snapshot as of 2026-06-13.
- `evidence_output_codebook.md`, `codebook.md`, and `data_dictionary.md`: current evidence-output labels, legacy coding definitions, and field descriptions.
- `ZOTERO_PDF_RESOLUTION_REPORT.md`: path-redacted public Zotero/PDF resolution summary.

Second-coder files include `data/core31_second_coder_blind.csv` for the blind 31-Core coding input, `data/core31_second_coder_results.csv` for completed coder2 strongest-evidence-output decisions, `data/core31_second_coder_adjudication_template.csv` for pre-adjudication comparison, and `reports/SECOND_CODER_AGREEMENT_REPORT.md` for agreement statistics. Auxiliary sampled-review worksheets include `data/intercoder_sample_blind.csv`, `data/intercoder_check_template.csv`, and `data/disagreement_resolution_template.csv`.

## Security Boundary

This artifact excludes undisclosed PoCs, exploit payloads, private targets, credentials, live vulnerability reproduction instructions, sensitive crash inputs, local Zotero paths, SQLite databases, PDFs, and private vendor or bug-bounty communication.

## Reproduce Checks

Run from this directory:

```bash
python reproduce_tables.py
```

Expected result: all schema, corpus count, Core count, product-snapshot, second-coder, legacy A/E, classification, and reproducibility-audit checks pass. Missing DOI rows remain documented warnings.

## License

- Data and documentation: CC BY 4.0, see `LICENSE-DATA`.
- Code scripts: MIT License, see `LICENSE-CODE`.

The current public repository URL is `https://github.com/oldpanthead/agentic-llm-vuln-mining-survey-artifact`. An archival DOI is not yet assigned.
