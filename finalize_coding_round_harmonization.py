from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
AUDIT = DATA / "coding_round_harmonization_audit.csv"
MATRIX = DATA / "current_study_level_coding_matrix_harmonized.csv"
STATS = DATA / "current_synthesis_statistics_by_round.csv"


def labels(value: str) -> list[str]:
    return [part.strip() for part in str(value or "").split(";") if part.strip()]


def count_multilabel(frame: pd.DataFrame, field: str) -> Counter[str]:
    counter: Counter[str] = Counter()
    for value in frame[field]:
        counter.update(labels(value))
    return counter


def add_stat_rows(rows: list[dict[str, object]], category: str, field: str,
                  initial: pd.DataFrame, update: pd.DataFrame) -> None:
    initial_counts = count_multilabel(initial, field)
    update_counts = count_multilabel(update, field)
    for label in sorted(set(initial_counts) | set(update_counts)):
        rows.append({
            "category": category,
            "label": label,
            "initial_cohort_count": initial_counts[label],
            "submission_update_cohort_count": update_counts[label],
            "combined_harmonized_count": initial_counts[label] + update_counts[label],
            "counting_unit": "target-software coded studies",
            "harmonization_status": "author_confirmed",
        })


def main() -> None:
    audit = pd.read_csv(AUDIT).fillna("")
    pending_mask = audit["author_review_status"].eq("pending_author_review")
    audit.loc[pending_mask, "author_review_status"] = "author_confirmed_2026-07-16"
    audit.loc[pending_mask, "final_harmonized_label"] = audit.loc[
        pending_mask, "current_codebook_candidate_label"
    ]
    audit.to_csv(AUDIT, index=False, quoting=csv.QUOTE_MINIMAL)

    matrix = pd.read_csv(MATRIX).fillna("")
    matrix["lifecycle_coverage"] = matrix["proposed_lifecycle_coverage"]
    matrix["cross_stage_capabilities"] = matrix["proposed_cross_stage_capabilities"]
    matrix["harmonization_status"] = "author_confirmed_2026-07-16"
    matrix = matrix.drop(columns=[
        "proposed_lifecycle_coverage",
        "proposed_cross_stage_capabilities",
    ])
    matrix.to_csv(MATRIX, index=False, quoting=csv.QUOTE_MINIMAL)

    target = matrix[matrix["analytical_role"].eq("target_software_study")]
    initial = target[target["coding_round"].eq("initial_frozen_round")]
    update = target[target["coding_round"].eq("submission_update_20260715")]
    rows: list[dict[str, object]] = []
    add_stat_rows(rows, "lifecycle_coverage", "lifecycle_coverage", initial, update)
    add_stat_rows(rows, "cross_stage_capability", "cross_stage_capabilities", initial, update)
    add_stat_rows(rows, "primary_system_shape", "primary_system_shape", initial, update)

    initial_evidence = initial["strongest_evidence_output"].value_counts().to_dict()
    update_evidence = update["strongest_evidence_output"].value_counts().to_dict()
    for label in sorted(set(initial_evidence) | set(update_evidence)):
        rows.append({
            "category": "strongest_evidence_output",
            "label": label,
            "initial_cohort_count": int(initial_evidence.get(label, 0)),
            "submission_update_cohort_count": int(update_evidence.get(label, 0)),
            "combined_harmonized_count": int(initial_evidence.get(label, 0)) + int(update_evidence.get(label, 0)),
            "counting_unit": "target-software coded studies",
            "harmonization_status": "author_confirmed",
        })

    governance = matrix[matrix["analytical_role"].eq("governance_boundary_case")]
    rows.append({
        "category": "governance_boundary",
        "label": "governance boundary case",
        "initial_cohort_count": len(governance[governance["coding_round"].eq("initial_frozen_round")]),
        "submission_update_cohort_count": len(governance[governance["coding_round"].eq("submission_update_20260715")]),
        "combined_harmonized_count": len(governance),
        "counting_unit": "governance boundary records",
        "harmonization_status": "author_confirmed",
    })
    pd.DataFrame(rows).to_csv(STATS, index=False, quoting=csv.QUOTE_MINIMAL)

    changed = audit[
        audit["author_review_status"].eq("author_confirmed_2026-07-16")
        & audit["original_label"].ne(audit["final_harmonized_label"])
    ]
    round_stats = pd.DataFrame(rows)
    shape_stats = round_stats[round_stats["category"].eq("primary_system_shape")]
    evidence_stats = round_stats[round_stats["category"].eq("strongest_evidence_output")]
    report = [
        "# Coding-Round Harmonization Report",
        "",
        "## Scope and status",
        "",
        "The frozen initial-round files and the adjudicated submission-update files remain unchanged. The author reviewed and accepted the evidence-linked harmonization candidates on 2026-07-16. The harmonized matrix applies one controlled schema across both rounds while retaining coding-round provenance and field-specific reliability scope.",
        "",
        f"- Study-level coded records: {len(matrix)} (67 target-software studies plus one governance boundary case).",
        f"- Author-confirmed substantive initial-round field changes: {len(changed)} across {changed['matrix_id'].nunique()} records.",
        "- New literature added by this pass: none.",
        "- New evidence-output category required: none.",
        "- Synthetic combined kappa computed: no.",
        "",
        "## Fields changed",
        "",
    ]
    for field, count in changed["field"].value_counts().items():
        report.append(f"- `{field}`: {count} author-confirmed changes.")
    report.extend([
        "",
        "Schema-only changes separated `primary_system_shape` from `overlay_tags`, renamed the validation-centered shape to include repair systems, and removed `role discussion / textual reflection` from the formal capability vocabulary while preserving it in `legacy_notes`.",
        "",
        "## Round-aware distributions",
        "",
        "The round differences narrow after the initial cohort is recoded at the July 15 granularity, especially for context aggregation, tool routing, feedback interpretation, and candidate analysis. Differences remain and should be read as cohort-specific descriptive variation rather than temporal evolution.",
        "",
        "### Primary system shapes",
        "",
        "| Shape | Initial | Update | Combined |",
        "|---|---:|---:|---:|",
    ])
    for _, row in shape_stats.iterrows():
        report.append(
            f"| {row['label']} | {row['initial_cohort_count']} | "
            f"{row['submission_update_cohort_count']} | {row['combined_harmonized_count']} |"
        )
    report.extend([
        "",
        "### Principal reported evidence outputs",
        "",
        "| Evidence output | Initial | Update | Combined |",
        "|---|---:|---:|---:|",
    ])
    for _, row in evidence_stats.iterrows():
        report.append(
            f"| {row['label']} | {row['initial_cohort_count']} | "
            f"{row['submission_update_cohort_count']} | {row['combined_harmonized_count']} |"
        )
    report.extend([
        "",
        "## Interpretation",
        "",
        "All four target-software system-shape patterns remain populated. Repair-oriented additions stretch the existing reproduction/validation shape rather than requiring a fifth category. Externally traceable material appears only in the update cohort under the current strongest-output coding, but no new evidence-output category is needed. The central workflow--capability--evidence conclusions are unchanged: broader Agentic action scope requires corresponding workflow and validation traces before stronger vulnerability claims can be supported.",
        "",
        "## Preservation and disclosure",
        "",
        "- Original author labels, independent-coder labels, and pre-adjudication reports remain preserved.",
        "- Every changed initial-round label is traceable through `data/coding_round_harmonization_audit.csv` to an existing frozen coding note or public-material audit location.",
        "- AI-assisted tools organized the comparison and drafted evidence-linked working notes. The author reviewed the underlying recorded evidence and accepted the final changes; AI output is not an independent human coding decision.",
    ])
    (ROOT / "CODING_ROUND_HARMONIZATION_REPORT.md").write_text(
        "\n".join(report) + "\n", encoding="utf-8"
    )

    print(f"author-confirmed audit changes: {len(changed)}")
    print(f"harmonized matrix rows: {len(matrix)}")
    print(f"round-stat rows: {len(rows)}")


if __name__ == "__main__":
    main()
