#!/usr/bin/env python3
"""Build the auditable final multi-source search and PRISMA account."""

from __future__ import annotations

import csv
import importlib.util
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RESULTS = DATA / "final_multisource_search_20260730_results.csv"
SCREENING = DATA / "final_multisource_search_20260730_complete_screening.csv"
OLD_CORPUS = DATA / "corpus_pre_final_multisource_20260730.csv"
OLD_CROSSWALK = DATA / "study_version_crosswalk_pre_final_multisource_20260730.csv"
CURRENT_CORPUS = DATA / "corpus.csv"
CURRENT_CROSSWALK = DATA / "study_version_crosswalk.csv"
OUTPUT = DATA / "final_multisource_search_20260730_prisma_counts.csv"
SOURCE_OUTPUT = DATA / "final_multisource_search_20260730_source_counts.csv"
REPORT = ROOT / "FINAL_MULTISOURCE_SEARCH_AND_PRISMA_20260730.md"


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def load_screening_module():
    path = ROOT / "prepare_final_multisource_screening_20260730.py"
    spec = importlib.util.spec_from_file_location("final_search_screening", path)
    if spec is None or spec.loader is None:
        raise SystemExit("ERROR: unable to load screening rules")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    search_module = load_screening_module()
    result_rows = read(RESULTS)
    screening_rows = read(SCREENING)
    current_corpus = read(CURRENT_CORPUS)
    current_crosswalk = read(CURRENT_CROSSWALK)
    canonical = [
        row for row in current_crosswalk if row["counting_status"] == "canonical_counted"
    ]
    canonical_layers = Counter(row["analytical_layer"] for row in canonical)
    integrated = {
        "source_records": len(current_corpus),
        "canonical_studies": len(canonical),
        "target_software_studies": canonical_layers["study_level_coded"],
        "extended_synthesis_studies": canonical_layers["extended_synthesis"],
        "canonical_layer_study_level_coded": canonical_layers["study_level_coded"],
        "canonical_layer_extended_synthesis": canonical_layers["extended_synthesis"],
        "canonical_layer_background_reference": canonical_layers["background_reference"],
        "canonical_layer_excluded_near_neighbor": canonical_layers["excluded_near_neighbor"],
    }

    raw = Counter(row["source_id"] for row in result_rows)
    entered = Counter()
    for row in result_rows:
        source = row["source_id"]
        if source in search_module.DISCOVERY_SOURCES or (
            source in search_module.CROSSREF_SOURCES
            and search_module.local_crossref_relevance(row)
        ):
            entered[source] += 1
    source_rows = [
        {
            "source_interface": source,
            "exported_occurrences": str(raw[source]),
            "occurrences_entering_deduplication": str(entered[source]),
            "count_note": (
                "source-query boundary; all exported occurrences entered deduplication"
                if source in search_module.DISCOVERY_SOURCES
                else "publisher/Crossref export subject to the recorded per-query cap and title-level security-task filter"
            ),
        }
        for source in sorted(raw)
    ]
    write(SOURCE_OUTPUT, source_rows)

    stage_counts = Counter(row["screening_stage"] for row in screening_rows)
    layer_counts = Counter(row["final_analytical_layer"] for row in screening_rows)
    cross = Counter(
        (row["screening_stage"], row["final_analytical_layer"])
        for row in screening_rows
    )

    raw_occurrences = len(result_rows)
    entered_dedup = sum(entered.values())
    unique_search_records = len(screening_rows)
    query_filter_removed = raw_occurrences - entered_dedup
    duplicate_occurrences = entered_dedup - unique_search_records
    reports_sought = stage_counts["full_text"] + stage_counts["report_retrieval"]
    reports_not_retrieved = stage_counts["report_retrieval"]
    reports_assessed = stage_counts["full_text"]
    exact_existing = layer_counts["existing_study_or_version"]
    new_versions = layer_counts["version_reconciliation"]
    supplementary_source_records = len(read(OLD_CORPUS)) - exact_existing
    prior_canonical_not_reidentified = (
        sum(row["counting_status"] == "canonical_counted" for row in read(OLD_CROSSWALK))
        - exact_existing
    )

    prisma = [
        ("identification", "exported_source_occurrences", raw_occurrences, "All saved API/interface exports before local query-specific filtering"),
        ("identification", "removed_by_deterministic_query_filter", query_filter_removed, "Broad ranked metadata outside the four-group query boundary"),
        ("deduplication", "source_occurrences_entering_deduplication", entered_dedup, "Occurrences retained by the documented query-specific rules"),
        ("deduplication", "duplicate_source_occurrences_removed", duplicate_occurrences, "Exact normalized-title source duplicates before record screening"),
        ("screening", "unique_search_records_screened", unique_search_records, "Records screened by title/abstract and, where indicated, full text"),
        ("screening", "records_not_advanced_to_report_retrieval", stage_counts["title_abstract"], "Resolved at title/abstract stage, including background, existing-study, and exclusion decisions"),
        ("retrieval", "reports_sought", reports_sought, "Reports selected for retrieval or already retrieved"),
        ("retrieval", "reports_not_retrieved", reports_not_retrieved, "No accessible full report from documented public sources"),
        ("eligibility", "reports_assessed_at_full_text", reports_assessed, "Downloaded and text-extracted reports"),
        ("eligibility", "full_text_study_level", cross[("full_text", "study_level")], "New target-software study-level records"),
        ("eligibility", "full_text_extended_synthesis", cross[("full_text", "extended_synthesis")], "Adjacent studies with full-text-supported thematic extraction"),
        ("eligibility", "full_text_background_reference", cross[("full_text", "background_reference")], "Contextual studies retained outside analytical synthesis"),
        ("eligibility", "full_text_excluded_near_neighbor", cross[("full_text", "excluded_near_neighbor")], "Full-text exclusions"),
        ("integration", "current_search_matches_to_retained_studies", exact_existing, "Search records already represented in the retained corpus"),
        ("integration", "new_or_reconciled_source_records_added", unique_search_records - exact_existing, "Includes new canonical studies and alternate source versions"),
        ("integration", "supplementary_source_records_not_reidentified", supplementary_source_records, "Previously retained seed, snowball, benchmark, project, or official-page records not reidentified by the current export interfaces"),
        ("integration", "prior_canonical_studies_not_reidentified", prior_canonical_not_reidentified, "Canonical studies retained from supplementary discovery sources"),
        ("final", "integrated_source_records", integrated["source_records"], "Source versions remain traceable"),
        ("final", "integrated_canonical_studies", integrated["canonical_studies"], "Each study counted once after version reconciliation"),
        ("final", "target_software_studies", integrated["target_software_studies"], "Study-level analytical denominator"),
        ("final", "extended_synthesis_studies", integrated["extended_synthesis_studies"], "Adjacent synthesis with record-level public-material audit"),
        ("final", "background_reference_studies", integrated["canonical_layer_background_reference"], "Contextual literature"),
        ("final", "excluded_studies", integrated["canonical_layer_excluded_near_neighbor"], "Title/abstract exclusions, full-text near-neighbors, and unavailable potentially eligible reports"),
    ]
    rows = [
        {"stage": stage, "metric": metric, "count": str(count), "definition": definition}
        for stage, metric, count, definition in prisma
    ]
    write(OUTPUT, rows)

    if reports_sought - reports_not_retrieved != reports_assessed:
        raise SystemExit("ERROR: report retrieval account does not close")
    if sum(
        integrated[key]
        for key in (
            "canonical_layer_study_level_coded",
            "canonical_layer_extended_synthesis",
            "canonical_layer_background_reference",
            "canonical_layer_excluded_near_neighbor",
        )
    ) != integrated["canonical_studies"]:
        raise SystemExit("ERROR: final canonical layers do not close")

    lines = [
        "# Final Integrated Multi-Source Search and PRISMA Account",
        "",
        "## Scope",
        "",
        "The review integrates database, metadata-index, publisher, conference, seed, snowball, benchmark, and project searches covering 2023-01-01 through 2026-07-30. Search executions occurred on their recorded dates; the account does not claim that every interface was queried on one day or with identical export capabilities.",
        "",
        "## Database and Metadata Exports",
        "",
        "| Source/interface | Exported occurrences | Entered deduplication |",
        "|---|---:|---:|",
    ]
    for row in source_rows:
        lines.append(
            f"| {row['source_interface']} | {row['exported_occurrences']} | {row['occurrences_entering_deduplication']} |"
        )
    lines.extend(
        [
            "",
            "Publisher-filtered Crossref feeds were used for ACM, IEEE, Springer, and Elsevier metadata. Official ACM Digital Library, IEEE Xplore, SpringerLink, ScienceDirect, USENIX, NDSS, and DBLP pages were checked as supplementary interfaces; their access records are preserved even where no complete export count was available. Scopus and Web of Science were inaccessible without authenticated subscriptions, and Google Scholar automated access was blocked, so none is represented as a completed database export.",
            "ArXiv and OpenAlex occurrences entered deduplication under their source-query boundaries. Crossref-derived occurrences additionally required a vulnerability, security-testing, or offensive-security cue in the title; the source-count file records the resulting interface-specific reductions.",
            "",
            "## PRISMA-ScR Account",
            "",
            "| Stage | Item | Count |",
            "|---|---|---:|",
        ]
    )
    for row in rows:
        lines.append(f"| {row['stage']} | {row['metric'].replace('_', ' ')} | {row['count']} |")
    lines.extend(
        [
            "",
            "## Final Analytical Allocation",
            "",
            f"After version reconciliation, the integrated corpus contains **{integrated['canonical_studies']} canonical studies** from **{integrated['source_records']} source records**: **{integrated['target_software_studies']} target-software studies**, **{integrated['extended_synthesis_studies']} extended-synthesis studies with record-level public-material audit**, **{integrated['canonical_layer_background_reference']} background/reference studies**, and **{integrated['canonical_layer_excluded_near_neighbor']} excluded studies**.",
            "",
            "Historical search files remain unchanged as provenance. The manuscript-facing method can report the integrated source coverage, date range, screening rules, version reconciliation, and final allocation without narrating internal search rounds.",
        ]
    )
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        f"RAW={raw_occurrences} FILTERED={entered_dedup} UNIQUE={unique_search_records} "
        f"SOUGHT={reports_sought} ASSESSED={reports_assessed} FINAL={integrated['canonical_studies']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
