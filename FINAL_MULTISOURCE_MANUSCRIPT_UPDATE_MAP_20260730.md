# Final Multi-Source Manuscript Update Map (2026-07-30)

This file records the manuscript locations that must be updated after human
screening, second coding, version reconciliation, and final corpus integration.
It is not a source of final counts and does not replace the screening audit.

## Integrated search narrative

The final manuscript should describe one integrated review search covering
2023-01-01 through 2026-07-30. It may combine searches conducted on different
dates, but must not imply that every database was queried once or on the same
day. Historical round names and execution chronology remain in the artifact.

Recommended method structure:

1. sources and date coverage;
2. four concept groups and source-specific syntax;
3. title/abstract screening and full-text eligibility;
4. exact-key deduplication plus study/version reconciliation;
5. analytical allocation and final study counts;
6. coding and reliability after inclusion.

## Manuscript replacement points

- `main_acm_csur.tex` abstract: replace 248/67/65 and dependent findings only
  after final integration and recoding.
- `sections/01_introduction.tex`: update scope denominators and any findings
  whose numerators or denominators change.
- `sections/03_methodology.tex`, opening search paragraph: replace the separate
  July arXiv update account with the integrated source and date description.
- `sections/03_methodology.tex`, PRISMA figure and description: rebuild from the
  final identification, deduplication, screening, retrieval, exclusion,
  reconciliation, and analysis-use counts. Do not retain earlier/update lanes as
  the main visual organization.
- `sections/03_methodology.tex`, corpus composition figure: regenerate year and
  source-type panels from the final reconciled source ledger.
- `sections/03_methodology.tex`, stratification paragraph: update every layer
  count after version reconciliation.
- `sections/03_methodology.tex`, second-coder section: report the final added
  study-level records and their human review without presenting search rounds as
  separate methodological standards.
- `sections/03_methodology.tex`, cohort distribution table: remove or replace it
  with a corpus-level summary if the round comparison no longer answers an
  analytical question. Round provenance remains in the artifact.
- `sections/03_methodology.tex`, threats: remove the July arXiv-asymmetry sentence
  after the integrated multi-source search; retain only actual residual source
  access limitations.
- `sections/04_lifecycle.tex` through `sections/08_conclusion.tex`: recompute all
  corpus-derived counts and conclusions from the final integrated matrix.
- `sections/09_appendix.tex`: update the study matrix, reporting examples, and
  reliability denominators.
- Data Availability: point to a new immutable artifact snapshot only after the
  final local validation; do not move an existing tag.

## Access limitations that must remain factual

- arXiv and OpenAlex were retrieved through paginated APIs.
- Crossref supplied ranked metadata candidates and is not described as an
  exhaustive Boolean export from publisher databases.
- ACM DL, IEEE Xplore, SpringerLink, ScienceDirect, DBLP, USENIX, and NDSS were
  checked through accessible source-restricted interfaces; no complete structured
  export is claimed where one was not obtained.
- Scopus and Web of Science were unavailable in the execution environment.
- Google Scholar was attempted only as a supplementary source and was blocked.
- Publicly unavailable full texts remain explicitly unresolved rather than being
  assessed from abstracts as though they were full reports.

## Release gate

No final manuscript count should be changed until all of the following hold:

- author screening decisions are confirmed;
- the blind human second-coder file is complete;
- eligibility disagreements are explicitly resolved;
- duplicate/version relations are confirmed;
- one canonical study occupies one primary analytical layer;
- all corpus-derived tables and figures reproduce from the integrated files.
