# Extended Synthesis Audit Report

This report documents the record-level audit for the 66-study extended synthesis set used by the current ACM CSUR manuscript.

## Scope

- Audited file: `data/extended_synthesis_audit.csv`
- Rows: 66
- Corpus relationship: these rows correspond exactly to records with the legacy `Supporting` layer in `data/corpus.csv`.
- Coding depth: these records are not full study-level workflow--capability--evidence coding rows. They are audited through predefined thematic-use fields for adjacent mechanisms, evaluation context, and evidence-boundary discussion.

## Material Types

- `conference_paper`: 28
- `journal_article`: 15
- `preprint_or_arxiv`: 23

All 66 records are scholarly papers or preprints in the current artifact (`conference_paper`, `journal_article`, or `preprint_or_arxiv`), so the manuscript may describe this layer as a 66-study extended synthesis set.

## Primary Synthesis Roles

- `adjacent_candidate_analysis`: 4
- `adjacent_fuzzing_or_testing`: 31
- `agent_orchestration`: 9
- `benchmark_or_evaluation`: 15
- `evidence_or_reproducibility`: 7

Controlled role vocabulary: `lower_level_primitive`, `adjacent_candidate_analysis`, `adjacent_fuzzing_or_testing`, `benchmark_or_evaluation`, `agent_orchestration`, `governance_or_safety`, `evidence_or_reproducibility`.

## RQ Contribution

- `RQ2_context`: 44
- `evaluation_agenda`: 22

Controlled RQ-use vocabulary: `RQ1`, `RQ2_context`, `evaluation_agenda`, `governance_agenda`.

## Manuscript Use

- `Section 7.1 / evaluation and benchmark discussion`: 15
- `Sections 4.1 and 5.1 / candidate-analysis context`: 4
- `Sections 4.1--4.2 / fuzzing, testing, and feedback-loop context`: 31
- `Sections 4.3--5 / orchestration and system-shape context`: 9
- `Sections 6--7 / validation, reproducibility, and evidence-boundary discussion`: 7

## Closure Statement

The extended synthesis audit gives every one of the 66 records a traceable material basis, primary synthesis role, RQ contribution, manuscript-use location, extracted contribution, and reason for not being full study-level coded. It does not reclassify these records as study-level coded studies and does not alter the corpus counts or study-level coded distributions.
