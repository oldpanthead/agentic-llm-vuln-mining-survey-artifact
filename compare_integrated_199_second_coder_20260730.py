#!/usr/bin/env python3
"""Compute independent-coder agreement across the integrated 199-study set.

The released 67-study review and the final multi-source search used the same
controlled lifecycle, capability, shape, evidence-output, and traceability
labels. This script combines those independent assignments without modifying
either source file or creating consensus labels.
"""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"

OLD_AUTHOR = DATA / "current_study_level_coding_matrix_harmonized_pre_final_multisource_20260730.csv"
OLD_CODER2 = DATA / "unified_second_coder_final_results.csv"
NEW_COMPARISON = DATA / "final_multisource_search_20260730_all_coder_comparison.csv"

OUTPUT_COMPARISON = DATA / "integrated_199_second_coder_comparison_20260730.csv"
OUTPUT_PER_LABEL = DATA / "integrated_199_per_label_reliability_20260730.csv"
OUTPUT_SENSITIVITY = DATA / "integrated_199_label_substitution_sensitivity_20260730.csv"
REPORT = ROOT / "INTEGRATED_199_SECOND_CODER_AGREEMENT_20260730.md"

MULTI_FIELDS = ("lifecycle", "capability")
SINGLE_FIELDS = ("primary_shape", "principal_evidence", "external_traceability")


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def norm(value: str) -> str:
    return " ".join((value or "").strip().split())


def label_set(value: str) -> set[str]:
    return {norm(item) for item in (value or "").split(";") if norm(item)}


def serialise(values: set[str]) -> str:
    return ";".join(sorted(values))


def raw_agreement(a: list[str], b: list[str]) -> float:
    return sum(x == y for x, y in zip(a, b)) / len(a)


def kappa(a: list[str], b: list[str]) -> float:
    n = len(a)
    observed = raw_agreement(a, b)
    ca, cb = Counter(a), Counter(b)
    expected = sum((ca[key] / n) * (cb[key] / n) for key in set(ca) | set(cb))
    if expected == 1.0:
        return 1.0 if observed == 1.0 else 0.0
    return (observed - expected) / (1.0 - expected)


def jaccard(a: set[str], b: set[str]) -> float:
    union = a | b
    return 1.0 if not union else len(a & b) / len(union)


def micro_f1(pairs: list[tuple[set[str], set[str]]]) -> float:
    tp = sum(len(a & b) for a, b in pairs)
    fp = sum(len(a - b) for a, b in pairs)
    fn = sum(len(b - a) for a, b in pairs)
    return 0.0 if 2 * tp + fp + fn == 0 else 2 * tp / (2 * tp + fp + fn)


def old_pairs() -> list[dict[str, str]]:
    author_rows = {
        row["matrix_id"]: row
        for row in read_rows(OLD_AUTHOR)
        if row["analytical_role"] == "target_software_study"
    }
    coder_rows = {
        row["matrix_id"]: row
        for row in read_rows(OLD_CODER2)
        if row["review_scope"] == "target-software study"
    }
    if set(author_rows) != set(coder_rows):
        raise SystemExit("ERROR: released author and coder2 IDs differ")

    rows: list[dict[str, str]] = []
    for record_id, author in author_rows.items():
        coder = coder_rows[record_id]
        rows.append(
            {
                "cohort": "released_67",
                "record_id": record_id,
                "title": author["title"],
                "first_lifecycle": serialise(label_set(author["lifecycle_coverage"])),
                "second_lifecycle": serialise(label_set(coder["final_lifecycle_coverage"])),
                "first_capability": serialise(label_set(author["cross_stage_capabilities"])),
                "second_capability": serialise(label_set(coder["final_cross_stage_capabilities"])),
                "first_primary_shape": norm(author["primary_system_shape"]),
                "second_primary_shape": norm(coder["final_primary_system_shape"]),
                "first_principal_evidence": norm(author["strongest_evidence_output"]),
                "second_principal_evidence": norm(coder["final_strongest_evidence_output"]),
                "first_external_traceability": norm(author["external_traceability"]),
                "second_external_traceability": norm(coder["final_external_traceability"]),
            }
        )
    return rows


def new_pairs() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source in read_rows(NEW_COMPARISON):
        if source["jointly_included"] != "true":
            continue
        rows.append(
            {
                "cohort": "final_multisource_132",
                "record_id": source["discovery_id"],
                "title": source["title"],
                "first_lifecycle": source["first_lifecycle"],
                "second_lifecycle": source["second_lifecycle"],
                "first_capability": source["first_capabilities"],
                "second_capability": source["second_capabilities"],
                "first_primary_shape": source["first_shape"],
                "second_primary_shape": source["second_shape"],
                "first_principal_evidence": source["first_evidence"],
                "second_principal_evidence": source["second_evidence"],
                "first_external_traceability": source["first_trace"],
                "second_external_traceability": source["second_trace"],
            }
        )
    return rows


def single_stats(rows: list[dict[str, str]], field: str) -> tuple[float, float]:
    first = [row[f"first_{field}"] for row in rows]
    second = [row[f"second_{field}"] for row in rows]
    return raw_agreement(first, second), kappa(first, second)


def multi_stats(rows: list[dict[str, str]], field: str) -> tuple[float, float, float]:
    pairs = [
        (label_set(row[f"first_{field}"]), label_set(row[f"second_{field}"]))
        for row in rows
    ]
    exact = sum(a == b for a, b in pairs) / len(pairs)
    return exact, sum(jaccard(a, b) for a, b in pairs) / len(pairs), micro_f1(pairs)


def per_label(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    for field in MULTI_FIELDS:
        pairs = [
            (label_set(row[f"first_{field}"]), label_set(row[f"second_{field}"]))
            for row in rows
        ]
        universe = sorted(set().union(*(a | b for a, b in pairs)))
        for label in universe:
            first = ["1" if label in a else "0" for a, _ in pairs]
            second = ["1" if label in b else "0" for _, b in pairs]
            output.append(
                {
                    "field": field,
                    "label": label,
                    "n": str(len(rows)),
                    "first_positive": str(first.count("1")),
                    "second_positive": str(second.count("1")),
                    "raw_agreement": f"{raw_agreement(first, second):.6f}",
                    "cohen_kappa": f"{kappa(first, second):.6f}",
                }
            )
    return output


def sensitivity(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    for field in (*MULTI_FIELDS, *SINGLE_FIELDS):
        if field in MULTI_FIELDS:
            first_values = [label for row in rows for label in label_set(row[f"first_{field}"])]
            second_values = [label for row in rows for label in label_set(row[f"second_{field}"])]
        else:
            first_values = [row[f"first_{field}"] for row in rows]
            second_values = [row[f"second_{field}"] for row in rows]
        first_counts, second_counts = Counter(first_values), Counter(second_values)
        for label in sorted(set(first_counts) | set(second_counts)):
            difference = second_counts[label] - first_counts[label]
            output.append(
                {
                    "field": field,
                    "label": label,
                    "n": str(len(rows)),
                    "first_coder_count": str(first_counts[label]),
                    "second_coder_substitution_count": str(second_counts[label]),
                    "difference": str(difference),
                }
            )
    return output


def main() -> int:
    rows = old_pairs() + new_pairs()
    if len(rows) != 199 or len({row["record_id"] for row in rows}) != 199:
        raise SystemExit(f"ERROR: expected 199 unique target studies, found {len(rows)}")

    write_rows(OUTPUT_COMPARISON, rows)
    write_rows(OUTPUT_PER_LABEL, per_label(rows))
    write_rows(OUTPUT_SENSITIVITY, sensitivity(rows))

    lines = [
        "# Integrated 199-Study Independent-Coder Agreement",
        "",
        "The calculation combines the released 67-study review with 132 studies jointly included from the final multi-source search. Both cohorts use the same controlled label vocabulary. Source assignments remain separate, and this report does not create consensus labels or score claim-boundary prose by exact textual agreement.",
        "",
        "## Coverage",
        "",
        "| Cohort | Target-software studies |",
        "|---|---:|",
        "| Released study set | 67 |",
        "| Final multi-source search | 132 |",
        "| **Integrated set** | **199** |",
        "",
        "## Single-Label Fields",
        "",
        "| Field | Raw agreement | Cohen's kappa |",
        "|---|---:|---:|",
    ]
    for field in SINGLE_FIELDS:
        raw, kap = single_stats(rows, field)
        lines.append(f"| {field.replace('_', ' ')} | {raw:.3f} | {kap:.3f} |")
    lines.extend(
        [
            "",
            "## Multi-Label Fields",
            "",
            "| Field | Row exact | Mean row Jaccard | Micro F1 |",
            "|---|---:|---:|---:|",
        ]
    )
    for field in MULTI_FIELDS:
        exact, mean_j, f1 = multi_stats(rows, field)
        lines.append(f"| {field} | {exact:.3f} | {mean_j:.3f} | {f1:.3f} |")
    lines.extend(
        [
            "",
            "## Interpretation Boundary",
            "",
            "Eligibility agreement for the new search is reported separately because the released 67-study set had already passed inclusion before its unified second-coder review. The integrated reliability result therefore covers analytical coding fields only.",
            "",
            "## Audit Files",
            "",
            f"- `{OUTPUT_COMPARISON.relative_to(ROOT).as_posix()}`",
            f"- `{OUTPUT_PER_LABEL.relative_to(ROOT).as_posix()}`",
            f"- `{OUTPUT_SENSITIVITY.relative_to(ROOT).as_posix()}`",
        ]
    )
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"INTEGRATED_TARGET_STUDIES={len(rows)}")
    for field in SINGLE_FIELDS:
        raw, kap = single_stats(rows, field)
        print(f"{field.upper()} raw={raw:.3f} kappa={kap:.3f}")
    for field in MULTI_FIELDS:
        exact, mean_j, f1 = multi_stats(rows, field)
        print(f"{field.upper()} exact={exact:.3f} jaccard={mean_j:.3f} micro_f1={f1:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
