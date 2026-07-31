#!/usr/bin/env python3
"""Compare all independently coded final multi-source search batches."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"

BATCHES = (
    (
        "main",
        DATA / "final_multisource_search_20260730_first_coder.csv",
        DATA / "final_multisource_search_20260730_second_coder_blind.csv",
    ),
    (
        "addendum",
        DATA / "final_multisource_search_20260730_first_coder_addendum.csv",
        DATA / "final_multisource_search_20260730_second_coder_addendum_blind.csv",
    ),
    (
        "remaining",
        DATA / "final_multisource_search_20260730_first_coder_remaining.csv",
        DATA / "final_multisource_search_20260730_second_coder_remaining_blind.csv",
    ),
)

COMPARISON = DATA / "final_multisource_search_20260730_all_coder_comparison.csv"
PER_LABEL = DATA / "final_multisource_search_20260730_all_per_label_reliability.csv"
REPORT = ROOT / "FINAL_MULTISOURCE_ALL_CODER_AGREEMENT_20260730.md"

MULTI_FIELDS = {
    "lifecycle": "final_lifecycle_coverage",
    "capability": "final_cross_stage_capabilities",
}
SINGLE_FIELDS = {
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


def compare_batch(
    batch: str, first_path: Path, second_path: Path
) -> tuple[list[dict[str, str]], list[tuple[dict[str, str], dict[str, str]]]]:
    first_rows = read_rows(first_path)
    second_rows = read_rows(second_path)
    first = {row["discovery_id"]: row for row in first_rows}
    second = {row["discovery_id"]: row for row in second_rows}
    if set(first) != set(second):
        raise SystemExit(f"ERROR {batch}: coder files contain different discovery IDs")

    comparison_rows: list[dict[str, str]] = []
    jointly_included: list[tuple[dict[str, str], dict[str, str]]] = []
    for first_row in first_rows:
        record_id = first_row["discovery_id"]
        second_row = second[record_id]
        first_decision = norm(first_row["eligibility_decision"])
        second_decision = norm(second_row["eligibility_decision"])
        joint = first_decision == second_decision == "include_study_level"
        if joint:
            jointly_included.append((first_row, second_row))
        comparison_rows.append(
            {
                "batch": batch,
                "discovery_id": record_id,
                "title": first_row["title"],
                "first_eligibility": first_decision,
                "second_eligibility": second_decision,
                "eligibility_exact": str(first_decision == second_decision).lower(),
                "jointly_included": str(joint).lower(),
                "first_shape": norm(first_row["final_primary_system_shape"]),
                "second_shape": norm(second_row["final_primary_system_shape"]),
                "first_evidence": norm(
                    first_row["final_principal_reported_evidence_output"]
                ),
                "second_evidence": norm(
                    second_row["final_principal_reported_evidence_output"]
                ),
                "first_trace": norm(first_row["final_external_traceability"]),
                "second_trace": norm(second_row["final_external_traceability"]),
                "first_lifecycle": ";".join(
                    sorted(labels(first_row["final_lifecycle_coverage"]))
                ),
                "second_lifecycle": ";".join(
                    sorted(labels(second_row["final_lifecycle_coverage"]))
                ),
                "first_capabilities": ";".join(
                    sorted(labels(first_row["final_cross_stage_capabilities"]))
                ),
                "second_capabilities": ";".join(
                    sorted(labels(second_row["final_cross_stage_capabilities"]))
                ),
            }
        )
    return comparison_rows, jointly_included


def stats_for_pairs(
    pairs: list[tuple[dict[str, str], dict[str, str]]]
) -> tuple[dict[str, tuple[float, float]], dict[str, tuple[float, float, float]], list[dict[str, str]]]:
    single_stats: dict[str, tuple[float, float]] = {}
    for name, field in SINGLE_FIELDS.items():
        a = [norm(first[field]) for first, _ in pairs]
        b = [norm(second[field]) for _, second in pairs]
        single_stats[name] = (raw_agreement(a, b), kappa(a, b))

    multi_stats: dict[str, tuple[float, float, float]] = {}
    per_label_rows: list[dict[str, str]] = []
    for name, field in MULTI_FIELDS.items():
        label_pairs = [(labels(first[field]), labels(second[field])) for first, second in pairs]
        exact = sum(a == b for a, b in label_pairs) / len(label_pairs)
        mean_j = sum(jaccard(a, b) for a, b in label_pairs) / len(label_pairs)
        mf1 = micro_f1(label_pairs)
        multi_stats[name] = (exact, mean_j, mf1)
        universe = sorted(set().union(*(a | b for a, b in label_pairs)))
        for label in universe:
            a_bin = ["1" if label in a else "0" for a, _ in label_pairs]
            b_bin = ["1" if label in b else "0" for _, b in label_pairs]
            per_label_rows.append(
                {
                    "field": name,
                    "label": label,
                    "n_jointly_included": str(len(pairs)),
                    "first_positive": str(a_bin.count("1")),
                    "second_positive": str(b_bin.count("1")),
                    "raw_agreement": f"{raw_agreement(a_bin, b_bin):.6f}",
                    "cohen_kappa": f"{kappa(a_bin, b_bin):.6f}",
                }
            )
    return single_stats, multi_stats, per_label_rows


def main() -> int:
    all_comparisons: list[dict[str, str]] = []
    all_joint_pairs: list[tuple[dict[str, str], dict[str, str]]] = []
    batch_summary: list[tuple[str, int, int, int]] = []
    for batch, first_path, second_path in BATCHES:
        comparisons, joint_pairs = compare_batch(batch, first_path, second_path)
        eligibility_agreements = sum(
            row["eligibility_exact"] == "true" for row in comparisons
        )
        batch_summary.append(
            (batch, len(comparisons), eligibility_agreements, len(joint_pairs))
        )
        all_comparisons.extend(comparisons)
        all_joint_pairs.extend(joint_pairs)

    ids = [row["discovery_id"] for row in all_comparisons]
    if len(ids) != len(set(ids)):
        raise SystemExit("ERROR duplicate discovery IDs across coder batches")

    with COMPARISON.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(all_comparisons[0]))
        writer.writeheader()
        writer.writerows(all_comparisons)

    eligibility_a = [row["first_eligibility"] for row in all_comparisons]
    eligibility_b = [row["second_eligibility"] for row in all_comparisons]
    eligibility_stats = (
        raw_agreement(eligibility_a, eligibility_b),
        kappa(eligibility_a, eligibility_b),
    )
    single_stats, multi_stats, per_label_rows = stats_for_pairs(all_joint_pairs)

    with PER_LABEL.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(per_label_rows[0]))
        writer.writeheader()
        writer.writerows(per_label_rows)

    lines = [
        "# Final Multi-Source Search: All Independent-Coder Batches",
        "",
        "Eligibility agreement is calculated over every reviewed candidate. Analytical coding agreement is calculated only for records that both coders included at study level. Claim-boundary prose is not assigned a synthetic exact-agreement statistic.",
        "",
        "## Coverage",
        "",
        "| Batch | Reviewed | Eligibility exact | Jointly included |",
        "|---|---:|---:|---:|",
    ]
    for batch, reviewed, exact_n, joint_n in batch_summary:
        lines.append(f"| {batch} | {reviewed} | {exact_n}/{reviewed} | {joint_n} |")
    lines.extend(
        [
            f"| **All** | **{len(all_comparisons)}** | **{sum(x[2] for x in batch_summary)}/{len(all_comparisons)}** | **{len(all_joint_pairs)}** |",
            "",
            "## Eligibility",
            "",
            "| Raw agreement | Cohen's kappa |",
            "|---:|---:|",
            f"| {eligibility_stats[0]:.3f} | {eligibility_stats[1]:.3f} |",
            "",
            "## Single-Label Fields Among Jointly Included Records",
            "",
            "| Field | Raw agreement | Cohen's kappa |",
            "|---|---:|---:|",
        ]
    )
    for name, (raw, kap) in single_stats.items():
        lines.append(f"| {name} | {raw:.3f} | {kap:.3f} |")
    lines.extend(
        [
            "",
            "## Multi-Label Fields Among Jointly Included Records",
            "",
            "| Field | Row exact | Mean row Jaccard | Micro F1 |",
            "|---|---:|---:|---:|",
        ]
    )
    for name, (exact, mean_j, mf1) in multi_stats.items():
        lines.append(f"| {name} | {exact:.3f} | {mean_j:.3f} | {mf1:.3f} |")
    lines.extend(
        [
            "",
            "## Files",
            "",
            f"- `{COMPARISON.relative_to(ROOT).as_posix()}` preserves eligibility and label differences.",
            f"- `{PER_LABEL.relative_to(ROOT).as_posix()}` reports binary per-label agreement among jointly included records.",
            "",
            "No disagreement is automatically resolved by this script.",
        ]
    )
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(
        f"REVIEWED={len(all_comparisons)} ELIGIBILITY_EXACT={sum(x[2] for x in batch_summary)} "
        f"JOINTLY_INCLUDED={len(all_joint_pairs)}"
    )
    print(
        f"ELIGIBILITY raw={eligibility_stats[0]:.3f} kappa={eligibility_stats[1]:.3f}"
    )
    for name, (raw, kap) in single_stats.items():
        print(f"{name.upper()} raw={raw:.3f} kappa={kap:.3f}")
    for name, (exact, mean_j, mf1) in multi_stats.items():
        print(
            f"{name.upper()} exact={exact:.3f} jaccard={mean_j:.3f} micro_f1={mf1:.3f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
