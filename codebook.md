# Codebook

This codebook documents the minimal public coding scheme for the Agentic LLM vulnerability mining survey. It is intended to support auditability of the manuscript-level observations, not to publish exploit payloads or sensitive vulnerability details.

## A-profile: Agentic capability profiles

- **A0 Prompt-level judgment**: the LLM mainly produces labels, explanations, rankings, or hypotheses from text.
- **A1 Role discussion**: multiple personas, debate, reflection, or validator roles organize text-level reasoning, but without independent external signals.
- **A2 Tool-augmented analysis**: the LLM uses retrieval, specifications, static analysis, domain knowledge, or other non-executing sources to expand context and narrow candidates.
- **A3 Execution-feedback loop**: execution feedback enters the next input, strategy, or validation step, forming a run--observe--revise loop.
- **A4 Multi-agent orchestration**: planning, execution, validation, reporting, or other responsibilities are distributed across traceable agents or modules.
- **A5 Workflow self-optimization**: failures, coverage gaps, logs, or prior attempts produce reusable strategy updates beyond one-off retry or prompt rewriting.

A0--A3 describe the main interaction path. A4 and A5 are overlay capability tags that can coexist with lower levels. The plus sign is used for coexistence, not for a strict ordinal interval.

## E-level: evidence strength levels

- **E0 Model judgment**: labels, probabilities, textual explanations, F1/accuracy, or candidate hypotheses.
- **E1 Controlled task completion**: benchmark success, CTF flag, cyber range objective, task score, or trajectory.
- **E2 Runtime signal**: crash, coverage, assertion, sanitizer, oracle, or other execution-time signal. Coverage alone mainly indicates exploration progress.
- **E3 Reproducible validation material**: PoC/PoV, replay, validation script, or failing-before / passing-after patch validation.
- **E4a Author-reported external clue**: CVE/CNVD, bug bounty, vendor clue, or maintainer-related clue as reported by the original study.
- **E4b Public/background evidence**: public material or benchmark ground truth provides a real-vulnerability background, but not necessarily a system-new discovery.
- **E4c Audit-ready external confirmation profile**: external confirmation, accessible artifact, explicit version, and environment are all reported.

## Evidence object values

- **Model judgment**: labels, scores, probabilities, or textual vulnerability reasoning.
- **Task completion**: CTF, benchmark, cyber range, or task objective completion.
- **System output**: tool execution output, PoC/PoV, validation scripts, reports, traces, or patches.
- **Task background**: real-vulnerability background built into a benchmark, range, or task setting.
- **External clue**: author-reported CVE, bug bounty, vendor, maintainer, or disclosure-related clue.
- **Governance risk**: security risks introduced by agent tool use, permissions, sandboxing, or deployment configuration.

## External-evidence profiles

E4a, E4b, and E4c are external-evidence profiles. They distinguish source, public verifiability, and audit readiness. They should not be read as a strictly linear scale of vulnerability discovery capability.

## External Rereview Rule

For the final 199-study descriptive matrix, OY externally rereviewed 410 study--field disagreements using the prespecified controlled definitions and supplied source materials. OY had not seen the manuscript, first-round materials, or old adjudication results before the initial rereview; later material-identity corrections and targeted feedback were disclosed, so the process is not described as fully blinded adjudication. Operational definitions take precedence over author terminology. Benchmark ground truth is not external confirmation; author-reported CVE/CNVD, vendor, maintainer, or bounty material is an external clue; and only a concrete system result aligned with a concrete public external record is a publicly aligned external trace. Retain only labels explicitly supported by the material; do not infer from a system name, promotion, or expected capability. LLM-assisted preparation and deterministic scripts organized materials, checked task--study--field--PDF mappings, hashes, and tables, and regenerated counts; they did not replace OY's manual judgments. See `ADJUDICATION_COMPLETION_20260812.md` and `adjudication/ADJUDICATION_RULES_20260812.md`.

## Boundary examples

- **Cybench: A4 / E1**. The system or benchmark setting may involve long-horizon agentic behavior, but the result evidence is mainly controlled task completion.
- **RFCAUDIT: A2 / E4a**. The system action depth is tool/specification-augmented rather than a full execution-feedback loop, while the original report may include external confirmation clues.
- **BountyBench: A4 / E4b**. The benchmark involves realistic bug-bounty-style tasks and agentic workflows, but the real-vulnerability grounding is benchmark/task background rather than direct external confirmation of every system output.

## Reproducibility Audit Status Values

The reproducibility audit uses `reported_yes`, `reported_partial`, `not_found_after_review`, `unknown_not_audited`, `restricted_or_sensitive`, and `not_applicable`. `unknown_not_audited` is not a negative result. Reported material requires a public source note.
