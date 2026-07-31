#!/usr/bin/env python3
"""Prepare auditable title/abstract screening recommendations.

Recommendations prioritize records for author review. They are not final
inclusion decisions and never assign a study to an analytical layer.
"""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
INPUT = DATA / "final_multisource_search_20260730_screening_audit.csv"
OUTPUT = DATA / "final_multisource_search_20260730_screening_recommendations.csv"
SUMMARY = DATA / "final_multisource_search_20260730_recommendation_summary.csv"


def rx(pattern: str) -> re.Pattern[str]:
    return re.compile(pattern, re.IGNORECASE)


MODEL = rx(
    r"\bllms?\b|large language model|chatgpt|gpt[- ]?\d|claude|gemini|"
    r"agentic|multi[- ]?agent|language-model"
)
TARGET_TASK = rx(
    r"vulnerab|fuzz|exploit|penetration test|pentest|proof.of.vulnerab|"
    r"\bpov\b|\bpoc\b|security audit|security testing|codeql|taint|"
    r"symbolic execution|vulnerability repair|security patch"
)
AGENT_CONTROL = rx(
    r"agentic|multi[- ]?agent|\bagent\b|autonom|orchestrat|planner|executor|"
    r"tool[- ]?(?:use|call|routing|collaboration)|closed[- ]?loop"
)
EXECUTION_CONTROL = rx(
    r"execution feedback|runtime feedback|tool output|coverage feedback|"
    r"crash feedback|coverage[- ]?guided|feedback[- ]?driven|iterative(?:ly)?|"
    r"replay|proof.of.vulnerab|\bpov\b|exploit execution|dynamic testing|"
    r"validation loop|test feedback|state update|state management|"
    r"command feedback|adaptive policy|self-correction"
)
PENTEST = rx(
    r"penetration test|pentest|offensive security|cyber reasoning|"
    r"capture.the.flag|\bctf\b|ip-to-shell"
)
FUZZING = rx(r"fuzz|harness|seed generation|input generation|mutator")
VALIDATION = rx(
    r"proof.of.vulnerab|\bpov\b|\bpoc\b|vulnerability reproduction|"
    r"vulnerability validation|exploit generation|patch validation"
)
REPAIR = rx(r"vulnerability repair|security patch|patching real.world cve")
ONE_SHOT = rx(
    r"classification|prediction|fine[- ]?tun|prompt engineering|benchmarking "
    r"study|dataset construction|one[- ]?shot|zero[- ]?shot"
)
TARGET_IS_AGENT = rx(
    r"vulnerabilit(?:y|ies) (?:of|in) (?:llm|agent)|security of (?:llm|agent)|"
    r"llm agent security|agent security|prompt injection|jailbreak|"
    r"agent skill|mcp (?:security|tool)|tool[- ]calling agents|"
    r"agentic workflow injection|llm serving systems"
)
NON_SOFTWARE = rx(
    r"clinical|healthcare|medical|complaint events|distribution networks|"
    r"ride-hailing|robot|materials|glaucoma|police incident|music "
    r"recommendation|autonomous driving|world models|misinformation"
)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def recommend(row: dict[str, str]) -> tuple[str, str]:
    prior = row["triage_status"]
    title = row["title"]
    abstract = row["abstract"]
    text = f"{title} {abstract}"

    if prior == "existing_study_or_version":
        return "retain_existing_match", "Exact current-corpus match; reconcile source metadata only."
    if prior == "manual_version_review":
        return "manual_version_review", "Possible alternate title or formal version of a current study."
    if NON_SOFTWARE.search(title):
        return "exclude_title_abstract", "The title identifies a non-software target domain."
    if TARGET_IS_AGENT.search(title):
        return (
            "governance_or_background_review",
            "The target is an LLM/agent system rather than target software.",
        )
    if prior == "background_or_related_review_candidate":
        return "background_review", "Review or survey material."
    if prior == "governance_or_agent_security_candidate":
        return "governance_or_background_review", "Agent-system security or governance context."
    if not MODEL.search(text) or not TARGET_TASK.search(text):
        return "exclude_title_abstract", "No in-scope LLM and target-software security combination."

    # Direct execution-oriented agent workflows receive full-text priority.
    if PENTEST.search(title) and (AGENT_CONTROL.search(text) or EXECUTION_CONTROL.search(text)):
        return "full_text_priority", "Possible agent-controlled penetration-testing trajectory."
    if VALIDATION.search(title) and (
        AGENT_CONTROL.search(text) or EXECUTION_CONTROL.search(text)
    ):
        return "full_text_priority", "Possible reproduction, exploit, or validation loop."
    if FUZZING.search(title):
        if EXECUTION_CONTROL.search(text) or AGENT_CONTROL.search(title):
            return "full_text_priority", "Possible feedback-linked fuzzing or harness workflow."
        return (
            "extended_synthesis_review",
            "LLM-assisted fuzzing/generation is visible, but a feedback transition is not yet established.",
        )
    if REPAIR.search(title):
        if EXECUTION_CONTROL.search(text) or AGENT_CONTROL.search(title):
            return "full_text_priority", "Possible iterative repair or validation workflow."
        return (
            "extended_synthesis_review",
            "Repair is visible, but execution feedback or validation control is not yet established.",
        )
    if AGENT_CONTROL.search(title) and TARGET_TASK.search(title):
        if not abstract:
            return "manual_full_text_needed", "Strong title match, but no abstract was exported."
        if ONE_SHOT.search(title) and not EXECUTION_CONTROL.search(text):
            return "extended_synthesis_review", "Agent/model analysis appears evaluation- or classification-centered."
        return "full_text_priority", "Possible agent-mediated target-software workflow."
    if EXECUTION_CONTROL.search(text) and TARGET_TASK.search(title):
        return "manual_full_text_needed", "Workflow evidence appears in the abstract but is ambiguous at title level."
    if ONE_SHOT.search(text):
        return "extended_synthesis_review", "Visible contribution is model evaluation, classification, or data generation."
    return "manual_title_abstract_review", "In-scope task is plausible, but observable workflow control remains unclear."


def main() -> None:
    rows = read_rows(INPUT)
    out: list[dict[str, str]] = []
    for row in rows:
        rec, reason = recommend(row)
        out.append(
            {
                **row,
                "ai_assisted_screening_recommendation": rec,
                "recommendation_basis": reason,
                "author_final_decision": "",
                "author_final_reason": "",
                "full_text_locator": "",
                "full_text_assessment_note": "",
                "proposed_analytical_layer": "",
                "second_coder_status": (
                    "required_if_study_level_included"
                    if rec in {"full_text_priority", "manual_full_text_needed"}
                    else "not_applicable_unless_reclassified"
                ),
            }
        )

    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(out[0]))
        writer.writeheader()
        writer.writerows(out)

    counts = Counter(row["ai_assisted_screening_recommendation"] for row in out)
    summary = [
        {"metric": "deduplicated_discovery_records", "value": str(len(out))}
    ] + [
        {"metric": f"recommendation_{key}", "value": str(value)}
        for key, value in sorted(counts.items())
    ]
    with SUMMARY.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["metric", "value"])
        writer.writeheader()
        writer.writerows(summary)

    print(f"WROTE {OUTPUT}")
    print(f"WROTE {SUMMARY}")
    for key, value in sorted(counts.items()):
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
