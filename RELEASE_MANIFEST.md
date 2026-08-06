# Release Manifest

## Release Scope

This public release contains non-sensitive data and scripts supporting the ACM CSUR manuscript. It includes the integrated multi-source search through 2026-07-30, study/version reconciliation, analytical-layer allocation, the 199-study target-software coding matrix, the 150-study extended synthesis audit, complete independent second-coder files, and source-located supplementary extractions.

The immutable synchronized submission tag is `csur-submission-2026-07-final-v8`. Earlier tags remain unchanged.

## Current Counts

- Source records: 1,785
- Studies after version reconciliation: 1,772
- Target-software studies: 199
- Extended-synthesis studies: 150, including AgentFuzz as governance and agent-safety context outside target-software distributions
- Background/reference studies: 670
- Excluded studies: 753
- Alternate versions or source variants: 13
- Product-ecosystem snapshot rows: 23, maintained outside the research-study counts

## Manuscript-Facing Files

The authoritative list is `manuscript_artifact_paths.txt`. It includes:

- integrated search, source-count, frozen complete-screening, retrieval/full-text, PRISMA, and deduplication audits;
- the stage-level exclusion account and pre-final/new-study cohort-stability audit;
- `data/corpus.csv` and `data/study_version_crosswalk.csv`;
- `data/current_study_level_coding_matrix_harmonized.csv`;
- `data/extended_synthesis_audit.csv` (88 full-text-supported and 62 title/abstract-metadata-supported records);
- study-level publication-status assignments and stratified distributions;
- the study-level primitive extraction, workflow-active/evaluation role split, and primitive--output cross-tab;
- target-domain/year, publication-status, public-artifact, and training-overlap reporting audits;
- `data/final_multisource_cohort_stability.csv`;
- integrated 199-study second-coder comparison, per-label reliability, and substitution sensitivity;
- representative mechanism, reported-result, cost, ablation, and failure-recovery extractions;
- reference metadata for newly integrated study-level records.

## Reproduction

Run:

```text
python reproduce_tables.py
```

The default public mode has no dependency on a manuscript checkout. It verifies file presence, unique CSV headers, corpus and layer counts, study/version uniqueness, shape and evidence distributions, lifecycle and capability counts, external traceability, integrated PRISMA allocation and source-specific acquisition provenance, primitive-use roles and output coupling, publication-status sensitivity, target-domain/year cross-tabs, public-artifact indicators, training-overlap reporting, reference metadata, per-label AC1, and the complete 199-study reliability files. Optional manuscript validation is available through `--manuscript`.

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
