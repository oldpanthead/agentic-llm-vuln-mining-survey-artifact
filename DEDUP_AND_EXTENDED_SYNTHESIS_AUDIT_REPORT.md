# Deduplication and Extended Synthesis Audit Report

This report documents the canonical study deduplication and extended-synthesis substantiation pass for the public artifact and current ACM CSUR manuscript.

## 1. Counts Before Canonical Deduplication

Source-record layer counts retained in `data/corpus.csv` and `data/source_screening_audit.csv`:

- Source records in screening ledger: 212
- Legacy Core source records: 31
- Legacy Supporting source records: 66
- Background source records: 95
- Excluded source records: 20

## 2. Counts After Canonical Deduplication

Analytical counts now use canonical studies from `data/study_version_crosswalk.csv`:

- `background_reference`: 95
- `excluded_near_neighbor`: 19
- `extended_synthesis`: 62
- `study_level_coded`: 31

Total canonical candidate studies: 207.

## 3. Merged Record Groups

- `CP094` counted as `study_level_coded`; alternates: `CP097` (source_variant_not_counted; same normalized title/system as CP094; local Zotero fragment duplicate of official USENIX page)
- `CP101` counted as `excluded_near_neighbor`; alternates: `CP073` (alternate_version_not_counted; same DOI as CP101; arXiv preprint superseded by IEEE conference record)
- `CP102` counted as `study_level_coded`; alternates: `CP074` (alternate_version_not_counted; same title and DOI as CP102; preprint superseded by IEEE conference record)
- `CP104` counted as `extended_synthesis`; alternates: `CP087` (alternate_version_not_counted; same title and arXiv DOI as CP104; preprint superseded by IEEE conference record)
- `CP208` counted as `study_level_coded`; alternates: `CP106` (exact_duplicate_removed; same title, arXiv ID, DOI, and URL as CP208)

## 4. Canonical Record Selection Basis

Formal or official versions are preferred when available. The crosswalk preserves alternate versions through `same_study_as`, `dedup_basis`, `version_type`, and `counting_status`. RFCAudit is represented by the IEEE conference record `CP102` while preserving the existing study-level evidence coding decisions; PANGOLIN is represented by the official USENIX page `CP094`; OSS-CRS is represented by the verified arXiv/HTML record `CP208`; MultiFuzz is represented by the IEEE record `CP104`; the A2A near-neighbor is represented by the IEEE record `CP101`.

## 5. Cross-Layer Duplicates

The pass identified and resolved Core/Supporting cross-layer duplicates for RFCAudit (`CP074`/`CP102`), PANGOLIN (`CP094`/`CP097`), and OSS-CRS (`CP106`/`CP208`). The alternate versions are retained for provenance but no longer enter an independent analytical denominator.

## 6. Alternate Versions Removed From Extended Synthesis

- `CP087` MultiFuzz preprint: alternate of `CP104`.
- `CP097` PANGOLIN local/source variant: alternate of `CP094`.
- `CP102` RFCAudit conference record: promoted to canonical study-level coded record, replacing the preprint record ID for C09.
- `CP106` OSS-CRS duplicate arXiv record: alternate of `CP208`.

## 7. Figure 2 and Manuscript Number Changes

Figure 2 now separates 212 source-record year/source distributions from the final canonical analysis-use allocation: 30 target-software study-level coded studies, one governance boundary coded record, 62 extended synthesis studies, 95 background/reference records, and 19 excluded near-neighbor studies. The analytical corpus is 93 canonical studies: 31 study-level coded records plus 62 extended synthesis studies.

## 8. Extended Synthesis Contribution Substantiation

The extended synthesis audit now contains 62 canonical studies. Template contribution and reason fields were replaced with study-specific text containing the study title and its concrete synthesis role.

Primary roles:

- `adjacent_candidate_analysis`: 4
- `adjacent_fuzzing_or_testing`: 29
- `agent_orchestration`: 7
- `benchmark_or_evaluation`: 15
- `evidence_or_reproducibility`: 7

Material types:

- `conference_paper`: 26
- `journal_article`: 15
- `preprint_or_arxiv`: 21

## 9. RQ Mapping

RQ contribution values after audit:

- `RQ2_context`: 47
- `evaluation_agenda`: 15

The extended synthesis set primarily supports contextual RQ2 synthesis and the evaluation agenda. RQ1 draws additionally on the background/reference literature about traditional security primitives rather than being inferred from the extended synthesis CSV alone.

## 10. Manual Review Rows

None.

## 11. Script Validation

`python reproduce_tables.py` was run after the pass. It checks that canonical counted studies total 207, one canonical study has one counted record and one primary analytical layer, counted records have no duplicate normalized title/DOI/arXiv/URL, the extended synthesis audit has 62 canonical rows, and public material locators do not use local fragments.

## 12. Closure Statement

One canonical study is counted once. Source records remain available for provenance, version history, and search transparency, but analytical denominators use `data/study_version_crosswalk.csv`.
