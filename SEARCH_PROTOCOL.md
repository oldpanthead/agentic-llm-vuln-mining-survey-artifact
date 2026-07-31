# Integrated Search Protocol

## Scope

The review integrates database and supplementary searches for public material dated from 2023-01-01 through 2026-07-30. The analytical start date marks the period in which public Agentic LLM vulnerability-discovery and validation workflows became the review target; earlier LLM-assisted analysis, fuzzing, code-model, and orchestration studies remain eligible as background.

The complete protocol, source-specific query strings, access status, and execution details are preserved in `FINAL_MULTISOURCE_SEARCH_PROTOCOL_20260730.md` and `data/final_multisource_search_20260730_access_log.csv`.

## Sources

Exportable results were collected through:

- arXiv official API;
- OpenAlex;
- Crossref and publisher-prefix queries for ACM, IEEE, Springer, and Elsevier records.

Supplementary discovery and formal-version checks used official ACM, IEEE, Springer, ScienceDirect, USENIX, NDSS, and DBLP pages where accessible, together with seed studies, backward and forward snowballing, benchmark pages, project pages, DOI/title checks, and prior retained records. These web checks are not represented as complete database exports. Google Scholar was blocked during execution; Scopus and Web of Science were unavailable without authenticated access. The access log records these limits directly.

## Query Logic

Four concept groups were adapted to each interface:

1. Agent/system form: LLM, large language model, agent, agentic, multi-agent, autonomous system, or cyber reasoning system.
2. Security task: vulnerability discovery/detection, fuzzing, penetration testing, exploit/PoC/PoV generation, repair, patch validation, or disclosure.
3. Interaction and evidence: tool use, execution, feedback, coverage, crash, sanitizer, oracle, replay, validation, or environment.
4. Evaluation and governance: benchmark, cost, ablation, failure analysis, human approval, permission, sandbox, audit, or external record.

The exact strings and pagination are stored in the access log and raw-export manifest rather than reconstructed from prose.

## Screening and Reconciliation

Saved interfaces returned 12,090 source occurrences. Documented query-specific filtering retained 2,289 occurrences; exact source-level deduplication produced 1,642 unique interface records for title/abstract screening. Reports were sought for 274 records, 239 were assessed at full text, and 35 could not be retrieved from the documented public sources.

Full-text assessment yielded 132 target-software studies, 83 extended-synthesis studies, 21 background records, and three exclusions from the interface search. Supplementary identification contributed 143 additional non-overlapping source records. Version reconciliation then combined preprints, formal publications, exact duplicates, and source variants at study level.

The final ledger contains 1,785 source records and 1,772 studies. Analytical allocation is:

- 199 target-software studies;
- one governance boundary case;
- 149 extended-synthesis studies;
- 670 background/reference studies;
- 753 excluded studies.

Thirteen alternate versions or source variants remain in the crosswalk without separate counting.

## Inclusion Boundary

Study-level inclusion requires public evidence that context or feedback interpreted by an LLM changes a later tool-mediated action or retained workflow state in vulnerability discovery, exploration, execution observation, validation, repair, or reporting. A stand-alone label, explanation, or general code-generation result does not satisfy this boundary. Adjacent mechanisms, benchmarks, and evaluation studies with partial workflow relevance enter extended synthesis; conventional primitives and general context enter background/reference; near-neighbor exclusions retain record-level reasons.

## Historical Provenance

Earlier source-ledger, July 15 arXiv, July 16 official-source, and round-specific coding files are retained to preserve provenance. The manuscript presents the integrated method and final counts above rather than treating those execution stages as separate analytical corpora.
