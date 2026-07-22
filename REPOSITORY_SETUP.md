# Repository Status Notes

This file records repository setup decisions for the current public audit artifact.

## Suggested Repository

Suggested repository name:

`agentic-llm-vuln-mining-survey-artifact`

Suggested short description:

`Non-sensitive audit artifact for a survey of Agentic LLM systems for vulnerability mining.`

## Repository Decisions

- [x] Choose final license: CC BY 4.0 for data/docs and MIT for code.
- [x] Replace `REPLACE_WITH_PUBLIC_REPOSITORY_URL` in `CITATION.cff`.
- [ ] Confirm any remaining manuscript repository references before formal submission.
- [ ] Decide whether author names should remain anonymous before review.
- [x] Decide whether the repository should be private until acceptance or public at submission: public repository for the current audit artifact.
- [x] Decide whether to archive the release on Zenodo: no Zenodo for now.

## Initial Repository Contents

Commit the contents of this artifact repository, not the whole manuscript working directory.

Do not commit:

- local Zotero export;
- internal phase reports;
- manuscript snapshots or logs;
- proposed/intermediate audit tables;
- `intercoder_sample_key.csv`;
- private notes or backup files.

## Suggested First Commit Message

`Add minimal audit artifact`

## Suggested Release Tag

`v0.1.0`

Use a `v1.0.0` release only after manuscript metadata, optional Zenodo archive, and any completed second-coder material are finalized.

## Current Local Git State

This artifact has already been initialized as a local Git repository on branch `main`.

The first local commit has been created with anonymous review-safe metadata:

- author name: `Jingran Fang`
- author email: `anonymous@example.com`
- commit message: `Add minimal audit artifact`

## Current Remote

The public GitHub remote is:

```bash
origin https://github.com/oldpanthead/agentic-llm-vuln-mining-survey-artifact.git
```
