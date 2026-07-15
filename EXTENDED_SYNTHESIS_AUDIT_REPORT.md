# Extended Synthesis Audit Report

This report documents the record-level audit for the 61-study canonical extended synthesis set used by the current ACM CSUR manuscript.

## Scope

- Audited file: data/extended_synthesis_audit.csv
- Rows: 61
- Corpus relationship: these rows correspond exactly to canonical counted records with analytical_layer=extended_synthesis in data/study_version_crosswalk.csv.
- Coding depth: these records use predefined thematic-use fields for adjacent mechanisms, evaluation context, and evidence-boundary discussion rather than the full study-level matrix.

## Material Types

- conference_paper: 25
- journal_article: 15
- preprint_or_arxiv: 21

## Primary Synthesis Roles

- adjacent_candidate_analysis: 4
- adjacent_fuzzing_or_testing: 29
- agent_orchestration: 7
- benchmark_or_evaluation: 14
- evidence_or_reproducibility: 7

## RQ Contribution

- RQ2_context: 47
- evaluation_agenda: 14

## Study-Specific Extraction Closure

All 61 extracted_contribution values and all 61 reason_not_study_level_coded values are unique. Each contribution names a concrete mechanism, tool/environment, feedback type, validation object, or evaluation distinction. Rows were checked against public title/abstract metadata on 2026-07-15.

CP189 was removed from this layer after manual review showed that it concerns in-house machine translation rather than software security or vulnerability mining.

## Closure Statement

The audit gives each canonical extended-synthesis study a traceable material basis, synthesis role, RQ use, manuscript location, study-specific contribution, and coding-depth rationale. It does not alter the existing 31 study-level evidence decisions or second-coder results.
