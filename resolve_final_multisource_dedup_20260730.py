#!/usr/bin/env python3
"""Resolve candidate study/version pairs using identifiers and audited metadata."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
INPUT = DATA / "final_multisource_search_20260730_dedup_candidates.csv"
SCREENING = DATA / "final_multisource_search_20260730_complete_screening_proposal.csv"
OUTPUT = DATA / "final_multisource_search_20260730_dedup_resolutions.csv"
REPORT = ROOT / "FINAL_MULTISOURCE_DEDUP_RESOLUTION_20260730.md"

DISTINCT_PAIRS = {
    frozenset(("FMS0859", "CP193")),
    frozenset(("FMS0859", "FMS0862")),
    frozenset(("FMS0611", "FMS1235")),
    frozenset(("FMS0056", "CP146")),
    frozenset(("FMS0861", "FMS0872")),
}

METADATA_REVIEWED_SAME = {
    frozenset(("FMS0073", "FMS0860")),
    frozenset(("FMS0722", "FMS0730")),
    frozenset(("FMS1293", "FMS1307")),
    frozenset(("FMS0496", "CP133")),
    frozenset(("FMS0457", "FMS0708")),
    frozenset(("FMS0983", "FMS0984")),
    frozenset(("FMS1102", "FMS1499")),
    frozenset(("FMS1578", "CP075")),
    frozenset(("FMS1570", "CP224")),
    frozenset(("FMS0595", "CP129")),
}


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    candidates = read(INPUT)
    screening = {row["discovery_id"]: row for row in read(SCREENING)}
    output: list[dict[str, str]] = []
    unresolved = 0
    for row in candidates:
        left, right = row["left_id"], row["right_id"]
        pair = frozenset((left, right))
        match_basis = row["match_basis"]
        if pair in DISTINCT_PAIRS:
            decision = "distinct_studies"
            basis = "title similarity produced a false positive; titles, scopes, and available metadata describe different studies"
        elif pair in METADATA_REVIEWED_SAME:
            decision = "same_study_or_version"
            basis = "identifier, author, date, abstract, and/or system continuity establish a study/version relationship"
        elif left in screening and screening[left]["existing_canonical_study_id"] == right:
            decision = "same_study_or_version"
            basis = "exact match to the existing study by DOI, arXiv identifier, or normalized title"
        elif any(token in match_basis.split(";") for token in ("doi", "arxiv", "normalized_title")):
            decision = "same_study_or_version"
            basis = "exact DOI, arXiv identifier, or normalized-title match"
        else:
            decision = "needs_author_confirmation"
            basis = "title similarity alone is insufficient for an automated study/version decision"
            unresolved += 1
        output.append(
            {
                **row,
                "audit_decision": decision,
                "audit_basis": basis,
                "decision_provenance": "identifier and metadata audit; author confirmation pending",
            }
        )

    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(output[0]))
        writer.writeheader()
        writer.writerows(output)

    same = sum(row["audit_decision"] == "same_study_or_version" for row in output)
    distinct = sum(row["audit_decision"] == "distinct_studies" for row in output)
    lines = [
        "# Final Multi-Source Deduplication Resolution",
        "",
        f"Candidate pairs reviewed: **{len(output)}**.",
        f"Same-study/version relationships: **{same}**.",
        f"Distinct-study false positives: **{distinct}**.",
        f"Unresolved pairs: **{unresolved}**.",
        "",
        "Exact DOI and arXiv matches take precedence over title similarity. Exact normalized-title matches are treated as the same study record unless the metadata audit identifies a false positive. Title-similarity-only pairs require identifier, author, abstract, or system-continuity evidence.",
        "",
        "The resolved proposal is stored in `data/final_multisource_search_20260730_dedup_resolutions.csv`; final author confirmation remains explicit rather than being inferred by the script.",
    ]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"PAIRS={len(output)} SAME={same} DISTINCT={distinct} UNRESOLVED={unresolved}")
    return 0 if unresolved == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
