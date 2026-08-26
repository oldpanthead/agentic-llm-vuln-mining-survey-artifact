import argparse
import csv
import sys
from collections import Counter
from pathlib import Path


FIELD_RULES = {
    "lifecycle coverage": {
        "type": "multi-label",
        "allowed": [
            "candidate analysis",
            "path and input exploration",
            "execution observation",
            "reproduction and validation",
            "patch validation",
            "reporting and audit",
        ],
    },
    "cross-stage capability": {
        "type": "multi-label",
        "allowed": [
            "context aggregation / rule extraction",
            "tool routing / strategy routing",
            "feedback interpretation / loop adjustment",
            "validation organization / evidence packaging",
            "long-horizon state management",
            "failure reuse / strategy update",
            "governance / human gates / disclosure control",
        ],
    },
    "primary system shape": {
        "type": "single-label",
        "allowed": [
            "candidate-analysis system",
            "feedback-driven fuzzing agent",
            "reproduction-, validation-, and repair-centered agent",
            "long-horizon pentest and CRS agent",
        ],
    },
    "principal reported evidence output": {
        "type": "single-label",
        "allowed": [
            "candidate judgment",
            "controlled task completion",
            "runtime safety signal",
            "reproducible validation",
            "externally traceable material",
        ],
    },
    "external traceability": {
        "type": "single-label",
        "allowed": [
            "no external trace reported",
            "author-reported external clue",
            "benchmark ground truth / public material",
            "publicly aligned external trace",
        ],
    },
}

EMPTY_SET_LABEL = "no qualifying label observed"

EXPECTED_COUNTS = {
    "lifecycle coverage": 147,
    "cross-stage capability": 137,
    "primary system shape": 23,
    "principal reported evidence output": 48,
    "external traceability": 55,
}

REQUIRED_COLUMNS = {
    "disagreement_id",
    "record_id",
    "field",
    "coder_x_label",
    "coder_y_label",
    "evidence_location_lead",
    "evidence_excerpt_lead",
    "codebook_rule",
    "human_final_label",
    "brief_reason",
    "evidence_location_verified",
    "unresolved",
}


def normalize_multilabel(value, allowed):
    labels = [part.strip() for part in value.split(";") if part.strip()]
    unknown = [label for label in labels if label not in allowed]
    duplicates = len(labels) != len(set(labels))
    expected_order = [label for label in allowed if label in set(labels)]
    return labels, unknown, duplicates, labels != expected_order


def validate(path, allow_pending):
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        missing_columns = REQUIRED_COLUMNS - set(reader.fieldnames or [])
        if missing_columns:
            return [f"Missing columns: {', '.join(sorted(missing_columns))}"], []
        rows = list(reader)

    errors = []
    warnings = []
    if len(rows) != 410:
        errors.append(f"Expected 410 rows, found {len(rows)}")
    ids = [row["disagreement_id"].strip() for row in rows]
    duplicate_ids = [key for key, count in Counter(ids).items() if count > 1]
    if duplicate_ids:
        errors.append(f"Duplicate disagreement_id values: {', '.join(duplicate_ids[:10])}")
    counts = Counter(row["field"].strip() for row in rows)
    if dict(counts) != EXPECTED_COUNTS:
        errors.append(f"Field counts differ: {dict(counts)}")

    unresolved_count = 0
    pending_count = 0
    for index, row in enumerate(rows, start=2):
        row_id = row["disagreement_id"].strip() or f"row {index}"
        field = row["field"].strip()
        if field not in FIELD_RULES:
            errors.append(f"{row_id}: unknown field {field!r}")
            continue
        if not row["evidence_location_lead"].strip() or not row["evidence_excerpt_lead"].strip():
            errors.append(f"{row_id}: missing prepared evidence lead")
        final_label = row["human_final_label"].strip()
        reason = row["brief_reason"].strip()
        location = row["evidence_location_verified"].strip()
        unresolved = row["unresolved"].strip().lower()
        if not final_label and not reason and not location and not unresolved:
            pending_count += 1
            if not allow_pending:
                errors.append(f"{row_id}: human adjudication is blank")
            continue
        if unresolved not in {"yes", "no"}:
            errors.append(f"{row_id}: unresolved must be yes or no")
        if not reason:
            errors.append(f"{row_id}: brief_reason is required")
        if not location:
            errors.append(f"{row_id}: evidence_location_verified is required")
        if unresolved == "yes":
            unresolved_count += 1
            if final_label != "unresolved":
                errors.append(f"{row_id}: unresolved=yes requires human_final_label=unresolved")
            continue
        if final_label == "unresolved":
            errors.append(f"{row_id}: human_final_label=unresolved requires unresolved=yes")
            continue
        rule = FIELD_RULES[field]
        if rule["type"] == "single-label":
            if final_label not in rule["allowed"]:
                errors.append(f"{row_id}: invalid single label {final_label!r}")
        else:
            if final_label == EMPTY_SET_LABEL:
                continue
            labels, unknown, duplicates, wrong_order = normalize_multilabel(final_label, rule["allowed"])
            if not labels:
                errors.append(f"{row_id}: at least one multi-label value is required")
            if unknown:
                errors.append(f"{row_id}: invalid labels {unknown}")
            if duplicates:
                errors.append(f"{row_id}: duplicate labels")
            if wrong_order:
                errors.append(f"{row_id}: multi-label values are not in codebook order")

    warnings.append(f"Pending rows: {pending_count}")
    warnings.append(f"Unresolved rows: {unresolved_count}")
    return errors, warnings


def main():
    parser = argparse.ArgumentParser(description="Validate the completed 199-study adjudication CSV.")
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--allow-pending", action="store_true", help="Validate package structure before human completion.")
    args = parser.parse_args()
    errors, warnings = validate(args.csv_path, args.allow_pending)
    for message in warnings:
        print(message)
    if errors:
        for message in errors:
            print(f"ERROR: {message}", file=sys.stderr)
        print(f"ADJUDICATION_VALIDATION_FAILED ({len(errors)} errors)", file=sys.stderr)
        raise SystemExit(1)
    print("ADJUDICATION_VALIDATION_OK")


if __name__ == "__main__":
    main()
