#!/usr/bin/env python3
"""Validate the blind final-search second-coder file without changing it."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DEFAULT_INPUT = ROOT / "data" / "final_multisource_search_20260730_second_coder_blind.csv"

LIFECYCLE = {
    "candidate analysis",
    "path and input exploration",
    "execution observation",
    "reproduction and validation",
    "patch validation",
    "reporting and audit",
}
CAPABILITIES = {
    "context aggregation / rule extraction",
    "tool routing / strategy routing",
    "feedback interpretation / loop adjustment",
    "validation organization / evidence packaging",
    "long-horizon state management",
    "failure reuse / strategy update",
    "governance / human gates / disclosure control",
}
SHAPES = {
    "candidate-analysis system",
    "feedback-driven fuzzing agent",
    "reproduction-, validation-, and repair-centered agent",
    "long-horizon pentest and CRS agent",
}
EVIDENCE = {
    "candidate judgment",
    "controlled task completion",
    "runtime safety signal",
    "reproducible validation",
    "externally traceable material",
}
TRACE = {
    "no external trace reported",
    "benchmark ground truth / public material",
    "author-reported external clue",
    "publicly aligned external trace",
}


def split_labels(value: str) -> set[str]:
    return {item.strip() for item in value.split(";") if item.strip()}


def read_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--require-complete",
        action="store_true",
        help="return an error while any row remains unfinished",
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help="blind-review CSV to validate",
    )
    parser.add_argument(
        "--expected-rows",
        type=int,
        default=86,
        help="expected number of rows in the selected blind-review CSV",
    )
    args = parser.parse_args()

    input_path = args.input.resolve()
    headers, rows = read_rows(input_path)
    problems: list[str] = []
    if len(headers) != len(set(headers)):
        problems.append("duplicate CSV headers")
    if len(rows) != args.expected_rows:
        problems.append(
            f"expected {args.expected_rows} blind-review rows, found {len(rows)}"
        )
    ids = [row.get("discovery_id", "") for row in rows]
    if len(ids) != len(set(ids)) or any(not item for item in ids):
        problems.append("discovery_id values are not unique and complete")
    for row in rows:
        record_id = row.get("discovery_id", "?")
        for field in ("local_review_pdf", "local_extracted_text"):
            value = row.get(field, "").strip()
            if not value or not Path(value).is_file():
                problems.append(f"{record_id}: unavailable {field}")

    completed = 0
    included = 0
    excluded = 0
    pending_ids: list[str] = []
    for row in rows:
        record_id = row.get("discovery_id", "?")
        decision = row.get("eligibility_decision", "").strip()
        status = row.get("row_status", "").strip()
        if status != "complete":
            pending_ids.append(record_id)
            continue
        completed += 1
        if decision == "not_study_level":
            excluded += 1
            if not row.get("eligibility_reason", "").strip():
                problems.append(f"{record_id}: missing exclusion reason")
            continue
        if decision != "include_study_level":
            problems.append(f"{record_id}: invalid eligibility decision {decision!r}")
            continue

        included += 1
        required = (
            "eligibility_reason",
            "final_lifecycle_coverage",
            "final_cross_stage_capabilities",
            "final_primary_system_shape",
            "final_principal_reported_evidence_output",
            "final_external_traceability",
            "final_claim_boundary",
            "material_checked",
        )
        for field in required:
            if not row.get(field, "").strip():
                problems.append(f"{record_id}: missing {field}")
        life = split_labels(row.get("final_lifecycle_coverage", ""))
        caps = split_labels(row.get("final_cross_stage_capabilities", ""))
        if not life or not life <= LIFECYCLE:
            problems.append(f"{record_id}: invalid lifecycle labels {sorted(life - LIFECYCLE)}")
        if not caps or not caps <= CAPABILITIES:
            problems.append(f"{record_id}: invalid capability labels {sorted(caps - CAPABILITIES)}")
        if row.get("final_primary_system_shape", "") not in SHAPES:
            problems.append(f"{record_id}: invalid primary shape")
        if row.get("final_principal_reported_evidence_output", "") not in EVIDENCE:
            problems.append(f"{record_id}: invalid principal evidence output")
        if row.get("final_external_traceability", "") not in TRACE:
            problems.append(f"{record_id}: invalid external traceability")

    print(f"INPUT={input_path}")
    print(f"ROWS={len(rows)} COMPLETE={completed} INCLUDE={included} NOT_STUDY_LEVEL={excluded}")
    print(f"PENDING={len(pending_ids)}")
    if pending_ids:
        print("PENDING_IDS=" + ";".join(pending_ids))
    if problems:
        print("ERRORS=")
        for problem in problems:
            print(f"- {problem}")
        return 1
    if args.require_complete and pending_ids:
        print("ERROR: second-coder review is not complete")
        return 1
    print("STRUCTURE_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
