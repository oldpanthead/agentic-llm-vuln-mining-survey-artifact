# Coding-Round Harmonization Report

## Scope and status

The frozen initial-round files and the adjudicated submission-update files remain unchanged. The author reviewed and accepted the evidence-linked harmonization candidates on 2026-07-16. The harmonized matrix applies one controlled schema across both rounds while retaining coding-round provenance and field-specific reliability scope.

- Study-level coded records: 68 (67 target-software studies plus one governance boundary case).
- Author-confirmed substantive initial-round field changes: 38 across 24 records. One additional `change_required=yes` row is schema normalization only (`role discussion / textual reflection` removed from the formal controlled field and retained in `legacy_notes`).
- New literature added by this pass: none.
- New evidence-output category required: none.
- Synthetic combined kappa computed: no.
- Change-only independent human recoding after harmonization: no. Harmonized lifecycle, capability, and shape labels are author-confirmed descriptive recodings; frozen author labels and independent-coder labels remain preserved.

## Fields changed

- `cross_stage_capabilities`: 23 author-confirmed substantive changes, plus one schema-normalization row.
- `lifecycle_coverage`: 15 author-confirmed changes.

Schema-only changes separated `primary_system_shape` from `overlay_tags`, renamed the validation-centered shape to include repair systems, and removed `role discussion / textual reflection` from the formal capability vocabulary while preserving it in `legacy_notes`.

## Round-aware distributions

The round differences narrow after the initial cohort is recoded at the July 15 granularity, especially for context aggregation, tool routing, feedback interpretation, and candidate analysis. Differences remain and should be read as cohort-specific descriptive variation rather than temporal evolution.

### Primary system shapes

| Shape | Initial | Update | Combined |
|---|---:|---:|---:|
| candidate-analysis system | 4 | 12 | 16 |
| feedback-driven fuzzing agent | 9 | 8 | 17 |
| long-horizon pentest and CRS agent | 9 | 5 | 14 |
| reproduction-, validation-, and repair-centered agent | 8 | 12 | 20 |

### Principal reported evidence outputs

| Evidence output | Initial | Update | Combined |
|---|---:|---:|---:|
| candidate judgment | 3 | 3 | 6 |
| controlled task completion | 5 | 8 | 13 |
| externally traceable material | 0 | 4 | 4 |
| reproducible validation | 14 | 17 | 31 |
| runtime safety signal | 8 | 5 | 13 |

## Interpretation

All four target-software system-shape patterns remain populated. Repair-oriented additions stretch the existing reproduction-, validation-, and repair-centered shape rather than requiring a fifth category. Externally traceable material appears only in the update cohort under the current strongest-output coding, but no new evidence-output category is needed. The central workflow--capability--evidence conclusions are unchanged: broader Agentic action scope requires corresponding workflow and validation traces before stronger vulnerability claims can be supported.

## Preservation and disclosure

- Original author labels, independent-coder labels, and pre-adjudication reports remain preserved.
- Every changed initial-round label is traceable through `data/coding_round_harmonization_audit.csv` to an existing frozen coding note or public-material audit location.
- AI-assisted tools organized the comparison and drafted evidence-linked working notes. The author reviewed the underlying recorded evidence and accepted the final changes; AI output is not an independent human coding decision.

