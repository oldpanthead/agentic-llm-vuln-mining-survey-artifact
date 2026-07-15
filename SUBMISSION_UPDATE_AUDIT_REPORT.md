# Submission-Time arXiv Sensitivity and Recall-Recovery Search Audit (2026-07-15)

> **Status note.** This report preserves the July 15 recall-recovery search state and links it to the completed author-confirmed 37/4 resolution and corpus integration.

## Purpose

This audit documents a deliberately broader arXiv-only sensitivity and recall-recovery search conducted after the narrower multi-source historical ledger had been frozen. It exposed a recall limitation while preserving the original and update rounds as separate audit trails.

## Search material

- Search service: official arXiv API.
- Query groups: `agent_task`, `pov_crs`, `review_update`, and `execution_validation` (defined in `submission_update_search.py`).
- Date searched: 2026-07-15.
- Analytical date boundary used for comparison: 2026-06-30.
- Raw unique arXiv results: 432.
- Raw responses and SHA-256 hashes: `data/submission_update_20260715_raw/` and `data/submission_update_20260715_manifest.json`.
- Normalized metadata: `data/submission_update_20260715_arxiv_results.csv`.
- Record-level decisions: `data/submission_update_20260715_screening_audit.csv`.
- Full-text author audit: `data/submission_update_20260715_full_coding_audit.csv`.
- Blank independent-review input: `data/submission_update_20260715_second_coder_blind_template.csv`.
- Completed independent decisions: `data/submission_update_20260715_second_coder_results.csv`.
- Pre-adjudication agreement: `reports/SUBMISSION_UPDATE_SECOND_CODER_PRE_ADJUDICATION_REPORT.md`.
- Preserved pre-confirmation AI-assisted resolution working draft: `data/submission_update_20260715_adjudication_working_draft.csv`.
- Full-text audit report: `SUBMISSION_UPDATE_FULL_TEXT_AUDIT_REPORT.md`.

## Screening result

| Status | Count | Interpretation |
|---|---:|---|
| Existing corpus match | 12 | Matches a retained source/canonical record by normalized title or arXiv identifier; no new count. |
| Outside date window | 26 | First arXiv submission after 2026-06-30; retained only in the update ledger. |
| Potentially eligible update record | 41 | These records received author and independent full-text coding. The author-confirmed resolution places 37 in study-level coding and four in extended synthesis; canonical integration is complete. |
| Contextual/background update | 30 | Relevant to adjacent mechanisms, benchmarks, evaluation, repair, or governance context, but not selected as a new target-software coded record in this audit. |
| Excluded at title/abstract update | 323 | Did not meet the operational target-software Agentic workflow criterion for the coded set. |

Sixty-one records were checked against downloaded public full text in a temporary, untracked workspace; ten additional contextual/background records were checked from public abstract and metadata. All 41 potentially eligible records received full-text review. No PDF or private path is included in the public artifact.

## Methodological implication

The update search used broader sensitivity queries than the reconciled historical source ledger. Full-text author review initially identified 38 provisional study-level candidates and 3 extended-synthesis records. The completed independent pass and operational-rule review produce a proposed 37/4 split, with U24 (SynthFix) moved to extended synthesis. The present 31-record study-level matrix remains frozen until the proposal is confirmed and canonically deduplicated; update agreement is reported separately and no completed human-consensus labels are claimed.

## Corpus correction found during the audit

CP189, a machine-translation fine-tuning study, was a false-positive keyword/metadata match. It was moved from Supporting/extended synthesis to Excluded. The corrected source-record allocation is 31 Core, 65 Supporting, 95 Background, and 21 Excluded. The corrected canonical allocation is 31 study-level coded records, 61 extended-synthesis studies, 95 background/reference studies, and 20 excluded studies, totaling 207 canonical studies from 212 source records.

## Reproducibility

Run:

```bash
python submission_update_search.py
python prepare_submission_update_screening.py
python prepare_submission_update_adjudication.py
python reproduce_tables.py
```

The first command verifies the saved raw-response hashes without requiring a new network request. The second regenerates the record-level screening file from the frozen reviewed decision sets. The third reproduces the proposed update adjudication and agreement report. The fourth validates the corpus, crosswalk, extended-synthesis audit, second-coder files, and update-search checks.

## Safety boundary

The update contains bibliographic metadata and category-level screening rationales only. It does not include exploit payloads, undisclosed proof-of-concept details, sensitive crash inputs, private targets, credentials, live reproduction steps, or vendor-private communications.

