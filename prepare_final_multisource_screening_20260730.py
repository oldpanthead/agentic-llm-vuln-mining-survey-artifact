#!/usr/bin/env python3
"""Deduplicate final-search hits and prepare a record-level screening audit.

The script applies only deterministic discovery and triage rules. Records that
could satisfy the Agentic workflow boundary remain explicit full-text or manual
review candidates; the script does not assign final analytical layers.
"""

from __future__ import annotations

import csv
import difflib
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
SOURCE_RESULTS = DATA / "final_multisource_search_20260730_results.csv"
CORPUS = DATA / "corpus_pre_final_multisource_20260730.csv"
REFERENCE_AUDIT = DATA / "reference_audit_pre_final_multisource_20260730.csv"
CROSSWALK = DATA / "study_version_crosswalk_pre_final_multisource_20260730.csv"
OUTPUT = DATA / "final_multisource_search_20260730_screening_audit.csv"
SUMMARY = DATA / "final_multisource_search_20260730_screening_summary.csv"

DISCOVERY_SOURCES = {"arxiv", "openalex"}
CROSSREF_SOURCES = {
    "crossref",
    "acm_crossref",
    "ieee_crossref",
    "springer_crossref",
    "elsevier_crossref",
}

MODEL_RE = re.compile(
    r"\b(llms?|large language models?|chatgpt|gpt[- ]?\d|claude|gemini|"
    r"language-model(?:-based)?|generative ai)\b",
    re.IGNORECASE,
)
SECURITY_TASK_RE = re.compile(
    r"vulnerab|fuzz|exploit|penetration test|pentest|cyber reasoning|"
    r"proof of (?:concept|vulnerability)|\bpoc\b|\bpov\b|security audit|"
    r"secure code|patch|static analysis|taint|sanitizer",
    re.IGNORECASE,
)
CONTROL_RE = re.compile(
    r"agentic|multi[- ]?agent|\bagents?\b|autonom|orchestrat|planner|executor|"
    r"tool[- ]?(?:use|call|routing|collaboration)|feedback|iterative|"
    r"closed[- ]?loop|state[- ]?(?:management|update)|replay|harness|runtime|"
    r"execution|coverage[- ]?guided|crash[- ]?guided|reasoning loop",
    re.IGNORECASE,
)
REVIEW_RE = re.compile(
    r"\b(review|survey|systematic literature review|mapping study|"
    r"state of the art|roadmap)\b",
    re.IGNORECASE,
)
AGENT_TARGET_RE = re.compile(
    r"prompt injection|jailbreak|llm security|security of (?:llm|agent)|"
    r"attacks? on (?:llm|agent)|llm vulnerabilit|agent vulnerabilit|"
    r"mcp security|memory poisoning|tool poisoning|agent skill security|"
    r"security of ai agents|agent framework security",
    re.IGNORECASE,
)
NON_SOFTWARE_DOMAIN_RE = re.compile(
    r"patient|clinical|healthcare|medical diagnosis|road network|power dispatch|"
    r"power grid|microgrid|waterlogging|economic vulnerability|financial|"
    r"credit assignment|trading|robot manipulation|building disassembly|"
    r"social science|police incident logs|colorectal cancer|materials? science|"
    r"wireless covert|uav agents?|education|psychological counseling",
    re.IGNORECASE,
)
PEER_REVIEW_ATTACHMENT_RE = re.compile(
    r"^(author response|decision letter|review for)\b",
    re.IGNORECASE,
)
ONE_SHOT_RE = re.compile(
    r"classification|prediction|fine[- ]?tun|prompting|benchmarking|dataset|"
    r"code explanation|detection accuracy|retrieval[- ]?augmented",
    re.IGNORECASE,
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def compact(value: str) -> str:
    return " ".join((value or "").split())


def strip_markup(value: str) -> str:
    return re.sub(r"<[^>]+>", " ", value or "")


def norm_title(value: str) -> str:
    value = strip_markup(value).lower().replace("’", "'")
    return re.sub(r"[^a-z0-9]+", " ", value).strip()


def normalize_doi(value: str) -> str:
    value = compact(value).lower()
    value = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", value)
    return value.rstrip("/")


def arxiv_from(value: str) -> str:
    value = compact(value).lower()
    if re.fullmatch(r"\d{4}\.\d{4,5}(?:v\d+)?", value):
        return re.sub(r"v\d+$", "", value)
    match = re.search(
        r"(?:arxiv(?:\.org/(?:abs|pdf)/|:|\.)|10\.48550/arxiv\.)"
        r"(\d{4}\.\d{4,5})(?:v\d+)?",
        value,
        re.IGNORECASE,
    )
    return match.group(1).lower() if match else ""


def token_jaccard(left: str, right: str) -> float:
    a, b = set(left.split()), set(right.split())
    return len(a & b) / len(a | b) if a and b else 0.0


def title_similarity(left: str, right: str) -> float:
    if not left or not right:
        return 0.0
    seq = difflib.SequenceMatcher(None, left, right).ratio()
    return max(seq, token_jaccard(left, right))


def local_crossref_relevance(row: dict[str, str]) -> bool:
    """Turn the broad ranked Crossref export into an auditable candidate query."""
    title = strip_markup(row.get("title", ""))
    text = title + " " + row.get("abstract", "")
    return bool(
        MODEL_RE.search(text)
        and SECURITY_TASK_RE.search(title)
        and (CONTROL_RE.search(text) or REVIEW_RE.search(title))
    )


def source_key(row: dict[str, str]) -> str:
    title = norm_title(row.get("title", ""))
    doi = normalize_doi(row.get("doi", ""))
    arxiv_id = arxiv_from(row.get("arxiv_id", "")) or arxiv_from(doi)
    # Search interfaces frequently expose the arXiv and formal DOI versions as
    # separate records. Exact normalized-title grouping keeps those source
    # versions together while retaining every identifier in the audit row.
    if title:
        return f"title:{title}"
    if doi and not doi.startswith("10.48550/arxiv."):
        return f"doi:{doi}"
    if arxiv_id:
        return f"arxiv:{arxiv_id}"
    return "untitled"


def choose_title(rows: list[dict[str, str]]) -> str:
    return max((compact(strip_markup(row.get("title", ""))) for row in rows), key=len)


def choose_abstract(rows: list[dict[str, str]]) -> str:
    return max((compact(strip_markup(row.get("abstract", ""))) for row in rows), key=len)


def join_unique(values: Iterable[str], delimiter: str = "; ") -> str:
    return delimiter.join(sorted({compact(value) for value in values if compact(value)}))


def current_maps() -> tuple[
    dict[str, str], dict[str, str], dict[str, str], list[tuple[str, str]]
]:
    corpus = read_csv(CORPUS)
    refs = read_csv(REFERENCE_AUDIT)
    crosswalk = read_csv(CROSSWALK)
    title_map: dict[str, str] = {}
    doi_map: dict[str, str] = {}
    arxiv_map: dict[str, str] = {}

    for row in corpus:
        title = norm_title(row.get("title", ""))
        if title:
            title_map.setdefault(title, row.get("record_id", ""))
        locator = row.get("doi_or_url", "")
        doi = normalize_doi(locator)
        if doi.startswith("10."):
            doi_map.setdefault(doi, row.get("record_id", ""))
        arxiv_id = arxiv_from(locator)
        if arxiv_id:
            arxiv_map.setdefault(arxiv_id, row.get("record_id", ""))

    for row in refs:
        record_id = row.get("record_id", "")
        title = norm_title(row.get("canonical_title", ""))
        if title:
            title_map.setdefault(title, record_id)
        doi = normalize_doi(row.get("doi", ""))
        if doi:
            doi_map.setdefault(doi, record_id)
        arxiv_id = arxiv_from(row.get("arxiv_id", ""))
        if arxiv_id:
            arxiv_map.setdefault(arxiv_id, record_id)

    canonical_by_record = {
        row.get("record_id", ""): row.get("canonical_study_id", "")
        for row in crosswalk
    }
    candidates = [
        (title, canonical_by_record.get(record_id, record_id))
        for title, record_id in title_map.items()
    ]
    return title_map, doi_map, arxiv_map, candidates


def existing_match(
    title: str,
    doi: str,
    arxiv_id: str,
    title_map: dict[str, str],
    doi_map: dict[str, str],
    arxiv_map: dict[str, str],
    title_candidates: list[tuple[str, str]],
) -> tuple[str, str, float]:
    norm = norm_title(title)
    if doi and doi in doi_map:
        return doi_map[doi], "exact DOI", 1.0
    if arxiv_id and arxiv_id in arxiv_map:
        return arxiv_map[arxiv_id], "exact arXiv ID", 1.0
    if norm and norm in title_map:
        return title_map[norm], "exact normalized title", 1.0
    best_id, best_score = "", 0.0
    for candidate, record_id in title_candidates:
        score = title_similarity(norm, candidate)
        if score > best_score:
            best_id, best_score = record_id, score
    if best_score >= 0.93:
        return best_id, "high-similarity title; manual version confirmation required", best_score
    return "", "", best_score


def triage(title: str, abstract: str) -> tuple[str, str]:
    text = f"{title} {abstract}"
    if PEER_REVIEW_ATTACHMENT_RE.search(title):
        return (
            "exclude_title_abstract",
            "Publisher peer-review attachment rather than a study report.",
        )
    if not MODEL_RE.search(text):
        return (
            "exclude_title_abstract",
            "No LLM or closely related model component is identifiable in the title or abstract.",
        )
    if not SECURITY_TASK_RE.search(text):
        return (
            "exclude_title_abstract",
            "No vulnerability-mining, validation, fuzzing, exploitation, repair, or adjacent security task is identifiable.",
        )
    if NON_SOFTWARE_DOMAIN_RE.search(title):
        return (
            "exclude_title_abstract",
            "The title indicates a non-software vulnerability domain outside the review scope.",
        )
    if REVIEW_RE.search(title):
        return (
            "background_or_related_review_candidate",
            "Review or survey material; retain for related-work/background assessment rather than study-level coding.",
        )
    if AGENT_TARGET_RE.search(title):
        return (
            "governance_or_agent_security_candidate",
            "The apparent target is an LLM/agent system rather than target software; assess only for governance or boundary context.",
        )
    if CONTROL_RE.search(text):
        return (
            "full_text_candidate",
            "Title/abstract indicates a possible LLM-mediated tool, execution, feedback, state, or multi-step control function.",
        )
    if ONE_SHOT_RE.search(text):
        return (
            "extended_or_background_candidate",
            "The visible material suggests model evaluation, classification, generation, or adjacent analysis without an observable tool-feedback transition.",
        )
    return (
        "manual_title_abstract_review",
        "Security and LLM scope is plausible, but the observable workflow effect is unclear from available metadata.",
    )


def main() -> None:
    source_rows = read_csv(SOURCE_RESULTS)
    included_occurrences: list[dict[str, str]] = []
    for row in source_rows:
        source = row.get("source_id", "")
        if source in DISCOVERY_SOURCES:
            included_occurrences.append(row)
        elif source in CROSSREF_SOURCES and local_crossref_relevance(row):
            included_occurrences.append(row)

    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in included_occurrences:
        grouped[source_key(row)].append(row)

    title_map, doi_map, arxiv_map, title_candidates = current_maps()
    audit: list[dict[str, str]] = []
    for index, rows in enumerate(
        sorted(grouped.values(), key=lambda group: norm_title(choose_title(group))),
        start=1,
    ):
        title = choose_title(rows)
        abstract = choose_abstract(rows)
        doi = next(
            (
                normalize_doi(row.get("doi", ""))
                for row in rows
                if normalize_doi(row.get("doi", ""))
                and not normalize_doi(row.get("doi", "")).startswith("10.48550/arxiv.")
            ),
            "",
        )
        arxiv_id = next(
            (
                arxiv_from(row.get("arxiv_id", ""))
                or arxiv_from(row.get("doi", ""))
                for row in rows
                if arxiv_from(row.get("arxiv_id", ""))
                or arxiv_from(row.get("doi", ""))
            ),
            "",
        )
        match_id, match_basis, similarity = existing_match(
            title,
            doi,
            arxiv_id,
            title_map,
            doi_map,
            arxiv_map,
            title_candidates,
        )
        if match_id and not match_basis.startswith("high-similarity"):
            status = "existing_study_or_version"
            reason = f"Matched current corpus by {match_basis}."
        else:
            status, reason = triage(title, abstract)
            if match_id:
                status = "manual_version_review"
                reason = (
                    "High-similarity title match may represent an existing study version; "
                    "confirm before screening as a new study."
                )
        audit.append(
            {
                "discovery_id": f"FMS{index:04d}",
                "title": title,
                "publication_dates": join_unique(
                    row.get("publication_date", "") for row in rows
                ),
                "year": next((row.get("year", "") for row in rows if row.get("year", "")), ""),
                "authors": max((row.get("authors", "") for row in rows), key=len),
                "source_ids": join_unique(row.get("source_id", "") for row in rows),
                "query_ids": join_unique(row.get("query_id", "") for row in rows),
                "source_occurrence_count": str(len(rows)),
                "doi": doi,
                "arxiv_id": arxiv_id,
                "urls": join_unique(row.get("url", "") for row in rows),
                "abstract": abstract,
                "existing_record_or_canonical_id": match_id,
                "match_basis": match_basis,
                "best_existing_title_similarity": f"{similarity:.3f}",
                "triage_status": status,
                "triage_reason": reason,
                "author_screening_decision": "",
                "author_decision_reason": "",
                "full_text_status": "",
                "final_analytical_layer": "",
                "canonical_study_id": "",
                "second_coder_required": (
                    "yes_if_study_level_included"
                    if status in {"full_text_candidate", "manual_title_abstract_review"}
                    else "no"
                ),
                "notes": "",
            }
        )

    fields = list(audit[0]) if audit else []
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(audit)

    status_counts = Counter(row["triage_status"] for row in audit)
    summary_rows = [
        {"metric": "raw_source_occurrences_all_interfaces", "value": str(len(source_rows))},
        {
            "metric": "source_occurrences_entering_deduplication",
            "value": str(len(included_occurrences)),
        },
        {"metric": "unique_records_after_exact_deduplication", "value": str(len(audit))},
    ]
    summary_rows.extend(
        {"metric": f"triage_{key}", "value": str(value)}
        for key, value in sorted(status_counts.items())
    )
    with SUMMARY.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["metric", "value"])
        writer.writeheader()
        writer.writerows(summary_rows)

    print(f"WROTE {OUTPUT} ({len(audit)} deduplicated discovery records)")
    print(f"WROTE {SUMMARY}")
    print(json.dumps(status_counts, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
