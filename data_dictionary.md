# Data Dictionary

This dictionary describes the non-sensitive audit artifact used by the survey manuscript. It is intended to help reviewers inspect corpus construction, legacy A/E traceability fields, current evidence-output labels, bibliographic verification, pilot second-coder calibration materials, formal second-coder templates/results, agreement reports, the submission-update rerun notes, and submission-update adjudication materials. Files with `v13_` prefixes are retained filenames from the prior restructuring stage but are used by the current manuscript synthesis unless superseded.


## Current Manuscript Layer Terminology

Current terminology maps legacy artifact values as follows: `Core` identifies study-level coded source records and `Supporting` identifies extended-synthesis source records. The current corpus contains 68 study-level coded records (67 target-software studies plus one governance boundary case) and 65 extended-synthesis studies. `data/current_study_level_coding_matrix_harmonized.csv` is the author-confirmed current study-level view; `data/current_study_level_coding_matrix.csv` preserves the pre-harmonization combined view. Legacy `core31` and `v13_` files preserve the frozen first coding round; the additions file preserves update-round provenance without imputed A/E labels.

## Unified second-coder review files

`unified_second_coder_codebook.md` and `UNIFIED_SECOND_CODER_REVIEW_GUIDE.md` define the single frozen review boundary applied across all 67 target-software studies plus the governance boundary case. `data/unified_second_coder_final_blind_template.csv` is the blank public input, and `data/unified_second_coder_final_results.csv` contains the completed independent labels and row-level material/decision provenance. `data/unified_second_coder_pre_adjudication_disagreements.csv` compares those labels with the manuscript-facing harmonized matrix without creating consensus labels. `data/unified_second_coder_label_substitution_sensitivity.csv` reports, for each lifecycle, capability, system-shape, evidence-output, and external-traceability label, the author-harmonized count, complete coder2 substitution count, absolute difference, and direction on the 67-study target-software denominator. `reports/UNIFIED_SECOND_CODER_PRE_ADJUDICATION_REPORT.md` reports field-specific agreement before adjudication; adjudication is not planned and no post-adjudication reliability is claimed. Historical 31-record and 41-record files remain as codebook-development and round-provenance records rather than a synthetic combined reliability result.

## `SUBMISSION_UPDATE_SECOND_CODER_RERUN_NOTES.md`

Lightweight boundary notes for an adopted tightened-boundary rerun of the 41-record submission-update second-coder pass. It records the tightened primary/overlay and external-traceability rules used for the adopted update-pass rerun.
## `data/current_study_level_coding_matrix_harmonized.csv` and pre-harmonization provenance

`data/current_study_level_coding_matrix_harmonized.csv` is the author-confirmed current matrix for all 68 study-level coded records. It applies one controlled lifecycle, primary-shape, overlay, cross-stage-capability, evidence-output, and external-traceability schema while preserving round provenance and reliability scope. `data/current_study_level_coding_matrix.csv` is retained unchanged as the pre-harmonization combined view. Neither file contains legacy A/E fields.

- `matrix_id`: stable row identifier inherited from the coding round (`C01`--`C31` or the applicable `U` identifier).
- `record_id`, `canonical_study_id`: source-record and canonical-study links.
- `system_alias`, `title`: system and publication identifiers.
- `analytical_role`: `target_software_study` or `governance_boundary_case`.
- `coding_round`: `initial_frozen_round` or `submission_update_20260715`.
- `harmonization_status`: author-confirmed coding-round harmonization status.
- `lifecycle_coverage`: current controlled multi-label lifecycle coding.
- `primary_system_shape`: one approved primary shape; the governance row remains separate.
- `overlay_tags`: optional controlled overlays kept separate from the primary shape.
- `cross_stage_capabilities`: current controlled multi-label capability field.
- `legacy_notes`: historical textual labels retained outside formal capability coding.
- `strongest_evidence_output`: historical schema field name retained for compatibility; it stores the manuscript's principal reported evidence-output label.
- `external_traceability`: reported external-trace category or note.
- `claim_boundary`: current English claim-boundary wording.
- `claim_boundary_original`: source-round wording retained for traceability; it may match `claim_boundary` for update rows.
- `coding_status`: frozen initial-round or author-confirmed update status.
- `reliability_scope`: fields independently checked in that row's coding round; it prevents reliability results from being generalized across fields or rounds.
- `official_url`: public URL or ISBN locator.

## `data/coding_round_harmonization_audit.csv`, `data/current_synthesis_statistics_by_round.csv`, and `CODING_ROUND_HARMONIZATION_REPORT.md`

The harmonization audit preserves each original field value, current-codebook candidate, evidence basis, source location, uncertainty, author-review status, and final author-confirmed label. The round-statistics file reports initial, submission-update, and combined harmonized counts without constructing a combined reliability coefficient. The report summarizes coding drift, accepted changes, residual round differences, taxonomy stability, and the AI-assisted working-note boundary.
## Common Identifiers

- `record_id`: stable identifier for one source record in the 253-record screening ledger.
- `core_id`: stable identifier for one legacy Core record in the 31-record study-level coded set.
- `sample_id`: stable identifier for one record in the second-coder sample.

## `data/corpus.csv`

- `record_id`: candidate record identifier.
- `title`: record title as used in the local corpus.
- `year`: publication or release year from local metadata.
- `authors`: author string when available; `NA` means not filled in the public-minimal artifact.
- `source_type`: local source type, such as `journalArticle`, `conferencePaper`, `preprint`, or `thesis`.
- `venue_or_source`: local venue/source provenance.
- `doi_or_url`: DOI, URL, ISBN URN, or other local locator.
- `corpus_layer`: legacy analysis-use layer: `Core`, `Supporting`, `Background`, or `Excluded`; in current manuscript terms, `Core` maps to study-level coded records and `Supporting` maps to extended synthesis studies.
- `task_category`: coarse task family used during screening.
- `exclusion_reason`: reason for exclusion, or `NA`.
- `note`: local audit note.

## `data/source_search_log.csv`

This file records the source-specific search ledger for the current manuscript corpus. Counts are deduplicated records captured in the public screening ledger, not volatile web-search result totals.

- `source_id`: compact source bucket identifier.
- `source_name`: human-readable source bucket name.
- `source_category`: source class, such as publisher platform, preprint index, conference platform, DOI lookup, or local library metadata.
- `search_interface`: search or reconciliation mode used for the source bucket.
- `query_string`: query family or metadata lookup rule used for the source bucket.
- `date_searched`: date when the source-specific ledger was frozen.
- `date_range`: publication or release-date range covered by the search ledger.
- `records_captured_before_dedup`: records captured in the ledger for this source bucket.
- `duplicates_or_variants_removed`: duplicate or superseded variants removed within the public ledger.
- `unique_candidate_records_after_dedup`: source records assigned to this source bucket after source-bucket deduplication and before canonical study/version consolidation.
- `core_records`, `supporting_records`, `background_records`, `excluded_records`: canonical analysis-use counts after study/version deduplication. Field names are retained for compatibility; in current manuscript terminology, `core_records` means study-level coded records and `supporting_records` means extended synthesis studies.
- `zotero_metadata_used`: whether local Zotero metadata was used for source reconciliation.
- `notes`: source-counting boundary notes.

## `data/source_screening_audit.csv`

This file records one source assignment and screening decision for each of the 253 source records in the screening ledger.

- `record_id`: stable candidate record identifier linked to `data/corpus.csv`.
- `title`, `year`: record title and year from corpus metadata.
- `source_bucket`, `source_name`: source bucket assigned from DOI/URL, venue/source, source type, and Zotero/reference metadata.
- `source_type`, `venue_or_source`, `doi_or_url`: corpus source fields copied for auditability.
- `corpus_layer`: legacy final analysis-use layer: `Core`, `Supporting`, `Background`, or `Excluded`; in current manuscript terms, `Core` maps to study-level coded records and `Supporting` maps to extended synthesis studies.
- `task_category`: coarse task family used during screening.
- `screening_decision`: layer-oriented screening decision.
- `deduplication_status`: deduplication status; `record_id` is the public candidate key.
- `source_trace_note`: explanation of source assignment and deduplication policy.


## `data/official_source_followup_20260716_search_log.csv`, `data/official_source_followup_20260716_screening_audit.csv`, and `OFFICIAL_SOURCE_FOLLOWUP_REPORT.md`

These files record the 2026-07-16 targeted official-source follow-up after the arXiv recall-recovery update. The check reviewed official conference/publisher sources for formal records corresponding to the update query families and exact-title probes. It matched PANGOLIN and FirmAgent to already integrated canonical records and introduced no new canonical candidate, study-level coded, extended-synthesis, background, or excluded records.

- `source_id`, `source_name`, `source_category`, `search_interface`, `query_string`, `date_searched`, `date_range`: source and query provenance for the targeted follow-up.
- `official_source_url`: public source page used for the check.
- `records_reviewed`, `existing_canonical_matches`, `new_candidate_records`, `new_study_level_additions`, `new_extended_synthesis_additions`, `new_background_or_excluded_records`: follow-up outcomes kept separate from the main source-count ledger.
- `match_status`, `screening_status`, `decision_reason`, `analytical_implication`: record-level decision fields explaining why each formal-source hit did or did not affect the current analytical corpus.

## `data/submission_update_20260715_screening_audit.csv`

This file records the submission-time arXiv sensitivity-search decisions. The later 37/4 author-confirmed resolution has been integrated into the current corpus and harmonized study-level matrix.

- `arxiv_id`, `title`, `published`, `official_url`, `query_ids`: normalized public arXiv metadata.
- `existing_record_id`: matching corpus record, or `NA`.
- `screening_status`: existing match, outside date window, potentially eligible update record, contextual/background update, or title/abstract exclusion.
- `screening_level`: identity, date, title/abstract, abstract-plus-metadata, or full-text review.
- `decision_reason`: record-level rationale.
- `analytical_implication`: whether the record changes the current analysis. Author and independent coding, author-confirmed adjudication, canonical matching, and corpus integration are complete; manuscript alignment is tracked separately.

## `data/submission_update_20260715_full_coding_audit.csv`

This file records the frozen author full-text audit of the 41 potentially eligible update-search records. It preserves the pre-review baseline used for agreement calculation.

- `arxiv_id`, `title`, `official_url`, `published`: public study identity and date.
- `review_material`, `full_text_status`: material and review level used for the author decision.
- `author_analysis_layer`: provisional study-level candidate pending independent review, or extended synthesis.
- `inclusion_rule_applied`: operational rule used to distinguish an observable Agentic workflow from adjacent static-analysis, management, or ecosystem material.
- `target_domain`, `lifecycle_coverage`, `primary_system_shape`: descriptive mapping fields.
- `agentic_capabilities`: multi-label capability coding using the current manuscript definitions.
- `strongest_evidence_output`: historical schema field name retained for compatibility; it stores the manuscript's principal reported evidence-output label.
- `external_traceability`: external-audit-material profile.
- `claim_boundary`, `author_decision_reason`, `uncertainty_note`: study-specific rationale and interpretation boundary.
- `formal_second_coder_status`: frozen pre-review status retained to document that this author file preceded the independent pass; current completion status is recorded in the results and agreement report.

## `data/submission_update_20260715_second_coder_blind_template.csv`

This file is the blank independent-review input for the 41 update records. It contains public identity fields and review instructions, but no `author_*`, original-label, agreement, or adjudication fields. All `coder2_*` fields remain blank so the workflow can be rerun.

- `update_id`, `arxiv_id`, `title`, `publication_status`: public record identity.
- `materials_to_review`: independent-review instruction and public material locator.
- `coder2_analysis_layer_decision`, `coder2_inclusion_reason`: independent screening decision and rationale.
- `coder2_lifecycle_coverage`, `coder2_primary_system_shape`: descriptive workflow coding.
- `coder2_cross_stage_capability_label`: independent multi-label capability coding.
- `coder2_strongest_evidence_output`: independent evidence-output label.
- `coder2_external_traceability_label`: independent external-traceability profile.
- `coder2_claim_boundary`, `coder2_uncertainty_note`: independent boundary rationale and uncertainty.

## `data/submission_update_20260715_second_coder_rerun_blind_template.csv`

Blank rerun template for the 41-record submission-update pass. It has the same coder2 fields as the original blind template, keeps all coder2 fields empty, and points the coder to `SUBMISSION_UPDATE_SECOND_CODER_RERUN_NOTES.md`. It is not a completed results file.

## `data/submission_update_20260715_second_coder_initial_results.csv`

Previous completed update-pass coder2 decisions retained for provenance before the tightened-boundary rerun was adopted. It is not the current reported update-pass agreement source.

## `data/submission_update_20260715_second_coder_results.csv`

This file contains the adopted tightened-boundary independent 41-record update-search pass. Its schema matches the rerun blind template, contains no `author_*` or `original_*` fields, and preserves coder2 labels, reasons, claim boundaries, and uncertainty notes.

## `reports/SUBMISSION_UPDATE_SECOND_CODER_PRE_ADJUDICATION_REPORT.md`

This report compares the frozen author audit with the completed independent pass. It reports single-label raw agreement and Cohen's kappa, plus row-level exact agreement, mean row Jaccard, micro F1, and per-label agreement for the multi-label fields. It reports no post-adjudication statistic.

## `data/submission_update_20260715_adjudication_working_draft.csv`

This file retains author, coder2, and proposed values side by side for analytical layer, lifecycle coverage, primary system shape, agentic capabilities, principal reported evidence output, external traceability, and claim boundary. `field_resolution_trace` records whether the proposal retains one input or applies an operational-rule harmonization. The file is a preserved working draft; final author-confirmed decisions are recorded in `data/submission_update_20260715_adjudicated.csv` and the current cross-round harmonization is recorded in `data/coding_round_harmonization_audit.csv`.

## `SUBMISSION_UPDATE_ADJUDICATION_SUMMARY.md` and `prepare_submission_update_adjudication.py`

The summary records the resolution rules and proposed 37/4 analytical-layer outcome. The script reproduces the working draft and pre-adjudication report from the frozen author and coder2 inputs. The final author-confirmed 37/4 outcome has since been integrated through the current corpus and harmonization files.

## `data/submission_update_20260715_adjudicated.csv`

This file preserves the author and coder2 inputs while recording the author-confirmed evidence-based resolution for all 41 update records. `adjudication_status` is `author_confirmed_evidence_based_resolution`. The finalization does not claim a discussion between two human coders, a third-coder decision, or a post-adjudication agreement statistic.

## `reports/SUBMISSION_UPDATE_ADJUDICATION_REPORT.md` and `finalize_submission_update_adjudication.py`

The report states the confirmation scope, 37/4 analytical-layer outcome, preservation boundary, and consensus limitation. The script deterministically promotes the reviewed working draft while leaving the author audit, coder2 result, and pre-adjudication report unchanged.

## `data/submission_update_20260715_canonical_integration_crosswalk.csv`

- `update_id`, `arxiv_id`, `title`, `authors`, `official_url`, `doi`: public update-study identity.
- `adjudicated_analytical_layer`: confirmed study-level or extended-synthesis assignment.
- `matched_existing_record_id`, `match_basis`, `best_existing_title`: canonical identity evidence against the frozen corpus.
- `proposed_canonical_study_id`, `integration_status`, `counted_after_integration`: integration decision later reflected in the current corpus files.
- `integration_note`: provenance note for how the update records entered the integrated current corpus.

## `SUBMISSION_UPDATE_CANONICAL_INTEGRATION_REPORT.md` and `prepare_submission_update_canonical_integration.py`

The report records the exact-identifier/title comparison and corpus impact. All 41 update records are new canonical studies under the current matching rules, yielding the integrated totals of 253 source records and 248 canonical studies now reflected in the coding matrices, distributions, and manuscript text.

## `data/submission_update_20260715_study_level_additions.csv`

This file contains the 37 update studies added to the current study-level set. It uses current workflow, system-shape, capability, evidence-output, external-traceability, and claim-boundary fields. Legacy A/E fields are not created for these studies.

## `data/current_synthesis_statistics.csv`

This file reports combined descriptive counts for 67 target-software studies across lifecycle coverage, agentic capabilities, and principal reported evidence output. The governance boundary case is included only in the evidence-output total where explicitly labeled. `baseline_count` and `update_addition_count` preserve the two-cohort arithmetic.

## `SUBMISSION_UPDATE_CORPUS_INTEGRATION_REPORT.md` and `integrate_submission_update_corpus.py`

The report records the completed 253-source-record / 248-canonical-study integration and the 67+1 denominator policy. The deterministic script expands the source ledger, canonical crosswalk, reference audit, current-field additions, extended synthesis, mapping views, and current descriptive statistics while preserving the legacy 31-record coding files and both rounds of reliability results.

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




## `data/study_version_crosswalk.csv`

This file links the 253 source records to 248 canonical studies. It preserves version history while preventing preprints, conference versions, exact duplicates, or source variants of the same study from being counted twice.

- `record_id`: source-record identifier from `data/corpus.csv`.
- `title`: source-record title.
- `canonical_study_id`: stable canonical study identifier.
- `canonical_record_id`: source record selected as the counted canonical record. Formal or official versions are preferred when available.
- `version_type`: `preprint`, `conference_version`, `journal_version`, `project_report`, `exact_duplicate`, or `other`.
- `source_version`: public source, DOI, URL, arXiv, or venue evidence used for version tracking.
- `same_study_as`: canonical record for alternate versions, or `NA` for counted canonical records.
- `dedup_basis`: title, DOI, arXiv ID, URL, or source-variant evidence used for linking versions.
- `analytical_layer`: canonical analytical use: `study_level_coded`, `extended_synthesis`, `background_reference`, `excluded_near_neighbor`, or `alternate_version`.
- `counting_status`: `canonical_counted`, `alternate_version_not_counted`, `exact_duplicate_removed`, `source_variant_not_counted`, or `needs_manual_review`.
- `retained_reason`: reason the canonical version is counted or the alternate version is retained only for provenance.
- `notes`: audit note.

## `data/extended_synthesis_audit.csv`

This file provides a lightweight, record-level synthesis-use audit for the 65-study canonical extended synthesis set. It complements the study-level workflow--capability--evidence coding used for 67 target-software studies plus one governance boundary case.

- `record_id`: stable identifier linked to `data/corpus.csv`.
- `citation_key`: bibliography key extracted from the public reference audit when available; `NA` means no key was recorded in the source note.
- `title`: record title.
- `material_type`: normalized public material type, such as `conference_paper`, `journal_article`, or `preprint_or_arxiv`.
- `primary_synthesis_role`: unique controlled role for the record. Allowed values are `lower_level_primitive`, `adjacent_candidate_analysis`, `adjacent_fuzzing_or_testing`, `benchmark_or_evaluation`, `agent_orchestration`, `governance_or_safety`, and `evidence_or_reproducibility`.
- `secondary_synthesis_roles`: optional semicolon-separated supporting roles from the same vocabulary, or `NA`.
- `rq_contribution`: main manuscript use: `RQ1`, `RQ2_context`, `evaluation_agenda`, or `governance_agenda`.
- `manuscript_section_use`: section-level location where the record contributes to synthesis.
- `extracted_contribution`: concise contribution extracted for thematic synthesis; it must be more specific than generic context.
- `reason_not_study_level_coded`: why the record remains outside the full study-level coded set.
- `public_material_basis`: public metadata, source, and locator supporting the audit row.
- `reviewer_note`: boundary note explaining that this is lightweight synthesis-use audit rather than full coding.

Positive examples: an LLM-guided fuzzing paper without full study-level trace fields can be `adjacent_fuzzing_or_testing`; a benchmark or empirical-evaluation paper can be `benchmark_or_evaluation`; a reproduction or patch-validation adjacent work can be `evidence_or_reproducibility`. Negative examples: a general scoping-review method paper, a traditional tool definition, or a product page that only supports ecosystem context should remain in the background/reference or product-ecosystem layer rather than this file.


## `data/corpus_layer_audit.csv`

- `record_id`: link to `corpus.csv`.
- `title`: record title as used in the local corpus.
- `year`: publication or release year from local metadata.
- `source_type`: local source type.
- `publication_status`: working publication-status audit field.
- `original_layer`: layer in the original public-minimal corpus.
- `supplemental_layer`: supplemental analysis layer, including `Analytical Core`, `Supporting`, `Background Context`, and `Excluded`.
- `task_category`: coarse task family used during screening.
- `is_analytical_core`: whether the record is part of the current 68-record study-level coded set.
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
- `publication_status`: publication/material status only. Current allowed values in the 31-record study-level coded second-coder files include `not_publicly_available`, `preprint_or_arxiv_from_local_metadata`, `arXiv preprint`, `journal article`, `preprint/project page`, `verified_by_official_source`, and `peer_reviewed`. This field must not encode boundary role.
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


## `data/core31_second_coder_capability_traceability_blind_template.csv`

This blank blind template is retained for future reruns of the independent review of two auxiliary fields: cross-stage capability and external traceability / external audit material. It contains 31 rows, hides all `original_*` fields, and leaves coder2 fields blank. Because the capability field can be multi-label, agreement for completed results uses per-label, Jaccard-style, or other suitable multi-label metrics rather than forcing a single-label Cohen's kappa.

- `core_id`, `record_id`, `system_alias`, `title`, `publication_status`, `boundary_role`, `materials_to_review`: blind review identifiers and non-sensitive review instructions.
- `coder2_cross_stage_capability_label`: blank future coder2 label for cross-stage capability.
- `coder2_capability_decision_reason`: blank future rationale field.
- `coder2_capability_uncertainty_note`: blank future uncertainty field.
- `coder2_external_traceability_label`: blank future coder2 label for external traceability / external audit material.
- `coder2_external_traceability_decision_reason`: blank future rationale field.
- `coder2_external_traceability_uncertainty_note`: blank future uncertainty field.

## `data/core31_second_coder_capability_traceability_results.csv`

This file contains the completed formal second-coder results for cross-stage capability and external traceability / external audit material. It has 31 rows, contains no `original_*` fields, and preserves coder2 labels, rationales, and uncertainty notes.

## `reports/SECOND_CODER_CAPABILITY_TRACEABILITY_AGREEMENT_REPORT.md`

This report is generated from the author baseline in `data/v13_core_synthesis_matrix.csv` and the completed coder2 decisions in `data/core31_second_coder_capability_traceability_results.csv`. It reports row-level exact agreement, mean row Jaccard, micro precision/recall/F1 over label assignments, and per-label agreement/Jaccard. It does not use single-label Cohen's kappa for the multi-label capability field.

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
- `count`: count for the current source-specific ledger or final corpus layer.
- `note`: explanation, source boundary, or screening-stage condition.

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

Manuscript citation count is not a corpus statistic. The earlier reference-list expansion cited rows already present in the corpus; the 2026-07-15 update is instead recorded as a separate, fully screened and coded integration. Current totals are 253 source records, 248 canonical studies, 68 study-level coded records, 65 extended synthesis studies, 95 Background references, and 20 Excluded near-neighbor studies.


## `data/mapping_snapshot_counts.csv`

This file records descriptive mapping views used by the current manuscript. The counts describe the manuscript corpus and product boundary snapshot only; they are not field-level prevalence estimates.

- `view`: mapping view, such as `year_distribution`, `source_type_distribution`, or `task_facet_distribution`.
- `category`: category displayed in the manuscript mapping view.
- `count`: count for the category.
- `denominator`: counting scope, such as 253 source records, the independent product snapshot layer, 67 target-software studies, the 68-record coded set including the governance boundary case, or the 65-study extended synthesis set.
- `scope_note`: boundary note explaining that the count is descriptive rather than a prevalence estimate.

## `data/product_ecosystem_snapshot.csv`

This file is an independent product-ecosystem boundary data layer. Rows in this file are not part of `data/corpus.csv`, do not count toward the 253 source records, and do not alter study-level coded aggregate statistics. Product materials that also support manuscript background or extended-synthesis discussion are represented separately in `data/reference_audit.csv`. Public vendor/project materials are recorded as source-limited ecosystem evidence.

- `product_or_system`: public product, model, workflow, policy, or attempted source check.
- `vendor`: vendor or organization associated with the material.
- `snapshot_date`: global product-ecosystem snapshot date, currently 2026-06-29.
- `model_or_version`: public model, version, release, or availability detail when visible; `NA` if not applicable.
- `public_capabilities`: high-level public capability description from official sources.
- `security_workflow`: security-relevant workflow or boundary described by the source.
- `public_evidence_type`: material type, such as product page, developer documentation, help page, vendor blog, model page, policy page, or excluded attempted source.
- `source_url`: official public source URL; `NA` if no reliable official source was captured.
- `publication_or_update_date`: publication, update, or explicit page date when available; otherwise a no-date note.
- `access_date`: date the individual source was accessed for this snapshot; row-level access dates can differ from the global snapshot date when a source was checked earlier in the same update cycle.
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

Product and policy pages added for the product-ecosystem snapshot are also listed there when DOI is not applicable. These rows record `doi_not_applicable_product_page` or equivalent status and do not change the 253-record research corpus or the 68-record study-level coded set.

Rows already audited with DOI or official URL in `reference_audit.csv` are not duplicated in `doi_remaining_manual_status.csv` merely because they are newly cited in a manuscript draft.

## Intercoder Files

`data/core31_second_coder_formal_blind_template.csv` is the blank formal second-coder input for future strongest-evidence-output reruns. `data/core31_second_coder_formal_results.csv` contains the completed formal strongest-evidence-output second-coder pass and no `original_*` fields. `reports/FORMAL_SECOND_CODER_AGREEMENT_REPORT.md` reports formal pre-adjudication agreement against `data/core31_second_coder_adjudication_template.csv`. `data/core31_second_coder_capability_traceability_blind_template.csv` is a blank extension template for future cross-stage capability and external-traceability reruns. `data/core31_second_coder_capability_traceability_results.csv` contains the completed extension second-coder results and no `original_*` fields. `reports/SECOND_CODER_CAPABILITY_TRACEABILITY_AGREEMENT_REPORT.md` reports set-style and per-label agreement for those fields. `data/core31_second_coder_blind.csv` is also kept blank as a blind workflow template.

`archive/pilot_second_coder_round_1/` preserves the pilot round for calibration only; its raw agreement and kappa should not be cited as formal reliability. Formal strongest-evidence-output reliability statistics are reported in `reports/FORMAL_SECOND_CODER_AGREEMENT_REPORT.md`; cross-stage capability and external-traceability extension agreement is reported separately in `reports/SECOND_CODER_CAPABILITY_TRACEABILITY_AGREEMENT_REPORT.md`.

`data/intercoder_sample_blind.csv` is an optional sampled-review worksheet. `data/intercoder_sample_key.csv` is private and not included in the public artifact.

`data/disagreement_resolution_template.csv` records coder decisions, adjudicated decisions, rationales, and resolution metadata if a separate adjudication worksheet is later used.

## Metadata Field Status

`NA` means one of the following:

- not applicable to the record;
- not recoverable from local records;
- intentionally withheld from the minimal public artifact;
- awaiting official-source reconciliation.

Do not infer a missing value from surrounding rows without recording the source and rationale.


## Record classification audit fields
`final_decision`, `decision_reason`, and `stats_treatment` in `data/literature_update_decisions.csv` preserve the provenance of Core / Supporting / Background / Excluded decisions (legacy artifact labels; Supporting corresponds to the source-record layer from which the canonical extended synthesis set is derived) for the seven high-relevance records. The manuscript-facing classification summary is provided in `data/record_classification_audit.csv`, and these decisions are reflected in the current canonical stratification through `data/study_version_crosswalk.csv`.

## data/core_reproducibility_audit.csv

Per-Core public-material audit linked by `core_id`. Private Zotero paths are excluded. Status fields distinguish public artifact visibility, target version, environment, replay/PoC/PoV material, structured trace, author-reported external traces, publicly traceable external material, and claim-level alignment.




## submission_update_20260715_rerun_sensitivity_analysis.csv
Label-count sensitivity analysis for the July 15 update-search rerun. It compares author-confirmed final labels with rerun second-coder labels for analytical layer, primary system shape, principal reported evidence output, external traceability, lifecycle coverage, and agentic capability labels. It is a sensitivity/audit file, not a replacement for the harmonized coding matrix.

## publication_status_standardized.csv
Standardized publication-status view for the current study-level coding matrix. Allowed manuscript-facing values are `journal`, `conference`, `workshop`, `preprint`, and `benchmark/system report`. The table is used for appendix display and source-status sensitivity summaries; legacy source-specific status fields remain in older audit files for traceability.

## publication_status_distribution_by_layer.csv
Publication-status distribution summary for the target-software study-level set. It reports evidence-output counts, primary-shape counts, failure-reuse labels, and governance/human-gate labels by standardized publication status.

## publication_status_sensitivity_analysis.csv
Publication-status sensitivity view derived from `publication_status_standardized.csv`. It reports counts, denominators, and shares for the four primary system shapes, five principal reported evidence outputs, seven cross-stage capabilities, and external-traceability categories. `peer_reviewed` combines conference, journal, and workshop records; `preprint` retains the standardized preprint category. The three benchmark/system reports remain visible in the complete-set totals and in `publication_status_distribution_by_layer.csv`, but are not folded into either comparison subset.

- `scope`: fixed target-software denominator.
- `publication_status_group`: `all_target_software`, `peer_reviewed`, or `preprint`.
- `dimension`, `label`: coded dimension and controlled label.
- `count`, `denominator`, `share`: directly reproduced frequency, group size, and proportion.


## `data/representative_reported_results.csv`
Source-located audit file for the representative reported-results table in Appendix B/Table 13. Each row corresponds to one manuscript table row and records the system, citation key, primary shape, evaluation setting, reported scale/result, validation material, source location, and extraction note. The file is descriptive and does not normalize or rank results across systems.

## `data/empirical_reporting_extraction.csv`

One source-scoped row for each of the 67 target-software studies. This table is parallel to the coding matrix and does not add or revise lifecycle, capability, shape, evidence-output, or claim-boundary labels.

- `matrix_id`, `record_id`, `system`, `citation_key`: links to the current study-level matrix and reference audit.
- `primary_shape`: copied from the harmonized study-level matrix for grouped summaries.
- `evaluation_setting`: concise target or task setting used in the study evaluation.
- `agent_mechanism`: observable control functions derived from the coded cross-stage capabilities.
- `*_status`: whether the reviewed public material reports the named item; controlled values are `reported` and `not located`.
- `reported_result`: source-scoped result summary. Quantitative units retain the original study definition.
- `validation_material`: executable, benchmark, runtime, or other validation material associated with the reported result.
- `source_location`: reviewed paper pages/sections and field-specific locator where available.
- `extraction_note`: interpretation rule; reporting status is not a performance score.

## `data/empirical_reporting_completeness.csv`

Counts recomputed from `data/empirical_reporting_extraction.csv` for the full 67-study set and each primary system shape.

- `scope`: all target-software studies or one primary system shape.
- `reporting_item`: model/version, evaluation scale, quantitative result, baseline, validation material, runtime, cost, ablation, or failure reporting.
- `reported_n`, `denominator`, `reported_share`: source-located reporting count and proportion within the scope.

## `data/traditional_security_primitives.csv`

One source-located row for each of the 67 target-software studies. This author-audited extraction supports RQ1 and is separate from the five coded workflow/evidence fields and the qualitative claim-boundary note.

- `matrix_id`, `system`: links to the harmonized study-level matrix.
- `primitive_tags`: semicolon-delimited labels from seven families: `static_taint_specification`, `fuzzing_input_harness`, `symbolic_constraint`, `runtime_oracle`, `replay_poc_pov`, `patch_build_test`, and `recon_scan_pentest`.
- `named_tools`: tools or execution mechanisms explicitly used in the study; `not specified` is used when the public material does not name one.
- `source_location`: public-paper location supporting the extraction.
- `extraction_note`: scope rule excluding related-work mentions and unsupported inference.

## `data/unified_second_coder_per_label_reliability.csv`

Per-label binary agreement for the 67 target-software studies in the complete independent review.

- `field`, `label`, `scope_n`: coding dimension, controlled label, and denominator.
- `author_positive_n`, `coder2_positive_n`: positive assignments under the harmonized author matrix and complete independent coding.
- `raw_agreement_n`, `raw_agreement`: binary agreement count and proportion for the label.
- `cohens_kappa`: label-specific Cohen's kappa; these values complement rather than replace row-level Jaccard and micro-F1 for the multi-label fields.
