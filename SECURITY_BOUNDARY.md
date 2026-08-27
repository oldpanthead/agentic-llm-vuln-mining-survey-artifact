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

This tagged repository is the public export. The compact bundle manifest and `reproduce_tables.py` define the files that belong to this snapshot; internal release-builder scripts and superseded manifests remain in repository history.

The reproducibility audit follows the exclusions above and also omits Zotero PDFs and private local paths.

Official product and policy pages, when encountered during boundary checks, remain outside the research-study counts and do not alter study-level statistics without a documented corpus update. They are not included as empirical study evidence in this release.

