"""Recompute public count views from canonical and source-level audit files."""
from __future__ import annotations
import csv
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parent
DATA=ROOT/'data'

def read(name):
    with (DATA/name).open('r',encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))

def write(name,rows,fields):
    with (DATA/name).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n'); w.writeheader(); w.writerows(rows)

corpus=read('corpus.csv')
cross=read('study_version_crosswalk.csv')
source=read('source_screening_audit.csv')
counted=[r for r in cross if r['counting_status']=='canonical_counted']
source_counts=Counter(r['corpus_layer'] for r in corpus)
canon_counts=Counter(r['analytical_layer'] for r in counted)
alternates=len(cross)-len(counted)

summary=[
 {'stage':'Source-specific search ledger','count':len(corpus),'note':'Source records retained in corpus.csv and source_screening_audit.csv; versions remain traceable.'},
 {'stage':'Canonical study/version resolution','count':alternates,'note':'Alternate or duplicate source records are linked to canonical studies in study_version_crosswalk.csv.'},
 {'stage':'Canonical candidate studies after version deduplication','count':len(counted),'note':'Analytical study counts use canonical studies rather than source-record rows.'},
 {'stage':'Study-level coded records','count':canon_counts['study_level_coded'],'note':'30 target-software studies plus one governance boundary record; existing coding and second-coder decisions are unchanged.'},
 {'stage':'Extended synthesis studies','count':canon_counts['extended_synthesis'],'note':'Canonical extended-synthesis studies after removing alternate versions and the CP189 false-positive source match.'},
 {'stage':'Background references','count':canon_counts['background_reference'],'note':'Background/reference canonical records for primitives, concepts, tools, benchmarks, methods, and ecosystem context.'},
 {'stage':'Excluded near-neighbor studies','count':canon_counts['excluded_near_neighbor'],'note':'Canonical excluded studies after version deduplication; source-level excluded rows remain traceable.'},
 {'stage':'Product ecosystem snapshot','count':23,'note':'Independent boundary layer in product_ecosystem_snapshot.csv; not part of source-record or canonical-study counts.'},
]
write('screening_summary.csv',summary,['stage','count','note'])

mapping=read('mapping_snapshot_counts.csv')
for row in mapping:
    if row['view']=='final_canonical_stratification':
        if row['category']=='extended synthesis studies': row['count']=str(canon_counts['extended_synthesis'])
        elif row['category']=='excluded near-neighbor studies': row['count']=str(canon_counts['excluded_near_neighbor'])
        row['denominator']=f"{len(counted)} canonical candidate studies"
    if row['category']=='product/system boundary snapshot':
        row['scope_note']='separate boundary layer; not included in source-record or canonical-study counts'
write('mapping_snapshot_counts.csv',mapping,list(mapping[0]))

log=read('source_search_log.csv')
by_source=defaultdict(Counter)
for row in source:
    by_source[row['source_bucket']][row['corpus_layer']]+=1
for row in log:
    c=by_source[row['source_id']]
    # Source rows are assigned once; canonical duplicate removal remains recorded separately.
    row['core_records']=str(c['Core'])
    row['background_records']=str(c['Background'])
    # Allocate canonical layers to the canonical record's source bucket.
    row['supporting_records']='0'; row['excluded_records']='0'
for row in counted:
    canonical_id=row['canonical_record_id']
    src=next(x['source_bucket'] for x in source if x['record_id']==canonical_id)
    target=next(x for x in log if x['source_id']==src)
    if row['analytical_layer']=='extended_synthesis': target['supporting_records']=str(int(target['supporting_records'])+1)
    if row['analytical_layer']=='excluded_near_neighbor': target['excluded_records']=str(int(target['excluded_records'])+1)
write('source_search_log.csv',log,list(log[0]))

print('source counts',dict(source_counts))
print('canonical counts',dict(canon_counts),'alternates',alternates)
