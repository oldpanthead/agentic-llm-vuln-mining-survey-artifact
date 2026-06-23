#!/usr/bin/env python3
import csv
import sys
import subprocess
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'data'

CSV_REQUIRED_FIELDS = {
    'corpus.csv': ['record_id', 'corpus_layer'],
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

def validate_second_coder_files(blind_rows, adjudication_rows, formal_rows=None):
    formal_rows = formal_rows or []
    blind_path = DATA / 'core31_second_coder_blind.csv'
    formal_path = DATA / 'core31_second_coder_formal_blind_template.csv'
    adjudication_path = DATA / 'core31_second_coder_adjudication_template.csv'
    pilot_dir = ROOT / 'archive' / 'pilot_second_coder_round_1'
    pilot_report = pilot_dir / 'SECOND_CODER_AGREEMENT_REPORT.md'
    pilot_results = pilot_dir / 'core31_second_coder_results.csv'
    status('ERROR', blind_path.exists(), 'core31_second_coder_blind.csv exists')
    status('ERROR', formal_path.exists(), 'core31_second_coder_formal_blind_template.csv exists')
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
        status('ERROR', not formal_filled, 'adjudication template coder2/adjudication fields are blank before formal rerun')
        if formal_filled:
            print('ERROR: nonblank formal adjudication fields:', formal_filled[:10])

    status('ERROR', pilot_dir.exists(), 'pilot second-coder calibration archive exists')
    status('ERROR', pilot_report.exists(), 'pilot agreement report is archived outside the formal report path')
    status('ERROR', pilot_results.exists(), 'pilot coder2 results are archived outside the formal data path')
    pilot_readme = pilot_dir / 'README.md'
    status('ERROR', pilot_readme.exists(), 'pilot archive README exists')
    if pilot_readme.exists():
        archive_text = pilot_readme.read_text(encoding='utf-8')
        status('ERROR', 'formal intercoder reliability' in archive_text and 'should not be cited' in archive_text, 'pilot archive warns against formal reliability citation')
    print('PILOT_SECOND_CODER_ARCHIVE: archived for calibration only; formal reliability check pending after codebook clarification')

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
summary = read_csv('screening_summary.csv')
ref = read_csv('reference_audit.csv')
product_snapshot = read_csv('product_ecosystem_snapshot.csv')
second_coder_blind = read_csv('core31_second_coder_blind.csv')
second_coder_formal = read_csv('core31_second_coder_formal_blind_template.csv')
second_coder_adjudication = read_csv('core31_second_coder_adjudication_template.csv')
record_classification = read_csv('record_classification_audit.csv')
repro_audit = read_csv('core_reproducibility_audit.csv')
repro_summary = read_csv('core_reproducibility_audit_summary.csv')

validate_product_ecosystem_snapshot(product_snapshot)
validate_second_coder_files(second_coder_blind, second_coder_adjudication, second_coder_formal)
validate_tracked_file_boundary()

expected_layers = {'Core': 31, 'Supporting': 66, 'Background': 95, 'Excluded': 20}
if corpus:
    status('ERROR', len(corpus) == 212, f'candidate records = {len(corpus)}; expected 212')
    layer_counts = Counter(r.get('corpus_layer', 'NA') for r in corpus)
    for layer, expected in expected_layers.items():
        status('ERROR', layer_counts.get(layer, 0) == expected, f'{layer} = {layer_counts.get(layer, 0)}; expected {expected}')

if core:
    status('ERROR', len(core) == 31, f'Core rows = {len(core)}; expected 31')
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
