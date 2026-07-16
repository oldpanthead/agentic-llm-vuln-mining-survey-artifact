# Source-Parity Update Search Report

Date: 2026-07-16

This report records a source-parity check performed after the 2026-07-15 arXiv recall-recovery update. The purpose was to check whether official conference and publisher sources exposed formal records that were missed because the recall-recovery update itself used arXiv as its active search interface.

## Sources Checked

- USENIX Security 2026 official technical sessions: https://www.usenix.org/conference/usenixsecurity26/technical-sessions
- NDSS 2026 accepted papers page: https://www.ndss-symposium.org/ndss2026/accepted-papers/
- ACM DL and IEEE Xplore title/keyword web checks using the update-cohort query families and exact-title probes.
- SpringerLink and ScienceDirect title/keyword web checks using Agentic/LLM/vulnerability/fuzzing terms.

The detailed source rows are in `data/source_parity_update_20260716_search_log.csv`; record-level screening decisions are in `data/source_parity_update_20260716_screening_audit.csv`.

## Result

No corpus counts changed. The check introduced no new canonical candidate records, no new study-level coded records, and no new extended-synthesis records.

Two formal-source matches were already represented in the canonical corpus:

- PANGOLIN matched existing canonical record `CP094` / `CS_CP094`; the official USENIX page was already retained as the canonical source record.
- FirmAgent matched existing canonical record `CP089` / `CS_CP089`; the NDSS accepted-paper listing matched the existing DOI-backed record.

Several official-program or accepted-paper titles were screened as adjacent, public-program-only, or outside the target-software Agentic LLM vulnerability-mining scope at this check. Examples include Kintsugi, PatchWeaver, FidelityGPT, MUTATO, and NEXUS. They did not alter analytical denominators because they either lacked enough public full-text workflow/evidence material at the check or did not establish an Agentic LLM target-software vulnerability-mining workflow.

## Corpus Impact

The current manuscript-facing corpus remains:

- 253 source records;
- 248 canonical candidate studies;
- 68 study-level coded records, consisting of 67 target-software studies plus one governance boundary case;
- 65 extended synthesis studies;
- 95 background/reference records;
- 20 excluded near-neighbor studies.

The source-parity check is an audit closure file rather than a new source bucket in the main source-count ledger. It therefore validates publication-source symmetry without changing the canonical source-record totals.
