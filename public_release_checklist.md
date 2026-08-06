# Public Release Checklist

This checklist describes the current integrated artifact. It is a release gate, not a record of earlier coding rounds.

## Current Snapshot

- Search and integration cutoff: 2026-07-30.
- Source records: 1,785; version-reconciled studies: 1,772.
- Target-software studies: 199; extended-synthesis studies: 150.
- Background/reference studies: 670; excluded studies: 753.
- Synchronized submission tag: `csur-submission-2026-07-final-v8`.

## Public Contents

- [x] `README.md`, `ARTIFACT_INDEX.md`, `RELEASE_MANIFEST.md`, and `data_dictionary.md` describe the current snapshot.
- [x] `manuscript_artifact_paths.txt` lists the manuscript-facing data and reference files.
- [x] `reproduce_tables.py` validates the integrated corpus, distributions, provenance, and second-coder files.
- [x] `SECURITY_BOUNDARY.md` defines excluded material.
- [x] Data and code licenses are present.

## Security Gate

- [ ] Export only the release allowlist; do not archive the whole working directory.
- [ ] Exclude `local_private_working/`, full-text PDFs, `.git/`, caches, logs, PID files, and private paths.
- [ ] Inspect proposed, blind, unresolved, and temporary files before release.
- [ ] Confirm no credentials, private targets, exploit payloads, sensitive crash inputs, or vendor-private communications are present.

## Reproducibility Gate

- [x] All manifest paths exist and are unique.
- [x] The standalone reproduction command passes without a manuscript checkout.
- [x] The optional manuscript-facing validation passes against the synchronized manuscript.
- [ ] Re-run the standalone validator after the final export is staged.
- [ ] Confirm the final public repository URL, release date, and author-approved disclosure metadata.

## Release Rule

Publish a clean export assembled from the manifest and release documentation. Preserve historical build inputs separately; do not mix them with the current release snapshot or use them as current denominators.
