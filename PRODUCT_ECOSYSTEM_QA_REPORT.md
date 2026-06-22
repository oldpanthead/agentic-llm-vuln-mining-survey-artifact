# Product Ecosystem QA Report

Date: 2026-06-15

## 1. Product Snapshot vs. 212 Candidate Records

`data/product_ecosystem_snapshot.csv` is an independent boundary data layer. It is not part of `data/corpus.csv`, does not count toward the 212 candidate records, and does not alter Core aggregate statistics. Product materials that also support background or supporting discussion are represented separately in `data/reference_audit.csv` through `PE` rows.

Current checked corpus counts remain:

- Candidate records: 212
- Core: 31
- Supporting: 66
- Background: 95
- Excluded: 20

## 2. Manuscript Wording Updates

- Section 3.1 now states that the product ecosystem snapshot is an independent boundary data layer and is not counted in the 212 candidate records or Core aggregate statistics.
- Section 4.5 now points telemetry, trace identifiers, tool interface definitions, state snapshots, delegation graphs, and rollback mechanisms to Section 6.6 as system design choices and Section 7.6 as the trustworthy-deployment agenda.
- The Excalibur sentence now reads as a Chinese expression: `PentestAgent、Co-RedTeam 和真实世界渗透测试研究中的 Excalibur`.
- The claim-level audit table title is now `声明级审计要素检查清单`.

## 3. Mythos Version Relationship

The manuscript now uses a source-limited version-evolution expression: `Claude Mythos Preview、后续 Mythos 5 页面更新与 Project Glasswing 公告`. The table row remains `Claude Mythos Preview / Mythos 5` and the note clarifies that the row records public vendor-material evolution only. It does not state independent validation, Core eligibility, or identical availability scope across pages.

## 4. Claude Code Security URL

The old documentation URL `https://docs.anthropic.com/en/docs/claude-code/security` was rechecked on 2026-06-15 and redirects to `https://code.claude.com/docs/en/security`. The current official entry is used in:

- `latex/references_seed.bib`
- `data/product_ecosystem_snapshot.csv`
- `data/reference_audit.csv`
- `data/doi_remaining_manual_status.csv`
- `ZOTERO_PDF_RESOLUTION_REPORT.md`

Local Zotero search for `Claude Code security` returned no matching item.

## 5. Artifact Documentation Sync

Updated:

- `README.md`
- `RELEASE_MANIFEST.md`
- `data_dictionary.md`
- `SECURITY_BOUNDARY.md`
- `public_release_checklist.md`
- `reference_audit.csv`
- `doi_remaining_manual_status.csv`
- `ZOTERO_PDF_RESOLUTION_REPORT.md`

The synchronized wording states that legacy A/E fields are retained for historical reproducibility and cross-version traceability, while the current manuscript primarily presents natural-language workflow, capability, and evidence fields.

## 6. reproduce_tables.py Product QA

`reproduce_tables.py` now checks `data/product_ecosystem_snapshot.csv` offline and deterministically:

- file exists and can be read with Python `csv`;
- required columns exist and are non-empty;
- `snapshot_date` parses as ISO date and matches `RELEASE_MANIFEST.md`;
- `access_date` parses as ISO date;
- `manuscript_role` uses the approved enumeration;
- product/vendor documentation is not promoted to Core without manual confirmation;
- non-Excluded rows have public source URLs;
- `source_url` is non-empty;
- no local Zotero paths, PDF/SQLite paths, or private working paths appear;
- `update_required` parses as a boolean-like value.

Product snapshot CSV parse result: 18 rows.

## 7. Reference Audit

- Product pages, official help pages, model pages, policy pages, and vendor documentation remain DOI-not-applicable rows.
- Formal paper DOI handling was not changed.
- No product material was represented as a paper.
- Claude Code security controls now record access date 2026-06-15 and the redirect source.
- No duplicate row was added for the redirecting URL.

## 8. Verification

`python reproduce_tables.py` result:

- product snapshot QA passed;
- Candidate/Core/Supporting/Background/Excluded counts remained 212/31/66/95/20;
- Core rows remained 31;
- E-level distribution and E4c check remained unchanged.

LaTeX result:

- `latexmk -xelatex -interaction=nonstopmode -halt-on-error -jobname=main_zh_v13_product_ecosystem main_zh_v13_full.tex` succeeded.
- Precise log scan found no undefined citation, undefined reference, overfull hbox, underfull hbox, natbib warning, or LaTeX warning.
- Current PDF pages: 49.
- Page change against the previous `main_zh_v13_product_ecosystem.pdf` baseline: 0 pages.

Security/file-boundary checks:

- No tracked PDF, SQLite, SQLite journal, private working directory, or private Zotero resolution report.
- Local/private path scan over public artifact files found no matches.

## 9. git diff --stat

Artifact tracked-file diff is:

```text
README.md                            |   6 ++
RELEASE_MANIFEST.md                  |   6 ++
SECURITY_BOUNDARY.md                 |   2 +
ZOTERO_PDF_RESOLUTION_REPORT.md      |   2 +
data/doi_remaining_manual_status.csv |   2 +-
data/product_ecosystem_snapshot.csv  |   2 +-
data/reference_audit.csv             |   2 +-
data_dictionary.md                   |   4 +-
public_release_checklist.md          |   2 +
reproduce_tables.py                  | 163 +++++++++++++++++++++++++++++++++++
10 files changed, 187 insertions(+), 4 deletions(-)
```

This report adds one untracked Markdown file:

```text
PRODUCT_ECOSYSTEM_QA_REPORT.md | 134 ++++++++++++++++++++++++++++++++++
1 file changed, 134 insertions(+)
```

## 10. Manual Decisions

No Core candidate requires author decision in this round. The remaining manual decision is procedural: refresh the product ecosystem snapshot before any future manuscript release because product pages and default models may change quickly.

## 11. Commit / Push Suitability

- Suitable to commit after author review.
- Suitable to push after commit if the author wants the artifact repo updated.
- This round did not commit and did not push.
