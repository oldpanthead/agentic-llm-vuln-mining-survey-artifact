# Public Release Checklist

This checklist prepares the minimal artifact for a future GitHub or Zenodo release. It does not authorize public release by itself.

## Release Boundary

- [ ] Do not include undisclosed PoCs, exploit payloads, private targets, credentials, reproduction scripts for live vulnerabilities, or sensitive crash inputs.
- [ ] Do not include private reviewer, coder, or author notes unless explicitly intended for release.
- [ ] Keep `intercoder_sample_key.csv` private until independent second-coder work is complete.
- [ ] Confirm `data/core31_second_coder_blind.csv` does not expose original labels or answer-key fields.
- [ ] Confirm `data/core31_second_coder_adjudication_template.csv` is not used before independent coding.
- [x] Report formal agreement statistics only after revised codebook freeze and new independent coding.
- [x] Maintain `SUBMISSION_UPDATE_SECOND_CODER_RERUN_NOTES.md` and the blank rerun template for a lightweight tightened-boundary update-pass rerun.
- [x] Confirm the cross-stage capability / external-traceability extension template hides original labels and contains blank coder2 fields.
- [x] Confirm cross-stage capability / external-traceability results exist after real coder2 decisions.
- [x] Report cross-stage capability / external-traceability agreement only with suitable set-style, Jaccard, or per-label metrics.
- [ ] Confirm that any public repository URL has author approval before replacing `[REPOSITORY URL]` in the manuscript.

## Data Files

- [x] `data/corpus.csv` contains only bibliographic/corpus-layer metadata.
- [x] `data/core_coding.csv` contains coding rationales and caveats, not exploit payloads.
- [x] data/source_search_log.csv and data/source_screening_audit.csv document the source-specific search ledger and record-level screening decisions.
- [x] The submission-time arXiv update export, manifest, and record-level screening audit are included.
- [x] All 41 potentially eligible update-search records received an author full-text workflow--capability--evidence audit.
- [x] The 41-row update-search blind template hides all author labels and keeps every coder2 field blank.
- [x] Complete a real independent update-search second-coder pass before any denominator change or update agreement report.
- [x] Verify the 41-record update results contain complete decisions and no author/original answer-key fields.
- [x] Recompute update-search pre-adjudication agreement from the frozen author and coder2 files.
- [x] Preserve the proposed update adjudication working draft as the reviewed pre-confirmation record.
- [x] Record the author-confirmed 37/4 update resolution without claiming two-human consensus.
- [x] Run canonical matching for all 41 adjudicated records and preserve the projected 253-source-record / 248-canonical-study impact separately from the frozen manuscript counts.
- [x] Integrate the update cohort into the corpus with current-field additions, updated mappings, and preserved round-specific reliability.
- [x] Generate and validate `data/current_study_level_coding_matrix.csv` as the unified 68-record current matrix while retaining round-specific provenance.
- [x] Preserve that file as the pre-harmonization view and publish the author-confirmed controlled-schema matrix in `data/current_study_level_coding_matrix_harmonized.csv`.
- [x] Publish the field-level coding-round harmonization audit and round-specific statistics without constructing a synthetic combined kappa.
- [x] Update and compile the manuscript against the integrated 253 / 248 / 67+1 / 65 corpus counts.
- [x] `data/reference_audit.csv` has DOI coverage improved from Zotero/local audit and leaves unresolved DOI cases as `NA`.
- [x] `data/screening_summary.csv` summarizes the current source-specific ledger and final corpus layers.
- [x] `data/core31_second_coder_blind.csv` can be shared for independent 31-Core strongest-evidence-output coding.
- [x] `data/core31_second_coder_formal_blind_template.csv` exists as a blank template for future reruns.
- [x] `data/core31_second_coder_formal_results.csv` exists and contains the completed formal strongest-evidence-output second-coder pass.
- [x] `data/core31_second_coder_capability_traceability_blind_template.csv` exists as a blank extension template for cross-stage capability and external-traceability checks.
- [x] `data/core31_second_coder_capability_traceability_results.csv` exists and contains the completed extension second-coder results.
- [x] `data/intercoder_sample_blind.csv` can be shared for optional sampled review.
- [ ] Decide whether proposed/intermediate audit files should be included in public release or moved to a private working archive.
- [ ] Decide whether `zotero_export_20260530.bib` should remain private because it reflects the local Zotero library export.

## Documentation

- [x] `README.md` explains purpose, file list, reproduction command, and security boundary.
- [x] `codebook.md` defines A/E coding categories and evidence objects.
- [x] `data_dictionary.md` defines all core data fields.
- [x] `intercoder_instructions.md` explains independent second-coder workflow.
- [x] `SUBMISSION_UPDATE_SECOND_CODER_RERUN_NOTES.md` documents the tightened primary/overlay and external-traceability rules for the update-pass rerun.
- [ ] Add final repository URL and release date.
- [ ] Add license after author decision.
- [ ] Add citation metadata if archiving on Zenodo.

## Reproducibility

- [x] `reproduce_tables.py` runs without count or A/E distribution errors.
- [x] Remaining DOI gaps are documented rather than guessed.
- [x] Pilot second-coder round archived for codebook calibration.
- [x] Pilot agreement/kappa must not be cited as formal reliability.
- [x] Formal second-coder template is blank and hides original labels.
- [x] Formal strongest-evidence-output agreement report added after revised codebook freeze and new independent coding.
- [x] Formal agreement report lists disagreement rows.
- [x] Capability/traceability extension agreement report exists and uses multi-label/set-style metrics.
- [x] Adjudication result is not claimed unless completed.
- [ ] If disagreements are adjudicated, add `data/core31_second_coder_adjudicated.csv`; do not create it before adjudication.
- [ ] Record the final corpus date and search cutoff date in the manuscript and artifact README.

## Submission Notes

- [ ] In the manuscript, describe the artifact as a non-sensitive audit package.
- [ ] State that the manuscript uses the current source-specific search ledger and record-level screening audit for corpus construction.
- [ ] State that Zotero DOI merge improved metadata coverage but does not replace official landing-page verification for every record.
- [ ] State that no exploit payloads or undisclosed vulnerability reproduction materials are released.

- [x] Confirm `local_private_working/`, `.pdf`, and `.sqlite` files are not tracked.
- [x] Confirm `core_reproducibility_audit.csv` contains no private Zotero paths.
- [x] Confirm `unknown_not_audited` is not counted as absence of material.
- [x] Confirm `data/product_ecosystem_snapshot.csv` is an independent boundary layer and not counted in the 253 source records.
- [x] Confirm product-page changes do not automatically alter Core statistics.
- [x] Confirm product-ecosystem global snapshot date is consistent with `RELEASE_MANIFEST.md` and row-level access dates are retained.
- [x] Confirm `data/mapping_snapshot_counts.csv` is descriptive only and not a field-level prevalence estimate.
- [ ] For anonymous review, remove or replace personal GitHub/account URLs with an anonymized artifact link or package.


