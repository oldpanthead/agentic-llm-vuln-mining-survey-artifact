# Corpus Stratification Closure Report

This report summarizes the corpus-stratification closure pass for the current ACM CSUR manuscript and public artifact.

## Corpus Counts

- Source records in screening ledger: 212
- Canonical candidate studies after version deduplication: 207
- Target-software study-level coded studies: 30
- Governance boundary record coded where applicable: 1
- Extended synthesis studies: 62
- Background references: 95
- Excluded near-neighbor studies: 19

No evidence-output classification, coding decision, research question, or second-coder statistic was changed.

## Study-Level Coding vs Extended Synthesis

The manuscript distinguishes a 31-record study-level coded set from a 62-study extended synthesis set. The 31-record set consists of 30 target-software vulnerability-mining studies plus one governance boundary record. The governance boundary record is coded only where applicable and is not used as the denominator for target-software lifecycle, capability, or system-shape distributions.

The 62-study extended synthesis set is audited through `data/extended_synthesis_audit.csv`, using thematic-use fields rather than the full workflow--capability--evidence coding matrix. Version history and duplicate source records are tracked in `data/study_version_crosswalk.csv`.

## Extended Synthesis Role Distribution

- `adjacent_candidate_analysis`: 4
- `adjacent_fuzzing_or_testing`: 29
- `agent_orchestration`: 7
- `benchmark_or_evaluation`: 15
- `evidence_or_reproducibility`: 7

## Extended Synthesis RQ Use

- `RQ2_context`: 47
- `evaluation_agenda`: 15

## Scope Statement

This pass improves corpus transparency and reviewer traceability. It does not expand the literature corpus, introduce new evidence classifications, change study-level coding, change second-coder results, or alter the workflow--capability--evidence framework.
