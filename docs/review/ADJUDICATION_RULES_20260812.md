# Human Third-Party Adjudication Rules

This package contains one row for every disagreement between the two independent assignments in the current 199-study comparison. The form anonymizes the assignments as coder X and coder Y.

## Required human action

1. Open the cited public source for each row.
2. Verify or replace the evidence locator and write a brief evidence-based reason.
3. Enter one allowed single label or a semicolon-separated allowed multi-label set.
4. If the source cannot resolve the boundary, enter `unresolved` and set `unresolved=yes`; do not guess.

## Fixed rules

- **lifecycle coverage**: Mark only observable lifecycle actions or outputs. Reporting and audit requires explicit packaging, routing, disclosure, or audit transition; a report name alone is insufficient. Allowed values: `candidate analysis`, `path and input exploration`, `execution observation`, `reproduction and validation`, `patch validation`, `reporting and audit`.
- **cross-stage capability**: Require an explicit cross-stage connection. Information must guide later action; feedback must alter later action; packaging must assemble prior outputs; governance must enforce an actual gate. Allowed values: `context aggregation / rule extraction`, `tool routing / strategy routing`, `feedback interpretation / loop adjustment`, `validation organization / evidence packaging`, `long-horizon state management`, `failure reuse / strategy update`, `governance / human gates / disclosure control`.
- **primary system shape**: Choose the dominant locus and objective of agent control in the main evaluated contribution. Use the evaluation task and primary metrics to resolve ties; do not infer from agent count or system name. Allowed values: `candidate-analysis system`, `feedback-driven fuzzing agent`, `reproduction-, validation-, and repair-centered agent`, `long-horizon pentest and CRS agent`.
- **principal reported evidence output**: Select the observable result most directly supporting the main finding. Benchmark ground truth or aggregate CVE counts do not automatically establish externally traceable material. Allowed values: `candidate judgment`, `controlled task completion`, `runtime safety signal`, `reproducible validation`, `externally traceable material`.
- **external traceability**: Code separately from principal output. Only item-level alignment between a concrete system result and a specific public external record qualifies as publicly aligned external trace. Allowed values: `no external trace reported`, `author-reported external clue`, `benchmark ground truth / public material`, `publicly aligned external trace`.

The lead excerpt and lead locator are preparation aids only. They do not constitute a human adjudication. The final matrix must be generated only after the completed form passes validation.
