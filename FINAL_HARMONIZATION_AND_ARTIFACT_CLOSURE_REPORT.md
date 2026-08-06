# Major-Revision Methodological and Empirical Closure Report

## Scope

This report records the single synchronized local manuscript/artifact state after the major-revision closure pass. The review scope, workflow--capability--evidence framework, four system shapes, seven capabilities, five principal outputs, and existing study-level labels were not changed. No literature search, corpus expansion, or label adjustment was performed in this pass.

## Closed Reviewer Issues

- **Search and PRISMA closure.** The manuscript now presents one integrated review process through July 30, 2026. Frozen ledgers reproduce 1,785 source records, 1,772 studies after version reconciliation, 199 target-software studies, 150 extended-synthesis studies, 670 background/reference studies, and 753 exclusions. Each study enters one final analytical layer; 13 alternate versions, duplicates, or source variants remain traceable without independent counting.
- **Material-basis reconciliation.** All 199 target-software studies have detailed public workflow and evaluation material for complete coding. Extended synthesis comprises 88 studies supported by full text or equivalent public material and 62 supported by audited title-and-abstract metadata. Source-specific query, retrieval, and historical integration fields remain available as provenance rather than manuscript cohorts.
- **Reliability and sensitivity.** The 199-study comparison now reports positive counts, raw agreement, Cohen's kappa, and Gwet's AC1 for every lifecycle and capability label. Sensitivity ranges replace low-reliability point estimates in the abstract, synthesis, and conclusion: feedback interpretation 179--186, validation organization 147--180, failure reuse 81--94, governance control 18--27, and externally traceable material 6--18. The reporting-and-audit audit contains 82 disagreements: 78 second-coder-only and four author-only positives. Most second-coder-only cases treated a generated report or packaged finding as coverage, whereas the final coding required an observable packaging or routing transition.
- **Shape/output construct relation.** Primary shape records the dominant organization and objective of agent control; principal output records the observable result supporting the main evaluated contribution. They intentionally share that analytical anchor. The joint table is presented as a construct-consistency and coupling check, not as a causal or independent-association result; non-diagonal cells show that the fields are not synonyms.
- **Publication robustness.** The study set contains 31 conference/journal studies, 164 preprints, and four benchmark/report/other records. Reproducible validation is the modal principal output in both formal-publication and preprint subsets, while shape ordering is not identical. The manuscript treats this as a description of publicly reported systems rather than a causal publication-status effect.
- **RQ1 empirical support.** A source-located study--primitive extraction separates workflow-active use, evaluation/support use, and both. Table 5 reports these non-exclusive roles. Co-occurrence checks show that reconnaissance/pentest machinery accompanies controlled task completion in 44 of 49 studies, patch/build/test validation accompanies reproducible validation in 28 of 35, and replay/PoC/PoV execution accompanies reproducible validation in 51 of 75. These observations describe technical dependence, not dynamic tool selection or causation.
- **Domain and time stratification.** Source-located target-domain assignments support the domain-by-output panel, and publication year supports the year-by-shape panel. The 2026 counts are marked as an incomplete-year description rather than a trend.
- **Public artifacts and training overlap.** Source-located author extraction located 50 public implementations, five environment/build descriptions, 14 trigger/replay/PoC/PoV artifacts, six traces/logs, and five patch artifacts. Located does not mean executed or reproduced. Training-overlap controls were explicit in six studies, discussed without a control in two, and not located in 191.
- **Reference architecture.** Figure 5 labels only nodes that map to existing lifecycle/capability fields with coder-sensitive ranges and supports other design elements with representative citations. It is identified as a corpus-grounded synthesis, not an experimentally validated architecture or fifth system shape. The worked trace was shortened while retaining model, runtime, tool, state, validation, repair, packaging, and human-gate responsibilities.
- **Reference metadata.** All 2026 BibTeX entries retain authors, titles, years, and a DOI, arXiv identifier, or official URL. Across both bibliography files, 189 pure arXiv preprints were normalized to one `howpublished`/DOI/URL form; entries with formal publication DOIs retain those DOIs.

## Recomputed Statistics

- Corpus: 1,785 source records; 1,772 studies; 199 target-software; 150 extended synthesis (88 full text, 62 metadata); 670 background/reference; 753 excluded.
- Primary shapes: 46 candidate analysis; 34 feedback-driven fuzzing; 62 reproduction/validation/repair; 57 long-horizon penetration testing or CRS.
- Principal outputs: 34 candidate judgment; 55 controlled task completion; 21 runtime safety signal; 83 reproducible validation; six externally traceable material.
- Publication status: 31 formal publications; 164 preprints; four benchmark/report/other.
- Public-artifact and training-overlap counts are recorded above and in their source-located CSVs.
- Complete per-label reliability and the reporting-and-audit disagreement audit are indexed in `ARTIFACT_INDEX.md`.

## Unchanged Core Data

No study-level lifecycle, capability, primary-shape, principal-output, external-traceability, or claim-boundary assignment was changed. The corpus scope and analytical-layer assignments remain 199 target-software and 150 extended-synthesis studies. The original author labels and complete independent second-coder labels remain separate; sensitivity analysis substitutes one full assignment set for the other without changing either source file.

## Second-Coder Record

The methods section identifies Shangru Zhao, University of Chinese Academy of Sciences, and records his background in software security and LLM agents. He independently reviewed all 199 included target-software studies after calibration without seeing the primary labels or final assignments. Screening and stratification were not represented as independently double-screened. Acknowledgment consent and any separate ACM authorship assessment remain decisions for the author; no consent or authorship status is inferred here.

## Validation

- `python build_final_multisource_prisma_20260730.py`: exit code 0; regenerated the integrated manuscript-facing account and preserved source-specific provenance from frozen inputs.
- `python reproduce_tables.py`: exit code 0 in standalone public mode; all 42 manifest paths and manuscript-facing statistics verified without an external LaTeX directory.
- `python reproduce_tables.py --manuscript ../latex/latex_acm_csur_en/main_acm_csur.tex`: exit code 0; the recursive manuscript check verified the integrated counts, cutoff date, artifact paths, and absence of historical-round flow language.
- LaTeX/BibTeX compilation: exit code 0; 36-page PDF. The final page contains only the end of the bibliography; no font, margin, or bibliography-size reduction was applied.
- Undefined citations/references: none.
- Overfull boxes: none.
- Visual inspection: all 36 pages rendered; the unified Figure 3 and adjacent methodology pages show no overlap, clipping, abnormal blank area, or interrupted sentence. Box 1 follows its Section 3.2 introduction, and the final reference page is not clipped.

## Snapshot

The immutable tag `csur-submission-2026-07-final-v8` remains unchanged. This local documentation and manuscript closure is intentionally untagged and unpushed, as required for the present pass.
