# Final Harmonization and Artifact Closure Report

## Scope

This report records the synchronized local manuscript/artifact state after the integrated multi-source search through 2026-07-30 and the complete independent review of the target-software set. Earlier search rounds and submission tags remain preserved as provenance.

## Integrated Corpus

- 12,090 exported source occurrences
- 2,289 occurrences entering source-level deduplication
- 1,642 unique interface records screened
- 274 reports sought; 239 assessed at full text
- 1,785 integrated source records
- 1,772 studies after version reconciliation
- 199 target-software studies
- one governance boundary case outside target-software distributions
- 149 extended-synthesis studies
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
- Public standalone mode: exit code 0 in a fresh 24-path manifest-only copy with no manuscript checkout or external LaTeX directory.
- LaTeX compilation: successful; current PDF is 35 pages and includes bibliography entries for the newly integrated study-level records.
- New-study BibTeX validation: 132/132 entries structurally valid; official metadata corrects two ACL conference records and one Research Square preprint.
- Undefined citations/references: none.
- Overfull boxes: none.
- Visual check: PRISMA-ScR flow and adjacent corpus figures render without overlap or clipping.

The immutable submission commit/tag will be recorded only after remote publication is explicitly approved.
