# Formal Second-Coder Agreement Report

This report summarizes the formal pre-adjudication agreement between the author baseline and the completed second-coder pass for the strongest-evidence-output field across the 31 Core studies.

## Inputs

- Baseline labels: `data/core31_second_coder_adjudication_template.csv` field `original_strongest_evidence_output`.
- Second-coder labels: `data/core31_second_coder_formal_results.csv` field `coder2_strongest_evidence_output`.
- Scope: 31 Core studies.

## Agreement Statistics

- Rows compared: 31
- Agreements: 28
- Disagreements: 3
- Raw agreement: 0.903
- Cohen's kappa: 0.860

These are formal pre-adjudication agreement statistics. If disagreements are later adjudicated, adjudicated labels should be recorded separately and should not overwrite this pre-adjudication report.

## Disagreement Rows

| core_id | system_alias | author baseline | formal coder2 |
|---|---|---|---|
| C12 | NeTestLLM | runtime safety signal | controlled task completion |
| C17 | Multi-Agent Harnesses | reproducible validation | runtime safety signal |
| C24 | BountyBench | controlled task completion | reproducible validation |

## Notes

- The archived pilot round remains a calibration artifact only and is not cited as formal intercoder reliability.
- No adjudicated labels are claimed in this report.
