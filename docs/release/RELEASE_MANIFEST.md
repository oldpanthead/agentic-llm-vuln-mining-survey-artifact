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

The authoritative lists are the `manuscript_artifact_paths` and `static_release_files` arrays in `manifests/release_manifest.json`. They include:

- integrated search, source-count, frozen complete-screening, retrieval/full-text, PRISMA, and deduplication audits;
- the stage-level exclusion account and pre-final/new-study cohort-stability audit;
- `data/corpus/corpus.csv` and `data/corpus/study_version_crosswalk.csv`;
- `data/coding/adjudicated_study_level_coding_matrix_199.csv` as the final descriptive source, with `data/coding/current_study_level_coding_matrix_harmonized.csv` preserved as the primary pre-adjudication matrix;
- `data/coding/extended_synthesis_audit.csv` (92 full-text-supported and 62 title/abstract-metadata-supported records);
- the joined `data/synthesis/study_synthesis_199.csv` view containing study-level publication status, primitive extraction, target domain, public-artifact, controlled-task membership, and training-overlap fields;
- the workflow-active/evaluation role split and primitive--output cross-tab;
- target-domain/year, publication-status, public-artifact, controlled-task membership and denominator sensitivity, public-alignment, and training-overlap reporting audits;
- the provenance-only `final_multisource_cohort_stability.csv` table inside `data/derived/derived_summary_tables.json`;
- integrated 199-study pre-adjudication second-coder comparison, per-label reliability, and substitution sensitivity;
- the raw 460-row OY external rereview export, consolidated 410-row decision layer (including the earlier completed-form fields), separate 50-row QC layer, full 995-row log, embedded completion metadata, and the derived-summary bundle containing adjudicated statistics;
- representative mechanism, reported-result, cost, ablation, and failure-recovery extractions;
- reference metadata for newly integrated study-level records.

## Reproduction

Run:

```text
python reproduce_tables.py
```

The default public mode has no dependency on a manuscript checkout. It verifies file presence, the complete 410-row adjudication record, the final 199-study matrix and adjudicated statistics, unique CSV headers, corpus and layer counts, study/version uniqueness, shape and evidence distributions, lifecycle and capability counts, external traceability, integrated PRISMA allocation and source-specific acquisition provenance, primitive-use roles and output coupling, publication-status sensitivity, target-domain/year cross-tabs, public-artifact indicators, training-overlap reporting, reference metadata, and complete pre-adjudication reliability files. Optional manuscript validation is available through `--manuscript`.

Create a clean public directory with `python scripts/build_public_release.py <new-output-directory>`. The export is assembled from `manifests/release_manifest.json` and is validated after copying.

## Release Gate

- The release cutoff is 2026-07-30 and the synchronized submission tag is `csur-submission-2026-08-final-v10`.
- `README.md`, this manifest, `docs/coding/data_dictionary.md`, and `docs/coding/codebook.md` describe the current release.
- `manifests/release_manifest.json` lists the manuscript-facing and static release files; all paths must exist and be unique.
- `reproduce_tables.py` validates the integrated corpus, adjudicated distributions, provenance, and pre-adjudication independent-coder files in standalone mode. Re-run it after staging a clean export.
- The raw 460-row OY export, 410-row decision layer, separate 50-row QC layer, 995-row decision log, embedded completion metadata, and final matrix are present and validated.
- Publish only an allowlisted export. Exclude `.git/`, caches, logs, full-text PDFs, private paths, proposed or unresolved working files, credentials, private targets, exploit payloads, sensitive crash inputs, and vendor-private communications.
- Before release, confirm the repository URL, release date, and author-approved disclosure metadata. `SECURITY_BOUNDARY.md` defines the disclosure boundary.

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

## Closure Record

This section records the synchronized manuscript/artifact state after major-revision closure and OY external-rereview integration. The review scope, workflow--capability--evidence framework, four system shapes, seven capabilities, and five principal outputs were not changed. No literature search or corpus expansion was performed; final study-level labels combine 585 frozen agreements with OY's resolutions of 410 frozen disagreements.

### Closed Reviewer Issues

- Search and PRISMA closure: frozen ledgers reproduce 1,785 source records, 1,772 studies after version reconciliation, 199 target-software studies, 154 extended-synthesis studies, 668 background/reference studies, and 751 exclusions. Each study enters one final analytical layer; 13 alternate versions, duplicates, or source variants remain traceable without independent counting.
- Material-basis reconciliation: all 199 target-software studies have detailed public workflow and evaluation material for complete coding. Extended synthesis comprises 92 studies supported by full text or equivalent public material and 62 supported by audited title-and-abstract metadata.
- Reliability and external rereview: the 199-study comparison reports positive counts, raw agreement, Cohen's kappa, and Gwet's AC1 for every lifecycle and capability label before adjudication. OY externally rereviewed 410 field-level disagreements; 50 QC tasks remain separate. The final matrix reports 43 reporting-and-audit studies, 69 validation-organization studies, three studies with externally traceable material as principal output, and four with a publicly aligned external trace.
- Shape/output relation: primary shape records the dominant organization and objective of agent control; principal output records the observable result supporting the main evaluated contribution. Their joint table is a construct-consistency and coupling check, not a causal result.
- Publication robustness: the set contains 31 conference/journal studies, 164 preprints, and four benchmark/report/other records. Reproducible validation is the modal principal output in formal-publication and preprint subsets; the manuscript makes no causal publication-status claim.
- RQ1 support: source-located primitive extraction separates workflow-active use, evaluation/support use, and both. Co-occurrence checks describe technical dependence, not dynamic tool selection or causation.
- Domain and time: source-located target-domain and publication-year assignments support the study-level panels; 2026 is marked as an incomplete year.
- Public artifacts and training overlap: source-located extraction located 50 public implementations, five environment/build descriptions, 14 trigger/replay/PoC/PoV candidates, six traces/logs, and five patch artifacts. The strict audit retained one system-generated item-level trigger/replay artifact and excluded 13 candidates under the stated rule. Training-overlap controls were explicit in six studies, discussed without a control in two, and not located in 191.
- Reference architecture: Figure 5 is a corpus-grounded synthesis, not an experimentally validated architecture or fifth system shape.
- Reference metadata: all 2026 BibTeX entries retain authors, titles, years, and a DOI, arXiv identifier, or official URL; pure arXiv entries were normalized without removing formal publication DOIs.

### Recomputed Statistics

- Corpus: 1,785 source records; 1,772 studies; 199 target-software; 154 extended synthesis (92 full text, 62 metadata); 668 background/reference; 751 excluded.
- Primary shapes: 41 candidate analysis; 33 feedback-driven fuzzing; 70 reproduction/validation/repair; 55 long-horizon penetration testing or CRS.
- Principal outputs: 51 candidate judgment; 56 controlled task completion; 19 runtime safety signal; 70 reproducible validation; three externally traceable material.
- Publication status: 31 formal publications; 164 preprints; four benchmark/report/other.
- Complete per-label reliability, disagreement review, the 995-row decision log, completion metadata, and final statistics are indexed by `README.md` and the data dictionary.

### Preserved Data And Reliability Boundary

The original author matrix and complete independent second-coder matrix remain unchanged and separate. OY's external-rereview decisions produce a distinct adjudicated 199-study matrix for descriptive distributions; they do not overwrite either independent source or create a post-adjudication reliability statistic.

For title-and-abstract screening, a second reviewer completed a disjoint 20-record calibration and independently assessed a fixed-seed sample of 153 records from the 1,524-record screening frame without access to the first reviewer's decisions. Exact agreement was 142/153 (92.8%), Cohen's kappa 0.690, and Gwet's AC1 0.906; all 11 disagreements were resolved by consensus in confidential screening-audit workbooks.

For post-inclusion coding, Shangru Zhao independently reviewed all 199 included target-software studies after calibration without seeing the primary labels or final assignments. Any acknowledgment consent or ACM authorship assessment remains an author decision.

### Validation Snapshot

- `reproduce_tables.py`: exit code 0 on 2026-08-26 in standalone public mode; all manifest paths, 410 decisions, final matrix, and manuscript-facing statistics verified.
- `reproduce_tables.py --manuscript`: exit code 0 on 2026-08-26 against the synchronized manuscript.
- LaTeX/BibTeX compilation: exit code 0 on 2026-08-26; 34-page PDF. No bibliography-size reduction was applied.
- Undefined citations/references: none. Two overfull boxes remain in the Section 5 comparison table for a separate layout pass.
- Visual inspection covered abstract, methodology, lifecycle, Table 10, sensitivity analysis, conclusion, appendix, and reference-tail pages; no overlap or clipping was found.

The immutable synchronized release is `csur-submission-2026-08-final-v10`.
