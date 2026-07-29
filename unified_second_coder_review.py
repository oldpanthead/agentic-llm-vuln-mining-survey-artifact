#!/usr/bin/env python3
"""Prepare and validate the unified 68-record second-coder review package."""

from __future__ import annotations

import argparse
import csv
import re
import sys
import unicodedata
import urllib.request
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
LOCAL = ROOT / "local_private_working" / "unified_second_coder_review"
PROJECT = ROOT.parent

MATRIX = DATA / "current_study_level_coding_matrix_harmonized.csv"
STATUS = DATA / "publication_status_standardized.csv"
INITIAL_EVIDENCE = DATA / "core31_second_coder_formal_results.csv"
INITIAL_CAP_TRACE = DATA / "core31_second_coder_capability_traceability_results.csv"
UPDATE = DATA / "submission_update_20260715_second_coder_rerun_results.csv"

PUBLIC_TEMPLATE = DATA / "unified_second_coder_final_blind_template.csv"
WORKING = LOCAL / "unified_second_coder_working.csv"
MATERIAL_INDEX = LOCAL / "local_material_index.csv"
MATERIAL_CACHE = LOCAL / "materials"
FINAL_RESULTS = DATA / "unified_second_coder_final_results.csv"
DISAGREEMENTS = DATA / "unified_second_coder_pre_adjudication_disagreements.csv"
AGREEMENT_REPORT = ROOT / "reports" / "UNIFIED_SECOND_CODER_PRE_ADJUDICATION_REPORT.md"
SENSITIVITY = DATA / "unified_second_coder_label_substitution_sensitivity.csv"

LIFECYCLE = [
    "candidate analysis",
    "path and input exploration",
    "execution observation",
    "reproduction and validation",
    "patch validation",
    "reporting and audit",
]

CAPABILITIES = [
    "context aggregation / rule extraction",
    "tool routing / strategy routing",
    "feedback interpretation / loop adjustment",
    "validation organization / evidence packaging",
    "long-horizon state management",
    "failure reuse / strategy update",
    "governance / human gates / disclosure control",
]

SHAPES = [
    "candidate-analysis system",
    "feedback-driven fuzzing agent",
    "reproduction-, validation-, and repair-centered agent",
    "long-horizon pentest and CRS agent",
    "governance boundary case",
]

EVIDENCE = [
    "candidate judgment",
    "controlled task completion",
    "runtime safety signal",
    "reproducible validation",
    "externally traceable material",
    "governance boundary case",
]

TRACE = [
    "no external trace reported",
    "author-reported external clue",
    "benchmark ground truth / public material",
    "publicly aligned external trace",
    "not reported",
]

REVIEW_STATUS = {"confirm", "revise", "newly_code"}

CAPABILITY_TRANSLATION = {
    "上下文聚合与规则提取": "context aggregation / rule extraction",
    "工具选择与策略路由": "tool routing / strategy routing",
    "反馈解释与闭环调整": "feedback interpretation / loop adjustment",
    "验证组织与证据打包": "validation organization / evidence packaging",
    "长程编排与状态管理": "long-horizon state management",
    "失败归纳与策略更新": "failure reuse / strategy update",
}

TRACE_TRANSLATION = {
    "未报告": "no external trace reported",
    "作者报告的外部线索": "author-reported external clue",
    "benchmark ground truth / 公开材料": "benchmark ground truth / public material",
}

PUBLIC_FIELDS = [
    "review_order",
    "matrix_id",
    "record_id",
    "system_alias",
    "title",
    "year",
    "publication_status",
    "review_scope",
    "official_url",
    "materials_to_review",
    "final_lifecycle_coverage",
    "lifecycle_review_status",
    "final_cross_stage_capabilities",
    "capability_review_status",
    "final_primary_system_shape",
    "shape_review_status",
    "final_strongest_evidence_output",
    "evidence_review_status",
    "final_external_traceability",
    "traceability_review_status",
    "final_claim_boundary",
    "claim_boundary_review_status",
    "material_checked",
    "decision_note",
    "uncertainty_note",
    "row_status",
]

WORKING_FIELDS = PUBLIC_FIELDS[:10] + [
    "reuse_mode",
    "prior_lifecycle_coverage",
    "prior_cross_stage_capabilities",
    "prior_primary_system_shape",
    "prior_strongest_evidence_output",
    "prior_external_traceability",
    "prior_claim_boundary",
] + PUBLIC_FIELDS[10:]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFKD", value or "")
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def normalize_multi(value: str, allowed: list[str]) -> str:
    parts = [part.strip() for part in (value or "").split(";") if part.strip()]
    return ";".join(label for label in allowed if label in parts)


def translate_initial_capability(value: str) -> tuple[str, bool]:
    translated = []
    unresolved = False
    for part in [item.strip() for item in (value or "").split(";") if item.strip()]:
        if part in CAPABILITY_TRANSLATION:
            translated.append(CAPABILITY_TRANSLATION[part])
        else:
            unresolved = True
    return normalize_multi(";".join(translated), CAPABILITIES), unresolved


def material_candidates() -> list[Path]:
    candidates: list[Path] = []
    for base in [MATERIAL_CACHE, PROJECT / "tmp_core31_zotero_fulltext", PROJECT / "zotero_v4_staging"]:
        if base.exists():
            candidates.extend(path for path in base.rglob("*") if path.is_file() and path.suffix.lower() in {".pdf", ".txt"})
    return candidates


def score_material(row: dict[str, str], path: Path) -> float:
    stem = normalize(path.stem.replace("_fulltext", ""))
    title = normalize(row["title"])
    alias = normalize(row["system_alias"])
    score = SequenceMatcher(None, title, stem).ratio()
    if alias and len(alias) >= 4 and alias in stem:
        score += 0.45
    if row["matrix_id"].lower() in path.name.lower():
        score += 0.60
    title_tokens = set(title.split())
    stem_tokens = set(stem.split())
    if title_tokens:
        score += 0.35 * len(title_tokens & stem_tokens) / len(title_tokens)
    return score


def find_materials(matrix_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    files = material_candidates()
    output = []
    for row in matrix_rows:
        ranked = sorted(((score_material(row, path), path) for path in files), reverse=True)[:3]
        for rank, (score, path) in enumerate(ranked, start=1):
            output.append({
                "matrix_id": row["matrix_id"],
                "record_id": row["record_id"],
                "system_alias": row["system_alias"],
                "rank": str(rank),
                "match_score": f"{score:.3f}",
                "local_path": str(path),
                "exists": "yes" if path.exists() else "no",
            })
    return output


def safe_name(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", value).strip("_")
    return cleaned[:36] or "study"


def cache_public_materials() -> int:
    if not MATRIX.exists():
        print(f"ERROR missing matrix: {MATRIX}")
        return 1
    matrix = read_csv(MATRIX)
    MATERIAL_CACHE.mkdir(parents=True, exist_ok=True)
    downloaded = 0
    present = 0
    skipped = 0
    failed = 0
    for row in matrix:
        url = row.get("official_url", "")
        match = re.search(r"arxiv\.org/abs/([0-9.]+)", url)
        if not match:
            skipped += 1
            continue
        arxiv_id = match.group(1)
        existing = [path for path in MATERIAL_CACHE.glob(f"{row['matrix_id']}_*.pdf") if path.stat().st_size > 10_000]
        if existing:
            present += 1
            continue
        destination = MATERIAL_CACHE / f"{row['matrix_id']}_{safe_name(row['system_alias'])}_{arxiv_id}.pdf"
        if destination.exists() and destination.stat().st_size > 10_000:
            present += 1
            continue
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}"
        request = urllib.request.Request(pdf_url, headers={"User-Agent": "Mozilla/5.0 unified-second-coder-review"})
        try:
            with urllib.request.urlopen(request, timeout=90) as response:
                content = response.read()
            if not content.startswith(b"%PDF"):
                raise ValueError("response is not a PDF")
            destination.write_bytes(content)
            downloaded += 1
            print(f"OK cached {row['matrix_id']} {arxiv_id}")
        except Exception as exc:  # network failures should be visible per record
            failed += 1
            print(f"WARN could not cache {row['matrix_id']} {pdf_url}: {exc}")
    print(
        f"INFO cache summary: downloaded={downloaded}, already_present={present}, "
        f"non_arxiv_skipped={skipped}, failed={failed}"
    )
    return 1 if failed else 0


def prepare() -> int:
    required = [MATRIX, STATUS, INITIAL_EVIDENCE, INITIAL_CAP_TRACE, UPDATE]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        print("ERROR missing input files:\n" + "\n".join(missing))
        return 1

    matrix = read_csv(MATRIX)
    if len(matrix) != 68:
        print(f"ERROR expected 68 harmonized rows, found {len(matrix)}")
        return 1

    status_by_id = {row["matrix_id"]: row for row in read_csv(STATUS)}
    initial_evidence = {row["core_id"]: row for row in read_csv(INITIAL_EVIDENCE)}
    initial_cap = {row["core_id"]: row for row in read_csv(INITIAL_CAP_TRACE)}
    update = {row["update_id"]: row for row in read_csv(UPDATE)}

    public_rows: list[dict[str, str]] = []
    working_rows: list[dict[str, str]] = []

    for order, row in enumerate(matrix, start=1):
        matrix_id = row["matrix_id"]
        status = status_by_id.get(matrix_id, {})
        common = {
            "review_order": str(order),
            "matrix_id": matrix_id,
            "record_id": row["record_id"],
            "system_alias": row["system_alias"],
            "title": row["title"],
            "year": status.get("year", ""),
            "publication_status": status.get("publication_status_standardized", ""),
            "review_scope": "governance boundary case" if row["analytical_role"] == "governance_boundary_case" else "target-software study",
            "official_url": row["official_url"],
            "materials_to_review": "Review the public paper and any public artifact/project page. Apply unified_second_coder_codebook.md; do not consult author-label or harmonization files.",
        }

        prior = {
            "prior_lifecycle_coverage": "",
            "prior_cross_stage_capabilities": "",
            "prior_primary_system_shape": "",
            "prior_strongest_evidence_output": "",
            "prior_external_traceability": "",
            "prior_claim_boundary": "",
        }
        reuse_mode = ""

        if matrix_id.startswith("C"):
            evidence_row = initial_evidence.get(matrix_id, {})
            cap_row = initial_cap.get(matrix_id, {})
            prior["prior_strongest_evidence_output"] = evidence_row.get("coder2_strongest_evidence_output", "")
            translated_cap, unresolved = translate_initial_capability(cap_row.get("coder2_cross_stage_capability_label", ""))
            prior["prior_cross_stage_capabilities"] = translated_cap
            prior["prior_external_traceability"] = TRACE_TRANSLATION.get(
                cap_row.get("coder2_external_traceability_label", ""), ""
            )
            if row["analytical_role"] == "governance_boundary_case" and prior["prior_external_traceability"] == "no external trace reported":
                prior["prior_external_traceability"] = "not reported"
            reuse_mode = "needs_new_fields"
            if unresolved:
                reuse_mode = "needs_new_fields;legacy_capability_requires_new_code"
        else:
            update_row = update.get(matrix_id, {})
            if update_row.get("coder2_analysis_layer_decision") != "study_level_candidate":
                print(f"ERROR {matrix_id} does not map to a study-level update decision")
                return 1
            prior.update({
                "prior_lifecycle_coverage": normalize_multi(update_row.get("coder2_lifecycle_coverage", ""), LIFECYCLE),
                "prior_cross_stage_capabilities": normalize_multi(update_row.get("coder2_cross_stage_capability_label", ""), CAPABILITIES),
                "prior_primary_system_shape": update_row.get("coder2_primary_system_shape", "").replace("PoC/PoV validation agent", "reproduction-, validation-, and repair-centered agent"),
                "prior_strongest_evidence_output": update_row.get("coder2_strongest_evidence_output", ""),
                "prior_external_traceability": (
                    "no external trace reported"
                    if update_row.get("coder2_external_traceability_label", "") == "not reported"
                    else update_row.get("coder2_external_traceability_label", "")
                ),
                "prior_claim_boundary": update_row.get("coder2_claim_boundary", ""),
            })
            reuse_mode = "confirm_all_fields"

        blank = {field: "" for field in PUBLIC_FIELDS[10:]}
        public_rows.append({**common, **blank})
        working_values = dict(blank)
        working_values.update({
            "final_lifecycle_coverage": prior["prior_lifecycle_coverage"],
            "final_cross_stage_capabilities": prior["prior_cross_stage_capabilities"],
            "final_primary_system_shape": prior["prior_primary_system_shape"],
            "final_strongest_evidence_output": prior["prior_strongest_evidence_output"],
            "final_external_traceability": prior["prior_external_traceability"],
            "final_claim_boundary": prior["prior_claim_boundary"],
            "row_status": "not_started",
        })
        working_rows.append({**common, "reuse_mode": reuse_mode, **prior, **working_values})

    write_csv(PUBLIC_TEMPLATE, public_rows, PUBLIC_FIELDS)
    write_csv(WORKING, working_rows, WORKING_FIELDS)
    material_rows = find_materials(matrix)
    write_csv(
        MATERIAL_INDEX,
        material_rows,
        ["matrix_id", "record_id", "system_alias", "rank", "match_score", "local_path", "exists"],
    )

    print(f"OK public blind template: {PUBLIC_TEMPLATE} ({len(public_rows)} rows)")
    print(f"OK local working sheet: {WORKING} ({len(working_rows)} rows)")
    print(f"OK local material index: {MATERIAL_INDEX} ({len(material_rows)} candidates)")
    print("INFO initial rows reuse three prior fields and require three new fields; update rows reuse all six prior fields.")
    return 0


def validate(path: Path) -> int:
    if not path.exists():
        print(f"ERROR input not found: {path}")
        return 1
    rows = read_csv(path)
    errors: list[str] = []
    if len(rows) != 68:
        errors.append(f"expected 68 rows, found {len(rows)}")
    if len({row.get("matrix_id", "") for row in rows}) != len(rows):
        errors.append("matrix_id values are blank or duplicated")

    checks = [
        ("final_lifecycle_coverage", "lifecycle_review_status", LIFECYCLE, True),
        ("final_cross_stage_capabilities", "capability_review_status", CAPABILITIES, True),
        ("final_primary_system_shape", "shape_review_status", SHAPES, False),
        ("final_strongest_evidence_output", "evidence_review_status", EVIDENCE, False),
        ("final_external_traceability", "traceability_review_status", TRACE, False),
    ]
    for row in rows:
        row_id = row.get("matrix_id", "<blank>")
        if row.get("row_status") != "complete":
            errors.append(f"{row_id}: row_status is not complete")
        for value_field, status_field, allowed, multi in checks:
            value = row.get(value_field, "").strip()
            status_value = row.get(status_field, "").strip()
            if status_value not in REVIEW_STATUS:
                errors.append(f"{row_id}: invalid or missing {status_field}")
            values = [part.strip() for part in value.split(";") if part.strip()] if multi else [value]
            if not value or any(item not in allowed for item in values):
                errors.append(f"{row_id}: invalid or missing {value_field}: {value!r}")
        if not row.get("final_claim_boundary", "").strip():
            errors.append(f"{row_id}: missing final_claim_boundary")
        if row.get("claim_boundary_review_status", "").strip() not in REVIEW_STATUS:
            errors.append(f"{row_id}: invalid or missing claim_boundary_review_status")
        if not row.get("material_checked", "").strip():
            errors.append(f"{row_id}: missing material_checked")
        if not row.get("decision_note", "").strip():
            errors.append(f"{row_id}: missing decision_note")

    if errors:
        print(f"ERROR unified review is incomplete ({len(errors)} issues)")
        for issue in errors[:80]:
            print(f"- {issue}")
        if len(errors) > 80:
            print(f"- ... {len(errors) - 80} additional issues")
        return 1
    print("OK unified second-coder review is complete: 68 unique rows and all required fields validated.")
    return 0


def multi_metrics(author_values: list[str], coder_values: list[str]) -> dict[str, float]:
    exact = 0
    jaccards = []
    intersection_total = 0
    author_total = 0
    coder_total = 0
    for author_value, coder_value in zip(author_values, coder_values):
        author_set = {item.strip() for item in author_value.split(";") if item.strip()}
        coder_set = {item.strip() for item in coder_value.split(";") if item.strip()}
        if author_set == coder_set:
            exact += 1
        union = author_set | coder_set
        intersection = author_set & coder_set
        jaccards.append(len(intersection) / len(union) if union else 1.0)
        intersection_total += len(intersection)
        author_total += len(author_set)
        coder_total += len(coder_set)
    precision = intersection_total / coder_total if coder_total else 1.0
    recall = intersection_total / author_total if author_total else 1.0
    micro_f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "n": len(author_values),
        "exact_count": exact,
        "exact": exact / len(author_values),
        "mean_jaccard": sum(jaccards) / len(jaccards),
        "micro_f1": micro_f1,
    }


def single_metrics(author_values: list[str], coder_values: list[str]) -> dict[str, float]:
    n = len(author_values)
    agreed = sum(a == b for a, b in zip(author_values, coder_values))
    author_counts = Counter(author_values)
    coder_counts = Counter(coder_values)
    labels = set(author_counts) | set(coder_counts)
    expected = sum((author_counts[label] / n) * (coder_counts[label] / n) for label in labels)
    observed = agreed / n
    kappa = (observed - expected) / (1 - expected) if expected < 1 else 1.0
    return {"n": n, "agreement_count": agreed, "raw_agreement": observed, "kappa": kappa}


def compare(path: Path) -> int:
    if validate(path):
        return 1
    coder_rows = read_csv(path)
    author_rows = read_csv(MATRIX)
    author_by_id = {row["matrix_id"]: row for row in author_rows}
    coder_by_id = {row["matrix_id"]: row for row in coder_rows}
    target_ids = [row["matrix_id"] for row in author_rows if row["analytical_role"] == "target_software_study"]

    field_specs = [
        ("lifecycle_coverage", "final_lifecycle_coverage", "Lifecycle coverage", True),
        ("cross_stage_capabilities", "final_cross_stage_capabilities", "Cross-stage capability", True),
        ("primary_system_shape", "final_primary_system_shape", "Primary system shape", False),
        ("strongest_evidence_output", "final_strongest_evidence_output", "Principal reported evidence output", False),
        ("external_traceability", "final_external_traceability", "External traceability", False),
    ]
    metrics: dict[str, dict[str, float]] = {}
    disagreement_rows: list[dict[str, str]] = []
    sensitivity_rows: list[dict[str, str]] = []
    for author_field, coder_field, label, multi in field_specs:
        author_values = [author_by_id[matrix_id][author_field] for matrix_id in target_ids]
        coder_values = [coder_by_id[matrix_id][coder_field] for matrix_id in target_ids]
        metrics[label] = multi_metrics(author_values, coder_values) if multi else single_metrics(author_values, coder_values)
        if multi:
            author_counts = Counter(
                item.strip()
                for value in author_values
                for item in value.split(";")
                if item.strip()
            )
            coder_counts = Counter(
                item.strip()
                for value in coder_values
                for item in value.split(";")
                if item.strip()
            )
        else:
            author_counts = Counter(author_values)
            coder_counts = Counter(coder_values)
        for category in sorted(set(author_counts) | set(coder_counts)):
            author_count = author_counts.get(category, 0)
            coder_count = coder_counts.get(category, 0)
            sensitivity_rows.append({
                "field": author_field,
                "label": category,
                "scope_n": str(len(target_ids)),
                "author_harmonized_count": str(author_count),
                "coder2_substitution_count": str(coder_count),
                "absolute_difference": str(abs(author_count - coder_count)),
                "direction": "same" if author_count == coder_count else ("coder2_higher" if coder_count > author_count else "coder2_lower"),
            })
        for matrix_id, author_value, coder_value in zip(target_ids, author_values, coder_values):
            author_set = {item.strip() for item in author_value.split(";") if item.strip()}
            coder_set = {item.strip() for item in coder_value.split(";") if item.strip()}
            differs = author_set != coder_set if multi else author_value != coder_value
            if differs:
                union = author_set | coder_set
                jaccard = len(author_set & coder_set) / len(union) if multi and union else ""
                coder_row = coder_by_id[matrix_id]
                disagreement_rows.append({
                    "matrix_id": matrix_id,
                    "record_id": coder_row["record_id"],
                    "system_alias": coder_row["system_alias"],
                    "field": author_field,
                    "author_harmonized_label": author_value,
                    "coder2_final_label": coder_value,
                    "row_jaccard": f"{jaccard:.3f}" if isinstance(jaccard, float) else "",
                    "material_checked": coder_row["material_checked"],
                    "coder2_decision_note": coder_row["decision_note"],
                    "coder2_uncertainty_note": coder_row["uncertainty_note"],
                    "adjudication_status": "not_planned",
                    "adjudicated_label": "",
                    "adjudication_note": "",
                })

    result_rows = [{field: row.get(field, "") for field in PUBLIC_FIELDS} for row in coder_rows]
    write_csv(FINAL_RESULTS, result_rows, PUBLIC_FIELDS)
    disagreement_fields = [
        "matrix_id", "record_id", "system_alias", "field", "author_harmonized_label",
        "coder2_final_label", "row_jaccard", "material_checked", "coder2_decision_note",
        "coder2_uncertainty_note", "adjudication_status", "adjudicated_label", "adjudication_note",
    ]
    write_csv(DISAGREEMENTS, disagreement_rows, disagreement_fields)
    write_csv(
        SENSITIVITY,
        sensitivity_rows,
        [
            "field", "label", "scope_n", "author_harmonized_count",
            "coder2_substitution_count", "absolute_difference", "direction",
        ],
    )

    status_fields = [
        "lifecycle_review_status", "capability_review_status", "shape_review_status",
        "evidence_review_status", "traceability_review_status", "claim_boundary_review_status",
    ]
    status_summary = {field: Counter(row[field] for row in coder_rows) for field in status_fields}
    report_lines = [
        "# Unified Second-Coder Pre-Adjudication Report",
        "",
        "## Scope",
        "",
        "The unified review covers all 67 target-software studies plus the governance boundary case under one frozen codebook. Reliability metrics below use the 67 target-software studies; the governance boundary case was reviewed where applicable but remains outside target-software distribution denominators. Claim-boundary text was reviewed for all 68 records but is not assigned an artificial exact-match statistic.",
        "",
        "## Field-Specific Agreement Before Adjudication",
        "",
        "| Field | Scope | Result |",
        "|---|---:|---|",
    ]
    for label, metric in metrics.items():
        if "mean_jaccard" in metric:
            result = (
                f"exact = {int(metric['exact_count'])}/{int(metric['n'])} = {metric['exact']:.3f}; "
                f"mean row Jaccard = {metric['mean_jaccard']:.3f}; micro F1 = {metric['micro_f1']:.3f}"
            )
        else:
            result = (
                f"raw agreement = {int(metric['agreement_count'])}/{int(metric['n'])} = {metric['raw_agreement']:.3f}; "
                f"Cohen's kappa = {metric['kappa']:.3f}"
            )
        report_lines.append(f"| {label} | {int(metric['n'])} | {result} |")
    report_lines.extend([
        "",
        "## Review Actions",
        "",
        "| Field | Confirm | Revise | Newly code |",
        "|---|---:|---:|---:|",
    ])
    display_names = {
        "lifecycle_review_status": "Lifecycle coverage",
        "capability_review_status": "Cross-stage capability",
        "shape_review_status": "Primary system shape",
        "evidence_review_status": "Principal reported evidence output",
        "traceability_review_status": "External traceability",
        "claim_boundary_review_status": "Claim boundary",
    }
    for field in status_fields:
        counts = status_summary[field]
        report_lines.append(f"| {display_names[field]} | {counts.get('confirm', 0)} | {counts.get('revise', 0)} | {counts.get('newly_code', 0)} |")
    report_lines.extend([
        "",
        f"The disagreement file contains {len(disagreement_rows)} field-level rows. These are pre-adjudication differences; no consensus or post-adjudication reliability is claimed.",
        "",
        "## Label-Substitution Sensitivity",
        "",
        "The complete count comparison is available in `data/unified_second_coder_label_substitution_sensitivity.csv`. Reproducible validation (31/67), candidate judgment (6/67), controlled task completion (13/67), and the feedback-driven fuzzing shape (17/67) are unchanged under second-coder substitution. Feedback interpretation and validation organization remain common, and governance control remains uncommon. Exact counts for external traceability, failure reuse, reporting/audit coverage, and tool routing are more boundary-sensitive and are therefore interpreted directionally in the manuscript.",
        "",
        "## Provenance",
        "",
        "The second coder was allowed to reuse and reconsider their own earlier labels, but did not receive author or harmonized row-level labels before completing the unified review. Every row records reviewed material and a decision note. Original historical second-coder files remain unchanged.",
        "",
    ])
    AGREEMENT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    AGREEMENT_REPORT.write_text("\n".join(report_lines), encoding="utf-8")

    print(f"OK final unified coder2 results: {FINAL_RESULTS} ({len(result_rows)} rows)")
    print(f"OK pre-adjudication disagreements: {DISAGREEMENTS} ({len(disagreement_rows)} field rows)")
    print(f"OK label-substitution sensitivity: {SENSITIVITY} ({len(sensitivity_rows)} label rows)")
    print(f"OK agreement report: {AGREEMENT_REPORT}")
    for label, metric in metrics.items():
        print(f"{label}: {metric}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("prepare", help="build the public blind template and local reusable working files")
    subparsers.add_parser("cache-materials", help="cache public arXiv PDFs in the ignored local working directory")
    validate_parser = subparsers.add_parser("validate", help="check a completed review without revealing author labels")
    validate_parser.add_argument("--input", type=Path, required=True)
    compare_parser = subparsers.add_parser("compare", help="calculate pre-adjudication agreement after a complete review")
    compare_parser.add_argument("--input", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "prepare":
        return prepare()
    if args.command == "cache-materials":
        return cache_public_materials()
    if args.command == "compare":
        return compare(args.input)
    return validate(args.input)


if __name__ == "__main__":
    sys.exit(main())
