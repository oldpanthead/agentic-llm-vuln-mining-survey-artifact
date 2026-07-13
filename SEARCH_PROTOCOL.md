# Source-Specific Search Protocol

This file records the source-specific search and screening protocol used by the
current manuscript artifact. The protocol is designed for auditability of the
mapping-oriented scoping review corpus, not for claiming a PRISMA-complete
systematic review.

## Search Date And Scope

- Search ledger date: 2026-06-30
- Date range covered: 2023-01-01 to 2026-06-30
- Corpus scope: Agentic LLM systems for vulnerability mining, vulnerability
  validation, fuzzing, PoC/PoV generation, automated penetration testing, cyber
  reasoning systems, benchmarks, reproducibility artifacts, and Agent security
  governance boundaries.
- Product ecosystem materials are maintained separately in
  `data/product_ecosystem_snapshot.csv` and are not counted as corpus records.

## Sources

The screening ledger uses the following source buckets:

- ACM Digital Library
- arXiv / CoRR
- DOI / Crossref / publisher-title lookup
- IEEE Xplore
- ScienceDirect / Elsevier
- SpringerLink
- USENIX / security-conference official pages
- Local Zotero / seed / snowball metadata

The source buckets are recorded in `data/source_search_log.csv`. Record-level
source assignment and screening decisions are recorded in
`data/source_screening_audit.csv`.

## Concept Groups

The search strings combine four concept groups:

- Model and system form: `LLM`, `large language model`, `agent`,
  `multi-agent`, `workflow`, `tool use`.
- Vulnerability-mining task: `vulnerability detection`, `vulnerability
  discovery`, `vulnerability validation`, `fuzzing`, `PoC`, `PoV`, `exploit`,
  `patch validation`.
- Environment interaction and evidence: `execution feedback`, `crash`,
  `coverage`, `sanitizer`, `oracle`, `replay`, `harness`, `artifact`.
- Evaluation and governance: `benchmark`, `CTF`, `bug bounty`, `CVE`, `CRS`,
  `cyber agent`, `permission`, `sandbox`, `disclosure`.

## Inclusion And Exclusion Criteria

Records are included when they have an identifiable research object, system,
benchmark, artifact, or source-limited public material related to the review
scope. Records are excluded when they are generic LLM/code-generation work
without a security task, commentary without an identifiable source object,
duplicates superseded by a later version, inaccessible records, or materials
outside vulnerability mining, validation, benchmarking, or Agent governance.

## Counting Policy

`record_id` is the source-record key in the public screening ledger. The artifact records 212 source records and uses `data/study_version_crosswalk.csv` to consolidate preprints, conference versions, exact duplicates, and source variants into 207 canonical candidate studies. Current canonical analysis-use counts are 31 study-level coded records, 62 extended synthesis studies, 95 background/reference records, and 19 excluded near-neighbor studies. Source search counts in `data/source_search_log.csv` are counts of records captured in the public screening ledger after source reconciliation; they are not volatile web-search result totals.

Zotero metadata is used for title, source-type, DOI/URL, venue, and local
bibliographic reconciliation. Local Zotero paths, PDFs, SQLite databases, and
private working directories are excluded from the public artifact.

