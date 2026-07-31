#!/usr/bin/env python3
"""Prepare the 2026-07-15 submission-update adjudication working draft.

The script preserves the author audit and independent coder2 results, computes
pre-adjudication agreement, and writes an evidence-based proposed resolution.
The proposed labels remain pending author confirmation; no human consensus or
completed adjudication is claimed.
"""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
REPORTS = ROOT / "reports"

AUTHOR_PATH = DATA / "submission_update_20260715_full_coding_audit.csv"
CODER2_PATH = DATA / "submission_update_20260715_second_coder_results.csv"
OUTPUT_PATH = DATA / "submission_update_20260715_adjudication_working_draft.csv"
REPORT_PATH = REPORTS / "SUBMISSION_UPDATE_SECOND_CODER_PRE_ADJUDICATION_REPORT.md"
SUMMARY_PATH = ROOT / "SUBMISSION_UPDATE_ADJUDICATION_SUMMARY.md"

LIFECYCLE_ORDER = [
    "candidate analysis",
    "path and input exploration",
    "execution observation",
    "reproduction and validation",
    "patch validation",
    "reporting and audit",
]

CAPABILITY_ORDER = [
    "context aggregation / rule extraction",
    "tool routing / strategy routing",
    "feedback interpretation / loop adjustment",
    "validation organization / evidence packaging",
    "long-horizon state management",
    "failure reuse / strategy update",
    "governance / human gates / disclosure control",
]


def joined(*labels: str) -> str:
    return ";".join(labels)


PROPOSED_LAYER = {f"U{i:02d}": "study_level_candidate" for i in range(1, 42)}
for update_id in ("U19", "U20", "U24", "U30"):
    PROPOSED_LAYER[update_id] = "extended_synthesis"

PROPOSED_LIFECYCLE = {
    "U01": joined("candidate analysis", "patch validation"),
    "U02": joined("candidate analysis", "path and input exploration", "execution observation", "reproduction and validation", "reporting and audit"),
    "U03": joined("candidate analysis", "path and input exploration", "execution observation", "reproduction and validation"),
    "U04": joined("candidate analysis", "path and input exploration", "execution observation", "reproduction and validation", "reporting and audit"),
    "U05": joined("candidate analysis", "reporting and audit"),
    "U06": joined("candidate analysis", "path and input exploration", "execution observation", "reproduction and validation"),
    "U07": joined("candidate analysis", "path and input exploration", "execution observation", "reproduction and validation", "reporting and audit"),
    "U08": joined("candidate analysis", "execution observation", "patch validation"),
    "U09": joined("path and input exploration", "execution observation", "reporting and audit"),
    "U10": joined("candidate analysis", "path and input exploration", "execution observation", "patch validation"),
    "U11": joined("candidate analysis", "execution observation", "patch validation"),
    "U12": joined("candidate analysis", "path and input exploration", "execution observation", "reproduction and validation", "reporting and audit"),
    "U13": joined("candidate analysis", "path and input exploration", "execution observation", "reporting and audit"),
    "U14": joined("candidate analysis", "path and input exploration", "execution observation", "reproduction and validation", "reporting and audit"),
    "U15": joined("candidate analysis", "path and input exploration", "execution observation", "patch validation"),
    "U16": joined("candidate analysis", "path and input exploration", "execution observation", "reproduction and validation", "reporting and audit"),
    "U17": joined("path and input exploration", "execution observation", "reproduction and validation", "reporting and audit"),
    "U18": joined("candidate analysis", "path and input exploration", "execution observation", "reproduction and validation", "patch validation", "reporting and audit"),
    "U19": joined("candidate analysis"),
    "U20": joined("candidate analysis", "reporting and audit"),
    "U21": joined("candidate analysis", "path and input exploration", "execution observation"),
    "U22": joined("candidate analysis", "path and input exploration", "execution observation", "reproduction and validation"),
    "U23": joined("candidate analysis", "path and input exploration", "execution observation", "reproduction and validation"),
    "U24": joined("patch validation"),
    "U25": joined("candidate analysis", "path and input exploration", "execution observation", "reproduction and validation"),
    "U26": joined("candidate analysis", "execution observation"),
    "U27": joined("candidate analysis", "reporting and audit"),
    "U28": joined("candidate analysis", "path and input exploration", "execution observation", "reproduction and validation"),
    "U29": joined("candidate analysis", "path and input exploration", "execution observation", "reproduction and validation"),
    "U30": joined("reporting and audit"),
    "U31": joined("path and input exploration", "execution observation"),
    "U32": joined("candidate analysis", "path and input exploration", "execution observation", "reproduction and validation"),
    "U33": joined("candidate analysis", "execution observation", "reproduction and validation", "reporting and audit"),
    "U34": joined("path and input exploration", "execution observation"),
    "U35": joined("candidate analysis", "reporting and audit"),
    "U36": joined("path and input exploration", "execution observation", "reproduction and validation"),
    "U37": joined("candidate analysis", "path and input exploration", "reproduction and validation", "reporting and audit"),
    "U38": joined("candidate analysis", "path and input exploration", "execution observation", "reproduction and validation"),
    "U39": joined("candidate analysis", "patch validation", "reporting and audit"),
    "U40": joined("candidate analysis", "execution observation", "reproduction and validation", "patch validation"),
    "U41": joined("candidate analysis", "reporting and audit"),
}

PROPOSED_CAPABILITIES = {
    "U01": joined("context aggregation / rule extraction", "tool routing / strategy routing", "feedback interpretation / loop adjustment", "validation organization / evidence packaging"),
    "U02": joined("context aggregation / rule extraction", "tool routing / strategy routing", "feedback interpretation / loop adjustment", "validation organization / evidence packaging"),
    "U03": joined("context aggregation / rule extraction", "tool routing / strategy routing", "feedback interpretation / loop adjustment", "validation organization / evidence packaging"),
    "U04": joined("context aggregation / rule extraction", "feedback interpretation / loop adjustment", "validation organization / evidence packaging", "failure reuse / strategy update"),
    "U05": joined("tool routing / strategy routing", "feedback interpretation / loop adjustment", "validation organization / evidence packaging", "long-horizon state management", "failure reuse / strategy update"),
    "U06": joined("context aggregation / rule extraction", "tool routing / strategy routing", "feedback interpretation / loop adjustment", "validation organization / evidence packaging", "long-horizon state management"),
    "U07": joined("context aggregation / rule extraction", "feedback interpretation / loop adjustment", "validation organization / evidence packaging"),
    "U08": joined("context aggregation / rule extraction", "feedback interpretation / loop adjustment", "validation organization / evidence packaging", "long-horizon state management", "failure reuse / strategy update"),
    "U09": joined("context aggregation / rule extraction", "tool routing / strategy routing", "feedback interpretation / loop adjustment", "validation organization / evidence packaging"),
    "U10": joined("context aggregation / rule extraction", "feedback interpretation / loop adjustment", "validation organization / evidence packaging", "failure reuse / strategy update"),
    "U11": joined("context aggregation / rule extraction", "feedback interpretation / loop adjustment", "validation organization / evidence packaging", "long-horizon state management", "failure reuse / strategy update"),
    "U12": joined("context aggregation / rule extraction", "tool routing / strategy routing", "feedback interpretation / loop adjustment", "validation organization / evidence packaging"),
    "U13": joined("context aggregation / rule extraction", "tool routing / strategy routing", "feedback interpretation / loop adjustment", "validation organization / evidence packaging", "long-horizon state management", "governance / human gates / disclosure control"),
    "U14": joined("context aggregation / rule extraction", "tool routing / strategy routing", "feedback interpretation / loop adjustment", "validation organization / evidence packaging", "failure reuse / strategy update", "governance / human gates / disclosure control"),
    "U15": joined("context aggregation / rule extraction", "tool routing / strategy routing", "feedback interpretation / loop adjustment", "validation organization / evidence packaging"),
    "U16": joined("context aggregation / rule extraction", "tool routing / strategy routing", "feedback interpretation / loop adjustment", "validation organization / evidence packaging"),
    "U17": joined("tool routing / strategy routing", "feedback interpretation / loop adjustment", "validation organization / evidence packaging", "long-horizon state management", "failure reuse / strategy update"),
    "U18": joined("tool routing / strategy routing", "feedback interpretation / loop adjustment", "validation organization / evidence packaging", "long-horizon state management", "governance / human gates / disclosure control"),
    "U19": joined("context aggregation / rule extraction", "validation organization / evidence packaging"),
    "U20": joined("context aggregation / rule extraction", "validation organization / evidence packaging"),
    "U21": joined("context aggregation / rule extraction", "tool routing / strategy routing", "validation organization / evidence packaging"),
    "U22": joined("tool routing / strategy routing", "feedback interpretation / loop adjustment", "validation organization / evidence packaging", "long-horizon state management", "governance / human gates / disclosure control"),
    "U23": joined("tool routing / strategy routing", "feedback interpretation / loop adjustment", "validation organization / evidence packaging", "long-horizon state management"),
    "U24": joined("validation organization / evidence packaging"),
    "U25": joined("context aggregation / rule extraction", "feedback interpretation / loop adjustment", "validation organization / evidence packaging", "failure reuse / strategy update"),
    "U26": joined("context aggregation / rule extraction", "feedback interpretation / loop adjustment", "validation organization / evidence packaging"),
    "U27": joined("context aggregation / rule extraction", "tool routing / strategy routing", "validation organization / evidence packaging"),
    "U28": joined("context aggregation / rule extraction", "tool routing / strategy routing", "feedback interpretation / loop adjustment", "validation organization / evidence packaging", "long-horizon state management", "failure reuse / strategy update"),
    "U29": joined("context aggregation / rule extraction", "feedback interpretation / loop adjustment", "validation organization / evidence packaging"),
    "U30": joined("context aggregation / rule extraction", "feedback interpretation / loop adjustment", "validation organization / evidence packaging", "governance / human gates / disclosure control"),
    "U31": joined("context aggregation / rule extraction", "feedback interpretation / loop adjustment"),
    "U32": joined("tool routing / strategy routing", "feedback interpretation / loop adjustment", "validation organization / evidence packaging", "long-horizon state management"),
    "U33": joined("context aggregation / rule extraction", "tool routing / strategy routing", "feedback interpretation / loop adjustment", "validation organization / evidence packaging"),
    "U34": joined("context aggregation / rule extraction", "tool routing / strategy routing", "feedback interpretation / loop adjustment"),
    "U35": joined("context aggregation / rule extraction", "tool routing / strategy routing", "feedback interpretation / loop adjustment", "validation organization / evidence packaging", "long-horizon state management", "failure reuse / strategy update"),
    "U36": joined("context aggregation / rule extraction", "feedback interpretation / loop adjustment", "validation organization / evidence packaging", "long-horizon state management"),
    "U37": joined("context aggregation / rule extraction", "tool routing / strategy routing", "feedback interpretation / loop adjustment", "validation organization / evidence packaging"),
    "U38": joined("context aggregation / rule extraction", "tool routing / strategy routing", "feedback interpretation / loop adjustment", "validation organization / evidence packaging", "long-horizon state management", "failure reuse / strategy update"),
    "U39": joined("context aggregation / rule extraction", "tool routing / strategy routing", "feedback interpretation / loop adjustment", "validation organization / evidence packaging"),
    "U40": joined("context aggregation / rule extraction", "tool routing / strategy routing", "feedback interpretation / loop adjustment", "validation organization / evidence packaging"),
    "U41": joined("context aggregation / rule extraction", "tool routing / strategy routing", "feedback interpretation / loop adjustment", "validation organization / evidence packaging"),
}

PROPOSED_SHAPE = {
    "U01": "candidate-analysis system", "U02": "PoC/PoV validation agent",
    "U03": "PoC/PoV validation agent", "U04": "feedback-driven fuzzing agent",
    "U05": "long-horizon pentest and CRS agent", "U06": "PoC/PoV validation agent",
    "U07": "candidate-analysis system", "U08": "PoC/PoV validation agent",
    "U09": "feedback-driven fuzzing agent", "U10": "PoC/PoV validation agent",
    "U11": "PoC/PoV validation agent", "U12": "candidate-analysis system",
    "U13": "feedback-driven fuzzing agent", "U14": "feedback-driven fuzzing agent",
    "U15": "PoC/PoV validation agent", "U16": "PoC/PoV validation agent",
    "U17": "feedback-driven fuzzing agent", "U18": "long-horizon pentest and CRS agent",
    "U19": "candidate-analysis system", "U20": "candidate-analysis system",
    "U21": "candidate-analysis system", "U22": "long-horizon pentest and CRS agent",
    "U23": "long-horizon pentest and CRS agent", "U24": "candidate-analysis system",
    "U25": "PoC/PoV validation agent", "U26": "candidate-analysis system",
    "U27": "candidate-analysis system", "U28": "PoC/PoV validation agent",
    "U29": "candidate-analysis system", "U30": "candidate-analysis system",
    "U31": "feedback-driven fuzzing agent", "U32": "long-horizon pentest and CRS agent",
    "U33": "candidate-analysis system", "U34": "feedback-driven fuzzing agent",
    "U35": "candidate-analysis system", "U36": "feedback-driven fuzzing agent",
    "U37": "candidate-analysis system", "U38": "PoC/PoV validation agent",
    "U39": "candidate-analysis system", "U40": "PoC/PoV validation agent",
    "U41": "candidate-analysis system",
}

PROPOSED_EVIDENCE = {
    "U01": "controlled task completion", "U02": "reproducible validation",
    "U03": "runtime safety signal", "U04": "externally traceable material",
    "U05": "controlled task completion", "U06": "reproducible validation",
    "U07": "reproducible validation", "U08": "reproducible validation",
    "U09": "reproducible validation", "U10": "reproducible validation",
    "U11": "reproducible validation", "U12": "reproducible validation",
    "U13": "runtime safety signal", "U14": "externally traceable material",
    "U15": "reproducible validation", "U16": "reproducible validation",
    "U17": "externally traceable material", "U18": "controlled task completion",
    "U19": "candidate judgment", "U20": "candidate judgment",
    "U21": "reproducible validation", "U22": "controlled task completion",
    "U23": "controlled task completion", "U24": "controlled task completion",
    "U25": "reproducible validation", "U26": "runtime safety signal",
    "U27": "candidate judgment", "U28": "reproducible validation",
    "U29": "reproducible validation", "U30": "controlled task completion",
    "U31": "controlled task completion", "U32": "controlled task completion",
    "U33": "runtime safety signal", "U34": "runtime safety signal",
    "U35": "candidate judgment", "U36": "reproducible validation",
    "U37": "externally traceable material", "U38": "reproducible validation",
    "U39": "controlled task completion", "U40": "reproducible validation",
    "U41": "candidate judgment",
}

PROPOSED_TRACE = {
    "U01": "benchmark ground truth / public material", "U02": "author-reported external clue",
    "U03": "author-reported external clue", "U04": "publicly aligned external trace",
    "U05": "benchmark ground truth / public material", "U06": "benchmark ground truth / public material",
    "U07": "author-reported external clue", "U08": "benchmark ground truth / public material",
    "U09": "author-reported external clue", "U10": "benchmark ground truth / public material",
    "U11": "benchmark ground truth / public material", "U12": "author-reported external clue",
    "U13": "author-reported external clue", "U14": "publicly aligned external trace",
    "U15": "benchmark ground truth / public material", "U16": "benchmark ground truth / public material",
    "U17": "publicly aligned external trace", "U18": "benchmark ground truth / public material",
    "U19": "benchmark ground truth / public material", "U20": "not reported",
    "U21": "benchmark ground truth / public material", "U22": "no external trace reported",
    "U23": "benchmark ground truth / public material", "U24": "benchmark ground truth / public material",
    "U25": "benchmark ground truth / public material", "U26": "benchmark ground truth / public material",
    "U27": "author-reported external clue", "U28": "benchmark ground truth / public material",
    "U29": "author-reported external clue", "U30": "author-reported external clue",
    "U31": "benchmark ground truth / public material", "U32": "benchmark ground truth / public material",
    "U33": "benchmark ground truth / public material", "U34": "author-reported external clue",
    "U35": "author-reported external clue", "U36": "author-reported external clue",
    "U37": "publicly aligned external trace", "U38": "benchmark ground truth / public material",
    "U39": "benchmark ground truth / public material", "U40": "benchmark ground truth / public material",
    "U41": "author-reported external clue",
}

RECORD_NOTES = {
    "U01": "Ground-truth-patch similarity and LLM review support benchmark task completion, not executable failing-before/passing-after patch validation.",
    "U03": "Dynamic tests provide runtime confirmation, but the generated environments are explicitly ephemeral and discarded.",
    "U04": "Executable invariants, guided fuzzing, PoVs, and item-level public CVE or maintainer records support the aligned external category.",
    "U09": "The public artifact supports reproducibility, while upstream fixes and confirmations remain aggregate rather than item-level aligned in the reviewed material.",
    "U14": "Clean-build PoC re-execution and linked public Chromium issue records support externally traceable material.",
    "U17": "Pinned compiler revisions, reproducible failures, a public artifact, and mapped upstream issue identifiers support the aligned external category.",
    "U21": "The public replication package preserves inputs, wrappers, symbolic-execution outputs, and environment details, supporting reproducible validation.",
    "U24": "The public workflow is a fixed neuro-symbolic repair and selection pipeline; it lacks the observable Agentic tool-feedback loop required for study-level inclusion.",
    "U26": "TLC counterexamples are security-conditioned formal runtime signals, not concrete target-software replay packages.",
    "U27": "The reviewed workflow packages static-analysis findings and generated PoC text without a demonstrated execution oracle or replay chain.",
    "U36": "Replay-guided crash confirmation and dependency-preserving minimization yield reproducible PoCs; vendor and CVE counts remain aggregate in the reviewed public material.",
    "U37": "Specific public CVE and maintainer patch links align system findings with external records.",
    "U39": "Detection and repair are checked by the detector and an LLM validation agent rather than executable failing-before/passing-after tests, so the result remains benchmark task completion.",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def normalize_layer(value: str) -> str:
    return value.removeprefix("provisional_").removesuffix("_pending_independent_review")


def normalize_multilabel(value: str, *, lifecycle: bool = False) -> set[str]:
    labels = {part.strip() for part in value.split(";") if part.strip()}
    if lifecycle and "path exploration" in labels:
        labels.remove("path exploration")
        labels.add("path and input exploration")
    return labels


def canonical_multilabel(value: str, order: list[str], *, lifecycle: bool = False) -> str:
    labels = normalize_multilabel(value, lifecycle=lifecycle)
    unknown = labels - set(order)
    if unknown:
        raise ValueError(f"Unknown multilabel values: {sorted(unknown)}")
    return ";".join(label for label in order if label in labels)


def kappa(left: list[str], right: list[str]) -> float:
    if len(left) != len(right) or not left:
        raise ValueError("Kappa inputs must have equal nonzero length")
    n = len(left)
    observed = sum(a == b for a, b in zip(left, right)) / n
    left_counts = Counter(left)
    right_counts = Counter(right)
    labels = set(left_counts) | set(right_counts)
    expected = sum((left_counts[x] / n) * (right_counts[x] / n) for x in labels)
    return (observed - expected) / (1 - expected) if expected < 1 else 1.0


def single_metrics(left: list[str], right: list[str]) -> tuple[int, float, float]:
    agreements = sum(a == b for a, b in zip(left, right))
    return agreements, agreements / len(left), kappa(left, right)


def multilabel_metrics(left: list[set[str]], right: list[set[str]], labels: list[str]) -> dict[str, object]:
    exact = sum(a == b for a, b in zip(left, right))
    jaccards = [len(a & b) / len(a | b) if a | b else 1.0 for a, b in zip(left, right)]
    tp = sum(len(a & b) for a, b in zip(left, right))
    fp = sum(len(b - a) for a, b in zip(left, right))
    fn = sum(len(a - b) for a, b in zip(left, right))
    micro_f1 = 2 * tp / (2 * tp + fp + fn) if 2 * tp + fp + fn else 1.0
    per_label = {
        label: sum((label in a) == (label in b) for a, b in zip(left, right)) / len(left)
        for label in labels
    }
    return {
        "exact": exact,
        "exact_rate": exact / len(left),
        "mean_jaccard": sum(jaccards) / len(jaccards),
        "micro_f1": micro_f1,
        "per_label": per_label,
    }


def relation(proposed: str, author: str, coder2: str) -> str:
    if proposed == author == coder2:
        return "author_and_coder2_agreed"
    if proposed == author:
        return "author_label_retained"
    if proposed == coder2:
        return "coder2_label_adopted"
    return "operational_rule_harmonization"


def main() -> None:
    author_rows = read_csv(AUTHOR_PATH)
    coder_rows = read_csv(CODER2_PATH)
    if len(author_rows) != 41 or len(coder_rows) != 41:
        raise SystemExit("Expected 41 author rows and 41 coder2 rows")

    author_by_arxiv = {row["arxiv_id"]: row for row in author_rows}
    if len(author_by_arxiv) != 41:
        raise SystemExit("Author audit contains duplicate arXiv identifiers")
    if {row["arxiv_id"] for row in coder_rows} != set(author_by_arxiv):
        raise SystemExit("Author and coder2 arXiv identifier sets differ")

    expected_ids = {f"U{i:02d}" for i in range(1, 42)}
    for mapping_name, mapping in (
        ("layer", PROPOSED_LAYER), ("lifecycle", PROPOSED_LIFECYCLE),
        ("capabilities", PROPOSED_CAPABILITIES), ("shape", PROPOSED_SHAPE),
        ("evidence", PROPOSED_EVIDENCE), ("trace", PROPOSED_TRACE),
    ):
        if set(mapping) != expected_ids:
            raise SystemExit(f"{mapping_name} proposal does not cover U01-U41")

    output_rows: list[dict[str, str]] = []
    for coder in coder_rows:
        author = author_by_arxiv[coder["arxiv_id"]]
        update_id = coder["update_id"]
        if author["title"] != coder["title"]:
            raise SystemExit(f"Title mismatch for {update_id}")

        author_layer = normalize_layer(author["author_analysis_layer"])
        author_lifecycle = canonical_multilabel(author["lifecycle_coverage"], LIFECYCLE_ORDER, lifecycle=True)
        coder_lifecycle = canonical_multilabel(coder["coder2_lifecycle_coverage"], LIFECYCLE_ORDER, lifecycle=True)
        proposed_lifecycle = canonical_multilabel(PROPOSED_LIFECYCLE[update_id], LIFECYCLE_ORDER, lifecycle=True)
        author_capabilities = canonical_multilabel(author["agentic_capabilities"], CAPABILITY_ORDER)
        coder_capabilities = canonical_multilabel(coder["coder2_cross_stage_capability_label"], CAPABILITY_ORDER)
        proposed_capabilities = canonical_multilabel(PROPOSED_CAPABILITIES[update_id], CAPABILITY_ORDER)

        field_relations = [
            "layer=" + relation(PROPOSED_LAYER[update_id], author_layer, coder["coder2_analysis_layer_decision"]),
            "lifecycle=" + relation(proposed_lifecycle, author_lifecycle, coder_lifecycle),
            "capabilities=" + relation(proposed_capabilities, author_capabilities, coder_capabilities),
            "shape=" + relation(PROPOSED_SHAPE[update_id], author["primary_system_shape"], coder["coder2_primary_system_shape"]),
            "evidence=" + relation(PROPOSED_EVIDENCE[update_id], author["strongest_evidence_output"], coder["coder2_strongest_evidence_output"]),
            "trace=" + relation(PROPOSED_TRACE[update_id], author["external_traceability"], coder["coder2_external_traceability_label"]),
        ]
        note = RECORD_NOTES.get(
            update_id,
            "The proposed labels apply the frozen operational definitions to the author and coder2 rationales; differences concern overlapping secondary stages or capabilities.",
        )
        output_rows.append({
            "update_id": update_id,
            "arxiv_id": coder["arxiv_id"],
            "title": coder["title"],
            "publication_status": coder["publication_status"],
            "author_analysis_layer": author_layer,
            "coder2_analysis_layer_decision": coder["coder2_analysis_layer_decision"],
            "proposed_analysis_layer": PROPOSED_LAYER[update_id],
            "author_lifecycle_coverage": author_lifecycle,
            "coder2_lifecycle_coverage": coder_lifecycle,
            "proposed_lifecycle_coverage": proposed_lifecycle,
            "author_primary_system_shape": author["primary_system_shape"],
            "coder2_primary_system_shape": coder["coder2_primary_system_shape"],
            "proposed_primary_system_shape": PROPOSED_SHAPE[update_id],
            "author_agentic_capabilities": author_capabilities,
            "coder2_agentic_capabilities": coder_capabilities,
            "proposed_agentic_capabilities": proposed_capabilities,
            "author_strongest_evidence_output": author["strongest_evidence_output"],
            "coder2_strongest_evidence_output": coder["coder2_strongest_evidence_output"],
            "proposed_strongest_evidence_output": PROPOSED_EVIDENCE[update_id],
            "author_external_traceability": author["external_traceability"],
            "coder2_external_traceability": coder["coder2_external_traceability_label"],
            "proposed_external_traceability": PROPOSED_TRACE[update_id],
            "author_claim_boundary": author["claim_boundary"],
            "coder2_claim_boundary": coder["coder2_claim_boundary"],
            "proposed_claim_boundary": coder["coder2_claim_boundary"],
            "author_decision_reason": author["author_decision_reason"],
            "coder2_inclusion_reason": coder["coder2_inclusion_reason"],
            "coder2_uncertainty_note": coder["coder2_uncertainty_note"],
            "adjudication_basis": note,
            "field_resolution_trace": ";".join(field_relations),
            "adjudication_status": "assistant_proposed_pending_author_confirmation",
        })

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(output_rows[0]))
        writer.writeheader()
        writer.writerows(output_rows)

    author_layers = [row["author_analysis_layer"] for row in output_rows]
    coder_layers = [row["coder2_analysis_layer_decision"] for row in output_rows]
    author_shapes = [row["author_primary_system_shape"] for row in output_rows]
    coder_shapes = [row["coder2_primary_system_shape"] for row in output_rows]
    author_evidence = [row["author_strongest_evidence_output"] for row in output_rows]
    coder_evidence = [row["coder2_strongest_evidence_output"] for row in output_rows]
    author_trace = [row["author_external_traceability"] for row in output_rows]
    coder_trace = [row["coder2_external_traceability"] for row in output_rows]
    life_author = [normalize_multilabel(row["author_lifecycle_coverage"], lifecycle=True) for row in output_rows]
    life_coder = [normalize_multilabel(row["coder2_lifecycle_coverage"], lifecycle=True) for row in output_rows]
    cap_author = [normalize_multilabel(row["author_agentic_capabilities"]) for row in output_rows]
    cap_coder = [normalize_multilabel(row["coder2_agentic_capabilities"]) for row in output_rows]

    layer_metrics = single_metrics(author_layers, coder_layers)
    shape_metrics = single_metrics(author_shapes, coder_shapes)
    evidence_metrics = single_metrics(author_evidence, coder_evidence)
    trace_metrics = single_metrics(author_trace, coder_trace)
    life_metrics = multilabel_metrics(life_author, life_coder, LIFECYCLE_ORDER)
    capability_metrics = multilabel_metrics(cap_author, cap_coder, CAPABILITY_ORDER)

    def disagreements(field_a: str, field_b: str) -> str:
        ids = [row["update_id"] for row in output_rows if row[field_a] != row[field_b]]
        return ", ".join(ids) if ids else "none"

    REPORTS.mkdir(parents=True, exist_ok=True)
    report = f"""# Submission Update Second-Coder Pre-Adjudication Report

## Scope

- Update date: 2026-07-15
- Independently coded records: 41
- Inputs: `data/submission_update_20260715_full_coding_audit.csv` and `data/submission_update_20260715_second_coder_results.csv`
- Status: pre-adjudication agreement from completed independent labels

The completed blind pass contains all 41 decisions and does not expose author labels. Agreement below compares the frozen author audit with the independent coder2 results before any resolution. The proposed resolution is stored separately as a working draft and is not reported as human consensus.

## Single-Label Fields

| Field | Agreement | Raw agreement | Cohen's kappa | Disagreement rows |
|---|---:|---:|---:|---|
| Analysis layer | {layer_metrics[0]} / 41 | {layer_metrics[1]:.3f} | {layer_metrics[2]:.3f} | {disagreements('author_analysis_layer', 'coder2_analysis_layer_decision')} |
| Primary system shape | {shape_metrics[0]} / 41 | {shape_metrics[1]:.3f} | {shape_metrics[2]:.3f} | {disagreements('author_primary_system_shape', 'coder2_primary_system_shape')} |
| Principal reported evidence output | {evidence_metrics[0]} / 41 | {evidence_metrics[1]:.3f} | {evidence_metrics[2]:.3f} | {disagreements('author_strongest_evidence_output', 'coder2_strongest_evidence_output')} |
| External traceability | {trace_metrics[0]} / 41 | {trace_metrics[1]:.3f} | {trace_metrics[2]:.3f} | {disagreements('author_external_traceability', 'coder2_external_traceability')} |

## Multi-Label Fields

| Field | Row-level exact | Mean row Jaccard | Micro F1 |
|---|---:|---:|---:|
| Lifecycle coverage | {life_metrics['exact']} / 41 = {life_metrics['exact_rate']:.3f} | {life_metrics['mean_jaccard']:.3f} | {life_metrics['micro_f1']:.3f} |
| Agentic capabilities | {capability_metrics['exact']} / 41 = {capability_metrics['exact_rate']:.3f} | {capability_metrics['mean_jaccard']:.3f} | {capability_metrics['micro_f1']:.3f} |

`path exploration` in the author audit is normalized to the frozen label `path and input exploration` before comparison. Row-level exact agreement is intentionally strict; Jaccard and micro F1 capture overlap among secondary labels.

### Per-Label Raw Agreement

| Lifecycle label | Agreement |
|---|---:|
"""
    for label in LIFECYCLE_ORDER:
        report += f"| {label} | {life_metrics['per_label'][label]:.3f} |\n"
    report += "\n| Agentic-capability label | Agreement |\n|---|---:|\n"
    for label in CAPABILITY_ORDER:
        report += f"| {label} | {capability_metrics['per_label'][label]:.3f} |\n"

    report += """

## Interpretation

- The analytical-layer boundary is stable except for U24 (SynthFix).
- Lifecycle differences are concentrated in whether ordinary result packaging counts as `reporting and audit`, and whether input generation or patch checks constitute separate lifecycle stages.
- Capability differences are concentrated in strict thresholds for long-horizon state, dynamic tool routing, failure reuse, and governance controls.
- Evidence-output and traceability differences primarily concern whether public artifacts are reproducibility material or whether item-level external alignment is available.

No adjudicated labels or post-adjudication agreement statistic are claimed in this report.
"""
    REPORT_PATH.write_text(report, encoding="utf-8")

    proposed_layers = Counter(row["proposed_analysis_layer"] for row in output_rows)
    proposed_evidence = Counter(row["proposed_strongest_evidence_output"] for row in output_rows)
    proposed_trace = Counter(row["proposed_external_traceability"] for row in output_rows)
    summary = f"""# Submission Update Adjudication Summary

## Status

`data/submission_update_20260715_adjudication_working_draft.csv` is an evidence-based proposed resolution of the completed 41-record blind pass. It preserves author and coder2 labels side by side and marks every row `assistant_proposed_pending_author_confirmation`. It does not represent a discussion between two human coders or a completed consensus round.

## Operational Resolution Rules

1. Ordinary paper reporting is not coded as a system-level `reporting and audit` stage; the workflow must explicitly package or route evidence for audit, disclosure, or downstream review.
2. Short iterative loops do not automatically count as `long-horizon state management`; persistent state must span nontrivial iterations, tasks, or strategy transitions.
3. `tool routing` requires a dynamic choice of tool or strategy, rather than a fixed pipeline that merely invokes tools.
4. Runtime or formal counterexamples support `runtime safety signal`; `reproducible validation` additionally requires a replay, PoC/PoV, patch-validation, or equivalent versioned validation package.
5. `externally traceable material` requires item-level alignment between a concrete system output and a public issue, advisory, CVE, patch, commit, or comparable external record. Aggregate author reports remain `author-reported external clue`.
6. Primary system shape follows the dominant workflow role and evidence-producing mechanism; shape labels remain descriptive and may overlap.

## Proposed Outcome Pending Author Confirmation

- Study-level candidates: {proposed_layers['study_level_candidate']}
- Extended-synthesis records: {proposed_layers['extended_synthesis']}
- Boundary change: U24 (SynthFix) moves from provisional study-level candidate to extended synthesis.
- Proposed strongest-evidence distribution: {dict(sorted(proposed_evidence.items()))}
- Proposed external-traceability distribution: {dict(sorted(proposed_trace.items()))}

The working draft does not itself change the frozen manuscript or canonical corpus denominators. The author subsequently accepted the proposed resolution on 2026-07-15; the confirmed record is generated separately as `data/submission_update_20260715_adjudicated.csv`. Canonical matching and manuscript integration remain separate operations.

## Files

- Independent results: `data/submission_update_20260715_second_coder_results.csv`
- Pre-adjudication report: `reports/SUBMISSION_UPDATE_SECOND_CODER_PRE_ADJUDICATION_REPORT.md`
- Proposed working draft: `data/submission_update_20260715_adjudication_working_draft.csv`
- Reproduction script: `prepare_submission_update_adjudication.py`
"""
    SUMMARY_PATH.write_text(summary, encoding="utf-8")

    print(f"WROTE {OUTPUT_PATH.relative_to(ROOT)} ({len(output_rows)} rows)")
    print(f"WROTE {REPORT_PATH.relative_to(ROOT)}")
    print(f"WROTE {SUMMARY_PATH.relative_to(ROOT)}")
    print(f"PROPOSED_LAYER_COUNTS {dict(sorted(proposed_layers.items()))}")
    print(f"PRE_ADJUDICATION_EVIDENCE {evidence_metrics[0]}/41 raw={evidence_metrics[1]:.3f} kappa={evidence_metrics[2]:.3f}")


if __name__ == "__main__":
    main()
