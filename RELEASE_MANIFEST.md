# Release Manifest

## Release Scope

This public release contains non-sensitive data and scripts supporting the ACM CSUR manuscript. It includes the integrated multi-source search through 2026-07-30, study/version reconciliation, analytical-layer allocation, the 199-study target-software coding matrix, the 154-study extended synthesis audit, complete independent second-coder files, and source-located supplementary extractions.

The immutable synchronized submission tag is `csur-submission-2026-08-final-v10`. Earlier tags, including `csur-submission-2026-08-final-v9`, remain unchanged.

## Current Counts

- Source records: 1,785
- Studies after version reconciliation: 1,772
- Target-software studies: 199
- Extended-synthesis studies: 154, including AgentFuzz as governance and agent-safety context outside target-software distributions
- Background/reference studies: 668
- Excluded studies: 751
- Alternate versions or source variants: 13
- Product-ecosystem snapshot rows: 23, maintained outside the research-study counts

## Manuscript-Facing Files

The authoritative list is `manuscript_artifact_paths.txt`. It includes:

- integrated search, source-count, frozen complete-screening, retrieval/full-text, PRISMA, and deduplication audits;
- the stage-level exclusion account and pre-final/new-study cohort-stability audit;
- `data/corpus.csv` and `data/study_version_crosswalk.csv`;
- `data/adjudicated_study_level_coding_matrix_199.csv` as the final descriptive source, with `data/current_study_level_coding_matrix_harmonized.csv` preserved as the primary pre-adjudication matrix;
- `data/extended_synthesis_audit.csv` (92 full-text-supported and 62 title/abstract-metadata-supported records);
- study-level publication-status assignments and stratified distributions;
- the study-level primitive extraction, workflow-active/evaluation role split, and primitive--output cross-tab;
- target-domain/year, publication-status, public-artifact, controlled-task membership and denominator sensitivity, public-alignment, and training-overlap reporting audits;
- `data/final_multisource_cohort_stability.csv`;
- integrated 199-study pre-adjudication second-coder comparison, per-label reliability, and substitution sensitivity;
- the raw 460-row OY external rereview export, separate 410-row decision and 50-row QC layers, full 995-row log, completion manifest, and adjudicated statistics. The integrated decision export supersedes the earlier completed form;
- representative mechanism, reported-result, cost, ablation, and failure-recovery extractions;
- reference metadata for newly integrated study-level records.

## Reproduction

Run:

```text
python reproduce_tables.py
```

The default public mode has no dependency on a manuscript checkout. It verifies file presence, the complete 410-row adjudication record, the final 199-study matrix and adjudicated statistics, unique CSV headers, corpus and layer counts, study/version uniqueness, shape and evidence distributions, lifecycle and capability counts, external traceability, integrated PRISMA allocation and source-specific acquisition provenance, primitive-use roles and output coupling, publication-status sensitivity, target-domain/year cross-tabs, public-artifact indicators, training-overlap reporting, reference metadata, and complete pre-adjudication reliability files. Optional manuscript validation is available through `--manuscript`.

Create a clean public directory with `python build_public_release.py <new-output-directory>`. The export is assembled from `public_release_files.txt` and `manuscript_artifact_paths.txt` and is validated after copying.

## Historical Provenance

The tagged source repository retains earlier search and coding stages, including 31-record, 41-record, and 67-study views. The clean public export excludes those historical build files except for the frozen pre-final matrix used by the current validator.

## Security Boundary

Excluded from the public release:

- undisclosed PoCs and exploit payloads;
- sensitive crash-triggering inputs;
- credentials, private targets, and live reproduction steps;
- local document-library paths and private databases;
- full-text PDFs not licensed for redistribution;
- vendor-private and bug-bounty communications.

See `SECURITY_BOUNDARY.md` for the complete boundary.
