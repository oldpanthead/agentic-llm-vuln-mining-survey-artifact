#!/usr/bin/env python3
"""Prepare the 13-record late addendum found by expanded full-text review.

The earlier nine-record addendum is preserved unchanged. This script writes a
separate first-coder file and a blind second-coder file, and refuses to replace
coder-entered results.
"""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
ACCESS = DATA / "final_multisource_search_20260730_fulltext_access.csv"
SCREENING = DATA / "final_multisource_search_20260730_screening_audit.csv"
FIRST_OUT = DATA / "final_multisource_search_20260730_first_coder_late_addendum.csv"
SECOND_OUT = DATA / "final_multisource_search_20260730_second_coder_late_addendum_blind.csv"

ADDENDUM_IDS = [
    "FMS0090",
    "FMS0100",
    "FMS0239",
    "FMS0297",
    "FMS0362",
    "FMS0376",
    "FMS0479",
    "FMS0533",
    "FMS0677",
    "FMS0885",
    "FMS0925",
    "FMS1394",
    "FMS1473",
]

FIRST_CODER = {
    "FMS0090": {
        "eligibility_reason": "Two execution validators return payload and path feedback to an adaptive prompting loop that revises web-vulnerability PoCs before re-execution.",
        "final_lifecycle_coverage": "path and input exploration;execution observation;reproduction and validation",
        "final_cross_stage_capabilities": "context aggregation / rule extraction;feedback interpretation / loop adjustment;validation organization / evidence packaging;long-horizon state management",
        "final_primary_system_shape": "reproduction-, validation-, and repair-centered agent",
        "final_principal_reported_evidence_output": "reproducible validation",
        "final_external_traceability": "benchmark ground truth / public material",
        "final_claim_boundary": "The material supports executable PoC generation for versioned, publicly disclosed web vulnerabilities under the study's validators. It does not establish open-world discovery of previously unknown vulnerabilities.",
        "material_checked": "Public full text: Sections 3-5, adaptive-feedback design, validator definitions, and the 100-CVE evaluation.",
        "uncertainty_note": "The target vulnerabilities are supplied by public disclosure records rather than discovered by the evaluated system.",
    },
    "FMS0100": {
        "eligibility_reason": "A generator and validator form a bounded repair loop; validator feedback revises the role-permission patch until it passes or the attempt limit is reached.",
        "final_lifecycle_coverage": "candidate analysis;execution observation;patch validation",
        "final_cross_stage_capabilities": "context aggregation / rule extraction;feedback interpretation / loop adjustment;validation organization / evidence packaging;long-horizon state management",
        "final_primary_system_shape": "reproduction-, validation-, and repair-centered agent",
        "final_principal_reported_evidence_output": "reproducible validation",
        "final_external_traceability": "benchmark ground truth / public material",
        "final_claim_boundary": "The material supports access-control patch generation checked by compilation, validator review, and exploit-script execution on the reported 118-case benchmark. It does not establish that every generated repair is independently maintained or externally confirmed.",
        "material_checked": "Public full text: Sections IV-V, generator-validator loop, patch-validation procedure, Table II, and exploit-script evaluation.",
        "uncertainty_note": "The external CVE and incident records provide benchmark provenance rather than system-originated discovery.",
    },
    "FMS0239": {
        "eligibility_reason": "ATLANTIS combines LLM agents with static analysis, symbolic execution, directed fuzzing, PoV generation, patching, and fallback scheduling in an evaluated cyber reasoning system.",
        "final_lifecycle_coverage": "candidate analysis;path and input exploration;execution observation;reproduction and validation;patch validation;reporting and audit",
        "final_cross_stage_capabilities": "context aggregation / rule extraction;tool routing / strategy routing;feedback interpretation / loop adjustment;validation organization / evidence packaging;long-horizon state management;failure reuse / strategy update;governance / human gates / disclosure control",
        "final_primary_system_shape": "long-horizon pentest and CRS agent",
        "final_principal_reported_evidence_output": "reproducible validation",
        "final_external_traceability": "benchmark ground truth / public material",
        "final_claim_boundary": "The material supports PoV and patch-validation outcomes within the AIxCC task environment and the released ATLANTIS workflow. Competition success does not by itself establish open-world discovery outside those targets and oracles.",
        "material_checked": "Public final report: Sections 4-7, multi-fuzzer loop, symbolic execution, PoV generation, patching, scheduling, and end-to-end evaluation.",
        "uncertainty_note": "The report describes a large heterogeneous CRS; individual subsystems do not all use LLM control.",
    },
    "FMS0297": {
        "eligibility_reason": "JitVul evaluates ReAct agents that request interprocedural context, observe retrieved code, and iteratively refine repository-level vulnerability judgments.",
        "final_lifecycle_coverage": "candidate analysis",
        "final_cross_stage_capabilities": "context aggregation / rule extraction;tool routing / strategy routing;feedback interpretation / loop adjustment;long-horizon state management",
        "final_primary_system_shape": "candidate-analysis system",
        "final_principal_reported_evidence_output": "candidate judgment",
        "final_external_traceability": "benchmark ground truth / public material",
        "final_claim_boundary": "The material supports vulnerability and fix judgments on CVE-linked repository pairs after agent-selected context retrieval. It does not supply execution-based validation of the judged vulnerability or fix.",
        "material_checked": "Public full text: Sections 2-4, JitVul construction, ReAct context tools, benchmark definition, and evaluation.",
        "uncertainty_note": "CVE and commit links are benchmark ground truth rather than externally aligned new system findings.",
    },
    "FMS0362": {
        "eligibility_reason": "FDSP feeds compiler and Bandit findings back to the LLM so that later patch candidates respond to external tool results.",
        "final_lifecycle_coverage": "candidate analysis;patch validation",
        "final_cross_stage_capabilities": "context aggregation / rule extraction;feedback interpretation / loop adjustment;validation organization / evidence packaging",
        "final_primary_system_shape": "reproduction-, validation-, and repair-centered agent",
        "final_principal_reported_evidence_output": "reproducible validation",
        "final_external_traceability": "benchmark ground truth / public material",
        "final_claim_boundary": "The material supports iterative security repair on PythonSecurityEval when revised code compiles and the reported Bandit finding is removed. It does not establish exploit-level validation or independent confirmation of real-world fixes.",
        "material_checked": "Public full text: Fig. 1, FDSP algorithm and iteration budget, PythonSecurityEval construction, Bandit feedback, and evaluation.",
        "uncertainty_note": "Validation is scanner- and benchmark-based rather than a vulnerability-specific runtime trigger.",
    },
    "FMS0376": {
        "eligibility_reason": "Chaintrix feeds protocol-coverage gaps back into focused LLM audit prompts and routes residual findings through deterministic checks and selected symbolic or fuzz validation.",
        "final_lifecycle_coverage": "candidate analysis;path and input exploration;execution observation;reporting and audit",
        "final_cross_stage_capabilities": "context aggregation / rule extraction;tool routing / strategy routing;feedback interpretation / loop adjustment;validation organization / evidence packaging;long-horizon state management",
        "final_primary_system_shape": "candidate-analysis system",
        "final_principal_reported_evidence_output": "candidate judgment",
        "final_external_traceability": "benchmark ground truth / public material",
        "final_claim_boundary": "The material supports benchmark-scored smart-contract findings after structural filtering and selective executable checking. Because executable validation is selective and the main result is an audit finding set, it does not establish a replay package for every reported candidate.",
        "material_checked": "Public full text: Sections 3-4, resolution map, risk dossiers, coverage-feedback loop, selective Mythril/fuzz validation, and EVMbench evaluation.",
        "uncertainty_note": "The pipeline contains fixed deterministic stages; agentic inclusion rests on feedback-driven re-auditing and routing of residual claims.",
    },
    "FMS0479": {
        "eligibility_reason": "Agents iteratively formalize protocols, invoke Tamarin, and adapt to prover feedback until a counterexample is found or the call budget is exhausted.",
        "final_lifecycle_coverage": "candidate analysis;path and input exploration;execution observation;reproduction and validation",
        "final_cross_stage_capabilities": "context aggregation / rule extraction;tool routing / strategy routing;feedback interpretation / loop adjustment;validation organization / evidence packaging;long-horizon state management;failure reuse / strategy update",
        "final_primary_system_shape": "reproduction-, validation-, and repair-centered agent",
        "final_principal_reported_evidence_output": "reproducible validation",
        "final_external_traceability": "benchmark ground truth / public material",
        "final_claim_boundary": "The material supports Tamarin counterexamples that are translated and checked in the reported symbolic sandbox for the benchmark protocols. The result remains conditional on the correctness of the generated formalization and symbolic assumptions.",
        "material_checked": "Public full text: Sections 2.3-4, middleware loop, Tamarin feedback filtering, attack-trace translation, symbolic validator, and benchmark evaluation.",
        "uncertainty_note": "The reviewed version states that supporting tools were planned for release, so public replay availability is limited.",
    },
    "FMS0533": {
        "eligibility_reason": "VIC-RAGENT passes structured intermediate judgments through specialized agents and uses audit-supervisor feedback before the final commit classification.",
        "final_lifecycle_coverage": "candidate analysis;reporting and audit",
        "final_cross_stage_capabilities": "context aggregation / rule extraction;feedback interpretation / loop adjustment;validation organization / evidence packaging;long-horizon state management",
        "final_primary_system_shape": "candidate-analysis system",
        "final_principal_reported_evidence_output": "candidate judgment",
        "final_external_traceability": "benchmark ground truth / public material",
        "final_claim_boundary": "The material supports vulnerability-inducing-commit judgments and explanations on the V-SZZ benchmark after multi-stage agent review. It does not provide execution evidence that independently validates exploitability.",
        "material_checked": "Public full text: Sections 2-4, Fig. 1, audit-supervisor feedback, decision stages, and V-SZZ evaluation.",
        "uncertainty_note": "Agent exchanges validate reasoning consistency rather than executing the target software.",
    },
    "FMS0677": {
        "eligibility_reason": "The study executes existing pentesting agents against expert-annotated real-world targets and evaluates their multi-step tool trajectories and reported findings.",
        "final_lifecycle_coverage": "candidate analysis;path and input exploration;execution observation;reporting and audit",
        "final_cross_stage_capabilities": "tool routing / strategy routing;feedback interpretation / loop adjustment;long-horizon state management;governance / human gates / disclosure control",
        "final_primary_system_shape": "long-horizon pentest and CRS agent",
        "final_principal_reported_evidence_output": "controlled task completion",
        "final_external_traceability": "benchmark ground truth / public material",
        "final_claim_boundary": "The material supports finding-level evaluation of multi-step pentesting agents against expert-maintained target ground truth. It evaluates bounded target performance rather than establishing independent public disclosure outcomes.",
        "material_checked": "Public full text: Sections 1-4, target-selection protocol, finding-to-ground-truth pipeline, trajectory execution, and evaluation procedure.",
        "uncertainty_note": "The contribution is an evaluation protocol applied to existing agents rather than a new unified agent architecture.",
    },
    "FMS0885": {
        "eligibility_reason": "VulTrial passes vulnerability arguments among specialized agents over multiple discussion rounds before a review-board verdict.",
        "final_lifecycle_coverage": "candidate analysis;reporting and audit",
        "final_cross_stage_capabilities": "context aggregation / rule extraction;feedback interpretation / loop adjustment;validation organization / evidence packaging;long-horizon state management",
        "final_primary_system_shape": "candidate-analysis system",
        "final_principal_reported_evidence_output": "candidate judgment",
        "final_external_traceability": "benchmark ground truth / public material",
        "final_claim_boundary": "The material supports vulnerability labels and explanations on the paired PrimeVul benchmark after structured multi-agent debate. It does not supply runtime validation of the predicted vulnerabilities.",
        "material_checked": "Public full text: Sections 2-4, Fig. 1, role-specific debate sequence, review-board decision, and PrimeVul evaluation.",
        "uncertainty_note": "The interaction is model-to-model deliberation rather than tool-mediated execution feedback.",
    },
    "FMS0925": {
        "eligibility_reason": "LLM-SmartAudit uses specialized conversational agents and iterative feedback to move from contract analysis through vulnerability identification to a final audit report.",
        "final_lifecycle_coverage": "candidate analysis;reporting and audit",
        "final_cross_stage_capabilities": "context aggregation / rule extraction;feedback interpretation / loop adjustment;validation organization / evidence packaging;long-horizon state management",
        "final_primary_system_shape": "candidate-analysis system",
        "final_principal_reported_evidence_output": "candidate judgment",
        "final_external_traceability": "benchmark ground truth / public material",
        "final_claim_boundary": "The material supports smart-contract vulnerability findings and audit reports on labeled and Code4rena-derived datasets. It does not provide executable validation or item-level external alignment for each reported finding.",
        "material_checked": "Public full text: Sections 3-4, multi-agent conversation workflow, labeled and real-world datasets, final report stage, and evaluation.",
        "uncertainty_note": "Public contest records provide dataset context; the reviewed material does not align each system output to an external outcome.",
    },
    "FMS1394": {
        "eligibility_reason": "StealthBench executes tool-calling offensive-security agents in dockerized tasks and records full action-observation trajectories for task-success and operational-stealth judgment.",
        "final_lifecycle_coverage": "candidate analysis;path and input exploration;execution observation;reporting and audit",
        "final_cross_stage_capabilities": "tool routing / strategy routing;feedback interpretation / loop adjustment;long-horizon state management;governance / human gates / disclosure control",
        "final_primary_system_shape": "long-horizon pentest and CRS agent",
        "final_principal_reported_evidence_output": "controlled task completion",
        "final_external_traceability": "benchmark ground truth / public material",
        "final_claim_boundary": "The material supports task-completion and stealth measurements for offensive agents across 14 dockerized scenarios with complete tool trajectories. It does not establish external vulnerability discovery beyond the released benchmark tasks.",
        "material_checked": "Public full text: Sections 1-4, Fig. 1, 14-scenario harness, ATIF trajectories, task-success oracle, and judge protocol.",
        "uncertainty_note": "The principal result is benchmark task performance, even when individual scenarios contain real vulnerability behavior.",
    },
    "FMS1473": {
        "eligibility_reason": "Compiler, CodeQL, and KLEE feedback drives iterative repair; prior repair patterns are retrieved for later attempts and final candidates receive symbolic validation.",
        "final_lifecycle_coverage": "candidate analysis;execution observation;patch validation",
        "final_cross_stage_capabilities": "context aggregation / rule extraction;feedback interpretation / loop adjustment;validation organization / evidence packaging;long-horizon state management;failure reuse / strategy update",
        "final_primary_system_shape": "reproduction-, validation-, and repair-centered agent",
        "final_principal_reported_evidence_output": "reproducible validation",
        "final_external_traceability": "benchmark ground truth / public material",
        "final_claim_boundary": "The material supports iterative C-code repair checked by compilation, CodeQL, and final KLEE symbolic execution on the reported benchmarks. It does not establish maintenance or external confirmation of the generated repairs in deployed projects.",
        "material_checked": "Public full text: Sections 3.1-3.4, compiler and CodeQL feedback loop, repair-pattern repository, KLEE validation, and evaluation.",
        "uncertainty_note": "KLEE validation is one-shot after repair iterations; earlier loop feedback comes from compilation and CodeQL.",
    },
}

BASE_FIELDS = [
    "review_order", "discovery_id", "title", "publication_dates", "doi",
    "arxiv_id", "public_fulltext_url", "local_review_pdf", "local_extracted_text",
]
CODE_FIELDS = [
    "eligibility_decision", "eligibility_reason", "final_lifecycle_coverage",
    "final_cross_stage_capabilities", "final_primary_system_shape",
    "final_principal_reported_evidence_output", "final_external_traceability",
    "final_claim_boundary", "material_checked", "decision_note",
    "uncertainty_note", "row_status",
]
BLIND_FIELDS = [
    "review_order", "discovery_id", "title", "publication_dates", "doi",
    "arxiv_id", "public_fulltext_url", "local_review_pdf", "local_extracted_text",
    "eligibility_decision", "eligibility_reason", "final_lifecycle_coverage",
    "lifecycle_review_status", "final_cross_stage_capabilities",
    "capability_review_status", "final_primary_system_shape",
    "shape_review_status", "final_principal_reported_evidence_output",
    "evidence_review_status", "final_external_traceability",
    "traceability_review_status", "final_claim_boundary",
    "claim_boundary_review_status", "material_checked", "decision_note",
    "uncertainty_note", "row_status",
]


def read_index(path: Path) -> dict[str, dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return {row["discovery_id"]: row for row in csv.DictReader(handle)}


def write_rows(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    access = read_index(ACCESS)
    screening = read_index(SCREENING)
    first_rows: list[dict[str, str]] = []
    blind_rows: list[dict[str, str]] = []

    for offset, discovery_id in enumerate(ADDENDUM_IDS, start=96):
        source = screening[discovery_id]
        local = access[discovery_id]
        base = {
            "review_order": str(offset),
            "discovery_id": discovery_id,
            "title": source["title"],
            "publication_dates": source["publication_dates"],
            "doi": source["doi"],
            "arxiv_id": source["arxiv_id"],
            "public_fulltext_url": local["public_fulltext_url"],
            "local_review_pdf": local["local_review_pdf"],
            "local_extracted_text": local["local_extracted_text"],
        }
        first_rows.append({
            **base,
            "eligibility_decision": "include_study_level",
            **FIRST_CODER[discovery_id],
            "decision_note": "Independent first-coder assessment under the unified codebook after expanded full-text review.",
            "row_status": "complete",
        })
        blind = {field: "" for field in BLIND_FIELDS}
        blind.update(base)
        blind_rows.append(blind)

    write_rows(FIRST_OUT, BASE_FIELDS + CODE_FIELDS, first_rows)
    if SECOND_OUT.exists():
        with SECOND_OUT.open(encoding="utf-8-sig", newline="") as handle:
            existing = list(csv.DictReader(handle))
        if any(row.get("row_status") or row.get("eligibility_decision") for row in existing):
            raise SystemExit(f"Refusing to overwrite coder-entered late addendum: {SECOND_OUT}")
    write_rows(SECOND_OUT, BLIND_FIELDS, blind_rows)
    print(f"WROTE_FIRST={len(first_rows)} {FIRST_OUT}")
    print(f"WROTE_BLIND={len(blind_rows)} {SECOND_OUT}")


if __name__ == "__main__":
    main()
