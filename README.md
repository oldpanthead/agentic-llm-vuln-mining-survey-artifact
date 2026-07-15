# Public Audit Artifact

This repository contains the non-sensitive public artifact for a mapping-oriented scoping review on Agentic LLM systems for vulnerability mining. It supports reviewer audit of corpus construction, study-level coding, the extended synthesis layer, second-coder checks, mapping counts, reference verification, product-ecosystem boundary materials, and reproducibility notes. It is not an exploit-reproduction package.

## Start Here

1. Read `SECURITY_BOUNDARY.md`.
2. Run `python reproduce_tables.py`.
3. Use `ARTIFACT_INDEX.md` as the compact file map.
4. Use `data_dictionary.md` for field-level definitions.

Expected validation highlights:

- Source records in screening ledger: 212
- Canonical candidate studies after version deduplication: 207
- Study-level coded records: 31 (30 target-software studies plus 1 governance boundary case)
- Source-layer Supporting records: 65
- Canonical extended synthesis studies: 61
- Background references: 95
- Source-layer Excluded records: 21
- Canonical excluded studies: 20
- Product/system boundary snapshot rows: 23
- Source-specific search ledger date: 2026-06-30
- Submission-time arXiv sensitivity-search date: 2026-07-15 (41-record independent blind pass and author-confirmed 37/4 analytical-layer resolution complete; canonical integration assessed separately)
- Product-ecosystem snapshot date: 2026-06-29


## Terminology Compatibility Note

The current manuscript refers to the 31-record study-level coded set and the 61-study extended synthesis set. Some CSV values and legacy filenames retain `Core` and `Supporting` for script compatibility: source records labeled `Core` resolve to the 31 canonical study-level coded records, while the 65 source records labeled `Supporting` resolve to 61 canonical extended synthesis studies after version deduplication. The file `data/extended_synthesis_audit.csv` provides the current record-level synthesis-use audit for those 61 canonical studies. These retained labels do not imply study quality or a lower importance tier.

## Main Entry Points

- `SEARCH_PROTOCOL.md`: source-specific search protocol.
- `data/source_search_log.csv`: source-level search ledger.
- `data/source_screening_audit.csv`: record-level screening audit for all 212 source records.
- `data/submission_update_20260715_screening_audit.csv`: submission-time arXiv sensitivity-search decisions.
- `data/submission_update_20260715_full_coding_audit.csv`: author full-text workflow--capability--evidence audit of the 41 potentially eligible records; labels remain provisional.
- `data/submission_update_20260715_second_coder_blind_template.csv`: blank independent-review sheet for the 41 update records; it exposes no author labels.
- `data/submission_update_20260715_second_coder_results.csv`: completed independent 41-record coder2 decisions, reasons, and uncertainty notes.
- `reports/SUBMISSION_UPDATE_SECOND_CODER_PRE_ADJUDICATION_REPORT.md`: computed agreement before disagreement resolution.
- `data/submission_update_20260715_adjudication_working_draft.csv`: preserved assistant-prepared proposal reviewed by the author.
- `data/submission_update_20260715_adjudicated.csv`: author-confirmed 37/4 field resolution preserving author and coder2 inputs.
- `reports/SUBMISSION_UPDATE_ADJUDICATION_REPORT.md`: confirmation scope, final layer outcome, and consensus boundary.
- `data/submission_update_20260715_canonical_integration_crosswalk.csv`: canonical-identity assessment against the frozen corpus.
- `SUBMISSION_UPDATE_CANONICAL_INTEGRATION_REPORT.md`: projected integration counts and manuscript-update boundary.
- `SUBMISSION_UPDATE_ADJUDICATION_SUMMARY.md`: resolution rules and reviewed working-draft history.
- `prepare_submission_update_adjudication.py`: reproducible generator for the working draft and update agreement reports.
- `finalize_submission_update_adjudication.py`: deterministic promotion of the author-confirmed resolution.
- `prepare_submission_update_canonical_integration.py`: reproducible canonical-match and projected-count assessment.
- `SUBMISSION_UPDATE_FULL_TEXT_AUDIT_REPORT.md`: full-text decision summary and reliability boundary.
- `SUBMISSION_UPDATE_AUDIT_REPORT.md`: scope, counts, and methodological implication of the update search.
- `data/corpus.csv`: source-record metadata and legacy analysis layer.
- `data/study_version_crosswalk.csv`: canonical study/version crosswalk used for analytical counts.
- `data/extended_synthesis_audit.csv`: record-level synthesis-use audit for the 61-study extended synthesis set.
- `EXTENDED_SYNTHESIS_AUDIT_REPORT.md`: summary of the extended synthesis audit.
- `CORPUS_STRATIFICATION_CLOSURE_REPORT.md`: corpus-stratification closure report for the manuscript and artifact.
- `DEDUP_AND_EXTENDED_SYNTHESIS_AUDIT_REPORT.md`: canonical deduplication and extended-synthesis substantiation report.
- `data/v13_core_synthesis_matrix.csv`: current manuscript-facing study-level coded synthesis matrix; filename retained from a prior restructuring stage.
- `data/v13_synthesis_statistics.csv`: checked synthesis statistics used by the manuscript.
- `data/mapping_snapshot_counts.csv`: descriptive mapping views for the manuscript corpus.
- `data/product_ecosystem_snapshot.csv`: product-ecosystem boundary snapshot, maintained outside the 212-record corpus.
- `evidence_output_codebook.md`: current evidence-output label definitions.
- `data_dictionary.md`: complete field dictionary.
- `reproduce_tables.py`: validation and count-check script.

## Second-Coder Status

The formal strongest-evidence-output second-coder pass covers all 31 study-level coded records (legacy `Core` files). Results are in `data/core31_second_coder_formal_results.csv`, with agreement reported in `reports/FORMAL_SECOND_CODER_AGREEMENT_REPORT.md`.

A separate extension check covers cross-stage capability and external traceability. Results are in `data/core31_second_coder_capability_traceability_results.csv`, with set-style agreement reported in `reports/SECOND_CODER_CAPABILITY_TRACEABILITY_AGREEMENT_REPORT.md`.

The pilot second-coder round is archived under `archive/pilot_second_coder_round_1/` for codebook calibration only and should not be cited as formal reliability.

The 2026-07-15 update-search blind pass is complete for all 41 records. Pre-adjudication agreement is reported separately for the update fields. The author accepted the evidence-based 37/4 resolution, with U24 (SynthFix) assigned to extended synthesis under the observable-workflow rule. Canonical matching found 41 new studies and projects a 67-target-study-plus-one-governance coded set after coordinated integration. The frozen manuscript and corpus denominators remain unchanged until that larger release updates the coding matrices, distributions, and text together.

## Evidence Boundary

Product pages, help pages, official blogs, model pages, project pages, and disclosure policies are recorded as dated boundary materials. They support ecosystem discussion and do not expand the 31-record study-level coded set. The product ecosystem snapshot is independent of the 212 source records; row-level roles and caveats are recorded in `data/product_ecosystem_snapshot.csv` and `data/reference_audit.csv`.

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
