#!/usr/bin/env python3
"""Compare independently completed first- and second-coder labels."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
FIRST = DATA / "final_multisource_search_20260730_first_coder.csv"
SECOND = DATA / "final_multisource_search_20260730_second_coder_blind.csv"
COMPARISON = DATA / "final_multisource_search_20260730_coder_comparison.csv"
PER_LABEL = DATA / "final_multisource_search_20260730_per_label_reliability.csv"
REPORT = ROOT / "FINAL_MULTISOURCE_CODER_AGREEMENT_20260730.md"

MULTI_FIELDS = {
    "lifecycle": "final_lifecycle_coverage",
    "capability": "final_cross_stage_capabilities",
}
SINGLE_FIELDS = {
    "eligibility": "eligibility_decision",
    "primary_shape": "final_primary_system_shape",
    "principal_evidence": "final_principal_reported_evidence_output",
    "external_traceability": "final_external_traceability",
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def norm(value: str) -> str:
    return " ".join((value or "").strip().split())


def labels(value: str) -> set[str]:
    return {norm(item) for item in (value or "").split(";") if norm(item)}


def raw_agreement(a: list[str], b: list[str]) -> float:
    return sum(x == y for x, y in zip(a, b)) / len(a)


def kappa(a: list[str], b: list[str]) -> float:
    n = len(a)
    po = raw_agreement(a, b)
    ca, cb = Counter(a), Counter(b)
    pe = sum((ca[key] / n) * (cb[key] / n) for key in set(ca) | set(cb))
    if pe == 1.0:
        return 1.0 if po == 1.0 else 0.0
    return (po - pe) / (1.0 - pe)


def jaccard(a: set[str], b: set[str]) -> float:
    union = a | b
    return 1.0 if not union else len(a & b) / len(union)


def micro_f1(pairs: list[tuple[set[str], set[str]]]) -> float:
    tp = sum(len(a & b) for a, b in pairs)
    fp = sum(len(a - b) for a, b in pairs)
    fn = sum(len(b - a) for a, b in pairs)
    return 0.0 if 2 * tp + fp + fn == 0 else 2 * tp / (2 * tp + fp + fn)


def main() -> int:
    first_rows = read_rows(FIRST)
    second_rows = read_rows(SECOND)
    first = {row["discovery_id"]: row for row in first_rows}
    second = {row["discovery_id"]: row for row in second_rows}
    if set(first) != set(second):
        raise SystemExit("ERROR coder files do not contain the same discovery IDs")
    ids = [row["discovery_id"] for row in first_rows]

    comparison_rows: list[dict[str, str]] = []
    for record_id in ids:
        a, b = first[record_id], second[record_id]
        life_a, life_b = labels(a[MULTI_FIELDS["lifecycle"]]), labels(b[MULTI_FIELDS["lifecycle"]])
        cap_a, cap_b = labels(a[MULTI_FIELDS["capability"]]), labels(b[MULTI_FIELDS["capability"]])
        row = {
            "discovery_id": record_id,
            "title": a["title"],
            "eligibility_exact": str(norm(a["eligibility_decision"]) == norm(b["eligibility_decision"])).lower(),
            "shape_exact": str(norm(a["final_primary_system_shape"]) == norm(b["final_primary_system_shape"])).lower(),
            "evidence_exact": str(norm(a["final_principal_reported_evidence_output"]) == norm(b["final_principal_reported_evidence_output"])).lower(),
            "trace_exact": str(norm(a["final_external_traceability"]) == norm(b["final_external_traceability"])).lower(),
            "lifecycle_exact": str(life_a == life_b).lower(),
            "lifecycle_jaccard": f"{jaccard(life_a, life_b):.6f}",
            "capability_exact": str(cap_a == cap_b).lower(),
            "capability_jaccard": f"{jaccard(cap_a, cap_b):.6f}",
            "first_shape": norm(a["final_primary_system_shape"]),
            "second_shape": norm(b["final_primary_system_shape"]),
            "first_evidence": norm(a["final_principal_reported_evidence_output"]),
            "second_evidence": norm(b["final_principal_reported_evidence_output"]),
            "first_trace": norm(a["final_external_traceability"]),
            "second_trace": norm(b["final_external_traceability"]),
            "first_lifecycle": ";".join(sorted(life_a)),
            "second_lifecycle": ";".join(sorted(life_b)),
            "first_capabilities": ";".join(sorted(cap_a)),
            "second_capabilities": ";".join(sorted(cap_b)),
        }
        row["has_any_label_disagreement"] = str(any(row[key] == "false" for key in (
            "eligibility_exact", "shape_exact", "evidence_exact", "trace_exact", "lifecycle_exact", "capability_exact"
        ))).lower()
        comparison_rows.append(row)

    with COMPARISON.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(comparison_rows[0]))
        writer.writeheader()
        writer.writerows(comparison_rows)

    single_stats: dict[str, tuple[float, float]] = {}
    for name, field in SINGLE_FIELDS.items():
        a = [norm(first[i][field]) for i in ids]
        b = [norm(second[i][field]) for i in ids]
        single_stats[name] = (raw_agreement(a, b), kappa(a, b))

    multi_stats: dict[str, tuple[float, float, float]] = {}
    per_label_rows: list[dict[str, str]] = []
    for name, field in MULTI_FIELDS.items():
        pairs = [(labels(first[i][field]), labels(second[i][field])) for i in ids]
        exact = sum(a == b for a, b in pairs) / len(pairs)
        mean_j = sum(jaccard(a, b) for a, b in pairs) / len(pairs)
        mf1 = micro_f1(pairs)
        multi_stats[name] = (exact, mean_j, mf1)
        universe = sorted(set().union(*(a | b for a, b in pairs)))
        for label in universe:
            a_bin = ["1" if label in a else "0" for a, _ in pairs]
            b_bin = ["1" if label in b else "0" for _, b in pairs]
            per_label_rows.append({
                "field": name,
                "label": label,
                "n": str(len(ids)),
                "first_positive": str(a_bin.count("1")),
                "second_positive": str(b_bin.count("1")),
                "raw_agreement": f"{raw_agreement(a_bin, b_bin):.6f}",
                "cohen_kappa": f"{kappa(a_bin, b_bin):.6f}",
            })

    with PER_LABEL.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(per_label_rows[0]))
        writer.writeheader()
        writer.writerows(per_label_rows)

    disagreement_count = sum(row["has_any_label_disagreement"] == "true" for row in comparison_rows)
    lines = [
        "# Final Multi-Source Independent-Coder Agreement (2026-07-30)",
        "",
        "The first-coder file was completed before the second-coder labels were opened. Claim-boundary prose is not assigned a synthetic exact-agreement statistic.",
        "",
        f"- Records compared: {len(ids)}",
        f"- Records with at least one label disagreement: {disagreement_count}",
        "",
        "## Single-Label Fields",
        "",
        "| Field | Raw agreement | Cohen's kappa |",
        "|---|---:|---:|",
    ]
    for name, (raw, kap) in single_stats.items():
        lines.append(f"| {name} | {raw:.3f} | {kap:.3f} |")
    lines.extend(["", "## Multi-Label Fields", "", "| Field | Row exact | Mean row Jaccard | Micro F1 |", "|---|---:|---:|---:|"])
    for name, (exact, mean_j, mf1) in multi_stats.items():
        lines.append(f"| {name} | {exact:.3f} | {mean_j:.3f} | {mf1:.3f} |")
    lines.extend([
        "",
        "## Files",
        "",
        f"- `{COMPARISON.relative_to(ROOT).as_posix()}` preserves row-level label differences.",
        f"- `{PER_LABEL.relative_to(ROOT).as_posix()}` reports prevalence-aware binary agreement for each lifecycle and capability label.",
        "",
        "No disagreement is automatically resolved by this script.",
    ])
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"ROWS={len(ids)} DISAGREEMENT_ROWS={disagreement_count}")
    for name, (raw, kap) in single_stats.items():
        print(f"{name.upper()} raw={raw:.3f} kappa={kap:.3f}")
    for name, (exact, mean_j, mf1) in multi_stats.items():
        print(f"{name.upper()} exact={exact:.3f} jaccard={mean_j:.3f} micro_f1={mf1:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
