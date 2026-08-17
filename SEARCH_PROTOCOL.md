# Integrated Search Protocol

## Scope

The review integrates database and supplementary searches for public material dated from 2023-01-01 through 2026-07-30. The analytical start date marks the period in which public Agentic LLM vulnerability-discovery and validation workflows became the review target; earlier LLM-assisted analysis, fuzzing, code-model, and orchestration studies remain eligible as background.

The complete protocol, source-specific query strings, access status, and execution details are preserved in `FINAL_MULTISOURCE_SEARCH_PROTOCOL_20260730.md` and `data/final_multisource_search_20260730_access_log.csv`.

## Sources

Exportable results were collected through:

- arXiv official API;
- OpenAlex;
- Crossref and publisher-prefix queries for ACM, IEEE, Springer, and Elsevier records.

Supplementary discovery and formal-version checks used official ACM, IEEE, Springer, ScienceDirect, USENIX, NDSS, and DBLP pages where accessible, together with seed studies, backward and forward snowballing, benchmark pages, project pages, and DOI/title checks. These web checks are not represented as complete database exports. The access log records source-specific access and export status directly.

## Query Logic

Four concept groups were adapted to each interface:

1. Agent/system form: LLM, large language model, agent, agentic, multi-agent, autonomous system, or cyber reasoning system.
2. Security task: vulnerability discovery/detection, fuzzing, penetration testing, exploit/PoC/PoV generation, repair, patch validation, or disclosure.
3. Interaction and evidence: tool use, execution, feedback, coverage, crash, sanitizer, oracle, replay, validation, or environment.
4. Evaluation and governance: benchmark, cost, ablation, failure analysis, human approval, permission, sandbox, audit, or external record.

The exact strings and pagination are stored in the access log and raw-export manifest rather than reconstructed from prose.

## Screening and Reconciliation

All source records acquired through the searches above were integrated through the July 30, 2026 cutoff, deduplicated at the source-occurrence level, reconciled across study versions, and assessed under common eligibility and analytical-layer rules. The final ledger contains 1,785 source records representing 1,772 studies. Thirteen alternate versions, exact duplicates, or source variants remain in the crosswalk without independent counting. Analytical allocation is:

- 199 target-software studies;
- 154 extended-synthesis studies, including governance and agent-safety context outside the target-software denominator;
- 668 background/reference studies;
- 751 excluded studies.

The 199 target-software studies have detailed public workflow and evaluation material for complete coding. The 154-study extended synthesis comprises 92 studies supported by full text or equivalent public material and 62 supported by audited title-and-abstract metadata. Source-interface exports, query-specific filtering, retrieval decisions, and acquisition dates remain in the linked audit files as provenance; because these fields were not recorded uniformly across all acquisition sources, they are not aggregated into manuscript-wide retrieval totals.

## Inclusion Boundary

Study-level inclusion requires public evidence that context or feedback interpreted by an LLM changes a later tool-mediated action or retained workflow state in vulnerability discovery, exploration, execution observation, validation, repair, or reporting. A stand-alone label, explanation, or general code-generation result does not satisfy this boundary. Adjacent mechanisms, benchmarks, and evaluation studies with partial workflow relevance enter extended synthesis; conventional primitives and general context enter background/reference; near-neighbor exclusions retain record-level reasons.

## Historical Provenance

Earlier source-ledger, July 15 arXiv, July 16 official-source, and round-specific coding files are retained to preserve provenance. The manuscript presents the integrated method and final counts above rather than treating those execution stages as separate analytical corpora.
