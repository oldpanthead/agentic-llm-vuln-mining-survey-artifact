# Unified Codebook

This codebook documents the public coding scheme for the Agentic LLM vulnerability-mining survey. It supports audit of manuscript-level observations, not publication of exploit payloads or sensitive vulnerability details. The current analytical set is the 199-study target-software set.

## General Decision Rule

Code observable system behavior and reported material. Do not infer a capability, lifecycle stage, evidence output, or external trace from a system name, stated ambition, number of agents, or workflow diagram alone. Operational definitions take precedence over author terminology. Record uncertainty when public material cannot resolve a boundary.

## Historical A-profile: Agentic Capability Profiles

- A0 Prompt-level judgment: the LLM mainly produces labels, explanations, rankings, or hypotheses from text.
- A1 Role discussion: multiple personas, debate, reflection, or validator roles organize text-level reasoning, but without independent external signals.
- A2 Tool-augmented analysis: the LLM uses retrieval, specifications, static analysis, domain knowledge, or other non-executing sources to expand context and narrow candidates.
- A3 Execution-feedback loop: execution feedback enters the next input, strategy, or validation step, forming a run--observe--revise loop.
- A4 Multi-agent orchestration: planning, execution, validation, reporting, or other responsibilities are distributed across traceable agents or modules.
- A5 Workflow self-optimization: failures, coverage gaps, logs, or prior attempts produce reusable strategy updates beyond one-off retry or prompt rewriting.

A0--A3 describe the main interaction path. A4 and A5 are overlay capability tags that can coexist with lower levels. The plus sign denotes coexistence, not a strict ordinal interval.

## Historical E-level: Evidence Strength Profiles

- E0 Model judgment: labels, probabilities, textual explanations, F1/accuracy, or candidate hypotheses.
- E1 Controlled task completion: benchmark success, CTF flag, cyber range objective, task score, or trajectory.
- E2 Runtime signal: crash, coverage, assertion, sanitizer, oracle, or other execution-time signal. Coverage alone mainly indicates exploration progress.
- E3 Reproducible validation material: PoC/PoV, replay, validation script, or failing-before / passing-after patch validation.
- E4a Author-reported external clue: CVE/CNVD, bug bounty, vendor clue, or maintainer-related clue as reported by the original study.
- E4b Public/background evidence: public material or benchmark ground truth provides a real-vulnerability background, but not necessarily a system-new discovery.
- E4c Audit-ready external confirmation profile: external confirmation, accessible artifact, explicit version, and environment are all reported.

E4a, E4b, and E4c distinguish source, public verifiability, and audit readiness. They are not a strictly linear scale of vulnerability discovery capability.

Legacy crosswalk: E0 usually overlaps with candidate judgment; E1 with controlled task completion; E2 with runtime safety signal; E3 with reproducible validation; and E4a, E4b, and E4c with the external-traceability profiles below.

## Evidence Object Values

- Model judgment: labels, scores, probabilities, or textual vulnerability reasoning.
- Task completion: CTF, benchmark, cyber range, or task objective completion.
- System output: tool execution output, PoC/PoV, validation scripts, reports, traces, or patches.
- Task background: real-vulnerability background built into a benchmark, range, or task setting.
- External clue: author-reported CVE, bug bounty, vendor, maintainer, or disclosure-related clue.
- Governance risk: security risks introduced by agent tool use, permissions, sandboxing, or deployment configuration.

External-evidence profiles distinguish source, public verifiability, and audit readiness. They should not be read as a strictly linear scale of vulnerability discovery capability.

## Lifecycle Coverage (multi-label)

Use semicolon-separated labels in the order below. Mark a stage only when the paper or public artifact shows an action or output at that stage. A stated end-to-end goal is not sufficient.

- candidate analysis: the system produces, ranks, filters, localizes, or refines a vulnerability hypothesis.
- path and input exploration: the system generates or selects inputs, seeds, harnesses, targets, paths, or exploration strategies.
- execution observation: the system executes a target or analysis environment and observes coverage, crashes, sanitizers, assertions, logs, or another runtime oracle.
- reproduction and validation: the system organizes or executes replay, PoC/PoV, exploitability checking, or another repeatable validation procedure.
- patch validation: the system checks a repair against a recorded trigger, test, security property, or regression condition.
- reporting and audit: the system packages findings, evidence, disclosure records, or audit-oriented reports.

## Cross-Stage Capability (multi-label)

A cross-stage capability connects hypotheses, tool actions, execution feedback, validation material, state transitions, or reporting decisions across more than one part of the workflow. Multi-agent naming alone establishes no label.

- context aggregation / rule extraction: combines code, specifications, retrieval results, warnings, history, or domain rules to guide later action.
- tool routing / strategy routing: selects tools, targets, strategies, or next actions based on current state.
- feedback interpretation / loop adjustment: interprets execution or tool feedback and changes a later action.
- validation organization / evidence packaging: assembles replay, PoC/PoV, patch checks, evidence packages, or reports from prior outputs.
- long-horizon state management: preserves task state across multiple steps, roles, or stages.
- failure reuse / strategy update: turns failed attempts, coverage gaps, or prior outcomes into reusable later strategy rather than a one-off retry.
- governance / human gates / disclosure control: enforces permissions, sandboxing, approval, target scope, or disclosure boundaries.

## Primary System Shape (single-label)

Choose the dominant location and objective of agent control in the study's main evaluated contribution. This field describes how the workflow is organized, not which result category is ultimately reported. Secondary roles belong in the uncertainty note.

- candidate-analysis system
- feedback-driven fuzzing agent
- reproduction-, validation-, and repair-centered agent
- long-horizon pentest and CRS agent

Long-horizon orchestration can overlay another role. Assign it as primary only when coordination across tasks or stages is the central evaluated contribution. The governance boundary case is historical C27 provenance only and is not a current target-software value.

## Principal Reported Evidence Output (single-label)

Code the observable result that most directly supports the study's main evaluated finding. The historical CSV field name strongest_evidence_output is retained for compatibility. These categories are not a universal linear quality ladder.

- candidate judgment: label, score, ranking, explanation, warning, hypothesis, or candidate report without stronger execution evidence.
- controlled task completion: benchmark, CTF, cyber-range, CRS, or bounded task success without a stronger vulnerability-specific output.
- runtime safety signal: crash, sanitizer, assertion, oracle, coverage-linked bug signal, or other execution-time safety observation without a sufficiently specified replay package.
- reproducible validation: replay, PoC/PoV, validation script, or failing-before / passing-after patch check aligned with the target version and environment.
- externally traceable material: a specific system result is publicly aligned with an issue, advisory, CVE, PR/commit, maintainer record, bounty record, or equivalent external-process record.

Tool count, number of agents, workflow length, benchmark name, or author wording does not determine the category. Benchmark ground truth or an aggregate author-reported CVE count does not automatically become externally traceable material. If PoC, PoV, replay, patch validation, or verified benchmark artifacts are present but external confirmation is aggregate or not item-aligned, retain reproducible validation and record the external clue separately.

Prospective reporting package is a recommended reporting outcome, not one of the five current evidence-output categories. It connects a concrete system output, target version, runtime environment, reproduction material, external process, and vulnerability claim into an auditable package.

Historical governance boundary value: earlier files used a governance-boundary value for C27. The current analytical allocation retains that study in extended synthesis as governance and agent-safety context, so it does not receive a target-software evidence-output label or enter target-software distributions. Historical files commonly recorded this value as N/A or another boundary-specific E-level value.

## External Traceability (single-label)

Code this field separately from principal output.

- no external trace reported: no relevant public external record is reported.
- author-reported external clue: the paper reports a CVE, vendor, maintainer, bounty, or disclosure outcome without public item-level alignment to the specific system output.
- benchmark ground truth / public material: a benchmark or public vulnerability record supplies task background, but does not establish that the system independently produced the externally recorded result.
- publicly aligned external trace: the reviewed public material links a specific system result to a specific external-process record.

Only a concrete system result aligned with a concrete public external record qualifies as a publicly aligned external trace. Benchmark ground truth is not external confirmation. Historical not reported values apply only to C27 provenance.

## Claim Boundary (short text)

Write one or two sentences stating the strongest vulnerability claim supported by the reviewed output. Identify the concrete result and conditions. If a stronger claim would require an unobserved trace link, state that boundary specifically.

Preferred pattern:

The material supports [candidate, runtime, task, reproducible, or external result] under [target and evaluation conditions]. A stronger claim would require [specific missing material or alignment].

Avoid generic statements such as “more evidence is needed.”

## Review Status Values

For every reviewed field, use confirm, revise, or newly_code. Set row_status to complete only after all six fields, the material locator, and the decision note have been reviewed. Use unresolved with unresolved=yes when the source cannot resolve the boundary; do not guess.

The reproducibility audit uses reported_yes, reported_partial, not_found_after_review, unknown_not_audited, restricted_or_sensitive, and not_applicable. unknown_not_audited is not a negative result. Reported material requires a public source note.

## External Rereview Rule

Two coders independently assigned lifecycle coverage, cross-stage capability, primary system shape, principal reported evidence output, and external traceability. OY externally rereviewed 410 study--field disagreements using this codebook and supplied source evidence. Fifty hidden-reference QC tasks were reviewed in the same package but remain separate from final decisions and reliability statistics.

Before the initial independent rereview OY had not seen the manuscript, first-round materials, or old adjudication results. Later material-identity corrections and targeted feedback were disclosed, so the process is reported as external third-party rereview, not fully blinded adjudication.

LLM-assisted preparation and deterministic scripts were limited to material assembly, task--study--field--PDF cross-checking, SHA-256 calculation, table validation, and count regeneration. They did not replace OY's manual judgments. The integration validator checks task identities, field labels, evidence locators, hashes, and material paths.

Operational definitions control; benchmark ground truth is not external confirmation; author-reported CVE, CNVD, vendor, maintainer, or bounty material is an external clue unless a concrete system result aligns with a concrete public external record; multi-label fields retain only explicitly shown labels; and evidence-insufficient cases are unresolved rather than guessed. Detailed procedure and reporting boundary are in ADJUDICATION_COMPLETION_20260812.md and adjudication/ADJUDICATION_RULES_20260812.md.

## Boundary Examples

- Cybench: the setting may involve long-horizon agentic behavior, but the main result evidence is controlled task completion.
- RFCAUDIT: tool/specification-augmented analysis is not necessarily a full execution-feedback loop, while the original report may include an author-reported external clue.
- BountyBench: realistic bug-bounty-style tasks and public vulnerability material provide task background, not direct external confirmation of every system output.

## Security Boundary

Use only public, non-sensitive material. Do not copy exploit payloads, undisclosed PoCs, sensitive crash inputs, private targets, or vendor/private communications into the review sheet.
