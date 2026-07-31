# Final Multi-Source Search Protocol

## Scope

- Coverage window: 2023-01-01 through 2026-07-30.
- Search execution date: 2026-07-31.
- Review scope: LLM-centered systems that affect tool-mediated actions or
  retained state in vulnerability discovery, fuzzing, execution observation,
  reproduction or validation, repair checking, penetration testing, cyber
  reasoning systems, or closely related evaluation and governance work.
- Counting unit: canonical study after title, DOI, arXiv identifier, URL, and
  study-version reconciliation.

This pass is a final coverage check. It does not overwrite the earlier search
exports or change an analytical layer until a newly discovered study has passed
record-level screening and version reconciliation.

## Query Families

The same four families are adapted to each interface:

1. **Agent and task**: LLM or large language model; agent, agentic, or
   multi-agent; vulnerability, fuzzing, penetration testing, or cyber
   reasoning.
2. **Execution and validation**: LLM or large language model; vulnerability,
   fuzzing, or software security; execution feedback, validation, tool use,
   crash, coverage, sanitizer, oracle, replay, or harness.
3. **PoV and CRS**: proof of vulnerability, PoV, cyber reasoning system, or
   CRS; LLM or agent.
4. **Review and evaluation context**: review or survey; LLM or large language
   model; vulnerability, fuzzing, or software security.

Exact source-specific strings are written to the machine-readable manifest
produced by `final_multisource_search_20260730.py`.

## Discovery Sources

- arXiv official API: complete metadata export for the four query families.
- Crossref REST API: ranked supplementary formal-publication metadata,
  including publisher-prefix searches for ACM (`10.1145`), IEEE (`10.1109`),
  Springer (`10.1007`), and Elsevier (`10.1016`). Crossref's free-text endpoint
  reports very broad relevance-ranked result sets rather than an exact Boolean
  census; the manifest therefore records both the reported total and the fixed
  retrieval cap.
- OpenAlex API: broad scholarly-index search used to recover formal versions
  and records not consistently indexed by a single publisher interface.
- Source-restricted web searches over ACM Digital Library, IEEE Xplore,
  SpringerLink, ScienceDirect, USENIX, NDSS, and DBLP pages. These searches are
  supplementary when a platform blocks automated export or requires an API
  key.
- Citation and version reconciliation using current corpus titles, DOI and
  arXiv identifiers, public references, and official venue pages.

Google Scholar is attempted as a supplementary source. If automated access is
blocked, the access result is recorded rather than represented as a completed
database export. Scopus and Web of Science are used only when authenticated
access is available.

## Screening And Reconciliation

1. Merge source records while preserving every source occurrence.
2. Normalize titles, DOI values, arXiv identifiers, and URLs.
3. Match exact identifiers and normalized titles against the current corpus.
4. Flag high-similarity title/author matches for manual version review.
5. Screen unmatched records by title and abstract, followed by full text for
   potentially eligible records.
6. Prefer a formal publication over its preprint when they report the same
   study; retain the version link in the crosswalk.
7. Assign one primary analytical layer per canonical study.

New study-level records, if any, use the current codebook and require the same
independent second-coder procedure before entering manuscript distributions.

## Reader-Facing Reporting

The manuscript reports the integrated search coverage, final search date,
canonical-study accounting, eligibility rules, and final PRISMA flow. Earlier
exports remain in the artifact as provenance, but intermediate update-round
counts are not required in the reader-facing narrative once the final
multi-source search has been reconciled.
