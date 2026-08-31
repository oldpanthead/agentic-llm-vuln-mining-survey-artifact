# Third-Party Rereview Completion Record (supersedes the historical 2026-08-12 summary)

## Scope

- Study-level denominator: 199 target-software studies.
- Independent field-level disagreements: 410.
- OY external rereview tasks: 410.
- Integrated third-party decisions: 410.
- Post-adjudication evidence corrections: 3 (U17/FunFuzz: two; C11/MALF: one official-record check).
- Pending decisions: 0.
- Unresolved decisions: 0.

## Procedure

Two coders independently assigned lifecycle coverage, cross-stage capability, primary system shape, principal reported evidence output, and external traceability. OY performed an external rereview of the 410 disagreement units against the prespecified codebook and cited source evidence. Before the initial independent rereview OY had not seen this manuscript, the first-round materials, or old adjudication results; later material-identity corrections and targeted feedback were disclosed. We therefore report this as external third-party rereview, not fully blinded adjudication.

LLM-assisted preparation and deterministic scripts were limited to material assembly, task--study--field--PDF cross-checking, SHA-256 calculation, table validation, and count regeneration. OY read the supplied material and entered every task judgment. The integration validator confirms 410 unique disagreement tasks, 196 unique studies represented by those tasks, the complete 199-study coder-to-matrix identity crosswalk, legal labels and nonempty evidence locators, and all seven corrected-material task paths. The two initial assignments agreed on 585 of the 995 study--field units. Two U17 (FunFuzz) agreements were later corrected through targeted evidence checks, leaving 583 unchanged agreement rows. OY rereviewed the 410 disagreement units; 409 were retained under the OY-rereview tag and one C11 (MALF) external-traceability decision was later corrected through an official-record check. The final field log consequently contains 583 `agreed_assignment` rows, 409 `third_party_external_rereview` rows, and three `post_adjudication_evidence_correction` rows.

The review applied the rules in `docs/review/ADJUDICATION_RULES_20260812.md`: operational definitions control; benchmark ground truth is not external confirmation; author-reported CVE, CNVD, vendor, maintainer, or bounty material is an external clue unless a concrete system result aligns with a concrete public external record; multi-label fields retain only explicitly shown labels; and evidence-insufficient cases would have been recorded as unresolved. No unresolved case remained after review.

## Outputs And Reporting Boundary

- `data/adjudication/third_party_rereview_decisions_20260824.csv` preserves the integrated 410 OY decisions.
- `data/coding/adjudicated_study_level_coding_matrix_199.csv` is the sole source for final descriptive distributions.
- `data/adjudication/adjudication_log_199_all_fields.csv` preserves the decision path for all 995 controlled study-field assignments, including two U17 post-adjudication evidence corrections and one C11 (MALF) official-record correction.
- `data/derived/derived_summary_tables.json#adjudicated_synthesis_statistics_199.csv` provides the final counts and shares.
- `data/coding/current_study_level_coding_matrix_harmonized.csv` and `data/adjudication/integrated_199_second_coder_comparison_20260730.csv` remain preserved pre-adjudication sources.

Agreement statistics, including raw agreement, Cohen's kappa, and AC1, describe the independent assignments before adjudication. The adjudicated matrix is not a new reliability test. The separate random 50-study sample by Rong Zhoujie is an external interpretability check; it diagnoses rule boundaries and is not a gold-standard accuracy estimate or a validation of the complete final matrix.

The record-level Rong check is released as `data/adjudication/rong_external_interpretability_check_50.csv`. It contains 200 field rows for the fixed 50-study sample, with 49 comparable records per field after excluding the unresolved CP209 rows. Its reference labels come from the preserved pre-adjudication harmonized matrix, so the check should not be read as a reliability estimate for the final adjudicated matrix.

The prior author-confirmed harmonized matrix had been carried forward as if it were the final adjudicated layer, which explains the formerly identical primary-coder and final marginal counts. OY's rereview decisions now replace that layer without modifying either coder's raw assignments. None of the 26 substantive label margins across the five rereviewed fields is identical to the corresponding primary-coder margin.

## Final Key Counts

- Reporting and audit: 43/199.
- No qualifying lifecycle label observed: 10/199.
- Validation organization / evidence packaging: 69/199.
- No qualifying cross-stage capability observed: 65/199.
- Externally traceable material as principal output: 3/199.
- Publicly aligned external trace: 4/199.

The four retained public-alignment rows were checked separately from the MALF correction: Code-Augur's paper-level Bug 2 mapping corresponds to CVE-2026-48113; Agentic Fuzzing identifies a concrete Chromium issue/CVE record; QRS identifies a concrete package/CVE and maintainer-patch record; and STITCH prints a concrete issue/GHSA link. FunFuzz was downgraded to an author-reported external clue because its local paper describes an anonymous fingerprint-to-issue map without exposing a concrete item-level public record, and the linked host returned an access challenge. That network result was not treated as evidence that the paper's mapping is false; it simply fails the strict public-alignment rule. None of the four retained rows rests only on an unlocated identifier analogous to CNVD-2024-16009.
