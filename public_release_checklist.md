# Public Release Checklist

This checklist describes the current integrated artifact. It is a release gate, not a record of earlier coding rounds.

## Current Snapshot

- Search and integration cutoff: 2026-07-30.
- Release date: 2026-08-17.
- Source records: 1,785; version-reconciled studies: 1,772.
- Target-software studies: 199; extended-synthesis studies: 154.
- Background/reference studies: 668; excluded studies: 751.
- Synchronized submission tag: `csur-submission-2026-08-final-v10`.

## Public Contents

- [x] `README.md`, `ARTIFACT_INDEX.md`, `RELEASE_MANIFEST.md`, and `data_dictionary.md` describe the current snapshot.
- [x] `manuscript_artifact_paths.txt` lists the manuscript-facing data and reference files.
- [x] `reproduce_tables.py` validates the integrated corpus, adjudicated distributions, provenance, and pre-adjudication second-coder files.
- [x] The 410-row third-review decision export, 995-row decision log, completion manifest, and final matrix are present and validated.
- [x] `SECURITY_BOUNDARY.md` defines excluded material.
- [x] Data and code licenses are present.

## Security Gate

- [x] Export only the release allowlist; do not archive the whole working directory.
- [x] Exclude `local_private_working/`, full-text PDFs, `.git/`, caches, logs, PID files, and private paths.
- [x] Inspect proposed, blind, unresolved, and temporary files before release.
- [x] Confirm no credentials, private targets, exploit payloads, sensitive crash inputs, or vendor-private communications are present.

## Reproducibility Gate

- [x] All manifest paths exist and are unique.
- [x] The standalone reproduction command passes without a manuscript checkout.
- [x] The optional manuscript-facing validation passes against the synchronized manuscript.
- [x] Re-run the standalone validator after the final export is staged.
- [x] Confirm the final public repository URL, release date, and author-approved disclosure metadata.

## Release Rule

Publish a clean export assembled from the manifest and release documentation. Preserve historical build inputs separately; do not mix them with the current release snapshot or use them as current denominators.
