#!/usr/bin/env python3
"""Build the author full-text audit and a blind second-coder sheet for the 2026-07-15 update search."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "data" / "submission_update_20260715_screening_audit.csv"
AUDIT = ROOT / "data" / "submission_update_20260715_full_coding_audit.csv"
BLIND = ROOT / "data" / "submission_update_20260715_second_coder_blind_template.csv"


def decision(
    layer: str,
    rule: str,
    domain: str,
    lifecycle: str,
    capabilities: str,
    evidence: str,
    trace: str,
    shape: str,
    boundary: str,
    reason: str,
    uncertainty: str = "",
) -> dict[str, str]:
    return {
        "author_analysis_layer": layer,
        "inclusion_rule_applied": rule,
        "target_domain": domain,
        "lifecycle_coverage": lifecycle,
        "agentic_capabilities": capabilities,
        "strongest_evidence_output": evidence,
        "external_traceability": trace,
        "primary_system_shape": shape,
        "claim_boundary": boundary,
        "author_decision_reason": reason,
        "uncertainty_note": uncertainty,
    }


STUDY = "provisional_study_level_candidate_pending_independent_review"
EXTENDED = "extended_synthesis"
OBSERVABLE = "observable tool routing, feedback interpretation, validation, state update, or reporting-boundary effect"
STATIC_ONLY = "LLM-assisted static-analysis or management workflow without an observable execution-feedback or validation loop"
ADJACENT = "adjacent security workflow rather than target-software vulnerability mining"


DECISIONS: dict[str, dict[str, str]] = {
    "2606.22647": decision(STUDY, OBSERVABLE, "repository-level vulnerability repair", "candidate analysis; patch validation", "context aggregation / rule extraction; feedback interpretation / loop adjustment; validation organization / evidence packaging; long-horizon state management", "reproducible validation", "benchmark ground truth / public material", "PoC/PoV validation agent", "Supports repair success under the reported repositories, versions, build, and test protocol.", "RAG, cross-file curation, and iterative repair are connected to executable patch checks rather than a one-shot patch suggestion."),
    "2606.22263": decision(STUDY, OBSERVABLE, "repository-scale memory-safety analysis", "candidate analysis; execution observation; reproduction and validation", "context aggregation / rule extraction; tool routing / strategy routing; feedback interpretation / loop adjustment; validation organization / evidence packaging; long-horizon state management", "reproducible validation", "benchmark ground truth / public material", "candidate-analysis system", "Supports sanitizer-checked PoV validation on the reported repository snapshots; broader discovery claims require aligned public records.", "The paper reports executable PoVs and deterministic sanitizer checks; external novelty claims remain source-limited unless individually traceable."),
    "2606.19149": decision(STUDY, OBSERVABLE, "repository-level vulnerability discovery", "candidate analysis; path exploration; execution observation; reproduction and validation", "context aggregation / rule extraction; tool routing / strategy routing; feedback interpretation / loop adjustment; validation organization / evidence packaging; long-horizon state management", "reproducible validation", "benchmark ground truth / public material", "long-horizon pentest and CRS agent", "Supports dynamically verified findings in the reported sandboxed targets and evaluation protocol.", "Static decomposition, adversarial verification, and sandbox execution are observable stages."),
    "2606.18619": decision(STUDY, OBSERVABLE, "specification-guided source-code analysis", "candidate analysis; path exploration; execution observation", "context aggregation / rule extraction; feedback interpretation / loop adjustment; validation organization / evidence packaging", "runtime safety signal", "benchmark ground truth / public material", "candidate-analysis system", "Supports security-condition violations reached by the guided execution process; stronger reproducibility claims require per-finding validation packages.", "The inferred assertions and guided fuzzer create an execution oracle, but the public material reviewed here does not establish a replay package for every finding."),
    "2606.16420": decision(STUDY, OBSERVABLE, "agentic security auditing", "candidate analysis; reporting and audit", "context aggregation / rule extraction; feedback interpretation / loop adjustment; long-horizon state management; failure reuse / strategy update", "controlled task completion", "benchmark ground truth / public material", "long-horizon pentest and CRS agent", "Supports improved audit-task performance and transferable playbooks within the evaluated benchmark.", "The evaluator-reviser loop evolves playbooks from prior failures; it does not by itself establish open-world vulnerability discovery."),
    "2606.13037": decision(STUDY, OBSERVABLE, "one-day vulnerability input generation", "path and input exploration; execution observation; reproduction and validation", "context aggregation / rule extraction; tool routing / strategy routing; feedback interpretation / loop adjustment; validation organization / evidence packaging", "reproducible validation", "benchmark ground truth / public material", "feedback-driven fuzzing agent", "Supports triggering of the evaluated one-day vulnerabilities under the patch-derived oracle and directed-execution setup.", "Unknown-vulnerability reports are author-reported unless aligned with public issue or advisory records."),
    "2606.00669": decision(STUDY, OBSERVABLE, "neuro-symbolic vulnerability discovery", "candidate analysis; path and input exploration; execution observation; reproduction and validation", "context aggregation / rule extraction; tool routing / strategy routing; feedback interpretation / loop adjustment; validation organization / evidence packaging", "reproducible validation", "author-reported external clue", "candidate-analysis system", "Supports concrete sanitizer-checked triggers produced by the Datalog/SMT/LLM pipeline on the reported targets.", "Upstream reports and fixes are treated as author-reported external clues unless each result is publicly aligned."),
    "2605.30105": decision(STUDY, OBSERVABLE, "repository-level vulnerability repair", "candidate analysis; patch validation", "context aggregation / rule extraction; feedback interpretation / loop adjustment; validation organization / evidence packaging; long-horizon state management; failure reuse / strategy update", "reproducible validation", "benchmark ground truth / public material", "PoC/PoV validation agent", "Supports benchmark-scoped repair and patch-validation claims.", "Experience reuse is coded as a stateful repair mechanism, not evidence that repairs generalize beyond the evaluated benchmarks."),
    "2605.21824": decision(STUDY, OBSERVABLE, "library fuzz-harness generation", "path and input exploration; execution observation; reporting and audit", "context aggregation / rule extraction; tool routing / strategy routing; feedback interpretation / loop adjustment; validation organization / evidence packaging", "runtime safety signal", "author-reported external clue", "feedback-driven fuzzing agent", "Supports quality-assured harness generation and runtime bug signals in the reported fuzzing campaigns.", "Maintainer fixes and confirmations are aggregate author reports unless linked finding by finding."),
    "2605.17450": decision(STUDY, OBSERVABLE, "vulnerability repair", "execution observation; patch validation", "context aggregation / rule extraction; feedback interpretation / loop adjustment; validation organization / evidence packaging; failure reuse / strategy update", "reproducible validation", "benchmark ground truth / public material", "PoC/PoV validation agent", "Supports repair validation through contrasted failing/non-failing executions and accepted patch checks.", "The replication package supports protocol-level reproducibility; claim scope remains the evaluated targets."),
    "2605.17444": decision(STUDY, OBSERVABLE, "repository-level vulnerability repair", "candidate analysis; patch validation", "context aggregation / rule extraction; validation organization / evidence packaging; long-horizon state management; failure reuse / strategy update", "reproducible validation", "benchmark ground truth / public material", "PoC/PoV validation agent", "Supports benchmark-scoped repair outcomes with memory and execution feedback.", "Memory effects are evaluated on named benchmarks and should not be read as universal long-horizon reliability."),
    "2605.15097": decision(STUDY, OBSERVABLE, "binary memory-corruption discovery", "candidate analysis; path exploration; execution observation; reproduction and validation", "context aggregation / rule extraction; tool routing / strategy routing; feedback interpretation / loop adjustment; validation organization / evidence packaging", "reproducible validation", "author-reported external clue", "candidate-analysis system", "Supports semantically grounded witnesses and runtime-validated memory-corruption findings on the evaluated binaries.", "The reported external confirmation remains author-reported until publicly linked to the concrete system output."),
    "2605.14431": decision(STUDY, OBSERVABLE, "library fuzzing", "path and input exploration; execution observation; reporting and audit", "context aggregation / rule extraction; tool routing / strategy routing; feedback interpretation / loop adjustment; validation organization / evidence packaging; long-horizon state management", "runtime safety signal", "author-reported external clue", "feedback-driven fuzzing agent", "Supports coverage and triaged runtime bug signals from the reported campaigns.", "Acknowledged or fixed bugs are aggregate external clues unless the public material aligns individual reports and triggers."),
    "2605.10074": decision(STUDY, OBSERVABLE, "coverage-guided fuzzing", "path and input exploration; execution observation; reproduction and validation", "context aggregation / rule extraction; tool routing / strategy routing; feedback interpretation / loop adjustment; validation organization / evidence packaging; failure reuse / strategy update", "reproducible validation", "author-reported external clue", "feedback-driven fuzzing agent", "Supports executed PoC-based validation under the reported fuzzing setup.", "Bounty and CVE statements are author-reported external clues unless a public record is aligned with each generated PoC."),
    "2605.04251": decision(STUDY, OBSERVABLE, "memory-safety vulnerability repair", "execution observation; patch validation", "context aggregation / rule extraction; feedback interpretation / loop adjustment; validation organization / evidence packaging", "reproducible validation", "benchmark ground truth / public material", "PoC/PoV validation agent", "Supports root-cause-guided patch validation on the evaluated C/C++ vulnerabilities.", "Expert assessment complements the executable checks but does not expand the benchmark denominator."),
    "2605.03956": decision(STUDY, OBSERVABLE, "proof-of-vulnerability test generation", "candidate analysis; reproduction and validation", "context aggregation / rule extraction; tool routing / strategy routing; feedback interpretation / loop adjustment; validation organization / evidence packaging", "reproducible validation", "benchmark ground truth / public material", "PoC/PoV validation agent", "Supports generated proof-of-vulnerability tests that execute against the reported application/library pairs.", "The evidence is reproduction-oriented and does not estimate open-world discovery prevalence."),
    "2605.02789": decision(STUDY, OBSERVABLE, "compiler fuzzing", "path and input exploration; execution observation", "feedback interpretation / loop adjustment; long-horizon state management; failure reuse / strategy update", "runtime safety signal", "not reported", "feedback-driven fuzzing agent", "Supports coverage growth and compiler failure signals in the evaluated campaigns.", "Runtime failures require separate security triage before being written as confirmed vulnerabilities."),
    "2605.02346": decision(STUDY, OBSERVABLE, "industrial OT vulnerability management", "candidate analysis; path exploration; execution observation; reproduction and validation; patch validation; reporting and audit", "tool routing / strategy routing; feedback interpretation / loop adjustment; validation organization / evidence packaging; long-horizon state management; governance / human gates / disclosure control", "controlled task completion", "benchmark ground truth / public material", "long-horizon pentest and CRS agent", "Supports end-to-end task completion in the reported bare-metal OT test environment.", "The controlled environment and governance design bound claims about deployment in live industrial networks."),
    "2605.01885": decision(EXTENDED, STATIC_ONLY, "SAST false-positive reduction", "candidate analysis", "context aggregation / rule extraction", "candidate judgment", "benchmark ground truth / public material", "candidate-analysis system", "Supports candidate triage quality on the evaluated SAST benchmark.", "The reviewed workflow consumes scanner findings but does not expose an execution-feedback or reproducible validation loop that changes the downstream security workflow."),
    "2605.01739": decision(EXTENDED, STATIC_ONLY, "vulnerability management and prioritization", "candidate analysis; reporting and audit", "context aggregation / rule extraction; validation organization / evidence packaging", "candidate judgment", "not reported", "candidate-analysis system", "Supports vulnerability-management prioritization and reporting within the evaluated workflow.", "The public workflow centers on scanner-output interpretation, scoring, and management rather than target execution or validation."),
    "2605.00034": decision(STUDY, OBSERVABLE, "Rust memory-safety analysis", "candidate analysis; path and input exploration; execution observation", "context aggregation / rule extraction; tool routing / strategy routing; feedback interpretation / loop adjustment; validation organization / evidence packaging", "runtime safety signal", "benchmark ground truth / public material", "candidate-analysis system", "Supports symbolic-execution detection of known memory vulnerabilities in the reconstructed CVE snippets.", "Incomplete snippets and known-CVE tasks constrain the claim to the reconstruction protocol."),
    "2604.22427": decision(STUDY, OBSERVABLE, "black-box and digital-twin offensive security", "candidate analysis; path exploration; execution observation; reproduction and validation", "tool routing / strategy routing; feedback interpretation / loop adjustment; validation organization / evidence packaging; long-horizon state management; governance / human gates / disclosure control", "controlled task completion", "benchmark ground truth / public material", "long-horizon pentest and CRS agent", "Supports adaptive exploitation task completion in the isolated digital-twin scenarios.", "The risk-mitigated test setting does not directly establish performance against unrestricted live targets."),
    "2604.18718": decision(STUDY, OBSERVABLE, "interactive offensive-security architecture evaluation", "candidate analysis; path exploration; execution observation; reproduction and validation", "tool routing / strategy routing; feedback interpretation / loop adjustment; validation organization / evidence packaging; long-horizon state management", "controlled task completion", "benchmark ground truth / public material", "long-horizon pentest and CRS agent", "Supports comparative claims about agent topology under the matched 20-target benchmark and validated-detection protocol.", "The paper is evaluation-centered, but it executes observable tool-using workflows and reports validation outcomes rather than serving only as benchmark context."),
    "2604.17184": decision(STUDY, OBSERVABLE, "neuro-symbolic vulnerability repair", "candidate analysis; patch validation", "context aggregation / rule extraction; feedback interpretation / loop adjustment; validation organization / evidence packaging", "reproducible validation", "benchmark ground truth / public material", "PoC/PoV validation agent", "Supports benchmark-scoped patch acceptance under compiler, test, and security-analysis checks.", "The public evidence supports repair validation, not a general claim of semantic correctness for unseen projects."),
    "2604.13611": decision(STUDY, OBSERVABLE, "smart-contract vulnerability validation", "candidate analysis; reproduction and validation", "context aggregation / rule extraction; feedback interpretation / loop adjustment; validation organization / evidence packaging; failure reuse / strategy update", "reproducible validation", "benchmark ground truth / public material", "PoC/PoV validation agent", "Supports triggerability-and-profitability validation on the 264 labeled contracts under the reported EVM setup.", "PoCs are iteratively refined from execution feedback; the full text was reviewed after the initial metadata-only screening."),
    "2604.12172": decision(STUDY, OBSERVABLE, "cross-chain bridge formal verification", "candidate analysis; execution observation", "context aggregation / rule extraction; tool routing / strategy routing; feedback interpretation / loop adjustment; validation organization / evidence packaging", "runtime safety signal", "benchmark ground truth / public material", "candidate-analysis system", "Supports model-checker counterexamples against the generated TLA+ specifications in the evaluated bridge models.", "Formal-model counterexamples are security-conditioned oracle traces, not automatically concrete target-software exploit validation."),
    "2604.06633": decision(STUDY, OBSERVABLE, "repository-level static and semantic vulnerability analysis", "candidate analysis; reproduction and validation; patch validation; reporting and audit", "context aggregation / rule extraction; tool routing / strategy routing; feedback interpretation / loop adjustment; validation organization / evidence packaging; long-horizon state management", "reproducible validation", "author-reported external clue", "candidate-analysis system", "Supports CodeQL-guided findings for which the PoC and verification agents produce executable validation under the reported setup.", "Zero-day and confirmation statements remain author-reported unless public records align them with specific PoCs, versions, and fixes."),
    "2604.06618": decision(STUDY, OBSERVABLE, "automated vulnerability reproduction", "candidate analysis; reproduction and validation", "context aggregation / rule extraction; feedback interpretation / loop adjustment; validation organization / evidence packaging; long-horizon state management; failure reuse / strategy update", "reproducible validation", "benchmark ground truth / public material", "PoC/PoV validation agent", "Supports benchmark-scoped PoC reproduction through semantic runtime oracles and adaptive failure routing.", "The adaptive policy is evidence of workflow control; the supported vulnerability claim still depends on successful replay."),
    "2604.06506": decision(STUDY, OBSERVABLE, "symbolic-execution-guided vulnerability discovery", "candidate analysis; path and input exploration; execution observation; reproduction and validation", "context aggregation / rule extraction; tool routing / strategy routing; feedback interpretation / loop adjustment; validation organization / evidence packaging", "reproducible validation", "benchmark ground truth / public material", "candidate-analysis system", "Supports concrete sanitizer-triggering inputs produced by the static-analysis/LLM/symbolic-execution loop.", "The claim is bounded to the reported projects, symbolic-execution configuration, and replay environment."),
    "2604.01977": decision(EXTENDED, ADJACENT, "web vulnerability detection-rule generation", "reporting and audit", "context aggregation / rule extraction; feedback interpretation / loop adjustment; governance / human gates / disclosure control", "controlled task completion", "author-reported external clue", "candidate-analysis system", "Supports generation and production validation of HTTP detection rules from known-vulnerability templates.", "The target output is a detection rule for already disclosed CVEs rather than target-software vulnerability discovery or reproduction, so it informs the boundary ecosystem and reporting discussion."),
    "2604.01442": decision(STUDY, OBSERVABLE, "fuzz-input generator synthesis", "path and input exploration; execution observation", "context aggregation / rule extraction; feedback interpretation / loop adjustment; validation organization / evidence packaging", "controlled task completion", "benchmark ground truth / public material", "feedback-driven fuzzing agent", "Supports executable generator synthesis and coverage-oriented task completion on the evaluated Java libraries.", "Coverage is treated as exploration progress rather than confirmed vulnerability evidence."),
    "2603.22577": decision(STUDY, OBSERVABLE, "CTF and offensive-security task solving", "candidate analysis; path exploration; execution observation; reproduction and validation", "tool routing / strategy routing; feedback interpretation / loop adjustment; validation organization / evidence packaging; long-horizon state management", "controlled task completion", "benchmark ground truth / public material", "long-horizon pentest and CRS agent", "Supports autonomous task completion in the reported live CTF and controlled challenge set.", "Competition placement and flags establish bounded task success rather than open-world vulnerability discovery prevalence."),
    "2603.13384": decision(STUDY, OBSERVABLE, "repository-level vulnerability detection", "candidate analysis; execution observation; reporting and audit", "context aggregation / rule extraction; tool routing / strategy routing; feedback interpretation / loop adjustment; validation organization / evidence packaging; long-horizon state management", "runtime safety signal", "benchmark ground truth / public material", "candidate-analysis system", "Supports calibrated candidate detection and selective verifier outcomes under the reported datasets and protocol.", "The verifier planning and execution are observable, but the reviewed material does not provide a replay package for every reported candidate."),
    "2603.08616": decision(STUDY, OBSERVABLE, "Java library fuzz-harness generation", "path and input exploration; execution observation", "context aggregation / rule extraction; tool routing / strategy routing; feedback interpretation / loop adjustment; validation organization / evidence packaging; long-horizon state management", "runtime safety signal", "author-reported external clue", "feedback-driven fuzzing agent", "Supports compile-correct harness generation, coverage-guided refinement, and runtime bug signals in the reported campaigns.", "Previously unknown bug statements remain author-reported unless aligned with public issue and trigger records."),
    "2603.01154": decision(STUDY, OBSERVABLE, "repository-level SAST augmentation", "candidate analysis; reporting and audit", "context aggregation / rule extraction; tool routing / strategy routing; feedback interpretation / loop adjustment; validation organization / evidence packaging; long-horizon state management; failure reuse / strategy update", "candidate judgment", "benchmark ground truth / public material", "candidate-analysis system", "Supports project-contextual candidate verification and analogous-candidate discovery on CWE-Bench-Java.", "The public evidence reviewed is primarily detection and false-positive evaluation rather than executable reproduction."),
    "2602.19490": decision(STUDY, OBSERVABLE, "DBMS fuzzing", "path and input exploration; execution observation; reproduction and validation", "context aggregation / rule extraction; feedback interpretation / loop adjustment; validation organization / evidence packaging", "runtime safety signal", "author-reported external clue", "feedback-driven fuzzing agent", "Supports DBMS crash and oracle findings under the reported versions, replay mechanism, and standardized triage protocol.", "Vendor confirmations, fixes, and CVEs are aggregate author reports unless individual public records are aligned with the generated cases."),
    "2602.09774": decision(STUDY, OBSERVABLE, "Python package vulnerability discovery", "candidate analysis; reproduction and validation; reporting and audit", "context aggregation / rule extraction; tool routing / strategy routing; feedback interpretation / loop adjustment; validation organization / evidence packaging; long-horizon state management", "reproducible validation", "author-reported external clue", "candidate-analysis system", "Supports CodeQL-generated findings accompanied by reported PoC reproduction in the evaluated packages.", "New CVEs and maintainer actions are treated as author-reported external clues unless the public records are aligned finding by finding."),
    "2602.05721": decision(STUDY, OBSERVABLE, "automated vulnerability reproduction", "candidate analysis; reproduction and validation", "context aggregation / rule extraction; tool routing / strategy routing; feedback interpretation / loop adjustment; validation organization / evidence packaging; long-horizon state management; failure reuse / strategy update", "reproducible validation", "benchmark ground truth / public material", "PoC/PoV validation agent", "Supports executable PoC reproduction on SecBench.js and PatchEval under the dual-loop validation protocol.", "The benchmark and patched-version checks bound the claim to known vulnerability reproduction."),
    "2601.17762": decision(STUDY, OBSERVABLE, "recurring-vulnerability management and repair", "candidate analysis; reproduction and validation; patch validation; reporting and audit", "context aggregation / rule extraction; tool routing / strategy routing; feedback interpretation / loop adjustment; validation organization / evidence packaging; long-horizon state management", "reproducible validation", "benchmark ground truth / public material", "PoC/PoV validation agent", "Supports recurring-vulnerability detection, confirmation, repair, and validation on the reported patch-migration datasets.", "End-to-end management is assessed on known recurring cases and does not estimate general discovery coverage."),
    "2601.13933": decision(STUDY, OBSERVABLE, "vulnerability issue resolution", "candidate analysis; reproduction and validation; patch validation", "context aggregation / rule extraction; tool routing / strategy routing; feedback interpretation / loop adjustment; validation organization / evidence packaging; long-horizon state management", "reproducible validation", "benchmark ground truth / public material", "PoC/PoV validation agent", "Supports SEC-bench issue resolution through repository exploration, PoC re-execution, safety-property refinement, and patch validation.", "Resolution rates remain tied to the benchmark versions, tests, and PoC environment."),
    "2601.10865": decision(STUDY, OBSERVABLE, "JavaScript taint-analysis specification extraction", "candidate analysis; reporting and audit", "context aggregation / rule extraction; tool routing / strategy routing; feedback interpretation / loop adjustment; validation organization / evidence packaging", "candidate judgment", "author-reported external clue", "candidate-analysis system", "Supports auditable taint specifications and CodeQL candidate findings under the reported npm datasets.", "Maintainer reports for newly found candidates do not by themselves establish public, reproducible validation for each finding."),
}


AUDIT_FIELDS = [
    "arxiv_id",
    "title",
    "official_url",
    "published",
    "review_material",
    "full_text_status",
    "author_analysis_layer",
    "inclusion_rule_applied",
    "target_domain",
    "lifecycle_coverage",
    "agentic_capabilities",
    "strongest_evidence_output",
    "external_traceability",
    "primary_system_shape",
    "claim_boundary",
    "author_decision_reason",
    "uncertainty_note",
    "formal_second_coder_status",
]

BLIND_FIELDS = [
    "update_id",
    "arxiv_id",
    "title",
    "publication_status",
    "materials_to_review",
    "coder2_analysis_layer_decision",
    "coder2_inclusion_reason",
    "coder2_lifecycle_coverage",
    "coder2_primary_system_shape",
    "coder2_cross_stage_capability_label",
    "coder2_strongest_evidence_output",
    "coder2_external_traceability_label",
    "coder2_claim_boundary",
    "coder2_uncertainty_note",
]


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as handle:
        candidates = [
            row
            for row in csv.DictReader(handle)
            if row["screening_status"] == "potentially_eligible_update_record"
        ]

    ids = {row["arxiv_id"] for row in candidates}
    if ids != set(DECISIONS):
        missing = sorted(ids - set(DECISIONS))
        extra = sorted(set(DECISIONS) - ids)
        raise SystemExit(f"Decision map mismatch. missing={missing}, extra={extra}")

    audit_rows: list[dict[str, str]] = []
    blind_rows: list[dict[str, str]] = []
    for index, source_row in enumerate(candidates, start=1):
        arxiv_id = source_row["arxiv_id"]
        row = {
            "arxiv_id": arxiv_id,
            "title": source_row["title"],
            "official_url": source_row["official_url"],
            "published": source_row["published"],
            "review_material": "public arXiv full text and public metadata",
            "full_text_status": "full_text_reviewed",
            **DECISIONS[arxiv_id],
            "formal_second_coder_status": "pending_independent_blind_review",
        }
        audit_rows.append(row)
        blind_rows.append(
            {
                "update_id": f"U{index:02d}",
                "arxiv_id": arxiv_id,
                "title": source_row["title"],
                "publication_status": "public_preprint_or_publication",
                "materials_to_review": (
                    f"Review the public paper and public non-sensitive artifact materials for arXiv:{arxiv_id}. "
                    "Independently decide the analytical layer and code lifecycle coverage, primary system shape, "
                    "cross-stage capabilities, principal reported evidence output, external traceability, and claim boundary. "
                    "Do not consult the author audit or adjudication files before completing the independent pass."
                ),
                "coder2_analysis_layer_decision": "",
                "coder2_inclusion_reason": "",
                "coder2_lifecycle_coverage": "",
                "coder2_primary_system_shape": "",
                "coder2_cross_stage_capability_label": "",
                "coder2_strongest_evidence_output": "",
                "coder2_external_traceability_label": "",
                "coder2_claim_boundary": "",
                "coder2_uncertainty_note": "",
            }
        )

    with AUDIT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=AUDIT_FIELDS)
        writer.writeheader()
        writer.writerows(audit_rows)

    with BLIND.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=BLIND_FIELDS)
        writer.writeheader()
        writer.writerows(blind_rows)

    layer_counts: dict[str, int] = {}
    for row in audit_rows:
        layer = row["author_analysis_layer"]
        layer_counts[layer] = layer_counts.get(layer, 0) + 1
    print(f"Wrote {len(audit_rows)} full-text audit rows to {AUDIT}")
    print(f"Wrote {len(blind_rows)} blank blind-review rows to {BLIND}")
    for layer, count in sorted(layer_counts.items()):
        print(f"  {layer}: {count}")


if __name__ == "__main__":
    main()
