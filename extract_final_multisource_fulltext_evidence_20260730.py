#!/usr/bin/env python3
"""Extract page-located screening evidence from locally cached candidate PDFs."""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
ACCESS = DATA / "final_multisource_search_20260730_fulltext_access.csv"
OUTPUT = DATA / "final_multisource_search_20260730_fulltext_evidence.csv"

PATTERNS = {
    "agent_or_llm_role": re.compile(
        r"(?:llm|language model|agent).{0,180}(?:select|decid|reason|interpret|"
        r"generat|plan|prioriti|analy|triag)",
        re.IGNORECASE | re.DOTALL,
    ),
    "tool_or_execution_action": re.compile(
        r"(?:invoke|execute|run|call|route|tool|command|fuzzer|symbolic "
        r"execution|static analy).{0,220}",
        re.IGNORECASE | re.DOTALL,
    ),
    "feedback_or_state_transition": re.compile(
        r"(?:feedback|coverage|crash|sanitizer|execution result|tool output|"
        r"state update|memory|iteration|iteratively|self-correction).{0,240}",
        re.IGNORECASE | re.DOTALL,
    ),
    "validation_or_replay": re.compile(
        r"(?:proof.of.vulnerab|\bpov\b|\bpoc\b|replay|reproduc|validat|"
        r"test case|patch test).{0,240}",
        re.IGNORECASE | re.DOTALL,
    ),
    "evaluation_result": re.compile(
        r"(?:we evaluate|evaluation|experiment|our results|results show).{0,260}",
        re.IGNORECASE | re.DOTALL,
    ),
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def compact(value: str) -> str:
    return " ".join(value.split())


def locate(text: str, pattern: re.Pattern[str]) -> tuple[str, str]:
    match = pattern.search(text)
    if not match:
        return "", ""
    page = text.count("\f", 0, match.start()) + 1
    start = max(0, match.start() - 120)
    end = min(len(text), match.end() + 120)
    return str(page), compact(text[start:end])


def main() -> None:
    out: list[dict[str, str]] = []
    for row in read_rows(ACCESS):
        result = {
            "discovery_id": row["discovery_id"],
            "title": row["title"],
            "public_fulltext_url": row["public_fulltext_url"],
            "access_status": row["access_status"],
        }
        text = ""
        if row["local_extracted_text"] and Path(row["local_extracted_text"]).exists():
            text = Path(row["local_extracted_text"]).read_text(
                encoding="utf-8", errors="replace"
            )
        for name, pattern in PATTERNS.items():
            page, snippet = locate(text, pattern)
            result[f"{name}_page"] = page
            result[f"{name}_snippet"] = snippet
            result[f"{name}_hit_count"] = str(len(pattern.findall(text))) if text else "0"
        result["automated_evidence_complete"] = (
            "yes"
            if all(result[f"{name}_snippet"] for name in PATTERNS)
            else "no"
        )
        result["manual_assessment_decision"] = ""
        result["manual_assessment_reason"] = ""
        result["proposed_layer"] = ""
        result["version_relation"] = ""
        result["source_locations_used"] = ""
        out.append(result)

    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(out[0]))
        writer.writeheader()
        writer.writerows(out)
    print(f"WROTE {OUTPUT} ({len(out)} records)")


if __name__ == "__main__":
    main()
