#!/usr/bin/env python3
"""Create a complete, auditable screening proposal for the 2026-07-30 search.

The output preserves AI-assisted decisions as proposals pending author
confirmation. It does not overwrite historical screening or corpus files.
"""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RECOMMENDATIONS = DATA / "final_multisource_search_20260730_screening_recommendations.csv"
ASSESSMENT = DATA / "final_multisource_search_20260730_fulltext_assessment.csv"
CODER_FILES = (
    DATA / "final_multisource_search_20260730_second_coder_blind.csv",
    DATA / "final_multisource_search_20260730_second_coder_addendum_blind.csv",
    DATA / "final_multisource_search_20260730_second_coder_remaining_blind.csv",
)
OUTPUT = DATA / "final_multisource_search_20260730_complete_screening_proposal.csv"
SUMMARY = DATA / "final_multisource_search_20260730_complete_screening_summary.csv"


# Formal or better documented source records retained as the search-level
# representative. The alternate record remains in the version crosswalk.
INTERNAL_ALTERNATE_TO_CANONICAL = {
    "FMS0457": "FMS0708",  # CovRL arXiv -> ACM conference version
    "FMS0073": "FMS0860",  # TechRxiv v1 -> v2 with revised title
    "FMS0730": "FMS0722",  # GenDetect arXiv -> Springer version
    "FMS0983": "FMS0984",  # title variant with same authors/date
    "FMS1102": "FMS1499",  # same arXiv study with revised title
    "FMS1293": "FMS1307",  # earlier SSRN title/author list
}

INTERNAL_CANONICAL_LAYER = {
    "FMS0708": "extended_synthesis",
    "FMS0860": "excluded_near_neighbor",
    "FMS0722": "background_reference",
    "FMS0984": "background_reference",
    "FMS1499": "excluded_near_neighbor",
    "FMS1307": "excluded_near_neighbor",
}

EXISTING_VERSION_OVERRIDES = {
    "FMS0444": "U10",  # ContraFix title variant
    "FMS1318": "C11",  # MALF formal journal version
}

SECOND_CODER_NOT_STUDY_LEVEL = {
    "FMS0614",
    "FMS0775",
    "FMS1155",
    "FMS1265",
}

MANUAL_BACKGROUND_OVERRIDES = {
    "FMS0026", "FMS0104", "FMS0121", "FMS0144", "FMS0177", "FMS0215",
    "FMS0245", "FMS0323", "FMS0325", "FMS0329", "FMS0332", "FMS0352",
    "FMS0411", "FMS0418", "FMS0556", "FMS0665", "FMS0673", "FMS0697",
    "FMS0780", "FMS0797", "FMS0940", "FMS0985", "FMS0995", "FMS1057",
    "FMS1105", "FMS1140", "FMS1324", "FMS1342", "FMS1363", "FMS1490",
    "FMS1511", "FMS1556", "FMS1568",
}

MANUAL_EXTENDED_OVERRIDES = {
    "FMS0188", "FMS0201", "FMS0343", "FMS0421", "FMS0670", "FMS0819",
    "FMS0826", "FMS0919", "FMS0999", "FMS1241", "FMS1252", "FMS1295",
    "FMS1311", "FMS1395", "FMS1411", "FMS1446", "FMS1541", "FMS1615",
}

MANUAL_EXCLUDE_OVERRIDES = {"FMS1191"}

REVIEW = re.compile(
    r"\b(review|survey|systematic literature review|state[- ]of[- ]the[- ]art|"
    r"roadmap|opportunities and challenges|sok:)\b",
    re.I,
)
AGENT_TARGET = re.compile(
    r"openclaw|model context protocol|\bmcp\b|code interpreter agents?|"
    r"security (?:evaluation|analysis|benchmark) of (?:llm|ai|coding|computer-use|web )?agents?|"
    r"securing (?:llm|ai|coding|computer-use|web )?agents?|"
    r"agents?' vulnerabilit|prompt injection|jailbreak|memory poisoning|"
    r"tool-invocation perspective|ai-generated code|llm-generated code|"
    r"coding agents? from a security|vibe-coded applications",
    re.I,
)
TARGET_SOFTWARE = re.compile(
    r"software|source code|code vulnerab|smart contract|fuzz|static analysis|"
    r"binary|firmware|web application|repository|patch|repair|codeql|"
    r"vulnerable code|secure code generation|vulnerability detection|"
    r"vulnerability localization|vulnerability explanation|cve",
    re.I,
)
NON_SOFTWARE = re.compile(
    r"voice agents?|uav|wireless network|power system|energy management|"
    r"healthcare|mental health|personalized dialogue|robot|vision.language|"
    r"e-commerce|credit|scientific discovery|privacy text sanitization|"
    r"foundation model industry|preference-undermining|anthropomorphic|"
    r"differential privacy|vulnerable users|mobile learning",
    re.I,
)
BENCHMARK_OR_MODEL_STUDY = re.compile(
    r"benchmark|dataset|empirical study|comparative|evaluation|evaluating|"
    r"fine[- ]tun|classification|detection accuracy|prompting|"
    r"large language models? (?:for|versus|in) .*vulnerab",
    re.I,
)


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def manual_title_abstract_layer(row: dict[str, str]) -> tuple[str, str]:
    record_id = row["discovery_id"]
    title = row.get("title", "")
    abstract = row.get("abstract", "")
    text = f"{title} {abstract}"
    if record_id in MANUAL_BACKGROUND_OVERRIDES:
        return (
            "background_reference",
            "The record informs agent/LLM security, governance, or evaluation context but does not study an Agentic target-software mining workflow.",
        )
    if record_id in MANUAL_EXTENDED_OVERRIDES:
        return (
            "background_reference",
            "The title and abstract provide adjacent target-software context, but no retrieved full text was available for study-specific extended synthesis.",
        )
    if record_id in MANUAL_EXCLUDE_OVERRIDES:
        return (
            "excluded_title_abstract",
            "The record is outside the LLM-mediated target-software scope of the review.",
        )
    if NON_SOFTWARE.search(title):
        return (
            "excluded_title_abstract",
            "The title identifies a non-software or non-target-software use of vulnerability.",
        )
    if REVIEW.search(title):
        return (
            "background_reference",
            "Review or survey material is retained as contextual literature rather than a primary analytical study.",
        )
    if AGENT_TARGET.search(text):
        return (
            "background_reference",
            "The security target is an AI/agent system or generated-code ecosystem rather than an Agentic target-software mining workflow.",
        )
    if TARGET_SOFTWARE.search(text):
        return (
            "background_reference",
            "The title and abstract indicate adjacent target-software relevance, but no retrieved full text was available for study-specific extended synthesis.",
        )
    if BENCHMARK_OR_MODEL_STUDY.search(text):
        return (
            "background_reference",
            "The visible contribution is a benchmark, model evaluation, or adjacent security study outside study-level workflow coding.",
        )
    return (
        "excluded_title_abstract",
        "The title and abstract do not establish an in-scope target-software vulnerability-mining workflow or a defined synthesis use.",
    )


def main() -> int:
    rows = read(RECOMMENDATIONS)
    assessments = {row["discovery_id"]: row for row in read(ASSESSMENT)}
    coder_rows: dict[str, dict[str, str]] = {}
    for path in CODER_FILES:
        for row in read(path):
            if row["discovery_id"] in coder_rows:
                raise SystemExit(f"ERROR duplicate second-coder ID {row['discovery_id']}")
            coder_rows[row["discovery_id"]] = row

    output: list[dict[str, str]] = []
    for row in rows:
        record_id = row["discovery_id"]
        recommendation = row["ai_assisted_screening_recommendation"]
        assessment = assessments.get(record_id, {})
        coder = coder_rows.get(record_id, {})
        existing = row.get("existing_record_or_canonical_id", "").strip()

        canonical_search_record = record_id
        existing_canonical = existing
        counting_status = "new_candidate_study"
        screening_stage = "title_abstract"
        source_location = "title, abstract, and exported source metadata"

        if record_id in INTERNAL_ALTERNATE_TO_CANONICAL:
            canonical_search_record = INTERNAL_ALTERNATE_TO_CANONICAL[record_id]
            layer = "version_reconciliation"
            counting_status = "alternate_version_not_counted"
            reason = (
                f"Alternate source/title version of {canonical_search_record}; retained in the version crosswalk."
            )
        elif record_id in INTERNAL_CANONICAL_LAYER:
            layer = INTERNAL_CANONICAL_LAYER[record_id]
            reason = (
                "Preferred search-level representative after title, identifier, author, and abstract comparison of source variants."
            )
        elif record_id in EXISTING_VERSION_OVERRIDES:
            existing_canonical = EXISTING_VERSION_OVERRIDES[record_id]
            layer = "version_reconciliation"
            counting_status = "existing_study_version_not_counted"
            reason = (
                f"Alternate or formal version of existing study {existing_canonical}; metadata may be reconciled without a new study count."
            )
        elif existing:
            layer = "existing_study_or_version"
            counting_status = "existing_study_match_not_counted"
            reason = f"Matched existing study {existing} by {row.get('match_basis', 'identifier/title')} ."
        elif assessment:
            screening_stage = (
                "full_text"
                if assessment.get("access_status") == "downloaded_and_text_extracted"
                else "report_retrieval"
            )
            source_location = assessment.get("source_location", "")
            proposed = assessment.get("ai_assisted_proposed_layer", "")
            if (
                assessment.get("ai_assisted_proposed_decision") == "study_level_candidate"
                and assessment.get("access_status") != "downloaded_and_text_extracted"
            ):
                layer = "report_not_retrieved"
                counting_status = "not_counted_report_unavailable"
                reason = (
                    "Potentially eligible report could not be retrieved from the documented public sources and was not coded."
                )
            elif record_id in SECOND_CODER_NOT_STUDY_LEVEL:
                layer = "extended_synthesis"
                reason = coder.get("eligibility_reason", "")
            elif proposed == "target_software_study":
                layer = "study_level"
                reason = assessment.get("decision_reason", "")
            elif proposed in {
                "extended_synthesis",
                "background_reference",
                "excluded_near_neighbor",
                "not_counted_as_separate_study",
            }:
                if (
                    proposed == "extended_synthesis"
                    and assessment.get("access_status") != "downloaded_and_text_extracted"
                ):
                    layer = "background_reference"
                    reason = (
                        "Adjacent mechanism or evaluation context was visible in metadata, "
                        "but no retrieved full text was available for study-specific extended synthesis."
                    )
                else:
                    layer = proposed
                    reason = assessment.get("decision_reason", "")
            else:
                raise SystemExit(f"ERROR {record_id}: unsupported assessment layer {proposed!r}")
        elif recommendation == "exclude_title_abstract":
            layer = "excluded_title_abstract"
            reason = row["recommendation_basis"]
        elif recommendation == "background_review":
            layer = "background_reference"
            reason = row["recommendation_basis"]
        elif recommendation == "governance_or_background_review":
            layer = "background_reference"
            reason = (
                "Agent-system security or governance context; the target is not target software."
            )
        elif recommendation == "extended_synthesis_review":
            layer = "background_reference"
            reason = (
                "Adjacent mechanism or evaluation context was visible at title/abstract screening, "
                "but no retrieved full text was available for study-specific extended synthesis."
            )
        elif recommendation == "manual_title_abstract_review":
            layer, reason = manual_title_abstract_layer(row)
        elif recommendation == "retain_existing_match":
            raise SystemExit(f"ERROR {record_id}: existing recommendation lacks match ID")
        else:
            raise SystemExit(
                f"ERROR {record_id}: unassessed recommendation {recommendation!r}"
            )

        if layer in {"version_reconciliation", "existing_study_or_version"}:
            final_counted = "no"
        elif layer == "report_not_retrieved":
            final_counted = "no"
        else:
            final_counted = "yes_after_author_confirmation"

        output.append(
            {
                "discovery_id": record_id,
                "title": row["title"],
                "publication_dates": row["publication_dates"],
                "doi": row["doi"],
                "arxiv_id": row["arxiv_id"],
                "source_ids": row["source_ids"],
                "screening_stage": screening_stage,
                "ai_assisted_proposed_layer": layer,
                "decision_reason": reason,
                "source_location": source_location,
                "canonical_search_record_id": canonical_search_record,
                "existing_canonical_study_id": existing_canonical,
                "counting_status": counting_status,
                "counted_after_confirmation": final_counted,
                "second_coder_required": "yes" if record_id in coder_rows else "no",
                "second_coder_status": coder.get("row_status", "not_applicable"),
                "second_coder_eligibility": coder.get("eligibility_decision", ""),
                "author_confirmation_status": "pending",
                "author_final_layer": "",
                "author_confirmation_note": "",
            }
        )

    if len(output) != 1642 or len({row["discovery_id"] for row in output}) != 1642:
        raise SystemExit("ERROR complete screening proposal must contain 1,642 unique rows")

    fields = list(output[0])
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(output)

    layer_counts = Counter(row["ai_assisted_proposed_layer"] for row in output)
    summary = [
        {"metric": "deduplicated_discovery_records", "value": str(len(output))},
        {"metric": "second_coder_rows", "value": str(len(coder_rows))},
        {
            "metric": "second_coder_complete",
            "value": str(sum(row.get("row_status") == "complete" for row in coder_rows.values())),
        },
    ]
    summary.extend(
        {"metric": f"proposed_layer_{key}", "value": str(value)}
        for key, value in sorted(layer_counts.items())
    )
    with SUMMARY.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["metric", "value"])
        writer.writeheader()
        writer.writerows(summary)

    print(f"WROTE {OUTPUT} ({len(output)} rows)")
    print(f"WROTE {SUMMARY}")
    for key, value in sorted(layer_counts.items()):
        print(f"{key}={value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
