#!/usr/bin/env python3
"""Prepare source-grounded reference metadata for new study-level records."""

from __future__ import annotations

import csv
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RESULTS = DATA / "final_multisource_search_20260730_results.csv"
SCREENING = DATA / "final_multisource_search_20260730_complete_screening_proposal.csv"
NEW_MATRIX = DATA / "final_multisource_search_20260730_new_study_level_coding.csv"
OLD_AUDIT = DATA / "reference_audit_pre_final_multisource_20260730.csv"

OUTPUT_BIB = ROOT / "references_final_multisource_new_studies_20260730.bib"
OUTPUT_AUDIT = DATA / "reference_audit_proposed_20260730.csv"
OUTPUT_FINAL_AUDIT = DATA / "reference_audit.csv"
OUTPUT_METADATA = DATA / "final_multisource_new_study_reference_metadata_20260730.csv"
OUTPUT_REPORT = ROOT / "FINAL_MULTISOURCE_REFERENCE_METADATA_20260730.md"


# Official citation metadata for records whose source export omitted the venue.
DOI_METADATA_OVERRIDES = {
    "10.18653/v1/2025.naacl-long.212": {
        "record_type": "conference-paper",
        "venue_or_source": (
            "Proceedings of the 2025 Conference of the Nations of the Americas "
            "Chapter of the Association for Computational Linguistics: Human "
            "Language Technologies (Volume 1: Long Papers)"
        ),
        "publisher": "Association for Computational Linguistics",
        "pages": "4207--4224",
        "url": "https://aclanthology.org/2025.naacl-long.212/",
    },
    "10.18653/v1/2025.emnlp-main.802": {
        "record_type": "conference-paper",
        "venue_or_source": (
            "Proceedings of the 2025 Conference on Empirical Methods in "
            "Natural Language Processing"
        ),
        "publisher": "Association for Computational Linguistics",
        "pages": "15879--15905",
        "url": "https://aclanthology.org/2025.emnlp-main.802/",
    },
    "10.21203/rs.3.rs-7582841/v1": {
        "record_type": "posted-content",
        "venue_or_source": "Research Square preprint",
        "publisher": "Springer Nature",
    },
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def norm(value: str) -> str:
    value = (value or "").casefold()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return " ".join(value.split())


def clean(value: str) -> str:
    return " ".join((value or "").strip().split())


def latex(value: str) -> str:
    value = clean(value)
    for old, new in (("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"), ("#", r"\#"), ("_", r"\_")):
        value = value.replace(old, new)
    return value


def candidate_score(row: dict[str, str]) -> tuple[int, int, int, int, int]:
    source = clean(row["source_id"]).lower()
    record_type = clean(row["record_type"]).lower()
    formal = int(bool(clean(row["doi"])) and source != "arxiv")
    proceedings_or_journal = int("proceed" in record_type or "journal" in record_type)
    has_authors = int(bool(clean(row["authors"])))
    has_venue = int(bool(clean(row["venue_or_source"])))
    source_priority = {
        "acm_crossref": 8,
        "ieee_crossref": 8,
        "springer_crossref": 8,
        "elsevier_crossref": 8,
        "crossref": 7,
        "openalex": 6,
        "arxiv": 5,
    }.get(source, 1)
    return formal, proceedings_or_journal, has_authors, has_venue, source_priority


def publication_status(row: dict[str, str]) -> str:
    source = clean(row["source_id"]).lower()
    record_type = clean(row["record_type"]).lower()
    venue = clean(row["venue_or_source"]).lower()
    if source == "arxiv" or "preprint" in record_type or "posted" in record_type or "preprint" in venue or venue == "arxiv":
        return "preprint"
    if "proceed" in record_type or "conference" in record_type or "conference" in venue or "symposium" in venue:
        return "conference"
    if "journal" in record_type or clean(row["doi"]):
        return "journal"
    return "report/other"


def bib_entry(key: str, row: dict[str, str]) -> str:
    status = publication_status(row)
    record_type = clean(row["record_type"]).lower()
    if status == "conference" or "proceed" in record_type:
        entry_type = "inproceedings"
        venue_field = "booktitle"
    elif status == "journal":
        entry_type = "article"
        venue_field = "journal"
    else:
        entry_type = "misc"
        venue_field = "howpublished"

    authors = " and ".join(latex(part) for part in clean(row["authors"]).split(";") if clean(part))
    title = latex(row["title"])
    year = clean(row["year"]) or clean(row["publication_date"])[:4]
    venue = clean(row["venue_or_source"])
    if entry_type == "misc" and not venue:
        venue = "arXiv preprint" if clean(row["arxiv_id"]) else "Public report"

    fields = [("author", authors or "{Metadata unavailable}"), ("title", "{" + title + "}"), ("year", year)]
    if venue:
        fields.append((venue_field, latex(venue)))
    if clean(row.get("publisher", "")):
        fields.append(("publisher", latex(row["publisher"])))
    if clean(row.get("pages", "")):
        fields.append(("pages", clean(row["pages"])))
    if clean(row["doi"]):
        fields.append(("doi", clean(row["doi"])))
    if clean(row["arxiv_id"]):
        fields.append(("eprint", clean(row["arxiv_id"])))
        fields.append(("archivePrefix", "arXiv"))
    if clean(row["url"]):
        fields.append(("url", clean(row["url"])))
    body = ",\n".join(f"  {name} = {{{value}}}" for name, value in fields)
    return f"@{entry_type}{{{key},\n{body}\n}}"


def main() -> int:
    results = read_rows(RESULTS)
    screening = {row["discovery_id"]: row for row in read_rows(SCREENING)}
    matrix = read_rows(NEW_MATRIX)
    old_audit = read_rows(OLD_AUDIT)

    by_title: dict[str, list[dict[str, str]]] = defaultdict(list)
    by_doi: dict[str, list[dict[str, str]]] = defaultdict(list)
    by_arxiv: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in results:
        by_title[norm(row["title"])].append(row)
        if clean(row["doi"]):
            by_doi[clean(row["doi"]).lower()].append(row)
        if clean(row["arxiv_id"]):
            by_arxiv[clean(row["arxiv_id"]).lower()].append(row)

    metadata_rows: list[dict[str, str]] = []
    bib_entries: list[str] = []
    audit_additions: list[dict[str, str]] = []
    missing: list[tuple[str, str, str]] = []
    for study in matrix:
        record_id = study["record_id"]
        screen = screening[record_id]
        candidates: list[dict[str, str]] = []
        doi = clean(screen["doi"]).lower()
        arxiv = clean(screen["arxiv_id"]).lower()
        if doi:
            candidates.extend(by_doi.get(doi, []))
        if arxiv:
            candidates.extend(by_arxiv.get(arxiv, []))
        candidates.extend(by_title.get(norm(screen["title"]), []))
        unique = {(row["source_id"], row["source_record_id"], row["url"]): row for row in candidates}
        candidates = list(unique.values())
        if not candidates:
            missing.append((record_id, study["title"], "no matching source metadata"))
            continue
        chosen = dict(max(candidates, key=candidate_score))
        chosen.update(DOI_METADATA_OVERRIDES.get(clean(chosen["doi"]).lower(), {}))
        key = record_id.lower()
        status = publication_status(chosen)
        official_url = clean(chosen["url"]) or clean(study["official_url"])
        metadata_rows.append(
            {
                "record_id": record_id,
                "citation_key": key,
                "title": study["title"],
                "authors": clean(chosen["authors"]),
                "year": clean(chosen["year"]) or clean(chosen["publication_date"])[:4],
                "publication_status": status,
                "venue_or_source": clean(chosen["venue_or_source"]),
                "publisher": clean(chosen["publisher"]),
                "doi": clean(chosen["doi"]) or clean(screen["doi"]),
                "arxiv_id": clean(chosen["arxiv_id"]) or clean(screen["arxiv_id"]),
                "official_url": official_url,
                "selected_source_id": chosen["source_id"],
                "selected_source_record_id": chosen["source_record_id"],
                "selection_basis": "formal metadata preferred; otherwise best available public metadata",
                "metadata_status": "complete" if clean(chosen["authors"]) and (clean(chosen["year"]) or clean(chosen["publication_date"])) and official_url else "incomplete",
            }
        )
        bib_entries.append(bib_entry(key, {**chosen, "title": study["title"], "url": official_url}))
        audit_additions.append(
            {
                "record_id": record_id,
                "canonical_title": study["title"],
                "system_alias": study["system_alias"],
                "publication_status": status,
                "venue": clean(chosen["venue_or_source"]),
                "official_url": official_url,
                "arxiv_id": clean(chosen["arxiv_id"]) or clean(screen["arxiv_id"]),
                "doi": clean(chosen["doi"]) or clean(screen["doi"]),
                "last_verified_date": "2026-07-30",
                "note": "New target-software study from the integrated multi-source search through 2026-07-30.",
                "citation_key": key,
            }
        )

    if len(metadata_rows) != len(matrix):
        details = "; ".join(f"{record_id}: {reason}" for record_id, _, reason in missing)
        raise SystemExit(f"ERROR: metadata resolved for {len(metadata_rows)}/{len(matrix)} studies. {details}")
    if len({row["citation_key"] for row in metadata_rows}) != len(metadata_rows):
        raise SystemExit("ERROR: duplicate generated citation keys")

    write_rows(OUTPUT_METADATA, metadata_rows)
    write_rows(OUTPUT_AUDIT, old_audit + audit_additions)
    write_rows(OUTPUT_FINAL_AUDIT, old_audit + audit_additions)
    OUTPUT_BIB.write_text("\n\n".join(bib_entries) + "\n", encoding="utf-8")

    incomplete = [row for row in metadata_rows if row["metadata_status"] != "complete"]
    statuses = defaultdict(int)
    sources = defaultdict(int)
    for row in metadata_rows:
        statuses[row["publication_status"]] += 1
        sources[row["selected_source_id"]] += 1
    lines = [
        "# Final Multi-Source Reference Metadata",
        "",
        f"Metadata records prepared: **{len(metadata_rows)}**.",
        f"Incomplete records: **{len(incomplete)}**.",
        "",
        "## Publication Status",
        "",
        "| Status | Count |",
        "|---|---:|",
    ]
    for status, count in sorted(statuses.items()):
        lines.append(f"| {status} | {count} |")
    lines.extend(["", "## Selected Metadata Sources", "", "| Source | Count |", "|---|---:|"])
    for source, count in sorted(sources.items()):
        lines.append(f"| {source} | {count} |")
    lines.extend(
        [
            "",
            "## Outputs",
            "",
            f"- `{OUTPUT_METADATA.relative_to(ROOT).as_posix()}`",
            f"- `{OUTPUT_AUDIT.relative_to(ROOT).as_posix()}`",
            f"- `{OUTPUT_FINAL_AUDIT.relative_to(ROOT).as_posix()}`",
            f"- `{OUTPUT_BIB.relative_to(ROOT).as_posix()}`",
            "",
            "The script uses saved source exports plus the documented official citation-metadata overrides above; it performs no live network lookup.",
        ]
    )
    if incomplete:
        lines.extend(["", "## Incomplete Records", ""])
        for row in incomplete:
            lines.append(f"- {row['record_id']}: {row['title']}")
    OUTPUT_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"NEW_REFERENCES={len(metadata_rows)} INCOMPLETE={len(incomplete)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
