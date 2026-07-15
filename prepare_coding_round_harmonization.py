from __future__ import annotations

import csv
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"

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

PRIMARY_SHAPES = {
    "candidate-analysis system",
    "feedback-driven fuzzing agent",
    "reproduction-, validation-, and repair-centered agent",
    "long-horizon pentest and CRS agent",
    "governance boundary case",
}

OVERLAY_ORDER = [
    "multi-agent orchestration",
    "iterative optimization",
    "failure-memory reuse",
    "governance control",
]

SHAPE_RENAME = {
    "PoC/PoV validation agent": "reproduction-, validation-, and repair-centered agent",
}

# These proposals use only explicit statements already present in the frozen
# initial-round coding notes. They remain pending until the author reviews them.
LIFECYCLE_ADDITIONS = {
    "C01": ["candidate analysis"],
    "C02": ["execution observation"],
    "C08": ["candidate analysis"],
    "C12": ["reporting and audit"],
    "C13": ["candidate analysis"],
    "C16": ["execution observation"],
    "C17": ["execution observation"],
    "C20": ["candidate analysis"],
    "C21": ["candidate analysis"],
    "C22": ["execution observation"],
    "C24": ["execution observation"],
    "C27": ["path and input exploration", "execution observation"],
    "C28": ["candidate analysis"],
    "C29": ["execution observation"],
    "C30": ["candidate analysis"],
}

CAPABILITY_ADDITIONS = {
    "C01": ["context aggregation / rule extraction", "tool routing / strategy routing"],
    "C02": ["tool routing / strategy routing"],
    "C05": ["context aggregation / rule extraction"],
    "C06": ["context aggregation / rule extraction"],
    "C07": ["context aggregation / rule extraction"],
    "C08": ["context aggregation / rule extraction"],
    "C11": [
        "context aggregation / rule extraction",
        "tool routing / strategy routing",
        "feedback interpretation / loop adjustment",
    ],
    "C12": [
        "context aggregation / rule extraction",
        "tool routing / strategy routing",
        "feedback interpretation / loop adjustment",
        "validation organization / evidence packaging",
    ],
    "C13": ["context aggregation / rule extraction", "tool routing / strategy routing"],
    "C14": [
        "context aggregation / rule extraction",
        "tool routing / strategy routing",
        "feedback interpretation / loop adjustment",
    ],
    "C15": ["context aggregation / rule extraction", "tool routing / strategy routing"],
    "C16": ["context aggregation / rule extraction"],
    "C17": [
        "tool routing / strategy routing",
        "feedback interpretation / loop adjustment",
        "validation organization / evidence packaging",
    ],
    "C18": ["context aggregation / rule extraction", "tool routing / strategy routing"],
    "C20": ["context aggregation / rule extraction"],
    "C21": ["context aggregation / rule extraction"],
    "C23": ["tool routing / strategy routing", "feedback interpretation / loop adjustment"],
    "C24": [
        "tool routing / strategy routing",
        "feedback interpretation / loop adjustment",
        "validation organization / evidence packaging",
    ],
    "C25": ["tool routing / strategy routing", "long-horizon state management"],
    "C27": ["feedback interpretation / loop adjustment"],
    "C28": [
        "context aggregation / rule extraction",
        "tool routing / strategy routing",
        "feedback interpretation / loop adjustment",
        "validation organization / evidence packaging",
    ],
    "C29": ["context aggregation / rule extraction"],
    "C30": [
        "context aggregation / rule extraction",
        "tool routing / strategy routing",
        "feedback interpretation / loop adjustment",
        "validation organization / evidence packaging",
    ],
}

PRIMARY_SHAPE_RESOLUTION = {
    "C07": "candidate-analysis system",
    "C20": "reproduction-, validation-, and repair-centered agent",
    "C31": "feedback-driven fuzzing agent",
}


def split_labels(value: str) -> list[str]:
    return [part.strip() for part in str(value or "").split(";") if part.strip()]


def ordered(labels: list[str], vocabulary: list[str]) -> str:
    label_set = set(labels)
    unknown = sorted(label_set - set(vocabulary))
    if unknown:
        raise ValueError(f"Unknown controlled labels: {unknown}")
    return ";".join(label for label in vocabulary if label in label_set)


def parse_shape(matrix_id: str, value: str, capabilities: str) -> tuple[str, str, str]:
    parts = split_labels(value)
    overlays: list[str] = []
    primary_candidates: list[str] = []
    for part in parts:
        if "multi-agent orchestration overlay" in part:
            overlays.append("multi-agent orchestration")
        elif "iterative optimization overlay" in part:
            overlays.append("iterative optimization")
        else:
            primary_candidates.append(SHAPE_RENAME.get(part, part))

    if "failure reuse / strategy update" in split_labels(capabilities):
        overlays.append("failure-memory reuse")
    if matrix_id == "C27":
        overlays.append("governance control")

    if matrix_id in PRIMARY_SHAPE_RESOLUTION:
        primary = PRIMARY_SHAPE_RESOLUTION[matrix_id]
        resolution = "explicit primary-shape resolution from the frozen system-archetype note"
    elif len(set(primary_candidates)) == 1:
        primary = primary_candidates[0]
        resolution = "schema normalization; no primary-shape meaning changed"
    else:
        raise ValueError(f"{matrix_id}: unresolved primary shapes {primary_candidates}")

    if primary not in PRIMARY_SHAPES:
        raise ValueError(f"{matrix_id}: unapproved primary shape {primary}")
    overlay_value = ordered(overlays, OVERLAY_ORDER)
    return primary, overlay_value, resolution


def add_audit_row(
    rows: list[dict[str, str]], *, matrix_id: str, record_id: str,
    coding_round: str, field: str, original: str, candidate: str,
    change_required: str, evidence_basis: str, source_location: str,
    uncertainty: str, review_status: str, final_label: str,
) -> None:
    rows.append({
        "matrix_id": matrix_id,
        "record_id": record_id,
        "coding_round": coding_round,
        "field": field,
        "original_label": original,
        "current_codebook_candidate_label": candidate,
        "change_required": change_required,
        "evidence_basis": evidence_basis,
        "source_location": source_location,
        "uncertainty": uncertainty,
        "author_review_status": review_status,
        "final_harmonized_label": final_label,
    })


def main() -> None:
    current = pd.read_csv(DATA / "current_study_level_coding_matrix.csv").fillna("")
    frozen = pd.read_csv(DATA / "v13_core_synthesis_matrix.csv").fillna("")
    core = pd.read_csv(DATA / "core_coding.csv").fillna("")
    notes = frozen.merge(
        core[["core_id", "a_level_reason", "e_level_reason", "note"]],
        on="core_id", how="left",
    ).set_index("core_id")

    audit_rows: list[dict[str, str]] = []
    output_rows: list[dict[str, str]] = []

    for _, row in current.iterrows():
        r = row.to_dict()
        matrix_id = r["matrix_id"]
        record_id = r["record_id"]
        initial = r["coding_round"] == "initial_frozen_round"
        source = (
            f"data/v13_core_synthesis_matrix.csv:{matrix_id}; "
            f"data/core_coding.csv:{matrix_id}"
            if initial else
            f"data/submission_update_20260715_adjudicated.csv:{matrix_id}"
        )

        original_lifecycle = r["lifecycle_coverage"]
        lifecycle_candidate = original_lifecycle
        lifecycle_status = "not_required"
        lifecycle_final = original_lifecycle
        lifecycle_basis = "Existing label already uses the current controlled vocabulary."
        lifecycle_uncertainty = "none"
        if initial and matrix_id in LIFECYCLE_ADDITIONS:
            lifecycle_candidate = ordered(
                split_labels(original_lifecycle) + LIFECYCLE_ADDITIONS[matrix_id],
                LIFECYCLE_ORDER,
            )
            lifecycle_status = "pending_author_review"
            lifecycle_final = ""
            lifecycle_basis = str(notes.loc[matrix_id, "a_level_reason"])
            lifecycle_uncertainty = "medium; secondary stage inferred from an explicit frozen workflow note"
        add_audit_row(
            audit_rows, matrix_id=matrix_id, record_id=record_id,
            coding_round=r["coding_round"], field="lifecycle_coverage",
            original=original_lifecycle, candidate=lifecycle_candidate,
            change_required="yes" if lifecycle_candidate != original_lifecycle else "no",
            evidence_basis=lifecycle_basis, source_location=source,
            uncertainty=lifecycle_uncertainty, review_status=lifecycle_status,
            final_label=lifecycle_final,
        )

        primary, overlays, shape_basis = parse_shape(
            matrix_id, r["system_shape"], r["agentic_capabilities"]
        )
        add_audit_row(
            audit_rows, matrix_id=matrix_id, record_id=record_id,
            coding_round=r["coding_round"], field="primary_system_shape",
            original=r["system_shape"], candidate=primary,
            change_required="schema_normalization",
            evidence_basis=shape_basis, source_location=source,
            uncertainty="none", review_status="not_required_schema_normalization",
            final_label=primary,
        )
        add_audit_row(
            audit_rows, matrix_id=matrix_id, record_id=record_id,
            coding_round=r["coding_round"], field="overlay_tags",
            original=r["system_shape"], candidate=overlays,
            change_required="schema_normalization",
            evidence_basis="Explicit overlay text and controlled capability labels were separated from the primary shape.",
            source_location=source, uncertainty="none",
            review_status="not_required_schema_normalization", final_label=overlays,
        )

        original_caps = r["agentic_capabilities"]
        cleaned_caps = [
            value for value in split_labels(original_caps)
            if value != "role discussion / textual reflection"
        ]
        caps_candidate = ordered(cleaned_caps, CAPABILITY_ORDER)
        caps_status = "not_required_schema_normalization" if caps_candidate != original_caps else "not_required"
        caps_final = caps_candidate
        caps_basis = "Legacy textual-reflection label removed from the formal controlled field and retained in legacy_notes."
        caps_uncertainty = "none"
        if initial and matrix_id in CAPABILITY_ADDITIONS:
            caps_candidate = ordered(cleaned_caps + CAPABILITY_ADDITIONS[matrix_id], CAPABILITY_ORDER)
            caps_status = "pending_author_review"
            caps_final = ""
            caps_basis = str(notes.loc[matrix_id, "a_level_reason"])
            caps_uncertainty = "medium; secondary capability inferred from an explicit frozen workflow note"
        add_audit_row(
            audit_rows, matrix_id=matrix_id, record_id=record_id,
            coding_round=r["coding_round"], field="cross_stage_capabilities",
            original=original_caps, candidate=caps_candidate,
            change_required="yes" if caps_candidate != original_caps else "no",
            evidence_basis=caps_basis, source_location=source,
            uncertainty=caps_uncertainty, review_status=caps_status,
            final_label=caps_final,
        )

        for field in ["strongest_evidence_output", "external_traceability"]:
            value = r[field]
            add_audit_row(
                audit_rows, matrix_id=matrix_id, record_id=record_id,
                coding_round=r["coding_round"], field=field,
                original=value, candidate=value, change_required="no",
                evidence_basis="Preserved from the field-specific independently checked coding result.",
                source_location=source, uncertainty="none",
                review_status="not_required", final_label=value,
            )

        out = dict(r)
        out.pop("system_shape", None)
        out.pop("agentic_capabilities", None)
        out["primary_system_shape"] = primary
        out["overlay_tags"] = overlays
        out["cross_stage_capabilities"] = ordered(cleaned_caps, CAPABILITY_ORDER)
        out["proposed_lifecycle_coverage"] = lifecycle_candidate
        out["proposed_cross_stage_capabilities"] = caps_candidate
        out["harmonization_status"] = (
            "pending_author_review"
            if lifecycle_status == "pending_author_review" or caps_status == "pending_author_review"
            else "author_confirmed_or_schema_only"
        )
        out["legacy_notes"] = (
            "role discussion / textual reflection retained from the frozen initial label"
            if "role discussion / textual reflection" in original_caps else ""
        )
        output_rows.append(out)

    audit = pd.DataFrame(audit_rows)
    harmonized = pd.DataFrame(output_rows)
    audit.to_csv(DATA / "coding_round_harmonization_audit.csv", index=False, quoting=csv.QUOTE_MINIMAL)
    harmonized.to_csv(
        DATA / "current_study_level_coding_matrix_harmonized.csv",
        index=False, quoting=csv.QUOTE_MINIMAL,
    )

    pending = audit[audit["author_review_status"] == "pending_author_review"]
    print(f"audit rows: {len(audit)}")
    print(f"matrix rows: {len(harmonized)}")
    print(f"pending field decisions: {len(pending)}")
    print(pending.groupby("field").size().to_string())


if __name__ == "__main__":
    main()
