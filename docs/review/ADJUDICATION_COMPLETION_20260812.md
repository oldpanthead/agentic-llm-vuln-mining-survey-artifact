# Third-Party Rereview Completion Record (supersedes the historical 2026-08-12 summary)

## Scope

- Study-level denominator: 199 target-software studies.
- Independent field-level disagreements: 410.
- OY external rereview tasks: 460 (410 disagreements + 50 hidden-reference QC rows).
- Integrated third-party decisions: 410.
- QC rows retained separately: 50.
- Pending decisions: 0.
- Unresolved decisions: 0.

The 50 QC rows are retained as process diagnostics only. They were hidden-reference tasks intended to expose material-mapping or rule-application problems; their reference labels were earlier coder assignments, not an independent gold standard, and the rows were not sampled as a random post-adjudication reliability set. Agreement with them must not be reported as OY accuracy. They do not enter the final matrix or any synthesis count.

## Procedure

Two coders independently assigned lifecycle coverage, cross-stage capability, primary system shape, principal reported evidence output, and external traceability. OY performed an external rereview of the disagreement and QC task package against the prespecified codebook and cited source evidence. Before the initial independent rereview OY had not seen this manuscript, the first-round materials, or old adjudication results; later material-identity corrections and targeted feedback were disclosed. We therefore report this as external third-party rereview, not fully blinded adjudication.

LLM-assisted preparation and deterministic scripts were limited to material assembly, task--study--field--PDF cross-checking, SHA-256 calculation, table validation, and count regeneration. OY read the supplied material and entered every task judgment. The integration validator confirms 460 unique tasks, 410 disagreement and 50 QC strata, 196 unique studies represented by those tasks, the complete 199-study coder-to-matrix identity crosswalk, legal labels and nonempty evidence locators, and all seven corrected-material task paths.

The review applied the rules in `adjudication/ADJUDICATION_RULES_20260812.md`: operational definitions control; benchmark ground truth is not external confirmation; author-reported CVE, CNVD, vendor, maintainer, or bounty material is an external clue unless a concrete system result aligns with a concrete public external record; multi-label fields retain only explicitly shown labels; and evidence-insufficient cases would have been recorded as unresolved. No unresolved case remained after review.

## Outputs And Reporting Boundary

- `third_party_rereview_oy_20260824.csv` is the raw 460-row OY export.
- `data/third_party_rereview_decisions_20260824.csv` and `data/third_party_rereview_qc_20260824.csv` preserve the integrated 410 decisions and separate 50 QC rows.
- `data/adjudicated_study_level_coding_matrix_199.csv` is the sole source for final descriptive distributions.
- `data/adjudication_log_199_all_fields.csv` preserves the decision path for all 995 controlled study-field assignments.
- `data/adjudicated_synthesis_statistics_199.csv` provides the final counts and shares.
- `data/current_study_level_coding_matrix_harmonized.csv` and `data/integrated_199_second_coder_comparison_20260730.csv` remain preserved pre-adjudication sources.

Agreement statistics, including raw agreement, Cohen's kappa, and AC1, describe the independent assignments before adjudication. The adjudicated matrix is not a new reliability test. The hidden-reference QC rows are likewise not a reliability estimate; they are preserved to document the process check and its limitations. The separate random 50-study sample by Rong Zhoujie is an external interpretability check; it diagnoses rule boundaries and is not a gold-standard accuracy estimate or a validation of the complete final matrix.

The prior author-confirmed harmonized matrix had been carried forward as if it were the final adjudicated layer, which explains the formerly identical primary-coder and final marginal counts. OY's rereview decisions now replace that layer without modifying either coder's raw assignments. None of the 26 substantive label margins across the five rereviewed fields is identical to the corresponding primary-coder margin.

## Final Key Counts

- Reporting and audit: 43/199.
- No qualifying lifecycle label observed: 10/199.
- Validation organization / evidence packaging: 69/199.
- No qualifying cross-stage capability observed: 65/199.
- Externally traceable material as principal output: 3/199.
- Publicly aligned external trace: 4/199.

The four retained public-alignment rows were checked separately from the MALF correction: Code-Augur's paper-level Bug 2 mapping corresponds to CVE-2026-48113; Agentic Fuzzing identifies a concrete Chromium issue/CVE record; QRS identifies a concrete package/CVE and maintainer-patch record; and STITCH prints a concrete issue/GHSA link. FunFuzz was downgraded to an author-reported external clue because its local paper describes an anonymous fingerprint-to-issue map without exposing a concrete item-level public record, and the linked host returned an access challenge. That network result was not treated as evidence that the paper's mapping is false; it simply fails the strict public-alignment rule. None of the four retained rows rests only on an unlocated identifier analogous to CNVD-2024-16009.
