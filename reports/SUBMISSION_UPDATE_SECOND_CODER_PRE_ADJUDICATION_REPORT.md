# Submission Update Second-Coder Pre-Adjudication Report

## Scope

- Update date: 2026-07-15
- Independently coded records: 41
- Inputs: `data/submission_update_20260715_full_coding_audit.csv` and `data/submission_update_20260715_second_coder_results.csv`
- Status: pre-adjudication agreement from completed independent labels

The completed blind pass contains all 41 decisions and does not expose author labels. Agreement below compares the frozen author audit with the independent coder2 results before any resolution. The proposed resolution is stored separately as a working draft and is not reported as human consensus.

## Single-Label Fields

| Field | Agreement | Raw agreement | Cohen's kappa | Disagreement rows |
|---|---:|---:|---:|---|
| Analysis layer | 40 / 41 | 0.976 | 0.844 | U24 |
| Primary system shape | 27 / 41 | 0.659 | 0.514 | U01, U02, U03, U04, U05, U06, U07, U08, U10, U11, U15, U24, U39, U40 |
| Strongest evidence output | 28 / 41 | 0.683 | 0.566 | U01, U03, U04, U09, U14, U17, U21, U24, U26, U27, U36, U37, U39 |
| External traceability | 25 / 41 | 0.610 | 0.320 | U02, U03, U04, U07, U09, U14, U16, U17, U18, U20, U22, U29, U30, U32, U35, U37 |

## Multi-Label Fields

| Field | Row-level exact | Mean row Jaccard | Micro F1 |
|---|---:|---:|---:|
| Lifecycle coverage | 4 / 41 = 0.098 | 0.667 | 0.794 |
| Agentic capabilities | 9 / 41 = 0.220 | 0.760 | 0.865 |

`path exploration` in the author audit is normalized to the frozen label `path and input exploration` before comparison. Row-level exact agreement is intentionally strict; Jaccard and micro F1 capture overlap among secondary labels.

### Per-Label Raw Agreement

| Lifecycle label | Agreement |
|---|---:|
| candidate analysis | 0.780 |
| path and input exploration | 0.780 |
| execution observation | 0.829 |
| reproduction and validation | 0.732 |
| patch validation | 0.976 |
| reporting and audit | 0.561 |

| Agentic-capability label | Agreement |
|---|---:|
| context aggregation / rule extraction | 0.902 |
| tool routing / strategy routing | 0.780 |
| feedback interpretation / loop adjustment | 0.878 |
| validation organization / evidence packaging | 0.829 |
| long-horizon state management | 0.732 |
| failure reuse / strategy update | 0.902 |
| governance / human gates / disclosure control | 0.878 |


## Interpretation

- The analytical-layer boundary is stable except for U24 (SynthFix).
- Lifecycle differences are concentrated in whether ordinary result packaging counts as `reporting and audit`, and whether input generation or patch checks constitute separate lifecycle stages.
- Capability differences are concentrated in strict thresholds for long-horizon state, dynamic tool routing, failure reuse, and governance controls.
- Evidence-output and traceability differences primarily concern whether public artifacts are reproducibility material or whether item-level external alignment is available.

No adjudicated labels or post-adjudication agreement statistic are claimed in this report.
