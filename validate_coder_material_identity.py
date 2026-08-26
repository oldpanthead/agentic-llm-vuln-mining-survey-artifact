#!/usr/bin/env python3
"""Verify that first/second coder local material maps resolve to the coded studies."""

from __future__ import annotations

import argparse
import csv
import re
import subprocess
from pathlib import Path


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def normalize(value: str) -> set[str]:
    return {
        token
        for token in re.sub(r"[^a-z0-9]+", " ", value.lower()).split()
        if len(token) >= 4
    }


def pdf_title_score(title: str, pdf: Path) -> float:
    result = subprocess.run(
        ["pdftotext", "-f", "1", "-l", "2", "-enc", "UTF-8", str(pdf), "-"],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    expected = normalize(title)
    observed = normalize(result.stdout)
    return len(expected & observed) / len(expected) if expected else 1.0


def resolve(path: str, archive_materials: Path) -> Path:
    candidate = Path(path)
    if candidate.is_file():
        return candidate
    migrated = archive_materials / candidate.name
    if migrated.is_file():
        return migrated
    raise FileNotFoundError(path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("comparison_csv", type=Path)
    parser.add_argument("first_map_csv", type=Path)
    parser.add_argument("second_map_csv", type=Path)
    parser.add_argument("multisource_dir", type=Path)
    parser.add_argument("archive_materials", type=Path)
    parser.add_argument("--matrix-csv", type=Path, required=True)
    parser.add_argument("--threshold", type=float, default=0.65)
    args = parser.parse_args()

    comparison = read_csv(args.comparison_csv)
    matrix = read_csv(args.matrix_csv)
    titles = {row["matrix_id"]: row["title"] for row in matrix}
    comparison_ids = {row["record_id"] for row in comparison}
    matrix_ids = set(titles)
    if comparison_ids != matrix_ids:
        raise ValueError("first/second comparison and final matrix record IDs differ")
    first = {
        row["matrix_id"]: row
        for row in read_csv(args.first_map_csv)
        if row["matrix_id"] in titles
    }
    second = {
        row["matrix_id"]: row
        for row in read_csv(args.second_map_csv)
        if row["rank"] == "1" and row["matrix_id"] in titles
    }
    if set(first) != set(second):
        raise ValueError(
            f"coder map coverage mismatch first={len(first)} second={len(second)}"
        )

    fms_rows: list[dict[str, str]] = []
    for path in sorted(args.multisource_dir.glob("final_multisource_search_20260730_second_coder*_blind.csv")):
        fms_rows.extend(read_csv(path))
    fms_by_id = {
        row["discovery_id"]: row
        for row in fms_rows
        if row.get("eligibility_decision") == "include_study_level"
    }
    if len(fms_by_id) != 132:
        raise ValueError(f"expected 132 multisource study rows, found {len(fms_by_id)}")
    if len(first) + len(fms_by_id) != len(titles):
        raise ValueError(
            f"material coverage mismatch core={len(first)} multisource={len(fms_by_id)} corpus={len(titles)}"
        )

    scores: list[float] = []
    for row in first.values():
        scores.append(pdf_title_score(titles[row["matrix_id"]], resolve(row["pdf_path"], args.archive_materials)))
    for row in second.values():
        scores.append(pdf_title_score(titles[row["matrix_id"]], resolve(row["local_path"], args.archive_materials)))
    for row in fms_by_id.values():
        scores.append(pdf_title_score(row["title"], Path(row["local_review_pdf"])))
    low = [score for score in scores if score < args.threshold]
    if low:
        raise ValueError(f"low title-identity scores: {len(low)}")
    print(
        f"CODER_MATERIAL_IDENTITY_OK first={len(first)} second={len(second)} "
        f"multisource={len(fms_by_id)} corpus={len(titles)} files_checked={len(scores)} "
        f"min_title_score={min(scores):.3f} low_score={len(low)}"
    )


if __name__ == "__main__":
    main()
