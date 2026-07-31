# Final Multi-Source Second-Coder Guide

## Scope

Review only `data/final_multisource_search_20260730_second_coder_blind.csv`.
The file contains final-search candidates with locally cached public full
texts. It contains no author or AI-assisted inclusion or coding decisions.
Use `unified_second_coder_codebook.md` for all controlled labels.
Once coding has started, do not regenerate the blind file. The preparation
script refuses to overwrite coder-entered values unless `--force` is supplied.

## One-Pass Task

For each row:

1. Open `local_review_pdf` and inspect the workflow and evaluation sections.
2. Set `eligibility_decision` to `include_study_level` only when an LLM-mediated
   interpretation or decision changes a later tool-mediated action, execution
   input, retained state, validation step, or reporting decision in a
   target-software vulnerability-discovery or validation workflow.
3. Otherwise set `eligibility_decision` to `not_study_level` and give a short
   reason. Fixed pipelines may contain scripts, harnesses, or validators; their
   presence does not exclude a study. The relevant question is whether the LLM
   affects a later workflow transition rather than merely supplying a label or
   explanation.
4. For `include_study_level` rows, complete the six fields from
   `unified_second_coder_codebook.md`: lifecycle coverage, cross-stage
   capabilities, primary system shape, principal reported evidence output,
   external traceability, and claim boundary.
5. Record the page, section, table, figure, or artifact inspected in
   `material_checked`. Use `uncertainty_note` only when the public material does
   not resolve a boundary.
6. Set `row_status` to `complete` only after the eligibility decision and all
   applicable fields have been checked.

Do not inspect `data/final_multisource_search_20260730_fulltext_assessment.csv`
or any manuscript-facing coding matrix while completing the blind pass.

## Records Without Full Text

`data/final_multisource_search_20260730_fulltext_unresolved.csv` is an access
queue, not a coding file. Do not code those records until a public full text has
been located and added to a later blind package.

## Completion Check

Run:

```text
python validate_final_multisource_second_coder_20260730.py --require-complete
```

The command checks row completion and the existing controlled vocabularies; it
does not alter the coder's entries.
