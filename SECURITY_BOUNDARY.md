# Security Boundary

This artifact is designed for survey auditability, not for vulnerability reproduction.

## Included

- Corpus-layer metadata for candidate records.
- Study-level coding decisions, adjudication records, and coding rationales.
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

## Release Export

Build the public directory with `python scripts/build_public_release.py <new-output-directory>`. The allowlist-based export excludes local review files even when a user archives the directory outside Git. `.gitignore` remains a source-repository safeguard, not the release boundary.

The reproducibility audit follows the exclusions above and also omits Zotero PDFs and private local paths.

The product-ecosystem snapshot records only official public product, model, help, blog, and policy materials. It remains outside the research-study counts, and product changes do not alter study-level statistics without a documented corpus update.

