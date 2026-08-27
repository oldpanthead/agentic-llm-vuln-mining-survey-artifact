# Final Integrated Multi-Source Search and PRISMA Account

## Scope

The review integrates database, metadata-index, publisher, conference, seed, snowball, benchmark, and project searches covering 2023-01-01 through 2026-07-30. Search executions occurred on their recorded dates; the account does not claim that every interface was queried on one day or with identical export capabilities.

## Database and Metadata Exports

| Source/interface | Exported occurrences | Entered deduplication |
|---|---:|---:|
| acm_crossref | 2000 | 34 |
| arxiv | 1673 | 1673 |
| crossref | 2000 | 84 |
| elsevier_crossref | 2000 | 14 |
| ieee_crossref | 2000 | 53 |
| openalex | 417 | 417 |
| springer_crossref | 2000 | 14 |

Publisher-filtered Crossref feeds were used for ACM, IEEE, Springer, and Elsevier metadata. Official ACM Digital Library, IEEE Xplore, SpringerLink, ScienceDirect, USENIX, NDSS, and DBLP pages were checked as supplementary interfaces; their access records are preserved even where no complete export count was available. Scopus and Web of Science were inaccessible without authenticated subscriptions, and Google Scholar automated access was blocked, so none is represented as a completed database export.
ArXiv and OpenAlex occurrences entered deduplication under their source-query boundaries. Crossref-derived occurrences additionally required a vulnerability, security-testing, or offensive-security cue in the title; the source-count file records the resulting interface-specific reductions.

## Manuscript-Facing Integrated PRISMA-ScR Account

| Stage | Item | Count |
|---|---|---:|
| integrated_flow | integrated source records | 1785 |
| integrated_flow | alternate or duplicate source versions not counted | 13 |
| integrated_flow | version reconciled studies screened | 1772 |
| integrated_flow | target software studies with detailed material | 199 |
| integrated_flow | extended synthesis full text or equivalent | 92 |
| integrated_flow | extended synthesis metadata supported | 62 |
| integrated_flow | final extended synthesis studies | 154 |
| integrated_flow | background reference studies | 668 |
| integrated_flow | excluded studies | 751 |

## Final Analytical Allocation

After version reconciliation, the integrated corpus contains **1772 studies** from **1785 source records**: **199 target-software studies**, **154 extended-synthesis studies**, **668 background/reference studies**, and **751 excluded studies**. Each study enters one final layer.

## Source-Specific Acquisition Provenance

The following rows preserve interface-specific query, filtering, retrieval, and historical integration provenance. Their stages were recorded under different acquisition workflows and are not presented as separate analytical cohorts or aggregated into manuscript-wide retrieval totals.

| Provenance stage | Item | Count |
|---|---|---:|
| identification | exported source occurrences | 12090 |
| identification | removed by deterministic query filter | 9801 |
| deduplication | source occurrences entering deduplication | 2289 |
| deduplication | duplicate source occurrences removed | 647 |
| screening | unique search records screened | 1642 |
| screening | records not advanced to report retrieval | 1364 |
| retrieval | reports sought | 278 |
| retrieval | reports not retrieved | 35 |
| eligibility | reports assessed at full text | 243 |
| eligibility | full text study level | 132 |
| eligibility | full text extended synthesis | 87 |
| eligibility | full text background reference | 21 |
| eligibility | full text excluded near neighbor | 3 |
| integration | current search matches to retained studies | 110 |
| integration | new or reconciled source records added | 1532 |
| integration | supplementary source records not reidentified | 143 |
| integration | prior canonical studies not reidentified | 138 |
| prior_path | prior source records | 253 |
| prior_path | prior canonical studies | 248 |
| prior_path | prior target software studies | 67 |
| prior_path | prior extended synthesis studies | 65 |
| prior_path | prior governance boundary record | 1 |
| current_path | new canonical studies | 1524 |
| current_path | new target software studies | 132 |
| current_path | new extended synthesis studies | 88 |
| current_path | new extended full text supported | 87 |
| current_path | new extended metadata supported | 1 |
| current_path | new background reference studies | 573 |
| current_path | new excluded studies | 731 |
| final | extended synthesis full text supported | 92 |
| final | extended synthesis metadata supported | 62 |
| final | integrated source records | 1785 |
| final | integrated canonical studies | 1772 |
| final | target software studies | 199 |
| final | extended synthesis studies | 154 |
| final | background reference studies | 668 |
| final | excluded studies | 751 |

Historical search files remain unchanged as provenance. The final extended-synthesis material basis is 92 studies supported by full text or equivalent public material and 62 supported by audited title-and-abstract metadata.

## Search Protocol

### Scope

- Coverage window: 2023-01-01 through 2026-07-30.
- Search execution date: 2026-07-31.
- Review scope: LLM-centered systems that affect tool-mediated actions or retained state in vulnerability discovery, fuzzing, execution observation, reproduction or validation, repair checking, penetration testing, cyber reasoning, or closely related evaluation and governance work.
- Counting unit: canonical study after title, DOI, arXiv identifier, URL, and study-version reconciliation.

This pass is a final coverage check. It does not overwrite earlier search exports or change an analytical layer until a newly discovered study passes record-level screening and version reconciliation.

### Query Families

1. Agent and task: LLM or large language model; agent, agentic, or multi-agent; vulnerability, fuzzing, penetration testing, or cyber reasoning.
2. Execution and validation: LLM or large language model; vulnerability, fuzzing, or software security; execution feedback, validation, tool use, crash, coverage, sanitizer, oracle, replay, or harness.
3. PoV and CRS: proof of vulnerability, PoV, cyber reasoning system, or CRS; LLM or agent.
4. Review and evaluation context: review or survey; LLM or large language model; vulnerability, fuzzing, or software security.

Exact source-specific strings and access outcomes are preserved in the released search access log and screening ledgers.

### Discovery Sources

- arXiv official API: complete metadata export for the four query families.
- Crossref REST API: ranked supplementary formal-publication metadata, including publisher-prefix searches for ACM, IEEE, Springer, and Elsevier. Crossref free-text results are broad relevance-ranked sets rather than an exact Boolean census; the manifest records both reported totals and fixed retrieval caps.
- OpenAlex API: broad scholarly-index search used to recover formal versions and records not consistently indexed by one publisher interface.
- Source-restricted web searches over ACM Digital Library, IEEE Xplore, SpringerLink, ScienceDirect, USENIX, NDSS, and DBLP pages. These are supplementary when a platform blocks automated export or requires an API key.
- Citation and version reconciliation using current corpus titles, DOI and arXiv identifiers, public references, and official venue pages.

Google Scholar is attempted as a supplementary source. If automated access is blocked, the access result is recorded rather than represented as a completed database export. Scopus and Web of Science are used only when authenticated access is available.

### Screening and Reconciliation

1. Merge source records while preserving every source occurrence.
2. Normalize titles, DOI values, arXiv identifiers, and URLs.
3. Match exact identifiers and normalized titles against the current corpus.
4. Flag high-similarity title/author matches for manual version review.
5. Screen unmatched records by title and abstract, followed by full text for potentially eligible records.
6. Prefer a formal publication over its preprint when they report the same study; retain the version link in the crosswalk.
7. Assign one primary analytical layer per canonical study.

New study-level records, if any, use the current codebook and require the same independent second-coder procedure before entering manuscript distributions.

### Reader-Facing Reporting

The manuscript reports integrated search coverage, final search date, canonical-study accounting, eligibility rules, and final PRISMA flow. Earlier exports remain as provenance, but intermediate update-round counts are not required in the reader-facing narrative once the final multi-source search has been reconciled.
