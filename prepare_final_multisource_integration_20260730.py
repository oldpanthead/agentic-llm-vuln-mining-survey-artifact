#!/usr/bin/env python3
"""Prepare, but never adjudicate, the final multi-source integration queue.

This script joins the full-text assessment, human second-coder review, and
existing study/version crosswalk. It does not update the released corpus or
choose between disagreements. Final integration remains blocked until the
human review and author confirmation fields are complete.
"""

from __future__ import annotations

import argparse
import csv
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
ASSESSMENT = DATA / "final_multisource_search_20260730_fulltext_assessment.csv"
CODER = DATA / "final_multisource_search_20260730_second_coder_blind.csv"
CROSSWALK = DATA / "study_version_crosswalk.csv"
CORPUS = DATA / "corpus.csv"
REFERENCE_AUDIT = DATA / "reference_audit.csv"
QUEUE = DATA / "final_multisource_search_20260730_integration_queue.csv"
SUMMARY = ROOT / "FINAL_MULTISOURCE_INTEGRATION_PRECHECK_20260730.md"

AUTHOR_LAYERS = {
    "study_level",
    "extended_synthesis",
    "background_reference",
    "excluded_near_neighbor",
    "version_reconciliation",
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_rows(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def clean(value: str | None) -> str:
    return (value or "").strip()


def normalized_title(value: str) -> str:
    text = unicodedata.normalize("NFKD", value).casefold()
    return re.sub(r"[^a-z0-9]+", "", text)


def normalized_doi(value: str) -> str:
    value = clean(value).casefold()
    value = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", value)
    return value.rstrip("/.,; ")


def normalized_arxiv(value: str) -> str:
    value = clean(value).casefold()
    value = re.sub(r"^https?://arxiv\.org/(?:abs|pdf)/", "", value)
    return value.removesuffix(".pdf").split("v", 1)[0]


def identifier_from_url(value: str) -> tuple[str, str] | None:
    value = clean(value)
    doi = normalized_doi(value)
    if doi.startswith("10."):
        return ("doi", doi)
    arxiv = normalized_arxiv(value)
    if re.fullmatch(r"\d{4}\.\d{4,5}", arxiv):
        return ("arxiv", arxiv)
    return None


def author_layer(row: dict[str, str]) -> str:
    decision = clean(row.get("author_final_decision"))
    if decision in AUTHOR_LAYERS:
        return decision
    return ""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--require-ready",
        action="store_true",
        help="fail unless all author confirmations and required second-coder rows are complete",
    )
    args = parser.parse_args()

    assessments = read_rows(ASSESSMENT)
    coder_rows = {row["discovery_id"]: row for row in read_rows(CODER)}
    crosswalk = read_rows(CROSSWALK)
    corpus = read_rows(CORPUS)
    reference_audit = read_rows(REFERENCE_AUDIT)

    existing_keys: dict[tuple[str, str], set[str]] = defaultdict(set)
    for row in crosswalk:
        record = clean(row.get("canonical_study_id")) or clean(row.get("record_id"))
        for key_type, key in (("title", normalized_title(clean(row.get("title")))),):
            if key:
                existing_keys[(key_type, key)].add(record)
    for row in corpus:
        record = clean(row.get("record_id"))
        title_key = normalized_title(clean(row.get("title")))
        if title_key:
            existing_keys[("title", title_key)].add(record)
        identifier = identifier_from_url(clean(row.get("doi_or_url")))
        if identifier:
            existing_keys[identifier].add(record)
    for row in reference_audit:
        record = clean(row.get("record_id"))
        for key_type, key in (
            ("title", normalized_title(clean(row.get("canonical_title")))),
            ("doi", normalized_doi(clean(row.get("doi")))),
            ("arxiv", normalized_arxiv(clean(row.get("arxiv_id")))),
        ):
            if key:
                existing_keys[(key_type, key)].add(record)
        identifier = identifier_from_url(clean(row.get("official_url")))
        if identifier:
            existing_keys[identifier].add(record)

    queue_rows: list[dict[str, str]] = []
    readiness_problems: list[str] = []
    duplicate_groups: dict[tuple[str, str], list[str]] = defaultdict(list)
    status_counts: Counter[str] = Counter()

    for row in assessments:
        discovery_id = row["discovery_id"]
        coder = coder_rows.get(discovery_id, {})
        proposed = clean(row.get("ai_assisted_proposed_layer"))
        final_layer = author_layer(row)
        author_confirmed = clean(row.get("human_confirmation_status")).casefold() in {
            "confirmed",
            "complete",
            "author_confirmed",
        }
        # Membership in the generated blind file is the authoritative signal;
        # the assessment column is retained for provenance and may be blank.
        coder_required = discovery_id in coder_rows
        coder_complete = clean(coder.get("row_status")).casefold() == "complete"
        coder_decision = clean(coder.get("eligibility_decision"))

        if not final_layer or not author_confirmed:
            readiness_problems.append(f"{discovery_id}: author final decision not confirmed")
        if coder_required and not coder_complete:
            readiness_problems.append(f"{discovery_id}: required second-coder row incomplete")

        if not final_layer:
            comparison = "awaiting_author_confirmation"
        elif coder_required and not coder_complete:
            comparison = "awaiting_second_coder"
        elif coder_required:
            coder_layer = "study_level" if coder_decision == "include_study_level" else "not_study_level"
            if final_layer == "study_level" and coder_layer == "study_level":
                comparison = "eligibility_agreement_study_level"
            elif final_layer != "study_level" and coder_layer == "not_study_level":
                comparison = "eligibility_agreement_not_study_level"
            else:
                comparison = "eligibility_disagreement_requires_confirmation"
        else:
            comparison = "author_layer_confirmation_only"

        keys = {
            "title": normalized_title(clean(row.get("title"))),
            "doi": normalized_doi(clean(row.get("doi"))),
            "arxiv": normalized_arxiv(clean(row.get("arxiv_id"))),
        }
        source_location = clean(row.get("source_location"))
        source_arxiv = re.search(r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})", source_location, re.I)
        if source_arxiv and not keys["arxiv"]:
            keys["arxiv"] = source_arxiv.group(1)
        existing_matches: set[str] = set()
        for key_type, key in keys.items():
            if not key:
                continue
            duplicate_groups[(key_type, key)].append(discovery_id)
            existing_matches |= existing_keys.get((key_type, key), set())
        if clean(row.get("version_target")):
            existing_matches.add(clean(row.get("version_target")))

        status_counts[comparison] += 1
        queue_rows.append(
            {
                "discovery_id": discovery_id,
                "title": clean(row.get("title")),
                "doi": clean(row.get("doi")),
                "arxiv_id": clean(row.get("arxiv_id")),
                "ai_assisted_proposed_layer": proposed,
                "author_final_layer": final_layer,
                "author_confirmation_status": clean(row.get("human_confirmation_status")),
                "second_coder_required": "yes" if coder_required else "no",
                "second_coder_row_status": clean(coder.get("row_status")),
                "second_coder_eligibility": coder_decision,
                "comparison_status": comparison,
                "existing_canonical_matches": ";".join(sorted(existing_matches)),
                "version_status": clean(row.get("version_status")),
                "version_target": clean(row.get("version_target")),
                "source_location": source_location,
                "integration_status": "pending_manual_confirmation",
                "final_canonical_study_id": "",
                "final_counting_status": "",
                "integration_note": "",
            }
        )

    internal_duplicate_groups = {
        f"{kind}:{value}": ids
        for (kind, value), ids in duplicate_groups.items()
        if value and len(set(ids)) > 1
    }
    for label, ids in internal_duplicate_groups.items():
        readiness_problems.append(f"duplicate candidate key {label}: {','.join(sorted(set(ids)))}")

    fields = list(queue_rows[0]) if queue_rows else []
    write_rows(QUEUE, queue_rows, fields)

    lines = [
        "# Final Multi-Source Integration Precheck (2026-07-30)",
        "",
        "This report is a non-adjudicating preview. It does not modify the released corpus,",
        "assign final layers, or resolve disagreements.",
        "",
        f"- Full-text assessment rows: {len(assessments)}",
        f"- Required blind second-coder rows: {len(coder_rows)}",
        f"- Complete blind second-coder rows: {sum(clean(r.get('row_status')).casefold() == 'complete' for r in coder_rows.values())}",
        f"- Confirmed author decisions: {sum(bool(author_layer(r)) and clean(r.get('human_confirmation_status')).casefold() in {'confirmed', 'complete', 'author_confirmed'} for r in assessments)}",
        f"- Candidate duplicate-key groups: {len(internal_duplicate_groups)}",
        f"- Readiness problems: {len(readiness_problems)}",
        "",
        "## Comparison Status",
        "",
    ]
    lines.extend(f"- {key}: {value}" for key, value in sorted(status_counts.items()))
    lines.extend(["", "## Readiness Problems", ""])
    if readiness_problems:
        lines.extend(f"- {problem}" for problem in readiness_problems)
    else:
        lines.append("- None.")
    lines.extend(
        [
            "",
            "Final corpus counts must not be calculated from this preview until all problems are closed.",
            "",
        ]
    )
    SUMMARY.write_text("\n".join(lines), encoding="utf-8")

    print(f"WROTE {QUEUE} ({len(queue_rows)} rows)")
    print(f"WROTE {SUMMARY}")
    print(f"READINESS_PROBLEMS={len(readiness_problems)}")
    if args.require_ready and readiness_problems:
        print("ERROR: integration inputs are not ready")
        return 1
    print("PREVIEW_ONLY_NO_CORPUS_CHANGES")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
