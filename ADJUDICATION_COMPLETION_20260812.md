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

The review applied the rules in `adjudication/ADJUDICATION_RULES_20260812.md`: operational definitions control; benchmark ground truth is not external confirmation; author-reported CVE, CNVD, vendor, maintainer, or bounty material is an external clue unless a concrete system result aligns with a concrete public external record; multi-label fields retain only explicitly shown labels; and evidence-insufficient cases would have been recorded as unresolved. No unresolved case remained after review.

## Outputs And Reporting Boundary

- `third_party_rereview_oy_20260824.csv` is the raw 460-row OY export.
- `data/third_party_rereview_decisions_20260824.csv` and `data/third_party_rereview_qc_20260824.csv` preserve the integrated 410 decisions and separate 50 QC rows.
- `data/adjudicated_study_level_coding_matrix_199.csv` is the sole source for final descriptive distributions.
- `data/adjudication_log_199_all_fields.csv` preserves the decision path for all 995 controlled study-field assignments.
- `data/adjudicated_synthesis_statistics_199.csv` provides the final counts and shares.
- `data/current_study_level_coding_matrix_harmonized.csv` and `data/integrated_199_second_coder_comparison_20260730.csv` remain preserved pre-adjudication sources.

Agreement statistics, including raw agreement, Cohen's kappa, and AC1, describe the independent assignments before adjudication. The adjudicated matrix is not a new reliability test.

## Final Key Counts

- Reporting and audit: 43/199.
- No qualifying lifecycle label observed: 10/199.
- Validation organization / evidence packaging: 69/199.
- No qualifying cross-stage capability observed: 65/199.
- Externally traceable material as principal output: 4/199.
- Publicly aligned external trace: 5/199.
