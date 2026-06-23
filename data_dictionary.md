# Data Dictionary

This dictionary describes the non-sensitive audit artifact used by the survey manuscript. It is intended to help reviewers inspect corpus construction, legacy A/E traceability fields, current evidence-output labels, bibliographic verification, pilot second-coder calibration materials, formal second-coder templates/results, agreement reports, and pending adjudication materials.

## Common Identifiers

- `record_id`: stable identifier for one candidate record in the 212-record corpus.
- `core_id`: stable identifier for one Core study in the 31-record deeply coded subset.
- `sample_id`: stable identifier for one record in the second-coder sample.

## `data/corpus.csv`

- `record_id`: candidate record identifier.
- `title`: record title as used in the local corpus.
- `year`: publication or release year from local metadata.
- `authors`: author string when available; `NA` means not filled in the public-minimal artifact.
- `source_type`: local source type, such as `journalArticle`, `conferencePaper`, `preprint`, or `thesis`.
- `venue_or_source`: local venue/source provenance.
- `doi_or_url`: DOI, URL, ISBN URN, or other local locator.
- `corpus_layer`: analysis-use layer: `Core`, `Supporting`, `Background`, or `Excluded`.
- `task_category`: coarse task family used during screening.
- `exclusion_reason`: reason for exclusion, or `NA`.
- `note`: local audit note.

## `data/core_coding.csv`

- `core_id`: Core-study coding identifier.
- `record_id`: link to `corpus.csv`.
- `system_alias`: short system or benchmark name.
- `task_category`: security task category used in manuscript analysis.
- `a_level`: A-profile tag or plus-style capability combination. See `codebook.md`.
- `a_level_reason`: textual rationale for A-profile coding.
- `e_level`: evidence level. See `codebook.md`.
- `e_level_reason`: textual rationale for E-level coding.
- `evidence_object`: object of evidence, such as model judgment, task completion, system output, task background, external clue, or governance risk.
- `external_evidence_profile`: brief external-evidence characterization.
- `artifact_available`: local note on artifact availability.
- `version_reported`: local note on version reporting.
- `environment_reported`: local note on environment reporting.
- `external_confirmation_reported`: local note on independent/external confirmation.
- `note`: boundary, caveat, or manual-check note.

## `data/corpus_layer_audit.csv`

- `record_id`: link to `corpus.csv`.
- `title`: record title as used in the local corpus.
- `year`: publication or release year from local metadata.
- `source_type`: local source type.
- `publication_status`: working publication-status audit field.
- `original_layer`: layer in the original public-minimal corpus.
- `supplemental_layer`: supplemental analysis layer, including `Analytical Core`, `Supporting`, `Background Context`, and `Excluded`.
- `task_category`: coarse task family used during screening.
- `is_analytical_core`: whether the record is part of the 31-study deep analytical set.
- `core_id`: Core identifier when applicable; otherwise `NA`.
- `system_alias`: short system or benchmark name when applicable.
- `a_level_original`: original A-profile code for Core records.
- `primary_evidence_stage_original`: original E0--E3 primary evidence stage for Core records.
- `external_evidence_profile_original`: original E4 profile field for Core records.
- `evidence_object_original`: original evidence-object field for Core records.
- `artifact_status_original`: artifact-availability note when available.
- `official_url`: official URL, DOI URL, arXiv URL, project page, or best available locator.
- `doi`: DOI if available; otherwise `NA`.
- `inclusion_or_exclusion_reason`: supplemental layer rationale.
- `supplemental_audit_note`: additional boundary or verification note.

## `data/record_classification_audit.csv`

- `record`: record or system name as shown in the manuscript discussion.
- `citation_id`: local citation or bibliography key used for traceability.
- `classification`: final analysis-use layer for the record: `Core`, `Supporting`, or `Background`.
- `boundary_case`: whether the record was treated as a boundary/high-relevance classification case.
- `classification_reason`: concise reason for the final layer decision.
- `core_eligibility`: whether the record has a codable system workflow for Core treatment.
- `evidence_chain_relevance`: relationship to CRS, PoV, execution feedback, fuzzing, or evidence-chain analysis.
- `high_risk_claim_handling`: how zero-day, CVE, maintainer-confirmation, unknown-vulnerability, or similar high-risk claims are scoped.
- `author_note`: release note explaining that the classification was retained in the public artifact after the manuscript boundary table was removed.

## `data/literature_update_decisions.csv`

- `supplemental_id`: stable identifier for one high-relevance literature candidate.
- `title`, `authors`, `year`: bibliographic metadata.
- `source_url`, `doi`: public locator fields.
- `publication_status`: working status such as preprint, proceedings paper, or accepted article.
- `candidate_layer`: layer after review; these rows are reflected in the current unified corpus statistics.
- `initial_task`: coarse task family.
- `initial_a_level`, `initial_primary_evidence_stage`, `initial_e4_profile`: initial A/E boundary assessment.
- `evidence_claim`: high-level evidence claim reported by the paper or public page.
- `artifact_link_or_status`: artifact URL or availability note.
- `external_confirmation_trace`: public external-confirmation clue if located.
- `e4c_impact`: whether the record changes the manuscript's specific-vulnerability E4c conclusion.
- `audit_note`: reviewer-facing caution and next-step note.

## `data/core31_second_coder_blind.csv`

This file is retained as a blank blind template after the pilot round was archived. It intentionally hides original A/E labels, original evidence labels, original evidence objects, and other answer-key fields.

- `core_id`, `record_id`, `system_alias`, `title`: Core-study identifiers.
- `publication_status`: publication/material status only. Current allowed values in the 31-Core second-coder files include `not_publicly_available`, `preprint_or_arxiv_from_local_metadata`, `arXiv preprint`, `journal article`, `preprint/project page`, `verified_by_official_source`, and `peer_reviewed`. This field must not encode boundary role.
- `boundary_role`: analysis-boundary role for second-coder workflow; currently `standard_core_entry` or `governance_boundary_case`.
- `materials_to_review`: non-sensitive instruction describing which public materials to inspect.
- `coder2_strongest_evidence_output`: blank field for a future formal second-coder decision using the current manuscript evidence-output label.
- `coder2_decision_reason`: blank rationale field for the future formal second coder.
- `coder2_uncertainty_note`: blank uncertainty or missing-material note.

## `data/core31_second_coder_formal_blind_template.csv`

This is the blank formal second-coder template for future reruns. It has the same schema as `data/core31_second_coder_blind.csv`, contains 31 rows, contains no `original_*` fields, and keeps `coder2_strongest_evidence_output`, `coder2_decision_reason`, and `coder2_uncertainty_note` empty.

## `data/core31_second_coder_formal_results.csv`

This file contains the completed formal second-coder results after codebook clarification. It has 31 rows, contains no `original_*` fields, and preserves the second coder's strongest-evidence-output labels, decision rationales, and uncertainty notes.

## `reports/FORMAL_SECOND_CODER_AGREEMENT_REPORT.md`

This report is generated from the author baseline in `data/core31_second_coder_adjudication_template.csv` and the completed formal coder2 decisions in `data/core31_second_coder_formal_results.csv`. It reports formal pre-adjudication raw agreement, Cohen's kappa, and disagreement rows.

## `archive/pilot_second_coder_round_1/`

This archive preserves the first pilot second-coder round for codebook calibration. It contains the pilot results and pre-adjudication agreement report. These materials should not be cited as the formal intercoder reliability result.

## `data/core31_second_coder_adjudication_template.csv`

This file is for comparison and adjudication after independent coding is complete. It may contain `original_*` fields and should not be used as second-coder input.

- `core_id`, `record_id`, `system_alias`, `title`: Core-study identifiers.
- `original_a_level`, `original_primary_evidence_stage`, `original_e4_profile`, `original_evidence_object`, `original_task_category`: first-pass labels retained for adjudication and historical traceability.
- `original_strongest_evidence_output`: current manuscript evidence-output baseline used only after independent coding for comparison and adjudication.
- `original_artifact_note`, `original_environment_note`, `publication_status`, `boundary_role`: context fields for later comparison. `publication_status` records publication/material status only; `boundary_role` records whether the row is a standard Core entry or governance boundary case.
- `coder2_strongest_evidence_output`, `coder2_decision_reason`, `coder2_uncertainty_note`: optional fields for a later adjudication step. If adjudication is performed, these fields may be copied from `data/core31_second_coder_formal_results.csv`; they are intentionally blank until adjudication is explicitly recorded.
- `coder2_a_level`, `coder2_primary_evidence_stage`, `coder2_e4_profile`, `coder2_evidence_object`: optional legacy second-coder decision fields if a later sampled A/E review is performed.
- `coder2_orchestration_flag`, `coder2_adaptation_flag`, `coder2_external_confirmation_level`, `coder2_reproducibility_level`, `coder2_publication_confidence`: optional auxiliary audit fields.
- `disagreement_note`, `adjudication_result`: adjudication fields to fill only if a separate adjudication step is performed after the formal independent coding pass.

## `data/screening_summary.csv`

- `stage`: corpus construction or screening stage.
- `count`: count if recoverable; `NA` means not recoverable from local records.
- `note`: explanation or boundary condition.

## `data/reference_audit.csv`

- `record_id`: link to `corpus.csv`.
- `canonical_title`: normalized title used for bibliographic audit.
- `system_alias`: system alias when available.
- `publication_status`: current working status after local/Zotero/official-source audit.
- `venue`: venue, repository, proceedings, or source.
- `official_url`: official page, DOI URL, arXiv URL, project page, or best available locator.
- `arxiv_id`: arXiv identifier if applicable; otherwise `NA`.
- `doi`: DOI if available; otherwise `NA`.
- `last_verified_date`: date of the latest local audit update for this row.
- `note`: provenance, risk flags, and manual-check notes.

Manuscript citation count is not a corpus statistic. The 2026-06-19 reference-list expansion cited additional rows that were already present in `corpus.csv` and `reference_audit.csv`; those citations remain Supporting or Background material and do not alter the 212 candidate records, 31 Core studies, 66 Supporting studies, 95 Background references, or 20 Excluded records.

## `data/product_ecosystem_snapshot.csv`

This file is an independent product-ecosystem boundary data layer. Rows in this file are not part of `data/corpus.csv`, do not count toward the 212 candidate records, and do not alter Core aggregate statistics. Product materials that also support manuscript background or supporting discussion are represented separately in `data/reference_audit.csv`.

- `product_or_system`: public product, model, workflow, policy, or attempted source check.
- `vendor`: vendor or organization associated with the material.
- `snapshot_date`: date on which the product snapshot was recorded.
- `model_or_version`: public model, version, release, or availability detail when visible; `NA` if not applicable.
- `public_capabilities`: high-level public capability description from official sources.
- `security_workflow`: security-relevant workflow or boundary described by the source.
- `public_evidence_type`: material type, such as product page, developer documentation, help page, vendor blog, model page, policy page, or excluded attempted source.
- `source_url`: official public source URL; `NA` if no reliable official source was captured.
- `publication_or_update_date`: publication, update, or explicit page date when available; otherwise a no-date note.
- `access_date`: date the source was accessed for this snapshot.
- `manuscript_role`: analysis-use layer for the manuscript: `Background`, `Supporting`, `Emerging boundary case`, `Core candidate`, or `Excluded`.
- `core_eligibility`: conservative Core-eligibility judgment. Vendor product materials do not automatically enter Core statistics.
- `evidence_caveat`: source-limitation note, especially for vendor claims and non-independent evidence.
- `external_traceability`: whether the public source points to independently traceable issues, advisories, CVEs, or maintainer processes.
- `update_required`: whether the item should be refreshed before future manuscript revisions.
- `notes`: local audit notes. This field must not include local Zotero paths, PDF paths, private working directories, credentials, or sensitive vulnerability material.

## Verification Worksheets

`data/verification_status.csv` is a official-source verification status sheet. Fields prefixed with `current_` describe the audit state when the worksheet was generated. `zotero_*` fields are local Zotero candidates, not final official-source proof.

`data/zotero_doi_merge_delta.csv` records DOI merge provenance and risk flags. Important risk flags include:

- `publisher_landing_recorded`
- `arxiv_doi_check_version`
- `differs_from_current_doi`
- `differs_from_url_doi_candidate`
- `published_doi_with_arxiv_url_check_version`

`data/doi_remaining_manual_status.csv` documents records that remain DOI-less after the DOI merge and supplemental pass.

Product and policy pages added for the product-ecosystem snapshot are also listed there when DOI is not applicable. These rows record `doi_not_applicable_product_page` or equivalent status and do not change manuscript corpus, the 212 candidate records, or Core counts.

Rows already audited with DOI or official URL in `reference_audit.csv` are not duplicated in `doi_remaining_manual_status.csv` merely because they are newly cited in a manuscript draft.

## Intercoder Files

`data/core31_second_coder_formal_blind_template.csv` is the blank formal second-coder input for future reruns. `data/core31_second_coder_formal_results.csv` contains the completed formal second-coder pass and no `original_*` fields. `reports/FORMAL_SECOND_CODER_AGREEMENT_REPORT.md` reports formal pre-adjudication agreement against `data/core31_second_coder_adjudication_template.csv`. `data/core31_second_coder_blind.csv` is also kept blank as a blind workflow template.

`archive/pilot_second_coder_round_1/` preserves the pilot round for calibration only; its raw agreement and kappa should not be cited as formal reliability. Formal reliability statistics are reported only in `reports/FORMAL_SECOND_CODER_AGREEMENT_REPORT.md`.

`data/intercoder_sample_blind.csv` is an optional sampled-review worksheet. `data/intercoder_sample_key.csv` is private and not included in the public artifact.

`data/disagreement_resolution_template.csv` records coder decisions, adjudicated decisions, rationales, and resolution metadata if a separate adjudication worksheet is later used.

## Missing Values

`NA` means one of the following:

- not applicable to the record;
- not recoverable from local records;
- intentionally withheld from the minimal public artifact;
- not yet verified against official sources.

Do not infer a missing value from surrounding rows without recording the source and rationale.


## Record classification audit fields
`final_decision`, `decision_reason`, and `stats_treatment` in `data/literature_update_decisions.csv` preserve the provenance of Core / Supporting / Background / Excluded decisions for the seven high-relevance records. The manuscript-facing classification summary is provided in `data/record_classification_audit.csv`, and these decisions are already reflected in the current 31-Core corpus statistics.

## data/core_reproducibility_audit.csv

Per-Core public-material audit linked by `core_id`. Private Zotero paths are excluded. Status fields distinguish public artifact visibility, target version, environment, replay/PoC/PoV material, structured trace, author-reported external traces, publicly traceable external material, and claim-level alignment.
