#!/usr/bin/env python3
"""Finalize the author-confirmed 2026-07-15 update adjudication.

This script promotes the evidence-based working draft without overwriting the
frozen author audit, independent coder2 results, or pre-adjudication report.
The author confirmed the proposed resolution on 2026-07-15. The resulting file
records an author-confirmed analytical decision, not a two-human consensus or a
third-coder adjudication.
"""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
REPORTS = ROOT / "reports"

INPUT_PATH = DATA / "submission_update_20260715_adjudication_working_draft.csv"
OUTPUT_PATH = DATA / "submission_update_20260715_adjudicated.csv"
REPORT_PATH = REPORTS / "SUBMISSION_UPDATE_ADJUDICATION_REPORT.md"

CONFIRMED_STATUS = "author_confirmed_evidence_based_resolution"


def main() -> None:
    with INPUT_PATH.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        source_rows = list(reader)
        source_fields = reader.fieldnames or []

    if len(source_rows) != 41:
        raise SystemExit(f"Expected 41 working-draft rows; found {len(source_rows)}")
    if any(row.get("adjudication_status") != "assistant_proposed_pending_author_confirmation" for row in source_rows):
        raise SystemExit("Working draft contains an unexpected adjudication status")

    final_rows: list[dict[str, str]] = []
    for row in source_rows:
        final = dict(row)
        final["adjudication_status"] = CONFIRMED_STATUS
        final_rows.append(final)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=source_fields)
        writer.writeheader()
        writer.writerows(final_rows)

    layers = Counter(row["proposed_analysis_layer"] for row in final_rows)
    evidence = Counter(row["proposed_strongest_evidence_output"] for row in final_rows)
    traceability = Counter(row["proposed_external_traceability"] for row in final_rows)
    if layers != Counter({"study_level_candidate": 37, "extended_synthesis": 4}):
        raise SystemExit(f"Unexpected confirmed layer counts: {dict(layers)}")

    REPORTS.mkdir(parents=True, exist_ok=True)
    report = f"""# Submission Update Adjudication Report

## Scope and Status

- Update-search records: 41
- Independent coder2 pass: complete
- Pre-adjudication agreement: reported separately in `reports/SUBMISSION_UPDATE_SECOND_CODER_PRE_ADJUDICATION_REPORT.md`
- Author confirmation date: 2026-07-15
- Final record: `data/submission_update_20260715_adjudicated.csv`

The assistant prepared an evidence-based field resolution from the frozen author audit, the independent coder2 decisions, the public review material, and the operational codebook. The author reviewed and accepted that resolution. This is an author-confirmed analytical decision; it is not represented as a discussion between two human coders, a two-human consensus round, or a third-coder adjudication. The original author and coder2 labels remain unchanged in their source files and are retained side by side in the final record.

## Confirmed Analytical-Layer Outcome

- Study-level candidates: {layers['study_level_candidate']}
- Extended-synthesis records: {layers['extended_synthesis']}
- Extended-synthesis IDs: U19, U20, U24, and U30
- U24 (SynthFix) is assigned to extended synthesis under the observable-workflow rule.

## Confirmed Evidence and Traceability Profiles

- Strongest-evidence distribution: {dict(sorted(evidence.items()))}
- External-traceability distribution: {dict(sorted(traceability.items()))}

These are adjudicated labels for the 41-record update set. They do not replace or alter the previously reported pre-adjudication agreement statistics. Canonical matching against the existing corpus is reported separately; coordinated corpus and manuscript integration remains required before any denominator is changed.

## Preservation Boundary

- `data/submission_update_20260715_full_coding_audit.csv` remains the frozen author audit.
- `data/submission_update_20260715_second_coder_results.csv` remains the frozen independent coder2 result.
- `data/submission_update_20260715_adjudication_working_draft.csv` remains the assistant-prepared proposal as reviewed by the author.
- No post-adjudication agreement statistic is reported.
"""
    REPORT_PATH.write_text(report, encoding="utf-8")

    print(f"WROTE {OUTPUT_PATH.relative_to(ROOT)} ({len(final_rows)} rows)")
    print(f"WROTE {REPORT_PATH.relative_to(ROOT)}")
    print(f"CONFIRMED_LAYER_COUNTS {dict(sorted(layers.items()))}")


if __name__ == "__main__":
    main()
