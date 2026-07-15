# Submission Update Adjudication Summary

## Status

`data/submission_update_20260715_adjudication_working_draft.csv` is an evidence-based proposed resolution of the completed 41-record blind pass. It preserves author and coder2 labels side by side and marks every row `assistant_proposed_pending_author_confirmation`. The proposal was prepared with AI-assisted tools to organize disagreements and evidence-linked candidate resolutions. It does not represent a discussion between two human coders, an independent human coding decision, or a completed consensus round.

## Operational Resolution Rules

1. Ordinary paper reporting is not coded as a system-level `reporting and audit` stage; the workflow must explicitly package or route evidence for audit, disclosure, or downstream review.
2. Short iterative loops do not automatically count as `long-horizon state management`; persistent state must span nontrivial iterations, tasks, or strategy transitions.
3. `tool routing` requires a dynamic choice of tool or strategy, rather than a fixed pipeline that merely invokes tools.
4. Runtime or formal counterexamples support `runtime safety signal`; `reproducible validation` additionally requires a replay, PoC/PoV, patch-validation, or equivalent versioned validation package.
5. `externally traceable material` requires item-level alignment between a concrete system output and a public issue, advisory, CVE, patch, commit, or comparable external record. Aggregate author reports remain `author-reported external clue`.
6. Primary system shape follows the dominant workflow role and evidence-producing mechanism; shape labels remain descriptive and may overlap.

## Proposed Outcome Pending Author Confirmation

- Study-level candidates: 37
- Extended-synthesis records: 4
- Boundary change: U24 (SynthFix) moves from provisional study-level candidate to extended synthesis.
- Proposed strongest-evidence distribution: {'candidate judgment': 5, 'controlled task completion': 10, 'externally traceable material': 4, 'reproducible validation': 17, 'runtime safety signal': 5}
- Proposed external-traceability distribution: {'author-reported external clue': 13, 'benchmark ground truth / public material': 22, 'not reported': 2, 'publicly aligned external trace': 4}

The working draft does not itself change the frozen manuscript or canonical corpus denominators. The author subsequently accepted the proposed resolution on 2026-07-15; the confirmed record is generated separately as `data/submission_update_20260715_adjudicated.csv`. Canonical matching and manuscript integration remain separate operations.

## Files

- Independent results: `data/submission_update_20260715_second_coder_results.csv`
- Pre-adjudication report: `reports/SUBMISSION_UPDATE_SECOND_CODER_PRE_ADJUDICATION_REPORT.md`
- Proposed working draft: `data/submission_update_20260715_adjudication_working_draft.csv`
- Reproduction script: `prepare_submission_update_adjudication.py`
