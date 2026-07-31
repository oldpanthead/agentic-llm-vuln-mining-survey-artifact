#!/usr/bin/env python3
"""Create a first-coder worksheet without exposing second-coder labels."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
SECOND = DATA / "final_multisource_search_20260730_second_coder_blind.csv"
OUTPUT = DATA / "final_multisource_search_20260730_first_coder.csv"

CODING_FIELDS = (
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
)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def work_present(path: Path) -> bool:
    if not path.exists():
        return False
    return any(row.get(field, "").strip() for row in read_rows(path) for field in CODING_FIELDS)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    if work_present(OUTPUT) and not args.force:
        raise SystemExit(f"ERROR: refusing to overwrite coder work in {OUTPUT.name}")

    output_rows = []
    for source in read_rows(SECOND):
        # Copy metadata only. No second-coder decision or label is read into the
        # first-coder worksheet.
        row = {
            "review_order": source["review_order"],
            "discovery_id": source["discovery_id"],
            "title": source["title"],
            "publication_dates": source["publication_dates"],
            "doi": source["doi"],
            "arxiv_id": source["arxiv_id"],
            "public_fulltext_url": source["public_fulltext_url"],
            "local_review_pdf": source["local_review_pdf"],
            "local_extracted_text": source["local_extracted_text"],
        }
        for field in CODING_FIELDS:
            row[field] = ""
        output_rows.append(row)

    fields = list(output_rows[0])
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(output_rows)
    print(f"WROTE {OUTPUT} ({len(output_rows)} rows; second-coder labels not copied)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
