# Second-Coder Capability / Traceability Agreement Report

This report covers the formal pre-adjudication second-coder check for two auxiliary Core-study fields after the strongest-evidence-output codebook clarification.

- Scope: 31 Core studies
- Coder2 input: `data/core31_second_coder_capability_traceability_blind_template.csv`
- Completed coder2 results: `data/core31_second_coder_capability_traceability_results.csv`
- Author baseline for comparison: `data/v13_core_synthesis_matrix.csv`
- Fields compared: `agent_capabilities` and `external_audit_materials`
- Adjudication status: no adjudicated labels are claimed in this report

Because Agent-increment / cross-stage capability can be multi-label, this report does not use single-label Cohen's kappa for that field. Agreement is reported with row-level exact match, mean row Jaccard, micro precision/recall/F1 over label assignments, and per-label agreement/Jaccard. The external-traceability field is reported with the same set-style metrics for consistency.

## Agent-Increment / Cross-Stage Capability

- Rows compared: 31
- Row-level exact agreement: 31 / 31 = 1.000
- Mean row Jaccard: 1.000
- Micro precision over label assignments: 1.000
- Micro recall over label assignments: 1.000
- Micro F1 over label assignments: 1.000
- Row-level disagreements: 0

| Label | Baseline rows | Coder2 rows | Per-label agreement | Label Jaccard |
|---|---:|---:|---:|---:|
| 上下文聚合与规则提取 | 3 | 3 | 1.000 | 1.000 |
| 反馈解释与闭环调整 | 15 | 15 | 1.000 | 1.000 |
| 失败归纳与策略更新 | 4 | 4 | 1.000 | 1.000 |
| 工具选择与策略路由 | 3 | 3 | 1.000 | 1.000 |
| 角色讨论或文本反思 | 1 | 1 | 1.000 | 1.000 |
| 长程编排与状态管理 | 16 | 16 | 1.000 | 1.000 |
| 验证组织与证据打包 | 15 | 15 | 1.000 | 1.000 |

No row-level disagreements were observed for this field.

## External Traceability / External Audit Material

- Rows compared: 31
- Row-level exact agreement: 31 / 31 = 1.000
- Mean row Jaccard: 1.000
- Micro precision over label assignments: 1.000
- Micro recall over label assignments: 1.000
- Micro F1 over label assignments: 1.000
- Row-level disagreements: 0

| Label | Baseline rows | Coder2 rows | Per-label agreement | Label Jaccard |
|---|---:|---:|---:|---:|
| benchmark ground truth / 公开材料 | 3 | 3 | 1.000 | 1.000 |
| 作者报告的外部线索 | 11 | 11 | 1.000 | 1.000 |
| 未报告 | 17 | 17 | 1.000 | 1.000 |

No row-level disagreements were observed for this field.

## Interpretation Boundary

These metrics are formal pre-adjudication agreement for two auxiliary Core-study fields. They do not imply that every artifact field has been double-coded, and they do not replace the separate strongest-evidence-output report in `reports/FORMAL_SECOND_CODER_AGREEMENT_REPORT.md`. The pilot round remains archived for codebook calibration only.
