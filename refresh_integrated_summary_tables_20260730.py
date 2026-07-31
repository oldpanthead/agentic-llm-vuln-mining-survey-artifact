#!/usr/bin/env python3
"""Refresh manuscript-facing corpus summaries from the integrated files."""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"


def read(name: str) -> list[dict[str, str]]:
    with (DATA / name).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write(name: str, rows: list[dict[str, str]]) -> None:
    with (DATA / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def labels(value: str) -> set[str]:
    return {item.strip() for item in (value or "").split(";") if item.strip()}


def main() -> int:
    corpus = read("corpus.csv")
    crosswalk = read("study_version_crosswalk.csv")
    matrix = read("current_study_level_coding_matrix_harmonized.csv")
    target = [row for row in matrix if row["analytical_role"] == "target_software_study"]
    extended = read("extended_synthesis_audit.csv")

    canonical = [row for row in crosswalk if row["counting_status"] == "canonical_counted"]
    layer_counts = Counter(row["analytical_layer"] for row in canonical)
    screening = [
        {"stage": "Exported source occurrences", "count": "12090", "note": "Saved API/interface exports before deterministic query-specific filtering."},
        {"stage": "Unique multi-source search records screened", "count": "1642", "note": "Exact-title-deduplicated records from the full-range search through 2026-07-30."},
        {"stage": "Integrated source records", "count": str(len(corpus)), "note": "Search and supplementary source records; versions remain traceable."},
        {"stage": "Version or duplicate source records", "count": str(len(crosswalk) - len(canonical)), "note": "Alternate source/version records not counted as separate studies."},
        {"stage": "Canonical studies after version reconciliation", "count": str(len(canonical)), "note": "Analytical counts use one canonical study per study/version group."},
        {"stage": "Study-level coded records", "count": str(len(matrix)), "note": "Target-software studies receiving complete study-level coding."},
        {"stage": "Extended synthesis studies", "count": str(len(extended)), "note": "Full-text-supported adjacent mechanism, evaluation, and governance synthesis."},
        {"stage": "Background/reference studies", "count": str(layer_counts["background_reference"]), "note": "Conceptual, benchmark, tool, method, and ecosystem context."},
        {"stage": "Excluded studies", "count": str(layer_counts["excluded_near_neighbor"]), "note": "Title/abstract exclusions, near-neighbors, and unavailable potentially eligible reports."},
        {"stage": "Product ecosystem snapshot", "count": "23", "note": "Independent deployment-context layer; not part of canonical study counts."},
    ]
    write("screening_summary.csv", screening)

    year_counts: Counter[str] = Counter()
    for row in corpus:
        match = re.search(r"20(?:23|24|25|26)", row.get("year", ""))
        year_counts[match.group(0) if match else "unknown"] += 1
    source_types = Counter()
    for row in corpus:
        value = row["source_type"].lower()
        if value in {"preprint", "arxiv"}:
            source_types["preprint/arXiv"] += 1
        elif value in {"conferencepaper", "conference"}:
            source_types["conference paper"] += 1
        elif value == "journalarticle":
            source_types["journal article"] += 1
        elif value == "formal_source_record":
            source_types["formal DOI/source record"] += 1
        else:
            source_types["book/thesis/report/other"] += 1

    shapes = Counter(row["primary_system_shape"] for row in target)
    snapshot: list[dict[str, str]] = []
    for year in ("2023", "2024", "2025", "2026"):
        snapshot.append({"view": "year_distribution", "category": year, "count": str(year_counts[year]), "denominator": f"{len(corpus)} integrated source records", "scope_note": "source-record composition; versions remain represented"})
    for category, count in sorted(source_types.items()):
        snapshot.append({"view": "source_type_distribution", "category": category, "count": str(count), "denominator": f"{len(corpus)} integrated source records", "scope_note": "source-record composition; categories describe retained metadata form"})
    shape_names = {
        "candidate-analysis system": "candidate analysis",
        "feedback-driven fuzzing agent": "feedback-driven fuzzing",
        "reproduction-, validation-, and repair-centered agent": "reproduction/validation/repair",
        "long-horizon pentest and CRS agent": "long-horizon pentest/CRS",
    }
    for shape, label in shape_names.items():
        snapshot.append({"view": "primary_system_shape", "category": label, "count": str(shapes[shape]), "denominator": f"{len(target)} target-software studies", "scope_note": "one primary shape per target-software study; capabilities remain multi-label"})
    final_labels = {
        "target-software study-level coded studies": len(target),
        "extended synthesis studies": len(extended),
        "background/reference studies": layer_counts["background_reference"],
        "excluded studies": layer_counts["excluded_near_neighbor"],
    }
    for category, count in final_labels.items():
        snapshot.append({"view": "final_canonical_stratification", "category": category, "count": str(count), "denominator": f"{len(canonical)} canonical studies", "scope_note": "analysis-use allocation after version reconciliation"})
    write("mapping_snapshot_counts.csv", snapshot)

    old_status = read("publication_status_standardized.csv")[:68]
    old_by_id = {row["matrix_id"]: row for row in old_status}
    new_meta = {row["record_id"]: row for row in read("final_multisource_new_study_reference_metadata_20260730.csv")}
    standardized: list[dict[str, str]] = []
    for row in matrix:
        if row["matrix_id"] in old_by_id:
            prior = old_by_id[row["matrix_id"]]
            status = prior["publication_status_standardized"]
            year = prior["year"]
        else:
            meta = new_meta[row["record_id"]]
            status = meta["publication_status"]
            year = meta["year"]
        standardized.append(
            {
                "matrix_id": row["matrix_id"],
                "record_id": row["record_id"],
                "system_alias": row["system_alias"],
                "analytical_role": row["analytical_role"],
                "coding_round": row["coding_round"],
                "year": year,
                "publication_status_standardized": status,
                "strongest_evidence_output": row["strongest_evidence_output"],
                "primary_system_shape": row["primary_system_shape"],
                "cross_stage_capabilities": row["cross_stage_capabilities"],
                "external_traceability": row["external_traceability"],
            }
        )
    write("publication_status_standardized.csv", standardized)

    statuses = sorted({row["publication_status_standardized"] for row in standardized if row["analytical_role"] == "target_software_study"})
    evidence_labels = ["candidate judgment", "controlled task completion", "runtime safety signal", "reproducible validation", "externally traceable material"]
    shape_labels = list(shape_names)
    distribution: list[dict[str, str]] = []
    for status in statuses:
        rows = [row for row in standardized if row["analytical_role"] == "target_software_study" and row["publication_status_standardized"] == status]
        item = {"publication_status_standardized": status, "target_software_studies": str(len(rows))}
        for label in evidence_labels:
            item[f"evidence_{label}"] = str(sum(row["strongest_evidence_output"] == label for row in rows))
        for label in shape_labels:
            item[f"shape_{label}"] = str(sum(row["primary_system_shape"] == label for row in rows))
        item["failure_reuse_or_strategy_update"] = str(sum("failure reuse / strategy update" in labels(row["cross_stage_capabilities"]) for row in rows))
        item["governance_or_human_gates"] = str(sum("governance / human gates / disclosure control" in labels(row["cross_stage_capabilities"]) for row in rows))
        distribution.append(item)
    write("publication_status_distribution_by_layer.csv", distribution)

    print(f"SOURCE_RECORDS={len(corpus)} CANONICAL={len(canonical)} TARGET={len(target)} EXTENDED={len(extended)}")
    print("YEARS=" + ",".join(f"{year}:{year_counts[year]}" for year in ("2023", "2024", "2025", "2026")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
