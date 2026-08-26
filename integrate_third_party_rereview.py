#!/usr/bin/env python3
"""Integrate OY's external rereview while keeping raw coder/QC layers separate."""

from __future__ import annotations

import argparse
import csv
import hashlib
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

CORRECTED_TASK_IDS = {
    "R2-011", "R2-062", "R2-064", "R2-077", "R2-116", "R2-159", "R2-202",
}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def validate_review_package(
    key_rows: list[dict[str, str]],
    review_rows: list[dict[str, str]],
    *,
    material_root: Path | None = None,
    corrected_crosswalk_rows: list[dict[str, str]] | None = None,
    comparison_rows: list[dict[str, str]] | None = None,
    matrix_rows: list[dict[str, str]] | None = None,
    expected_task_count: int = 460,
    expected_disagreement_count: int = 410,
    expected_qc_count: int = 50,
    expected_task_case_count: int = 196,
    expected_corpus_count: int = 199,
    corrected_task_ids: set[str] = CORRECTED_TASK_IDS,
) -> tuple[dict[str, int | str], dict[str, str]]:
    """Validate task, study, field, label, and local-material identity."""

    key_by_task = _index_by_task(key_rows)
    review_by_task = _index_by_task(review_rows)
    if len(key_rows) != expected_task_count or len(review_rows) != expected_task_count:
        raise ValueError(
            f"unexpected task counts key={len(key_rows)} review={len(review_rows)}"
        )
    if len(key_by_task) != len(key_rows) or len(review_by_task) != len(review_rows):
        raise ValueError("duplicate task ID in key or OY review export")
    if set(key_by_task) != set(review_by_task):
        missing = sorted(set(key_by_task) - set(review_by_task))
        extra = sorted(set(review_by_task) - set(key_by_task))
        raise ValueError(f"task-set mismatch missing={missing} extra={extra}")

    row_type_counts = {
        name: sum(row.get("row_type") == name for row in key_rows)
        for name in ("disagreement", "qc_agreement")
    }
    if row_type_counts != {
        "disagreement": expected_disagreement_count,
        "qc_agreement": expected_qc_count,
    }:
        raise ValueError(f"unexpected task strata: {row_type_counts}")

    corrected_by_case = {
        row["case_id"]: row for row in (corrected_crosswalk_rows or [])
    }
    case_identity: dict[str, tuple[str, str]] = {}
    material_hashes: dict[str, str] = {}
    corrected_seen: set[str] = set()

    for task_id, key in key_by_task.items():
        review = review_by_task[task_id]
        field = FIELD_KEY_MAP.get(key.get("field_key", ""))
        if not field:
            raise ValueError(f"unknown field key for {task_id}: {key.get('field_key')}")
        if review.get("case_id") != key.get("case_id"):
            raise ValueError(f"case identity mismatch for {task_id}")
        if review.get("study_title") != key.get("study_title"):
            raise ValueError(f"study-title mismatch for {task_id}")
        if review.get("field") != field:
            raise ValueError(f"field mismatch for {task_id}")
        if review.get("completion_check") != "ready":
            raise ValueError(f"incomplete OY review row: {task_id}")
        for column in (
            "final_label", "verified_evidence_locator", "brief_reason", "confidence",
            "unresolved", "reviewer_initials", "review_date", "included_local_file",
        ):
            if not review.get(column, "").strip():
                raise ValueError(f"missing {column} for {task_id}")
        if review["reviewer_initials"] != "OY" or review["unresolved"] != "no":
            raise ValueError(f"unexpected reviewer or unresolved state for {task_id}")

        labels = [part.strip() for part in review["final_label"].split(";") if part.strip()]
        illegal = sorted(set(labels) - set(FIELD_LABELS[field]))
        if illegal:
            raise ValueError(f"illegal label for {task_id}: {illegal}")
        is_multilabel = field in {"lifecycle coverage", "cross-stage capability"}
        if not is_multilabel and len(labels) != 1:
            raise ValueError(f"single-label field has {len(labels)} labels for {task_id}")
        if "no qualifying label observed" in labels and len(labels) != 1:
            raise ValueError(f"empty-set label combined with positive label for {task_id}")

        identity = (key["internal_record_id"], key["study_title"])
        prior = case_identity.setdefault(key["case_id"], identity)
        if prior != identity:
            raise ValueError(f"case maps to multiple studies: {key['case_id']}")

        relative = Path(*review["included_local_file"].replace("\\", "/").split("/"))
        if relative.stem != key["case_id"]:
            raise ValueError(f"material filename/case mismatch for {task_id}")
        uses_corrected = relative.parts[0] == "papers_corrected"
        if task_id in corrected_task_ids:
            if not uses_corrected:
                raise ValueError(f"corrected task uses old material path: {task_id}")
            corrected_seen.add(task_id)
        elif uses_corrected:
            raise ValueError(f"unexpected corrected material path for {task_id}")

        if material_root is not None:
            path = (material_root / relative).resolve()
            root = material_root.resolve()
            if root not in path.parents:
                raise ValueError(f"material path escapes review root for {task_id}")
            if not path.is_file():
                raise ValueError(f"material path does not exist for {task_id}: {path}")
            digest = _sha256(path)
            material_hashes[task_id] = digest
            if uses_corrected:
                crosswalk = corrected_by_case.get(key["case_id"])
                if not crosswalk:
                    raise ValueError(f"missing corrected crosswalk row for {task_id}")
                if digest != crosswalk.get("sha256", "").upper():
                    raise ValueError(f"corrected material hash mismatch for {task_id}")
                expected_suffix = crosswalk.get("new_file", "").replace("\\", "/")
                actual = review["included_local_file"].replace("\\", "/")
                if not expected_suffix.endswith(actual):
                    raise ValueError(f"corrected material path mismatch for {task_id}")

    if len(case_identity) != expected_task_case_count:
        raise ValueError(f"unexpected unique case count: {len(case_identity)}")
    if corrected_seen != corrected_task_ids:
        raise ValueError(
            f"corrected task-set mismatch seen={sorted(corrected_seen)} expected={sorted(corrected_task_ids)}"
        )

    coder_study_count = 0
    if comparison_rows is not None or matrix_rows is not None:
        if comparison_rows is None or matrix_rows is None:
            raise ValueError("comparison and matrix rows must be supplied together")
        comparison_by_id = {row["record_id"]: row for row in comparison_rows}
        matrix_by_id = {row["matrix_id"]: row for row in matrix_rows}
        if len(comparison_by_id) != expected_corpus_count or len(matrix_by_id) != expected_corpus_count:
            raise ValueError("coder/matrix study counts do not match the case count")
        if set(comparison_by_id) != set(matrix_by_id):
            raise ValueError("coder comparison and final matrix have different study IDs")
        for record_id, comparison in comparison_by_id.items():
            if comparison.get("title") != matrix_by_id[record_id].get("title"):
                raise ValueError(f"coder/matrix title mismatch: {record_id}")
        for record_id, title in case_identity.values():
            comparison = comparison_by_id.get(record_id)
            matrix = matrix_by_id.get(record_id)
            if comparison is None or matrix is None:
                raise ValueError(f"missing coder or matrix study: {record_id}")
            if comparison.get("title") != title:
                raise ValueError(f"task/coder title mismatch: {record_id}")
        coder_study_count = len(comparison_by_id)

    return (
        {
            "status": "passed",
            "task_count": len(key_rows),
            "disagreement_task_count": row_type_counts["disagreement"],
            "qc_task_count": row_type_counts["qc_agreement"],
            "unique_task_case_count": len(case_identity),
            "coder_crosswalk_study_count": coder_study_count,
            "corrected_task_count": len(corrected_seen),
            "material_hash_count": len(material_hashes),
        },
        material_hashes,
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
    material_hashes: dict[str, str] | None = None,
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
                "third_party_study_title": review.get(
                    "study_title", key.get("study_title", "")
                ),
                "third_party_material_path": review.get("included_local_file", ""),
                "third_party_material_sha256": (material_hashes or {}).get(task_id, ""),
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
            low_reliability_reporting = (
                field == "lifecycle coverage" and label == "reporting and audit"
            )
            output.append({
                "field": field,
                "label": label,
                "count": str(count),
                "denominator": str(len(target)),
                "share": f"{count / len(target):.6f}",
                "unresolved": "0",
                "reportable_point_estimate": "no" if low_reliability_reporting else "yes",
                "interpretation_scope": (
                    "adjudicated descriptive outcome only"
                    if low_reliability_reporting
                    else "adjudicated distribution"
                ),
            })
    write_csv(data / "adjudicated_synthesis_statistics_199.csv", output)


def integrate_into_artifact(
    root: Path,
    decisions: list[dict[str, str]],
    qc_rows: list[dict[str, str]],
    validation_summary: dict[str, int | str] | None = None,
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
                "task_material_validation": validation_summary or {},
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
    parser.add_argument("--material-root", type=Path, required=True)
    parser.add_argument("--corrected-crosswalk", type=Path, required=True)
    args = parser.parse_args()
    key_rows = read_csv(args.key_csv)
    review_rows = read_csv(args.review_csv)
    validation_summary, material_hashes = validate_review_package(
        key_rows,
        review_rows,
        material_root=args.material_root,
        corrected_crosswalk_rows=read_csv(args.corrected_crosswalk),
        comparison_rows=read_csv(
            args.artifact_root / "data" / "integrated_199_second_coder_comparison_20260730.csv"
        ),
        matrix_rows=read_csv(
            args.artifact_root / "data" / "adjudicated_study_level_coding_matrix_199.csv"
        ),
    )
    decisions, qc_rows = build_integration_rows(
        read_csv(args.template_csv), key_rows, review_rows, material_hashes
    )
    integrate_into_artifact(
        args.artifact_root, decisions, qc_rows, validation_summary
    )
    print(
        f"THIRD_PARTY_REREVIEW_INTEGRATED decisions={len(decisions)} qc_separate={len(qc_rows)} cnvd={CNVD_FINAL_LABEL}"
    )


if __name__ == "__main__":
    main()
