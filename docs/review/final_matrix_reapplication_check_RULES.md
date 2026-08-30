# Final Applied Rules

This file is the applied rule override for the final recode. Source material is restricted to `DELIVERY_TO_OY_EMPIRICAL_RULES_20260830` and its 60 manifest-listed materials.

## External traceability

Use exactly one of:

- `no external trace reported`: no public external record, or only a generic discovery claim;
- `author-reported external clue`: the authors mention CVE, issue, bug report, PR, vendor, maintainer, bounty, or disclosure, but do not align each system result to a specific record;
- `item-aligned external record`: a specific system result is aligned to a specific public issue, repository, CVE, PR, commit, GHSA, maintainer record, or public reproduction artifact.

Use of a benchmark, CVE corpus, or public dataset is recorded separately in `benchmark_public_material_descriptor_FINAL.csv` and never upgrades external traceability.

## Lifecycle coverage

Assign a stage only when the material shows a concrete workflow action, object, and result or subsequent use. The stages are `candidate analysis`, `path and input exploration`, `execution observation`, `reproduction and validation`, `patch validation`, and `reporting and audit`. Use `no qualifying label observed` when the material is sufficient but no stage is evidenced; use `not observable in supplied material` when it is insufficient; `unresolved` and `material mismatch` are whole-cell states.

## Cross-stage capability

Every positive label requires the observable relation `earlier information/result/state -> changed later action/state/gate`. The labels are `context aggregation / rule extraction`, `tool routing / strategy routing`, `feedback interpretation / loop adjustment`, `validation organization / evidence packaging`, `long-horizon state management`, `failure reuse / strategy update`, and `governance / human gates / disclosure control`. Component lists, architecture diagrams, generic memory, generic iteration, reflection claims, or unchanged retries do not qualify.

## Other fields and uncertainty

Choose primary system shape and principal reported evidence output from the main evaluated task and metrics; secondary outputs do not upgrade the principal category. Confidence is evidence-calibrated: `high` is direct and unambiguous, `medium` has a reasonable boundary alternative, `low` is incomplete or locator-uncertain, and `unresolved` cannot be responsibly judged.

