#!/usr/bin/env python3
"""Build an adjudicated 199-study matrix after human review is complete."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

from validate_199_adjudication_form import FIELD_RULES, validate


ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
CODING = DATA / "coding"
ADJUDICATION = DATA / "adjudication"
DERIVED = DATA / "derived"

FIELD_MAP = {
    "lifecycle coverage": {
        "comparison_first": "first_lifecycle",
        "comparison_second": "second_lifecycle",
        "matrix": "lifecycle_coverage",
    },
    "cross-stage capability": {
        "comparison_first": "first_capability",
        "comparison_second": "second_capability",
        "matrix": "cross_stage_capabilities",
    },
    "primary system shape": {
        "comparison_first": "first_primary_shape",
        "comparison_second": "second_primary_shape",
        "matrix": "primary_system_shape",
    },
    "principal reported evidence output": {
        "comparison_first": "first_principal_evidence",
        "comparison_second": "second_principal_evidence",
        "matrix": "strongest_evidence_output",
    },
    "external traceability": {
        "comparison_first": "first_external_traceability",
        "comparison_second": "second_external_traceability",
        "matrix": "external_traceability",
    },
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], headers: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def normalized(value: str, field: str) -> str:
    if FIELD_RULES[field]["type"] == "single-label":
        return value.strip()
    selected = {label.strip() for label in value.split(";") if label.strip()}
    return ";".join(label for label in FIELD_RULES[field]["allowed"] if label in selected)


def classify_resolution(first: str, second: str, final: str, field: str) -> str:
    first_normalized = normalized(first, field)
    second_normalized = normalized(second, field)
    if final == first_normalized and final == second_normalized:
        return "agreed_assignment"
    if final == first_normalized:
        return "coder_x_selected"
    if final == second_normalized:
        return "coder_y_selected"
    if final == "unresolved":
        return "unresolved"
    return "third_label_selected"


def count_labels(matrix: list[dict[str, str]], field: str, column: str) -> tuple[Counter[str], int]:
    counts: Counter[str] = Counter()
    unresolved = 0
    for row in matrix:
        value = row[column].strip()
        if value == "unresolved":
            unresolved += 1
            continue
        if FIELD_RULES[field]["type"] == "multi-label":
            counts.update(part.strip() for part in value.split(";") if part.strip())
        elif value:
            counts[value] += 1
    return counts, unresolved


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("adjudication_csv", type=Path)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Optional common output directory. By default, outputs use the repository's coding, adjudication, and derived layers.",
    )
    parser.add_argument(
        "--allow-unresolved",
        action="store_true",
        help="Write a matrix containing unresolved sentinels; affected fields are marked non-reportable.",
    )
    args = parser.parse_args()

    errors, messages = validate(args.adjudication_csv, allow_pending=False)
    for message in messages:
        print(message)
    if errors:
        raise SystemExit("Adjudication form is invalid:\n" + "\n".join(f"- {error}" for error in errors))

    decisions = read_csv(args.adjudication_csv)
    comparison = read_csv(ADJUDICATION / "integrated_199_second_coder_comparison_20260730.csv")
    source_matrix = read_csv(CODING / "current_study_level_coding_matrix_harmonized.csv")
    decisions_by_id = {row["disagreement_id"]: row for row in decisions}
    comparison_by_id = {row["record_id"]: row for row in comparison}
    matrix_by_id: dict[str, dict[str, str]] = {}
    for row in source_matrix:
        matrix_by_id[row["matrix_id"]] = row
        matrix_by_id[row["record_id"]] = row

    final_matrix: list[dict[str, str]] = []
    log_rows: list[dict[str, str]] = []
    unresolved_total = 0
    consumed_decision_ids: set[str] = set()

    for comparison_row in comparison:
        record_id = comparison_row["record_id"]
        source_row = matrix_by_id[record_id]
        final_row = dict(source_row)
        final_row["coding_status"] = "human_third_reviewer_adjudicated"
        final_row["harmonization_status"] = "adjudicated_after_independent_double_coding"
        for field, mapping in FIELD_MAP.items():
            first = comparison_row[mapping["comparison_first"]]
            second = comparison_row[mapping["comparison_second"]]
            if normalized(first, field) == normalized(second, field):
                final = normalized(first, field)
                resolution = "agreed_assignment"
                reason = "Independent assignments agreed; no adjudication was required."
                evidence_location = ""
                unresolved = "no"
                disagreement_id = ""
                reviewer_initials = ""
                review_date = ""
            else:
                disagreement_id = f"{record_id}__{next(key for key, spec in {
                    'lifecycle': 'lifecycle coverage',
                    'capability': 'cross-stage capability',
                    'primary_shape': 'primary system shape',
                    'principal_evidence': 'principal reported evidence output',
                    'external_traceability': 'external traceability',
                }.items() if spec == field)}"
                decision = decisions_by_id[disagreement_id]
                consumed_decision_ids.add(disagreement_id)
                final = decision["human_final_label"].strip()
                if final != "unresolved":
                    final = normalized(final, field)
                resolution = classify_resolution(first, second, final, field)
                reason = decision["brief_reason"].strip()
                evidence_location = decision["evidence_location_verified"].strip()
                unresolved = decision["unresolved"].strip().lower()
                reviewer_initials = decision.get("reviewer_initials", "").strip()
                review_date = decision.get("review_date", "").strip()
            if final == "unresolved":
                unresolved_total += 1
            final_row[mapping["matrix"]] = final
            log_rows.append(
                {
                    "record_id": record_id,
                    "matrix_id": source_row["matrix_id"],
                    "title": comparison_row["title"],
                    "field": field,
                    "coder_x_label": first,
                    "coder_y_label": second,
                    "final_label": final,
                    "resolution_type": resolution,
                    "brief_reason": reason,
                    "evidence_location": evidence_location,
                    "unresolved": unresolved,
                    "reviewer_initials": reviewer_initials,
                    "review_date": review_date,
                    "disagreement_id": disagreement_id,
                }
            )
        final_matrix.append(final_row)

    unused_decision_ids = set(decisions_by_id) - consumed_decision_ids
    if unused_decision_ids:
        raise SystemExit(
            "Adjudication decisions were not consumed by the current comparison: "
            + ", ".join(sorted(unused_decision_ids)[:20])
        )
    if len(consumed_decision_ids) != 410:
        raise SystemExit(f"Expected to consume 410 disagreement decisions, consumed {len(consumed_decision_ids)}")

    if unresolved_total and not args.allow_unresolved:
        raise SystemExit(
            f"Human review contains {unresolved_total} unresolved field decisions. "
            "Resolve them or rerun with --allow-unresolved to produce non-reportable field summaries."
        )

    if args.output_dir is None:
        matrix_path = CODING / "adjudicated_study_level_coding_matrix_199.csv"
        log_path = ADJUDICATION / "adjudication_log_199_all_fields.csv"
        stats_path = DERIVED / "adjudicated_synthesis_statistics_199.csv"
        manifest_path = ADJUDICATION / "adjudication_completion_manifest.json"
    else:
        matrix_path = args.output_dir / "adjudicated_study_level_coding_matrix_199.csv"
        log_path = args.output_dir / "adjudication_log_199_all_fields.csv"
        stats_path = args.output_dir / "adjudicated_synthesis_statistics_199.csv"
        manifest_path = args.output_dir / "adjudication_completion_manifest.json"
    write_csv(matrix_path, final_matrix, list(source_matrix[0]))
    write_csv(log_path, log_rows, list(log_rows[0]))

    statistics: list[dict[str, object]] = []
    field_manifest: dict[str, dict[str, object]] = {}
    for field, mapping in FIELD_MAP.items():
        counts, unresolved = count_labels(final_matrix, field, mapping["matrix"])
        reportable = unresolved == 0
        field_manifest[field] = {
            "unresolved": unresolved,
            "reportable_point_estimate": reportable,
        }
        for label in FIELD_RULES[field]["allowed"]:
            count = counts[label]
            statistics.append(
                {
                    "field": field,
                    "label": label,
                    "count": count if reportable else "",
                    "denominator": 199 if reportable else "",
                    "share": f"{count / 199:.6f}" if reportable else "",
                    "unresolved": unresolved,
                    "reportable_point_estimate": "yes" if reportable else "no",
                }
            )
    write_csv(
        stats_path,
        statistics,
        ["field", "label", "count", "denominator", "share", "unresolved", "reportable_point_estimate"],
    )
    manifest = {
        "source_comparison": "data/adjudication/integrated_199_second_coder_comparison_20260730.csv",
        "source_matrix_preserved": "data/coding/current_study_level_coding_matrix_harmonized.csv",
        "adjudication_form": str(args.adjudication_csv),
        "study_count": len(final_matrix),
        "field_log_rows": len(log_rows),
        "disagreement_rows": len(decisions),
        "unresolved_total": unresolved_total,
        "fields": field_manifest,
        "resolution_types": dict(Counter(row["resolution_type"] for row in log_rows)),
        "outputs": [str(matrix_path), str(log_path), str(stats_path)],
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"ADJUDICATION_FINALIZED studies={len(final_matrix)} disagreements={len(decisions)} unresolved={unresolved_total}")
    print(f"matrix={matrix_path}")
    print(f"log={log_path}")
    print(f"statistics={stats_path}")


if __name__ == "__main__":
    main()
