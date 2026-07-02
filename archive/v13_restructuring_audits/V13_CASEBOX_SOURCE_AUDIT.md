# V13 Casebox Source Audit

## Case 1: PBFuzz
- Core ID: C13
- BibTeX key: zeng2025pbfuzz
- Review status: Zotero indexed full text reviewed; manuscript wording is kept conservative.
- Keep in manuscript: given benchmark conditions, execution feedback can enter directed fuzzing and PoV-generation workflow, supporting known-vulnerability triggering or validation-material organization.
- Remove or avoid: matrix-only wording, unsupported true unknown-vulnerability discovery, or external confirmation.
- Boundary: coverage, crash, or author-reported signals are not treated as external confirmation.

## Case 2: OSS-CRS
- Core ID: C30
- BibTeX key: chin2026osscrs
- Review status: V4 PDF marker present in the current artifact matrix; high-risk external-confirmation claims remain source-limited.
- Real OSS / AIxCC-style: keep as workflow/background wording when tied to the source material.
- PoV / triggering input / validation result: keep only as system-output or validation-material wording unless per-vulnerability public chains are available.
- Report / trajectory / patch: keep as workflow or artifact fields only when explicitly reported by source material.
- Public artifact / target version / environment: record in reproducibility audit fields; repository presence alone is not treated as reproducibility sufficiency.
- External confirmation: do not convert unknown-bug or maintainer/CVE-like claims into independently confirmed conclusions without public per-claim links, versions, environments, and artifacts.
