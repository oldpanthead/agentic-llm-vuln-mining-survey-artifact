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

## Submission-Time Update Search

A separate arXiv update/sensitivity search was run on 2026-07-15 with four broader query groups defined in `submission_update_search.py`. Unlike the reconciled historical ledger, this search preserves raw Atom responses, query timestamps, pagination, and SHA-256 hashes. It returned 432 unique records: 12 matched the existing corpus, 26 were first submitted after the analytical cutoff, 41 advanced to full-text author review, 30 were retained as contextual/background update candidates, and 323 were excluded at title/abstract screening. Record-level screening decisions are in `data/submission_update_20260715_screening_audit.csv`.

The 41 full-text records received an author audit, an independent blind coding pass, and an author-confirmed evidence-based resolution. Canonical matching found all 41 to be new studies. The integrated cohort adds 37 target-software study-level records and four extended-synthesis records; original coder inputs, pre-adjudication metrics, resolution traces, and the integration crosswalk remain public in the artifact.
## Counting Policy

`record_id` is the source-record key in the public screening ledger. The artifact records 253 source records and uses `data/study_version_crosswalk.csv` to resolve them into 248 canonical studies. Current canonical analysis-use counts are 68 study-level coded records (67 target-software studies plus one governance boundary case), 65 extended synthesis studies, 95 background/reference records, and 20 excluded near-neighbor studies. Source-search counts in `data/source_search_log.csv` describe captured source records and canonical allocations rather than volatile web-result totals.

Zotero metadata is used for title, source-type, DOI/URL, venue, and local
bibliographic reconciliation. Local Zotero paths, PDFs, SQLite databases, and
private working directories are excluded from the public artifact.
