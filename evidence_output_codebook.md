# Evidence Output Codebook

This codebook defines the current manuscript's principal reported evidence-output labels for the study-level coded set. The same labels are used for the frozen initial round (30 target-software studies plus one governance boundary case) and the 37 target-software additions from the submission update. The historical CSV field name `strongest_evidence_output` is retained for compatibility. Legacy A/E fields remain in the artifact for historical traceability, but they are not the current manuscript's main prose axis.

## Current Evidence-Output Labels

### candidate judgment / 候选判断

The system produces a model judgment, ranked alert, suspected vulnerability, explanation, or triage result. This supports candidate screening but does not by itself establish runtime triggering or reproducible validation.

Legacy crosswalk: usually overlaps with old `E0`.

### controlled task completion / 受控任务完成

The system completes a benchmark, CTF, cyber range, CRS, or other bounded task under a predefined success condition. This supports task-completion claims within the benchmark boundary.

Legacy crosswalk: usually overlaps with old `E1`.

### runtime safety signal / 运行时安全信号

The system reports execution evidence such as crash, sanitizer, assertion, oracle, log, or security-conditioned coverage. This supports runtime-signal claims when the signal is tied to a security condition.

Legacy crosswalk: usually overlaps with old `E2`.

### reproducible validation / 可复现验证

The system provides replay, PoC, PoV, validation script, patch validation, target-version note, or environment material sufficient to inspect repeated triggering or repair behavior. This supports reproducible-validation claims within the reported scope.

Legacy crosswalk: usually overlaps with old `E3`.

### externally traceable material / 外部可追踪材料

The public material links a system result to an external process or record, such as project issue, security advisory, CVE, bug bounty note, maintainer confirmation, PR/commit, CI result, or disclosure status. This label records traceability; it does not automatically raise the system-output level unless the external material aligns with concrete output, target version, and reproducible material.

Legacy crosswalk: related to old `E4a`, `E4b`, and `E4c` profiles.

### claim-level audit material / 声明级审计材料

The material connects the specific system output, target version, runtime environment, reproduction material, external process, and vulnerability claim into an auditable chain. This is a claim-level audit label, not a separate exploit technique.

Legacy crosswalk: extends the old E4 profile idea with explicit claim alignment.

### governance boundary case / 治理边界案例

The Core item is included because it constrains governance, misuse, disclosure, or safety boundaries rather than because it contributes a target-software vulnerability evidence output. It should be kept separate from the main vulnerability-evidence progression.

Legacy crosswalk: commonly recorded as `N/A` or boundary-specific in old E-level fields.

## Coding Rule

Code `strongest_evidence_output` as the highest evidence strength supported by the system's own public output. Tool count, number of agents, workflow length, benchmark name, or author wording does not automatically increase the evidence-output label. When public material is incomplete, keep the decision at the weaker supported label and explain the uncertainty.

External materials such as CVE, CNVD, maintainer confirmation, bug bounty, vendor confirmation, or fix records do not automatically move the main label to `externally traceable material` when they appear only as aggregate author reports or cannot be checked item by item. Code `externally traceable material` only when the external material can be aligned with a concrete system output, target version, reproducibility material, and a public issue, advisory, CVE, PR, commit, vendor notice, or specific vulnerability claim.

If the system provides PoC, PoV, replay, patch validation, or verified benchmark artifacts, but external confirmation appears only as an aggregate author-reported clue, keep the main label at `reproducible validation` and record the external clue in the rationale or uncertainty note.

