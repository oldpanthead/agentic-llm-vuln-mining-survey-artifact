#!/usr/bin/env python3
"""Prepare the final pending independent-coder batch for the July 30 search."""

from __future__ import annotations

import csv
from pathlib import Path

from prepare_final_multisource_second_coder_late_addendum_20260730 import (
    BASE_FIELDS,
    BLIND_FIELDS,
    CODE_FIELDS,
    FIRST_CODER as EARLIER_FIRST_CODER,
)


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
ACCESS = DATA / "final_multisource_search_20260730_fulltext_access.csv"
SCREENING = DATA / "final_multisource_search_20260730_screening_audit.csv"
EVIDENCE = DATA / "final_multisource_search_20260730_fulltext_evidence.csv"
FIRST_OUT = DATA / "final_multisource_search_20260730_first_coder_remaining.csv"
SECOND_OUT = DATA / "final_multisource_search_20260730_second_coder_remaining_blind.csv"

NEW_IDS = [
    "FMS0120", "FMS0219", "FMS0347", "FMS0412", "FMS0443", "FMS0488",
    "FMS0558", "FMS0614", "FMS0659", "FMS0742", "FMS0752", "FMS0775",
    "FMS0782", "FMS0800", "FMS0913", "FMS0916", "FMS0961", "FMS1041",
    "FMS1076", "FMS1081", "FMS1155", "FMS1228", "FMS1233", "FMS1265",
    "FMS1283", "FMS1334", "FMS1530", "FMS1592",
]

NEW_FIRST_CODER = {
    "FMS0120": {
        "eligibility_reason": "A clue detector, on-demand code-property-graph slicing, verifier agent, and audit agent form a hypothesis-directed repository-analysis loop.",
        "final_lifecycle_coverage": "candidate analysis;reporting and audit",
        "final_cross_stage_capabilities": "context aggregation / rule extraction;tool routing / strategy routing;feedback interpretation / loop adjustment;validation organization / evidence packaging;long-horizon state management",
        "final_primary_system_shape": "candidate-analysis system",
        "final_principal_reported_evidence_output": "candidate judgment",
        "final_external_traceability": "benchmark ground truth / public material",
        "final_claim_boundary": "The material supports repository-grounded vulnerability judgments on PrimeVul after graph slicing and agent review. It does not provide target execution or a replayable trigger for each judgment.",
        "uncertainty_note": "The audit agent checks claims against retrieved traces, not against runtime exploit behavior.",
    },
    "FMS0219": {
        "eligibility_reason": "The black-box arm uses a shared-state Agentic Reasoning Graph with bounded tool execution and proof gates on web-security tasks.",
        "final_lifecycle_coverage": "candidate analysis;path and input exploration;execution observation;reproduction and validation;reporting and audit",
        "final_cross_stage_capabilities": "context aggregation / rule extraction;tool routing / strategy routing;feedback interpretation / loop adjustment;validation organization / evidence packaging;long-horizon state management;governance / human gates / disclosure control",
        "final_primary_system_shape": "long-horizon pentest and CRS agent",
        "final_principal_reported_evidence_output": "controlled task completion",
        "final_external_traceability": "benchmark ground truth / public material",
        "final_claim_boundary": "The material supports bounded web-security task completion under the benchmark's tools and proof gates. It does not establish open-world discovery outside those targets and success conditions.",
        "uncertainty_note": "The principal result is benchmark task completion even when trajectories include exploit evidence.",
    },
    "FMS0347": {
        "eligibility_reason": "Specialized agents recover paths, generate PoCs, validate behavior, propose repairs, and formally check container-escape patches.",
        "final_lifecycle_coverage": "candidate analysis;execution observation;reproduction and validation;patch validation;reporting and audit",
        "final_cross_stage_capabilities": "context aggregation / rule extraction;tool routing / strategy routing;feedback interpretation / loop adjustment;validation organization / evidence packaging;long-horizon state management",
        "final_primary_system_shape": "reproduction-, validation-, and repair-centered agent",
        "final_principal_reported_evidence_output": "reproducible validation",
        "final_external_traceability": "benchmark ground truth / public material",
        "final_claim_boundary": "The material supports reproduced container-escape behaviors and checked repairs in the reported environment. Broader discovery and deployment claims require independent target and environment confirmation.",
        "uncertainty_note": "Formal checks cover the modeled repair properties rather than every deployment behavior.",
    },
    "FMS0412": {
        "eligibility_reason": "Infer or CppCheck findings are returned to the LLM and drive bounded iterative repair of generated programs.",
        "final_lifecycle_coverage": "candidate analysis;patch validation",
        "final_cross_stage_capabilities": "feedback interpretation / loop adjustment;validation organization / evidence packaging;long-horizon state management",
        "final_primary_system_shape": "reproduction-, validation-, and repair-centered agent",
        "final_principal_reported_evidence_output": "reproducible validation",
        "final_external_traceability": "benchmark ground truth / public material",
        "final_claim_boundary": "The material supports analyzer-checked repair of generated benchmark programs within a three-iteration loop. It does not establish exploit-level validation or real-project maintenance outcomes.",
        "uncertainty_note": "Validation is based on static analyzers and benchmark generation rather than vulnerability-specific execution.",
    },
    "FMS0443": {
        "eligibility_reason": "Static-analysis context feeds successive LLM roles, and validator rejection with recommendations triggers another patch-refinement step.",
        "final_lifecycle_coverage": "candidate analysis;patch validation",
        "final_cross_stage_capabilities": "context aggregation / rule extraction;feedback interpretation / loop adjustment;validation organization / evidence packaging;long-horizon state management",
        "final_primary_system_shape": "reproduction-, validation-, and repair-centered agent",
        "final_principal_reported_evidence_output": "reproducible validation",
        "final_external_traceability": "benchmark ground truth / public material",
        "final_claim_boundary": "The material supports smart-contract patches checked by LLM review, compilation, and manual assessment on 48 reported findings. It does not provide executable exploit replay for every repair.",
        "uncertainty_note": "Compilation and manual checks occur after the LLM refinement loop and do not all feed back automatically.",
    },
    "FMS0488": {
        "eligibility_reason": "The benchmark executes LLM agents in sandboxed web applications and judges their multi-step exploit actions against vulnerability-specific success conditions.",
        "final_lifecycle_coverage": "candidate analysis;path and input exploration;execution observation;reproduction and validation",
        "final_cross_stage_capabilities": "tool routing / strategy routing;feedback interpretation / loop adjustment;validation organization / evidence packaging;long-horizon state management",
        "final_primary_system_shape": "long-horizon pentest and CRS agent",
        "final_principal_reported_evidence_output": "controlled task completion",
        "final_external_traceability": "benchmark ground truth / public material",
        "final_claim_boundary": "The material supports exploit-task success within versioned sandbox applications and benchmark oracles. It does not by itself establish open-world discovery or transfer beyond those tasks.",
        "uncertainty_note": "The vulnerabilities are supplied benchmark targets rather than system-originated discoveries.",
    },
    "FMS0558": {
        "eligibility_reason": "A planning agent forms hypotheses and directs a separate explorer agent to retrieve repository context on demand.",
        "final_lifecycle_coverage": "candidate analysis",
        "final_cross_stage_capabilities": "context aggregation / rule extraction;tool routing / strategy routing;feedback interpretation / loop adjustment;long-horizon state management",
        "final_primary_system_shape": "candidate-analysis system",
        "final_principal_reported_evidence_output": "candidate judgment",
        "final_external_traceability": "benchmark ground truth / public material",
        "final_claim_boundary": "The material supports repository-level vulnerability judgments on validated vulnerability-fix pairs after agent-directed context acquisition. It does not supply execution-based validation of exploitability.",
        "uncertainty_note": "Validated pairs provide benchmark provenance, not new externally confirmed findings.",
    },
    "FMS0614": {
        "eligibility_reason": "Repository-aware CLI agents inspect isolated plugin workspaces and produce vulnerability reports after agent-selected code exploration.",
        "final_lifecycle_coverage": "candidate analysis;reporting and audit",
        "final_cross_stage_capabilities": "context aggregation / rule extraction;tool routing / strategy routing;feedback interpretation / loop adjustment;long-horizon state management",
        "final_primary_system_shape": "candidate-analysis system",
        "final_principal_reported_evidence_output": "candidate judgment",
        "final_external_traceability": "benchmark ground truth / public material",
        "final_claim_boundary": "The material supports report-level vulnerability findings produced by repository-aware agents in the evaluated workspaces. It does not establish executable validation for each finding.",
        "uncertainty_note": "Repeated runs assess reporting behavior rather than item-level external disclosure outcomes.",
    },
    "FMS0659": {
        "eligibility_reason": "Agent-selected repository context, patch generation, oracle execution, and iteration feedback revise later OSS-Fuzz repair attempts.",
        "final_lifecycle_coverage": "candidate analysis;execution observation;patch validation",
        "final_cross_stage_capabilities": "context aggregation / rule extraction;tool routing / strategy routing;feedback interpretation / loop adjustment;validation organization / evidence packaging;long-horizon state management;failure reuse / strategy update",
        "final_primary_system_shape": "reproduction-, validation-, and repair-centered agent",
        "final_principal_reported_evidence_output": "reproducible validation",
        "final_external_traceability": "benchmark ground truth / public material",
        "final_claim_boundary": "The material supports agent-generated patches checked against OSS-Fuzz exploit and build oracles in the reported projects. It does not establish downstream maintainer acceptance for every validated patch.",
        "uncertainty_note": "OSS-Fuzz cases provide public provenance; acceptance and deployment are separate outcomes.",
    },
    "FMS0742": {
        "eligibility_reason": "CodeQL findings and LLM explanations are returned as structured feedback for later secure-code repair.",
        "final_lifecycle_coverage": "candidate analysis;patch validation",
        "final_cross_stage_capabilities": "context aggregation / rule extraction;feedback interpretation / loop adjustment;validation organization / evidence packaging;long-horizon state management",
        "final_primary_system_shape": "reproduction-, validation-, and repair-centered agent",
        "final_principal_reported_evidence_output": "reproducible validation",
        "final_external_traceability": "benchmark ground truth / public material",
        "final_claim_boundary": "The material supports iterative repair when revised code passes the reported CodeQL and functional checks. It does not establish exploit replay or independent confirmation of real-world fixes.",
        "uncertainty_note": "Scanner acceptance is the main security oracle.",
    },
    "FMS0752": {
        "eligibility_reason": "HarnessAgent routes source retrieval, compilation, repair, and validation tools, with build and validation failures changing later harness actions.",
        "final_lifecycle_coverage": "path and input exploration;execution observation;reproduction and validation",
        "final_cross_stage_capabilities": "context aggregation / rule extraction;tool routing / strategy routing;feedback interpretation / loop adjustment;validation organization / evidence packaging;long-horizon state management;failure reuse / strategy update",
        "final_primary_system_shape": "feedback-driven fuzzing agent",
        "final_principal_reported_evidence_output": "controlled task completion",
        "final_external_traceability": "benchmark ground truth / public material",
        "final_claim_boundary": "The material supports compiling, validated fuzz harnesses and measured coverage gains on OSS-Fuzz targets. Harness success and coverage do not alone establish confirmed vulnerabilities.",
        "uncertainty_note": "The principal outcome is harness construction rather than vulnerability confirmation.",
    },
    "FMS0775": {
        "eligibility_reason": "The study directly runs autonomous repair agents and evaluates their repository patches with security and functionality checks.",
        "final_lifecycle_coverage": "candidate analysis;execution observation;patch validation",
        "final_cross_stage_capabilities": "context aggregation / rule extraction;tool routing / strategy routing;feedback interpretation / loop adjustment;validation organization / evidence packaging;long-horizon state management",
        "final_primary_system_shape": "reproduction-, validation-, and repair-centered agent",
        "final_principal_reported_evidence_output": "reproducible validation",
        "final_external_traceability": "benchmark ground truth / public material",
        "final_claim_boundary": "The material supports security and functionality outcomes for agent-produced patches in the reported benchmark environments. It does not establish maintenance or deployment of those patches.",
        "uncertainty_note": "The study evaluates existing agents rather than introducing one uniform repair architecture.",
    },
    "FMS0782": {
        "eligibility_reason": "The secure-code agent repeatedly runs Bandit, returns findings to the LLM, and repairs code until the security condition or iteration limit is reached.",
        "final_lifecycle_coverage": "candidate analysis;patch validation",
        "final_cross_stage_capabilities": "feedback interpretation / loop adjustment;validation organization / evidence packaging;long-horizon state management",
        "final_primary_system_shape": "reproduction-, validation-, and repair-centered agent",
        "final_principal_reported_evidence_output": "reproducible validation",
        "final_external_traceability": "benchmark ground truth / public material",
        "final_claim_boundary": "The material supports iterative Python-code repair under Bandit and task checks. It does not establish exploit-level validation or performance on unseen deployed projects.",
        "uncertainty_note": "The principal security signal is scanner output.",
    },
    "FMS0800": {
        "eligibility_reason": "Compiler, CodeQL, and KLEE results drive iterative LLM repair, and prior successful repairs are retrieved for later candidates.",
        "final_lifecycle_coverage": "candidate analysis;execution observation;patch validation",
        "final_cross_stage_capabilities": "context aggregation / rule extraction;tool routing / strategy routing;feedback interpretation / loop adjustment;validation organization / evidence packaging;long-horizon state management;failure reuse / strategy update",
        "final_primary_system_shape": "reproduction-, validation-, and repair-centered agent",
        "final_principal_reported_evidence_output": "reproducible validation",
        "final_external_traceability": "benchmark ground truth / public material",
        "final_claim_boundary": "The material supports repaired programs checked by compilation, CodeQL, and symbolic execution in the reported tasks. It does not establish maintainer acceptance or deployment outcomes.",
        "uncertainty_note": "Different tools validate different properties and should not be treated as interchangeable oracles.",
    },
    "FMS0913": {
        "eligibility_reason": "The study executes project-scale LLM and agent-centric detectors, including iterative repository exploration and shell-mediated analysis.",
        "final_lifecycle_coverage": "candidate analysis;reporting and audit",
        "final_cross_stage_capabilities": "context aggregation / rule extraction;tool routing / strategy routing;feedback interpretation / loop adjustment;long-horizon state management",
        "final_primary_system_shape": "candidate-analysis system",
        "final_principal_reported_evidence_output": "candidate judgment",
        "final_external_traceability": "benchmark ground truth / public material",
        "final_claim_boundary": "The material supports project-scale vulnerability judgments and resource measurements on the study corpus. It does not provide runtime validation for every reported candidate.",
        "uncertainty_note": "The paper compares heterogeneous detector interfaces rather than one common execution oracle.",
    },
    "FMS0916": {
        "eligibility_reason": "Semgrep findings enter an LLM triage and PoC-generation workflow, so candidate decisions determine later validation actions.",
        "final_lifecycle_coverage": "candidate analysis;execution observation;reproduction and validation;reporting and audit",
        "final_cross_stage_capabilities": "context aggregation / rule extraction;tool routing / strategy routing;feedback interpretation / loop adjustment;validation organization / evidence packaging",
        "final_primary_system_shape": "reproduction-, validation-, and repair-centered agent",
        "final_principal_reported_evidence_output": "reproducible validation",
        "final_external_traceability": "benchmark ground truth / public material",
        "final_claim_boundary": "The material supports triaged findings with generated PoC material in the reported SAST workflow. Stronger discovery claims require item-level execution and external alignment for each finding.",
        "uncertainty_note": "PoC generation and successful replay must remain distinct when the paper reports them separately.",
    },
    "FMS0961": {
        "eligibility_reason": "Tool-using agents execute multi-step actions in Docker sandboxes across controlled prompt conditions and vulnerability-exploitation tasks.",
        "final_lifecycle_coverage": "candidate analysis;path and input exploration;execution observation;reproduction and validation",
        "final_cross_stage_capabilities": "tool routing / strategy routing;feedback interpretation / loop adjustment;long-horizon state management;governance / human gates / disclosure control",
        "final_primary_system_shape": "long-horizon pentest and CRS agent",
        "final_principal_reported_evidence_output": "controlled task completion",
        "final_external_traceability": "benchmark ground truth / public material",
        "final_claim_boundary": "The material supports prompt-conditioned exploitation rates for planted vulnerabilities in controlled Docker tasks. It does not establish discovery prevalence or behavior on open-world targets.",
        "uncertainty_note": "The study evaluates agent safety behavior rather than introducing a vulnerability-mining architecture.",
    },
    "FMS1041": {
        "eligibility_reason": "GUI agents explore Android applications, observe network behavior, and expose TLS-validation failures before downstream attribution.",
        "final_lifecycle_coverage": "path and input exploration;execution observation;reproduction and validation",
        "final_cross_stage_capabilities": "tool routing / strategy routing;feedback interpretation / loop adjustment;validation organization / evidence packaging;long-horizon state management",
        "final_primary_system_shape": "feedback-driven fuzzing agent",
        "final_principal_reported_evidence_output": "runtime safety signal",
        "final_external_traceability": "benchmark ground truth / public material",
        "final_claim_boundary": "The material supports observed TLS validation failures reached through agent-driven GUI exploration in the evaluated apps. Vulnerability attribution and broader exploitability require the downstream analysis described by the study.",
        "uncertainty_note": "The runtime signal precedes causal attribution.",
    },
    "FMS1076": {
        "eligibility_reason": "PatchEval executes code and repair agents on CVE tasks and validates their patches with security and functionality tests in sandboxes.",
        "final_lifecycle_coverage": "execution observation;patch validation",
        "final_cross_stage_capabilities": "tool routing / strategy routing;feedback interpretation / loop adjustment;validation organization / evidence packaging;long-horizon state management",
        "final_primary_system_shape": "reproduction-, validation-, and repair-centered agent",
        "final_principal_reported_evidence_output": "reproducible validation",
        "final_external_traceability": "benchmark ground truth / public material",
        "final_claim_boundary": "The material supports patch outcomes under benchmark-specific security and functionality tests in runtime sandboxes. It does not establish that passing patches are maintained or deployed upstream.",
        "uncertainty_note": "The benchmark evaluates agents and is not itself a single repair policy.",
    },
    "FMS1081": {
        "eligibility_reason": "Pen-Strategist converts strategies into tool actions, integrates with pentesting frameworks and MCP tools, and records iterative outcomes on vulnerable machines.",
        "final_lifecycle_coverage": "candidate analysis;path and input exploration;execution observation;reporting and audit",
        "final_cross_stage_capabilities": "context aggregation / rule extraction;tool routing / strategy routing;feedback interpretation / loop adjustment;long-horizon state management",
        "final_primary_system_shape": "long-horizon pentest and CRS agent",
        "final_principal_reported_evidence_output": "controlled task completion",
        "final_external_traceability": "benchmark ground truth / public material",
        "final_claim_boundary": "The material supports improved strategy and subtask completion in the reported vulnerable-machine and CTF settings. It does not establish open-world vulnerability discovery or independent disclosure outcomes.",
        "uncertainty_note": "Strategy-model gains and end-to-end exploit success are distinct evaluation objects.",
    },
    "FMS1155": {
        "eligibility_reason": "General-purpose LLM scanners run in tool-using agent mode with iterative repository exploration and shell-mediated analysis.",
        "final_lifecycle_coverage": "candidate analysis;reporting and audit",
        "final_cross_stage_capabilities": "context aggregation / rule extraction;tool routing / strategy routing;feedback interpretation / loop adjustment;long-horizon state management",
        "final_primary_system_shape": "candidate-analysis system",
        "final_principal_reported_evidence_output": "candidate judgment",
        "final_external_traceability": "benchmark ground truth / public material",
        "final_claim_boundary": "The material supports scanner findings on the study's real-world code corpus under the evaluated agent mode. It does not provide reproducible execution evidence for every candidate.",
        "uncertainty_note": "Rule-based and agentic scanners expose different result formats and search behavior.",
    },
    "FMS1228": {
        "eligibility_reason": "Tests, static analysis, and anchor checks gate every candidate; structured failures are retained and passed into later implementation attempts.",
        "final_lifecycle_coverage": "candidate analysis;execution observation;patch validation",
        "final_cross_stage_capabilities": "context aggregation / rule extraction;tool routing / strategy routing;feedback interpretation / loop adjustment;validation organization / evidence packaging;long-horizon state management;failure reuse / strategy update",
        "final_primary_system_shape": "reproduction-, validation-, and repair-centered agent",
        "final_principal_reported_evidence_output": "reproducible validation",
        "final_external_traceability": "benchmark ground truth / public material",
        "final_claim_boundary": "The material supports bounded iterative refinement under tests, static analysis, and anchor-integrity checks. It does not establish formal correctness or security beyond those gates.",
        "uncertainty_note": "The CEGIS analogy is operational; the verifier is not a complete formal specification.",
    },
    "FMS1233": {
        "eligibility_reason": "SCGAgent selects security guidance, generates tests, and iteratively revises code while retaining functional and security state.",
        "final_lifecycle_coverage": "candidate analysis;execution observation;patch validation",
        "final_cross_stage_capabilities": "context aggregation / rule extraction;tool routing / strategy routing;feedback interpretation / loop adjustment;validation organization / evidence packaging;long-horizon state management",
        "final_primary_system_shape": "reproduction-, validation-, and repair-centered agent",
        "final_principal_reported_evidence_output": "reproducible validation",
        "final_external_traceability": "benchmark ground truth / public material",
        "final_claim_boundary": "The material supports generated or revised code under the reported functional and security tests. It does not establish vulnerability freedom outside those tests and tasks.",
        "uncertainty_note": "Passing generated tests is narrower than complete security validation.",
    },
    "FMS1265": {
        "eligibility_reason": "Repository-editing agents are executed and their patches are checked with functionality tests, PoCs, SAST, and dynamic security oracles.",
        "final_lifecycle_coverage": "candidate analysis;path and input exploration;execution observation;reproduction and validation;patch validation",
        "final_cross_stage_capabilities": "context aggregation / rule extraction;tool routing / strategy routing;feedback interpretation / loop adjustment;validation organization / evidence packaging;long-horizon state management",
        "final_primary_system_shape": "long-horizon pentest and CRS agent",
        "final_principal_reported_evidence_output": "controlled task completion",
        "final_external_traceability": "benchmark ground truth / public material",
        "final_claim_boundary": "The material supports secure-code-agent task outcomes under reconstructed vulnerability scenarios and multiple benchmark oracles. It does not establish general secure-coding capability beyond those scenarios.",
        "uncertainty_note": "Different scenario oracles contribute to task success and should not be collapsed into one exploit measure.",
    },
    "FMS1283": {
        "eligibility_reason": "A teacher-verifier-student loop revises semantic lifting before graph-based global supply-chain vulnerability reasoning.",
        "final_lifecycle_coverage": "candidate analysis;reporting and audit",
        "final_cross_stage_capabilities": "context aggregation / rule extraction;feedback interpretation / loop adjustment;validation organization / evidence packaging;long-horizon state management",
        "final_primary_system_shape": "candidate-analysis system",
        "final_principal_reported_evidence_output": "candidate judgment",
        "final_external_traceability": "benchmark ground truth / public material",
        "final_claim_boundary": "The material supports candidate supply-chain vulnerability judgments after verifier-guided semantic reconstruction. It does not provide runtime reproduction of each reported dependency behavior.",
        "uncertainty_note": "Verification concerns semantic lifting and graph consistency rather than target execution.",
    },
    "FMS1334": {
        "eligibility_reason": "LLM-assisted execution-context reconstruction and test synthesis are followed by execution and timing-growth interpretation for complexity vulnerabilities.",
        "final_lifecycle_coverage": "candidate analysis;path and input exploration;execution observation;reproduction and validation",
        "final_cross_stage_capabilities": "context aggregation / rule extraction;tool routing / strategy routing;feedback interpretation / loop adjustment;validation organization / evidence packaging",
        "final_primary_system_shape": "reproduction-, validation-, and repair-centered agent",
        "final_principal_reported_evidence_output": "reproducible validation",
        "final_external_traceability": "benchmark ground truth / public material",
        "final_claim_boundary": "The material supports complexity-vulnerability validation through generated contexts, inputs, and measured timing growth in the reported environment. It does not establish impact outside those workloads and thresholds.",
        "uncertainty_note": "Timing growth is an execution-based oracle whose interpretation depends on the study threshold.",
    },
    "FMS1530": {
        "eligibility_reason": "Generation, vulnerability review, and refinement are assigned to successive LLM roles so earlier findings alter the retained code.",
        "final_lifecycle_coverage": "candidate analysis;patch validation",
        "final_cross_stage_capabilities": "context aggregation / rule extraction;feedback interpretation / loop adjustment;validation organization / evidence packaging;long-horizon state management",
        "final_primary_system_shape": "reproduction-, validation-, and repair-centered agent",
        "final_principal_reported_evidence_output": "controlled task completion",
        "final_external_traceability": "benchmark ground truth / public material",
        "final_claim_boundary": "The material supports secure-code-generation task outcomes after role-based review and refinement. It does not establish exploit-level validation or security outside the evaluated Scala tasks.",
        "uncertainty_note": "The principal outcome is task completion and review rather than a replayable vulnerability trigger.",
    },
    "FMS1592": {
        "eligibility_reason": "Reachability results and vulnerability context are converted into unit tests that are executed to verify third-party-library triggerability.",
        "final_lifecycle_coverage": "candidate analysis;execution observation;reproduction and validation",
        "final_cross_stage_capabilities": "context aggregation / rule extraction;tool routing / strategy routing;validation organization / evidence packaging",
        "final_primary_system_shape": "reproduction-, validation-, and repair-centered agent",
        "final_principal_reported_evidence_output": "reproducible validation",
        "final_external_traceability": "benchmark ground truth / public material",
        "final_claim_boundary": "The material supports executable tests showing whether known third-party-library vulnerabilities are triggerable in the evaluated applications. It does not establish discovery of previously unknown vulnerabilities.",
        "uncertainty_note": "Known vulnerability records provide the starting hypothesis and benchmark provenance.",
    },
}


def read_index(path: Path) -> dict[str, dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return {row["discovery_id"]: row for row in csv.DictReader(handle)}


def write_rows(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def material_checked(discovery_id: str, evidence: dict[str, dict[str, str]]) -> str:
    row = evidence[discovery_id]
    pages = []
    for field in (
        "agent_or_llm_role_page",
        "tool_or_execution_action_page",
        "feedback_or_state_transition_page",
        "validation_or_replay_page",
        "evaluation_result_page",
    ):
        page = (row.get(field) or "").strip()
        if page and page not in pages:
            pages.append(page)
    return "Public full text and extracted mechanism/evaluation locations: " + (
        ", ".join(f"p. {page}" for page in pages) if pages else "title, method, and evaluation sections"
    )


def main() -> None:
    decisions = {**EARLIER_FIRST_CODER, **NEW_FIRST_CODER}
    ordered_ids = list(EARLIER_FIRST_CODER) + NEW_IDS
    if len(ordered_ids) != 41 or len(set(ordered_ids)) != 41:
        raise SystemExit("ERROR expected 41 unique remaining records")
    if set(ordered_ids) != set(decisions):
        raise SystemExit("ERROR first-coder decisions do not match remaining IDs")

    access = read_index(ACCESS)
    screening = read_index(SCREENING)
    evidence = read_index(EVIDENCE)
    first_rows = []
    blind_rows = []
    for order, discovery_id in enumerate(ordered_ids, start=96):
        source = screening[discovery_id]
        local = access[discovery_id]
        if local["access_status"] != "downloaded_and_text_extracted":
            raise SystemExit(f"ERROR no extracted full text for {discovery_id}")
        base = {
            "review_order": str(order),
            "discovery_id": discovery_id,
            "title": source["title"],
            "publication_dates": source["publication_dates"],
            "doi": source["doi"],
            "arxiv_id": source["arxiv_id"],
            "public_fulltext_url": local["public_fulltext_url"],
            "local_review_pdf": local["local_review_pdf"],
            "local_extracted_text": local["local_extracted_text"],
        }
        decision = dict(decisions[discovery_id])
        decision.setdefault("material_checked", material_checked(discovery_id, evidence))
        first_rows.append({
            **base,
            "eligibility_decision": "include_study_level",
            **decision,
            "decision_note": "Independent first-coder assessment under the unified codebook after final multi-source full-text review.",
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
            raise SystemExit(f"Refusing to overwrite coder-entered results: {SECOND_OUT}")
    write_rows(SECOND_OUT, BLIND_FIELDS, blind_rows)
    print(f"WROTE_FIRST={len(first_rows)} {FIRST_OUT}")
    print(f"WROTE_BLIND={len(blind_rows)} {SECOND_OUT}")


if __name__ == "__main__":
    main()
