# Third-Party Rereview Completion Record (supersedes the historical 2026-08-12 summary)

## Scope

- Study-level denominator: 199 target-software studies.
- Independent field-level disagreements: 410.
- OY external rereview tasks: 460 (410 disagreements + 50 hidden-reference QC rows).
- Integrated third-party decisions: 410.
- QC rows retained separately: 50.
- Pending decisions: 0.
- Unresolved decisions: 0.

## Procedure

Two coders independently assigned lifecycle coverage, cross-stage capability, primary system shape, principal reported evidence output, and external traceability. OY performed an external rereview of the disagreement and QC task package against the prespecified codebook and cited source evidence. Before the initial independent rereview OY had not seen this manuscript, the first-round materials, or old adjudication results; later material-identity corrections and targeted feedback were disclosed. We therefore report this as external third-party rereview, not fully blinded adjudication.

LLM-assisted preparation and deterministic scripts were limited to material assembly, task--study--field--PDF cross-checking, SHA-256 calculation, table validation, and count regeneration. OY read the supplied material and entered every task judgment. The integration validator confirms 460 unique tasks, 410 disagreement and 50 QC strata, 196 unique studies represented by those tasks, the complete 199-study coder-to-matrix identity crosswalk, legal labels and nonempty evidence locators, and all seven corrected-material task paths.

The review applied the rules in `docs/review/ADJUDICATION_RULES_20260812.md`: operational definitions control; benchmark ground truth is not external confirmation; author-reported CVE, CNVD, vendor, maintainer, or bounty material is an external clue unless a concrete system result aligns with a concrete public external record; multi-label fields retain only explicitly shown labels; and evidence-insufficient cases would have been recorded as unresolved. No unresolved case remained after review.

## Outputs And Reporting Boundary

- `data/adjudication/third_party_rereview_oy_20260824.csv` is the raw 460-row OY export.
- `data/adjudication/third_party_rereview_decisions_20260824.csv` preserves the integrated 410 decisions and the five historical completed-form fields in `prior_form_*` columns; `data/adjudication/third_party_rereview_qc_20260824.csv` preserves the separate 50 QC rows.
- `data/coding/adjudicated_study_level_coding_matrix_199.csv` is the sole source for final descriptive distributions.
- `data/adjudication/adjudication_log_199_all_fields.csv` preserves the decision path for all 995 controlled study-field assignments.
- `data/derived/derived_summary_tables.json` contains the final counts and shares under the original table name `adjudicated_synthesis_statistics_199.csv`, together with the completion manifest in `metadata.adjudication_completion_manifest`.
- `data/coding/current_study_level_coding_matrix_harmonized.csv` and `data/adjudication/integrated_199_second_coder_comparison_20260730.csv` remain preserved pre-adjudication sources.

Agreement statistics, including raw agreement, Cohen's kappa, and AC1, describe the independent assignments before adjudication. The adjudicated matrix is not a new reliability test.

The prior author-confirmed harmonized matrix had been carried forward as if it were the final adjudicated layer, which explains the formerly identical primary-coder and final marginal counts. OY's rereview decisions now replace that layer without modifying either coder's raw assignments. None of the 26 substantive label margins across the five rereviewed fields is identical to the corresponding primary-coder margin.

## Integrated Independent-Coder Agreement

The calculation combines the released 67-study review with 132 studies jointly included from the final multi-source search. Both cohorts use the same controlled label vocabulary. This is the independent assignment record before external rereview; final descriptive distributions are reported separately from the adjudicated matrix.

| Cohort | Target-software studies |
|---|---:|
| Released study set | 67 |
| Final multi-source search | 132 |
| Integrated set | 199 |

| Single-label field | Raw agreement | Cohen's kappa |
|---|---:|---:|
| primary shape | 0.884 | 0.843 |
| principal evidence | 0.759 | 0.665 |
| external traceability | 0.724 | 0.448 |

| Multi-label field | Row exact | Mean row Jaccard | Micro F1 |
|---|---:|---:|---:|
| lifecycle | 0.261 | 0.726 | 0.831 |
| capability | 0.312 | 0.782 | 0.874 |

Eligibility agreement for the new search is reported separately because the released 67-study set had already passed inclusion before its unified second-coder review. The integrated reliability result therefore covers analytical coding fields only and does not score claim-boundary prose by exact textual agreement.

The underlying files are data/adjudication/integrated_199_second_coder_comparison_20260730.csv, data/adjudication/integrated_199_per_label_reliability_20260730.csv, data/adjudication/third_party_rereview_decisions_20260824.csv, data/adjudication/adjudication_log_199_all_fields.csv, and data/coding/adjudicated_study_level_coding_matrix_199.csv.

## Final Key Counts

- Reporting and audit: 43/199.
- No qualifying lifecycle label observed: 10/199.
- Validation organization / evidence packaging: 69/199.
- No qualifying cross-stage capability observed: 65/199.
- Externally traceable material as principal output: 3/199.
- Publicly aligned external trace: 4/199.

The four retained public-alignment rows were checked separately from the MALF correction: Code-Augur's paper-level Bug 2 mapping corresponds to CVE-2026-48113; Agentic Fuzzing identifies a concrete Chromium issue/CVE record; QRS identifies a concrete package/CVE and maintainer-patch record; and STITCH prints a concrete issue/GHSA link. FunFuzz was downgraded to an author-reported external clue because its local paper describes an anonymous fingerprint-to-issue map without exposing a concrete item-level public record, and the linked host returned an access challenge. That network result was not treated as evidence that the paper's mapping is false; it simply fails the strict public-alignment rule. None of the four retained rows rests only on an unlocated identifier analogous to CNVD-2024-16009.
