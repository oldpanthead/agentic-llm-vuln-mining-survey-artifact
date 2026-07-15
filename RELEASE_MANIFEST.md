# Release Manifest

Prepared for public review of the Agentic LLM vulnerability-mining survey artifact.

- Prepared date: 2026-07-15
- Source-specific search ledger date: 2026-06-30
- Submission-time arXiv sensitivity-search date: 2026-07-15
- Product-ecosystem snapshot date: 2026-06-29
- Repository: `https://github.com/oldpanthead/agentic-llm-vuln-mining-survey-artifact`

## Included

The release includes non-sensitive materials needed to review the survey evidence:

- compact entry map: `ARTIFACT_INDEX.md`;
- source-specific search protocol, source-level ledger, record-level screening audit, submission-time arXiv update export, screening audit, 41-record author full-text audit, blank update-search template, completed independent update coding, pre-adjudication agreement report, preserved working draft, author-confirmed adjudication, canonical-integration assessment, corpus metadata, canonical study/version crosswalk, corpus-layer audit, and screening summary;
- 31-record study-level coding table, `data/extended_synthesis_audit.csv`, extended synthesis audit report, corpus-stratification closure report, deduplication audit report, current evidence-output codebook, legacy A-profile codebook, field dictionary, and legacy-code crosswalk;
- manuscript-facing synthesis matrix, synthesis statistics, mapping counts, benchmark-boundary notes, research-agenda outputs, and reproducibility audit files;
- DOI/reference audit, DOI-status notes, Zotero/PDF resolution summary, and literature-update decisions;
- product-ecosystem snapshot for public coding-agent and security-agent materials;
- formal strongest-evidence-output second-coder results and agreement report;
- formal cross-stage capability / external-traceability extension results and set-style agreement report;
- pilot second-coder calibration archive;
- historical v13 restructuring audit archive;
- security boundary, release checklist, repository setup notes, licenses, and reproducibility script.

Files with `v13_` prefixes are retained filenames from a prior restructuring stage but are used by the current manuscript synthesis unless superseded. Historical narrative audit notes from that stage are under `archive/v13_restructuring_audits/`.

## Excluded

The release excludes:

- undisclosed PoCs, exploit payloads, live reproduction instructions, sensitive crash inputs, private targets, credentials, or tokens;
- local Zotero storage paths, Zotero SQLite databases, PDFs, private working directories, and private verification exports;
- second-coder answer keys before independent coding, undisclosed adjudication results, and private disagreement notes;
- manuscript source files, build logs, ZIP archives, and temporary audit variants.

## Evidence Boundary

Product pages, help pages, official blogs, model pages, project pages, and disclosure policies are recorded as dated public materials. They support ecosystem and boundary discussion only; they are not independently validated by this artifact and do not expand the 31-record study-level coded set.

The source-specific search ledger records the current manuscript corpus by source bucket, query family, record-level screening decision, and analysis layer. Reference-list size and corpus-record size are separate quantities. The current source-record statistics remain 212 source records. Canonical analytical counts are 207 candidate studies: 31 study-level coded records, 61 extended synthesis studies, 95 background/reference records, and 20 excluded near-neighbor studies.

The product-ecosystem snapshot is an independent boundary layer with 23 rows. It is not counted in the 212 source records or 207 canonical candidate studies. Row-level `access_date`, `manuscript_role`, and `evidence_caveat` fields record source timing and use.

Legacy A/E fields are retained for historical reproducibility and cross-version traceability. The current manuscript presents the synthesis primarily through natural-language workflow, capability, evidence-output, external-audit, and claim-boundary fields.

## Second-Coder Outputs

- `data/core31_second_coder_formal_blind_template.csv`
- `data/core31_second_coder_formal_results.csv`
- `data/core31_second_coder_adjudication_template.csv`
- `reports/FORMAL_SECOND_CODER_AGREEMENT_REPORT.md`
- `data/core31_second_coder_capability_traceability_blind_template.csv`
- `data/core31_second_coder_capability_traceability_results.csv`
- `reports/SECOND_CODER_CAPABILITY_TRACEABILITY_AGREEMENT_REPORT.md`
- `archive/pilot_second_coder_round_1/`
- `data/submission_update_20260715_full_coding_audit.csv`
- `data/submission_update_20260715_second_coder_blind_template.csv`
- `data/submission_update_20260715_second_coder_results.csv`
- `reports/SUBMISSION_UPDATE_SECOND_CODER_PRE_ADJUDICATION_REPORT.md`
- `data/submission_update_20260715_adjudication_working_draft.csv`
- `data/submission_update_20260715_adjudicated.csv`
- `reports/SUBMISSION_UPDATE_ADJUDICATION_REPORT.md`
- `data/submission_update_20260715_canonical_integration_crosswalk.csv`
- `SUBMISSION_UPDATE_CANONICAL_INTEGRATION_REPORT.md`
- `SUBMISSION_UPDATE_ADJUDICATION_SUMMARY.md`
- `prepare_submission_update_adjudication.py`
- `finalize_submission_update_adjudication.py`
- `prepare_submission_update_canonical_integration.py`
- `SUBMISSION_UPDATE_FULL_TEXT_AUDIT_REPORT.md`

Pilot agreement/kappa values in the archive are retained for codebook calibration only and must not be cited as formal intercoder reliability. Formal strongest-evidence-output agreement and capability/traceability extension agreement are reported separately. The update-search report contains pre-adjudication agreement from a completed independent pass. The separate final record documents an author-confirmed evidence-based resolution and does not claim two-human consensus or a post-adjudication agreement statistic.

## Open Items

- Decide whether and when to archive on Zenodo.
- Refresh fast-changing product materials before the next manuscript revision.
- Integrate the author-confirmed 37/4 update cohort only through a coordinated corpus/manuscript release. Canonical matching found 41 new studies and projects 253 source records, 248 canonical studies, 67 target-software coded studies plus one governance boundary case, and 65 extended-synthesis studies.
- Prepare an anonymized artifact package or anonymized repository link before anonymous peer review.

## Extended synthesis terminology note

The current manuscript describes the 31-record study-level coded set and the 61-study extended synthesis set. Legacy artifact values retain `Core` and `Supporting` for script compatibility: source records labeled `Core` resolve to the 31 canonical study-level coded records, while the 65 source records labeled `Supporting` resolve to 61 canonical extended synthesis studies after version deduplication.
