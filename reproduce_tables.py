#!/usr/bin/env python3
"""Validate the public artifact for the integrated search through 2026-07-30.

The default public mode is self-contained. Use ``--manuscript`` only when a
local LaTeX source should also be checked against the artifact snapshot.
"""

from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
ERRORS: list[str] = []
INFOS: list[str] = []

EXPECTED = {
    "source_records": 1785,
    "canonical_studies": 1772,
    "target_studies": 199,
    "extended_studies": 150,
    "background_studies": 670,
    "excluded_studies": 753,
    "alternate_sources": 13,
    "search_occurrences": 12090,
    "search_records": 1642,
    "reports_sought": 274,
    "reports_assessed": 239,
    "new_jointly_included": 132,
}

EVIDENCE = {
    "candidate judgment": 34,
    "controlled task completion": 55,
    "runtime safety signal": 21,
    "reproducible validation": 83,
    "externally traceable material": 6,
}
SHAPES = {
    "candidate-analysis system": 46,
    "feedback-driven fuzzing agent": 34,
    "reproduction-, validation-, and repair-centered agent": 62,
    "long-horizon pentest and CRS agent": 57,
}
LIFECYCLE = {
    "candidate analysis": 150,
    "path and input exploration": 116,
    "execution observation": 157,
    "reproduction and validation": 96,
    "patch validation": 46,
    "reporting and audit": 78,
}
CAPABILITY = {
    "context aggregation / rule extraction": 164,
    "tool routing / strategy routing": 150,
    "feedback interpretation / loop adjustment": 186,
    "validation organization / evidence packaging": 147,
    "long-horizon state management": 125,
    "failure reuse / strategy update": 94,
    "governance / human gates / disclosure control": 18,
}
TRACE = {
    "no external trace reported": 19,
    "author-reported external clue": 33,
    "benchmark ground truth / public material": 140,
    "publicly aligned external trace": 7,
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


def jaccard(a: set[str], b: set[str]) -> float:
    return 1.0 if not (a | b) else len(a & b) / len(a | b)


def micro_f1(pairs: list[tuple[set[str], set[str]]]) -> float:
    tp = sum(len(a & b) for a, b in pairs)
    fp = sum(len(a - b) for a, b in pairs)
    fn = sum(len(b - a) for a, b in pairs)
    return 2 * tp / (2 * tp + fp + fn)


def check_manifest() -> None:
    manifest = ROOT / "manuscript_artifact_paths.txt"
    require(manifest.exists(), "missing manuscript_artifact_paths.txt")
    if not manifest.exists():
        return
    paths = [
        line.strip()
        for line in manifest.read_text(encoding="utf-8-sig").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    require(len(paths) == len(set(paths)), "duplicate path in manuscript artifact manifest")
    for relative in paths:
        require((ROOT / relative).is_file(), f"manifest path is missing: {relative}")
    info(f"manifest paths verified: {len(paths)}")


def check_corpus() -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    corpus = read_csv(DATA / "corpus.csv")
    crosswalk = read_csv(DATA / "study_version_crosswalk.csv")
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
    matrix = read_csv(DATA / "current_study_level_coding_matrix_harmonized.csv")
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
    info("study-level coding: 199 target-software studies")
    return target


def check_extended(target: list[dict[str, str]]) -> None:
    rows = read_csv(DATA / "extended_synthesis_audit.csv")
    require(len(rows) == EXPECTED["extended_studies"], "extended synthesis must contain 150 studies")
    require(len({row.get("record_id", "") for row in rows}) == len(rows), "duplicate extended-synthesis record")
    target_records = {row.get("record_id", "") for row in target}
    require(not (target_records & {row.get("record_id", "") for row in rows}), "study-level and extended layers overlap")
    require(all(row.get("extracted_contribution", "").strip() for row in rows), "missing extended-synthesis contribution")
    require(all(row.get("reason_not_study_level_coded", "").strip() for row in rows), "missing extended-synthesis boundary reason")
    require(all(row.get("public_material_basis", "").strip() for row in rows), "missing extended-synthesis source basis")
    require(sum(row.get("record_id") == "CP114" for row in rows) == 1, "AgentFuzz must appear once in extended synthesis")
    metadata_only = [
        row for row in rows
        if "title/abstract metadata" in row.get("reviewer_note", "").casefold()
    ]
    require(len(metadata_only) == 61, "extended-synthesis metadata-supported count must be 61")
    require(len(rows) - len(metadata_only) == 89, "extended-synthesis full-text-supported count must be 89")
    info("extended synthesis: 89 full-text-supported and 61 metadata-supported studies")


def check_search_and_dedup() -> None:
    results = read_csv(DATA / "final_multisource_search_20260730_results.csv")
    screened = read_csv(DATA / "final_multisource_search_20260730_screening_audit.csv")
    completed = read_csv(DATA / "final_multisource_search_20260730_complete_screening.csv")
    require(len(results) == EXPECTED["search_occurrences"], "search export must contain 12,090 source occurrences")
    require(len(screened) == EXPECTED["search_records"], "screening audit must contain 1,642 unique records")
    require(len(completed) == EXPECTED["search_records"], "complete screening audit must contain 1,642 unique records")
    require(len({row.get("discovery_id", "") for row in completed}) == EXPECTED["search_records"], "complete screening audit contains duplicate discovery IDs")
    require(all(row.get("final_analytical_layer", "").strip() for row in completed), "complete screening audit contains an unresolved final layer")
    completed_layers = Counter(row["final_analytical_layer"] for row in completed)
    require(
        completed_layers == Counter({
            "excluded_near_neighbor": 733,
            "background_reference": 575,
            "study_level": 132,
            "existing_study_or_version": 110,
            "extended_synthesis": 84,
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
    exclusion_summary = read_csv(DATA / "final_multisource_exclusion_summary.csv")
    expected_exclusions = {
        "interface_title_abstract_exclusions": 705,
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
    prisma = {row["metric"]: int(row["count"]) for row in read_csv(DATA / "final_multisource_search_20260730_prisma_counts.csv")}
    checks = {
        "exported_source_occurrences": 12090,
        "removed_by_deterministic_query_filter": 9801,
        "source_occurrences_entering_deduplication": 2289,
        "duplicate_source_occurrences_removed": 647,
        "unique_search_records_screened": 1642,
        "records_not_advanced_to_report_retrieval": 1368,
        "reports_sought": 274,
        "reports_not_retrieved": 35,
        "reports_assessed_at_full_text": 239,
        "full_text_study_level": 132,
        "full_text_extended_synthesis": 83,
        "full_text_background_reference": 21,
        "full_text_excluded_near_neighbor": 3,
        "current_search_matches_to_retained_studies": 110,
        "new_or_reconciled_source_records_added": 1532,
        "supplementary_source_records_not_reidentified": 143,
        "prior_canonical_studies_not_reidentified": 138,
        "integrated_source_records": 1785,
        "integrated_canonical_studies": 1772,
        "target_software_studies": 199,
        "extended_synthesis_studies": 150,
        "background_reference_studies": 670,
        "excluded_studies": 753,
    }
    require(all(prisma.get(key) == value for key, value in checks.items()), "PRISMA counts differ from integrated corpus")
    resolutions = read_csv(DATA / "final_multisource_search_20260730_dedup_resolutions.csv")
    require(len(resolutions) == 124, "dedup audit must contain 124 candidate pairs")
    require(not any(row.get("audit_decision") == "needs_author_confirmation" for row in resolutions), "unresolved dedup pair remains")
    require(sum(row.get("audit_decision") == "same_study_or_version" for row in resolutions) == 119, "same-study/version resolution count differs")
    info("search and PRISMA ledger verified through 2026-07-30")


def check_supplementary_extractions(target: list[dict[str, str]]) -> None:
    primitives = read_csv(DATA / "traditional_security_primitives.csv")
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

    refs = read_csv(DATA / "reference_audit.csv")
    require(len(refs) == 402, "reference audit must contain 402 rows")
    new_refs = read_csv(DATA / "final_multisource_new_study_reference_metadata_20260730.csv")
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

    cohort_rows = read_csv(DATA / "final_multisource_cohort_stability.csv")
    require(len(cohort_rows) == 32, "cohort-stability audit must contain 32 rows")
    expected_denominators = {"retained_pre_final_67": 67, "new_multisource_132": 132}
    require(
        {row.get("cohort", "") for row in cohort_rows} == set(expected_denominators),
        "cohort-stability audit has unexpected cohorts",
    )
    pre_final_all = read_csv(DATA / "current_study_level_coding_matrix_harmonized_pre_final_multisource_20260730.csv")
    pre_ids = {
        row.get("matrix_id", "")
        for row in pre_final_all
        if row.get("analytical_role") == "target_software_study"
    }
    pre_final = [row for row in target if row.get("matrix_id", "") in pre_ids]
    require(len(pre_ids) == 67 and len(pre_final) == 67, "pre-final target-study baseline must contain 67 retained target rows")
    new_target = [row for row in target if row.get("matrix_id", "") not in pre_ids]
    require(len(new_target) == 132, "new multi-source target cohort must contain 132 rows")
    cohort_records = {"retained_pre_final_67": pre_final, "new_multisource_132": new_target}
    for cohort, denominator in expected_denominators.items():
        subset = [row for row in cohort_rows if row.get("cohort") == cohort]
        require(all(int(row.get("denominator", "0")) == denominator for row in subset), f"cohort denominator differs: {cohort}")
        require(sum(int(row["count"]) for row in subset if row["dimension"] == "primary_system_shape") == denominator, f"shape count does not close: {cohort}")
        require(sum(int(row["count"]) for row in subset if row["dimension"] == "principal_reported_evidence_output") == denominator, f"evidence count does not close: {cohort}")
        require(len([row for row in subset if row["dimension"] == "cross_stage_capability"]) == 7, f"capability labels differ: {cohort}")
        records = cohort_records[cohort]
        recomputed = {
            ("primary_system_shape", label): count
            for label, count in Counter(row.get("primary_system_shape", "") for row in records).items()
        }
        recomputed.update({
            ("principal_reported_evidence_output", label): count
            for label, count in Counter(row.get("strongest_evidence_output", "") for row in records).items()
        })
        capability_counts = Counter()
        for row in records:
            capability_counts.update(split_labels(row.get("cross_stage_capabilities", "")))
        recomputed.update({("cross_stage_capability", label): count for label, count in capability_counts.items()})
        for row in subset:
            key = (row.get("dimension", ""), row.get("label", ""))
            require(recomputed.get(key) == int(row.get("count", "0")), f"cohort label count differs: {cohort} {key}")
    require(
        all(int(row["count"]) > 0 for row in cohort_rows if row["dimension"] in {"primary_system_shape", "principal_reported_evidence_output"}),
        "a cohort does not populate every shape and evidence category",
    )
    info("supplementary primitive, reference, and cohort-stability extractions verified")


def check_publication_status(target: list[dict[str, str]]) -> None:
    rows = read_csv(DATA / "publication_status_standardized.csv")
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
    distribution = {row["publication_status_standardized"]: row for row in read_csv(DATA / "publication_status_distribution_by_layer.csv")}
    require(set(distribution) == set(PUBLICATION_STATUS), "publication-status distribution categories differ")
    for status, count in PUBLICATION_STATUS.items():
        require(int(distribution[status]["target_software_studies"]) == count, f"publication-status total differs: {status}")
    peer = [row for row in target_rows if row["publication_status_standardized"] in {"conference", "journal"}]
    preprints = [row for row in target_rows if row["publication_status_standardized"] == "preprint"]
    require(len(peer) == 31 and len(preprints) == 164, "publication-status manuscript denominators differ")
    require(sum(row["strongest_evidence_output"] == "reproducible validation" for row in peer) == 13, "peer-reviewed RV count differs")
    require(sum(row["strongest_evidence_output"] == "reproducible validation" for row in preprints) == 69, "preprint RV count differs")
    require(sum(row["strongest_evidence_output"] == "externally traceable material" for row in peer) == 1, "peer-reviewed ET count differs")
    require(sum(row["strongest_evidence_output"] == "externally traceable material" for row in preprints) == 5, "preprint ET count differs")
    info("publication-status assignments and manuscript-facing stratification verified")


def check_second_coder(target: list[dict[str, str]]) -> None:
    new = read_csv(DATA / "final_multisource_search_20260730_all_coder_comparison.csv")
    require(len(new) == 136, "new-search coder comparison must contain 136 reviewed records")
    require(sum(row.get("jointly_included") == "true" for row in new) == 132, "jointly included new studies must equal 132")
    integrated = read_csv(DATA / "integrated_199_second_coder_comparison_20260730.csv")
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
    require(len(read_csv(DATA / "integrated_199_per_label_reliability_20260730.csv")) > 0, "missing per-label reliability")
    require(len(read_csv(DATA / "integrated_199_label_substitution_sensitivity_20260730.csv")) > 0, "missing substitution sensitivity")
    info("complete independent coding comparison verified for 199 target studies")


def check_private_paths() -> None:
    needles = ("C:\\Users\\oldph", "/Users/oldph", "artifact_public_release_candidate/data/")
    for path in [ROOT / "README.md", ROOT / "ARTIFACT_INDEX.md", ROOT / "RELEASE_MANIFEST.md", ROOT / "data_dictionary.md"]:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        for needle in needles:
            require(needle not in text, f"private or stale path in {path.name}: {needle}")


def check_manuscript(path: Path) -> None:
    if not path.is_file():
        error(f"manuscript not found: {path}")
        return
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    for required in ("1,772", "199", "150"):
        require(required in text, f"manuscript does not contain integrated value/date: {required}")
    require(
        "2026-07-30" in text or "July 30, 2026" in text,
        "manuscript does not contain the integrated search cutoff date",
    )
    for match in re.findall(r"\\path\{([^}]+)\}", text):
        if match.startswith("data/") or match.endswith((".md", ".py", ".txt")):
            require((ROOT / match).exists(), f"manuscript artifact path is missing: {match}")
    info(f"manuscript checked: {path}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manuscript", type=Path, help="optional path to main_acm_csur.tex")
    args = parser.parse_args()

    check_manifest()
    _, _ = check_corpus()
    target = check_matrix()
    check_extended(target)
    check_search_and_dedup()
    check_supplementary_extractions(target)
    check_publication_status(target)
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
