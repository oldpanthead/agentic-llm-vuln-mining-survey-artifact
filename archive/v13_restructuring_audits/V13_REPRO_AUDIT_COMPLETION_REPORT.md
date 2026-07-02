# V13 Reproducibility Audit Completion Report

Scope: 30 vulnerability-mining Core studies. C27 AgentFuzz is treated as a governance-oriented boundary case and is excluded from the main reproducibility-material audit.

- Rows in data/core_reproducibility_audit.csv: 30
- Rows with no unknown_not_audited status across audit fields: 30
- Rows with at least one unknown_not_audited status: 0
- Rows with at least one restricted_or_sensitive status: 0

## Status Policy

- unknown_not_audited is not counted as absence of material; in this completion snapshot it is expected to be zero.
- not_found_after_review means the relevant material was not found in the reviewed public/PDF sources.
- restricted_or_sensitive is separated from missing material because sensitive disclosure constraints may prevent public release.
- Repository presence, reproducibility materials, and external confirmation are recorded separately.

## Unknown Rows

- None.

## Restricted Or Sensitive Rows

- None recorded in the current public audit snapshot.

## Summary Table

| audit_dimension | reported_yes | reported_partial | not_found_after_review | unknown_not_audited | restricted_or_sensitive | not_applicable |
|---|---:|---:|---:|---:|---:|---:|
| public_artifact_status | 0 | 23 | 7 | 0 | 0 | 0 |
| target_version_status | 0 | 17 | 13 | 0 | 0 | 0 |
| environment_status | 0 | 27 | 3 | 0 | 0 | 0 |
| replay_material_status | 0 | 24 | 6 | 0 | 0 | 0 |
| structured_trace_status | 0 | 18 | 12 | 0 | 0 | 0 |
| author_reported_external_trace_status | 0 | 21 | 9 | 0 | 0 | 0 |
| publicly_traceable_external_material_status | 0 | 22 | 8 | 0 | 0 | 0 |
| claim_level_alignment_status | 0 | 16 | 14 | 0 | 0 | 0 |
