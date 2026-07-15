#!/usr/bin/env python3
"""Integrate the author-confirmed 2026-07-15 update cohort into the corpus.

The operation is deterministic and idempotent. Legacy 31-record coding files
remain unchanged because their formal second-coder statistics describe that
frozen round. New study-level records are stored in a current-field additions
table, while source, canonical, reference, and synthesis views are expanded.
"""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"

FINAL_PATH = DATA / "submission_update_20260715_adjudicated.csv"
METADATA_PATH = DATA / "submission_update_20260715_arxiv_results.csv"

UPDATE_SOURCE_ID = "arxiv_update_20260715"
UPDATE_RECORD_START = 213


def read(name: str) -> list[dict[str, str]]:
    with (DATA / name).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write(name: str, rows: list[dict[str, str]], fields: list[str]) -> None:
    with (DATA / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def system_alias(title: str) -> str:
    if ":" in title:
        return title.split(":", 1)[0].strip()
    return title[:80].strip()


def task_category(shape: str) -> str:
    return {
        "candidate-analysis system": "Candidate analysis",
        "feedback-driven fuzzing agent": "Fuzzing / input exploration",
        "PoC/PoV validation agent": "PoC/PoV validation",
        "long-horizon pentest and CRS agent": "Pentest / CRS / long-horizon workflow",
    }[shape]


EXTENDED_DETAILS = {
    "U19": {
        "citation_key": "QASecClaw2026",
        "role": "adjacent_candidate_analysis",
        "secondary": "benchmark_or_evaluation",
        "rq": "RQ2_context",
        "section": "Sections 2.2, 4.1, and 7 / SAST triage and candidate-evidence boundary",
        "contribution": "Uses multiple LLM roles to retain or suppress Semgrep findings with repository context, providing a benchmarked false-positive-reduction example without an active execution-feedback path.",
        "reason": "The evaluated workflow performs contextual retain-or-suppress judgments over SAST alerts; its proposed dynamic-evidence path is not evaluated, so it lacks an observable execution-feedback or reproducible validation loop.",
    },
    "U20": {
        "citation_key": "AgenticVM2026",
        "role": "adjacent_candidate_analysis",
        "secondary": "agent_orchestration",
        "rq": "RQ2_context",
        "section": "Sections 2.5, 6, and 7 / vulnerability-management and reporting context",
        "contribution": "Aggregates scanner and public-vulnerability records for normalization, prioritization, missing-attribute prediction, and recommendation generation in an adaptive management workflow.",
        "reason": "The public workflow organizes externally supplied findings and reports but does not execute target software, validate a candidate vulnerability, or verify a generated repair.",
    },
    "U24": {
        "citation_key": "SynthFix2026",
        "role": "evidence_or_reproducibility",
        "secondary": "benchmark_or_evaluation",
        "rq": "evaluation_agenda",
        "section": "Sections 2.2 and 7 / repair-validation boundary",
        "contribution": "Combines generated patch candidates with symbolic and test-based scoring, illustrating benchmark-scoped neuro-symbolic patch selection and controlled validation.",
        "reason": "The public material describes a fixed repair-and-selection pipeline rather than an LLM agent that changes tool calls or strategy in response to observed validation failures.",
    },
    "U30": {
        "citation_key": "RuleForge2026",
        "role": "adjacent_candidate_analysis",
        "secondary": "evidence_or_reproducibility",
        "rq": "evaluation_agenda",
        "section": "Sections 6 and 7 / detection-rule validation and governance context",
        "contribution": "Generates HTTP detection rules from disclosed-CVE templates and refines them with synthetic tests, confidence judging, production feedback, and human review.",
        "reason": "Its primary output is a validated detection rule for known-vulnerability patterns rather than a new target-software vulnerability finding or reproduction workflow.",
    },
}


def main() -> None:
    final_rows = read(FINAL_PATH.name)
    metadata_rows = read(METADATA_PATH.name)
    metadata_by_id = {row["arxiv_id"]: row for row in metadata_rows}
    if len(final_rows) != 41:
        raise SystemExit(f"Expected 41 adjudicated update rows; found {len(final_rows)}")
    if any(row["adjudication_status"] != "author_confirmed_evidence_based_resolution" for row in final_rows):
        raise SystemExit("Update adjudication is not author-confirmed")

    record_map = {
        row["update_id"]: f"CP{UPDATE_RECORD_START + index:03d}"
        for index, row in enumerate(final_rows)
    }
    update_record_ids = set(record_map.values())

    corpus = [row for row in read("corpus.csv") if row["record_id"] not in update_record_ids]
    corpus_fields = list(corpus[0])
    source_audit = [row for row in read("source_screening_audit.csv") if row["record_id"] not in update_record_ids]
    source_fields = list(source_audit[0])
    crosswalk = [row for row in read("study_version_crosswalk.csv") if row["record_id"] not in update_record_ids]
    cross_fields = list(crosswalk[0])
    layer_audit = [row for row in read("corpus_layer_audit.csv") if row["record_id"] not in update_record_ids]
    layer_fields = list(layer_audit[0])
    reference = [row for row in read("reference_audit.csv") if row["record_id"] not in update_record_ids]
    reference_fields = list(reference[0])

    additions: list[dict[str, str]] = []
    for row in final_rows:
        update_id = row["update_id"]
        record_id = record_map[update_id]
        meta = metadata_by_id[row["arxiv_id"]]
        is_study = row["proposed_analysis_layer"] == "study_level_candidate"
        legacy_layer = "Core" if is_study else "Supporting"
        current_layer = "study_level_coded" if is_study else "extended_synthesis"
        category = task_category(row["proposed_primary_system_shape"])
        alias = system_alias(row["title"])

        corpus.append({
            "record_id": record_id,
            "title": row["title"],
            "year": "2026",
            "authors": meta["authors"],
            "source_type": "preprint",
            "venue_or_source": "arXiv submission-time update",
            "doi_or_url": meta["official_url"],
            "corpus_layer": legacy_layer,
            "task_category": category,
            "exclusion_reason": "NA",
            "note": "Author-confirmed 2026-07-15 update cohort; current analytical layer is recorded in the canonical crosswalk.",
        })
        source_audit.append({
            "record_id": record_id,
            "title": row["title"],
            "year": "2026",
            "source_bucket": UPDATE_SOURCE_ID,
            "source_name": "arXiv submission-time sensitivity update",
            "source_type": "preprint",
            "venue_or_source": "arXiv",
            "doi_or_url": meta["official_url"],
            "corpus_layer": legacy_layer,
            "task_category": category,
            "screening_decision": "included_study_level_coded" if is_study else "included_extended_synthesis",
            "deduplication_status": "unique_canonical_update_study",
            "source_trace_note": "Full-text author audit, independent blind coding, author-confirmed resolution, and canonical matching completed on 2026-07-15.",
        })
        crosswalk.append({
            "record_id": record_id,
            "title": row["title"],
            "canonical_study_id": f"CS_{record_id}",
            "canonical_record_id": record_id,
            "version_type": "preprint",
            "source_version": f"arXiv:{row['arxiv_id']}; {meta['official_url']}",
            "same_study_as": "NA",
            "dedup_basis": "No matching arXiv ID, DOI, normalized title, or high-similarity version in the frozen 212-record corpus.",
            "analytical_layer": current_layer,
            "counting_status": "canonical_counted",
            "retained_reason": "Author-confirmed update record retained in its adjudicated analytical layer.",
            "notes": "Integrated from the 2026-07-15 submission-time update cohort; original coding inputs and resolution trace remain in the update audit files.",
        })
        layer_audit.append({
            "record_id": record_id,
            "title": row["title"],
            "year": "2026",
            "source_type": "preprint",
            "publication_status": "public_preprint",
            "original_layer": legacy_layer,
            "analysis_layer": "Study-level coded" if is_study else "Extended synthesis",
            "task_category": category,
            "is_analytical_core": "yes" if is_study else "no",
            "core_id": update_id if is_study else "NA",
            "system_alias": alias if is_study else "NA",
            "a_level_original": "NA",
            "primary_evidence_stage_original": "NA",
            "external_evidence_profile_original": "NA",
            "evidence_object_original": "NA",
            "artifact_status_original": "public arXiv full text",
            "official_url": meta["official_url"],
            "doi": meta["doi"] or "NA",
            "inclusion_or_exclusion_reason": row["adjudication_basis"],
            "corpus_layer_note": "Current workflow--capability--evidence coding is stored in the submission-update adjudicated and additions files; legacy A/E fields are not imputed.",
        })
        reference.append({
            "record_id": record_id,
            "canonical_title": row["title"],
            "system_alias": alias,
            "publication_status": "public_preprint",
            "venue": "arXiv",
            "official_url": meta["official_url"],
            "arxiv_id": row["arxiv_id"],
            "doi": meta["doi"] or "NA",
            "last_verified_date": "2026-07-15",
            "note": "Submission-time update cohort; public metadata and full text reviewed.",
        })
        if is_study:
            additions.append({
                "update_id": update_id,
                "record_id": record_id,
                "canonical_study_id": f"CS_{record_id}",
                "title": row["title"],
                "system_alias": alias,
                "target_domain": next(x["target_domain"] for x in read("submission_update_20260715_full_coding_audit.csv") if x["arxiv_id"] == row["arxiv_id"]),
                "lifecycle_coverage": row["proposed_lifecycle_coverage"],
                "primary_system_shape": row["proposed_primary_system_shape"],
                "agentic_capabilities": row["proposed_agentic_capabilities"],
                "strongest_evidence_output": row["proposed_strongest_evidence_output"],
                "external_traceability": row["proposed_external_traceability"],
                "claim_boundary": row["proposed_claim_boundary"],
                "publication_status": row["publication_status"],
                "official_url": meta["official_url"],
                "coding_status": "author_confirmed_adjudicated",
                "second_coder_round": "submission_update_20260715",
            })

    corpus.sort(key=lambda row: int(row["record_id"][2:]))
    source_audit.sort(key=lambda row: int(row["record_id"][2:]))
    crosswalk.sort(key=lambda row: int(row["record_id"][2:]))
    layer_audit.sort(key=lambda row: int(row["record_id"][2:]))
    reference.sort(key=lambda row: (0, int(row["record_id"][2:])) if row["record_id"].startswith("CP") and row["record_id"][2:].isdigit() else (1, row["record_id"]))

    write("corpus.csv", corpus, corpus_fields)
    write("source_screening_audit.csv", source_audit, source_fields)
    write("study_version_crosswalk.csv", crosswalk, cross_fields)
    write("corpus_layer_audit.csv", layer_audit, layer_fields)
    write("reference_audit.csv", reference, reference_fields)
    write("submission_update_20260715_study_level_additions.csv", additions, list(additions[0]))

    log = [row for row in read("source_search_log.csv") if row["source_id"] != UPDATE_SOURCE_ID]
    log.append({
        "source_id": UPDATE_SOURCE_ID,
        "source_name": "arXiv submission-time sensitivity update",
        "source_category": "preprint index / submission update",
        "search_interface": "arXiv API query families with record-level screening and full-text review",
        "query_string": "Frozen agent-task, execution-validation, PoV/CRS, and review-update query families; see submission_update_20260715_manifest.json",
        "date_searched": "2026-07-15",
        "date_range": "2023-01-01 to 2026-06-30",
        "records_captured_before_dedup": "41",
        "duplicates_or_variants_removed": "0",
        "unique_candidate_records_after_dedup": "41",
        "core_records": "37",
        "supporting_records": "4",
        "background_records": "0",
        "excluded_records": "0",
        "zotero_metadata_used": "no",
        "notes": "These 41 source records form the full-text eligible update cohort after title/abstract screening; all were new canonical studies against the frozen corpus.",
    })
    write("source_search_log.csv", log, list(log[0]))

    extended = [row for row in read("extended_synthesis_audit.csv") if row["record_id"] not in update_record_ids]
    for row in final_rows:
        if row["proposed_analysis_layer"] != "extended_synthesis":
            continue
        detail = EXTENDED_DETAILS[row["update_id"]]
        meta = metadata_by_id[row["arxiv_id"]]
        extended.append({
            "record_id": record_map[row["update_id"]],
            "citation_key": detail["citation_key"],
            "title": row["title"],
            "material_type": "preprint_or_arxiv",
            "primary_synthesis_role": detail["role"],
            "secondary_synthesis_roles": detail["secondary"],
            "rq_contribution": detail["rq"],
            "manuscript_section_use": detail["section"],
            "extracted_contribution": detail["contribution"],
            "reason_not_study_level_coded": detail["reason"],
            "public_material_basis": f"publication_status=public_preprint; source=arXiv; locator={meta['official_url']}",
            "reviewer_note": "Full text reviewed in the 2026-07-15 update round; analytical layer confirmed after independent coding and author review.",
        })
    extended.sort(key=lambda row: int(row["record_id"][2:]))
    write("extended_synthesis_audit.csv", extended, list(extended[0]))

    # Update descriptive mapping views without altering the legacy 31-record files.
    mapping = read("mapping_snapshot_counts.csv")
    shape_additions = Counter(row["proposed_primary_system_shape"] for row in final_rows if row["proposed_analysis_layer"] == "study_level_candidate")
    task_updates = {
        "candidate/tool-enhanced analysis": 4 + shape_additions["candidate-analysis system"],
        "fuzzing/input exploration": 10 + shape_additions["feedback-driven fuzzing agent"],
        "PoC/PoV or validation": 9 + shape_additions["PoC/PoV validation agent"],
        "automated pentest/CRS/long workflow": 10 + shape_additions["long-horizon pentest and CRS agent"],
    }
    for row in mapping:
        if row["view"] in {"year_distribution", "source_type_distribution"} and row["category"] != "product/system boundary snapshot":
            row["denominator"] = "253 source records in screening ledger"
        if row["view"] == "year_distribution" and row["category"] == "2026":
            row["count"] = str(int(row["count"]) + 41 if int(row["count"]) == 37 else int(row["count"]))
        if row["view"] == "source_type_distribution" and row["category"] == "preprint/arXiv":
            row["count"] = str(int(row["count"]) + 41 if int(row["count"]) == 63 else int(row["count"]))
        if row["view"] == "task_facet_distribution" and row["category"] in task_updates:
            row["count"] = str(task_updates[row["category"]])
            row["denominator"] = "67 target-software study-level coded studies"
        if row["view"] == "task_facet_distribution" and row["category"] == "governance boundary":
            row["denominator"] = "68-record study-level coded set"
        if row["view"] == "final_canonical_stratification":
            row["denominator"] = "248 canonical candidate studies"
            if row["category"] == "target-software study-level coded studies": row["count"] = "67"
            elif row["category"] == "governance boundary coded record": row["count"] = "1"
            elif row["category"] == "extended synthesis studies": row["count"] = "65"
            elif row["category"] == "background/reference records": row["count"] = "95"
            elif row["category"] == "excluded near-neighbor studies": row["count"] = "20"
    write("mapping_snapshot_counts.csv", mapping, list(mapping[0]))

    lifecycle_base = {
        "candidate analysis": 9, "path and input exploration": 20,
        "execution observation": 20, "reproduction and validation": 15,
        "patch validation": 4, "reporting and audit": 6,
    }
    capability_base = {
        "context aggregation / rule extraction": 3, "tool routing / strategy routing": 3,
        "feedback interpretation / loop adjustment": 15,
        "validation organization / evidence packaging": 15,
        "long-horizon state management": 15, "failure reuse / strategy update": 4,
        "governance / human gates / disclosure control": 0,
    }
    evidence_base = {
        "candidate judgment": 3, "controlled task completion": 5,
        "runtime safety signal": 8, "reproducible validation": 14,
        "externally traceable material": 0, "governance boundary case": 1,
    }
    study_updates = [row for row in final_rows if row["proposed_analysis_layer"] == "study_level_candidate"]
    lifecycle_add = Counter(label for row in study_updates for label in row["proposed_lifecycle_coverage"].split(";"))
    capability_add = Counter(label for row in study_updates for label in row["proposed_agentic_capabilities"].split(";"))
    evidence_add = Counter(row["proposed_strongest_evidence_output"] for row in study_updates)
    statistics = []
    for dimension, base, added in [
        ("lifecycle_coverage", lifecycle_base, lifecycle_add),
        ("agentic_capabilities", capability_base, capability_add),
        ("strongest_evidence_output", evidence_base, evidence_add),
    ]:
        for category, baseline in base.items():
            statistics.append({
                "dimension": dimension,
                "category": category,
                "count": str(baseline + added.get(category, 0)),
                "counting_scope": "67 target-software studies" if category != "governance boundary case" else "67 target-software studies plus one governance boundary case",
                "baseline_count": str(baseline),
                "update_addition_count": str(added.get(category, 0)),
                "note": "Combined descriptive count; legacy 31-record reliability and update-round reliability remain reported separately.",
            })
    write("current_synthesis_statistics.csv", statistics, list(statistics[0]))

    report = f"""# Submission Update Corpus Integration Report

## Integrated Counts

- Source records: {len(corpus)}
- Canonical candidate studies: {sum(row['counting_status'] == 'canonical_counted' for row in crosswalk)}
- Target-software study-level coded studies: 67
- Governance boundary case: 1
- Extended-synthesis studies: {len(extended)}
- Background/reference studies: 95
- Excluded near-neighbor studies: 20
- Product-ecosystem boundary rows: 23 (independent layer)

## Cohort Structure

The current study-level coded set combines the frozen 30-target-study-plus-one-governance round with 37 author-confirmed update studies. The legacy 31-record files and their formal reliability statistics remain unchanged. The update cohort retains its own author audit, blind coder2 result, pre-adjudication agreement report, and author-confirmed resolution. No combined Cohen's kappa is inferred across the two rounds.

## Files Added or Expanded

- corpus.csv, source_screening_audit.csv, study_version_crosswalk.csv, corpus_layer_audit.csv, and reference_audit.csv include CP213--CP253.
- submission_update_20260715_study_level_additions.csv contains the 37 current-field study-level additions.
- extended_synthesis_audit.csv contains the four confirmed update additions.
- current_synthesis_statistics.csv reports combined descriptive lifecycle, capability, and evidence-output counts.
- mapping_snapshot_counts.csv and screening_summary.csv use the integrated source and canonical denominators.

## Counting Boundary

Analytical counts use canonical studies. The study-level denominator is 67 target-software studies; the governance boundary case remains separate from target-software lifecycle, capability, and system-shape distributions. Product-ecosystem materials remain outside the source-record and canonical-study counts.
"""
    (ROOT / "SUBMISSION_UPDATE_CORPUS_INTEGRATION_REPORT.md").write_text(report, encoding="utf-8")

    print(f"INTEGRATED_SOURCE_RECORDS {len(corpus)}")
    print(f"INTEGRATED_CANONICAL_STUDIES {sum(row['counting_status'] == 'canonical_counted' for row in crosswalk)}")
    print(f"STUDY_LEVEL_ADDITIONS {len(additions)}")
    print(f"EXTENDED_SYNTHESIS_TOTAL {len(extended)}")


if __name__ == "__main__":
    main()
