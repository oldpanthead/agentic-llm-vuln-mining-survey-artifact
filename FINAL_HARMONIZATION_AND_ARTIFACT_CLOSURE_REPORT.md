# Major-Revision Methodological and Empirical Closure Report

## Scope

This report records the synchronized local manuscript/artifact state after the major-revision closure and OY external-rereview integration. The review scope, workflow--capability--evidence framework, four system shapes, seven capabilities, and five principal outputs were not changed. No literature search or corpus expansion was performed; the final study-level descriptive labels combine 585 frozen agreements with OY's resolutions of 410 frozen disagreements.

## Closed Reviewer Issues

- **Search and PRISMA closure.** The manuscript now presents one integrated review process through July 30, 2026. Frozen ledgers reproduce 1,785 source records, 1,772 studies after version reconciliation, 199 target-software studies, 154 extended-synthesis studies, 668 background/reference studies, and 751 exclusions. Each study enters one final analytical layer; 13 alternate versions, duplicates, or source variants remain traceable without independent counting.
- **Material-basis reconciliation.** All 199 target-software studies have detailed public workflow and evaluation material for complete coding. Extended synthesis comprises 92 studies supported by full text or equivalent public material and 62 supported by audited title-and-abstract metadata. Source-specific query, retrieval, and historical integration fields remain available as provenance rather than manuscript cohorts.
- **Reliability and external rereview.** The 199-study comparison reports positive counts, raw agreement, Cohen's kappa, and Gwet's AC1 for every lifecycle and capability label before adjudication. OY externally rereviewed 410 field-level disagreements under the prespecified codebook and source evidence; 50 QC tasks remain separate. The final matrix reports 43 reporting-and-audit studies, 69 validation-organization studies, four studies with externally traceable material as principal output, and five with a publicly aligned external trace. The reporting-and-audit disagreement record remains a pre-adjudication boundary record.
- **Shape/output construct relation.** Primary shape records the dominant organization and objective of agent control; principal output records the observable result supporting the main evaluated contribution. They intentionally share that analytical anchor. The joint table is presented as a construct-consistency and coupling check, not as a causal or independent-association result; non-diagonal cells show that the fields are not synonyms.
- **Publication robustness.** The study set contains 31 conference/journal studies, 164 preprints, and four benchmark/report/other records. Reproducible validation is the modal principal output in both formal-publication and preprint subsets, while shape ordering is not identical. The manuscript treats this as a description of publicly reported systems rather than a causal publication-status effect.
- **RQ1 empirical support.** A source-located study--primitive extraction separates workflow-active use, evaluation/support use, and both. Table 5 reports these non-exclusive roles. Co-occurrence checks show that reconnaissance/pentest machinery accompanies controlled task completion in 44 of 49 studies, patch/build/test validation accompanies reproducible validation in 28 of 35, and replay/PoC/PoV execution accompanies reproducible validation in 51 of 75. These observations describe technical dependence, not dynamic tool selection or causation.
- **Domain and time stratification.** Source-located target-domain assignments support the domain-by-output panel, and publication year supports the year-by-shape panel. The 2026 counts are marked as an incomplete-year description rather than a trend.
- **Public artifacts and training overlap.** Source-located author extraction located 50 public implementations, five environment/build descriptions, 14 trigger/replay/PoC/PoV artifacts, six traces/logs, and five patch artifacts. Located does not mean executed or reproduced. Training-overlap controls were explicit in six studies, discussed without a control in two, and not located in 191.
- **Reference architecture.** Figure 5 labels only nodes that map to existing lifecycle/capability fields and supports other design elements with representative citations. It is identified as a corpus-grounded synthesis, not an experimentally validated architecture or fifth system shape. The worked trace was shortened while retaining model, runtime, tool, state, validation, repair, packaging, and human-gate responsibilities.
- **Reference metadata.** All 2026 BibTeX entries retain authors, titles, years, and a DOI, arXiv identifier, or official URL. Across both bibliography files, 189 pure arXiv preprints were normalized to one `howpublished`/DOI/URL form; entries with formal publication DOIs retain those DOIs.

## Recomputed Statistics

- Corpus: 1,785 source records; 1,772 studies; 199 target-software; 154 extended synthesis (92 full text, 62 metadata); 668 background/reference; 751 excluded.
- Primary shapes: 41 candidate analysis; 33 feedback-driven fuzzing; 70 reproduction/validation/repair; 55 long-horizon penetration testing or CRS.
- Principal outputs: 51 candidate judgment; 56 controlled task completion; 19 runtime safety signal; 69 reproducible validation; four externally traceable material.
- Publication status: 31 formal publications; 164 preprints; four benchmark/report/other.
- Public-artifact and training-overlap counts are recorded above and in their source-located CSVs.
- Complete per-label reliability and the reporting-and-audit disagreement audit are indexed in `ARTIFACT_INDEX.md`.
- The adjudication form, 995-row decision log, completion manifest, and final statistics are indexed in `ARTIFACT_INDEX.md`.

## Preserved And Final Data

The corpus scope and analytical-layer assignments are 199 target-software and 154 extended-synthesis studies. The original author matrix and complete independent second-coder matrix remain unchanged and separate. OY's external-rereview decisions produce a distinct adjudicated 199-study matrix for descriptive distributions; they do not overwrite either independent source or create a post-adjudication reliability statistic.

## Screening And Coding Reliability Record

For title-and-abstract screening, a second reviewer first completed a disjoint 20-record calibration and then independently assessed a deterministic fixed-seed random sample of 153 records from the 1,524-record screening frame without access to the first reviewer's decisions. Exact agreement was 142/153 (92.8%), Cohen's kappa was 0.690, and Gwet's AC1 was 0.906. The reviewers resolved all 11 disagreements by consensus while preserving both original decisions. The record-level calibration, blind-screening, comparison, and consensus workbooks remain in the confidential screening-audit archive and are not part of the public artifact.

For post-inclusion coding, the methods section identifies Shangru Zhao, University of Chinese Academy of Sciences, and records his background in software security and LLM agents. He independently reviewed all 199 included target-software studies after calibration without seeing the primary labels or final assignments. Acknowledgment consent and any separate ACM authorship assessment remain decisions for the author; no consent or authorship status is inferred here.

## Validation

- `python build_final_multisource_prisma_20260730.py`: exit code 0; regenerated the integrated manuscript-facing account and preserved source-specific provenance from frozen inputs.
 - `python reproduce_tables.py`: exit code 0 in standalone public mode on 2026-08-17; all manifest paths, the 410 completed decisions, the final matrix, and manuscript-facing statistics verified without an external LaTeX directory.
 - `python reproduce_tables.py --manuscript ../latex/latex_acm_csur_en/main_acm_csur.tex`: exit code 0 on 2026-08-17; the recursive manuscript check verified the integrated counts, cutoff date, artifact paths, and absence of superseded pre-adjudication ranges.
 - LaTeX/BibTeX compilation: exit code 0; 33-page PDF. No font, margin, or bibliography-size reduction was applied.
- Undefined citations/references: none.
- Overfull boxes: none.
 - Visual inspection: the affected methodology, lifecycle, benchmark, and reference pages show no overlap, clipping, or interrupted sentence. Figure 3 was replaced with the author-edited vector export, checked at manuscript scale on page 10, and matches the reconciled counts and caption.

## Snapshot

The immutable synchronized release is `csur-submission-2026-08-final-v9`. The release includes the reconciled Figure 3 asset, the manuscript link to this tag, and the validated public artifact snapshot.
