#!/usr/bin/env python3
from __future__ import annotations
import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"

def read(name):
    with (DATA / name).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def write(name, rows):
    if not rows:
        return
    with (DATA / name).open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), extrasaction="ignore")
        w.writeheader(); w.writerows(rows)

matrix = {r["matrix_id"]: r for r in read("adjudicated_study_level_coding_matrix_199.csv")}
target = {k: v for k, v in matrix.items() if v.get("analytical_role") == "target_software_study"}

pub = read("publication_status_standardized.csv")
for r in pub:
    m = target[r["matrix_id"]]
    r["strongest_evidence_output"] = m["strongest_evidence_output"]
    r["primary_system_shape"] = m["primary_system_shape"]
    r["cross_stage_capabilities"] = m["cross_stage_capabilities"]
    r["external_traceability"] = m["external_traceability"]
write("publication_status_standardized.csv", pub)

domains = read("target_domain_extraction.csv")
for r in domains:
    m = target[r["matrix_id"]]
    r["primary_system_shape"] = m["primary_system_shape"]
    r["principal_reported_evidence_output"] = m["strongest_evidence_output"]
write("target_domain_extraction.csv", domains)

# The denominator sensitivity is a deterministic two-field classification, not
# a post-hoc judgment.  Preserve all 199 membership decisions so the excluded
# cohort and every retained boundary case can be recomputed directly.
domain_by_id = {r["matrix_id"]: r for r in domains}
controlled_task_domain = "cyber range, CTF, or penetration testing"
membership = []
for matrix_id, m in sorted(target.items()):
    domain = domain_by_id[matrix_id]
    output = m["strongest_evidence_output"]
    is_controlled_output = output == "controlled task completion"
    is_controlled_domain = domain["target_domain"] == controlled_task_domain
    excluded = is_controlled_output and is_controlled_domain
    if excluded:
        reason = (
            "Excluded: principal output is controlled task completion and the "
            "author-audited target domain is cyber range, CTF, or penetration testing."
        )
    elif not is_controlled_output:
        reason = f"Retained: principal output is {output}, not controlled task completion."
    else:
        reason = (
            "Retained: principal output is controlled task completion, but the "
            f"author-audited target domain is {domain['target_domain']}."
        )
    membership.append({
        "matrix_id": matrix_id,
        "study_title": m["title"],
        "principal_reported_evidence_output": output,
        "target_domain": domain["target_domain"],
        "controlled_task_only_excluded": "yes" if excluded else "no",
        "decision_reason": reason,
        "domain_source_location": domain["source_location"],
    })
write("controlled_task_only_membership.csv", membership)

excluded_ids = {r["matrix_id"] for r in membership if r["controlled_task_only_excluded"] == "yes"}
scopes = {
    "all_target_software": list(target.values()),
    "excluding_controlled_task_only": [r for i, r in target.items() if i not in excluded_ids],
}
measures = {
    "author_reported_reproducible_validation": lambda r: r["strongest_evidence_output"] == "reproducible validation",
    "publicly_aligned_external_trace": lambda r: r["external_traceability"] == "publicly aligned external trace",
    "author_reported_external_clue": lambda r: r["external_traceability"] == "author-reported external clue",
}
sensitivity = []
definition = (
    "principal output is controlled task completion and target domain is cyber "
    "range, CTF, or penetration testing; real-OSS CRS workflows with another "
    "principal output remain in the denominator"
)
for scope, subset in scopes.items():
    for measure, predicate in measures.items():
        count = sum(predicate(r) for r in subset)
        sensitivity.append({
            "scope": scope,
            "controlled_task_only_excluded": len(excluded_ids) if scope == "excluding_controlled_task_only" else 0,
            "definition": definition,
            "measure": measure,
            "count": count,
            "denominator": len(subset),
            "share": f"{count / len(subset):.6f}",
        })
write("controlled_task_only_sensitivity.csv", sensitivity)

artifacts = read("public_artifact_availability.csv")
for r in artifacts:
    r["principal_reported_evidence_output"] = target[r["matrix_id"]]["strongest_evidence_output"]
write("public_artifact_availability.csv", artifacts)

detailed = read("traditional_security_primitives_by_use_role.csv")
families = sorted({r["primitive_family"] for r in detailed})
outputs = ["candidate judgment", "controlled task completion", "runtime safety signal", "reproducible validation", "externally traceable material"]
rows = []
for fam in families:
    ids = {r["matrix_id"] for r in detailed if r["primitive_family"] == fam}
    for label in outputs:
        rows.append({"primitive_family": fam, "principal_reported_evidence_output": label, "count": sum(target[i]["strongest_evidence_output"] == label for i in ids), "primitive_union_denominator": len(ids)})
write("traditional_security_primitive_by_output.csv", rows)

pre = {r["matrix_id"] for r in read("current_study_level_coding_matrix_harmonized_pre_final_multisource_20260730.csv") if r.get("analytical_role") == "target_software_study"}
cohorts = [("retained_pre_final_67", {i: target[i] for i in pre}), ("new_multisource_132", {i: r for i, r in target.items() if i not in pre})]
rows = []
for name, subset in cohorts:
    den = len(subset)
    for label, count in sorted(Counter(r["primary_system_shape"] for r in subset.values()).items()):
        rows.append({"cohort": name, "denominator": den, "dimension": "primary_system_shape", "label": label, "count": count, "share": f"{count/den:.3f}"})
    for label, count in sorted(Counter(r["strongest_evidence_output"] for r in subset.values()).items()):
        rows.append({"cohort": name, "denominator": den, "dimension": "principal_reported_evidence_output", "label": label, "count": count, "share": f"{count/den:.3f}"})
    counts = Counter()
    for r in subset.values():
        counts.update(x.strip() for x in r["cross_stage_capabilities"].split(";") if x.strip())
    for label, count in sorted(counts.items()):
        rows.append({"cohort": name, "denominator": den, "dimension": "cross_stage_capability", "label": label, "count": count, "share": f"{count/den:.3f}"})
write("final_multisource_cohort_stability.csv", rows)

groups = {
    "all_target_software": list(target.values()),
    "conference_or_journal": [r for r in pub if r["publication_status_standardized"] in {"conference", "journal"}],
    "preprint": [r for r in pub if r["publication_status_standardized"] == "preprint"],
    "benchmark_report_or_other": [r for r in pub if r["publication_status_standardized"] in {"benchmark/system report", "report/other"}],
}
rows = []
for group, subset in groups.items():
    den = len(subset)
    for dim, field in (("primary_system_shape", "primary_system_shape"), ("principal_reported_evidence_output", "strongest_evidence_output")):
        for label, count in sorted(Counter(r[field] for r in subset).items()):
            rows.append({"scope": "199_target_software_studies", "publication_status_group": group, "dimension": dim, "label": label, "count": count, "denominator": den, "share": f"{count/den:.6f}"})
write("publication_status_sensitivity_analysis.csv", rows)

rows = []
for domain in sorted({r["target_domain"] for r in domains}):
    subset = [r for r in domains if r["target_domain"] == domain]
    counts = Counter(r["principal_reported_evidence_output"] for r in subset)
    for label in outputs:
        count = counts[label]
        rows.append({"target_domain": domain, "principal_reported_evidence_output": label, "count": count, "domain_denominator": len(subset)})
write("target_domain_by_principal_output.csv", rows)

rows = []
for year in sorted({r["publication_year"] for r in domains}):
    subset = [r for r in domains if r["publication_year"] == year]
    counts = Counter(r["primary_system_shape"] for r in subset)
    for label in ("candidate-analysis system", "feedback-driven fuzzing agent", "reproduction-, validation-, and repair-centered agent", "long-horizon pentest and CRS agent"):
        count = counts[label]
        rows.append({"publication_year": year, "primary_system_shape": label, "count": count, "year_denominator": len(subset), "interpretation_note": "Descriptive count; 2026 is an incomplete publication year."})
write("publication_year_by_primary_shape.csv", rows)

rows = []
for label in sorted({r["principal_reported_evidence_output"] for r in artifacts}):
    subset = [r for r in artifacts if r["principal_reported_evidence_output"] == label]
    row = {"principal_reported_evidence_output": label, "studies": len(subset)}
    for field in ("public_implementation_located", "environment_or_build_instructions", "trigger_replay_poc_pov_artifact", "execution_trace_or_log", "patch_artifact"):
        row[field] = sum(r[field] == "located" for r in subset)
    rows.append(row)
write("principal_output_by_public_artifact_availability.csv", rows)
print(f"REGENERATED_DERIVED_VIEWS target={len(target)}")
