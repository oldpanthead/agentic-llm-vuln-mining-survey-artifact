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

## PRISMA-ScR Account

| Stage | Item | Count |
|---|---|---:|
| identification | exported source occurrences | 12090 |
| identification | removed by deterministic query filter | 9801 |
| deduplication | source occurrences entering deduplication | 2289 |
| deduplication | duplicate source occurrences removed | 647 |
| screening | unique search records screened | 1642 |
| screening | records not advanced to report retrieval | 1368 |
| retrieval | reports sought | 274 |
| retrieval | reports not retrieved | 35 |
| eligibility | reports assessed at full text | 239 |
| eligibility | full text study level | 132 |
| eligibility | full text extended synthesis | 83 |
| eligibility | full text background reference | 21 |
| eligibility | full text excluded near neighbor | 3 |
| integration | current search matches to retained studies | 110 |
| integration | new or reconciled source records added | 1532 |
| integration | supplementary source records not reidentified | 1675 |
| integration | prior canonical studies not reidentified | 1662 |
| final | integrated source records | 1785 |
| final | integrated canonical studies | 1772 |
| final | target software studies | 199 |
| final | extended synthesis studies | 150 |
| final | background reference studies | 670 |
| final | excluded studies | 753 |

## Final Analytical Allocation

After version reconciliation, the integrated corpus contains **1772 canonical studies** from **1785 source records**: **199 target-software studies**, **150 full-text-supported extended-synthesis studies**, **670 background/reference studies**, and **753 excluded studies**. AgentFuzz is retained within extended synthesis as governance and agent-safety context and does not enter target-software distributions.

Historical search files remain unchanged as provenance. The manuscript-facing method can report the integrated source coverage, date range, screening rules, version reconciliation, and final allocation without narrating internal search rounds.
