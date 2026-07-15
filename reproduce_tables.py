#!/usr/bin/env python3
import csv
import sys
import subprocess
import re
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'data'
REPORTS = ROOT / 'reports'

CSV_REQUIRED_FIELDS = {
    'corpus.csv': ['record_id', 'corpus_layer'],
    'current_study_level_coding_matrix.csv': [
        'matrix_id',
        'record_id',
        'canonical_study_id',
        'system_alias',
        'title',
        'analytical_role',
        'coding_round',
        'lifecycle_coverage',
        'system_shape',
        'agentic_capabilities',
        'strongest_evidence_output',
        'external_traceability',
        'claim_boundary',
        'claim_boundary_original',
        'coding_status',
        'reliability_scope',
        'official_url',
    ],
    'submission_update_20260715_screening_audit.csv': [
      'arxiv_id',
      'title',
      'published',
      'existing_record_id',
      'screening_status',
      'screening_level',
      'decision_reason',
      'analytical_implication',
      'official_url',
      'query_ids',
    ],
    'submission_update_20260715_full_coding_audit.csv': [
      'arxiv_id',
      'title',
      'official_url',
      'published',
      'review_material',
      'full_text_status',
      'author_analysis_layer',
      'inclusion_rule_applied',
      'target_domain',
      'lifecycle_coverage',
      'agentic_capabilities',
      'strongest_evidence_output',
      'external_traceability',
      'primary_system_shape',
      'claim_boundary',
      'author_decision_reason',
      'uncertainty_note',
      'formal_second_coder_status',
    ],
    'submission_update_20260715_second_coder_blind_template.csv': [
      'update_id',
      'arxiv_id',
      'title',
      'publication_status',
      'materials_to_review',
      'coder2_analysis_layer_decision',
      'coder2_inclusion_reason',
      'coder2_lifecycle_coverage',
      'coder2_primary_system_shape',
      'coder2_cross_stage_capability_label',
      'coder2_strongest_evidence_output',
      'coder2_external_traceability_label',
      'coder2_claim_boundary',
      'coder2_uncertainty_note',
    ],
    'submission_update_20260715_second_coder_results.csv': [
      'update_id',
      'arxiv_id',
      'title',
      'publication_status',
      'materials_to_review',
      'coder2_analysis_layer_decision',
      'coder2_inclusion_reason',
      'coder2_lifecycle_coverage',
      'coder2_primary_system_shape',
      'coder2_cross_stage_capability_label',
      'coder2_strongest_evidence_output',
      'coder2_external_traceability_label',
      'coder2_claim_boundary',
      'coder2_uncertainty_note',
    ],
    'submission_update_20260715_adjudication_working_draft.csv': [
      'update_id',
      'arxiv_id',
      'title',
      'publication_status',
      'author_analysis_layer',
      'coder2_analysis_layer_decision',
      'proposed_analysis_layer',
      'author_lifecycle_coverage',
      'coder2_lifecycle_coverage',
      'proposed_lifecycle_coverage',
      'author_primary_system_shape',
      'coder2_primary_system_shape',
      'proposed_primary_system_shape',
      'author_agentic_capabilities',
      'coder2_agentic_capabilities',
      'proposed_agentic_capabilities',
      'author_strongest_evidence_output',
      'coder2_strongest_evidence_output',
      'proposed_strongest_evidence_output',
      'author_external_traceability',
      'coder2_external_traceability',
      'proposed_external_traceability',
      'author_claim_boundary',
      'coder2_claim_boundary',
      'proposed_claim_boundary',
      'author_decision_reason',
      'coder2_inclusion_reason',
      'coder2_uncertainty_note',
      'adjudication_basis',
      'field_resolution_trace',
      'adjudication_status',
    ],    'study_version_crosswalk.csv': [
        'record_id',
        'title',
        'canonical_study_id',
        'canonical_record_id',
        'version_type',
        'source_version',
        'same_study_as',
        'dedup_basis',
        'analytical_layer',
        'counting_status',
        'retained_reason',
        'notes',
    ],
    'extended_synthesis_audit.csv': [
        'record_id',
        'citation_key',
        'title',
        'material_type',
        'primary_synthesis_role',
        'secondary_synthesis_roles',
        'rq_contribution',
        'manuscript_section_use',
        'extracted_contribution',
        'reason_not_study_level_coded',
        'public_material_basis',
        'reviewer_note',
    ],
    'core_coding.csv': ['core_id', 'record_id', 'a_level', 'e_level', 'evidence_object'],
    'screening_summary.csv': ['stage', 'count'],
    'reference_audit.csv': ['record_id', 'canonical_title'],
    'record_classification_audit.csv': [
        'record',
        'citation_id',
        'classification',
        'boundary_case',
        'classification_reason',
        'core_eligibility',
        'evidence_chain_relevance',
        'high_risk_claim_handling',
        'author_note',
    ],
    'v13_synthesis_statistics.csv': [
        'dimension',
        'category',
        'token',
        'count',
        'core_ids',
        'includes_governance_boundary_case',
        'field_type',
        'note',
    ],
    'v13_core_synthesis_matrix.csv': [
        'core_id',
        'system_alias',
        'reference_key',
        'core_type',
        'lifecycle_coverage',
        'agent_capabilities',
        'strongest_evidence_output',
        'external_audit_materials',
        'main_claim_boundary',
    ],
    'v13_benchmark_boundary.csv': [
        'benchmark_or_scenario',
        'task_background',
        'typical_system_output',
        'supported_claim',
        'unsupported_extrapolation',
    ],
    'v13_reproducibility_audit.csv': [
        'audit_dimension',
        'counting_scope',
        'core_count',
        'interpretation',
        'unsupported_extrapolation',
    ],
    'v13_research_agenda_outputs.csv': [
        'observation_basis',
        'unclosed_gap',
        'materials_to_report',
        'structured_output',
        'purpose',
    ],
    'core_reproducibility_audit.csv': [
        'core_id',
        'system_alias',
        'reference_key',
        'core_type',
        'public_artifact_status',
        'target_version_status',
        'environment_status',
        'replay_material_status',
        'structured_trace_status',
        'author_reported_external_trace_status',
        'publicly_traceable_external_material_status',
        'claim_level_alignment_status',
        'zotero_pdf_review_status',
        'review_status',
        'manual_review_required',
    ],
    'core_reproducibility_audit_summary.csv': [
      'audit_dimension',
      'reported_yes',
      'reported_partial',
      'not_found_after_review',
      'unknown_not_audited',
      'restricted_or_sensitive',
      'not_applicable',
      'scope_note',
    ],
    'doi_remaining_manual_status.csv': [
      'reference_key',
      'title',
      'current_source_type',
      'doi_status',
      'evidence',
      'manual_action_required',
      'notes',
    ],
    'core31_second_coder_blind.csv': [
      'core_id',
      'record_id',
      'system_alias',
      'title',
      'publication_status',
      'boundary_role',
      'materials_to_review',
    ],
    'core31_second_coder_formal_blind_template.csv': [
      'core_id',
      'record_id',
      'system_alias',
      'title',
      'publication_status',
      'boundary_role',
      'materials_to_review',
      'coder2_strongest_evidence_output',
      'coder2_decision_reason',
      'coder2_uncertainty_note',
    ],
    'core31_second_coder_formal_results.csv': [
      'core_id',
      'record_id',
      'system_alias',
      'title',
      'publication_status',
      'boundary_role',
      'materials_to_review',
      'coder2_strongest_evidence_output',
      'coder2_decision_reason',
      'coder2_uncertainty_note',
    ],
    'core31_second_coder_capability_traceability_blind_template.csv': [
      'core_id',
      'record_id',
      'system_alias',
      'title',
      'publication_status',
      'boundary_role',
      'materials_to_review',
      'coder2_cross_stage_capability_label',
      'coder2_capability_decision_reason',
      'coder2_capability_uncertainty_note',
      'coder2_external_traceability_label',
      'coder2_external_traceability_decision_reason',
      'coder2_external_traceability_uncertainty_note',
    ],
    'core31_second_coder_capability_traceability_results.csv': [
      'core_id',
      'record_id',
      'system_alias',
      'title',
      'publication_status',
      'boundary_role',
      'materials_to_review',
      'coder2_cross_stage_capability_label',
      'coder2_capability_decision_reason',
      'coder2_capability_uncertainty_note',
      'coder2_external_traceability_label',
      'coder2_external_traceability_decision_reason',
      'coder2_external_traceability_uncertainty_note',
    ],
    'core31_second_coder_adjudication_template.csv': [
      'core_id',
      'record_id',
      'system_alias',
      'title',
      'publication_status',
      'boundary_role',
      'original_strongest_evidence_output',
    ],
    'product_ecosystem_snapshot.csv': [
      'product_or_system',
      'vendor',
      'snapshot_date',
      'model_or_version',
      'public_capabilities',
      'security_workflow',
      'public_evidence_type',
      'source_url',
      'publication_or_update_date',
      'access_date',
      'manuscript_role',
      'core_eligibility',
      'evidence_caveat',
      'external_traceability',
      'update_required',
      'notes',
    ],
    'mapping_snapshot_counts.csv': [
      'view',
      'category',
      'count',
      'denominator',
      'scope_note',
    ],
    'source_search_log.csv': [
      'source_id',
      'source_name',
      'source_category',
      'search_interface',
      'query_string',
      'date_searched',
      'date_range',
      'records_captured_before_dedup',
      'duplicates_or_variants_removed',
      'unique_candidate_records_after_dedup',
      'core_records',
      'supporting_records',
      'background_records',
      'excluded_records',
      'zotero_metadata_used',
      'notes',
    ],
    'source_screening_audit.csv': [
      'record_id',
      'title',
      'year',
      'source_bucket',
      'source_name',
      'source_type',
      'venue_or_source',
      'doi_or_url',
      'corpus_layer',
      'task_category',
      'screening_decision',
      'deduplication_status',
      'source_trace_note',
    ],
}
VALIDATED_CSVS = set()
ERROR_COUNT = 0

def status(kind, ok, msg):
    global ERROR_COUNT
    if not ok:
        ERROR_COUNT += 1
    print(f'{kind if not ok else "PASS"}: {msg}')

def parse_iso_date(value):
    try:
        return date.fromisoformat(value)
    except Exception:
        return None

def load_manifest_product_snapshot_date():
    path = ROOT / 'RELEASE_MANIFEST.md'
    if not path.exists():
        return None
    prefix = '- Product-ecosystem snapshot date:'
    for line in path.read_text(encoding='utf-8').splitlines():
        if line.startswith(prefix):
            return line.split(':', 1)[1].strip()
    return None

def contains_private_material(value):
    lowered = value.lower()
    sensitive_tokens = [
        'c:\\users\\',
        'zotero\\storage',
        '.sqlite',
        '.sqlite-journal',
        'local_private_working',
        'zotero_private_paths',
        'private working directory',
    ]
    return any(token in lowered for token in sensitive_tokens)

def validate_csv_schema(name, reader, rows):
    fieldnames = reader.fieldnames or []
    required = CSV_REQUIRED_FIELDS.get(name, [])
    status('ERROR', bool(fieldnames), f'{name} has a header row')
    missing = [field for field in required if field not in fieldnames]
    status('ERROR', not missing, f'{name} contains required fields: {", ".join(required) if required else "no file-specific required fields"}')
    if missing:
        print(f'ERROR: {name} missing fields:', ', '.join(missing))
    required_non_empty = list(required)
    if name == 'core31_second_coder_formal_blind_template.csv':
        required_non_empty = [field for field in required_non_empty if field not in {
            'coder2_strongest_evidence_output',
            'coder2_decision_reason',
            'coder2_uncertainty_note',
        }]
    if name == 'core31_second_coder_capability_traceability_blind_template.csv':
        required_non_empty = [field for field in required_non_empty if not field.startswith('coder2_')]
    if name == 'submission_update_20260715_full_coding_audit.csv':
        required_non_empty = [field for field in required_non_empty if field != 'uncertainty_note']
    if name == 'submission_update_20260715_second_coder_blind_template.csv':
        required_non_empty = [field for field in required_non_empty if not field.startswith('coder2_')]
    width_errors = []
    required_errors = []
    for idx, row in enumerate(rows, start=2):
        if None in row:
            width_errors.append(idx)
        empty_required = [field for field in required_non_empty if row.get(field, '') == '']
        if empty_required:
            required_errors.append((idx, empty_required))
    status('ERROR', not width_errors, f'{name} has consistent column width for {len(rows)} rows')
    if width_errors:
        print(f'ERROR: {name} column width errors at rows:', ', '.join(map(str, width_errors)))
    status('ERROR', not required_errors, f'{name} required fields are non-empty for {len(rows)} rows')
    if required_errors:
        for idx, fields in required_errors[:10]:
            print(f'ERROR: {name} row {idx} empty required fields:', ', '.join(fields))
        if len(required_errors) > 10:
            print(f'ERROR: {name} additional rows with empty required fields:', len(required_errors) - 10)
    if name == 'record_classification_audit.csv':
        expected = CSV_REQUIRED_FIELDS[name]
        status('ERROR', fieldnames == expected, f'{name} schema matches expected 9 columns')
    VALIDATED_CSVS.add(name)

def validate_all_csv_files():
    for path in sorted(DATA.glob('*.csv')):
        with path.open(encoding='utf-8-sig', newline='') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        validate_csv_schema(path.name, reader, rows)

def read_csv(name):
    path = DATA / name
    if not path.exists():
        print(f'ERROR: missing {name}')
        return []
    with path.open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    if name not in VALIDATED_CSVS:
        validate_csv_schema(name, reader, rows)
    return rows

def expand_a_level(value):
    if not value or value == 'NA':
        return []
    value = value.replace(' ', '')
    if '+' in value:
        expanded = []
        for part in value.split('+'):
            expanded.extend(expand_a_level(part))
        return expanded
    if '--' in value:
        left, right = value.split('--', 1)
        try:
            start = int(left[1:]); end = int(right[1:])
            return [f'A{i}' for i in range(start, end + 1)]
        except Exception:
            return [value]
    if '-' in value and value.count('A') >= 2:
        left, right = value.split('-', 1)
        try:
            start = int(left[1:]); end = int(right[1:])
            return [f'A{i}' for i in range(start, end + 1)]
        except Exception:
            return [value]
    return [value]

def validate_product_ecosystem_snapshot(rows):
    manifest_snapshot_date = load_manifest_product_snapshot_date()
    status('ERROR', bool(rows), 'product_ecosystem_snapshot.csv has at least one row')
    status('ERROR', bool(manifest_snapshot_date), 'RELEASE_MANIFEST.md records product snapshot date')
    if not rows:
        return

    allowed_roles = {'Background', 'Supporting', 'Emerging boundary case', 'Core candidate', 'Excluded'}
    allowed_update_required = {'yes', 'no', 'true', 'false'}
    product_doc_markers = [
        'product',
        'documentation',
        'help',
        'faq',
        'use-case',
        'use case',
        'blog',
        'model',
        'policy',
    ]

    invalid_snapshot_dates = []
    manifest_mismatches = []
    invalid_access_dates = []
    invalid_roles = []
    invalid_update_flags = []
    missing_public_urls = []
    empty_urls = []
    private_material_rows = []
    unconfirmed_core_rows = []

    for idx, row in enumerate(rows, start=2):
        snapshot_value = row.get('snapshot_date', '')
        parsed_snapshot = parse_iso_date(snapshot_value)
        if not parsed_snapshot:
            invalid_snapshot_dates.append(idx)
        if manifest_snapshot_date and snapshot_value != manifest_snapshot_date:
            manifest_mismatches.append(idx)

        access_value = row.get('access_date', '')
        if not parse_iso_date(access_value):
            invalid_access_dates.append(idx)

        role = row.get('manuscript_role', '')
        if role not in allowed_roles:
            invalid_roles.append((idx, role))

        update_required = row.get('update_required', '').strip().lower()
        if update_required not in allowed_update_required:
            invalid_update_flags.append((idx, row.get('update_required', '')))

        source_url = row.get('source_url', '').strip()
        if source_url == '':
            empty_urls.append(idx)
        if role != 'Excluded' and not source_url.startswith(('http://', 'https://')):
            missing_public_urls.append(idx)

        joined = ' '.join(str(v) for v in row.values())
        if contains_private_material(joined):
            private_material_rows.append(idx)

        evidence_type = row.get('public_evidence_type', '').lower()
        core_eligibility = row.get('core_eligibility', '').lower()
        manual_text = ' '.join([
            row.get('core_eligibility', ''),
            row.get('evidence_caveat', ''),
            row.get('notes', ''),
        ]).lower()
        looks_like_product_doc = any(marker in evidence_type for marker in product_doc_markers)
        if looks_like_product_doc and role == 'Core candidate' and 'manual' not in manual_text and 'author' not in manual_text:
            unconfirmed_core_rows.append(idx)
        if looks_like_product_doc and 'not core' not in core_eligibility and role != 'Excluded' and role != 'Core candidate':
            unconfirmed_core_rows.append(idx)

    status('ERROR', not invalid_snapshot_dates, 'product snapshot dates parse as ISO dates')
    if invalid_snapshot_dates:
        print('ERROR: invalid product snapshot date rows:', ', '.join(map(str, invalid_snapshot_dates)))
    status('ERROR', not manifest_mismatches, 'product snapshot dates match RELEASE_MANIFEST.md')
    if manifest_mismatches:
        print('ERROR: product snapshot date mismatch rows:', ', '.join(map(str, manifest_mismatches)))
    status('ERROR', not invalid_access_dates, 'product access dates parse as ISO dates')
    if invalid_access_dates:
        print('ERROR: invalid product access date rows:', ', '.join(map(str, invalid_access_dates)))
    status('ERROR', not invalid_roles, 'product manuscript_role values use the approved enumeration')
    if invalid_roles:
        print('ERROR: invalid product manuscript_role rows:', invalid_roles[:10])
    status('ERROR', not invalid_update_flags, 'product update_required values are parseable booleans')
    if invalid_update_flags:
        print('ERROR: invalid update_required rows:', invalid_update_flags[:10])
    status('ERROR', not empty_urls, 'product source_url values are non-empty')
    if empty_urls:
        print('ERROR: empty product source_url rows:', ', '.join(map(str, empty_urls)))
    status('ERROR', not missing_public_urls, 'non-Excluded product rows have public source URLs')
    if missing_public_urls:
        print('ERROR: non-Excluded product rows missing public URLs:', ', '.join(map(str, missing_public_urls)))
    status('ERROR', not private_material_rows, 'product snapshot contains no local Zotero/PDF/SQLite/private path material')
    if private_material_rows:
        print('ERROR: product private-material rows:', ', '.join(map(str, private_material_rows)))
    status('ERROR', not unconfirmed_core_rows, 'product/vendor documentation is not promoted to Core without manual confirmation')
    if unconfirmed_core_rows:
        print('ERROR: product Core-eligibility rows needing review:', ', '.join(map(str, sorted(set(unconfirmed_core_rows)))))
    print(f'product_ecosystem_snapshot.csv rows: {len(rows)}')


def cohen_kappa(first, second):
    if not first or len(first) != len(second):
        return None
    total = len(first)
    observed = sum(1 for a, b in zip(first, second) if a == b) / total
    first_counts = Counter(first)
    second_counts = Counter(second)
    categories = set(first_counts) | set(second_counts)
    expected = sum((first_counts[c] / total) * (second_counts[c] / total) for c in categories)
    if expected == 1:
        return 1.0 if observed == 1 else None
    return (observed - expected) / (1 - expected)

def split_multilabel(value):
    if not value:
        return set()
    return {item.strip() for item in value.replace('；', ';').split(';') if item.strip()}

def set_agreement_metrics(baseline_rows, coder_rows, baseline_field, coder_field):
    baseline_by_id = {row.get('core_id', ''): row for row in baseline_rows}
    compared = []
    missing = []
    for row in coder_rows:
        core_id = row.get('core_id', '')
        if core_id not in baseline_by_id:
            missing.append(core_id or '?')
            continue
        base_set = split_multilabel(baseline_by_id[core_id].get(baseline_field, ''))
        coder_set = split_multilabel(row.get(coder_field, ''))
        compared.append((core_id, row.get('system_alias', ''), base_set, coder_set))

    if not compared:
        return {
            'missing': missing,
            'rows': 0,
            'exact': 0,
            'row_exact': 0,
            'mean_jaccard': 0,
            'micro_precision': 0,
            'micro_recall': 0,
            'micro_f1': 0,
            'per_label': [],
            'disagreements': [],
        }

    exact = 0
    jaccards = []
    tp = fp = fn = 0
    disagreements = []
    all_labels = set()
    for core_id, system_alias, base_set, coder_set in compared:
        all_labels.update(base_set)
        all_labels.update(coder_set)
        if base_set == coder_set:
            exact += 1
        else:
            disagreements.append((core_id, system_alias, base_set, coder_set))
        union = base_set | coder_set
        intersection = base_set & coder_set
        jaccards.append(1.0 if not union else len(intersection) / len(union))
        tp += len(intersection)
        fp += len(coder_set - base_set)
        fn += len(base_set - coder_set)

    per_label = []
    core_ids = [core_id for core_id, *_ in compared]
    for label in sorted(all_labels):
        baseline_positive = {core_id for core_id, _, base_set, _ in compared if label in base_set}
        coder_positive = {core_id for core_id, _, _, coder_set in compared if label in coder_set}
        label_tp = len(baseline_positive & coder_positive)
        label_fp = len(coder_positive - baseline_positive)
        label_fn = len(baseline_positive - coder_positive)
        label_tn = len(core_ids) - label_tp - label_fp - label_fn
        label_union = baseline_positive | coder_positive
        per_label.append({
            'label': label,
            'baseline_rows': len(baseline_positive),
            'coder2_rows': len(coder_positive),
            'agreement': (label_tp + label_tn) / len(core_ids),
            'jaccard': 1.0 if not label_union else label_tp / len(label_union),
        })

    precision = 1.0 if (tp + fp) == 0 else tp / (tp + fp)
    recall = 1.0 if (tp + fn) == 0 else tp / (tp + fn)
    f1 = 1.0 if (precision + recall) == 0 else 2 * precision * recall / (precision + recall)
    return {
        'missing': missing,
        'rows': len(compared),
        'exact': exact,
        'row_exact': exact / len(compared),
        'mean_jaccard': sum(jaccards) / len(jaccards),
        'micro_precision': precision,
        'micro_recall': recall,
        'micro_f1': f1,
        'per_label': per_label,
        'disagreements': disagreements,
    }

def validate_formal_agreement_report(formal_results_rows, adjudication_rows, allowed_outputs):
    report_path = REPORTS / 'FORMAL_SECOND_CODER_AGREEMENT_REPORT.md'
    status('ERROR', report_path.exists(), 'formal second-coder agreement report exists')
    if not formal_results_rows or not adjudication_rows:
        return

    baseline_by_id = {row.get('core_id', ''): row for row in adjudication_rows}
    missing_baselines = [row.get('core_id', '?') for row in formal_results_rows if row.get('core_id', '') not in baseline_by_id]
    status('ERROR', not missing_baselines, 'formal results rows all have adjudication-template baselines')
    if missing_baselines:
        print('ERROR: formal results missing baselines:', ', '.join(missing_baselines))
        return

    baseline = []
    coder2 = []
    disagreements = []
    for row in formal_results_rows:
        core_id = row.get('core_id', '')
        base_label = baseline_by_id[core_id].get('original_strongest_evidence_output', '').strip()
        coder_label = row.get('coder2_strongest_evidence_output', '').strip()
        baseline.append(base_label)
        coder2.append(coder_label)
        if base_label != coder_label:
            disagreements.append((core_id, row.get('system_alias', ''), base_label, coder_label))

    rows_compared = len(formal_results_rows)
    agreements = sum(1 for a, b in zip(baseline, coder2) if a == b)
    raw_agreement = agreements / rows_compared if rows_compared else 0
    kappa = cohen_kappa(baseline, coder2)
    status('ERROR', all(label in allowed_outputs for label in baseline), 'formal agreement baseline labels use approved values')
    status('ERROR', all(label in allowed_outputs for label in coder2), 'formal agreement coder2 labels use approved values')

    expected_disagreements = {'C12', 'C17', 'C24'}
    actual_disagreements = {core_id for core_id, *_ in disagreements}
    status('ERROR', rows_compared == 31, f'formal agreement rows compared = {rows_compared}; expected 31')
    status('ERROR', len(disagreements) == 3, f'formal agreement disagreements = {len(disagreements)}; expected 3')
    status('ERROR', actual_disagreements == expected_disagreements, 'formal disagreement rows are C12, C17, and C24')
    if actual_disagreements != expected_disagreements:
        print('ERROR: formal disagreement rows:', ', '.join(sorted(actual_disagreements)))
    print(f'FORMAL_SECOND_CODER_AGREEMENT: rows={rows_compared} raw={raw_agreement:.3f} kappa={kappa:.3f} disagreements={len(disagreements)}')

    if report_path.exists():
        report_text = report_path.read_text(encoding='utf-8')
        required_snippets = [
            f'Rows compared: {rows_compared}',
            f'Raw agreement: {raw_agreement:.3f}',
            f"Cohen's kappa: {kappa:.3f}",
            f'Disagreements: {len(disagreements)}',
            'formal pre-adjudication agreement',
            'No adjudicated labels are claimed',
        ]
        missing_snippets = [snippet for snippet in required_snippets if snippet not in report_text]
        missing_disagreement_ids = [core_id for core_id, *_ in disagreements if core_id not in report_text]
        status('ERROR', not missing_snippets, 'formal report contains computed raw agreement, kappa, and pre-adjudication note')
        if missing_snippets:
            print('ERROR: formal report missing snippets:', '; '.join(missing_snippets))
        status('ERROR', not missing_disagreement_ids, 'formal report lists computed disagreement rows')
        if missing_disagreement_ids:
            print('ERROR: formal report missing disagreement rows:', ', '.join(missing_disagreement_ids))


def validate_second_coder_files(blind_rows, adjudication_rows, formal_rows=None, formal_results_rows=None):
    formal_rows = formal_rows or []
    formal_results_rows = formal_results_rows or []
    blind_path = DATA / 'core31_second_coder_blind.csv'
    formal_path = DATA / 'core31_second_coder_formal_blind_template.csv'
    formal_results_path = DATA / 'core31_second_coder_formal_results.csv'
    adjudication_path = DATA / 'core31_second_coder_adjudication_template.csv'
    pilot_dir = ROOT / 'archive' / 'pilot_second_coder_round_1'
    pilot_report = pilot_dir / 'SECOND_CODER_AGREEMENT_REPORT.md'
    pilot_results = pilot_dir / 'core31_second_coder_results.csv'
    status('ERROR', blind_path.exists(), 'core31_second_coder_blind.csv exists')
    status('ERROR', formal_path.exists(), 'core31_second_coder_formal_blind_template.csv exists')
    status('ERROR', formal_results_path.exists(), 'core31_second_coder_formal_results.csv exists')
    status('ERROR', adjudication_path.exists(), 'core31_second_coder_adjudication_template.csv exists')
    if not blind_rows:
        return

    allowed_outputs = {
        'candidate judgment',
        'controlled task completion',
        'runtime safety signal',
        'reproducible validation',
        'externally traceable material',
        'claim-level audit material',
        'governance boundary case',
    }
    allowed_boundary_roles = {'standard_core_entry', 'governance_boundary_case'}
    coder2_fields = [
        'coder2_strongest_evidence_output',
        'coder2_decision_reason',
        'coder2_uncertainty_note',
    ]

    def check_blind_like(rows, label, require_blank=True):
        fields = set(rows[0].keys()) if rows else set()
        required = {
            'core_id',
            'record_id',
            'system_alias',
            'title',
            'publication_status',
            'boundary_role',
            'materials_to_review',
            *coder2_fields,
        }
        missing = sorted(required - fields)
        original_fields = sorted(field for field in fields if field.startswith('original_'))
        status('ERROR', len(rows) == 31, f'{label} rows = {len(rows)}; expected 31')
        status('ERROR', not missing, f'{label} contains required fields')
        if missing:
            print(f'ERROR: {label} missing fields:', ', '.join(missing))
        status('ERROR', not original_fields, f'{label} contains no original_* answer-key columns')
        if original_fields:
            print(f'ERROR: {label} exposes original fields:', ', '.join(original_fields))
        boundary_roles = sorted(set(row.get('boundary_role', '').strip() for row in rows))
        invalid_boundary_roles = [role for role in boundary_roles if role not in allowed_boundary_roles]
        status('ERROR', not invalid_boundary_roles, f'{label} boundary_role values use approved labels')
        if invalid_boundary_roles:
            print(f'ERROR: invalid {label} boundary_role values:', ', '.join(invalid_boundary_roles))
        if require_blank:
            filled = []
            for row in rows:
                for field in coder2_fields:
                    if row.get(field, '').strip():
                        filled.append((row.get('core_id', '?'), field))
            status('ERROR', not filled, f'{label} coder2 fields are blank for formal rerun')
            if filled:
                print(f'ERROR: {label} nonblank coder2 fields:', filled[:10])

    check_blind_like(blind_rows, 'core31_second_coder_blind.csv', require_blank=True)
    if formal_rows:
        check_blind_like(formal_rows, 'core31_second_coder_formal_blind_template.csv', require_blank=True)

    if formal_results_rows:
        check_blind_like(formal_results_rows, 'core31_second_coder_formal_results.csv', require_blank=False)
        missing_formal_values = []
        invalid_formal_values = []
        for row in formal_results_rows:
            for field in coder2_fields:
                if not row.get(field, '').strip():
                    missing_formal_values.append((row.get('core_id', '?'), field))
            label = row.get('coder2_strongest_evidence_output', '').strip()
            if label and label not in allowed_outputs:
                invalid_formal_values.append((row.get('core_id', '?'), label))
        status('ERROR', not missing_formal_values, 'formal results coder2 labels, rationale, and uncertainty notes are populated')
        if missing_formal_values:
            print('ERROR: missing formal results fields:', missing_formal_values[:10])
        status('ERROR', not invalid_formal_values, 'formal results coder2 labels use approved evidence-output labels')
        if invalid_formal_values:
            print('ERROR: invalid formal results labels:', invalid_formal_values[:10])

    adjudication_fields = set(adjudication_rows[0].keys()) if adjudication_rows else set()
    required_adjudication_fields = {
        'boundary_role',
        'original_strongest_evidence_output',
        'coder2_strongest_evidence_output',
        'coder2_decision_reason',
        'coder2_uncertainty_note',
    }
    missing_adjudication_fields = sorted(required_adjudication_fields - adjudication_fields)
    status('ERROR', not missing_adjudication_fields, 'adjudication template contains current second-coder workflow fields')
    if missing_adjudication_fields:
        print('ERROR: adjudication template missing fields:', ', '.join(missing_adjudication_fields))
    if adjudication_rows:
        baseline_values = [row.get('original_strongest_evidence_output', '').strip() for row in adjudication_rows]
        invalid_baselines = sorted(set(value for value in baseline_values if value not in allowed_outputs))
        missing_baselines = [row.get('core_id', '?') for row in adjudication_rows if not row.get('original_strongest_evidence_output', '').strip()]
        status('ERROR', not missing_baselines, 'adjudication template original_strongest_evidence_output is populated for all rows')
        if missing_baselines:
            print('ERROR: missing original_strongest_evidence_output for:', ', '.join(missing_baselines))
        status('ERROR', not invalid_baselines, 'adjudication template original_strongest_evidence_output values use approved labels')
        if invalid_baselines:
            print('ERROR: invalid original_strongest_evidence_output labels:', ', '.join(invalid_baselines))
        status('ERROR', any(field.startswith('original_') for field in adjudication_fields), 'adjudication template retains original_* fields for post-coding comparison')
        adjudication_boundary_roles = sorted(set(row.get('boundary_role', '').strip() for row in adjudication_rows))
        invalid_adjudication_boundary_roles = [role for role in adjudication_boundary_roles if role not in allowed_boundary_roles]
        status('ERROR', not invalid_adjudication_boundary_roles, 'adjudication template boundary_role values use approved labels')
        if invalid_adjudication_boundary_roles:
            print('ERROR: invalid adjudication boundary_role values:', ', '.join(invalid_adjudication_boundary_roles))
        status('ERROR', len(adjudication_rows) == 31, f'core31_second_coder_adjudication_template.csv rows = {len(adjudication_rows)}; expected 31')
        formal_filled = []
        for row in adjudication_rows:
            for field in coder2_fields + ['disagreement_note', 'adjudication_result']:
                if row.get(field, '').strip():
                    formal_filled.append((row.get('core_id', '?'), field))
        status('ERROR', not formal_filled, 'adjudication template coder2/adjudication fields remain blank until adjudication is explicitly recorded')
        if formal_filled:
            print('ERROR: nonblank formal adjudication fields:', formal_filled[:10])

    validate_formal_agreement_report(formal_results_rows, adjudication_rows, allowed_outputs)

    status('ERROR', pilot_dir.exists(), 'pilot second-coder calibration archive exists')
    status('ERROR', pilot_report.exists(), 'pilot agreement report is archived outside the formal report path')
    status('ERROR', pilot_results.exists(), 'pilot coder2 results are archived outside the formal data path')
    pilot_readme = pilot_dir / 'README.md'
    status('ERROR', pilot_readme.exists(), 'pilot archive README exists')
    if pilot_readme.exists():
        archive_text = pilot_readme.read_text(encoding='utf-8')
        status('ERROR', 'formal intercoder reliability' in archive_text and 'should not be cited' in archive_text, 'pilot archive warns against formal reliability citation')
    print('PILOT_SECOND_CODER_ARCHIVE: archived for calibration only; formal reliability uses data/core31_second_coder_formal_results.csv and reports/FORMAL_SECOND_CODER_AGREEMENT_REPORT.md')


def validate_second_coder_extension_template(rows, results_rows, baseline_rows):
    path = DATA / 'core31_second_coder_capability_traceability_blind_template.csv'
    results_path = DATA / 'core31_second_coder_capability_traceability_results.csv'
    report_path = REPORTS / 'SECOND_CODER_CAPABILITY_TRACEABILITY_AGREEMENT_REPORT.md'
    status('ERROR', path.exists(), 'capability/traceability second-coder blind template exists')
    status('ERROR', results_path.exists(), 'capability/traceability second-coder formal results file exists')
    status('ERROR', report_path.exists(), 'capability/traceability second-coder agreement report exists')
    if not rows:
        return

    fields = set(rows[0].keys())
    original_fields = sorted(field for field in fields if field.startswith('original_'))
    coder2_fields = [field for field in fields if field.startswith('coder2_')]
    status('ERROR', len(rows) == 31, f'capability/traceability blind template rows = {len(rows)}; expected 31')
    status('ERROR', not original_fields, 'capability/traceability blind template exposes no original_* answer-key columns')
    if original_fields:
        print('ERROR: exposed original fields:', ', '.join(original_fields))
    filled = []
    for row in rows:
        for field in coder2_fields:
            if row.get(field, '').strip():
                filled.append((row.get('core_id', '?'), field))
    status('ERROR', not filled, 'capability/traceability blind template coder2 fields remain blank for future reruns')
    if filled:
        print('ERROR: nonblank capability/traceability coder2 template fields:', filled[:10])

    def check_extension_materials(material_rows, label):
        forbidden = []
        missing_scope = []
        for row in material_rows:
            material = row.get('materials_to_review', '')
            lower = material.lower()
            if 'strongest evidence output' in lower:
                forbidden.append(row.get('core_id', '?'))
            has_capability = 'cross-stage capability labels' in lower or 'capability definitions' in lower
            has_traceability = 'external traceability' in lower or 'external-audit-material' in lower or 'external audit material' in lower
            if not (has_capability and has_traceability):
                missing_scope.append(row.get('core_id', '?'))
        status('ERROR', not forbidden, f'{label} materials_to_review does not mention strongest evidence output')
        if forbidden:
            print(f'ERROR: {label} rows with strongest evidence output wording:', ', '.join(forbidden[:20]))
        status('ERROR', not missing_scope, f'{label} materials_to_review describes cross-stage capability labels and external traceability')
        if missing_scope:
            print(f'ERROR: {label} rows missing capability/traceability scope wording:', ', '.join(missing_scope[:20]))

    check_extension_materials(rows, 'capability/traceability blind template')

    if not results_rows or not baseline_rows:
        return

    check_extension_materials(results_rows, 'capability/traceability results')

    result_fields = set(results_rows[0].keys())
    result_original_fields = sorted(field for field in result_fields if field.startswith('original_'))
    required_result_fields = {
        'coder2_cross_stage_capability_label',
        'coder2_capability_decision_reason',
        'coder2_capability_uncertainty_note',
        'coder2_external_traceability_label',
        'coder2_external_traceability_decision_reason',
        'coder2_external_traceability_uncertainty_note',
    }
    status('ERROR', len(results_rows) == 31, f'capability/traceability results rows = {len(results_rows)}; expected 31')
    status('ERROR', not result_original_fields, 'capability/traceability results expose no original_* answer-key columns')
    if result_original_fields:
        print('ERROR: capability/traceability result original fields:', ', '.join(result_original_fields))
    missing_values = []
    for row in results_rows:
        for field in required_result_fields:
            if not row.get(field, '').strip():
                missing_values.append((row.get('core_id', '?'), field))
    status('ERROR', not missing_values, 'capability/traceability results coder2 labels, rationales, and uncertainty notes are populated')
    if missing_values:
        print('ERROR: missing capability/traceability result values:', missing_values[:10])

    baseline_fields = set(baseline_rows[0].keys()) if baseline_rows else set()
    status('ERROR', {'agent_capabilities', 'external_audit_materials'} <= baseline_fields, 'Core synthesis matrix contains capability and external-audit baseline fields')
    cap = set_agreement_metrics(baseline_rows, results_rows, 'agent_capabilities', 'coder2_cross_stage_capability_label')
    ext = set_agreement_metrics(baseline_rows, results_rows, 'external_audit_materials', 'coder2_external_traceability_label')
    status('ERROR', not cap['missing'], 'capability results rows all have Core synthesis baselines')
    status('ERROR', not ext['missing'], 'external-traceability results rows all have Core synthesis baselines')
    status('ERROR', cap['rows'] == 31, f'capability agreement rows compared = {cap["rows"]}; expected 31')
    status('ERROR', ext['rows'] == 31, f'external-traceability agreement rows compared = {ext["rows"]}; expected 31')
    print(f'CAPABILITY_SECOND_CODER_AGREEMENT: rows={cap["rows"]} exact={cap["row_exact"]:.3f} mean_jaccard={cap["mean_jaccard"]:.3f} micro_f1={cap["micro_f1"]:.3f} disagreements={len(cap["disagreements"])}')
    print(f'EXTERNAL_TRACEABILITY_SECOND_CODER_AGREEMENT: rows={ext["rows"]} exact={ext["row_exact"]:.3f} mean_jaccard={ext["mean_jaccard"]:.3f} micro_f1={ext["micro_f1"]:.3f} disagreements={len(ext["disagreements"])}')

    if report_path.exists():
        report_text = report_path.read_text(encoding='utf-8')
        required_snippets = [
            f'Rows compared: {cap["rows"]}',
            f'Row-level exact agreement: {cap["exact"]} / {cap["rows"]} = {cap["row_exact"]:.3f}',
            f'Mean row Jaccard: {cap["mean_jaccard"]:.3f}',
            f'Rows compared: {ext["rows"]}',
            f'Row-level exact agreement: {ext["exact"]} / {ext["rows"]} = {ext["row_exact"]:.3f}',
            f'Mean row Jaccard: {ext["mean_jaccard"]:.3f}',
            'does not use single-label Cohen',
            'no adjudicated labels are claimed',
        ]
        missing_snippets = [snippet for snippet in required_snippets if snippet not in report_text]
        status('ERROR', not missing_snippets, 'capability/traceability report contains computed Jaccard/per-label agreement and boundary notes')
        if missing_snippets:
            print('ERROR: capability/traceability report missing snippets:', '; '.join(missing_snippets))
        missing_labels = [item['label'] for item in cap['per_label'] + ext['per_label'] if item['label'] not in report_text]
        status('ERROR', not missing_labels, 'capability/traceability report lists computed per-label rows')
        if missing_labels:
            print('ERROR: capability/traceability report missing labels:', ', '.join(sorted(set(missing_labels))))

def validate_source_search_audit(corpus, source_log, source_audit):
    status('ERROR', bool(source_log), 'source_search_log.csv has at least one source row')
    status('ERROR', bool(source_audit), 'source_screening_audit.csv has at least one record row')
    if not corpus or not source_log or not source_audit:
        return

    corpus_ids = {row.get('record_id', '') for row in corpus}
    audit_ids = [row.get('record_id', '') for row in source_audit]
    status('ERROR', len(source_audit) == 253, f'source_screening_audit rows = {len(source_audit)}; expected 253')
    status('ERROR', set(audit_ids) == corpus_ids, 'source_screening_audit covers exactly the corpus record_ids')
    status('ERROR', len(audit_ids) == len(set(audit_ids)), 'source_screening_audit record_id values are unique')

    audit_layer_counts = Counter(row.get('corpus_layer', 'NA') for row in source_audit)
    expected_layers = {'Core': 68, 'Supporting': 69, 'Background': 95, 'Excluded': 21}
    for layer, expected in expected_layers.items():
        status('ERROR', audit_layer_counts.get(layer, 0) == expected, f'source_screening_audit {layer} = {audit_layer_counts.get(layer, 0)}; expected {expected}')

    def to_int(row, field):
        try:
            return int(row.get(field, '0'))
        except Exception:
            return -999999

    totals = {
        'captured': sum(to_int(row, 'records_captured_before_dedup') for row in source_log),
        'variants_removed': sum(to_int(row, 'duplicates_or_variants_removed') for row in source_log),
        'unique': sum(to_int(row, 'unique_candidate_records_after_dedup') for row in source_log),
        'core': sum(to_int(row, 'core_records') for row in source_log),
        'supporting': sum(to_int(row, 'supporting_records') for row in source_log),
        'background': sum(to_int(row, 'background_records') for row in source_log),
        'excluded': sum(to_int(row, 'excluded_records') for row in source_log),
    }
    status('ERROR', totals['captured'] == 253, f'source_search_log source records = {totals["captured"]}; expected 253')
    status('ERROR', totals['variants_removed'] == 5, f'source_search_log source variants removed from canonical counts = {totals["variants_removed"]}; expected 5')
    status('ERROR', totals['unique'] == 248, f'source_search_log canonical candidate studies = {totals["unique"]}; expected 248')
    status('ERROR', totals['core'] == 68, f'source_search_log study-level coded records = {totals["core"]}; expected 68')
    status('ERROR', totals['supporting'] == 65, f'source_search_log extended synthesis studies = {totals["supporting"]}; expected 65')
    status('ERROR', totals['background'] == 95, f'source_search_log Background records = {totals["background"]}; expected 95')
    status('ERROR', totals['excluded'] == 20, f'source_search_log canonical Excluded records = {totals["excluded"]}; expected 20')

    missing_trace = [row.get('record_id', '?') for row in source_audit if row.get('source_bucket', '') in ('', 'NA') or row.get('source_name', '') in ('', 'NA')]
    status('ERROR', not missing_trace, 'all source_screening_audit rows include a source bucket and source name')
    if missing_trace:
        print('ERROR: source rows missing source bucket/name:', ', '.join(missing_trace[:20]))

    volatile_hit_claims = [
        row.get('source_id', '?') for row in source_log
        if 'source records from canonical study counts' not in row.get('notes', '') and 'source records' not in row.get('notes', '')
    ]
    status('ERROR', not volatile_hit_claims, 'source_search_log notes distinguish source records from canonical study counts')



def norm_text(value):
    value = (value or '').lower().replace('’', "'")
    return re.sub(r'[^a-z0-9]+', ' ', value).strip()

def normalize_locator(value):
    return (value or '').strip().lower().rstrip('/')

def arxiv_from_text(value):
    match = re.search(r'(\d{4}\.\d{4,5})(v\d+)?', value or '', re.IGNORECASE)
    return match.group(1).lower() if match else ''

def validate_study_version_crosswalk(corpus, ref, crosswalk, mapping_rows):
    status('ERROR', bool(crosswalk), 'study_version_crosswalk.csv has at least one row')
    if not corpus or not crosswalk:
        return
    corpus_ids = {row.get('record_id', '') for row in corpus}
    cross_ids = {row.get('record_id', '') for row in crosswalk}
    status('ERROR', cross_ids == corpus_ids, 'study_version_crosswalk covers exactly the 253 source records')
    status('ERROR', len(crosswalk) == 253, f'study_version_crosswalk rows = {len(crosswalk)}; expected 253')

    allowed_status = {'canonical_counted', 'alternate_version_not_counted', 'exact_duplicate_removed', 'source_variant_not_counted', 'needs_manual_review'}
    allowed_layers = {'study_level_coded', 'extended_synthesis', 'background_reference', 'excluded_near_neighbor', 'alternate_version', 'needs_manual_review'}
    allowed_version = {'preprint', 'conference_version', 'journal_version', 'project_report', 'exact_duplicate', 'other'}
    invalid = []
    for row in crosswalk:
        if row.get('counting_status') not in allowed_status:
            invalid.append((row.get('record_id'), 'counting_status', row.get('counting_status')))
        if row.get('analytical_layer') not in allowed_layers:
            invalid.append((row.get('record_id'), 'analytical_layer', row.get('analytical_layer')))
        if row.get('version_type') not in allowed_version:
            invalid.append((row.get('record_id'), 'version_type', row.get('version_type')))
    status('ERROR', not invalid, 'study_version_crosswalk uses approved status/layer/version vocabularies')
    if invalid:
        print('ERROR: invalid crosswalk values:', invalid[:10])

    counted = [row for row in crosswalk if row.get('counting_status') == 'canonical_counted']
    status('ERROR', len(counted) == 248, f'canonical counted studies = {len(counted)}; expected 248')
    layer_counts = Counter(row.get('analytical_layer') for row in counted)
    expected_layers = {
        'study_level_coded': 68,
        'extended_synthesis': 65,
        'background_reference': 95,
        'excluded_near_neighbor': 20,
    }
    for layer, expected in expected_layers.items():
        status('ERROR', layer_counts.get(layer, 0) == expected, f'canonical {layer} = {layer_counts.get(layer, 0)}; expected {expected}')
    alt_count = sum(1 for row in crosswalk if row.get('counting_status') != 'canonical_counted')
    status('ERROR', alt_count == 5, f'non-counted alternate/source-variant records = {alt_count}; expected 5')

    layers_by_study = defaultdict(set)
    counted_records_by_study = defaultdict(list)
    for row in crosswalk:
        sid = row.get('canonical_study_id')
        if row.get('counting_status') == 'canonical_counted':
            layers_by_study[sid].add(row.get('analytical_layer'))
            counted_records_by_study[sid].append(row.get('record_id'))
    multi_layer = {sid: layers for sid, layers in layers_by_study.items() if len(layers) > 1}
    multi_counted = {sid: ids for sid, ids in counted_records_by_study.items() if len(ids) > 1}
    status('ERROR', not multi_layer, 'each canonical study has one primary analytical layer')
    status('ERROR', not multi_counted, 'each canonical study has one counted record')
    if multi_layer:
        print('ERROR: canonical studies with multiple layers:', dict(list(multi_layer.items())[:10]))
    if multi_counted:
        print('ERROR: canonical studies with multiple counted records:', dict(list(multi_counted.items())[:10]))

    # duplicate keys among counted records
    ref_by_id = {row.get('record_id'): row for row in ref}
    corpus_by_id = {row.get('record_id'): row for row in corpus}
    def key_values(record_id):
        ref_row = ref_by_id.get(record_id, {})
        corpus_row = corpus_by_id.get(record_id, {})
        title = norm_text(ref_row.get('canonical_title') or corpus_row.get('title'))
        doi = normalize_locator(ref_row.get('doi'))
        if doi in {'', 'na', 'n/a'}:
            doi = normalize_locator(corpus_row.get('doi_or_url')) if 'doi.org' in corpus_row.get('doi_or_url', '').lower() else ''
        arxiv = normalize_locator(ref_row.get('arxiv_id'))
        if arxiv in {'', 'na', 'n/a'}:
            arxiv = arxiv_from_text((ref_row.get('official_url','') + ' ' + corpus_row.get('doi_or_url','')))
        url = normalize_locator(ref_row.get('official_url') or corpus_row.get('doi_or_url'))
        if url.startswith('#'):
            url = ''
        return title, doi, arxiv, url
    for label, idx in [('normalized title',0), ('DOI',1), ('arXiv ID',2), ('URL',3)]:
        groups = defaultdict(list)
        for row in counted:
            vals = key_values(row.get('record_id'))
            v = vals[idx]
            if v and v not in {'na','n/a'}:
                groups[v].append(row.get('record_id'))
        dup = {k:v for k,v in groups.items() if len(v)>1}
        status('ERROR', not dup, f'no duplicate counted records by {label}')
        if dup:
            print(f'ERROR: duplicate counted {label} groups:', dict(list(dup.items())[:10]))

    final_rows = [row for row in mapping_rows if row.get('view') == 'final_canonical_stratification']
    final_total = sum(int(row.get('count', '0')) for row in final_rows)
    status('ERROR', final_total == 248, f'mapping final canonical stratification total = {final_total}; expected 248')
    print('CANONICAL_STUDY_COUNTS: ' + str(dict(sorted(layer_counts.items()))))

def validate_extended_synthesis_audit(corpus, extended, crosswalk):
    status('ERROR', bool(extended), 'extended_synthesis_audit.csv has at least one row')
    if not corpus or not extended or not crosswalk:
        return
    counted_extended_ids = {row.get('record_id', '') for row in crosswalk if row.get('counting_status') == 'canonical_counted' and row.get('analytical_layer') == 'extended_synthesis'}
    study_level_canonical_ids = {row.get('canonical_study_id', '') for row in crosswalk if row.get('counting_status') == 'canonical_counted' and row.get('analytical_layer') == 'study_level_coded'}
    cross_by_record = {row.get('record_id'): row for row in crosswalk}
    extended_ids = {row.get('record_id', '') for row in extended}
    status('ERROR', len(extended) == 65, f'extended_synthesis_audit rows = {len(extended)}; expected 65')
    status('ERROR', extended_ids == counted_extended_ids, 'extended synthesis audit covers exactly canonical counted extended synthesis studies')
    overlap = [rid for rid in extended_ids if cross_by_record.get(rid, {}).get('canonical_study_id') in study_level_canonical_ids]
    status('ERROR', not overlap, 'extended_synthesis_audit contains no study-level coded study alternate versions')
    if overlap:
        print('ERROR: extended synthesis rows overlapping study-level canonical studies:', ', '.join(overlap[:20]))

    allowed_roles = {
        'lower_level_primitive',
        'adjacent_candidate_analysis',
        'adjacent_fuzzing_or_testing',
        'benchmark_or_evaluation',
        'agent_orchestration',
        'governance_or_safety',
        'evidence_or_reproducibility',
    }
    allowed_rq = {'RQ1', 'RQ2_context', 'evaluation_agenda', 'governance_agenda'}
    invalid_roles = []
    invalid_secondary = []
    invalid_rq = []
    generic_contrib = []
    generic_reason = []
    invalid_locator = []
    contribution_counter = Counter()
    reason_counter = Counter()
    unresolved = []
    for idx, row in enumerate(extended, start=2):
        rid = row.get('record_id', '?')
        role = row.get('primary_synthesis_role', '')
        if role not in allowed_roles:
            invalid_roles.append((idx, rid, role))
        secondary = row.get('secondary_synthesis_roles', '')
        if secondary and secondary != 'NA':
            for item in secondary.split(';'):
                if item and item not in allowed_roles:
                    invalid_secondary.append((idx, rid, item))
        rq = row.get('rq_contribution', '')
        if rq not in allowed_rq:
            invalid_rq.append((idx, rid, rq))
        contrib = row.get('extracted_contribution', '').strip()
        reason = row.get('reason_not_study_level_coded', '').strip()
        contribution_counter[contrib] += 1
        reason_counter[reason] += 1
        title_tokens = {tok for tok in norm_text(row.get('title','')).split() if len(tok) >= 5}
        contrib_tokens = set(norm_text(contrib).split())
        if contrib.lower() in ('', 'provides context', 'context') or len(title_tokens & contrib_tokens) < 1:
            generic_contrib.append((idx, rid))
        if 'Existing screening classified this record as Supporting' in reason or len(reason) < 40:
            generic_reason.append((idx, rid))
        basis = row.get('public_material_basis', '')
        if '#item_' in basis or not re.search(r'(https?://|10\.\d{4,9}/|isbn|official)', basis, re.IGNORECASE):
            invalid_locator.append((idx, rid, basis[:80]))
        if 'manual_review' in row.get('reviewer_note','').lower() or 'needs_manual_review' in row.get('reviewer_note','').lower():
            unresolved.append(rid)
    duplicate_contribs = {k:v for k,v in contribution_counter.items() if v > 1}
    duplicate_reasons = {k:v for k,v in reason_counter.items() if v > 1}
    unique_ratio = len(contribution_counter) / len(extended) if extended else 0
    status('ERROR', not invalid_roles, 'extended synthesis primary roles use approved vocabulary')
    status('ERROR', not invalid_secondary, 'extended synthesis secondary roles use approved vocabulary')
    status('ERROR', not invalid_rq, 'extended synthesis rq_contribution uses approved vocabulary')
    status('ERROR', not generic_contrib, 'extended synthesis extracted_contribution values contain study-specific terms')
    status('ERROR', not duplicate_contribs, 'extended synthesis extracted_contribution values are unique')
    status('ERROR', not generic_reason, 'extended synthesis reason_not_study_level_coded values are study-specific')
    status('ERROR', not duplicate_reasons, 'extended synthesis reason_not_study_level_coded values are unique')
    status('ERROR', unique_ratio >= 0.95, f'extended synthesis unique contribution ratio = {unique_ratio:.3f}; expected >= 0.950')
    status('ERROR', not invalid_locator, 'extended synthesis public_material_basis contains public URL, DOI, ISBN, or official source and no local fragments')
    if invalid_roles: print('ERROR: invalid extended synthesis roles:', invalid_roles[:10])
    if invalid_secondary: print('ERROR: invalid secondary roles:', invalid_secondary[:10])
    if invalid_rq: print('ERROR: invalid RQ values:', invalid_rq[:10])
    if generic_contrib: print('ERROR: generic contribution rows:', generic_contrib[:10])
    if duplicate_contribs: print('ERROR: duplicate contribution groups:', list(duplicate_contribs.items())[:5])
    if generic_reason: print('ERROR: generic reason rows:', generic_reason[:10])
    if duplicate_reasons: print('ERROR: duplicate reason groups:', list(duplicate_reasons.items())[:5])
    if invalid_locator: print('ERROR: invalid locator rows:', invalid_locator[:10])
    role_counts = Counter(row.get('primary_synthesis_role', 'NA') for row in extended)
    rq_counts = Counter(row.get('rq_contribution', 'NA') for row in extended)
    material_counts = Counter(row.get('material_type', 'NA') for row in extended)
    print(f'EXTENDED_SYNTHESIS_AUDIT: rows={len(extended)} roles=' + str(dict(sorted(role_counts.items()))))
    print('EXTENDED_SYNTHESIS_RQ_USE: ' + str(dict(sorted(rq_counts.items()))))
    print('EXTENDED_SYNTHESIS_MATERIAL_TYPES: ' + str(dict(sorted(material_counts.items()))))
    print(f'EXTENDED_SYNTHESIS_UNIQUE_CONTRIBUTION_RATIO: {unique_ratio:.3f}')
    print('EXTENDED_SYNTHESIS_UNRESOLVED_ROWS: ' + (','.join(unresolved) if unresolved else 'none'))


def validate_submission_update_screening(rows):
    status('ERROR', len(rows) == 432, f'submission update screening rows = {len(rows)}; expected 432')
    if not rows:
        return
    ids = [row.get('arxiv_id', '') for row in rows]
    status('ERROR', len(ids) == len(set(ids)), 'submission update arXiv identifiers are unique')
    allowed = {
        'existing_corpus_match',
        'outside_date_window',
        'potentially_eligible_update_record',
        'contextual_or_background_update',
        'excluded_at_title_abstract_update',
    }
    invalid = [row.get('arxiv_id', '?') for row in rows if row.get('screening_status') not in allowed]
    status('ERROR', not invalid, 'submission update screening statuses use the approved vocabulary')
    missing_reason = [row.get('arxiv_id', '?') for row in rows if len(row.get('decision_reason', '').strip()) < 30]
    status('ERROR', not missing_reason, 'submission update rows contain explicit decision reasons')
    counts = Counter(row.get('screening_status', 'NA') for row in rows)
    expected = {
        'existing_corpus_match': 12,
        'outside_date_window': 26,
        'potentially_eligible_update_record': 41,
        'contextual_or_background_update': 30,
        'excluded_at_title_abstract_update': 323,
    }
    status('ERROR', counts == Counter(expected), 'submission update screening counts match the frozen audit')
    print('SUBMISSION_UPDATE_SCREENING: ' + str(dict(sorted(counts.items()))))
    print('SUBMISSION_UPDATE_METHOD_NOTE: the 41 potentially eligible records have author and independent coding plus an author-confirmed resolution; corpus integration is complete, and manuscript alignment is validated separately.')
def validate_submission_update_full_audit(screening_rows, audit_rows, blind_rows):
    potential_ids = {
        row.get('arxiv_id', '')
        for row in screening_rows
        if row.get('screening_status') == 'potentially_eligible_update_record'
    }
    audit_ids = [row.get('arxiv_id', '') for row in audit_rows]
    blind_ids = [row.get('arxiv_id', '') for row in blind_rows]
    status('ERROR', len(audit_rows) == 41, f'submission update full-text audit rows = {len(audit_rows)}; expected 41')
    status('ERROR', len(blind_rows) == 41, f'submission update blind-review rows = {len(blind_rows)}; expected 41')
    status('ERROR', set(audit_ids) == potential_ids and len(audit_ids) == len(set(audit_ids)), 'full-text audit covers each potentially eligible update record exactly once')
    status('ERROR', set(blind_ids) == potential_ids and len(blind_ids) == len(set(blind_ids)), 'blind-review template covers each potentially eligible update record exactly once')

    allowed_layers = {
        'provisional_study_level_candidate_pending_independent_review',
        'extended_synthesis',
    }
    invalid_layers = [row.get('arxiv_id', '?') for row in audit_rows if row.get('author_analysis_layer') not in allowed_layers]
    status('ERROR', not invalid_layers, 'author full-text audit uses the approved provisional layer vocabulary')
    layer_counts = Counter(row.get('author_analysis_layer', 'NA') for row in audit_rows)
    expected_layers = Counter({
        'provisional_study_level_candidate_pending_independent_review': 38,
        'extended_synthesis': 3,
    })
    status('ERROR', layer_counts == expected_layers, 'author full-text audit has 38 provisional study-level candidates and 3 extended-synthesis records')

    allowed_outputs = {
        'candidate judgment',
        'controlled task completion',
        'runtime safety signal',
        'reproducible validation',
        'externally traceable material',
        'claim-level audit material',
        'governance boundary case',
    }
    invalid_outputs = [row.get('arxiv_id', '?') for row in audit_rows if row.get('strongest_evidence_output') not in allowed_outputs]
    status('ERROR', not invalid_outputs, 'author update audit uses approved evidence-output labels')
    status('ERROR', all(row.get('full_text_status') == 'full_text_reviewed' for row in audit_rows), 'all 41 update candidates have full-text author review')
    status('ERROR', all(row.get('formal_second_coder_status') == 'pending_independent_blind_review' for row in audit_rows), 'author update audit preserves its pre-review freeze status')

    blind_columns = set(blind_rows[0].keys()) if blind_rows else set()
    leaked_author_columns = sorted(column for column in blind_columns if column.startswith('author_'))
    status('ERROR', not leaked_author_columns, 'submission update blind template contains no author_* columns')
    coder2_fields = sorted(column for column in blind_columns if column.startswith('coder2_'))
    populated = [
        (row.get('update_id', '?'), field)
        for row in blind_rows
        for field in coder2_fields
        if row.get(field, '').strip()
    ]
    status('ERROR', not populated, 'submission update blind template coder2 fields are blank')
    safe_instructions = all(
        'independently decide' in row.get('materials_to_review', '').lower()
        and 'do not consult' in row.get('materials_to_review', '').lower()
        for row in blind_rows
    )
    status('ERROR', safe_instructions, 'submission update blind instructions require independent coding and hide the author audit')

    results_path = DATA / 'submission_update_20260715_second_coder_results.csv'
    if results_path.exists():
        print('SUBMISSION_UPDATE_METHOD_NOTE: the independent second-coder pass is complete; pre-adjudication agreement and the preserved working draft are validated below.')
    else:
        print('WARNING: submission update independent second-coder pass is pending; no agreement statistic or expanded manuscript denominator is reported.')
    print('SUBMISSION_UPDATE_FULL_AUDIT: ' + str(dict(sorted(layer_counts.items()))))

def validate_submission_update_second_coder(audit_rows, blind_rows, result_rows, adjudication_rows):
    status('ERROR', len(result_rows) == 41, f'submission update coder2 result rows = {len(result_rows)}; expected 41')
    status('ERROR', len(adjudication_rows) == 41, f'submission update adjudication working-draft rows = {len(adjudication_rows)}; expected 41')
    if not result_rows or not adjudication_rows:
        return

    audit_by_arxiv = {row.get('arxiv_id', ''): row for row in audit_rows}
    blind_by_arxiv = {row.get('arxiv_id', ''): row for row in blind_rows}
    result_ids = [row.get('arxiv_id', '') for row in result_rows]
    update_ids = [row.get('update_id', '') for row in result_rows]
    status('ERROR', len(result_ids) == len(set(result_ids)) == 41, 'submission update coder2 arXiv identifiers are unique')
    status('ERROR', set(result_ids) == set(audit_by_arxiv) == set(blind_by_arxiv), 'submission update coder2 results cover the frozen 41-record audit')
    status('ERROR', set(update_ids) == {f'U{i:02d}' for i in range(1, 42)}, 'submission update coder2 results use U01-U41 exactly once')

    leaked = sorted(field for field in result_rows[0] if field.startswith('author_') or field.startswith('original_'))
    status('ERROR', not leaked, 'submission update coder2 results expose no author_* or original_* fields')
    fixed_fields = ['update_id', 'arxiv_id', 'title', 'publication_status', 'materials_to_review']
    fixed_mismatches = []
    for row in result_rows:
        blind = blind_by_arxiv.get(row.get('arxiv_id', ''), {})
        if any(row.get(field, '') != blind.get(field, '') for field in fixed_fields):
            fixed_mismatches.append(row.get('update_id', '?'))
    status('ERROR', not fixed_mismatches, 'submission update coder2 fixed fields match the blind template')

    coder_fields = [
        'coder2_analysis_layer_decision', 'coder2_inclusion_reason', 'coder2_lifecycle_coverage',
        'coder2_primary_system_shape', 'coder2_cross_stage_capability_label',
        'coder2_strongest_evidence_output', 'coder2_external_traceability_label',
        'coder2_claim_boundary', 'coder2_uncertainty_note',
    ]
    incomplete = [row.get('update_id', '?') for row in result_rows if any(not row.get(field, '').strip() for field in coder_fields)]
    status('ERROR', not incomplete, 'all 41 submission update coder2 decisions, reasons, and uncertainty notes are populated')

    allowed_layers = {'study_level_candidate', 'extended_synthesis'}
    current_shape_vocab = {
        'candidate-analysis system', 'feedback-driven fuzzing agent',
        'reproduction-, validation-, and repair-centered agent',
        'long-horizon pentest and CRS agent',
    }
    legacy_shape_aliases = {
        'PoC/PoV validation agent': 'reproduction-, validation-, and repair-centered agent',
    }
    allowed_shapes = current_shape_vocab | set(legacy_shape_aliases)
    def normalize_shape_label(value):
        return legacy_shape_aliases.get(value, value)
    allowed_outputs = {
        'candidate judgment', 'controlled task completion', 'runtime safety signal',
        'reproducible validation', 'externally traceable material',
        'claim-level audit material', 'governance boundary case',
    }
    allowed_trace = {
        'not reported', 'benchmark ground truth / public material',
        'author-reported external clue', 'publicly aligned external trace',
    }
    status('ERROR', all(row.get('coder2_analysis_layer_decision') in allowed_layers for row in result_rows), 'submission update coder2 layer labels use the approved vocabulary')
    status('ERROR', all(row.get('coder2_primary_system_shape') in allowed_shapes for row in result_rows), 'submission update coder2 system-shape labels use approved current or preserved legacy vocabulary')
    status('ERROR', all(row.get('coder2_strongest_evidence_output') in allowed_outputs for row in result_rows), 'submission update coder2 evidence-output labels use the approved vocabulary')
    status('ERROR', all(row.get('coder2_external_traceability_label') in allowed_trace for row in result_rows), 'submission update coder2 traceability labels use the approved vocabulary')

    def author_layer(value):
        return value.removeprefix('provisional_').removesuffix('_pending_independent_review')

    def normalized_set(value, lifecycle=False):
        labels = split_multilabel(value)
        if lifecycle and 'path exploration' in labels:
            labels.remove('path exploration')
            labels.add('path and input exploration')
        return labels

    def update_set_metrics(author_field, coder_field, lifecycle=False):
        compared = []
        for row in result_rows:
            author = audit_by_arxiv[row.get('arxiv_id', '')]
            compared.append((
                normalized_set(author.get(author_field, ''), lifecycle=lifecycle),
                normalized_set(row.get(coder_field, ''), lifecycle=lifecycle),
            ))
        exact = sum(a == b for a, b in compared)
        jaccards = [1.0 if not (a | b) else len(a & b) / len(a | b) for a, b in compared]
        tp = sum(len(a & b) for a, b in compared)
        fp = sum(len(b - a) for a, b in compared)
        fn = sum(len(a - b) for a, b in compared)
        f1 = 1.0 if 2 * tp + fp + fn == 0 else 2 * tp / (2 * tp + fp + fn)
        return exact, exact / len(compared), sum(jaccards) / len(jaccards), f1

    author_layers = [author_layer(audit_by_arxiv[row['arxiv_id']].get('author_analysis_layer', '')) for row in result_rows]
    coder_layers = [row.get('coder2_analysis_layer_decision', '') for row in result_rows]
    author_shapes = [normalize_shape_label(audit_by_arxiv[row['arxiv_id']].get('primary_system_shape', '')) for row in result_rows]
    coder_shapes = [normalize_shape_label(row.get('coder2_primary_system_shape', '')) for row in result_rows]
    author_outputs = [audit_by_arxiv[row['arxiv_id']].get('strongest_evidence_output', '') for row in result_rows]
    coder_outputs = [row.get('coder2_strongest_evidence_output', '') for row in result_rows]
    author_trace = [audit_by_arxiv[row['arxiv_id']].get('external_traceability', '') for row in result_rows]
    coder_trace = [row.get('coder2_external_traceability_label', '') for row in result_rows]

    layer_agree = sum(a == b for a, b in zip(author_layers, coder_layers))
    shape_agree = sum(a == b for a, b in zip(author_shapes, coder_shapes))
    output_agree = sum(a == b for a, b in zip(author_outputs, coder_outputs))
    trace_agree = sum(a == b for a, b in zip(author_trace, coder_trace))
    layer_kappa = cohen_kappa(author_layers, coder_layers)
    shape_kappa = cohen_kappa(author_shapes, coder_shapes)
    output_kappa = cohen_kappa(author_outputs, coder_outputs)
    trace_kappa = cohen_kappa(author_trace, coder_trace)
    life = update_set_metrics('lifecycle_coverage', 'coder2_lifecycle_coverage', lifecycle=True)
    cap = update_set_metrics('agentic_capabilities', 'coder2_cross_stage_capability_label')

    status('ERROR', layer_agree == 40 and abs(layer_kappa - 0.844) < 0.001, 'submission update layer agreement reproduces 40/41 and kappa 0.844')
    status('ERROR', shape_agree == 27 and abs(shape_kappa - 0.514) < 0.001, 'submission update system-shape agreement reproduces 27/41 and kappa 0.514')
    status('ERROR', output_agree == 28 and abs(output_kappa - 0.566) < 0.001, 'submission update evidence-output agreement reproduces 28/41 and kappa 0.566')
    status('ERROR', trace_agree == 25 and abs(trace_kappa - 0.320) < 0.001, 'submission update traceability agreement reproduces 25/41 and kappa 0.320')
    status('ERROR', life[0] == 4 and abs(life[2] - 0.667) < 0.001 and abs(life[3] - 0.794) < 0.001, 'submission update lifecycle agreement reproduces exact 4/41, Jaccard 0.667, and micro F1 0.794')
    status('ERROR', cap[0] == 9 and abs(cap[2] - 0.760) < 0.001 and abs(cap[3] - 0.865) < 0.001, 'submission update capability agreement reproduces exact 9/41, Jaccard 0.760, and micro F1 0.865')
    print(f'SUBMISSION_UPDATE_SECOND_CODER: layer={layer_agree}/41 kappa={layer_kappa:.3f}; shape={shape_agree}/41 kappa={shape_kappa:.3f}; evidence={output_agree}/41 kappa={output_kappa:.3f}; trace={trace_agree}/41 kappa={trace_kappa:.3f}')
    print(f'SUBMISSION_UPDATE_MULTILABEL: lifecycle exact={life[0]}/41 jaccard={life[2]:.3f} micro_f1={life[3]:.3f}; capabilities exact={cap[0]}/41 jaccard={cap[2]:.3f} micro_f1={cap[3]:.3f}')

    report_path = REPORTS / 'SUBMISSION_UPDATE_SECOND_CODER_PRE_ADJUDICATION_REPORT.md'
    summary_path = ROOT / 'SUBMISSION_UPDATE_ADJUDICATION_SUMMARY.md'
    generator_path = ROOT / 'prepare_submission_update_adjudication.py'
    status('ERROR', report_path.exists(), 'submission update pre-adjudication agreement report exists')
    status('ERROR', summary_path.exists(), 'submission update adjudication summary exists')
    status('ERROR', generator_path.exists(), 'submission update adjudication generator exists')
    if report_path.exists():
        report_text = report_path.read_text(encoding='utf-8')
        required = ['40 / 41', '0.844', '27 / 41', '0.514', '28 / 41', '0.566', '25 / 41', '0.320', 'No adjudicated labels or post-adjudication agreement statistic are claimed']
        status('ERROR', all(item in report_text for item in required), 'submission update agreement report contains computed metrics and preserves pre-adjudication scope')

    draft_ids = [row.get('update_id', '') for row in adjudication_rows]
    status('ERROR', set(draft_ids) == set(update_ids) and len(draft_ids) == len(set(draft_ids)), 'adjudication working draft covers U01-U41 exactly once')
    status('ERROR', all(row.get('adjudication_status') == 'assistant_proposed_pending_author_confirmation' for row in adjudication_rows), 'adjudication working draft remains pending author confirmation')
    proposed_layers = Counter(row.get('proposed_analysis_layer', '') for row in adjudication_rows)
    status('ERROR', proposed_layers == Counter({'study_level_candidate': 37, 'extended_synthesis': 4}), 'proposed update layer counts are 37 study-level candidates and 4 extended-synthesis records')
    u24 = next((row for row in adjudication_rows if row.get('update_id') == 'U24'), {})
    status('ERROR', u24.get('proposed_analysis_layer') == 'extended_synthesis', 'U24 SynthFix is proposed as extended synthesis under the observable-workflow rule')
    print('SUBMISSION_UPDATE_WORKING_DRAFT: the assistant-prepared proposal remains preserved; author confirmation is validated separately.')


def validate_submission_update_finalization(adjudication_rows, final_rows, integration_rows):
    status('ERROR', len(final_rows) == 41, f'author-confirmed submission update adjudication rows = {len(final_rows)}; expected 41')
    status('ERROR', len(integration_rows) == 41, f'submission update canonical-integration rows = {len(integration_rows)}; expected 41')
    if not final_rows or not integration_rows:
        return

    final_ids = [row.get('update_id', '') for row in final_rows]
    integration_ids = [row.get('update_id', '') for row in integration_rows]
    expected_ids = {f'U{i:02d}' for i in range(1, 42)}
    status('ERROR', set(final_ids) == expected_ids and len(final_ids) == len(set(final_ids)), 'author-confirmed adjudication covers U01-U41 exactly once')
    status('ERROR', set(integration_ids) == expected_ids and len(integration_ids) == len(set(integration_ids)), 'canonical-integration crosswalk covers U01-U41 exactly once')
    status('ERROR', all(row.get('adjudication_status') == 'author_confirmed_evidence_based_resolution' for row in final_rows), 'submission update adjudication is marked author-confirmed without claiming human consensus')

    draft_by_id = {row.get('update_id', ''): row for row in adjudication_rows}
    comparison_fields = [
        'proposed_analysis_layer', 'proposed_lifecycle_coverage', 'proposed_primary_system_shape',
        'proposed_agentic_capabilities', 'proposed_strongest_evidence_output',
        'proposed_external_traceability', 'proposed_claim_boundary',
    ]
    mismatches = []
    for row in final_rows:
        draft = draft_by_id.get(row.get('update_id', ''), {})
        if any(row.get(field, '') != draft.get(field, '') for field in comparison_fields):
            mismatches.append(row.get('update_id', '?'))
    status('ERROR', not mismatches, 'author-confirmed adjudication preserves the reviewed working-draft labels')

    final_layers = Counter(row.get('proposed_analysis_layer', '') for row in final_rows)
    status('ERROR', final_layers == Counter({'study_level_candidate': 37, 'extended_synthesis': 4}), 'author-confirmed update layer counts are 37 study-level candidates and 4 extended-synthesis records')
    status('ERROR', all(row.get('integration_status') == 'new_canonical_study' for row in integration_rows), 'canonical integration finds all 41 update records to be new canonical studies')
    status('ERROR', all(row.get('counted_after_integration') == 'yes' for row in integration_rows), 'all update records are countable after canonical integration')

    final_report = REPORTS / 'SUBMISSION_UPDATE_ADJUDICATION_REPORT.md'
    integration_report = ROOT / 'SUBMISSION_UPDATE_CANONICAL_INTEGRATION_REPORT.md'
    finalizer = ROOT / 'finalize_submission_update_adjudication.py'
    integration_generator = ROOT / 'prepare_submission_update_canonical_integration.py'
    for path, description in [
        (final_report, 'author-confirmed update adjudication report exists'),
        (integration_report, 'submission update canonical-integration report exists'),
        (finalizer, 'submission update finalization script exists'),
        (integration_generator, 'submission update canonical-integration generator exists'),
    ]:
        status('ERROR', path.exists(), description)
    if final_report.exists():
        report_text = final_report.read_text(encoding='utf-8')
        required = ['author-confirmed analytical decision', 'not represented as a discussion between two human coders', 'No post-adjudication agreement statistic is reported']
        status('ERROR', all(item in report_text for item in required), 'final adjudication report states the confirmation and consensus boundary accurately')
    if integration_report.exists():
        report_text = integration_report.read_text(encoding='utf-8')
        required = ['Source records | 212 | 253', 'Canonical candidate studies | 207 | 248', '67 target-software studies plus the existing governance boundary case']
        status('ERROR', all(item in report_text for item in required), 'canonical-integration report records projected counts without changing the frozen corpus')
    print('SUBMISSION_UPDATE_FINALIZATION: author-confirmed 37/4 resolution and pre-integration assessment preserved; current corpus integration is validated separately.')


def validate_current_study_level_matrix(current_matrix, additions):
    status('ERROR', len(current_matrix) == 68, f'current study-level matrix rows = {len(current_matrix)}; expected 68')
    if not current_matrix:
        return

    matrix_ids = [row.get('matrix_id', '') for row in current_matrix]
    record_ids = [row.get('record_id', '') for row in current_matrix]
    canonical_ids = [row.get('canonical_study_id', '') for row in current_matrix]
    status('ERROR', len(matrix_ids) == len(set(matrix_ids)), 'current matrix IDs are unique')
    status('ERROR', len(record_ids) == len(set(record_ids)), 'current matrix record IDs are unique')
    status('ERROR', len(canonical_ids) == len(set(canonical_ids)), 'current matrix canonical study IDs are unique')
    status('ERROR', set(matrix_ids) == {f'C{i:02d}' for i in range(1, 32)} | {row.get('update_id', '') for row in additions}, 'current matrix covers the frozen 31 rows and all 37 update additions')

    roles = Counter(row.get('analytical_role', '') for row in current_matrix)
    rounds = Counter(row.get('coding_round', '') for row in current_matrix)
    evidence = Counter(row.get('strongest_evidence_output', '') for row in current_matrix)
    status('ERROR', roles == Counter({'target_software_study': 67, 'governance_boundary_case': 1}), 'current matrix uses the 67+1 analytical-role boundary')
    status('ERROR', rounds == Counter({'initial_frozen_round': 31, 'submission_update_20260715': 37}), 'current matrix preserves the 31+37 coding-round provenance')
    status('ERROR', evidence == Counter({'reproducible validation': 31, 'runtime safety signal': 13, 'controlled task completion': 13, 'candidate judgment': 6, 'externally traceable material': 4, 'governance boundary case': 1}), 'current matrix reproduces the combined strongest-evidence distribution')
    status('ERROR', not any(field.startswith('a_level') or field.startswith('e_level') for field in current_matrix[0]), 'current matrix does not reintroduce legacy A/E fields')
    status('ERROR', all(row.get('official_url', '').startswith(('http://', 'https://', 'urn:isbn:')) for row in current_matrix), 'current matrix rows contain public URLs or ISBN locators')
    status('ERROR', all(row.get('claim_boundary', '').strip() and row.get('claim_boundary_original', '').strip() for row in current_matrix), 'current matrix retains current and original claim-boundary text')

    by_id = {row.get('matrix_id', ''): row for row in current_matrix}
    c27 = by_id.get('C27', {})
    status('ERROR', c27.get('record_id') == 'CP114' and c27.get('canonical_study_id') == 'CS_CP114', 'C27 governance case resolves to canonical record CP114')
    status('ERROR', c27.get('analytical_role') == 'governance_boundary_case', 'C27 remains outside the target-software denominator')

    additions_by_id = {row.get('update_id', ''): row for row in additions}
    comparable = {
        'record_id': 'record_id',
        'canonical_study_id': 'canonical_study_id',
        'system_alias': 'system_alias',
        'title': 'title',
        'lifecycle_coverage': 'lifecycle_coverage',
        'system_shape': 'primary_system_shape',
        'agentic_capabilities': 'agentic_capabilities',
        'strongest_evidence_output': 'strongest_evidence_output',
        'external_traceability': 'external_traceability',
        'claim_boundary': 'claim_boundary',
        'official_url': 'official_url',
    }
    mismatches = []
    for update_id, addition in additions_by_id.items():
        row = by_id.get(update_id, {})
        for matrix_field, addition_field in comparable.items():
            if row.get(matrix_field) != addition.get(addition_field):
                mismatches.append(f'{update_id}:{matrix_field}')
    status('ERROR', not mismatches, 'current matrix update rows match the 37 author-confirmed additions field by field')
    if mismatches:
        print('ERROR: current matrix mismatches:', ', '.join(mismatches))
    print('CURRENT_STUDY_LEVEL_MATRIX: rows=68 target=67 governance=1 initial_round=31 update_round=37')

def validate_integrated_submission_update(corpus, crosswalk, extended, final_rows, additions, current_stats):
    status('ERROR', len(corpus) == 253, f'integrated corpus source rows = {len(corpus)}; expected 253')
    status('ERROR', len(crosswalk) == 253, f'integrated canonical crosswalk rows = {len(crosswalk)}; expected 253')
    status('ERROR', len(additions) == 37, f'current-field update study-level additions = {len(additions)}; expected 37')
    status('ERROR', len(extended) == 65, f'integrated extended-synthesis rows = {len(extended)}; expected 65')
    if not final_rows or not additions:
        return

    final_study_ids = {row.get('update_id', '') for row in final_rows if row.get('proposed_analysis_layer') == 'study_level_candidate'}
    addition_ids = {row.get('update_id', '') for row in additions}
    status('ERROR', addition_ids == final_study_ids, 'study-level additions match the 37 author-confirmed update records')
    status('ERROR', not any(field.startswith('a_level') or field.startswith('e_level') for field in additions[0]), 'update additions do not impute legacy A/E fields')
    status('ERROR', all(row.get('coding_status') == 'author_confirmed_adjudicated' for row in additions), 'update additions retain author-confirmed coding status')

    update_record_ids = {f'CP{i:03d}' for i in range(213, 254)}
    corpus_ids = {row.get('record_id', '') for row in corpus}
    cross_by_id = {row.get('record_id', ''): row for row in crosswalk}
    status('ERROR', update_record_ids <= corpus_ids, 'integrated corpus contains CP213-CP253')
    status('ERROR', update_record_ids <= set(cross_by_id), 'canonical crosswalk contains CP213-CP253')
    update_layers = Counter(cross_by_id[rid].get('analytical_layer', '') for rid in update_record_ids)
    status('ERROR', update_layers == Counter({'study_level_coded': 37, 'extended_synthesis': 4}), 'integrated update canonical layers reproduce the confirmed 37/4 resolution')
    status('ERROR', all(cross_by_id[rid].get('counting_status') == 'canonical_counted' for rid in update_record_ids), 'all integrated update records count once as canonical studies')

    expected = {
        ('lifecycle_coverage', 'candidate analysis'): 48,
        ('lifecycle_coverage', 'path and input exploration'): 46,
        ('lifecycle_coverage', 'execution observation'): 56,
        ('lifecycle_coverage', 'reproduction and validation'): 36,
        ('lifecycle_coverage', 'patch validation'): 12,
        ('lifecycle_coverage', 'reporting and audit'): 24,
        ('agentic_capabilities', 'context aggregation / rule extraction'): 51,
        ('agentic_capabilities', 'tool routing / strategy routing'): 44,
        ('agentic_capabilities', 'feedback interpretation / loop adjustment'): 58,
        ('agentic_capabilities', 'validation organization / evidence packaging'): 55,
        ('agentic_capabilities', 'long-horizon state management'): 30,
        ('agentic_capabilities', 'failure reuse / strategy update'): 15,
        ('agentic_capabilities', 'governance / human gates / disclosure control'): 4,
        ('strongest_evidence_output', 'candidate judgment'): 6,
        ('strongest_evidence_output', 'controlled task completion'): 13,
        ('strongest_evidence_output', 'runtime safety signal'): 13,
        ('strongest_evidence_output', 'reproducible validation'): 31,
        ('strongest_evidence_output', 'externally traceable material'): 4,
        ('strongest_evidence_output', 'governance boundary case'): 1,
        ('primary_system_shape', 'candidate-analysis system'): 16,
        ('primary_system_shape', 'feedback-driven fuzzing agent'): 17,
        ('primary_system_shape', 'reproduction-, validation-, and repair-centered agent'): 20,
        ('primary_system_shape', 'long-horizon pentest and CRS agent'): 14,
    }
    actual = {(row.get('dimension', ''), row.get('category', '')): int(row.get('count', '-1')) for row in current_stats}
    status('ERROR', actual == expected, 'current synthesis statistics reproduce the integrated lifecycle, capability, and evidence-output counts')

    report = ROOT / 'SUBMISSION_UPDATE_CORPUS_INTEGRATION_REPORT.md'
    integrator = ROOT / 'integrate_submission_update_corpus.py'
    status('ERROR', report.exists(), 'submission update corpus integration report exists')
    status('ERROR', integrator.exists(), 'submission update corpus integration script exists')
    if report.exists():
        report_text = report.read_text(encoding='utf-8')
        required = ['Source records: 253', 'Canonical candidate studies: 248', 'Target-software study-level coded studies: 67', 'Extended-synthesis studies: 65', "No combined Cohen's kappa is inferred"]
        status('ERROR', all(item in report_text for item in required), 'corpus integration report records current counts and the two-round reliability boundary')
    print('SUBMISSION_UPDATE_CORPUS_INTEGRATION: source=253 canonical=248 target_studies=67 governance=1 extended=65 background=95 excluded=20')




def validate_harmonized_coding_matrix(pre_matrix, harmonized, audit_rows, round_stats, extended_rows):
    lifecycle_vocab = {'candidate analysis', 'path and input exploration', 'execution observation', 'reproduction and validation', 'patch validation', 'reporting and audit'}
    shape_vocab = {'candidate-analysis system', 'feedback-driven fuzzing agent', 'reproduction-, validation-, and repair-centered agent', 'long-horizon pentest and CRS agent', 'governance boundary case'}
    overlay_vocab = {'multi-agent orchestration', 'iterative optimization', 'failure-memory reuse', 'governance control'}
    capability_vocab = {'context aggregation / rule extraction', 'tool routing / strategy routing', 'feedback interpretation / loop adjustment', 'validation organization / evidence packaging', 'long-horizon state management', 'failure reuse / strategy update', 'governance / human gates / disclosure control'}
    status('ERROR', len(harmonized) == 68, f'harmonized study-level matrix rows = {len(harmonized)}; expected 68')
    status('ERROR', len(audit_rows) == 408, f'harmonization audit rows = {len(audit_rows)}; expected 408')
    status('ERROR', all(row.get('harmonization_status') == 'author_confirmed_2026-07-16' for row in harmonized), 'combined counts use only the author-confirmed harmonized matrix')
    status('ERROR', all(split_multilabel(row.get('lifecycle_coverage', '')) <= lifecycle_vocab for row in harmonized), 'harmonized lifecycle fields use the controlled vocabulary')
    status('ERROR', all(row.get('primary_system_shape', '') in shape_vocab for row in harmonized), 'harmonized primary shapes use approved values')
    status('ERROR', all(split_multilabel(row.get('overlay_tags', '')) <= overlay_vocab for row in harmonized), 'overlay tags use approved values and remain outside primary shapes')
    status('ERROR', all(split_multilabel(row.get('cross_stage_capabilities', '')) <= capability_vocab for row in harmonized), 'formal capability fields use the controlled vocabulary')
    status('ERROR', all('role discussion / textual reflection' not in row.get('cross_stage_capabilities', '') for row in harmonized), 'formal capability fields contain no legacy textual-reflection label')
    pre_by_id = {row.get('matrix_id', ''): row for row in pre_matrix}
    harm_by_id = {row.get('matrix_id', ''): row for row in harmonized}
    status('ERROR', set(pre_by_id) == set(harm_by_id) and len(harm_by_id) == 68, 'all 68 harmonized records preserve matrix identity')
    status('ERROR', all(pre_by_id[mid].get('canonical_study_id') == harm_by_id[mid].get('canonical_study_id') for mid in harm_by_id), 'all harmonized records preserve canonical-study mapping')
    status('ERROR', all(row.get('author_review_status') != 'pending_author_review' and (row.get('field') == 'overlay_tags' or row.get('final_harmonized_label', '')) for row in audit_rows), 'harmonization audit contains no pending decisions; blank overlay tags are allowed')
    audit_fields = Counter((row.get('matrix_id', ''), row.get('field', '')) for row in audit_rows)
    status('ERROR', all(value == 1 for value in audit_fields.values()) and len(audit_fields) == 408, 'harmonization audit covers six fields for each matrix row exactly once')
    source_map = {'lifecycle_coverage': 'lifecycle_coverage', 'primary_system_shape': 'system_shape', 'overlay_tags': 'system_shape', 'cross_stage_capabilities': 'agentic_capabilities', 'strongest_evidence_output': 'strongest_evidence_output', 'external_traceability': 'external_traceability'}
    status('ERROR', all(row.get('original_label', '') == pre_by_id.get(row.get('matrix_id', ''), {}).get(source_map.get(row.get('field', ''), ''), '') for row in audit_rows), 'all frozen/pre-harmonization labels remain preserved in the audit')
    coded_canonical = {row.get('canonical_study_id', '') for row in harmonized}
    extended_canonical = {row.get('canonical_study_id', '') for row in extended_rows}
    status('ERROR', not (coded_canonical & extended_canonical), 'extended synthesis does not overlap the harmonized coded set')
    target = [row for row in harmonized if row.get('analytical_role') == 'target_software_study']
    initial = [row for row in target if row.get('coding_round') == 'initial_frozen_round']
    update = [row for row in target if row.get('coding_round') == 'submission_update_20260715']
    status('ERROR', len(initial) == 30 and len(update) == 37, 'round-wise target-software totals reconcile to 30 + 37 = 67')
    expected_shape_by_round = {
        'initial': Counter({'candidate-analysis system': 4, 'feedback-driven fuzzing agent': 9, 'reproduction-, validation-, and repair-centered agent': 8, 'long-horizon pentest and CRS agent': 9}),
        'update': Counter({'candidate-analysis system': 12, 'feedback-driven fuzzing agent': 8, 'reproduction-, validation-, and repair-centered agent': 12, 'long-horizon pentest and CRS agent': 5}),
        'combined': Counter({'candidate-analysis system': 16, 'feedback-driven fuzzing agent': 17, 'reproduction-, validation-, and repair-centered agent': 20, 'long-horizon pentest and CRS agent': 14}),
    }
    expected_evidence_by_round = {
        'initial': Counter({'candidate judgment': 3, 'controlled task completion': 5, 'runtime safety signal': 8, 'reproducible validation': 14, 'externally traceable material': 0}),
        'update': Counter({'candidate judgment': 3, 'controlled task completion': 8, 'runtime safety signal': 5, 'reproducible validation': 17, 'externally traceable material': 4}),
        'combined': Counter({'candidate judgment': 6, 'controlled task completion': 13, 'runtime safety signal': 13, 'reproducible validation': 31, 'externally traceable material': 4}),
    }
    shape_initial = Counter(row.get('primary_system_shape') for row in initial)
    shape_update = Counter(row.get('primary_system_shape') for row in update)
    shape_combined = Counter(row.get('primary_system_shape') for row in target)
    evidence_initial = Counter(row.get('strongest_evidence_output') for row in initial)
    evidence_update = Counter(row.get('strongest_evidence_output') for row in update)
    evidence_combined = Counter(row.get('strongest_evidence_output') for row in target)
    status('ERROR', shape_initial == expected_shape_by_round['initial'], 'initial-round primary-shape counts are 4/9/8/9')
    status('ERROR', shape_update == expected_shape_by_round['update'], 'recall-recovery primary-shape counts are 12/8/12/5')
    status('ERROR', shape_combined == expected_shape_by_round['combined'], 'combined primary-shape counts are 16/17/20/14')
    status('ERROR', evidence_initial == expected_evidence_by_round['initial'], 'initial-round evidence counts are CJ3/TC5/RS8/RV14/ET0')
    status('ERROR', evidence_update == expected_evidence_by_round['update'], 'recall-recovery evidence counts are CJ3/TC8/RS5/RV17/ET4')
    status('ERROR', evidence_combined == expected_evidence_by_round['combined'], 'combined evidence counts are CJ6/TC13/RS13/RV31/ET4')

    substantive = [row for row in audit_rows if row.get('change_required') == 'yes']
    changed_record_ids = sorted({row.get('matrix_id') for row in substantive})
    changed_fields = Counter(row.get('field') for row in substantive)
    missing_basis = [row.get('matrix_id', '?') + ':' + row.get('field', '?') for row in substantive if len(row.get('evidence_basis', '').strip()) < 20]
    unresolved = [row.get('matrix_id', '?') + ':' + row.get('field', '?') for row in audit_rows if 'pending' in row.get('author_review_status', '').lower()]
    status('ERROR', not missing_basis, 'every substantive harmonization change has an evidence basis')
    status('ERROR', not unresolved, 'harmonization audit has no unresolved fields')
    if missing_basis:
        print('ERROR: harmonization changes missing evidence basis:', ', '.join(missing_basis[:20]))
    if unresolved:
        print('ERROR: unresolved harmonization fields:', ', '.join(unresolved[:20]))
    print('HARMONIZATION_CHANGE_SUMMARY: changed_records=' + str(len(changed_record_ids)) + ' changed_fields=' + str(dict(sorted(changed_fields.items()))))
    stat_lookup = {(row.get('category', ''), row.get('label', '')): row for row in round_stats}
    for category, field in [('lifecycle_coverage', 'lifecycle_coverage'), ('cross_stage_capability', 'cross_stage_capabilities'), ('primary_system_shape', 'primary_system_shape')]:
        all_labels = set().union(*(split_multilabel(row.get(field, '')) for row in target))
        for label in all_labels:
            expected_initial = sum(label in split_multilabel(row.get(field, '')) for row in initial)
            expected_update = sum(label in split_multilabel(row.get(field, '')) for row in update)
            stat = stat_lookup.get((category, label), {})
            status('ERROR', int(stat.get('initial_cohort_count', -1)) == expected_initial and int(stat.get('submission_update_cohort_count', -1)) == expected_update and int(stat.get('combined_harmonized_count', -1)) == expected_initial + expected_update, f'round statistics reconcile for {category}: {label}')
    print('CODING_ROUND_HARMONIZATION: rows=68 target=67 governance=1 audit_fields=408 status=author_confirmed')



def validate_manuscript_artifact_paths():
    manuscript = ROOT.parent / 'latex' / 'latex_acm_csur_en' / 'main_acm_csur.tex'
    status('ERROR', manuscript.exists(), 'manuscript main_acm_csur.tex exists for artifact-path validation')
    if not manuscript.exists():
        return
    text = manuscript.read_text(encoding='utf-8')
    paths = re.findall(r'\\path\{([^}]+)\}', text)
    missing = []
    for rel in paths:
        if rel.startswith(('data/', 'reports/')) or rel.endswith('.md') or rel.endswith('.py'):
            candidate = ROOT / rel.replace('/', '\\')
            if not candidate.exists():
                missing.append(rel)
    status('ERROR', not missing, 'Data and Code Availability artifact paths exist in the public artifact')
    if missing:
        print('ERROR: missing artifact paths from manuscript:', ', '.join(missing))
def validate_tracked_file_boundary():
    try:
        result = subprocess.run(['git', 'ls-files'], cwd=ROOT, check=True, capture_output=True, text=True)
    except Exception as exc:
        print(f'WARNING: could not run git ls-files for tracked-file boundary check: {exc}')
        return
    tracked = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    forbidden_path_tokens = [
        'local_private_working/',
        'zotero_private_paths',
        '.sqlite',
        '.sqlite-journal',
    ]
    forbidden_suffixes = ('.pdf', '.sqlite', '.sqlite-journal')
    forbidden_paths = []
    private_content_hits = []
    for rel in tracked:
        normalized = rel.replace('\\', '/').lower()
        if normalized.endswith(forbidden_suffixes) or any(token in normalized for token in forbidden_path_tokens):
            forbidden_paths.append(rel)
            continue
        path = ROOT / rel
        try:
            content = path.read_text(encoding='utf-8')
        except Exception:
            continue
        lowered = content.lower()
        actual_private_markers = ['c:\\users\\', 'zotero\\storage', 'zotero/storage']
        if rel != 'reproduce_tables.py' and any(marker in lowered for marker in actual_private_markers):
            private_content_hits.append(rel)
    status('ERROR', not forbidden_paths, 'no tracked PDFs, SQLite files, local_private_working files, or private Zotero path files')
    if forbidden_paths:
        print('ERROR: forbidden tracked paths:', ', '.join(forbidden_paths))
    status('ERROR', not private_content_hits, 'tracked text files contain no absolute local Zotero paths or Zotero storage references')
    if private_content_hits:
        print('ERROR: tracked files needing security-boundary review:', ', '.join(sorted(set(private_content_hits))))

validate_all_csv_files()

corpus = read_csv('corpus.csv')
core = read_csv('core_coding.csv')
core_synthesis = read_csv('v13_core_synthesis_matrix.csv')
summary = read_csv('screening_summary.csv')
ref = read_csv('reference_audit.csv')
product_snapshot = read_csv('product_ecosystem_snapshot.csv')
second_coder_blind = read_csv('core31_second_coder_blind.csv')
second_coder_formal = read_csv('core31_second_coder_formal_blind_template.csv')
second_coder_formal_results = read_csv('core31_second_coder_formal_results.csv')
second_coder_extension_template = read_csv('core31_second_coder_capability_traceability_blind_template.csv')
second_coder_extension_results = read_csv('core31_second_coder_capability_traceability_results.csv')
second_coder_adjudication = read_csv('core31_second_coder_adjudication_template.csv')
record_classification = read_csv('record_classification_audit.csv')
repro_audit = read_csv('core_reproducibility_audit.csv')
repro_summary = read_csv('core_reproducibility_audit_summary.csv')
source_search_log = read_csv('source_search_log.csv')
source_screening_audit = read_csv('source_screening_audit.csv')
extended_synthesis = read_csv('extended_synthesis_audit.csv')
study_version_crosswalk = read_csv('study_version_crosswalk.csv')
mapping_snapshot_counts = read_csv('mapping_snapshot_counts.csv')
submission_update_screening = read_csv('submission_update_20260715_screening_audit.csv')
submission_update_full_audit = read_csv('submission_update_20260715_full_coding_audit.csv')
submission_update_blind = read_csv('submission_update_20260715_second_coder_blind_template.csv')
submission_update_results = read_csv('submission_update_20260715_second_coder_results.csv')
submission_update_adjudication = read_csv('submission_update_20260715_adjudication_working_draft.csv')
submission_update_adjudicated = read_csv('submission_update_20260715_adjudicated.csv')
submission_update_integration = read_csv('submission_update_20260715_canonical_integration_crosswalk.csv')
submission_update_additions = read_csv('submission_update_20260715_study_level_additions.csv')
current_synthesis_statistics = read_csv('current_synthesis_statistics.csv')
current_study_level_matrix = read_csv('current_study_level_coding_matrix.csv')
harmonized_study_level_matrix = read_csv('current_study_level_coding_matrix_harmonized.csv')
coding_round_harmonization_audit = read_csv('coding_round_harmonization_audit.csv')
current_synthesis_statistics_by_round = read_csv('current_synthesis_statistics_by_round.csv')

validate_product_ecosystem_snapshot(product_snapshot)
validate_second_coder_files(second_coder_blind, second_coder_adjudication, second_coder_formal, second_coder_formal_results)
validate_second_coder_extension_template(second_coder_extension_template, second_coder_extension_results, core_synthesis)
validate_source_search_audit(corpus, source_search_log, source_screening_audit)
validate_study_version_crosswalk(corpus, ref, study_version_crosswalk, mapping_snapshot_counts)
validate_extended_synthesis_audit(corpus, extended_synthesis, study_version_crosswalk)
validate_submission_update_screening(submission_update_screening)
validate_submission_update_full_audit(submission_update_screening, submission_update_full_audit, submission_update_blind)
validate_submission_update_second_coder(submission_update_full_audit, submission_update_blind, submission_update_results, submission_update_adjudication)
validate_submission_update_finalization(submission_update_adjudication, submission_update_adjudicated, submission_update_integration)
validate_current_study_level_matrix(current_study_level_matrix, submission_update_additions)
validate_harmonized_coding_matrix(current_study_level_matrix, harmonized_study_level_matrix, coding_round_harmonization_audit, current_synthesis_statistics_by_round, extended_synthesis)
validate_integrated_submission_update(corpus, study_version_crosswalk, extended_synthesis, submission_update_adjudicated, submission_update_additions, current_synthesis_statistics)
validate_manuscript_artifact_paths()
validate_tracked_file_boundary()

expected_layers = {'Core': 68, 'Supporting': 69, 'Background': 95, 'Excluded': 21}
if corpus:
    status('ERROR', len(corpus) == 253, f'source records = {len(corpus)}; expected 253')
    layer_counts = Counter(r.get('corpus_layer', 'NA') for r in corpus)
    for layer, expected in expected_layers.items():
        status('ERROR', layer_counts.get(layer, 0) == expected, f'{layer} = {layer_counts.get(layer, 0)}; expected {expected}')

if core:
    status('ERROR', len(core) == 31, f'study-level coding rows = {len(core)}; expected 31')
    core_ids = [r.get('core_id', '') for r in core]
    record_ids = [r.get('record_id', '') for r in core]
    status('ERROR', len(core_ids) == len(set(core_ids)), 'core_id values are unique')
    status('ERROR', len(record_ids) == len(set(record_ids)), 'record_id values are unique in core_coding.csv')
    for required_core in ['C28', 'C29', 'C30', 'C31']:
        status('ERROR', required_core in core_ids, f'{required_core} exists in core_coding.csv')
    missing_reason = [r.get('core_id','?') for r in core if r.get('a_level_reason','NA') in ('', 'NA') or r.get('e_level_reason','NA') in ('', 'NA')]
    if missing_reason:
        print('WARNING: missing A/E reason fields for:', ', '.join(missing_reason))
    else:
        print('PASS: all Core rows include A/E reason fields')

    a_counts = Counter()
    for r in core:
        for a in expand_a_level(r.get('a_level','')):
            a_counts[a] += 1
    print('A-profile occurrence counts:', dict(sorted(a_counts.items())))

    e_counts = Counter(r.get('e_level','NA') for r in core)
    expected_e = {'E0':3, 'E1':5, 'E2':8, 'E3':14, 'N/A':1}
    for e, expected in expected_e.items():
        status('ERROR', e_counts.get(e, 0) == expected, f'{e} = {e_counts.get(e, 0)}; expected {expected}')
    e4c_count = sum(1 for r in core if 'E4c' in (r.get('external_evidence_profile', '') or ''))
    status('ERROR', e4c_count == 0, f'E4c external profile = {e4c_count}; expected 0')

if summary:
    stage_counts = {r.get('stage'): r.get('count') for r in summary}
    print('screening_summary.csv stages:', stage_counts)

if ref:
    missing_url = sum(1 for r in ref if r.get('official_url','NA') in ('', 'NA'))
    missing_doi = sum(1 for r in ref if r.get('doi','NA') in ('', 'NA'))
    missing_verified = sum(1 for r in ref if r.get('last_verified_date','NA') in ('', 'NA'))
    print(f'WARNING: reference_audit missing official_url in {missing_url} rows')
    print(f'WARNING: reference_audit missing doi in {missing_doi} rows')
    print(f'WARNING: reference_audit missing last_verified_date in {missing_verified} rows')

if record_classification:
    expected_records = {
        'FuzzingBrain V2': 'Core',
        'DrillAgent': 'Core',
        'AIxCC SoK': 'Background',
        'OSS-CRS': 'Core',
        'GONDAR': 'Core',
        'COTTONTAIL': 'Supporting',
        'Wan et al.': 'Background',
    }
    status('ERROR', len(record_classification) == 7, f'record_classification_audit rows = {len(record_classification)}; expected 7')
    actual = {r.get('record', ''): r.get('classification', '') for r in record_classification}
    for record, expected in expected_records.items():
        status('ERROR', actual.get(record) == expected, f'{record} classification = {actual.get(record, "MISSING")}; expected {expected}')

if repro_audit:
    repro_ids = [r.get('core_id', '') for r in repro_audit]
    status('ERROR', len(repro_audit) == 30, f'core_reproducibility_audit rows = {len(repro_audit)}; expected 30 vulnerability-mining Core rows')
    status('ERROR', 'C27' not in repro_ids, 'C27 governance boundary case is excluded from reproducibility audit')
    core_ids = {r.get('core_id', '') for r in core if r.get('core_id') != 'C27'} if core else set()
    status('ERROR', set(repro_ids) == core_ids, 'core_reproducibility_audit core_id values align with core_coding.csv excluding C27')
    status_fields = [f for f in (CSV_REQUIRED_FIELDS['core_reproducibility_audit.csv']) if f.endswith('_status')]
    source_errors = []
    private_leaks = []
    for row in repro_audit:
        joined = ' '.join(str(v) for v in row.values())
        if 'C:\\\\Users\\\\' in joined or 'Zotero\\\\storage' in joined or joined.lower().endswith('.pdf'):
            private_leaks.append(row.get('core_id', '?'))
        for field in status_fields:
            value = row.get(field, '')
            if value in ('reported_yes', 'reported_partial'):
                evidence_field = field.replace('_status', '_evidence_public')
                if field == 'public_artifact_status':
                    evidence_field = 'public_artifact_public_reference'
                if row.get(evidence_field, '') in ('', 'NA'):
                    source_errors.append((row.get('core_id', '?'), field))
    status('ERROR', not source_errors, 'reported_yes/reported_partial reproducibility fields include public source notes')
    status('ERROR', not private_leaks, 'public reproducibility audit contains no private Zotero/PDF paths')
    unknown_counts = Counter()
    for row in repro_audit:
        for field in status_fields:
            if row.get(field) == 'unknown_not_audited':
                unknown_counts[field] += 1
    print('Reproducibility audit unknown_not_audited counts:', dict(sorted(unknown_counts.items())))

if repro_summary:
    print('core_reproducibility_audit_summary rows:', len(repro_summary))

if ERROR_COUNT:
    print(f'DONE with {ERROR_COUNT} error(s)')
    sys.exit(1)

print('DONE')




