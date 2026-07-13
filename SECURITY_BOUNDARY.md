# Security Boundary

This artifact is designed for survey auditability, not for vulnerability reproduction.

## Included

- Corpus-layer metadata for candidate records.
- Legacy A/E coding decisions and rationales for the study-level coded records.
- Bibliographic audit fields such as DOI, arXiv ID, official URL, venue, and publication status.
- Reproducibility checks for corpus counts and coding distributions.
- Templates for independent second-coder checking and disagreement resolution.

## Excluded

- Undisclosed PoCs.
- Exploit payloads.
- Private targets, credentials, tokens, or service endpoints.
- Live vulnerability reproduction instructions.
- Sensitive crash inputs or proof artifacts that could enable exploitation.
- Private communication with vendors, bug bounty programs, or affected maintainers.

## Handling High-Risk Claims

Claims involving CVEs, zero-days, bug bounty outcomes, vendor confirmation, exploitability, or real-world deployment impact should be treated as author-reported or public-material-supported unless independently verified and explicitly documented.

## Reviewer Use

Reviewers can use this artifact to inspect corpus construction, coding logic, and bibliographic traceability. The artifact should not be used as an exploit reproduction package.

## Future Release

Before public release, authors should decide:

- which working/proposed audit files to include;
- whether second-coder adjudication files are ready for release;
- the public license;
- the archival target, such as GitHub, Zenodo, or both.

The reproducibility audit does not publish Zotero PDFs, private paths, undisclosed PoC, exploit payloads, sensitive crash inputs, private targets, credentials, or vendor communications. Local review files are excluded through `.gitignore`.

The product-ecosystem snapshot records only official public product, model, help, blog, and policy materials. It is an independent boundary data layer, not part of the 212 candidate-record corpus, and product changes do not automatically alter Core statistics.

