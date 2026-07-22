# Unified Second-Coder Review Guide

## Goal

Review the complete 68-record study-level set under one frozen codebook. This is a unified confirmation/revision pass, not a request to discard work already completed. Previous second-coder decisions are prefilled where they can be mapped without changing their meaning.

## Files To Use

1. Read `unified_second_coder_codebook.md`.
2. Open the local workbook or CSV under `local_private_working/unified_second_coder_review/`.
3. Use the `official_url` and local material index to inspect the paper or public artifact.

Public arXiv PDFs can be cached locally before review with:

```powershell
python unified_second_coder_review.py cache-materials
python unified_second_coder_review.py prepare
```

The cached PDFs and absolute local-path index remain under the git-ignored `local_private_working/` directory.

Do not open these author-label files before finishing the review:

- `data/current_study_level_coding_matrix.csv`
- `data/current_study_level_coding_matrix_harmonized.csv`
- adjudication or harmonization audit files
- manuscript tables that disclose row-level author coding

## Efficient Review Order

1. Start with rows marked `needs_new_fields`; these are initial-round records whose lifecycle, primary shape, or claim boundary was not previously coded by the second coder.
2. Continue with rows marked `confirm_all_fields`; all six prior decisions are available for confirmation or revision.
3. Review the governance boundary case last because some target-software fields are not applicable.

For a prefilled field, compare the prior decision with the public material and the frozen codebook. Copy it into the corresponding `final_*` field only if it remains appropriate; otherwise enter the revised value. For a blank prior field, code it directly.

## Required Completion Steps Per Row

1. Record the paper, section, page, table, figure, or public artifact inspected in `material_checked`.
2. Complete all `final_*` fields.
3. Set each `*_review_status` to `confirm`, `revise`, or `newly_code`.
4. Add a concise `decision_note` grounded in the reviewed material.
5. Add an `uncertainty_note` only when a real boundary remains unresolved.
6. Set `row_status=complete`.

Do not change a decision to improve agreement. The comparison with author labels is performed only after the complete sheet is returned.

## Label Formatting

- For lifecycle and capability multi-label fields, separate labels with semicolons and preserve the codebook order.
- Use the exact spelling in the codebook for single-label fields.
- Keep claim-boundary notes concise and non-sensitive.

## Validation

After all rows are complete, run:

```powershell
node local_private_working/unified_second_coder_review/export_review_to_csv.mjs
python unified_second_coder_review.py validate --input local_private_working/unified_second_coder_review/unified_second_coder_working.csv
```

The validator checks completeness and allowed labels but does not reveal author labels or agreement results.
