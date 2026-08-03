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
| integration | supplementary source records not reidentified | 143 |
| integration | prior canonical studies not reidentified | 138 |
| prior_path | prior source records | 253 |
| prior_path | prior canonical studies | 248 |
| prior_path | prior target software studies | 67 |
| prior_path | prior extended synthesis studies | 65 |
| prior_path | prior governance boundary record | 1 |
| current_path | new canonical studies | 1524 |
| current_path | new target software studies | 132 |
| current_path | new extended synthesis studies | 84 |
| current_path | new extended full text supported | 83 |
| current_path | new extended metadata supported | 1 |
| current_path | new background reference studies | 575 |
| current_path | new excluded studies | 733 |
| final | extended synthesis full text supported | 88 |
| final | extended synthesis metadata supported | 62 |
| final | integrated source records | 1785 |
| final | integrated canonical studies | 1772 |
| final | target software studies | 199 |
| final | extended synthesis studies | 150 |
| final | background reference studies | 670 |
| final | excluded studies | 753 |

## Final Analytical Allocation

After version reconciliation, the integrated corpus contains **1772 canonical studies** from **1785 source records**: **199 target-software studies**, **150 extended-synthesis studies with record-level public-material audit**, **670 background/reference studies**, and **753 excluded studies**.

## Dual-Path Closure

The prior retained path contains **248 studies** from **253 source records**: 67 target-software studies, 65 extended-synthesis studies, one governance boundary record, 95 background/reference studies, and 20 exclusions. The current interface path contributes 1524 new studies after overlap and version reconciliation. The final analytical sets therefore close as **67 + 132 = 199 target-software studies** and **65 + 84 + 1 = 150 extended-synthesis studies**.

The values 143 and 138 use different units: 143 is the number of prior source records not reidentified by the current interfaces, whereas 138 is the corresponding number of prior canonical studies. For extended synthesis, 83 is the number of current-interface records assessed at full text, while 84 is the number of new canonical extended-synthesis studies after one title-and-abstract-supported record is included. The earlier 89 full-text figure arose when that metadata-supported row inherited a generic full-text note; the corrected final material-basis account is 88 full-text-supported and 62 metadata-supported studies.

Historical search files remain unchanged as provenance. The manuscript-facing method can report the integrated source coverage, date range, screening rules, version reconciliation, and final allocation without narrating internal search rounds.
