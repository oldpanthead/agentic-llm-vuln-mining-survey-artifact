#!/usr/bin/env python3
"""Audit final-search records against the frozen corpus and each other."""

from __future__ import annotations

import csv
import re
from difflib import SequenceMatcher
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DISCOVERY = DATA / "final_multisource_search_20260730_screening_recommendations.csv"
CORPUS = DATA / "corpus_pre_final_multisource_20260730.csv"
CROSSWALK = DATA / "study_version_crosswalk_pre_final_multisource_20260730.csv"
REFERENCE = DATA / "reference_audit_pre_final_multisource_20260730.csv"
OUTPUT = DATA / "final_multisource_search_20260730_dedup_candidates.csv"

STOP = {"a", "an", "and", "for", "from", "in", "of", "on", "the", "to", "using", "via", "with"}


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def norm_title(value: str) -> str:
    text = unquote(value or "").lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(token for token in text.split() if token not in STOP)


def compact_id(value: str) -> str:
    return re.sub(r"[^a-z0-9.]", "", (value or "").lower())


def doi_from(value: str) -> str:
    match = re.search(r"10\.\d{4,9}/[^\s?#]+", unquote(value or ""), re.I)
    return match.group(0).rstrip(".,);]").lower() if match else ""


def doi_base(value: str) -> str:
    return compact_id(re.sub(r"/v\d+$", "", unquote(value or "").lower()))


def arxiv_from(value: str) -> str:
    text = (value or "").strip()
    direct = re.fullmatch(r"(\d{4}\.\d{4,5})(?:v\d+)?", text, re.I)
    if direct:
        return direct.group(1)
    match = re.search(
        r"(?:arxiv\.org/(?:abs|pdf)/|10\.48550/arxiv\.)(\d{4}\.\d{4,5})(?:v\d+)?",
        text,
        re.I,
    )
    return match.group(1) if match else ""


def similarity(
    a: str,
    b: str,
    a_tokens: set[str] | None = None,
    b_tokens: set[str] | None = None,
) -> float:
    """Return title similarity after a cheap token-overlap candidate filter."""
    if not a or not b:
        return 0.0
    a_tokens = a_tokens if a_tokens is not None else set(a.split())
    b_tokens = b_tokens if b_tokens is not None else set(b.split())
    union = a_tokens | b_tokens
    token_jaccard = len(a_tokens & b_tokens) / len(union) if union else 0.0
    same_prefix = a[:24] == b[:24]
    if token_jaccard < 0.35 and not same_prefix:
        return token_jaccard
    return max(token_jaccard, SequenceMatcher(None, a, b).ratio())


def main() -> int:
    new_rows = read(DISCOVERY)
    corpus = read(CORPUS)
    crosswalk = {row["record_id"]: row for row in read(CROSSWALK)}
    references = {row["record_id"]: row for row in read(REFERENCE)}
    existing = []
    for row in corpus:
        cw = crosswalk.get(row["record_id"], {})
        if cw.get("counting_status") != "canonical_counted":
            continue
        ref = references.get(row["record_id"], {})
        existing.append({
            "id": row["record_id"],
            "title": row["title"],
            "doi": doi_base(ref.get("doi", "")) or doi_base(doi_from(row.get("doi_or_url", ""))),
            "arxiv": arxiv_from(ref.get("arxiv_id", "")) or arxiv_from(row.get("doi_or_url", "")),
            "layer": cw.get("analytical_layer", ""),
            "_norm_title": norm_title(row["title"]),
            "_title_tokens": set(norm_title(row["title"]).split()),
        })

    for row in new_rows:
        row["_norm_title"] = norm_title(row["title"])
        row["_title_tokens"] = set(row["_norm_title"].split())

    candidates: list[dict[str, str]] = []
    for row in new_rows:
        nd = doi_base(row.get("doi", ""))
        na = arxiv_from(row.get("arxiv_id", "")) or arxiv_from(row.get("urls", ""))
        for old in existing:
            basis = []
            score = similarity(
                row["_norm_title"],
                old["_norm_title"],
                row["_title_tokens"],
                old["_title_tokens"],
            )
            if nd and old["doi"] and nd == old["doi"]:
                basis.append("doi")
            if na and old["arxiv"] and na == old["arxiv"]:
                basis.append("arxiv")
            if row["_norm_title"] == old["_norm_title"]:
                basis.append("normalized_title")
            if score >= 0.84:
                basis.append("title_similarity")
            if basis:
                candidates.append({
                    "left_id": row["discovery_id"],
                    "left_title": row["title"],
                    "left_proposed_layer": row.get("proposed_analytical_layer", ""),
                    "left_screening_recommendation": row.get(
                        "ai_assisted_screening_recommendation", ""
                    ),
                    "right_id": old["id"],
                    "right_title": old["title"],
                    "right_layer": old["layer"],
                    "right_screening_recommendation": "existing_corpus",
                    "match_basis": ";".join(basis),
                    "title_similarity": f"{score:.6f}",
                    "manual_decision": "pending",
                    "decision_note": "",
                })

    for i, left in enumerate(new_rows):
        for right in new_rows[i + 1 :]:
            score = similarity(
                left["_norm_title"],
                right["_norm_title"],
                left["_title_tokens"],
                right["_title_tokens"],
            )
            ld, rd = doi_base(left.get("doi", "")), doi_base(right.get("doi", ""))
            la = arxiv_from(left.get("arxiv_id", "")) or arxiv_from(left.get("urls", ""))
            ra = arxiv_from(right.get("arxiv_id", "")) or arxiv_from(right.get("urls", ""))
            basis = []
            if ld and rd and ld == rd:
                basis.append("doi")
            if la and ra and la == ra:
                basis.append("arxiv")
            if left["_norm_title"] == right["_norm_title"]:
                basis.append("normalized_title")
            if score >= 0.84:
                basis.append("title_similarity")
            if basis:
                candidates.append({
                    "left_id": left["discovery_id"],
                    "left_title": left["title"],
                    "left_proposed_layer": left.get("proposed_analytical_layer", ""),
                    "left_screening_recommendation": left.get(
                        "ai_assisted_screening_recommendation", ""
                    ),
                    "right_id": right["discovery_id"],
                    "right_title": right["title"],
                    "right_layer": right.get("proposed_analytical_layer", ""),
                    "right_screening_recommendation": right.get(
                        "ai_assisted_screening_recommendation", ""
                    ),
                    "match_basis": ";".join(basis),
                    "title_similarity": f"{score:.6f}",
                    "manual_decision": "pending",
                    "decision_note": "",
                })

    candidates.sort(key=lambda row: (-float(row["title_similarity"]), row["left_id"], row["right_id"]))
    fields = [
        "left_id", "left_title", "left_proposed_layer", "left_screening_recommendation",
        "right_id", "right_title", "right_layer", "right_screening_recommendation",
        "match_basis", "title_similarity", "manual_decision", "decision_note",
    ]
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(candidates)
    print(f"EXISTING_CANONICAL={len(existing)} NEW_REVIEW_ROWS={len(new_rows)} CANDIDATE_PAIRS={len(candidates)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
