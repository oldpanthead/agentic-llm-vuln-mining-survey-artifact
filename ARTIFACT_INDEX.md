# Artifact Index

This index points reviewers to the public, non-sensitive files needed to audit the survey. Start with `README.md`, then use this page as a compact map.

## Fast Validation

- `reproduce_tables.py`: schema, count, second-coder, product snapshot, source ledger, and safety-boundary checks.
- Expected corpus counts: 212 source records; 207 canonical candidate studies; 31 study-level coded records (30 target-software studies plus 1 governance boundary case); 62 extended synthesis studies; 95 Background references; 19 Excluded near-neighbor studies.
- Product ecosystem snapshot: 23 rows, maintained as an independent boundary layer.

## Corpus Construction

- `SEARCH_PROTOCOL.md`: source-specific search protocol.
- `data/source_search_log.csv`: source-level search ledger frozen on 2026-06-30.
- `data/source_screening_audit.csv`: record-level screening audit for all 212 source records.
- `data/corpus.csv`: source-record metadata and legacy analysis layer.
- `data/study_version_crosswalk.csv`: canonical study/version crosswalk used for analytical counts.
- `data/screening_summary.csv`: compact count summary.

## Study-Level Coding And Extended Synthesis

- `data/v13_core_synthesis_matrix.csv`: current manuscript-facing study-level coded synthesis matrix; filename retained from an earlier restructuring stage.
- `data/v13_synthesis_statistics.csv`: checked synthesis statistics used by the manuscript.
- `data/extended_synthesis_audit.csv`: record-level synthesis-use audit for the 62-study extended synthesis set.
- `EXTENDED_SYNTHESIS_AUDIT_REPORT.md`: summary of the extended synthesis audit.
- `CORPUS_STRATIFICATION_CLOSURE_REPORT.md`: corpus-stratification closure report for the manuscript and artifact.
- `DEDUP_AND_EXTENDED_SYNTHESIS_AUDIT_REPORT.md`: canonical deduplication and extended-synthesis substantiation report.
- `data/mapping_snapshot_counts.csv`: descriptive mapping views for the manuscript corpus.
- `data/core_coding.csv`: legacy A/E fields retained for historical traceability.
- `evidence_output_codebook.md`: current evidence-output labels.
- `codebook.md`: legacy coding definitions and cross-version context.
- `LEGACY_CODE_CROSSWALK.md`: mapping between historical and current coding views.

## Second-Coder Materials

- `data/core31_second_coder_formal_blind_template.csv`: blank strongest-evidence-output template for future reruns.
- `data/core31_second_coder_formal_results.csv`: completed formal strongest-evidence-output pass.
- `reports/FORMAL_SECOND_CODER_AGREEMENT_REPORT.md`: formal agreement report.
- `data/core31_second_coder_capability_traceability_blind_template.csv`: blank capability/traceability extension template.
- `data/core31_second_coder_capability_traceability_results.csv`: completed capability/traceability extension pass.
- `reports/SECOND_CODER_CAPABILITY_TRACEABILITY_AGREEMENT_REPORT.md`: set-style agreement report.
- `archive/pilot_second_coder_round_1/`: pilot calibration only; do not cite as formal reliability.

## References, Products, And Reproducibility

- `data/reference_audit.csv`: bibliographic audit table.
- `data/doi_remaining_manual_status.csv`: DOI-not-found or DOI-not-applicable notes.
- `data/product_ecosystem_snapshot.csv`: dated product-ecosystem boundary snapshot as of 2026-06-29.
- `data/core_reproducibility_audit.csv`: public-material reproducibility audit for 30 target-software study-level coded studies.
- `data/core_reproducibility_audit_summary.csv`: aggregate reproducibility audit summary.
- `ZOTERO_PDF_RESOLUTION_REPORT.md`: path-redacted Zotero/PDF resolution summary.

## Archive And Local-Only Material

- `archive/v13_restructuring_audits/`: historical audit notes from prior manuscript restructuring.
- `archive/pilot_second_coder_round_1/`: archived pilot second-coder calibration.
- `local_private_working/`: ignored local workspace; not part of the public artifact.

## Safety Boundary

Read `SECURITY_BOUNDARY.md` before using security-related rows. The public artifact excludes undisclosed PoCs, exploit payloads, sensitive crash inputs, private targets, credentials, live reproduction steps, PDFs, Zotero databases, local paths, and private vendor or bug-bounty communication.

