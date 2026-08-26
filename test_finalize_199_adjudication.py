#!/usr/bin/env python3
"""Dry-run the adjudication finalizer with synthetic, non-research decisions."""

from __future__ import annotations

import csv
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

from validate_199_adjudication_form import FIELD_RULES


ROOT = Path(__file__).resolve().parent
FORM = ROOT / "adjudication" / "adjudication_form_199_all_disagreements_20260812.csv"
SOURCE_MATRIX = ROOT / "data" / "current_study_level_coding_matrix_harmonized.csv"

MATRIX_FIELD = {
    "lifecycle_coverage": "lifecycle coverage",
    "cross_stage_capabilities": "cross-stage capability",
    "primary_system_shape": "primary system shape",
    "strongest_evidence_output": "principal reported evidence output",
    "external_traceability": "external traceability",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def normalized(value: str, field: str) -> str:
    rule = FIELD_RULES[field]
    if rule["type"] == "single-label":
        return value.strip()
    selected = {part.strip() for part in value.split(";") if part.strip()}
    return ";".join(label for label in rule["allowed"] if label in selected)


def main() -> None:
    rows = read_csv(FORM)
    for row in rows:
        row["human_final_label"] = normalized(row["coder_x_label"], row["field"])
        row["brief_reason"] = "Synthetic pipeline test selecting coder X; not a research adjudication."
        row["evidence_location_verified"] = row["evidence_location_lead"]
        row["unresolved"] = "no"
        row["reviewer_initials"] = "TEST"
        row["review_date"] = "1900-01-01"

    with tempfile.TemporaryDirectory(prefix="adjudication_dry_run_") as temp:
        temp_dir = Path(temp)
        synthetic_form = temp_dir / "synthetic.csv"
        output_dir = temp_dir / "output"
        write_csv(synthetic_form, rows)
        subprocess.run(
            [
                sys.executable,
                str(ROOT / "finalize_199_adjudication.py"),
                str(synthetic_form),
                "--output-dir",
                str(output_dir),
            ],
            check=True,
        )
        source = read_csv(SOURCE_MATRIX)
        adjudicated = read_csv(output_dir / "adjudicated_study_level_coding_matrix_199.csv")
        log = read_csv(output_dir / "adjudication_log_199_all_fields.csv")
        statistics = read_csv(output_dir / "adjudicated_synthesis_statistics_199.csv")
        assert len(adjudicated) == 199
        assert len(log) == 995
        assert len(statistics) == 26
        assert all(row["reportable_point_estimate"] == "yes" for row in statistics)
        source_by_id = {row["matrix_id"]: row for row in source}
        for row in adjudicated:
            original = source_by_id[row["matrix_id"]]
            for field in (
                "lifecycle_coverage",
                "cross_stage_capabilities",
                "primary_system_shape",
                "strongest_evidence_output",
                "external_traceability",
            ):
                assert row[field] == normalized(original[field], MATRIX_FIELD[field]), (row["matrix_id"], field)
        assert Counter(row["resolution_type"] for row in log)["coder_x_selected"] == 410
        assert Counter(row["resolution_type"] for row in log)["agreed_assignment"] == 585

        unresolved_rows = [dict(row) for row in rows]
        unresolved_target = next(row for row in unresolved_rows if row["field"] == "external traceability")
        unresolved_target["human_final_label"] = "unresolved"
        unresolved_target["brief_reason"] = "Synthetic unresolved-path test; not a research adjudication."
        unresolved_target["unresolved"] = "yes"
        unresolved_form = temp_dir / "synthetic_unresolved.csv"
        unresolved_output = temp_dir / "unresolved_output"
        write_csv(unresolved_form, unresolved_rows)
        subprocess.run(
            [
                sys.executable,
                str(ROOT / "finalize_199_adjudication.py"),
                str(unresolved_form),
                "--output-dir",
                str(unresolved_output),
                "--allow-unresolved",
            ],
            check=True,
        )
        unresolved_statistics = read_csv(unresolved_output / "adjudicated_synthesis_statistics_199.csv")
        for row in unresolved_statistics:
            if row["field"] == "external traceability":
                assert row["reportable_point_estimate"] == "no"
                assert row["count"] == ""
            else:
                assert row["reportable_point_estimate"] == "yes"
    print("ADJUDICATION_DRY_RUN_OK")


if __name__ == "__main__":
    main()
