# Final Harmonization and Artifact Closure Report

## Scope

This report records the synchronized local manuscript/artifact state after the integrated multi-source search through 2026-07-30 and the complete independent review of the target-software set. Earlier search rounds and submission tags remain preserved as provenance.

## Integrated Corpus

- 12,090 exported source occurrences
- 2,289 occurrences entering source-level deduplication
- 1,642 unique interface records screened
- 274 reports sought; 239 assessed at full text
- 110 current-search matches to the frozen pre-integration ledger
- 143 supplementary source records and 138 prior canonical studies not reidentified by the current interfaces
- 1,785 integrated source records
- 1,772 studies after version reconciliation
- 199 target-software studies
- 150 extended-synthesis studies: 89 full-text-supported and 61 title/abstract-metadata-supported records, including AgentFuzz as cross-cutting governance and agent-safety context
- 670 background/reference studies
- 753 excluded studies
- 13 alternate versions or source variants retained without separate counting

The deduplication audit contains 124 reviewed candidate pairs: 119 same-study/version relationships, five distinct-study decisions, and no unresolved pair. Each study has one counted analytical role.

## Complete Independent Review

All 199 target-software studies received independent second-coder review under the shared codebook. Agreement was:

- primary system shape: 176/199, raw 0.884, Cohen's kappa 0.843;
- principal reported evidence output: 151/199, raw 0.759, kappa 0.665;
- external traceability: 144/199, raw 0.724, kappa 0.448;
- lifecycle coverage: exact 52/199, mean row Jaccard 0.726, micro F1 0.831;
- cross-stage capability: exact 62/199, mean row Jaccard 0.782, micro F1 0.874.

Final descriptive counts and complete coder2 substitution counts remain separate. The integrated comparison, per-label reliability, and substitution files are indexed in `ARTIFACT_INDEX.md`.

## Manuscript Synchronization

The local manuscript uses the integrated corpus and reports:

- system shapes: 46 candidate analysis, 34 feedback-driven fuzzing, 62 reproduction/validation/repair, and 57 long-horizon pentest/CRS;
- principal evidence outputs: 34 candidate judgment, 55 controlled task completion, 21 runtime safety signal, 83 reproducible validation, and six externally traceable material;
- complete second-coder substitution: 78 reproducible validation and 18 externally traceable material;
- RQ1 primitive extraction over all 199 target-software studies.
- publication-status stratification: 31 conference or journal studies, 164 preprints, and four benchmark/system/report records; reproducible validation remains the modal principal output in both main status groups.

The adapted PRISMA-ScR figure presents one integrated flow rather than a sequence of internal update rounds.

## Validation

- `python reproduce_tables.py`: exit code 0 in the working artifact directory.
- `python build_final_multisource_prisma_20260730.py`: regenerates the PRISMA ledger from the frozen complete-screening audit and the tracked pre-integration corpus/crosswalk.
- `data/final_multisource_exclusion_summary.csv` closes the 753 exclusions by screening stage; `data/final_multisource_cohort_stability.csv` records the retained-67 versus new-132 schema comparison.
- Public standalone mode: exit code 0 in a fresh clone with all 27 manifest paths and no manuscript checkout or external LaTeX directory.
- LaTeX compilation: successful; current PDF is 36 pages and includes bibliography entries for the newly integrated study-level records.
- New-study BibTeX validation: 132/132 entries structurally valid; official metadata corrects two ACL conference records and one Research Square preprint.
- Undefined citations/references: none.
- Overfull boxes: none.
- Visual check: PRISMA-ScR flow and adjacent corpus figures render without overlap or clipping.

Submission snapshot tag: `csur-submission-2026-07-final-v7`.
