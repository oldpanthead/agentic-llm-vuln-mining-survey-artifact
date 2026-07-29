# Submission-Update Second-Coder Rerun Notes

This lightweight note is for a possible rerun of the 41-record submission-update second-coder pass after tightening the boundary rules. It does not replace the existing completed results, does not change any reported agreement value, and does not create post-adjudication agreement statistics.

## What To Code

Use `data/submission_update_20260715_second_coder_rerun_blind_template.csv`. The coder should decide the analytical layer and code lifecycle coverage, primary system shape, cross-stage capability labels, principal reported evidence output, external traceability, and claim boundary from public materials only. Do not inspect author audit files, adjudication files, previous coder2 results, or author-confirmed resolutions before completing the independent pass.

## Boundary Rules

- Analytical layer: include a record in the study-level layer only when the LLM visibly changes tool use, input or harness generation, feedback interpretation, validation organization, state handling, or reporting boundary. LLM label/explanation only remains contextual rather than study-level.
- Primary system shape: choose the dominant evaluated role. Treat secondary roles as overlays or uncertainty notes rather than as a second primary label.
- Lifecycle coverage: mark a stage only when the public material shows an action or evidence output for that stage. Do not infer stages from system ambition alone.
- Cross-stage capability: code observed capabilities, not the agent name, number of agents, or workflow length. Long-horizon state preservation is one capability, not the definition of the whole category.
- Principal reported evidence output: code the result or aligned evidence state that most directly supports the study's main evaluated finding. Aggregate author-reported external outcomes do not by themselves establish item-level externally traceable material.
- External traceability: require item-level public alignment between a specific system result and a public issue, advisory, CVE, PR, commit, benchmark ground truth, maintainer record, or bounty record. If the public material reports only aggregate outcomes, record uncertainty rather than treating it as externally traceable material.
- Claim boundary: state the strongest vulnerability claim supported by the coded evidence and note any missing trace link.

## Metrics After A Real Rerun

After a real rerun is completed, report field-specific pre-adjudication agreement only. Use raw agreement and Cohen's kappa for single-label fields when appropriate. For multi-label lifecycle and capability fields, report row-level exact agreement, mean row Jaccard, and micro F1 rather than forcing a single-label kappa. Do not tune labels to improve agreement. AI-assisted working notes may organize disagreements, but they are not an independent coder decision.
