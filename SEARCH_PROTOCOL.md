# Source-Specific Search Protocol

This file records the source-specific search and screening protocol used by the
current manuscript artifact. The protocol is designed for auditability of the
mapping-oriented scoping review corpus, not for claiming a PRISMA-complete
systematic review.

## Reconciled Ledger Date And Scope

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

## Submission-Time arXiv Sensitivity and Recall-Recovery Search

A deliberately broader arXiv-only sensitivity and recall-recovery search was run on 2026-07-15 with four query groups defined in `submission_update_search.py`. The historical ledger was multi-source and used narrower query families; the July 15 pass assessed cutoff and query sensitivity and recovered relevant studies that predated the June 30 cutoff. Raw Atom responses, query timestamps, pagination, and SHA-256 hashes are preserved. The search returned 432 unique records: 12 matched the existing corpus, 26 were first submitted after the analytical cutoff, 41 advanced to full-text review, 30 were retained as contextual/background candidates, and 323 were excluded at title/abstract screening. Record-level decisions are in `data/submission_update_20260715_screening_audit.csv`.

The 41 full-text records received an author audit, an independent blind coding pass, and an author-confirmed evidence-based resolution. Thirty-seven entered study-level coding and four entered extended synthesis. Original and recall-recovery rounds remain separately auditable. The recall-recovery cohort broadened the empirical base and extended the reproduction-, validation-, and repair-centered shape to cover repair-centered systems, but it required no new evidence-output category and did not change the four dominant comparison shapes or the central workflow--capability--evidence finding. The resulting corpus is a documented analytical set rather than an exhaustive census.
## Counting Policy

`record_id` is the source-record key in the public screening ledger. The artifact records 253 source records and uses `data/study_version_crosswalk.csv` to resolve them into 248 canonical studies. Current canonical analysis-use counts are 68 study-level coded records (67 target-software studies plus one governance boundary case), 65 extended synthesis studies, 95 background/reference records, and 20 excluded near-neighbor studies. Source-search counts in `data/source_search_log.csv` describe captured source records and canonical allocations rather than volatile web-result totals.

Zotero metadata is used for title, source-type, DOI/URL, venue, and local
bibliographic reconciliation. Local Zotero paths, PDFs, SQLite databases, and
private working directories are excluded from the public artifact.

