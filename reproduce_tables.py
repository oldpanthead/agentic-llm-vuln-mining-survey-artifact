#!/usr/bin/env python3
"""Validate the public artifact for the integrated search through 2026-07-30.

The default public mode is self-contained. Use ``--manuscript`` only when a
local LaTeX source should also be checked against the artifact snapshot.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
SEARCH = DATA / "search"
CORPUS = DATA / "corpus"
CODING = DATA / "coding"
ADJUDICATION = DATA / "adjudication"
SYNTHESIS = DATA / "synthesis"
DERIVED = DATA / "derived"
ERRORS: list[str] = []
INFOS: list[str] = []

EXPECTED = {
    "source_records": 1785,
    "canonical_studies": 1772,
    "target_studies": 199,
    "extended_studies": 154,
    "background_studies": 668,
    "excluded_studies": 751,
    "alternate_sources": 13,
    "search_occurrences": 12090,
    "search_records": 1642,
    "reports_sought": 278,
    "reports_assessed": 243,
    "new_jointly_included": 132,
}

EVIDENCE = {
    "candidate judgment": 51,
    "controlled task completion": 56,
    "runtime safety signal": 19,
    "reproducible validation": 70,
    "externally traceable material": 3,
}
SHAPES = {
    "candidate-analysis system": 41,
    "feedback-driven fuzzing agent": 33,
    "reproduction-, validation-, and repair-centered agent": 70,
    "long-horizon pentest and CRS agent": 55,
}
LIFECYCLE = {
    "candidate analysis": 153,
    "path and input exploration": 77,
    "execution observation": 115,
    "reproduction and validation": 79,
    "patch validation": 33,
    "reporting and audit": 43,
    "no qualifying label observed": 10,
}
CAPABILITY = {
    "context aggregation / rule extraction": 97,
    "tool routing / strategy routing": 59,
    "feedback interpretation / loop adjustment": 92,
    "validation organization / evidence packaging": 69,
    "long-horizon state management": 41,
    "failure reuse / strategy update": 27,
    "governance / human gates / disclosure control": 9,
    "no qualifying label observed": 65,
}
TRACE = {
    "no external trace reported": 26,
    "author-reported external clue": 41,
    "benchmark ground truth / public material": 128,
    "publicly aligned external trace": 4,
}
PUBLICATION_STATUS = {
    "benchmark/system report": 3,
    "conference": 18,
    "journal": 13,
    "preprint": 164,
    "report/other": 1,
}


def error(message: str) -> None:
    ERRORS.append(message)
    print(f"ERROR: {message}")


def info(message: str) -> None:
    INFOS.append(message)
    print(f"INFO: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        error(message)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        error(f"missing file: {path.relative_to(ROOT)}")
        return []
    with path.open(encoding="utf-8-sig", newline="") as handle:
        raw = csv.reader(handle)
        try:
            header = next(raw)
        except StopIteration:
            error(f"empty CSV: {path.relative_to(ROOT)}")
            return []
    duplicates = sorted({name for name in header if header.count(name) > 1})
    require(not duplicates, f"duplicate CSV header(s) in {path.name}: {duplicates}")
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    require(all(None not in row for row in rows), f"ragged row in {path.name}")
    return rows


def read_derived_table(name: str) -> list[dict[str, str]]:
    bundle = DERIVED / "derived_summary_tables.json"
    if not bundle.exists():
        error(f"missing derived-summary bundle: {bundle.relative_to(ROOT)}")
        return []
    try:
        payload = json.loads(bundle.read_text(encoding="utf-8-sig"))
        require(payload.get("format") == "derived-summary-tables-v1", "invalid derived-summary bundle format")
        table = payload.get("tables", {}).get(name)
        require(isinstance(table, dict), f"derived table missing from bundle: {name}")
        columns = table.get("columns", [])
        rows = table.get("rows", [])
        require(all(isinstance(row, dict) and set(row) == set(columns) for row in rows), f"invalid derived table rows: {name}")
        return rows
    except (json.JSONDecodeError, OSError, TypeError) as exc:
        error(f"cannot read derived-summary bundle: {exc}")
        return []


def read_derived_metadata(name: str) -> dict[str, object]:
    bundle = DERIVED / "derived_summary_tables.json"
    if not bundle.exists():
        error(f"missing derived-summary bundle: {bundle.relative_to(ROOT)}")
        return {}
    try:
        payload = json.loads(bundle.read_text(encoding="utf-8-sig"))
        require(payload.get("format") == "derived-summary-tables-v1", "invalid derived-summary bundle format")
        metadata = payload.get("metadata", {})
        value = metadata.get(name) if isinstance(metadata, dict) else None
        require(isinstance(value, dict), f"derived metadata missing from bundle: {name}")
        return value if isinstance(value, dict) else {}
    except (json.JSONDecodeError, OSError, TypeError) as exc:
        error(f"cannot read derived-summary metadata: {exc}")
        return {}


SYNTHESIS_VIEW_PREFIXES = {
    "publication_status_standardized": "pub",
    "traditional_security_primitives": "prim",
    "target_domain_extraction": "domain",
    "public_artifact_availability": "artifact",
    "controlled_task_only_membership": "task",
    "training_data_overlap_control": "overlap",
}


def read_study_synthesis_view(name: str) -> list[dict[str, str]]:
    prefix = SYNTHESIS_VIEW_PREFIXES[name]
    merged = read_csv(SYNTHESIS / "study_synthesis_199.csv")
    marker = f"{prefix}__"
    view = []
    for row in merged:
        projected = {"matrix_id": row.get("matrix_id", "")}
        projected.update({key[len(marker):]: value for key, value in row.items() if key.startswith(marker)})
        view.append(projected)
    return view


def read_new_reference_metadata() -> list[dict[str, str]]:
    rows = read_csv(CORPUS / "reference_audit.csv")
    marker = "new__"
    view = []
    for row in rows:
        if row.get("new__present") != "yes":
            continue
        projected = {"record_id": row.get("record_id", "")}
        projected.update({key[len(marker):]: value for key, value in row.items() if key.startswith(marker) and key != "new__present"})
        view.append(projected)
    return view


def split_labels(value: str) -> set[str]:
    return {item.strip() for item in (value or "").split(";") if item.strip()}


def count_multilabel(rows: list[dict[str, str]], field: str) -> Counter[str]:
    counts: Counter[str] = Counter()
    for row in rows:
        counts.update(split_labels(row.get(field, "")))
    return counts


def metric_map(path: Path) -> dict[str, int]:
    output: dict[str, int] = {}
    for row in read_csv(path):
        key = row.get("metric") or row.get("stage")
        value = row.get("count") or row.get("value")
        if key and value and str(value).isdigit():
            output[key] = int(value)
    return output


def raw_agreement(first: list[str], second: list[str]) -> float:
    return sum(a == b for a, b in zip(first, second)) / len(first)


def kappa(first: list[str], second: list[str]) -> float:
    observed = raw_agreement(first, second)
    n = len(first)
    ca, cb = Counter(first), Counter(second)
    expected = sum((ca[key] / n) * (cb[key] / n) for key in set(ca) | set(cb))
    if expected == 1:
        return 1.0 if observed == 1.0 else 0.0
    return (observed - expected) / (1 - expected)


def gwet_ac1_binary(first: list[str], second: list[str]) -> float:
    observed = raw_agreement(first, second)
    positive_prevalence = (
        sum(value == "1" for value in first) + sum(value == "1" for value in second)
    ) / (2 * len(first))
    expected = 2 * positive_prevalence * (1 - positive_prevalence)
    if expected == 1:
        return 1.0 if observed == 1.0 else 0.0
    return (observed - expected) / (1 - expected)


def jaccard(a: set[str], b: set[str]) -> float:
    return 1.0 if not (a | b) else len(a & b) / len(a | b)


def micro_f1(pairs: list[tuple[set[str], set[str]]]) -> float:
    tp = sum(len(a & b) for a, b in pairs)
    fp = sum(len(a - b) for a, b in pairs)
    fn = sum(len(b - a) for a, b in pairs)
    return 2 * tp / (2 * tp + fp + fn)


def check_compact_manifest() -> None:
    manifest_path = ROOT / "compact_bundle_manifest.json"
    require(manifest_path.exists(), "missing compact_bundle_manifest.json")
    if not manifest_path.exists():
        return
    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    except (json.JSONDecodeError, OSError) as exc:
        error(f"cannot read compact bundle manifest: {exc}")
        return
    require(payload.get("format") == "compact-audit-release-v2", "invalid compact bundle manifest format")
    core_files = payload.get("core_files", [])
    bundles = payload.get("bundles", {})
    require(isinstance(core_files, list), "compact manifest core_files must be a list")
    require(isinstance(bundles, dict) and bundles, "compact manifest bundles must be a non-empty object")
    require(len(core_files) == len(set(core_files)), "duplicate path in compact manifest core_files")
    for relative in core_files:
        require((ROOT / relative).is_file(), f"compact manifest core file is missing: {relative}")
    members: list[str] = []
    for archive, listed in bundles.items():
        archive_path = ROOT / archive
        require(archive_path.is_file(), f"compact bundle is missing: {archive}")
        require(isinstance(listed, list), f"compact manifest members must be a list: {archive}")
        require(len(listed) == len(set(listed)), f"duplicate path in compact bundle: {archive}")
        members.extend(listed)
        if archive_path.is_file():
            try:
                with zipfile.ZipFile(archive_path) as handle:
                    names = set(handle.namelist())
                for relative in listed:
                    require(relative in names, f"compact bundle member is missing from {archive}: {relative}")
            except zipfile.BadZipFile:
                error(f"invalid compact bundle archive: {archive}")
    require(not (set(core_files) & set(members)), "compact manifest path appears in core and bundle sections")
    require(len(members) == len(set(members)), "compact manifest member appears in multiple bundles")
    info(f"compact manifest paths verified: {len(core_files)} core and {len(members)} bundled")


def check_corpus() -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    corpus = read_csv(CORPUS / "corpus.csv")
    crosswalk = read_csv(CORPUS / "study_version_crosswalk.csv")
    require(len(corpus) == EXPECTED["source_records"], "corpus.csv must contain 1,785 source records")
    require(len(crosswalk) == EXPECTED["source_records"], "crosswalk must contain 1,785 source records")
    corpus_ids = [row.get("record_id", "") for row in corpus]
    crosswalk_ids = [row.get("record_id", "") for row in crosswalk]
    require(len(set(corpus_ids)) == len(corpus_ids), "duplicate record_id in corpus.csv")
    require(set(corpus_ids) == set(crosswalk_ids), "corpus and crosswalk record IDs differ")

    canonical = [row for row in crosswalk if row.get("counting_status") == "canonical_counted"]
    alternates = [row for row in crosswalk if row.get("counting_status") != "canonical_counted"]
    require(len(canonical) == EXPECTED["canonical_studies"], "canonical-study count must be 1,772")
    require(len(alternates) == EXPECTED["alternate_sources"], "alternate/version source count must be 13")
    canonical_ids = [row.get("canonical_study_id", "") for row in canonical]
    require(len(set(canonical_ids)) == len(canonical_ids), "a canonical study is counted more than once")
    layers = Counter(row.get("analytical_layer", "") for row in canonical)
    expected_layers = {
        "study_level_coded": EXPECTED["target_studies"],
        "extended_synthesis": EXPECTED["extended_studies"],
        "background_reference": EXPECTED["background_studies"],
        "excluded_near_neighbor": EXPECTED["excluded_studies"],
    }
    require(layers == expected_layers, f"canonical analytical layers differ: {dict(layers)}")
    info("corpus: 1,785 source records -> 1,772 canonical studies")
    return corpus, crosswalk


def check_matrix() -> list[dict[str, str]]:
    source_matrix = read_csv(CODING / "current_study_level_coding_matrix_harmonized.csv")
    matrix = read_csv(CODING / "adjudicated_study_level_coding_matrix_199.csv")
    require(len(source_matrix) == EXPECTED["target_studies"], "preserved author matrix must contain 199 rows")
    require(
        {row.get("matrix_id", "") for row in source_matrix} == {row.get("matrix_id", "") for row in matrix},
        "preserved author matrix and adjudicated matrix IDs differ",
    )
    require(len(matrix) == EXPECTED["target_studies"], "study-level matrix must contain 199 rows")
    require(len({row.get("matrix_id", "") for row in matrix}) == len(matrix), "matrix_id values must be unique")
    target = [row for row in matrix if row.get("analytical_role") == "target_software_study"]
    require(len(target) == EXPECTED["target_studies"], "target-software denominator must be 199")
    require(Counter(row.get("strongest_evidence_output", "") for row in target) == EVIDENCE, "principal evidence counts differ")
    require(Counter(row.get("primary_system_shape", "") for row in target) == SHAPES, "system-shape counts differ")
    require(count_multilabel(target, "lifecycle_coverage") == LIFECYCLE, "lifecycle counts differ")
    require(count_multilabel(target, "cross_stage_capabilities") == CAPABILITY, "capability counts differ")
    require(Counter(row.get("external_traceability", "") for row in target) == TRACE, "external-trace counts differ")
    require(all(row.get("claim_boundary", "").strip() for row in target), "missing claim-boundary note")
    require(not any(row.get("record_id") == "CP114" for row in matrix), "AgentFuzz must not enter target-software coding")
    info("adjudicated study-level coding: 199 target-software studies")
    return target


def check_adjudication(target: list[dict[str, str]]) -> None:
    decisions = read_csv(ADJUDICATION / "third_party_rereview_decisions_20260824.csv")
    qc_rows = read_csv(ADJUDICATION / "third_party_rereview_qc_20260824.csv")
    material_crosswalk = read_csv(ADJUDICATION / "third_party_rereview_material_crosswalk_20260824.csv")
    log = read_csv(ADJUDICATION / "adjudication_log_199_all_fields.csv")
    statistics = read_derived_table("adjudicated_synthesis_statistics_199.csv")
    completion = read_derived_metadata("adjudication_completion_manifest")

    require(len(decisions) == 410, "third-party decision export must contain 410 disagreements")
    historical_fields = (
        "prior_form_human_final_label", "prior_form_brief_reason",
        "prior_form_evidence_location_verified", "prior_form_reviewer_initials",
        "prior_form_review_date",
    )
    require(all(field in decisions[0] for field in historical_fields), "decision export is missing merged historical-form fields")
    require(all(all(row.get(field, "").strip() for field in historical_fields) for row in decisions), "merged historical-form fields contain blanks")
    require(len(qc_rows) == 50, "third-party QC export must contain 50 separate rows")
    require({row.get("case_id", "") for row in material_crosswalk} == {"A104", "A139", "A011", "A137"}, "corrected-material crosswalk cases differ")
    require(all(re.fullmatch(r"[0-9A-F]{64}", row.get("sha256", "")) for row in material_crosswalk), "corrected-material crosswalk contains an invalid SHA-256")
    require(len({row.get("third_party_task_id", "") for row in decisions}) == len(decisions), "third-party decision export has duplicate task IDs")
    require(all(row.get("third_party_final_label", "").strip() for row in decisions), "third-party decisions have blank final labels")
    require(all(row.get("third_party_brief_reason", "").strip() for row in decisions), "third-party decisions have blank reasons")
    require(all(row.get("third_party_verified_evidence_locator", "").strip() for row in decisions), "third-party decisions have blank evidence locations")
    require(all(row.get("third_party_unresolved", "").strip().lower() == "no" for row in decisions), "third-party decisions contain unresolved rows")
    cnvd = [row for row in decisions if row.get("third_party_task_id") == "R2-159"]
    require(len(cnvd) == 1 and cnvd[0].get("third_party_original_final_label") == "publicly aligned external trace" and cnvd[0].get("third_party_final_label") == "author-reported external clue" and "official-record check" in cnvd[0].get("decision_provenance", ""), "R2-159 post-adjudication provenance differs")
    require(len(log) == 995, "adjudication log must contain one row per study-field assignment")
    require(sum(bool(row.get("disagreement_id", "").strip()) for row in log) == 410, "adjudication log must contain 410 resolved disagreements")
    require(all(row.get("final_label", "").strip() != "unresolved" for row in log), "adjudication log contains unresolved labels")
    require(len(statistics) == 28, "adjudicated statistics must contain all controlled labels and empty-set rows")
    reporting_stat = [
        row for row in statistics
        if row.get("field") == "lifecycle coverage"
        and row.get("label") == "reporting and audit"
    ]
    require(
        len(reporting_stat) == 1
        and reporting_stat[0].get("reportable_point_estimate") == "no"
        and reporting_stat[0].get("interpretation_scope") == "adjudicated descriptive outcome only",
        "reporting-and-audit must be retained only as a low-reliability descriptive outcome",
    )
    require(
        all(
            row.get("reportable_point_estimate") == "yes"
            for row in statistics
            if not (
                row.get("field") == "lifecycle coverage"
                and row.get("label") == "reporting and audit"
            )
        ),
        "another adjudicated statistic is unexpectedly non-reportable",
    )
    expected_statistics = {
        ("lifecycle coverage", "reporting and audit"): 43,
        ("lifecycle coverage", "no qualifying label observed"): 10,
        ("cross-stage capability", "validation organization / evidence packaging"): 69,
        ("cross-stage capability", "no qualifying label observed"): 65,
        ("principal reported evidence output", "externally traceable material"): 3,
        ("external traceability", "publicly aligned external trace"): 4,
    }
    observed_statistics = {
        (row.get("field", ""), row.get("label", "")): int(row["count"])
        for row in statistics
    }
    require(all(observed_statistics.get(key) == value for key, value in expected_statistics.items()), "key adjudicated statistics differ")
    require(completion, "missing adjudication completion metadata")
    if completion:
        require(completion.get("disagreement_rows") == 410, "completion manifest disagreement count differs")
        require(completion.get("unresolved_total") == 0, "completion manifest unresolved count differs")
        final_matrix = completion.get("current_final_matrix", {})
        matrix_path = CODING / "adjudicated_study_level_coding_matrix_199.csv"
        # Git stores the CSV with LF endings, while Windows checkouts may use
        # CRLF.  Hash the canonical LF representation so validation is
        # independent of the checkout platform.
        matrix_bytes = matrix_path.read_bytes().replace(b"\r\n", b"\n")
        matrix_hash = hashlib.sha256(matrix_bytes).hexdigest().upper()
        require(final_matrix.get("path") == "data/coding/adjudicated_study_level_coding_matrix_199.csv", "completion manifest final-matrix path differs")
        require(final_matrix.get("sha256") == matrix_hash, "completion manifest final-matrix hash differs")
        require(final_matrix.get("study_count") == 199 and final_matrix.get("unique_matrix_ids") == 199, "completion manifest final-matrix cardinality differs")
        require(bool(final_matrix.get("freeze_recorded_utc")), "completion manifest final-matrix freeze time is missing")
    require({row.get("matrix_id", "") for row in log} == {row.get("matrix_id", "") for row in target}, "adjudication log and matrix IDs differ")
    matrix_fields = {
        "lifecycle coverage": "lifecycle_coverage",
        "cross-stage capability": "cross_stage_capabilities",
        "primary system shape": "primary_system_shape",
        "principal reported evidence output": "strongest_evidence_output",
        "external traceability": "external_traceability",
    }
    matrix_by_id = {row.get("matrix_id", ""): row for row in target}
    log_by_key = {(row.get("matrix_id", ""), row.get("field", "")): row for row in log}
    for matrix_id, matrix_row in matrix_by_id.items():
        for field, matrix_column in matrix_fields.items():
            log_row = log_by_key.get((matrix_id, field))
            require(log_row is not None, f"adjudication log is missing {matrix_id} / {field}")
            if log_row is not None:
                require(
                    split_labels(log_row.get("final_label", "")) == split_labels(matrix_row.get(matrix_column, "")),
                    f"adjudication log final label differs from final matrix: {matrix_id} / {field}",
                )
    info("third-party external rereview: 410 disagreements integrated; 50 QC rows kept separate; 0 unresolved")


def check_claim_alignment() -> None:
    rows = read_csv(ADJUDICATION / "claim_alignment_reconciled_199.csv")
    require(len(rows) == EXPECTED["target_studies"], "claim-alignment reconciliation must contain 199 rows")
    require(len({row.get("matrix_id", "") for row in rows}) == len(rows), "duplicate matrix_id in claim-alignment reconciliation")
    require(
        Counter(row.get("final_claim_alignment", "") for row in rows) == {"aligned": 190, "overclaim": 9},
        "claim-alignment final distribution differs",
    )
    require(sum(row.get("independent_agreement", "") == "yes" for row in rows) == 155, "claim-alignment independent-agreement count differs")
    require(sum(bool(row.get("rong_final_label", "").strip()) for row in rows) == 44, "claim-alignment adjudication count differs")
    info("claim-alignment reconciliation: 155 agreements, 44 adjudicated disagreements, 190 aligned and 9 overclaim")


def check_extended(target: list[dict[str, str]]) -> None:
    rows = read_csv(CODING / "extended_synthesis_audit.csv")
    require(len(rows) == EXPECTED["extended_studies"], "extended synthesis must contain 154 studies")
    require(len({row.get("record_id", "") for row in rows}) == len(rows), "duplicate extended-synthesis record")
    target_records = {row.get("record_id", "") for row in target}
    require(not (target_records & {row.get("record_id", "") for row in rows}), "study-level and extended layers overlap")
    require(all(row.get("extracted_contribution", "").strip() for row in rows), "missing extended-synthesis contribution")
    require(all(row.get("reason_not_study_level_coded", "").strip() for row in rows), "missing extended-synthesis boundary reason")
    require(all(row.get("public_material_basis", "").strip() for row in rows), "missing extended-synthesis source basis")
    require(sum(row.get("record_id") == "CP114" for row in rows) == 1, "AgentFuzz must appear once in extended synthesis")
    metadata_only = [
        row for row in rows
        if re.search(r"title(?:/|-and-)?abstract metadata", row.get("reviewer_note", ""), re.I)
    ]
    require(len(metadata_only) == 62, "extended-synthesis metadata-supported count must be 62")
    require(len(rows) - len(metadata_only) == 92, "extended-synthesis full-text-supported count must be 92")
    info("extended synthesis: 92 full-text-supported and 62 metadata-supported studies")


def check_search_and_dedup() -> None:
    results = read_csv(SEARCH / "final_multisource_search_20260730_results.csv")
    screened = read_csv(SEARCH / "final_multisource_search_20260730_screening_audit.csv")
    completed = read_csv(SEARCH / "final_multisource_search_20260730_complete_screening.csv")
    require(len(results) == EXPECTED["search_occurrences"], "search export must contain 12,090 source occurrences")
    require(len(screened) == EXPECTED["search_records"], "screening audit must contain 1,642 unique records")
    require(len(completed) == EXPECTED["search_records"], "complete screening audit must contain 1,642 unique records")
    require(len({row.get("discovery_id", "") for row in completed}) == EXPECTED["search_records"], "complete screening audit contains duplicate discovery IDs")
    require(all(row.get("final_analytical_layer", "").strip() for row in completed), "complete screening audit contains an unresolved final layer")
    completed_layers = Counter(row["final_analytical_layer"] for row in completed)
    require(
        completed_layers == Counter({
            "excluded_near_neighbor": 731,
            "background_reference": 573,
            "study_level": 132,
            "existing_study_or_version": 110,
            "extended_synthesis": 88,
            "version_reconciliation": 8,
        }),
        f"complete screening layer counts differ: {dict(completed_layers)}",
    )
    unretrieved = [row for row in completed if row["screening_stage"] == "report_retrieval"]
    require(len(unretrieved) == 35, "report-not-retrieved count must be 35")
    require(
        not any(row["final_analytical_layer"] in {"study_level", "extended_synthesis"} for row in unretrieved),
        "a report-not-retrieved record entered an analytical synthesis layer",
    )
    exclusion_summary = read_derived_table("final_multisource_exclusion_summary.csv")
    expected_exclusions = {
        "interface_title_abstract_exclusions": 703,
        "interface_full_text_exclusions": 3,
        "interface_retrieval_stage_exclusions": 25,
        "supplementary_retained_exclusions": 20,
    }
    require(
        {row.get("exclusion_group", ""): int(row.get("count", "0")) for row in exclusion_summary}
        == expected_exclusions,
        "high-level exclusion account differs",
    )
    require(sum(expected_exclusions.values()) == EXPECTED["excluded_studies"], "exclusion account does not close")
    prisma = {row["metric"]: int(row["count"]) for row in read_csv(SEARCH / "final_multisource_search_20260730_prisma_counts.csv")}
    integrated_checks = {
        "integrated_source_records": 1785,
        "alternate_or_duplicate_source_versions_not_counted": 13,
        "version_reconciled_studies_screened": 1772,
        "target_software_studies_with_detailed_material": 199,
        "extended_synthesis_full_text_or_equivalent": 92,
        "extended_synthesis_metadata_supported": 62,
        "final_extended_synthesis_studies": 154,
        "background_reference_studies": 668,
        "excluded_studies": 751,
    }
    require(
        all(prisma.get(key) == value for key, value in integrated_checks.items()),
        "integrated manuscript-facing PRISMA counts differ from the final ledger",
    )
    require(
        integrated_checks["target_software_studies_with_detailed_material"]
        + integrated_checks["final_extended_synthesis_studies"]
        + integrated_checks["background_reference_studies"]
        + integrated_checks["excluded_studies"]
        == integrated_checks["version_reconciled_studies_screened"],
        "integrated analytical layers do not sum to the version-reconciled study count",
    )
    provenance_checks = {
        "exported_source_occurrences": 12090,
        "removed_by_deterministic_query_filter": 9801,
        "source_occurrences_entering_deduplication": 2289,
        "duplicate_source_occurrences_removed": 647,
        "unique_search_records_screened": 1642,
        "records_not_advanced_to_report_retrieval": 1364,
        "reports_sought": 278,
        "reports_not_retrieved": 35,
        "reports_assessed_at_full_text": 243,
        "full_text_study_level": 132,
        "full_text_extended_synthesis": 87,
        "full_text_background_reference": 21,
        "full_text_excluded_near_neighbor": 3,
        "current_search_matches_to_retained_studies": 110,
        "new_or_reconciled_source_records_added": 1532,
        "supplementary_source_records_not_reidentified": 143,
        "prior_canonical_studies_not_reidentified": 138,
        "prior_source_records": 253,
        "prior_canonical_studies": 248,
        "prior_target_software_studies": 67,
        "prior_extended_synthesis_studies": 65,
        "prior_governance_boundary_record": 1,
        "new_canonical_studies": 1524,
        "new_target_software_studies": 132,
        "new_extended_synthesis_studies": 88,
        "new_extended_full_text_supported": 87,
        "new_extended_metadata_supported": 1,
        "new_background_reference_studies": 573,
        "new_excluded_studies": 731,
        "extended_synthesis_full_text_supported": 92,
        "extended_synthesis_metadata_supported": 62,
        "integrated_canonical_studies": 1772,
        "target_software_studies": 199,
        "extended_synthesis_studies": 154,
    }
    require(
        all(prisma.get(key) == value for key, value in provenance_checks.items()),
        "source-specific acquisition provenance differs from frozen audit files",
    )
    resolutions = read_csv(SEARCH / "final_multisource_search_20260730_dedup_resolutions.csv")
    require(len(resolutions) == 124, "dedup audit must contain 124 candidate pairs")
    require(not any(row.get("audit_decision") == "needs_author_confirmation" for row in resolutions), "unresolved dedup pair remains")
    require(sum(row.get("audit_decision") == "same_study_or_version" for row in resolutions) == 119, "same-study/version resolution count differs")
    info("integrated PRISMA allocation and source-specific provenance verified through 2026-07-30")


def check_supplementary_extractions(target: list[dict[str, str]]) -> None:
    primitives = read_study_synthesis_view("traditional_security_primitives")
    require(len(primitives) == EXPECTED["target_studies"], "traditional-security-primitives extraction must contain 199 rows")
    require({row.get("matrix_id", "") for row in primitives} == {row.get("matrix_id", "") for row in target}, "primitive extraction IDs differ from target matrix")
    allowed = {
        "static_taint_specification", "fuzzing_input_harness", "symbolic_constraint",
        "runtime_oracle", "replay_poc_pov", "patch_build_test",
        "recon_scan_pentest", "not specified",
    }
    observed = set().union(*(split_labels(row.get("primitive_tags", "")) for row in primitives))
    require(observed <= allowed, f"unknown primitive tag(s): {sorted(observed - allowed)}")
    require(all(row.get("source_location", "").strip() for row in primitives), "primitive extraction missing source location")

    detailed = read_csv(SYNTHESIS / "traditional_security_primitives_by_use_role.csv")
    require(len(detailed) == 503, "study-primitive role extraction must contain 503 rows")
    target_ids = {row.get("matrix_id", "") for row in target}
    require({row.get("matrix_id", "") for row in detailed} <= target_ids, "study-primitive role extraction contains a non-target ID")
    require(
        len({(row.get("matrix_id", ""), row.get("primitive_family", "")) for row in detailed}) == len(detailed),
        "duplicate study-primitive pair in role extraction",
    )
    require(
        {row.get("use_role", "") for row in detailed} <= {"workflow-active use", "evaluation/support use", "both"},
        "unknown primitive use role",
    )
    require(all(row.get("source_location", "").strip() for row in detailed), "role extraction missing source location")
    role_summary = {row["primitive_family"]: row for row in read_derived_table("traditional_security_primitive_use_role_counts.csv")}
    require(len(role_summary) == 7, "primitive role summary must contain seven families")
    for family, summary in role_summary.items():
        rows = [row for row in detailed if row["primitive_family"] == family]
        active = {row["matrix_id"] for row in rows if row["use_role"] in {"workflow-active use", "both"}}
        support = {row["matrix_id"] for row in rows if row["use_role"] in {"evaluation/support use", "both"}}
        both = active & support
        union = active | support
        require(int(summary["workflow_active_studies"]) == len(active), f"workflow-active primitive count differs: {family}")
        require(int(summary["evaluation_support_studies"]) == len(support), f"evaluation/support primitive count differs: {family}")
        require(int(summary["both_roles"]) == len(both), f"both-role primitive count differs: {family}")
        require(int(summary["union_studies"]) == len(union), f"primitive union count differs: {family}")
        require(int(summary["denominator"]) == 199, f"primitive denominator differs: {family}")
    unspecified = read_derived_table("traditional_security_primitives_not_specified.csv")
    require(len(unspecified) == 3, "primitive-not-specified audit must contain three studies")
    require({row["matrix_id"] for row in unspecified} == target_ids - {row["matrix_id"] for row in detailed}, "primitive-not-specified IDs do not close")

    output_by_id = {row["matrix_id"]: row["strongest_evidence_output"] for row in target}
    primitive_output = read_derived_table("traditional_security_primitive_by_output.csv")
    require(len(primitive_output) == 35, "primitive-output cross-tab must contain 35 rows")
    for family, summary in role_summary.items():
        family_ids = {row["matrix_id"] for row in detailed if row["primitive_family"] == family}
        rows = [row for row in primitive_output if row["primitive_family"] == family]
        require(len(rows) == 5, f"primitive-output cross-tab lacks output categories: {family}")
        for row in rows:
            actual = sum(output_by_id[matrix_id] == row["principal_reported_evidence_output"] for matrix_id in family_ids)
            require(actual == int(row["count"]), f"primitive-output count differs: {family} {row['principal_reported_evidence_output']}")
            require(int(row["primitive_union_denominator"]) == len(family_ids), f"primitive-output denominator differs: {family}")

    refs = read_csv(CORPUS / "reference_audit.csv")
    require(len(refs) == 385, "reference audit must contain 385 non-product rows")
    new_refs = read_new_reference_metadata()
    require(len(new_refs) == 132, "new target-study reference metadata must contain 132 rows")
    require(all(row.get("official_url", "").strip() for row in new_refs), "new reference metadata missing official URL")
    refs_by_id = {row.get("record_id", ""): row for row in refs}
    for row in new_refs:
        audited = refs_by_id.get(row.get("record_id", ""), {})
        require(
            audited.get("publication_status") == row.get("publication_status")
            and audited.get("official_url") == row.get("official_url"),
            f"reference audit differs from generated metadata: {row.get('record_id', '')}",
        )

    info("supplementary primitive roles, output coupling, and reference metadata verified")


def check_publication_status(target: list[dict[str, str]]) -> None:
    rows = read_study_synthesis_view("publication_status_standardized")
    target_rows = [row for row in rows if row.get("analytical_role") == "target_software_study"]
    require(len(rows) == 199, "publication-status view must contain 199 target-software records")
    require(len(target_rows) == EXPECTED["target_studies"], "publication-status target denominator must be 199")
    require(
        Counter(row.get("publication_status_standardized", "") for row in target_rows) == PUBLICATION_STATUS,
        "publication-status counts differ",
    )
    require(
        {row.get("matrix_id", "") for row in target_rows} == {row.get("matrix_id", "") for row in target},
        "publication-status IDs differ from target matrix",
    )
    target_by_id = {row["matrix_id"]: row for row in target}
    for row in target_rows:
        coded = target_by_id[row["matrix_id"]]
        require(row["strongest_evidence_output"] == coded["strongest_evidence_output"], f"publication-status output differs: {row['matrix_id']}")
        require(row["primary_system_shape"] == coded["primary_system_shape"], f"publication-status shape differs: {row['matrix_id']}")
        require(row["cross_stage_capabilities"] == coded["cross_stage_capabilities"], f"publication-status capabilities differ: {row['matrix_id']}")
        require(row["external_traceability"] == coded["external_traceability"], f"publication-status traceability differs: {row['matrix_id']}")
    distribution = {row["publication_status_standardized"]: row for row in read_derived_table("publication_status_distribution_by_layer.csv")}
    require(set(distribution) == set(PUBLICATION_STATUS), "publication-status distribution categories differ")
    for status, count in PUBLICATION_STATUS.items():
        require(int(distribution[status]["target_software_studies"]) == count, f"publication-status total differs: {status}")
    peer = [row for row in target_rows if row["publication_status_standardized"] in {"conference", "journal"}]
    preprints = [row for row in target_rows if row["publication_status_standardized"] == "preprint"]
    require(len(peer) == 31 and len(preprints) == 164, "publication-status manuscript denominators differ")
    sensitivity = read_derived_table("publication_status_sensitivity_analysis.csv")
    require(len(sensitivity) == 31, "publication-status sensitivity view must contain 31 rows")
    require({row["publication_status_group"] for row in sensitivity} == {
        "all_target_software", "conference_or_journal", "preprint", "benchmark_report_or_other"
    }, "publication-status sensitivity groups differ")
    for group, denominator in {
        "all_target_software": 199,
        "conference_or_journal": 31,
        "preprint": 164,
        "benchmark_report_or_other": 4,
    }.items():
        subset = [row for row in sensitivity if row["publication_status_group"] == group]
        require(all(int(row["denominator"]) == denominator for row in subset), f"publication sensitivity denominator differs: {group}")
        require(sum(int(row["count"]) for row in subset if row["dimension"] == "primary_system_shape") == denominator, f"publication shape counts do not close: {group}")
        require(sum(int(row["count"]) for row in subset if row["dimension"] == "principal_reported_evidence_output") == denominator, f"publication output counts do not close: {group}")
    info("publication-status assignments and manuscript-facing stratification verified")


def check_domain_and_reporting_extractions(target: list[dict[str, str]]) -> None:
    target_by_id = {row["matrix_id"]: row for row in target}
    target_ids = set(target_by_id)

    domains = read_study_synthesis_view("target_domain_extraction")
    require(len(domains) == 199, "target-domain extraction must contain 199 rows")
    require({row["matrix_id"] for row in domains} == target_ids, "target-domain IDs differ from target matrix")
    require(all(row["source_location"].strip() for row in domains), "target-domain extraction missing source location")
    allowed_domains = {
        "repository, package, or source code", "cyber range, CTF, or penetration testing",
        "mixed or general software targets", "smart contract and blockchain",
        "web application, API, or database", "native binary, compiler, or operating system",
        "firmware, embedded, IoT, or OT", "protocol and networked service",
    }
    require({row["target_domain"] for row in domains} == allowed_domains, "target-domain categories differ")
    for row in domains:
        coded = target_by_id[row["matrix_id"]]
        require(row["primary_system_shape"] == coded["primary_system_shape"], f"domain shape differs: {row['matrix_id']}")
        require(row["principal_reported_evidence_output"] == coded["strongest_evidence_output"], f"domain output differs: {row['matrix_id']}")

    domain_cross = read_derived_table("target_domain_by_principal_output.csv")
    require(len(domain_cross) == 40, "domain-output cross-tab must contain 40 rows")
    for row in domain_cross:
        subset = [item for item in domains if item["target_domain"] == row["target_domain"]]
        actual = sum(item["principal_reported_evidence_output"] == row["principal_reported_evidence_output"] for item in subset)
        require(actual == int(row["count"]), f"domain-output count differs: {row['target_domain']} {row['principal_reported_evidence_output']}")
        require(len(subset) == int(row["domain_denominator"]), f"domain denominator differs: {row['target_domain']}")

    year_cross = read_derived_table("publication_year_by_primary_shape.csv")
    require(len(year_cross) == 16, "year-shape cross-tab must contain 16 rows")
    for row in year_cross:
        subset = [item for item in domains if item["publication_year"] == row["publication_year"]]
        actual = sum(item["primary_system_shape"] == row["primary_system_shape"] for item in subset)
        require(actual == int(row["count"]), f"year-shape count differs: {row['publication_year']} {row['primary_system_shape']}")
        require(len(subset) == int(row["year_denominator"]), f"year denominator differs: {row['publication_year']}")

    artifacts = read_study_synthesis_view("public_artifact_availability")
    require(len(artifacts) == 199, "public-artifact extraction must contain 199 rows")
    require({row["matrix_id"] for row in artifacts} == target_ids, "public-artifact IDs differ from target matrix")
    artifact_fields = (
        "public_implementation_located", "environment_or_build_instructions",
        "trigger_replay_poc_pov_artifact", "execution_trace_or_log", "patch_artifact",
    )
    require(all(row["source_location"].strip() for row in artifacts), "public-artifact extraction missing source location")
    require(all(row[field] in {"located", "not located"} for row in artifacts for field in artifact_fields), "unknown public-artifact status")
    require(all(row["principal_reported_evidence_output"] == target_by_id[row["matrix_id"]]["strongest_evidence_output"] for row in artifacts), "public-artifact output labels differ")
    artifact_summary = {row["principal_reported_evidence_output"]: row for row in read_derived_table("principal_output_by_public_artifact_availability.csv")}
    require(set(artifact_summary) == set(EVIDENCE), "public-artifact summary output categories differ")
    for output, summary in artifact_summary.items():
        subset = [row for row in artifacts if row["principal_reported_evidence_output"] == output]
        require(len(subset) == int(summary["studies"]), f"public-artifact output denominator differs: {output}")
        for field in artifact_fields:
            require(sum(row[field] == "located" for row in subset) == int(summary[field]), f"public-artifact count differs: {output} {field}")

    # A public repository or benchmark input is not, by itself, a public
    # system-generated trigger/replay. The row-level index is the authority
    # for this deliberately narrow Table 10 column.
    trigger_index = read_csv(SYNTHESIS / "public_trigger_replay_evidence_index.csv")
    trigger_candidates = {row["matrix_id"] for row in trigger_index}
    require(len(trigger_index) == 14 and len(trigger_candidates) == 14, "trigger/replay index must retain 14 unique reviewed candidates")
    require(trigger_candidates <= target_ids, "trigger/replay index contains a non-matrix study")
    require(all(row["included_in_table_10"] in {"yes", "no"} for row in trigger_index), "invalid Table 10 trigger inclusion flag")
    included_triggers = {row["matrix_id"] for row in trigger_index if row["included_in_table_10"] == "yes"}
    located_triggers = {row["matrix_id"] for row in artifacts if row["trigger_replay_poc_pov_artifact"] == "located"}
    require(included_triggers == located_triggers == {"C02"}, "strict public trigger/replay index and artifact table differ")
    require(all(row.get("trigger_replay_evidence_scope", "") for row in artifacts), "missing trigger/replay evidence scope")

    membership = read_study_synthesis_view("controlled_task_only_membership")
    require(len(membership) == 199, "controlled-task membership must contain 199 rows")
    require({row["matrix_id"] for row in membership} == target_ids, "controlled-task membership IDs differ from final matrix")
    domain_by_id = {row["matrix_id"]: row for row in domains}
    excluded_ids = set()
    for row in membership:
        matrix_row = target_by_id[row["matrix_id"]]
        expected_excluded = (
            matrix_row["strongest_evidence_output"] == "controlled task completion"
            and domain_by_id[row["matrix_id"]]["target_domain"] == "cyber range, CTF, or penetration testing"
        )
        require(row["controlled_task_only_excluded"] == ("yes" if expected_excluded else "no"), f"controlled-task membership differs: {row['matrix_id']}")
        require(row["principal_reported_evidence_output"] == matrix_row["strongest_evidence_output"], f"controlled-task output differs: {row['matrix_id']}")
        require(row["target_domain"] == domain_by_id[row["matrix_id"]]["target_domain"], f"controlled-task domain differs: {row['matrix_id']}")
        require(row["decision_reason"].strip() and row["domain_source_location"].strip(), f"controlled-task membership lacks provenance: {row['matrix_id']}")
        if expected_excluded:
            excluded_ids.add(row["matrix_id"])
    require(len(excluded_ids) == 35, f"controlled-task exclusion size differs: {len(excluded_ids)}")

    sensitivity = read_derived_table("controlled_task_only_sensitivity.csv")
    require(len(sensitivity) == 6, "controlled-task sensitivity must contain six result rows")
    expected_sensitivity = {
        ("all_target_software", "author_reported_reproducible_validation"): (70, 199),
        ("all_target_software", "publicly_aligned_external_trace"): (4, 199),
        ("all_target_software", "author_reported_external_clue"): (41, 199),
        ("excluding_controlled_task_only", "author_reported_reproducible_validation"): (70, 164),
        ("excluding_controlled_task_only", "publicly_aligned_external_trace"): (4, 164),
        ("excluding_controlled_task_only", "author_reported_external_clue"): (41, 164),
    }
    actual_sensitivity = {
        (row["scope"], row["measure"]): (int(row["count"]), int(row["denominator"]))
        for row in sensitivity
    }
    require(actual_sensitivity == expected_sensitivity, "controlled-task sensitivity differs from final matrix")
    require(all(row["controlled_task_only_excluded"] in {"0", "35"} for row in sensitivity), "controlled-task exclusion size differs")
    retained = [row for row in target if row["matrix_id"] not in excluded_ids]
    computed_sensitivity = {
        ("all_target_software", "author_reported_reproducible_validation"): (sum(row["strongest_evidence_output"] == "reproducible validation" for row in target), len(target)),
        ("all_target_software", "publicly_aligned_external_trace"): (sum(row["external_traceability"] == "publicly aligned external trace" for row in target), len(target)),
        ("all_target_software", "author_reported_external_clue"): (sum(row["external_traceability"] == "author-reported external clue" for row in target), len(target)),
        ("excluding_controlled_task_only", "author_reported_reproducible_validation"): (sum(row["strongest_evidence_output"] == "reproducible validation" for row in retained), len(retained)),
        ("excluding_controlled_task_only", "publicly_aligned_external_trace"): (sum(row["external_traceability"] == "publicly aligned external trace" for row in retained), len(retained)),
        ("excluding_controlled_task_only", "author_reported_external_clue"): (sum(row["external_traceability"] == "author-reported external clue" for row in retained), len(retained)),
    }
    require(actual_sensitivity == computed_sensitivity, "controlled-task sensitivity is not mechanically reproduced from membership and final matrix")

    alignment = read_csv(SYNTHESIS / "public_alignment_evidence_index.csv")
    alignment_ids = {row["matrix_id"] for row in alignment}
    matrix_alignment_ids = {row["matrix_id"] for row in target if row["external_traceability"] == "publicly aligned external trace"}
    require(len(alignment) == 4 and alignment_ids == matrix_alignment_ids, "public-alignment index differs from final matrix")
    require(sum(row["principal_reported_evidence_output"] == "externally traceable material" for row in alignment) == 3, "principal externally-traceable cases differ")
    required_alignment_fields = ("system_output", "exact_item", "software_and_version", "validation_material", "public_external_record", "attribution", "local_evidence_locator")
    require(all(all(row.get(field, "").strip() for field in required_alignment_fields) for row in alignment), "public-alignment index lacks a structured local evidence chain")

    contamination = read_study_synthesis_view("training_data_overlap_control")
    require(len(contamination) == 199, "training-overlap extraction must contain 199 rows")
    require({row["matrix_id"] for row in contamination} == target_ids, "training-overlap IDs differ from target matrix")
    require(all(row["source_location"].strip() for row in contamination), "training-overlap extraction missing source location")
    contamination_counts = Counter(row["training_data_overlap_control"] for row in contamination)
    require(contamination_counts == Counter({"explicit control": 6, "discussion only": 2, "not located": 191}), f"training-overlap counts differ: {dict(contamination_counts)}")
    summary_counts = {row["status"]: int(row["count"]) for row in read_derived_table("training_data_overlap_control_counts.csv")}
    require(summary_counts == dict(contamination_counts), "training-overlap summary differs")
    info("target-domain, strict public-artifact, sensitivity, public-alignment, and training-overlap extractions verified")


def check_second_coder(target: list[dict[str, str]]) -> None:
    new = read_csv(SEARCH / "final_multisource_search_20260730_all_coder_comparison.csv")
    require(len(new) == 136, "new-search coder comparison must contain 136 reviewed records")
    require(sum(row.get("jointly_included") == "true" for row in new) == 132, "jointly included new studies must equal 132")
    integrated = read_csv(ADJUDICATION / "integrated_199_second_coder_comparison_20260730.csv")
    require(len(integrated) == EXPECTED["target_studies"], "integrated coder comparison must contain 199 studies")
    require({row.get("record_id", "") for row in integrated} == {row.get("matrix_id", "") for row in target}, "integrated coder IDs differ from target matrix")

    expected_single = {
        "primary_shape": (0.884, 0.843),
        "principal_evidence": (0.759, 0.665),
        "external_traceability": (0.724, 0.448),
    }
    for field, expected in expected_single.items():
        first = [row[f"first_{field}"] for row in integrated]
        second = [row[f"second_{field}"] for row in integrated]
        actual = (raw_agreement(first, second), kappa(first, second))
        require(all(abs(a - e) < 0.0006 for a, e in zip(actual, expected)), f"{field} reliability differs: {actual}")

    expected_multi = {
        "lifecycle": (0.261, 0.726, 0.831),
        "capability": (0.312, 0.782, 0.874),
    }
    for field, expected in expected_multi.items():
        pairs = [
            (split_labels(row[f"first_{field}"]), split_labels(row[f"second_{field}"]))
            for row in integrated
        ]
        actual = (
            sum(a == b for a, b in pairs) / len(pairs),
            sum(jaccard(a, b) for a, b in pairs) / len(pairs),
            micro_f1(pairs),
        )
        require(all(abs(a - e) < 0.0006 for a, e in zip(actual, expected)), f"{field} reliability differs: {actual}")
    per_label = read_csv(ADJUDICATION / "integrated_199_per_label_reliability_20260730.csv")
    require(len(per_label) == 13, "per-label reliability must contain 13 controlled labels")
    for row in per_label:
        field = row["field"]
        require(field in {"lifecycle", "capability"}, f"unknown per-label field: {field}")
        label = row["label"]
        first_binary = ["1" if label in split_labels(item[f"first_{field}"]) else "0" for item in integrated]
        second_binary = ["1" if label in split_labels(item[f"second_{field}"]) else "0" for item in integrated]
        actual = {
            "first_positive": sum(value == "1" for value in first_binary),
            "second_positive": sum(value == "1" for value in second_binary),
            "raw_agreement": raw_agreement(first_binary, second_binary),
            "cohen_kappa": kappa(first_binary, second_binary),
            "gwet_ac1": gwet_ac1_binary(first_binary, second_binary),
        }
        require(int(row["n"]) == 199, f"per-label denominator differs: {field} {label}")
        require(int(row["first_positive"]) == actual["first_positive"], f"first positive count differs: {field} {label}")
        require(int(row["second_positive"]) == actual["second_positive"], f"second positive count differs: {field} {label}")
        for metric in ("raw_agreement", "cohen_kappa", "gwet_ac1"):
            require(abs(float(row[metric]) - actual[metric]) < 0.000002, f"{metric} differs: {field} {label}")
    reporting = read_csv(ADJUDICATION / "integrated_199_reporting_audit_disagreement_review.csv")
    require(len(reporting) == 82, "reporting/audit disagreement audit must contain 82 rows")
    require(Counter(row["disagreement_direction"] for row in reporting) == Counter({"second_only": 78, "first_only": 4}), "reporting/audit disagreement directions differ")
    require({row["matrix_id"] for row in reporting} <= {row["record_id"] for row in integrated}, "reporting/audit audit contains an unknown study")
    require(all(row["boundary_basis"].strip() for row in reporting), "reporting/audit disagreement missing boundary basis")
    info("complete independent coding comparison, per-label AC1, and disagreement audit verified")


def check_private_paths() -> None:
    private_path_patterns = (
        re.compile(r"[A-Za-z]:\\Users\\[^\\\s]+"),
        re.compile(r"/Users/[^/\s]+"),
        re.compile(r"artifact_public_release_candidate/data/"),
    )
    for path in [ROOT / "README.md", ROOT / "SECURITY_BOUNDARY.md", ROOT / "docs/coding/data_dictionary.md"]:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        for pattern in private_path_patterns:
            require(not pattern.search(text), f"private or stale path in {path.name}: {pattern.pattern}")


def read_manuscript_tree(path: Path, seen: set[Path] | None = None) -> str:
    seen = set() if seen is None else seen
    path = path.resolve()
    if path in seen or not path.is_file():
        return ""
    seen.add(path)
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    parts = [text]
    for match in re.findall(r"\\(?:input|include)\{([^}]+)\}", text):
        child = path.parent / match
        if child.suffix == "":
            child = child.with_suffix(".tex")
        parts.append(read_manuscript_tree(child, seen))
    return "\n".join(parts)


def check_manuscript(path: Path) -> None:
    if not path.is_file():
        error(f"manuscript not found: {path}")
        return
    text = read_manuscript_tree(path)
    for required in ("1,785", "1,772", "199", "154", "668", "751"):
        require(required in text, f"manuscript does not contain integrated value/date: {required}")
    require(
        "2026-07-30" in text or "July 30, 2026" in text,
        "manuscript does not contain the integrated search cutoff date",
    )
    lowered = text.lower().replace(" ", "")
    forbidden = (
        "currentinterfacesearch",
        "priorretainedsearchpath",
        "previouslyretainedstudies",
        "67+132",
        "65+84+1",
        "30+37",
        "notreidentified",
        "143sourcerecords",
        "138studies",
    )
    for phrase in forbidden:
        require(phrase not in lowered, f"manuscript retains historical-round narrative: {phrase}")
    for phrase in ("6--18/199", "78--83/199", "18--27/199", "147--180", "78--152"):
        require(phrase not in text, f"manuscript retains superseded pre-adjudication range: {phrase}")
    for phrase in (
        "primaryauthor-codedmatrix",
        "undercompletesecond-codersubstitution",
        "descriptiverangesforthisstudyset",
        "changesfromsixto18studies",
    ):
        require(phrase not in lowered, f"manuscript treats pre-adjudication assignments as descriptive results: {phrase}")
    for match in re.findall(r"\\path\{([^}]+)\}", text):
        if match.startswith("data/") or match.endswith((".md", ".py", ".txt")):
            require((ROOT / match).exists(), f"manuscript artifact path is missing: {match}")
    info(f"unified manuscript flow checked across included TeX files: {path}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manuscript", type=Path, help="optional path to main_acm_csur.tex")
    parser.add_argument("--expanded-compact-release", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()

    compact_manifest = ROOT / "compact_bundle_manifest.json"
    if compact_manifest.exists() and not SEARCH.exists() and not args.expanded_compact_release:
        try:
            bundle_manifest = json.loads(compact_manifest.read_text(encoding="utf-8-sig"))
            bundles = bundle_manifest.get("bundles", {})
            require(isinstance(bundles, dict) and bundles, "invalid compact bundle manifest")
            if ERRORS:
                print(f"VALIDATION_FAILED errors={len(ERRORS)}")
                return 1
            with tempfile.TemporaryDirectory(prefix="artifact-validate-") as temporary:
                expanded = Path(temporary) / "artifact"
                shutil.copytree(ROOT, expanded)
                for archive in bundles:
                    archive_path = expanded / archive
                    require(archive_path.is_file(), f"compact bundle is missing: {archive}")
                    if archive_path.is_file():
                        with zipfile.ZipFile(archive_path) as handle:
                            handle.extractall(expanded)
                if ERRORS:
                    print(f"VALIDATION_FAILED errors={len(ERRORS)}")
                    return 1
                command = [sys.executable, "reproduce_tables.py", "--expanded-compact-release"]
                if args.manuscript:
                    command.extend(["--manuscript", str(args.manuscript.resolve())])
                return subprocess.run(command, cwd=expanded, check=False).returncode
        except (OSError, json.JSONDecodeError, zipfile.BadZipFile) as exc:
            error(f"cannot expand compact artifact release: {exc}")
            print(f"VALIDATION_FAILED errors={len(ERRORS)}")
            return 1

    check_compact_manifest()
    _, _ = check_corpus()
    target = check_matrix()
    check_extended(target)
    check_search_and_dedup()
    check_adjudication(target)
    check_claim_alignment()
    check_supplementary_extractions(target)
    check_publication_status(target)
    check_domain_and_reporting_extractions(target)
    check_second_coder(target)
    check_private_paths()
    if args.manuscript:
        check_manuscript(args.manuscript.resolve())
    else:
        info("public mode: manuscript source was not requested and no external LaTeX path was used")

    if ERRORS:
        print(f"VALIDATION_FAILED errors={len(ERRORS)}")
        return 1
    print("VALIDATION_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
