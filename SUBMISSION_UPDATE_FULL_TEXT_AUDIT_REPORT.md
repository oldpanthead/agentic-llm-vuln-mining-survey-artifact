# Submission-Update Full-Text Audit (2026-07-15)

> **Status note.** This report preserves the pre-adjudication full-text audit. The accepted resolution and current corpus integration are documented separately.

## Scope

The submission-time arXiv sensitivity search identified 41 records that required full-text review after title/abstract screening. The author reviewed the public full text and metadata for all 41 records and applied the manuscript's operational inclusion rules. The detailed, study-specific decisions are in `data/submission_update_20260715_full_coding_audit.csv`.

This report preserves the author coding pass used as the comparison baseline. The blank rerun input remains in `data/submission_update_20260715_second_coder_blind_template.csv`; completed independent decisions and pre-adjudication agreement are documented in the separate update results and report.

## Author Full-Text Decisions

| Provisional analytical treatment | Records | Interpretation |
|---|---:|---|
| Provisional study-level candidate pending independent review | 38 | The public workflow shows an observable LLM effect on tool routing, input or harness generation, feedback interpretation, validation organization, state update, or reporting/governance decisions. |
| Extended synthesis | 3 | The work is relevant to adjacent SAST triage, vulnerability management, or detection-rule operations, but the reviewed public workflow does not meet the target-software study-level rule. |
| Total | 41 | Every potentially eligible update record was reviewed exactly once. |

The three extended-synthesis decisions are:

- arXiv:2605.01885, **QASecClaw**: SAST false-positive reduction without an observable target execution-feedback or reproducible validation loop.
- arXiv:2605.01739, **AgenticVM**: scanner-output interpretation, prioritization, and reporting rather than target-software execution or validation.
- arXiv:2604.01977, **RuleForge**: generation and operational validation of detection rules for already disclosed CVEs; useful as adjacent workflow evidence rather than a target-software vulnerability-mining study.

## Evidence-Output Profile of the Author Audit

Across all 41 reviewed records, including the three extended-synthesis rows, the author audit assigned:

- candidate judgment: 4;
- controlled task completion: 7;
- runtime safety signal: 9;
- reproducible validation: 21.

These are the frozen author labels used for pre-adjudication comparison. They are not merged into the manuscript's frozen distributions.

## Reliability Boundary

The existing formal second-coder results continue to apply only to the frozen 31-record study-level coded set. The update-search blind template asks a second coder to independently decide:

- analytical layer;
- lifecycle coverage;
- primary system shape;
- cross-stage capability labels;
- principal reported evidence output;
- external traceability;
- claim boundary.

The independent pass is complete for all 41 records. `reports/SUBMISSION_UPDATE_SECOND_CODER_PRE_ADJUDICATION_REPORT.md` reports the resulting agreement, while `data/submission_update_20260715_adjudication_working_draft.csv` records an evidence-based proposal pending author confirmation. The manuscript denominators and existing 31-record second-coder statistics remain unchanged until that proposal is confirmed and canonically integrated.

## Reproduction

Run:

```text
python prepare_submission_update_full_audit.py
python prepare_submission_update_adjudication.py
python reproduce_tables.py
```

The first command deterministically rebuilds the frozen author audit and blank blind template. The second reproduces the proposed adjudication working draft and pre-adjudication report from the preserved author and coder2 inputs. The third validates schemas, agreement values, status boundaries, and frozen corpus counts.

## Security Boundary

The audit records only public bibliographic metadata and non-sensitive category-level coding. It does not include undisclosed PoCs, exploit payloads, sensitive crash inputs, private targets, credentials, live reproduction steps, or private vendor and bounty communications.
