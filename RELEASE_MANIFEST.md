# Release Manifest

Prepared for public review of the Agentic LLM vulnerability-mining survey artifact.

- Prepared date: 2026-06-19
- Source-specific search ledger date: 2026-06-30
- Product-ecosystem snapshot date: 2026-06-29
- Repository: `https://github.com/oldpanthead/agentic-llm-vuln-mining-survey-artifact`

## Included

The release includes only non-sensitive materials needed to review the survey evidence:

- source-specific search protocol, source-level search ledger, record-level screening audit, corpus metadata, corpus-layer audit, and screening summary;
- 31-Core coding table, current evidence-output codebook, legacy A-profile codebook, and field dictionary;
- boundary/high-relevance classification notes and literature-update decisions;
- v13 synthesis statistics, mapping-snapshot counts, benchmark-boundary notes, research-agenda outputs, and Core synthesis matrix;

Files with `v13_` prefixes are retained filenames from the prior restructuring stage but are used by the current v14 manuscript synthesis unless superseded.
- public-material reproducibility audit and aggregate summary;
- DOI/reference audit and DOI-not-applicable product-page notes;
- citation-expansion audit note for the 2026-06-19 manuscript reference-list update;
- product-ecosystem snapshot for public coding-agent and security-agent materials, including additional ecosystem-balancing background rows;
- pilot second-coder round archived for calibration; formal strongest-evidence-output second-coder pass completed after codebook clarification; formal agreement report included; Agent-increment and external-traceability second-coder extension completed with set-style agreement report; adjudication status recorded separately;
- security boundary, release checklist, repository setup notes, licenses, and reproducibility script.

## Excluded

The release excludes:

- undisclosed PoCs, exploit payloads, live reproduction instructions, sensitive crash inputs, private targets, credentials, or tokens;
- local Zotero storage paths, Zotero SQLite databases, PDFs, private working directories, and private verification exports;
- second-coder answer keys before independent coding, undisclosed adjudication results, and private disagreement notes;
- manuscript source files, build logs, ZIP archives, and temporary audit variants.

## Evidence Boundary

Product pages, help pages, official blogs, model pages, project pages, and disclosure policies are recorded as dated public materials. They support ecosystem and boundary discussion only; they are not independently validated by this artifact, do not automatically expand the 31-Core set, and are not treated as independent reproduction evidence.

The source-specific search ledger records the current manuscript corpus by source bucket, query family, record-level screening decision, and analysis layer. The 2026-06-19 reference-list expansion increases manuscript citation density by citing already-audited Supporting and Background rows. It does not add candidate records, does not expand Core studies, and does not change the 212 / 31 / 66 / 95 / 20 corpus statistics. Reference-list size and corpus-record size are intentionally separate quantities.

The product-ecosystem snapshot is an independent boundary data layer and is not counted in the 212 candidate records. If a product material also supports background or supporting discussion, that role is recorded in `data/reference_audit.csv`.

Legacy A/E fields are retained for historical reproducibility and cross-version traceability. The current manuscript presents the synthesis primarily through natural-language workflow, capability, and evidence-output fields.

The product ecosystem snapshot is date-bounded as of 2026-06-29 and should be refreshed before each manuscript release. Product changes do not automatically alter Core statistics. The snapshot currently contains 23 boundary rows; row-level `access_date` values record individual source checks.

The reproducibility audit separates repository presence, target version, environment, replay material, structured traces, author-reported external traces, publicly traceable external material, and claim-level alignment. `unknown_not_audited` is not counted as absence of material.

## Open Items

- Decide whether and when to archive on Zenodo.
- Refresh fast-changing product materials before the next manuscript revision.
- Prepare an anonymized artifact package or anonymized repository link before anonymous peer review.



## Second-Coder Outputs

- `data/core31_second_coder_formal_blind_template.csv`
- `data/core31_second_coder_formal_results.csv`
- `data/core31_second_coder_adjudication_template.csv`
- `reports/FORMAL_SECOND_CODER_AGREEMENT_REPORT.md`
- `archive/pilot_second_coder_round_1/`
- `data/core31_second_coder_capability_traceability_blind_template.csv`
- `data/core31_second_coder_capability_traceability_results.csv`
- `reports/SECOND_CODER_CAPABILITY_TRACEABILITY_AGREEMENT_REPORT.md`

Pilot agreement/kappa values in the archive are retained for codebook calibration only and must not be cited as formal intercoder reliability. Formal strongest-evidence-output agreement statistics are reported in `reports/FORMAL_SECOND_CODER_AGREEMENT_REPORT.md`; Agent-increment and external-traceability extension agreement is reported separately in `reports/SECOND_CODER_CAPABILITY_TRACEABILITY_AGREEMENT_REPORT.md` using set-style and per-label metrics. Adjudicated labels should be recorded separately if adjudication is performed.

