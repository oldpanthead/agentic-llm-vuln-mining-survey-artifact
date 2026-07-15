"""Create a transparent title/abstract and targeted-full-text audit for the July 2026 update search."""
from __future__ import annotations
import csv,re,unicodedata
from pathlib import Path

ROOT=Path(__file__).resolve().parent; DATA=ROOT/'data'
CUTOFF='2026-06-30T23:59:59Z'
FULLTEXT_ELIGIBLE=set('''2601.10865 2601.13933 2601.17762 2602.05721 2602.09774 2602.19490 2603.01154 2603.08616 2603.13384 2603.22577 2604.01442 2604.01977 2604.06506 2604.06618 2604.06633 2604.12172 2604.13611 2604.17184 2604.18718 2604.22427 2605.00034 2605.01739 2605.01885 2605.02346 2605.02789 2605.03956 2605.04251 2605.10074 2605.14431 2605.15097 2605.17444 2605.17450 2605.21824 2605.30105 2606.00669 2606.13037 2606.16420 2606.18619 2606.19149 2606.22263 2606.22647'''.split())
CONTEXTUAL=set('''2601.00509 2601.06177 2601.19138 2601.19239 2601.22952 2601.18847 2602.03271 2602.10487 2602.18689 2602.21892 2603.01272 2603.02297 2603.05689 2603.06365 2603.06858 2603.20637 2604.10767 2604.17948 2604.19049 2605.00413 2605.07737 2605.09350 2605.10834 2605.26548 2606.01364 2606.14164 2606.14261 2606.21397 2606.25973 2606.26216'''.split())
FULLTEXT_REVIEWED=set('''2601.00509 2601.06177 2601.10865 2601.13933 2601.17762 2601.19138 2601.19239 2601.22952 2602.03271 2602.05721 2602.09774 2602.10487 2602.18689 2602.19490 2603.01154 2603.01272 2603.06365 2603.06858 2603.08616 2603.13384 2603.20637 2603.22577 2604.01442 2604.01977 2604.06506 2604.06618 2604.06633 2604.10767 2604.12172 2604.17184 2604.17948 2604.18718 2604.19049 2604.22427 2605.00034 2605.00413 2605.01739 2605.01885 2605.02346 2605.02789 2605.03956 2605.04251 2605.07737 2605.09350 2605.10074 2605.14431 2605.15097 2605.17444 2605.17450 2605.21824 2605.30105 2606.00669 2606.13037 2606.14164 2606.14261 2606.16420 2606.18619 2606.19149 2606.22263 2606.22647'''.split())

def norm(s): return re.sub(r'[^a-z0-9]+',' ',unicodedata.normalize('NFKD',s or '').encode('ascii','ignore').decode().lower()).strip()
def read(name):
 with (DATA/name).open('r',encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))

results=read('submission_update_20260715_arxiv_results.csv'); corpus=read('corpus.csv'); ref=read('reference_audit.csv')
by_title={norm(r['title']):r['record_id'] for r in corpus}
by_arxiv={}
for r in ref:
 m=re.search(r'(\d{4}\.\d{4,5})', ' '.join([r.get('arxiv_id',''),r.get('official_url',''),r.get('doi','')]))
 if m: by_arxiv[m.group(1)]=r.get('record_id','')
fields=['arxiv_id','title','published','existing_record_id','screening_status','screening_level','decision_reason','analytical_implication','official_url','query_ids']
out=[]
for row in results:
 aid=row['arxiv_id']; existing=by_arxiv.get(aid) or by_title.get(norm(row['title'])) or ''
 if existing:
  status='existing_corpus_match'; level='identity_check'; reason=f'Matches existing source/canonical record {existing} by arXiv identifier or normalized title.'; implication='No new analytical count; retain version linkage.'
 elif row['published']>CUTOFF:
  status='outside_date_window'; level='date_filter'; reason='First arXiv submission is after the 2026-06-30 analytical cutoff.'; implication='Record only in the submission-time update ledger.'
 elif aid in FULLTEXT_ELIGIBLE:
  status='potentially_eligible_update_record'; level='full_text' if aid in FULLTEXT_REVIEWED else 'abstract_plus_metadata'; reason='Observable LLM/agent influence on tool use, inputs, feedback, validation, state, or vulnerability-handling workflow was identified; full study-level coding is required before inclusion in distributions.'; implication='Methodology blocker: do not fold into current denominators without first coding and extending reliability coverage.'
 elif aid in CONTEXTUAL:
  status='contextual_or_background_update'; level='full_text' if aid in FULLTEXT_REVIEWED else 'abstract_plus_metadata'; reason='Relevant to adjacent mechanisms, benchmarks, repair/evaluation, or governance context, but not selected as a new target-software study-level record in this audit.'; implication='May inform narrative/context after citation verification; does not enter current coded distributions.'
 else:
  title=row['title'].lower(); abstract=row['abstract'].lower()
  if any(k in title for k in ('survey','review','benchmark','empirical study','evaluation')):
   reason='Title/abstract describes a survey, benchmark, or evaluation context rather than a newly coded target-software Agentic vulnerability-mining workflow.'
  elif any(k in title for k in ('prompt injection','llm agent','agent security','openclaw','model context protocol','mcp ','agents under attack')):
   reason='Title/abstract focuses on the security of AI/agent systems or a neighboring governance topic rather than target-software vulnerability mining.'
  elif any(k in title for k in ('secure code generation','llm-generated code','coding agent','code generation')):
   reason='Title/abstract focuses on generated-code security or coding-agent behavior rather than an observable target-software vulnerability-mining workflow.'
  else:
   reason='Title/abstract does not meet the operational target-software Agentic workflow criterion used for the study-level coded set.'
  status='excluded_at_title_abstract_update'; level='title_abstract'; implication='No change to the frozen analytical corpus.'
 out.append({k:v for k,v in zip(fields,[aid,row['title'],row['published'],existing or 'NA',status,level,reason,implication,row['official_url'],row['query_ids']])})
with (DATA/'submission_update_20260715_screening_audit.csv').open('w',encoding='utf-8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n'); w.writeheader(); w.writerows(out)
from collections import Counter
print(Counter(r['screening_status'] for r in out)); print(Counter(r['screening_level'] for r in out))

