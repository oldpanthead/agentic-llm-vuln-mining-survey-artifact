# Public Audit Artifact

This repository contains the non-sensitive public artifact for a mapping-oriented scoping review on Agentic LLM systems for vulnerability mining. It supports reviewer audit of corpus construction, study-level coding, the extended synthesis layer, second-coder checks, mapping counts, reference verification, product-ecosystem boundary materials, and reproducibility notes. It is not an exploit-reproduction package.

## Start Here

1. Read `SECURITY_BOUNDARY.md`.
2. Run `python reproduce_tables.py`.
3. Use `ARTIFACT_INDEX.md` as the compact file map.
4. Use `data_dictionary.md` for field-level definitions.

Expected validation highlights:

- Source records in screening ledger: 253
- Canonical candidate studies after version deduplication: 248
- Study-level coded records: 68 (67 target-software studies plus 1 governance boundary case)
- Source-layer Supporting records: 69
- Canonical extended synthesis studies: 65
- Background references: 95
- Source-layer Excluded records: 21
- Canonical excluded studies: 20
- Product/system boundary snapshot rows: 23
- Source-specific search ledger date: 2026-06-30
- Submission-time arXiv sensitivity-search date: 2026-07-15 (41-record independent pass, author-confirmed 37/4 resolution, and canonical integration complete)
- Product-ecosystem snapshot date: 2026-06-29


## Terminology Compatibility Note

The current corpus contains 68 study-level coded records (67 target-software studies plus one governance boundary case) and 65 extended-synthesis studies. `data/current_study_level_coding_matrix_harmonized.csv` is the author-confirmed current study-level view; `data/current_study_level_coding_matrix.csv` preserves the pre-harmonization combined view. Legacy files with `core31` or `v13` names retain the frozen first-round coding and its formal reliability results, while the 37-row additions file preserves update-round provenance without imputed A/E labels. Source-layer values retain `Core` and `Supporting` for script compatibility and record analytical role rather than study quality.

## Main Entry Points

- `SEARCH_PROTOCOL.md`: source-specific search protocol.
- `data/source_search_log.csv`: source-level search ledger.
- `data/source_screening_audit.csv`: record-level screening audit for all 253 source records.
- `data/submission_update_20260715_screening_audit.csv`: submission-time arXiv sensitivity and recall-recovery decisions.
- `data/submission_update_20260715_full_coding_audit.csv`: frozen pre-adjudication author full-text workflow--capability--evidence audit of the 41 potentially eligible records.
- `data/submission_update_20260715_second_coder_blind_template.csv`: blank independent-review sheet for the 41 update records; it exposes no author labels.
- `data/submission_update_20260715_second_coder_results.csv`: completed independent 41-record coder2 decisions, reasons, and uncertainty notes.
- `reports/SUBMISSION_UPDATE_SECOND_CODER_PRE_ADJUDICATION_REPORT.md`: computed agreement before disagreement resolution.
- `data/submission_update_20260715_adjudication_working_draft.csv`: preserved AI-assisted evidence-linked proposal reviewed by the author.
- `data/submission_update_20260715_adjudicated.csv`: author-confirmed 37/4 field resolution preserving author and coder2 inputs.
- `reports/SUBMISSION_UPDATE_ADJUDICATION_REPORT.md`: confirmation scope, final layer outcome, and consensus boundary.
- `data/submission_update_20260715_canonical_integration_crosswalk.csv`: canonical-identity assessment against the frozen corpus.
- `SUBMISSION_UPDATE_CANONICAL_INTEGRATION_REPORT.md`: pre-integration canonical-match and projected-count assessment.
- `SUBMISSION_UPDATE_CORPUS_INTEGRATION_REPORT.md`: completed integration counts and cohort boundary.
- `data/current_study_level_coding_matrix_harmonized.csv`: author-confirmed harmonized matrix for all 67 target-software studies plus the governance boundary case, with controlled primary shapes, overlays, and cross-stage capabilities.
- `data/current_study_level_coding_matrix.csv`: pre-harmonization combined matrix retained for provenance.
- `data/coding_round_harmonization_audit.csv`: field-level original, candidate, evidence basis, review status, and final label for both rounds.
- `data/current_synthesis_statistics_by_round.csv`: initial, update, and combined harmonized distributions.
- `CODING_ROUND_HARMONIZATION_REPORT.md`: coding-drift findings, author-confirmed changes, and framework-stability assessment.
- `data/submission_update_20260715_study_level_additions.csv`: 37-row update-round view retained for auditability.
- `data/current_synthesis_statistics.csv`: combined descriptive lifecycle, capability, and evidence-output counts.
- `SUBMISSION_UPDATE_ADJUDICATION_SUMMARY.md`: resolution rules and reviewed working-draft history.
- `prepare_submission_update_adjudication.py`: reproducible generator for the working draft and update agreement reports.
- `finalize_submission_update_adjudication.py`: deterministic promotion of the author-confirmed resolution.
- `prepare_submission_update_canonical_integration.py`: reproducible canonical-match and projected-count assessment.
- `SUBMISSION_UPDATE_FULL_TEXT_AUDIT_REPORT.md`: full-text decision summary and reliability boundary.
- `SUBMISSION_UPDATE_AUDIT_REPORT.md`: scope, counts, and methodological implication of the update search.
- `data/corpus.csv`: source-record metadata and legacy analysis layer.
- `data/study_version_crosswalk.csv`: canonical study/version crosswalk used for analytical counts.
- `data/extended_synthesis_audit.csv`: record-level synthesis-use audit for the 65-study extended synthesis set.
- `EXTENDED_SYNTHESIS_AUDIT_REPORT.md`: summary of the extended synthesis audit.
- `CORPUS_STRATIFICATION_CLOSURE_REPORT.md`: corpus-stratification closure report for the manuscript and artifact.
- `DEDUP_AND_EXTENDED_SYNTHESIS_AUDIT_REPORT.md`: canonical deduplication and extended-synthesis substantiation report.
- `data/v13_core_synthesis_matrix.csv`: frozen initial-round 31-record matrix retained for historical traceability; it is not the current combined matrix.
- `data/v13_synthesis_statistics.csv`: checked synthesis statistics used by the manuscript.
- `data/mapping_snapshot_counts.csv`: descriptive mapping views for the manuscript corpus.
- `data/product_ecosystem_snapshot.csv`: product-ecosystem boundary snapshot, maintained outside the 253-record corpus.
- `evidence_output_codebook.md`: current evidence-output label definitions.
- `data_dictionary.md`: complete field dictionary.
- `reproduce_tables.py`: validation and count-check script.

## Second-Coder Status

The formal strongest-evidence-output second-coder pass covers the 31 records in the frozen initial round. Results are in `data/core31_second_coder_formal_results.csv`, with agreement reported in `reports/FORMAL_SECOND_CODER_AGREEMENT_REPORT.md`. The separate 41-record update-round pass and its author-confirmed 37/4 resolution remain documented in the submission-update files. Reliability is reported by round; harmonization does not create a synthetic combined kappa. AI-assisted tools organized disagreement records and prepared evidence-linked candidate resolutions, which the author independently reviewed against the recorded public-material basis.

A separate extension check covers cross-stage capability and external traceability. Results are in `data/core31_second_coder_capability_traceability_results.csv`, with set-style agreement reported in `reports/SECOND_CODER_CAPABILITY_TRACEABILITY_AGREEMENT_REPORT.md`.

The pilot second-coder round is archived under `archive/pilot_second_coder_round_1/` for codebook calibration only and should not be cited as formal reliability.

The 2026-07-15 update-search blind pass is complete for all 41 records. The author-confirmed resolution assigns 37 records to study-level coding and four to extended synthesis. Canonical integration is complete: the current corpus contains 253 source records, 248 canonical studies, 67 target-software coded studies plus one governance boundary case, and 65 extended-synthesis studies. Reliability remains reported by coding round rather than as a synthetic combined kappa.

## Evidence Boundary

Product pages, help pages, official blogs, model pages, project pages, and disclosure policies are recorded as dated boundary materials. They support ecosystem discussion outside the 68-record study-level coded set. The 23-row product snapshot is independent of the 253 source records; row-level roles and caveats are recorded in `data/product_ecosystem_snapshot.csv` and `data/reference_audit.csv`.

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
