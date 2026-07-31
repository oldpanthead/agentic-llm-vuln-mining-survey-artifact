#!/usr/bin/env python3
"""Prepare the nine-record addendum discovered after full-text retrieval repair.

The first-coder file and blind second-coder file are deliberately separate.
Running this script never alters the completed 86-record coding pass.
"""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
ACCESS = DATA / "final_multisource_search_20260730_fulltext_access.csv"
SCREENING = DATA / "final_multisource_search_20260730_screening_audit.csv"
FIRST_OUT = DATA / "final_multisource_search_20260730_first_coder_addendum.csv"
SECOND_OUT = DATA / "final_multisource_search_20260730_second_coder_addendum_blind.csv"

ADDENDUM_IDS = [
    "FMS0206",
    "FMS0258",
    "FMS0494",
    "FMS0651",
    "FMS0968",
    "FMS1299",
    "FMS1316",
    "FMS1571",
    "FMS1573",
]

FIRST_CODER = {
    "FMS0206": {
        "eligibility_reason": "LLM agents synthesize and refine detectors from verifier feedback, generate executable PoV/PoE artifacts, and revise failed proofs before deterministic oracle checks.",
        "final_lifecycle_coverage": "candidate analysis;path and input exploration;execution observation;reproduction and validation;reporting and audit",
        "final_cross_stage_capabilities": "context aggregation / rule extraction;tool routing / strategy routing;feedback interpretation / loop adjustment;validation organization / evidence packaging;long-horizon state management;failure reuse / strategy update;governance / human gates / disclosure control",
        "final_primary_system_shape": "reproduction-, validation-, and repair-centered agent",
        "final_principal_reported_evidence_output": "reproducible validation",
        "final_external_traceability": "author-reported external clue",
        "final_claim_boundary": "The material supports executable PoV and proof-of-exploitability validation under the reported target configurations and deterministic oracles. The reported zero-day and CVE outcomes require public item-level alignment before they support externally traceable discovery claims.",
        "material_checked": "Public full text: Fig. 3; Sections 3.1-3.3; Algorithm 1; Section 5 and Table 4; ethics discussion.",
        "uncertainty_note": "Twelve CVE assignments are reported in aggregate, without public item-level links for the disclosed findings in the reviewed paper.",
    },
    "FMS0258": {
        "eligibility_reason": "STITCH agents configure builds, refine specifications from compilation and test feedback, triage crashes, and produce minimized reproducers and reports.",
        "final_lifecycle_coverage": "candidate analysis;path and input exploration;execution observation;reproduction and validation;patch validation;reporting and audit",
        "final_cross_stage_capabilities": "context aggregation / rule extraction;tool routing / strategy routing;feedback interpretation / loop adjustment;validation organization / evidence packaging;long-horizon state management;failure reuse / strategy update;governance / human gates / disclosure control",
        "final_primary_system_shape": "feedback-driven fuzzing agent",
        "final_principal_reported_evidence_output": "externally traceable material",
        "final_external_traceability": "publicly aligned external trace",
        "final_claim_boundary": "The material supports reproducible crash findings and, for linked reports, item-level alignment with public issue or maintainer records. This alignment does not automatically extend to every aggregate bug count reported by the study.",
        "material_checked": "Public full text: Sections 4.1-4.5 and Fig. 5; Section 5; real-world results and Table 4; Sections 13-14.",
        "uncertainty_note": "Public traceability applies to the issue-linked subset; some security-sensitive report links remain anonymized for review.",
    },
    "FMS0494": {
        "eligibility_reason": "Evaluated coding agents select and invoke on-chain tools in a call/result loop, generate exploits and patches, and receive deterministic task feedback on historical forks.",
        "final_lifecycle_coverage": "candidate analysis;path and input exploration;execution observation;reproduction and validation;patch validation",
        "final_cross_stage_capabilities": "context aggregation / rule extraction;tool routing / strategy routing;feedback interpretation / loop adjustment;validation organization / evidence packaging;long-horizon state management;governance / human gates / disclosure control",
        "final_primary_system_shape": "long-horizon pentest and CRS agent",
        "final_principal_reported_evidence_output": "reproducible validation",
        "final_external_traceability": "benchmark ground truth / public material",
        "final_claim_boundary": "The material supports detection, exploit, and patch outcomes on block-anchored historical-fork tasks with deterministic economic and fail-to-pass oracles. It does not establish independent discovery of the historical incidents used as benchmark ground truth.",
        "material_checked": "Public full text: Sections 3.1-3.3 and Fig. 3; Sections 4.1-4.3; exploit and patch scoring definitions.",
        "uncertainty_note": "The paper is a benchmark study of agent configurations rather than a single new agent policy.",
    },
    "FMS0651": {
        "eligibility_reason": "A ReAct-based agent iteratively navigates repository context with specialized tools and uses observations to assess causal alignment between a CVE and candidate fix commits.",
        "final_lifecycle_coverage": "candidate analysis;reporting and audit",
        "final_cross_stage_capabilities": "context aggregation / rule extraction;tool routing / strategy routing;feedback interpretation / loop adjustment;long-horizon state management",
        "final_primary_system_shape": "candidate-analysis system",
        "final_principal_reported_evidence_output": "candidate judgment",
        "final_external_traceability": "benchmark ground truth / public material",
        "final_claim_boundary": "The material supports ranking and classifying vulnerability-fixing commits against CVE-linked benchmark records. It does not provide execution evidence that independently validates exploitability or patch correctness.",
        "material_checked": "Public full text: Section 4, especially Sections 4.1-4.2.2; Sections 5-6 and CVEVC evaluation.",
        "uncertainty_note": "The external CVE and commit records supply evaluation ground truth rather than independent system-originated vulnerability discovery.",
    },
    "FMS0968": {
        "eligibility_reason": "Planner, executor, verifier, and experience components repeatedly generate strategies, execute repository actions, validate PoCs, and update stored strategy from prior outcomes.",
        "final_lifecycle_coverage": "path and input exploration;execution observation;reproduction and validation;patch validation",
        "final_cross_stage_capabilities": "context aggregation / rule extraction;tool routing / strategy routing;feedback interpretation / loop adjustment;validation organization / evidence packaging;long-horizon state management;failure reuse / strategy update",
        "final_primary_system_shape": "reproduction-, validation-, and repair-centered agent",
        "final_principal_reported_evidence_output": "reproducible validation",
        "final_external_traceability": "benchmark ground truth / public material",
        "final_claim_boundary": "The material supports repository-scale PoC reproduction and patched-build verification on held-out CyberGym tasks. It does not by itself establish open-world vulnerability discovery or external disclosure outcomes.",
        "material_checked": "Public full text: system overview and policy/experience loops in Fig. 1; method sections; CyberGym evaluation and verifier definition.",
        "uncertainty_note": "",
    },
    "FMS1299": {
        "eligibility_reason": "Planner, Analyzer, Fixer, and Verifier outputs are passed through a CrewAI workflow; one variant exposes CodeQL through MCP and later roles act on earlier LLM-produced state.",
        "final_lifecycle_coverage": "candidate analysis;patch validation;reporting and audit",
        "final_cross_stage_capabilities": "context aggregation / rule extraction;tool routing / strategy routing;validation organization / evidence packaging;long-horizon state management",
        "final_primary_system_shape": "long-horizon pentest and CRS agent",
        "final_principal_reported_evidence_output": "controlled task completion",
        "final_external_traceability": "benchmark ground truth / public material",
        "final_claim_boundary": "The material supports stage-wise detection, patch-generation, and semantic verification outcomes on 25 curated CVE tasks. Because patch assessment is rubric-based rather than an executable fail-to-pass check, it does not establish reproducible patch validation.",
        "material_checked": "Public full text: Sections 3.1-3.5, especially role workflow and evaluation; Section 4 results and Table 4.",
        "uncertainty_note": "The Planner is static and the CodeQL tool is available only in one workflow variant; long-horizon is assigned because role coordination is the evaluated contribution.",
    },
    "FMS1316": {
        "eligibility_reason": "Agents query a code knowledge base, generate seeds, execute them against sanitizer-instrumented binaries, and revise seeds from execution feedback.",
        "final_lifecycle_coverage": "candidate analysis;path and input exploration;execution observation;reproduction and validation;reporting and audit",
        "final_cross_stage_capabilities": "context aggregation / rule extraction;tool routing / strategy routing;feedback interpretation / loop adjustment;validation organization / evidence packaging;long-horizon state management",
        "final_primary_system_shape": "feedback-driven fuzzing agent",
        "final_principal_reported_evidence_output": "reproducible validation",
        "final_external_traceability": "benchmark ground truth / public material",
        "final_claim_boundary": "The material supports sanitizer-checked crashing seeds and repeated trigger results on versioned Magma and ARVO targets. Claims about previously unreachable or zero-day vulnerabilities remain bounded by the reported benchmark or competition setting and public trace material.",
        "material_checked": "Public full text: Sections 4.1-4.3 and Fig. 3; Sections 6.1-6.4; Appendix D-E reproduction material.",
        "uncertainty_note": "The paper includes reproduced analysis and seed-generation material but does not provide a clearly identified standalone public artifact URL in the reviewed version.",
    },
    "FMS1571": {
        "eligibility_reason": "Detection and execution agents plan tool use, parse command outputs, validate success or failure, and adapt retries and subsequent attacks to environmental feedback.",
        "final_lifecycle_coverage": "candidate analysis;path and input exploration;execution observation;reproduction and validation;reporting and audit",
        "final_cross_stage_capabilities": "context aggregation / rule extraction;tool routing / strategy routing;feedback interpretation / loop adjustment;validation organization / evidence packaging;long-horizon state management",
        "final_primary_system_shape": "long-horizon pentest and CRS agent",
        "final_principal_reported_evidence_output": "controlled task completion",
        "final_external_traceability": "benchmark ground truth / public material",
        "final_claim_boundary": "The material supports autonomous reconnaissance and exploit-task completion in IoTGoat and Metasploitable testbeds under ten defined scenarios. It does not establish open-world IoT vulnerability discovery or public item-level disclosure outcomes.",
        "material_checked": "Public full text: Section III, Fig. 1, Algorithm 1, attack-execution feedback sequence, and Section IV results.",
        "uncertainty_note": "",
    },
    "FMS1573": {
        "eligibility_reason": "Static call chains guide an evolutionary prompt fuzzer whose agents execute MCP tools, classify tool-selection and parameter failures, and change later mutations from execution fitness.",
        "final_lifecycle_coverage": "candidate analysis;path and input exploration;execution observation;reproduction and validation;reporting and audit",
        "final_cross_stage_capabilities": "context aggregation / rule extraction;tool routing / strategy routing;feedback interpretation / loop adjustment;validation organization / evidence packaging;long-horizon state management;failure reuse / strategy update;governance / human gates / disclosure control",
        "final_primary_system_shape": "feedback-driven fuzzing agent",
        "final_principal_reported_evidence_output": "reproducible validation",
        "final_external_traceability": "author-reported external clue",
        "final_claim_boundary": "The material supports sandboxed end-to-end PoC traces for taint-style MCP-server vulnerabilities. The aggregate 106 zero-day and 67 CVE statements remain author-reported until specific system outputs can be aligned with public external records.",
        "material_checked": "Public full text: Section IV and Fig. 2; Algorithm 1; Section V evaluation and Table II; responsible-disclosure discussion.",
        "uncertainty_note": "CVE identifiers and affected projects are partly masked or anonymized in the reviewed submission.",
    },
}

BASE_FIELDS = [
    "review_order",
    "discovery_id",
    "title",
    "publication_dates",
    "doi",
    "arxiv_id",
    "public_fulltext_url",
    "local_review_pdf",
    "local_extracted_text",
]
CODE_FIELDS = [
    "eligibility_decision",
    "eligibility_reason",
    "final_lifecycle_coverage",
    "final_cross_stage_capabilities",
    "final_primary_system_shape",
    "final_principal_reported_evidence_output",
    "final_external_traceability",
    "final_claim_boundary",
    "material_checked",
    "decision_note",
    "uncertainty_note",
    "row_status",
]
BLIND_FIELDS = [
    "review_order",
    "discovery_id",
    "title",
    "publication_dates",
    "doi",
    "arxiv_id",
    "public_fulltext_url",
    "local_review_pdf",
    "local_extracted_text",
    "eligibility_decision",
    "eligibility_reason",
    "final_lifecycle_coverage",
    "lifecycle_review_status",
    "final_cross_stage_capabilities",
    "capability_review_status",
    "final_primary_system_shape",
    "shape_review_status",
    "final_principal_reported_evidence_output",
    "evidence_review_status",
    "final_external_traceability",
    "traceability_review_status",
    "final_claim_boundary",
    "claim_boundary_review_status",
    "material_checked",
    "decision_note",
    "uncertainty_note",
    "row_status",
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

    for offset, discovery_id in enumerate(ADDENDUM_IDS, start=87):
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

        coded = {
            **base,
            "eligibility_decision": "include_study_level",
            **FIRST_CODER[discovery_id],
            "decision_note": "Independent first-coder assessment under the same unified codebook as the completed 86-record pass.",
            "row_status": "complete",
        }
        first_rows.append(coded)

        blind = {field: "" for field in BLIND_FIELDS}
        blind.update(base)
        blind_rows.append(blind)

    write_rows(FIRST_OUT, BASE_FIELDS + CODE_FIELDS, first_rows)
    if SECOND_OUT.exists():
        with SECOND_OUT.open(encoding="utf-8-sig", newline="") as handle:
            existing = list(csv.DictReader(handle))
        if any(row.get("row_status") or row.get("eligibility_decision") for row in existing):
            raise SystemExit(f"Refusing to overwrite coder-entered addendum: {SECOND_OUT}")
    write_rows(SECOND_OUT, BLIND_FIELDS, blind_rows)
    print(f"WROTE_FIRST={len(first_rows)} {FIRST_OUT}")
    print(f"WROTE_BLIND={len(blind_rows)} {SECOND_OUT}")


if __name__ == "__main__":
    main()
