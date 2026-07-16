# Submission Update Second-Coder Pre-Adjudication Report

## Scope

- Update date: 2026-07-15
- Independently coded records: 41
- Inputs: `data/submission_update_20260715_full_coding_audit.csv` and `data/submission_update_20260715_second_coder_results.csv`
- Status: pre-adjudication agreement from the tightened-boundary rerun adopted as the formal update-pass second-coder result
- Previous pass: preserved for provenance as `data/submission_update_20260715_second_coder_initial_results.csv`

The completed rerun blind pass contains all 41 decisions and does not expose author labels. Agreement below compares the frozen author audit with the independent coder2 rerun results before any resolution. The proposed resolution is stored separately as a working draft and is not reported as human consensus.

## Single-Label Fields

| Field | Agreement | Raw agreement | Cohen's kappa | Disagreement rows |
|---|---:|---:|---:|---|
| Analysis layer | 40 / 41 | 0.976 | 0.844 | U24 |
| Primary system shape | 26 / 41 | 0.634 | 0.513 | U01, U02, U03, U04, U07, U08, U10, U11, U12, U15, U21, U24, U29, U39, U40 |
| Strongest evidence output | 28 / 41 | 0.683 | 0.551 | U01, U03, U04, U09, U14, U17, U21, U24, U26, U27, U36, U37, U39 |
| External traceability | 28 / 41 | 0.683 | 0.420 | U04, U07, U14, U16, U17, U18, U20, U22, U29, U30, U32, U35, U37 |

## Multi-Label Fields

| Field | Row-level exact | Mean row Jaccard | Micro F1 |
|---|---:|---:|---:|
| Lifecycle coverage | 7 / 41 = 0.171 | 0.666 | 0.783 |
| Agentic capabilities | 11 / 41 = 0.268 | 0.772 | 0.872 |

`path exploration` in the author audit is normalized to the frozen label `path and input exploration` before comparison. Row-level exact agreement is intentionally strict; Jaccard and micro F1 capture overlap among secondary labels.

### Per-Label Raw Agreement

| Lifecycle label | Agreement |
|---|---:|
| candidate analysis | 0.805 |
| execution observation | 0.756 |
| patch validation | 0.976 |
| path and input exploration | 0.756 |
| reporting and audit | 0.488 |
| reproduction and validation | 0.732 |

| Agentic-capability label | Agreement |
|---|---:|
| context aggregation / rule extraction | 0.902 |
| failure reuse / strategy update | 0.854 |
| feedback interpretation / loop adjustment | 0.902 |
| governance / human gates / disclosure control | 0.951 |
| long-horizon state management | 0.732 |
| tool routing / strategy routing | 0.683 |
| validation organization / evidence packaging | 0.878 |

## Interpretation

- The analytical-layer boundary remains stable except for U24 (SynthFix).
- The tightened boundary notes improved external-traceability agreement compared with the earlier pass, chiefly by clarifying item-level public alignment versus aggregate author-reported external clues.
- Lifecycle differences remain concentrated in whether adjacent workflow stages, especially reporting/audit and reproduction/validation, should be additionally marked. The low row-level exact value should be read together with the higher Jaccard and micro-F1 values.
- Capability differences are concentrated in strict thresholds for dynamic tool routing, validation organization, long-horizon state, failure reuse, and governance controls.
- Evidence-output differences primarily concern whether a public artifact is controlled task completion, runtime signal, reproducible validation, or externally traceable material.

No adjudicated labels or post-adjudication agreement statistic are claimed in this report.
