# Unified Second-Coder Codebook

## Purpose

This codebook supports one unified second-coder review of the complete study-level set: 67 target-software studies plus one governance boundary case. The same definitions apply to records from both corpus-acquisition stages. Earlier second-coder decisions may be confirmed or revised, but every final decision must be checked against the public paper or project material under this codebook.

The review covers six descriptive fields. The governance boundary case is coded where applicable but is not part of target-software lifecycle, capability, or system-shape denominators.

## General Decision Rule

Code observable system behavior and reported material. Do not infer a capability, lifecycle stage, evidence output, or external trace from the system name, stated ambition, number of agents, or workflow diagram alone. Record uncertainty when public material does not resolve a boundary.

## 1. Lifecycle Coverage (multi-label)

Use semicolon-separated labels in the order shown below.

- `candidate analysis`: the system produces, ranks, filters, localizes, or refines a vulnerability hypothesis.
- `path and input exploration`: the system generates or selects inputs, seeds, harnesses, targets, paths, or exploration strategies.
- `execution observation`: the system executes a target or analysis environment and observes coverage, crashes, sanitizers, assertions, logs, or another runtime oracle.
- `reproduction and validation`: the system organizes or executes replay, PoC/PoV, exploitability checking, or another repeatable validation procedure.
- `patch validation`: the system checks a repair against the recorded trigger, tests, security properties, or regression conditions.
- `reporting and audit`: the system packages findings, evidence, disclosure records, or audit-oriented reports.

Mark a stage only when the paper or public artifact shows an action or output at that stage. A stated end-to-end goal is not sufficient.

## 2. Cross-Stage Capability (multi-label)

A cross-stage capability connects hypotheses, tool actions, execution feedback, validation material, state transitions, or reporting decisions across more than one part of the workflow.

- `context aggregation / rule extraction`: combines code, specifications, retrieval results, warnings, history, or domain rules to guide later action.
- `tool routing / strategy routing`: selects tools, targets, strategies, or next actions based on current state.
- `feedback interpretation / loop adjustment`: interprets execution or tool feedback and changes a later action.
- `validation organization / evidence packaging`: assembles replay, PoC/PoV, patch checks, evidence packages, or reports from prior outputs.
- `long-horizon state management`: preserves task state across multiple steps, roles, or stages.
- `failure reuse / strategy update`: turns failed attempts, coverage gaps, or prior outcomes into reusable later strategy rather than a one-off retry.
- `governance / human gates / disclosure control`: enforces permissions, sandboxing, approval, target scope, or disclosure boundaries.

Long-horizon state preservation is one capability, not the definition of the entire category. Multi-agent naming alone does not establish any label.

## 3. Primary System Shape (single-label)

Choose the dominant evaluated role around which the study's main contribution and reported output are organized. Secondary roles belong in the uncertainty note rather than as a second primary label.

- `candidate-analysis system`
- `feedback-driven fuzzing agent`
- `reproduction-, validation-, and repair-centered agent`
- `long-horizon pentest and CRS agent`
- `governance boundary case` (C27 only)

Long-horizon orchestration can overlay the other roles. Assign it as primary only when coordination across tasks or stages is the central evaluated contribution.

## 4. Strongest Evidence Output (single-label)

Code the strongest system-produced output demonstrated in the reviewed material.

- `candidate judgment`: label, score, ranking, explanation, warning, hypothesis, or candidate report without stronger execution evidence.
- `controlled task completion`: benchmark, CTF, cyber-range, or bounded task success without a stronger vulnerability-specific output.
- `runtime safety signal`: crash, sanitizer, assertion, oracle, coverage-linked bug signal, or other execution-time safety observation without a sufficiently specified replay package.
- `reproducible validation`: replay, PoC/PoV, validation script, or failing-before/passing-after patch check aligned with the target version and environment.
- `externally traceable material`: a specific system result is publicly aligned with an issue, advisory, CVE, PR/commit, maintainer record, bounty record, or equivalent external-process record.
- `governance boundary case` (C27 only)

The categories describe reported outputs; they are not a universal linear quality ladder. Benchmark ground truth or an aggregate author-reported CVE count does not automatically become externally traceable material.

## 5. External Traceability (single-label)

- `no external trace reported`: no relevant public external record is reported.
- `author-reported external clue`: the paper reports a CVE, vendor, maintainer, bounty, or disclosure outcome without public item-level alignment to the specific system output.
- `benchmark ground truth / public material`: a benchmark or public vulnerability record supplies task background, but does not establish that the system independently produced the externally recorded result.
- `publicly aligned external trace`: the reviewed public material links a specific system result to a specific external-process record.
- `not reported` (governance boundary case only when the field is not applicable).

External traceability is coded separately from strongest evidence output. An external clue can coexist with reproducible validation without changing the strongest-output label.

## 6. Claim Boundary (short text)

Write one or two sentences stating the strongest vulnerability claim supported by the reviewed output. Identify the concrete result and conditions. If a stronger claim would require an unobserved trace link, state that boundary briefly and specifically.

Preferred pattern:

> The material supports [candidate/runtime/task/reproducible/external result] under [target and evaluation conditions]. [A stronger claim] would require [specific missing material or alignment].

Avoid generic statements such as "more evidence is needed."

## Review Status Values

For every field, use one of:

- `confirm`: the previous second-coder decision remains valid under this codebook.
- `revise`: the previous second-coder decision is changed after reviewing the material.
- `newly_code`: no reusable previous decision existed and a new decision was made.

Set `row_status` to `complete` only after all six fields, the material locator, and the decision note have been reviewed.

## Security Boundary

Use only public, non-sensitive material. Do not copy exploit payloads, undisclosed PoCs, sensitive crash inputs, private targets, or vendor/private communications into the review sheet.
