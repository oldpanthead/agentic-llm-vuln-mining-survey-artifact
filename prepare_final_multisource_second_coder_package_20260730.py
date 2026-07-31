#!/usr/bin/env python3
"""Prepare a blind human-review package for final-search candidates.

The package contains no author or AI-assisted inclusion/coding labels. It is
limited to candidates with a locally cached public full text. Candidates whose
full text could not be retrieved remain in a separate access-resolution queue.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
ASSESSMENT = DATA / "final_multisource_search_20260730_fulltext_assessment.csv"
ACCESS = DATA / "final_multisource_search_20260730_fulltext_access.csv"
BLIND_OUTPUT = DATA / "final_multisource_search_20260730_second_coder_blind.csv"
UNRESOLVED_OUTPUT = DATA / "final_multisource_search_20260730_fulltext_unresolved.csv"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise SystemExit(f"ERROR no rows prepared for {path.name}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def coder_work_present(path: Path) -> bool:
    if not path.exists():
        return False
    protected_fields = {
        "eligibility_decision",
        "eligibility_reason",
        "final_lifecycle_coverage",
        "final_cross_stage_capabilities",
        "final_primary_system_shape",
        "final_principal_reported_evidence_output",
        "final_external_traceability",
        "final_claim_boundary",
        "material_checked",
        "decision_note",
        "uncertainty_note",
        "row_status",
    }
    return any(
        row.get(field, "").strip()
        for row in read_rows(path)
        for field in protected_fields
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--force",
        action="store_true",
        help="overwrite an existing blind file even if coder-entered values are present",
    )
    args = parser.parse_args()

    if coder_work_present(BLIND_OUTPUT) and not args.force:
        raise SystemExit(
            "ERROR: coder-entered values are present in "
            f"{BLIND_OUTPUT.name}; refusing to overwrite them without --force"
        )

    assessments = {
        row["discovery_id"]: row
        for row in read_rows(ASSESSMENT)
        if row["ai_assisted_proposed_decision"] == "study_level_candidate"
    }
    access = {row["discovery_id"]: row for row in read_rows(ACCESS)}

    blind_rows: list[dict[str, str]] = []
    unresolved_rows: list[dict[str, str]] = []
    for review_order, discovery_id in enumerate(sorted(assessments), start=1):
        row = assessments[discovery_id]
        material = access[discovery_id]
        common = {
            "review_order": str(review_order),
            "discovery_id": discovery_id,
            "title": row["title"],
            "publication_dates": row["publication_dates"],
            "doi": row["doi"],
            "arxiv_id": row["arxiv_id"],
            "public_fulltext_url": material["public_fulltext_url"],
            "local_review_pdf": material["local_review_pdf"],
            "local_extracted_text": material["local_extracted_text"],
        }
        if material["access_status"] == "downloaded_and_text_extracted":
            blind_rows.append(
                {
                    **common,
                    "eligibility_decision": "",
                    "eligibility_reason": "",
                    "final_lifecycle_coverage": "",
                    "lifecycle_review_status": "",
                    "final_cross_stage_capabilities": "",
                    "capability_review_status": "",
                    "final_primary_system_shape": "",
                    "shape_review_status": "",
                    "final_principal_reported_evidence_output": "",
                    "evidence_review_status": "",
                    "final_external_traceability": "",
                    "traceability_review_status": "",
                    "final_claim_boundary": "",
                    "claim_boundary_review_status": "",
                    "material_checked": "",
                    "decision_note": "",
                    "uncertainty_note": "",
                    "row_status": "",
                }
            )
        else:
            unresolved_rows.append(
                {
                    **common,
                    "access_status": material["access_status"],
                    "access_basis": material["access_basis"],
                    "access_note": material["notes"],
                    "resolution_status": "public_full_text_needed",
                    "resolved_public_url": "",
                    "resolved_local_path": "",
                    "resolution_note": "",
                }
            )

    write_rows(BLIND_OUTPUT, blind_rows)
    write_rows(UNRESOLVED_OUTPUT, unresolved_rows)
    print(f"WROTE {BLIND_OUTPUT} ({len(blind_rows)} blind-review rows)")
    print(f"WROTE {UNRESOLVED_OUTPUT} ({len(unresolved_rows)} unresolved rows)")


if __name__ == "__main__":
    main()
