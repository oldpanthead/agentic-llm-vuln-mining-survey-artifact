# Public Release Checklist

This checklist prepares the minimal artifact for a future GitHub or Zenodo release. It does not authorize public release by itself.

## Release Boundary

- [ ] Do not include undisclosed PoCs, exploit payloads, private targets, credentials, reproduction scripts for live vulnerabilities, or sensitive crash inputs.
- [ ] Do not include private reviewer, coder, or author notes unless explicitly intended for release.
- [ ] Keep `intercoder_sample_key.csv` private until independent second-coder work is complete.
- [ ] Confirm `data/core31_second_coder_blind.csv` does not expose original labels or answer-key fields.
- [ ] Confirm `data/core31_second_coder_adjudication_template.csv` is not used before independent coding.
- [ ] Report agreement statistics only after real second-coder decisions exist.
- [ ] Confirm that any public repository URL has author approval before replacing `[REPOSITORY URL]` in the manuscript.

## Data Files

- [x] `data/corpus.csv` contains only bibliographic/corpus-layer metadata.
- [x] `data/core_coding.csv` contains coding rationales and caveats, not exploit payloads.
- [x] `data/reference_audit.csv` has DOI coverage improved from Zotero/local audit and leaves unresolved DOI cases as `NA`.
- [x] `data/screening_summary.csv` marks unrecoverable intermediate counts as `NA`.
- [x] `data/core31_second_coder_blind.csv` can be shared for independent 31-Core strongest-evidence-output coding.
- [x] `data/intercoder_sample_blind.csv` can be shared for optional sampled review.
- [ ] Decide whether proposed/intermediate audit files should be included in public release or moved to a private working archive.
- [ ] Decide whether `zotero_export_20260530.bib` should remain private because it reflects the local Zotero library export.

## Documentation

- [x] `README.md` explains purpose, file list, reproduction command, and security boundary.
- [x] `codebook.md` defines A/E coding categories and evidence objects.
- [x] `data_dictionary.md` defines all core data fields.
- [x] `intercoder_instructions.md` explains independent second-coder workflow.
- [ ] Add final repository URL and release date.
- [ ] Add license after author decision.
- [ ] Add citation metadata if archiving on Zenodo.

## Reproducibility

- [x] `reproduce_tables.py` runs without count or A/E distribution errors.
- [x] Remaining DOI gaps are documented rather than guessed.
- [ ] If second-coder results are completed, add `data/core31_second_coder_results.csv`; do not create it from blank templates.
- [ ] If disagreements are adjudicated, add `data/core31_second_coder_adjudicated.csv`; do not create it before adjudication.
- [ ] Add `reports/SECOND_CODER_AGREEMENT_REPORT.md` only after raw agreement and Cohen's kappa are computed from real coder2 decisions.
- [ ] Record the final corpus date and search cutoff date in the manuscript and artifact README.

## Submission Notes

- [ ] In the manuscript, describe the artifact as a non-sensitive audit package.
- [ ] State that missing intermediate screening counts are `NA` because they were not recoverable from local logs.
- [ ] State that Zotero DOI merge improved metadata coverage but does not replace official landing-page verification for every record.
- [ ] State that no exploit payloads or undisclosed vulnerability reproduction materials are released.

- [x] Confirm `local_private_working/`, `.pdf`, and `.sqlite` files are not tracked.
- [x] Confirm `core_reproducibility_audit.csv` contains no private Zotero paths.
- [x] Confirm `unknown_not_audited` is not counted as absence of material.
- [x] Confirm `data/product_ecosystem_snapshot.csv` is an independent boundary layer and not counted in the 212 candidate records.
- [x] Confirm product-page changes do not automatically alter Core statistics.
