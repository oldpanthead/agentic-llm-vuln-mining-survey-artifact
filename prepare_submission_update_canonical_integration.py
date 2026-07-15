#!/usr/bin/env python3
"""Assess canonical-study integration for the 2026-07-15 update cohort.

The script does not modify the frozen corpus. It compares the 41 adjudicated
update records against the current source-record corpus and canonical
study/version crosswalk, then writes an auditable integration crosswalk and a
projected-count report.
"""

from __future__ import annotations

import csv
import re
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"

ADJUDICATED = DATA / "submission_update_20260715_adjudicated.csv"
UPDATE_METADATA = DATA / "submission_update_20260715_arxiv_results.csv"
CORPUS = DATA / "corpus.csv"
CURRENT_CROSSWALK = DATA / "study_version_crosswalk.csv"
OUTPUT = DATA / "submission_update_20260715_canonical_integration_crosswalk.csv"
REPORT = ROOT / "SUBMISSION_UPDATE_CANONICAL_INTEGRATION_REPORT.md"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def normalize_title(value: str) -> str:
    value = value.lower().replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return " ".join(value.split())


def arxiv_ids(value: str) -> set[str]:
    return set(re.findall(r"\b\d{4}\.\d{4,5}\b", (value or "").lower()))


def normalize_doi(value: str) -> str:
    match = re.search(r"10\.\d{4,9}/[^\s?#]+", (value or "").lower())
    return match.group(0).rstrip(".,;)") if match else ""


def main() -> None:
    adjudicated = read_csv(ADJUDICATED)
    metadata_rows = read_csv(UPDATE_METADATA)
    corpus_rows = read_csv(CORPUS)
    canonical_rows = read_csv(CURRENT_CROSSWALK)

    if len(adjudicated) != 41:
        raise SystemExit(f"Expected 41 adjudicated rows; found {len(adjudicated)}")
    if any(row.get("adjudication_status") != "author_confirmed_evidence_based_resolution" for row in adjudicated):
        raise SystemExit("Adjudicated rows are not author-confirmed")

    metadata_by_id = {row["arxiv_id"]: row for row in metadata_rows}
    if len(metadata_by_id) != len(metadata_rows):
        raise SystemExit("Update metadata contains duplicate arXiv IDs")

    current_by_record = {row["record_id"]: row for row in canonical_rows}
    current_counted = [row for row in canonical_rows if row["counting_status"] == "canonical_counted"]
    current_layer_counts = Counter(row["analytical_layer"] for row in current_counted)

    corpus_index: list[dict[str, object]] = []
    for row in corpus_rows:
        corpus_index.append({
            "row": row,
            "title_norm": normalize_title(row["title"]),
            "arxiv_ids": arxiv_ids(" ".join([row.get("title", ""), row.get("doi_or_url", ""), row.get("note", "")])),
            "doi": normalize_doi(row.get("doi_or_url", "")),
        })

    output_rows: list[dict[str, str]] = []
    similarity_review: list[tuple[str, str, str, float]] = []
    for row in adjudicated:
        update_id = row["update_id"]
        arxiv_id = row["arxiv_id"]
        meta = metadata_by_id.get(arxiv_id)
        if not meta:
            raise SystemExit(f"Missing update metadata for {update_id} / {arxiv_id}")

        title_norm = normalize_title(row["title"])
        doi = normalize_doi(meta.get("doi", ""))
        exact_matches: list[tuple[str, str]] = []
        best_similarity = 0.0
        best_record = ""
        best_title = ""
        for item in corpus_index:
            existing = item["row"]
            reasons: list[str] = []
            if arxiv_id in item["arxiv_ids"]:
                reasons.append("same_arxiv_id")
            if title_norm == item["title_norm"]:
                reasons.append("exact_normalized_title")
            if doi and doi == item["doi"]:
                reasons.append("same_doi")
            if reasons:
                exact_matches.append((existing["record_id"], "+".join(reasons)))
            similarity = SequenceMatcher(None, title_norm, item["title_norm"]).ratio()
            if similarity > best_similarity:
                best_similarity = similarity
                best_record = existing["record_id"]
                best_title = existing["title"]

        if exact_matches:
            match_records = ";".join(record for record, _ in exact_matches)
            match_basis = ";".join(f"{record}:{basis}" for record, basis in exact_matches)
            primary_record = exact_matches[0][0]
            existing_canonical = current_by_record.get(primary_record, {}).get("canonical_study_id", "")
            integration_status = "existing_study_or_alternate_version"
            proposed_canonical = existing_canonical
            counted_after_integration = "no"
        elif best_similarity >= 0.80:
            match_records = best_record
            match_basis = f"high_title_similarity={best_similarity:.3f}"
            integration_status = "needs_manual_review"
            proposed_canonical = ""
            counted_after_integration = "pending"
            similarity_review.append((update_id, best_record, best_title, best_similarity))
        else:
            match_records = ""
            match_basis = f"no_identifier_or_title_match;best_title_similarity={best_similarity:.3f}"
            integration_status = "new_canonical_study"
            proposed_canonical = f"CS_UPDATE_{update_id}"
            counted_after_integration = "yes"

        analytical_layer = (
            "study_level_coded"
            if row["proposed_analysis_layer"] == "study_level_candidate"
            else "extended_synthesis"
        )
        output_rows.append({
            "update_id": update_id,
            "arxiv_id": arxiv_id,
            "title": row["title"],
            "authors": meta.get("authors", ""),
            "official_url": meta.get("official_url", ""),
            "doi": meta.get("doi", ""),
            "adjudicated_analytical_layer": analytical_layer,
            "matched_existing_record_id": match_records,
            "proposed_canonical_study_id": proposed_canonical,
            "match_basis": match_basis,
            "best_existing_title": best_title,
            "integration_status": integration_status,
            "counted_after_integration": counted_after_integration,
            "integration_note": "Canonical integration is projected here; the frozen corpus is not modified by this script.",
        })

    fields = list(output_rows[0])
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(output_rows)

    status_counts = Counter(row["integration_status"] for row in output_rows)
    new_rows = [row for row in output_rows if row["integration_status"] == "new_canonical_study"]
    new_layers = Counter(row["adjudicated_analytical_layer"] for row in new_rows)
    projected_layers = current_layer_counts + new_layers
    projected_source_records = len(corpus_rows) + len(output_rows)
    projected_canonical = len(current_counted) + len(new_rows)

    report = f"""# Submission Update Canonical Integration Report

## Scope

This report compares the 41 author-confirmed update-search records with the current source-record corpus and canonical study/version crosswalk. It uses exact arXiv IDs, DOI identifiers, normalized titles, and conservative title-similarity review. The assessment does not modify the frozen corpus or manuscript.

## Match Outcome

- Update records assessed: {len(output_rows)}
- New canonical studies: {status_counts['new_canonical_study']}
- Existing-study or alternate-version matches: {status_counts['existing_study_or_alternate_version']}
- Manual-review matches: {status_counts['needs_manual_review']}
- New study-level coded candidates after this pass: {new_layers['study_level_coded']}
- New extended-synthesis studies after this pass: {new_layers['extended_synthesis']}

No exact arXiv-ID, DOI, URL-derived arXiv-ID, or normalized-title match was found against the existing 212 source records. The highest title similarities are retained in `data/submission_update_20260715_canonical_integration_crosswalk.csv` for inspection; similarities below 0.80 are treated as topical naming overlap rather than version identity.

## Current and Projected Counts

| Analytical view | Current frozen count | Projected after canonical integration |
|---|---:|---:|
| Source records | {len(corpus_rows)} | {projected_source_records} |
| Canonical candidate studies | {len(current_counted)} | {projected_canonical} |
| Study-level coded records, including the governance boundary case | {current_layer_counts['study_level_coded']} | {projected_layers['study_level_coded']} |
| Extended-synthesis studies | {current_layer_counts['extended_synthesis']} | {projected_layers['extended_synthesis']} |
| Background/reference studies | {current_layer_counts['background_reference']} | {projected_layers['background_reference']} |
| Excluded near-neighbor studies | {current_layer_counts['excluded_near_neighbor']} | {projected_layers['excluded_near_neighbor']} |

The projected study-level total is 67 target-software studies plus the existing governance boundary case. These projected counts must not be used in the manuscript until corpus rows, canonical crosswalks, coding matrices, descriptive distributions, and manuscript tables are updated together.

## Manual Review

"""
    if similarity_review:
        for update_id, record_id, title, similarity in similarity_review:
            report += f"- {update_id} versus {record_id}: {similarity:.3f}; {title}\n"
    else:
        report += "No unresolved canonical-identity match exceeded the 0.80 manual-review threshold.\n"

    report += """

## Integration Boundary

The 37/4 analytical-layer decision is final for the update cohort, but canonical corpus integration remains a separate release operation. The existing 31-record second-coder statistics continue to describe the frozen 30-target-study-plus-one-governance set; the update cohort has its own pre-adjudication agreement report. No combined reliability statistic is inferred from the two rounds.
"""
    REPORT.write_text(report, encoding="utf-8")

    print(f"WROTE {OUTPUT.relative_to(ROOT)} ({len(output_rows)} rows)")
    print(f"WROTE {REPORT.relative_to(ROOT)}")
    print(f"INTEGRATION_STATUS {dict(sorted(status_counts.items()))}")
    print(f"PROJECTED_SOURCE_RECORDS {projected_source_records}")
    print(f"PROJECTED_CANONICAL_STUDIES {projected_canonical}")
    print(f"PROJECTED_LAYERS {dict(sorted(projected_layers.items()))}")


if __name__ == "__main__":
    main()
