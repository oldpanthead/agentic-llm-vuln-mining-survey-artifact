"""Refresh study-specific extended-synthesis notes and correct one false-positive row.

The script is intentionally deterministic.  It does not infer results from titles:
the short mechanism summaries below were checked against the public title/abstract
metadata retained in the local Zotero export.  CP189 is a machine-translation study
and is therefore moved from Supporting to Excluded.
"""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"


FOCUS = {
    "CP001": "Combines intra-function and inter-function reference context through collaborating LLM agents for vulnerability candidate reasoning",
    "CP003": "Parallelizes retrieval-augmented smart-contract vulnerability analysis to reduce inference cost while retaining candidate-level reasoning",
    "CP012": "Uses collaborative LLM reasoning to compare and justify smart-contract vulnerability candidates",
    "CP013": "Maps program facts into first-order-logic structures for agent-assisted vulnerability reasoning",
    "CP018": "Compares retrieval augmentation, supervised fine-tuning, and a dual-agent design on code-vulnerability detection",
    "CP027": "Builds a dynamic benchmark for measuring and improving LLM reasoning over static taint-analysis tasks",
    "CP032": "Uses executable delegation and a runtime-grown tree of agents to coordinate firmware-security analysis",
    "CP035": "Applies an LLM to validate and prioritize alerts emitted by static vulnerability analysis",
    "CP042": "Compares machine learning, ChatGPT, and static analysis for Python security findings",
    "CP045": "Uses LLM agents to plan and execute SQL-injection-oriented web penetration-testing steps",
    "CP063": "Combines LLM-guided input mutation with semantic feedback in a hybrid fuzzing loop",
    "CP065": "Generates IoT-protocol fuzzing test cases from protocol context with an LLM",
    "CP067": "Uses a code LLM to generate fuzzing inputs and drivers for industrial-IoT programs",
    "CP069": "Combines static context with runtime feedback to guide greybox fuzzing of structured-input programs",
    "CP079": "Pairs a specialized vulnerability-reasoning model with an agent scaffold for repository analysis",
    "CP086": "Coordinates multiple LLM agents around fuzz-test generation and execution feedback",
    "CP088": "Uses LLM agents to compare protocol behavior across multiple consistency levels",
    "CP090": "Combines multi-agent protocol reverse engineering with deep clustering for industrial-control traffic",
    "CP092": "Uses multi-agent reinforcement learning to adapt industrial-control protocol fuzzing policies",
    "CP093": "Uses protocol-aware multi-agent reinforcement learning for power-IoT fuzzing",
    "CP096": "Uses LLM-derived state and input context to direct fuzzing of stateful web applications",
    "CP098": "Combines LLM-generated protocol knowledge with reinforcement-learning feedback for IoT fuzzing",
    "CP100": "Retrieves API and dependency context from a code knowledge graph for LLM-generated fuzz drivers",
    "CP103": "Evaluates open-source LLMs for zero-shot vulnerability classification in low-level IoT code",
    "CP104": "Uses dense retrieval and specialized agents to provide protocol context for network-protocol fuzzing",
    "CP105": "Extracts an O-RAN behavioral model from specifications with an LLM and uses it for model-based fuzzing",
    "CP107": "Coordinates LLM agents to generate new intrusion-detection rules and repair redundant or conflicting rules",
    "CP108": "Generates and checks protocol-knowledge blueprints for low-altitude AAV networks",
    "CP110": "Transforms directed-fuzzing path constraints into LLM-generated harnesses and reachable inputs",
    "CP111": "Uses LLM reasoning to construct target-aware seeds and mutators for directed fuzzing",
    "CP112": "Fuzzes cross-tool dataflows in LLM-agent workflows to expose composition-level vulnerabilities",
    "CP113": "Generates adversarial smart-contract fuzzing seeds with chain-structured LLM guidance",
    "CP116": "Uses LLM-based constraint solving to generate inputs for hybrid language-processor fuzzing",
    "CP118": "Synthesizes syscall specifications with an LLM to extend kernel-fuzzing coverage",
    "CP119": "Synthesizes executable input generators for low-cost fuzzing of non-textual interfaces",
    "CP122": "Infers option dependencies from source code with an LLM to guide option-aware fuzzing",
    "CP123": "Orchestrates multiple LLM repair agents around failures produced by continuous-fuzzing infrastructure",
    "CP128": "Uses a planning agent and specialist agents to explore and exploit previously unseen real-world vulnerabilities",
    "CP134": "Mimics human program-repair steps in an LLM agent that proposes and checks vulnerability patches",
    "CP135": "Evaluates an autonomous penetration-testing agent with planning and feedback summarization on CTF tasks",
    "CP136": "Uses self-improvement feedback to update a vulnerability-analysis agent across attempts",
    "CP137": "Parses protocol traffic, generates executable Boofuzz scripts, repairs them, and iterates fuzzing through an LLM agent",
    "CP138": "Combines recursive memory and retrieval augmentation in a human-supervised penetration-testing agent",
    "CP139": "Evaluates an autonomous LLM agent on Linux privilege-escalation tasks in a public benchmark environment",
    "CP140": "Uses MCP Security Bench (MSB) to evaluate agent resistance across planning, tool invocation, and response handling",
    "CP141": "Aggregates offensive and defensive cybersecurity tasks into a modular agent meta-benchmark",
    "CP154": "Evaluates ChatGPT across vulnerability prediction, classification, severity estimation, and repair",
    "CP156": "Introduces VulBench to compare LLM vulnerability identification, classification, and localization",
    "CP160": "Surveys how LLMs are used for seed generation, driver generation, mutation, and feedback handling in fuzzing",
    "CP170": "Introduces VulDetectBench to evaluate vulnerability identification, classification, and localization tasks",
    "CP174": "Uses coverage feedback to iteratively prompt an LLM for fuzz-driver generation",
    "CP175": "Combines fine-tuning with LLM agents that produce smart-contract vulnerability decisions and justifications",
    "CP178": "Evaluates ChatGPT and GPT-3 on binary and multi-label code-vulnerability classification",
    "CP187": "Decouples vulnerability reasoning from retrieval, context provision, and prompting in the LLM4Vuln evaluation framework",
    "CP188": "Uses the SecLLMHolmes framework to test security-vulnerability identification and reasoning across controlled code scenarios",
    "CP192": "Uses the Fuzz4All auto-prompting loop to generate diverse inputs for compilers, runtimes, solvers, and libraries",
    "CP195": "Uses source-level compiler context to prompt LLM-generated programs that exercise target optimizations",
    "CP197": "Evaluates open-source LLMs on vulnerability detection, assessment, localization, and related tasks",
    "CP199": "Evaluates large-language-model fuzz-driver generation for correctness, coverage, and characteristic failure modes",
    "CP204": "Evaluates LLM vulnerability detection and patching on 307 Linux-kernel vulnerability cases",
    "CP210": "Combines LLM input reasoning with concolic execution for highly structured test-input generation",
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_rows(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def contextual_reason(row: dict[str, str], focus: str) -> str:
    role = row["primary_synthesis_role"]
    if role == "benchmark_or_evaluation":
        return (
            "Retained for extended synthesis because its audited contribution is an evaluation design or "
            f"benchmark comparison: {focus[0].lower() + focus[1:]}. It is not used as a study-level workflow "
            "trajectory in the lifecycle or system-shape distributions."
        )
    if role == "adjacent_candidate_analysis":
        return (
            f"Retained to contextualize candidate analysis: {focus[0].lower() + focus[1:]}. The record is not "
            "used for the study-level lifecycle distributions because this audit treats its public contribution "
            "as candidate reasoning rather than a fully extracted execution-and-validation trajectory."
        )
    if role == "adjacent_fuzzing_or_testing":
        return (
            f"Retained to contextualize a specific testing mechanism: {focus[0].lower() + focus[1:]}. The present "
            "artifact does not use this record in the full study-level matrix, so its mechanism is synthesized "
            "without adding it to the lifecycle, capability, or evidence-output denominators."
        )
    if role == "agent_orchestration":
        return (
            f"Retained for orchestration context because it {focus[0].lower() + focus[1:]}. Its coordination "
            "mechanism is discussed comparatively, but this record is not used in the full study-level "
            "workflow--capability--evidence distributions."
        )
    return (
        f"Retained for evidence or reproducibility context because it {focus[0].lower() + focus[1:]}. The record "
        "is used to distinguish validation or audit materials and is not added to the study-level distribution "
        "denominators in this artifact release."
    )


def update_extended() -> None:
    path = DATA / "extended_synthesis_audit.csv"
    rows = read_rows(path)
    fields = list(rows[0])
    output: list[dict[str, str]] = []
    for row in rows:
        record_id = row["record_id"]
        if record_id == "CP189":
            continue
        focus = FOCUS.get(record_id)
        if not focus:
            raise SystemExit(f"Missing study-specific extraction for {record_id}")
        row["extracted_contribution"] = focus + "."
        row["reason_not_study_level_coded"] = contextual_reason(row, focus)
        row["reviewer_note"] = (
            "Manually checked against public title/abstract metadata on 2026-07-15. The row records a "
            "study-specific synthesis use; it does not create an additional study-level coding decision."
        )
        output.append(row)
    write_rows(path, output, fields)


def update_record_layer(path: Path, layer_field: str) -> None:
    rows = read_rows(path)
    fields = list(rows[0])
    for row in rows:
        if row.get("record_id") != "CP189":
            continue
        row[layer_field] = "Excluded"
        if "exclusion_reason" in row:
            row["exclusion_reason"] = "Out of scope: machine-translation fine-tuning study with no software-security or vulnerability-mining task"
        if "screening_decision" in row:
            row["screening_decision"] = "excluded_near_neighbor"
        if "note" in row:
            row["note"] = "False-positive keyword/metadata match removed from extended synthesis during the 2026-07-15 audit."
    write_rows(path, rows, fields)


def update_crosswalk() -> None:
    path = DATA / "study_version_crosswalk.csv"
    rows = read_rows(path)
    fields = list(rows[0])
    for row in rows:
        if row["record_id"] == "CP189":
            row["analytical_layer"] = "excluded_near_neighbor"
            row["retained_reason"] = "canonical record retained as an excluded false-positive source match"
            row["notes"] = "Machine-translation study; no vulnerability-mining or software-security task."
    write_rows(path, rows, fields)


def main() -> None:
    update_extended()
    update_record_layer(DATA / "corpus.csv", "corpus_layer")
    update_record_layer(DATA / "source_screening_audit.csv", "corpus_layer")
    update_record_layer(DATA / "corpus_layer_audit.csv", "analysis_layer")
    update_crosswalk()
    print("Updated 61 extended-synthesis rows and reclassified CP189 as Excluded.")


if __name__ == "__main__":
    main()


