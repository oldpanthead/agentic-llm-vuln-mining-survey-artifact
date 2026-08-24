#!/usr/bin/env python3
"""Integrate OY's external rereview while keeping raw coder/QC layers separate."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Iterable


FIELD_MAP = {
    "lifecycle coverage": "lifecycle_coverage",
    "cross-stage capability": "cross_stage_capabilities",
    "primary system shape": "primary_system_shape",
    "principal reported evidence output": "strongest_evidence_output",
    "external traceability": "external_traceability",
}

FIELD_LABELS = {
    "lifecycle coverage": [
        "candidate analysis", "path and input exploration", "execution observation",
        "reproduction and validation", "patch validation", "reporting and audit",
        "no qualifying label observed",
    ],
    "cross-stage capability": [
        "context aggregation / rule extraction", "tool routing / strategy routing",
        "feedback interpretation / loop adjustment", "validation organization / evidence packaging",
        "long-horizon state management", "failure reuse / strategy update",
        "governance / human gates / disclosure control", "no qualifying label observed",
    ],
    "primary system shape": [
        "candidate-analysis system", "feedback-driven fuzzing agent",
        "reproduction-, validation-, and repair-centered agent", "long-horizon pentest and CRS agent",
    ],
    "principal reported evidence output": [
        "candidate judgment", "controlled task completion", "runtime safety signal",
        "reproducible validation", "externally traceable material",
    ],
    "external traceability": [
        "no external trace reported", "author-reported external clue",
        "benchmark ground truth / public material", "publicly aligned external trace",
    ],
}

FIELD_KEY_MAP = {
    "lifecycle": "lifecycle coverage",
    "capability": "cross-stage capability",
    "primary_shape": "primary system shape",
    "principal_evidence": "principal reported evidence output",
    "external_traceability": "external traceability",
}

CNVD_TASK_ID = "R2-159"
CNVD_FINAL_LABEL = "author-reported external clue"
CNVD_PROVENANCE = (
    "post-adjudication official-record check: "
    "CNVD-2024-16009 not publicly retrievable; retained as author-reported clue"
)


def _canonical_labels(value: str) -> str:
    return ";".join(part.strip() for part in value.split(";") if part.strip())


def _index_by_task(rows: Iterable[dict[str, str]]) -> dict[str, dict[str, str]]:
    indexed = {}
    for row in rows:
        task_id = row.get("task_id") or row.get("r2_task_id")
        if not task_id:
            raise ValueError("review/key row is missing task_id or r2_task_id")
        indexed[task_id] = row
    return indexed


def build_integration_rows(
    template_rows: list[dict[str, str]],
    key_rows: list[dict[str, str]],
    review_rows: list[dict[str, str]],
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    """Return disagreement decisions and independent QC rows.

    The 50 qc_agreement rows are deliberately returned separately. They test
    rule application and must not become adjudication decisions or reliability
    observations.
    """

    template_by_key = {
        (row["record_id"], row["field"]): row for row in template_rows
    }
    key_by_task = _index_by_task(key_rows)
    review_by_task = _index_by_task(review_rows)
    if len(key_by_task) != len(key_rows) or len(review_by_task) != len(review_rows):
        raise ValueError("duplicate task ID in key or OY review export")
    row_types = {row.get("row_type", "") for row in key_rows}
    if row_types - {"disagreement", "qc_agreement"}:
        raise ValueError(f"unknown task row type(s): {sorted(row_types)}")
    decisions: list[dict[str, str]] = []
    qc_rows: list[dict[str, str]] = []
    for task_id, key in key_by_task.items():
        review = review_by_task.get(task_id)
        if review is None:
            raise ValueError(f"missing OY review row: {task_id}")
        field = FIELD_KEY_MAP[key["field_key"]]
        if review.get("case_id") != key.get("case_id"):
            raise ValueError(f"case identity mismatch for {task_id}")
        if review.get("field") != field:
            raise ValueError(f"field mismatch for {task_id}")
        if key.get("study_title") and review.get("study_title") != key.get("study_title"):
            raise ValueError(f"study-title mismatch for {task_id}")
        if review.get("completion_check") != "ready":
            raise ValueError(f"incomplete OY review row: {task_id}")
        if review.get("reviewer_initials") != "OY" or review.get("unresolved") != "no":
            raise ValueError(f"unexpected reviewer or unresolved state for {task_id}")
        template = template_by_key.get((key["internal_record_id"], field))
        if template is None:
            if key["row_type"] != "qc_agreement":
                raise ValueError(
                    f"missing adjudication template for {key['internal_record_id']} / {field}"
                )
            # QC rows are intentionally outside the old 410-row adjudication
            # form; retain their identity and OY result in the separate QC export.
            row = {
                "record_id": key["internal_record_id"],
                "field": field,
                "row_status": "qc_agreement",
            }
        else:
            row = dict(template)
        row.update(
            {
                "task_id": task_id,
                "case_id": key["case_id"],
                "third_party_task_id": task_id,
                "third_party_case_id": key["case_id"],
                "third_party_row_type": key["row_type"],
                "third_party_final_label": review["final_label"],
                "third_party_verified_evidence_locator": review[
                    "verified_evidence_locator"
                ],
                "third_party_brief_reason": review["brief_reason"],
                "third_party_confidence": review["confidence"],
                "third_party_unresolved": review["unresolved"],
                "third_party_reviewer_initials": review["reviewer_initials"],
                "third_party_review_date": review["review_date"],
                "reviewer_initials": review["reviewer_initials"],
                "review_date": review["review_date"],
            }
        )
        if key["row_type"] == "qc_agreement":
            row["qc_hidden_reference_label"] = key.get("hidden_reference_label", "")
            row["qc_matches_hidden_reference"] = (
                _canonical_labels(review["final_label"])
                == _canonical_labels(key.get("hidden_reference_label", ""))
            )
            qc_rows.append(row)
            continue
        if task_id == CNVD_TASK_ID:
            row["third_party_original_final_label"] = row["third_party_final_label"]
            row["third_party_final_label"] = CNVD_FINAL_LABEL
            row["third_party_brief_reason"] = (
                row["third_party_brief_reason"].rstrip()
                + " "
                + CNVD_PROVENANCE
            )
            row["decision_provenance"] = CNVD_PROVENANCE
        else:
            row["third_party_original_final_label"] = ""
            row["decision_provenance"] = "OY external rereview"
        # Keep the legacy adjudication-form field populated for audit readers;
        # the third-party value remains available in the prefixed fields above.
        row["human_final_label"] = row["third_party_final_label"]
        row["brief_reason"] = row["third_party_brief_reason"]
        row["evidence_location_verified"] = row[
            "third_party_verified_evidence_locator"
        ]
        row["unresolved"] = row["third_party_unresolved"]
        decisions.append(row)
    return decisions, qc_rows


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows and not fieldnames:
        raise ValueError(f"cannot infer headers for empty output: {path}")
    fields = fieldnames or list(rows[0])
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_statistics(data: Path, matrix: list[dict[str, str]]) -> None:
    target = [row for row in matrix if row.get("analytical_role") == "target_software_study"]
    output: list[dict[str, str]] = []
    for field, column in FIELD_MAP.items():
        counts = {label: 0 for label in FIELD_LABELS[field]}
        for row in target:
            value = row.get(column, "").strip()
            labels = [part.strip() for part in value.split(";") if part.strip()]
            if field not in {"lifecycle coverage", "cross-stage capability"}:
                labels = labels[:1]
            if not labels:
                labels = ["no qualifying label observed"]
            for label in labels:
                if label in counts:
                    counts[label] += 1
        for label in FIELD_LABELS[field]:
            count = counts[label]
            output.append({
                "field": field,
                "label": label,
                "count": str(count),
                "denominator": str(len(target)),
                "share": f"{count / len(target):.6f}",
                "unresolved": "0",
                "reportable_point_estimate": "yes",
            })
    write_csv(data / "adjudicated_synthesis_statistics_199.csv", output)


def integrate_into_artifact(
    root: Path,
    decisions: list[dict[str, str]],
    qc_rows: list[dict[str, str]],
) -> None:
    data = root / "data"
    matrix_path = data / "adjudicated_study_level_coding_matrix_199.csv"
    log_path = data / "adjudication_log_199_all_fields.csv"
    matrix = read_csv(matrix_path)
    log = read_csv(log_path)
    decision_by_key = {(row["record_id"], row["field"]): row for row in decisions}
    matrix_by_id = {row["matrix_id"]: row for row in matrix}
    log_by_key = {(row["record_id"], row["field"]): row for row in log}
    if len(matrix) != 199 or len(log) != 995 or len(decisions) != 410 or len(qc_rows) != 50:
        raise ValueError(
            f"unexpected sizes matrix={len(matrix)} log={len(log)} decisions={len(decisions)} qc={len(qc_rows)}"
        )
    for key, decision in decision_by_key.items():
        record_id, field = key
        matrix_row = matrix_by_id[record_id]
        matrix_row[FIELD_MAP[field]] = decision["third_party_final_label"]
        matrix_row["coding_status"] = "external_rereview_integrated"
        matrix_row["harmonization_status"] = (
            "adjudicated_after_independent_double_coding_and_external_rereview"
        )
        log_row = log_by_key[key]
        log_row.update(
            {
                "final_label": decision["third_party_final_label"],
                "resolution_type": "third_party_external_rereview",
                "brief_reason": decision["third_party_brief_reason"],
                "evidence_location": decision[
                    "third_party_verified_evidence_locator"
                ],
                "unresolved": decision["third_party_unresolved"],
                "reviewer_initials": decision["third_party_reviewer_initials"],
                "review_date": decision["third_party_review_date"],
            }
        )
    write_csv(matrix_path, matrix)
    write_csv(log_path, log)
    write_statistics(data, matrix)
    write_csv(
        data / "third_party_rereview_decisions_20260824.csv",
        decisions,
    )
    write_csv(
        data / "third_party_rereview_qc_20260824.csv",
        qc_rows,
    )
    manifest_path = data / "adjudication_completion_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest.update(
        {
            "resolution_types": {
                "third_party_external_rereview": len(decisions),
                "agreed_assignment": 585,
            },
            "third_party_rereview": {
                "reviewer_initials": "OY",
                "review_date": "2026-08-24",
                "task_count": 460,
                "disagreement_tasks_integrated": len(decisions),
                "qc_tasks_kept_separate": len(qc_rows),
                "source_workbook_name": "third_party_core_adjudication_rereview_round2_R2_material_identity_corrected_7cases.xlsx",
                "raw_review_export": "third_party_rereview_oy_20260824.csv",
                "material_identity_crosswalk": "data/third_party_rereview_material_crosswalk_20260824.csv",
                "decision_export": "data/third_party_rereview_decisions_20260824.csv",
                "qc_export": "data/third_party_rereview_qc_20260824.csv",
                "cnvd_post_check_task": CNVD_TASK_ID,
                "cnvd_final_label": CNVD_FINAL_LABEL,
                "final_statistics": "data/adjudicated_synthesis_statistics_199.csv",
            }
        }
    )
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("template_csv", type=Path)
    parser.add_argument("key_csv", type=Path)
    parser.add_argument("review_csv", type=Path)
    parser.add_argument("--artifact-root", type=Path, required=True)
    args = parser.parse_args()
    decisions, qc_rows = build_integration_rows(
        read_csv(args.template_csv), read_csv(args.key_csv), read_csv(args.review_csv)
    )
    integrate_into_artifact(args.artifact_root, decisions, qc_rows)
    print(
        f"THIRD_PARTY_REREVIEW_INTEGRATED decisions={len(decisions)} qc_separate={len(qc_rows)} cnvd={CNVD_FINAL_LABEL}"
    )


if __name__ == "__main__":
    main()
