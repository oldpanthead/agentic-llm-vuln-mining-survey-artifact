# Corpus Stratification Closure Report

This report summarizes the corpus-stratification closure pass for the current ACM CSUR manuscript and public artifact.

## 1. Corpus Counts Preserved

- Candidate records: 212
- Target-software study-level coded studies: 30
- Governance boundary record coded where applicable: 1
- Extended synthesis studies: 66
- Background references: 95
- Excluded near-neighbor records: 20

No corpus number, evidence-output classification, coding decision, research question, or second-coder statistic was changed.

## 2. Study-Level Coding vs Extended Synthesis

The manuscript now distinguishes a 31-record study-level coded set from a 66-study extended synthesis set. The 31-record set consists of 30 target-software vulnerability-mining studies plus one governance boundary record. The governance boundary record is coded only where applicable and is not used as the denominator for target-software lifecycle, capability, or system-shape distributions.

The 66-study extended synthesis set is audited through `data/extended_synthesis_audit.csv`, using thematic-use fields rather than the full workflow--capability--evidence coding matrix.

## 3. Extended Synthesis Audit File

Created and validated: `artifact_public_release_candidate/data/extended_synthesis_audit.csv`.

Required fields included:

`record_id`, `citation_key`, `title`, `material_type`, `primary_synthesis_role`, `secondary_synthesis_roles`, `rq_contribution`, `manuscript_section_use`, `extracted_contribution`, `reason_not_study_level_coded`, `public_material_basis`, `reviewer_note`.

## 4. Extended Synthesis Role Distribution

- `adjacent_candidate_analysis`: 4
- `adjacent_fuzzing_or_testing`: 31
- `agent_orchestration`: 9
- `benchmark_or_evaluation`: 15
- `evidence_or_reproducibility`: 7

## 5. Extended Synthesis RQ Use

- `RQ2_context`: 44
- `evaluation_agenda`: 22

## 6. Manuscript Changes

- Abstract reframed the corpus as a two-depth analytical corpus.
- Section 3.1/3.2 now defines study-level coded records, extended synthesis studies, background references, and product-ecosystem boundary material separately.
- Methodology Box 2 now uses mutually exclusive operational treatment rows rather than a slash category.
- Section 4 and Section 7 include short qualitative observations grounded in the extended synthesis audit.
- Conclusion now states that the 31-record coded set supports study-level distributions while the 66-study extended synthesis layer broadens mechanism and evaluation context without changing those distributions.

## 7. Artifact Changes

- Added `data/extended_synthesis_audit.csv`.
- Updated `README.md`, `RELEASE_MANIFEST.md`, and `data_dictionary.md` to document the extended synthesis layer and legacy label mapping.
- Updated `reproduce_tables.py` with validation checks for the extended synthesis audit.
- Added `EXTENDED_SYNTHESIS_AUDIT_REPORT.md`.

## 8. Script Validation

`reproduce_tables.py` checks that the extended synthesis audit has 66 rows, covers exactly the legacy Supporting records, uses approved role/RQ vocabularies, and contains specific extracted contributions.

## 9. Terminology Closure

Visible manuscript terminology was updated from `deep-analysis`/`Core` wording to `study-level coded set`, `study-level coding`, `study-level coded statistics`, and `extended synthesis` where appropriate. Legacy CSV values are preserved for reproducibility and mapped in artifact documentation.

## 10. Scope Statement

This pass improves corpus transparency and reviewer traceability. It does not expand the literature corpus, introduce new evidence classifications, change study-level coding, change second-coder results, or alter the workflow--capability--evidence framework.
