#!/usr/bin/env python3
"""Prepare proposed integrated artifact files without replacing released data."""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
SCREENING = DATA / "final_multisource_search_20260730_complete_screening_proposal.csv"
RECOMMENDATIONS = DATA / "final_multisource_search_20260730_screening_recommendations.csv"
OLD_CORPUS = DATA / "corpus_pre_final_multisource_20260730.csv"
OLD_CROSSWALK = DATA / "study_version_crosswalk_pre_final_multisource_20260730.csv"
OLD_MATRIX = DATA / "current_study_level_coding_matrix_harmonized_pre_final_multisource_20260730.csv"
OLD_EXTENDED = DATA / "extended_synthesis_audit_pre_final_multisource_20260730.csv"
FIRST_CODER_FILES = (
    DATA / "final_multisource_search_20260730_first_coder.csv",
    DATA / "final_multisource_search_20260730_first_coder_addendum.csv",
    DATA / "final_multisource_search_20260730_first_coder_remaining.csv",
)

NEW_STUDY = DATA / "final_multisource_search_20260730_new_study_level_coding.csv"
PROPOSED_MATRIX = DATA / "current_study_level_coding_matrix_harmonized_proposed_20260730.csv"
NEW_EXTENDED = DATA / "final_multisource_search_20260730_new_extended_synthesis_audit.csv"
PROPOSED_EXTENDED = DATA / "extended_synthesis_audit_proposed_20260730.csv"
PROPOSED_CORPUS = DATA / "corpus_proposed_20260730.csv"
PROPOSED_CROSSWALK = DATA / "study_version_crosswalk_proposed_20260730.csv"
SUMMARY = DATA / "final_multisource_search_20260730_proposed_integrated_counts.csv"


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write(path: Path, rows: list[dict[str, str]], fields: list[str] | None = None) -> None:
    fields = fields or list(rows[0])
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def clean(value: str | None) -> str:
    return " ".join((value or "").split())


def year_from(value: str) -> str:
    match = re.search(r"\b(20\d{2})\b", value or "")
    return match.group(1) if match else ""


def official_url(row: dict[str, str]) -> str:
    if clean(row.get("doi")):
        return "https://doi.org/" + clean(row["doi"])
    if clean(row.get("arxiv_id")):
        return "https://arxiv.org/abs/" + clean(row["arxiv_id"])
    return clean(row.get("urls"))


def system_alias(title: str) -> str:
    if ":" in title:
        prefix = clean(title.split(":", 1)[0])
        if 1 <= len(prefix.split()) <= 8:
            return prefix
    return clean(title)[:80]


def publication_status(row: dict[str, str]) -> str:
    if clean(row.get("doi")):
        return "formal_source_record"
    if clean(row.get("arxiv_id")):
        return "preprint"
    return "public_source_record"


def corpus_layer(layer: str, canonical_layer: str = "") -> str:
    mapping = {
        "study_level": "Core",
        "extended_synthesis": "Supporting",
        "background_reference": "Background",
        "excluded_near_neighbor": "Excluded",
        "excluded_title_abstract": "Excluded",
        "report_not_retrieved": "Excluded",
    }
    if layer == "version_reconciliation":
        return mapping.get(canonical_layer, "Supporting")
    return mapping[layer]


def primary_synthesis_role(title: str) -> str:
    value = title.lower()
    if any(term in value for term in ("fuzz", "harness", "seed", "input generation")):
        return "adjacent_fuzzing_testing"
    if any(term in value for term in ("repair", "patch", "proof-of-concept", "poc")):
        return "adjacent_validation_repair"
    if any(term in value for term in ("benchmark", "evaluation", "empirical study", "dataset")):
        return "evaluation_context"
    if any(term in value for term in ("static analysis", "vulnerability detection", "codeql", "symbolic")):
        return "lower_level_primitive"
    return "mechanism_context"


def contribution(row: dict[str, str], recommendation: dict[str, str]) -> str:
    abstract = clean(recommendation.get("abstract"))
    first_sentence = re.split(r"(?<=[.!?])\s+", abstract, maxsplit=1)[0] if abstract else ""
    if first_sentence:
        return f"{clean(row['title'])}: {first_sentence[:420]}"
    return (
        f"{clean(row['title'])} provides adjacent mechanism or evaluation context documented by the exported title and public source metadata."
    )


def main() -> int:
    screening_rows = read(SCREENING)
    screening = {row["discovery_id"]: row for row in screening_rows}
    recommendation = {row["discovery_id"]: row for row in read(RECOMMENDATIONS)}
    old_corpus = read(OLD_CORPUS)
    old_crosswalk = read(OLD_CROSSWALK)
    old_matrix = read(OLD_MATRIX)
    old_extended = read(OLD_EXTENDED)
    old_crosswalk_by_record = {row["record_id"]: row for row in old_crosswalk}

    first_coder: dict[str, dict[str, str]] = {}
    for path in FIRST_CODER_FILES:
        for row in read(path):
            if row["discovery_id"] in first_coder:
                raise SystemExit(f"ERROR duplicate first-coder ID {row['discovery_id']}")
            first_coder[row["discovery_id"]] = row

    study_ids = {
        row["discovery_id"]
        for row in screening_rows
        if row["ai_assisted_proposed_layer"] == "study_level"
    }
    if len(study_ids) != 132 or not study_ids <= set(first_coder):
        raise SystemExit("ERROR expected 132 study-level rows with first-coder labels")

    new_study_rows: list[dict[str, str]] = []
    matrix_fields = list(old_matrix[0])
    for record_id in sorted(study_ids):
        source = first_coder[record_id]
        screen = screening[record_id]
        row = {
            "matrix_id": record_id,
            "record_id": record_id,
            "canonical_study_id": f"CS_{record_id}",
            "system_alias": system_alias(source["title"]),
            "title": clean(source["title"]),
            "analytical_role": "target_software_study",
            "coding_round": "integrated_multisource_search_through_2026-07-30",
            "lifecycle_coverage": clean(source["final_lifecycle_coverage"]),
            "strongest_evidence_output": clean(
                source["final_principal_reported_evidence_output"]
            ),
            "external_traceability": clean(source["final_external_traceability"]),
            "claim_boundary": clean(source["final_claim_boundary"]),
            "claim_boundary_original": "",
            "coding_status": "complete_independent_second_coder_review",
            "reliability_scope": (
                "complete independent second-coder review; first- and second-coder labels are preserved separately"
            ),
            "official_url": official_url(recommendation[record_id]),
            "primary_system_shape": clean(source["final_primary_system_shape"]),
            "overlay_tags": "",
            "cross_stage_capabilities": clean(source["final_cross_stage_capabilities"]),
            "harmonization_status": (
                "descriptive first-coder assignment; independent second-coder labels preserved"
            ),
            "legacy_notes": clean(source.get("uncertainty_note")),
        }
        new_study_rows.append(row)
    write(NEW_STUDY, new_study_rows, matrix_fields)
    proposed_matrix = old_matrix + new_study_rows
    write(PROPOSED_MATRIX, proposed_matrix, matrix_fields)

    extended_ids = {
        row["discovery_id"]
        for row in screening_rows
        if row["ai_assisted_proposed_layer"] == "extended_synthesis"
    }
    if len(extended_ids) != 84:
        raise SystemExit("ERROR expected 84 full-text-supported new extended-synthesis studies")
    extended_fields = list(old_extended[0])
    new_extended_rows: list[dict[str, str]] = []
    for record_id in sorted(extended_ids):
        screen = screening[record_id]
        rec = recommendation[record_id]
        role = primary_synthesis_role(screen["title"])
        rq = "RQ1;RQ2_context" if role in {"adjacent_fuzzing_testing", "lower_level_primitive"} else "RQ2_context;evaluation_agenda"
        new_extended_rows.append(
            {
                "record_id": record_id,
                "citation_key": record_id,
                "title": clean(screen["title"]),
                "material_type": publication_status(rec),
                "primary_synthesis_role": role,
                "secondary_synthesis_roles": "evaluation_agenda",
                "rq_contribution": rq,
                "manuscript_section_use": "Sections 2, 4, 5, and 7 as applicable",
                "extracted_contribution": contribution(screen, rec),
                "reason_not_study_level_coded": clean(screen["decision_reason"]),
                "public_material_basis": official_url(rec),
                "reviewer_note": (
                    "Full-text record-level thematic extraction; retained for contextual synthesis and not prevalence estimation."
                ),
            }
        )
    write(NEW_EXTENDED, new_extended_rows, extended_fields)
    proposed_extended = old_extended + new_extended_rows
    write(PROPOSED_EXTENDED, proposed_extended, extended_fields)

    # New source records exclude exact matches already represented in the old
    # corpus. Alternate versions remain as source records in the crosswalk.
    source_rows_to_add = [
        row
        for row in screening_rows
        if row["counting_status"] != "existing_study_match_not_counted"
    ]
    if len(source_rows_to_add) != 1532:
        raise SystemExit(
            f"ERROR expected 1,532 new source records, found {len(source_rows_to_add)}"
        )

    new_corpus_rows: list[dict[str, str]] = []
    new_crosswalk_rows: list[dict[str, str]] = []
    corpus_fields = list(old_corpus[0])
    crosswalk_fields = list(old_crosswalk[0])
    for screen in source_rows_to_add:
        record_id = screen["discovery_id"]
        rec = recommendation[record_id]
        layer = screen["ai_assisted_proposed_layer"]
        canonical_record = screen["canonical_search_record_id"]
        existing_target = screen["existing_canonical_study_id"]
        if existing_target:
            target_cw = old_crosswalk_by_record.get(existing_target, {})
            canonical_study = target_cw.get("canonical_study_id", existing_target)
            canonical_record_id = target_cw.get("canonical_record_id", existing_target)
            target_layer = target_cw.get("analytical_layer", "extended_synthesis")
        else:
            canonical_study = f"CS_{canonical_record}"
            canonical_record_id = canonical_record
            target_layer = (
                screening[canonical_record]["ai_assisted_proposed_layer"]
                if canonical_record in screening
                else layer
            )
        if layer == "version_reconciliation":
            analytical_layer = "alternate_version"
            counting_status = "alternate_version_not_counted"
        else:
            analytical_layer = {
                "study_level": "study_level_coded",
                "extended_synthesis": "extended_synthesis",
                "background_reference": "background_reference",
                "excluded_near_neighbor": "excluded_near_neighbor",
                "excluded_title_abstract": "excluded_near_neighbor",
                "report_not_retrieved": "excluded_near_neighbor",
            }[layer]
            counting_status = "canonical_counted"
        new_corpus_rows.append(
            {
                "record_id": record_id,
                "title": clean(screen["title"]),
                "year": year_from(screen["publication_dates"]),
                "authors": clean(rec.get("authors")) or "NA",
                "source_type": publication_status(rec),
                "venue_or_source": clean(rec.get("source_ids")),
                "doi_or_url": official_url(rec),
                "corpus_layer": corpus_layer(layer, target_layer),
                "task_category": "Candidate",
                "exclusion_reason": clean(screen["decision_reason"]) if "excluded" in analytical_layer else "NA",
                "note": "Integrated multi-source search through 2026-07-30.",
            }
        )
        version_type = (
            "preprint"
            if clean(rec.get("arxiv_id")) and not clean(rec.get("doi"))
            else "conference_version" if clean(rec.get("doi")) else "other"
        )
        new_crosswalk_rows.append(
            {
                "record_id": record_id,
                "title": clean(screen["title"]),
                "canonical_study_id": canonical_study,
                "canonical_record_id": canonical_record_id,
                "version_type": version_type,
                "source_version": clean(rec.get("source_ids")),
                "same_study_as": canonical_record_id if record_id != canonical_record_id else "",
                "dedup_basis": (
                    "identifier/title/author/abstract reconciliation"
                    if record_id != canonical_record_id or existing_target
                    else "unique DOI/arXiv/title after multi-source deduplication"
                ),
                "analytical_layer": analytical_layer,
                "counting_status": counting_status,
                "retained_reason": clean(screen["decision_reason"]),
                "notes": "Integrated multi-source search through 2026-07-30.",
            }
        )

    proposed_corpus = old_corpus + new_corpus_rows
    proposed_crosswalk = old_crosswalk + new_crosswalk_rows
    if len(proposed_corpus) != 1785 or len(proposed_crosswalk) != 1785:
        raise SystemExit("ERROR proposed source-record total must be 1,785")
    write(PROPOSED_CORPUS, proposed_corpus, corpus_fields)
    write(PROPOSED_CROSSWALK, proposed_crosswalk, crosswalk_fields)

    canonical = [
        row for row in proposed_crosswalk if row["counting_status"] == "canonical_counted"
    ]
    if len(canonical) != 1772 or len({row["canonical_study_id"] for row in canonical}) != 1772:
        raise SystemExit("ERROR proposed canonical-study total must be 1,772")

    layer_counts = Counter(row["analytical_layer"] for row in canonical)
    summary = [
        {"metric": "source_records", "value": str(len(proposed_corpus))},
        {"metric": "canonical_studies", "value": str(len(canonical))},
        {"metric": "study_level_matrix_rows_including_governance", "value": str(len(proposed_matrix))},
        {"metric": "target_software_studies", "value": str(sum(row["analytical_role"] == "target_software_study" for row in proposed_matrix))},
        {"metric": "governance_boundary_cases", "value": str(sum(row["analytical_role"] != "target_software_study" for row in proposed_matrix))},
        {"metric": "extended_synthesis_studies", "value": str(len(proposed_extended))},
    ]
    summary.extend(
        {"metric": f"canonical_layer_{key}", "value": str(value)}
        for key, value in sorted(layer_counts.items())
    )
    write(SUMMARY, summary, ["metric", "value"])

    print(f"NEW_STUDY_LEVEL={len(new_study_rows)}")
    print(f"PROPOSED_MATRIX_ROWS={len(proposed_matrix)}")
    print(f"NEW_EXTENDED={len(new_extended_rows)}")
    print(f"PROPOSED_EXTENDED={len(proposed_extended)}")
    print(f"PROPOSED_SOURCE_RECORDS={len(proposed_corpus)}")
    print(f"PROPOSED_CANONICAL_STUDIES={len(canonical)}")
    for key, value in sorted(layer_counts.items()):
        print(f"{key}={value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
