# Second-Coder Capability / Traceability Agreement Report

This report covers the rerun formal pre-adjudication second-coder check for two auxiliary Core-study fields after the strongest-evidence-output codebook clarification.

- Scope: 31-record study-level coded set (30 target-software studies plus one governance boundary case)
- Coder2 input: `data/core31_second_coder_capability_traceability_blind_template.csv`
- Completed coder2 results: `data/core31_second_coder_capability_traceability_results.csv`
- Author baseline for comparison: `data/v13_core_synthesis_matrix.csv`
- Fields compared: `agent_capabilities` and `external_audit_materials`
- Review materials: Zotero library records and available indexed/full-text attachments, supplemented by non-sensitive public artifact notes where Zotero full text was unavailable
- Adjudication status: no adjudicated labels are claimed in this report

Because cross-stage capability can be multi-label, this report does not use single-label Cohen's kappa for that field. Agreement is reported with row-level exact match, mean row Jaccard, micro precision/recall/F1 over label assignments, and per-label agreement/Jaccard. The external-traceability field is reported with the same set-style metrics for consistency.

## Agent-Increment / Cross-Stage Capability

- Rows compared: 31
- Row-level exact agreement: 20 / 31 = 0.645
- Mean row Jaccard: 0.772
- Micro precision over label assignments: 0.783
- Micro recall over label assignments: 0.947
- Micro F1 over label assignments: 0.857
- Row-level disagreements: 11

| Label | Baseline rows | Coder2 rows | Per-label agreement | Label Jaccard |
|---|---:|---:|---:|---:|
| 上下文聚合与规则提取 | 3 | 4 | 0.968 | 0.750 |
| 反馈解释与闭环调整 | 15 | 18 | 0.903 | 0.833 |
| 失败归纳与策略更新 | 4 | 6 | 0.935 | 0.667 |
| 工具选择与策略路由 | 3 | 7 | 0.871 | 0.429 |
| 角色讨论或文本反思 | 1 | 1 | 0.935 | 0.000 |
| 长程编排与状态管理 | 16 | 14 | 0.935 | 0.875 |
| 验证组织与证据打包 | 15 | 19 | 0.871 | 0.789 |

| Core ID | System | Author baseline | Coder2 decision |
|---|---|---|---|
| C03 | Multi-Agent Collaborative Smart Contract Fuzzing | 长程编排与状态管理 | 反馈解释与闭环调整; 失败归纳与策略更新; 长程编排与状态管理 |
| C10 | VulAgent | 上下文聚合与规则提取; 工具选择与策略路由; 角色讨论或文本反思 | 上下文聚合与规则提取; 工具选择与策略路由; 验证组织与证据打包 |
| C12 | NeTestLLM | 长程编排与状态管理 | 反馈解释与闭环调整; 长程编排与状态管理 |
| C14 | Co-RedTeam | 长程编排与状态管理 | 工具选择与策略路由; 长程编排与状态管理 |
| C15 | Real-world Pentest Agent Study | 长程编排与状态管理 | 工具选择与策略路由; 长程编排与状态管理 |
| C18 | PentestAgent | 长程编排与状态管理 | 工具选择与策略路由; 长程编排与状态管理 |
| C24 | BountyBench | 长程编排与状态管理 | 长程编排与状态管理; 验证组织与证据打包 |
| C27 | AgentFuzz | 长程编排与状态管理 | 角色讨论或文本反思 |
| C28 | FuzzingBrain V2 | 长程编排与状态管理 | 反馈解释与闭环调整; 失败归纳与策略更新; 长程编排与状态管理; 验证组织与证据打包 |
| C30 | OSS-CRS | 长程编排与状态管理 | 工具选择与策略路由; 长程编排与状态管理; 验证组织与证据打包 |
| C31 | GONDAR | 长程编排与状态管理 | 上下文聚合与规则提取 |

## External Traceability / External Audit Material

- Rows compared: 31
- Row-level exact agreement: 26 / 31 = 0.839
- Mean row Jaccard: 0.839
- Micro precision over label assignments: 0.839
- Micro recall over label assignments: 0.839
- Micro F1 over label assignments: 0.839
- Row-level disagreements: 5

| Label | Baseline rows | Coder2 rows | Per-label agreement | Label Jaccard |
|---|---:|---:|---:|---:|
| benchmark ground truth / 公开材料 | 3 | 3 | 0.935 | 0.500 |
| 作者报告的外部线索 | 11 | 8 | 0.839 | 0.583 |
| 未报告 | 17 | 20 | 0.903 | 0.850 |

| Core ID | System | Author baseline | Coder2 decision |
|---|---|---|---|
| C09 | RFCAUDIT | 作者报告的外部线索 | benchmark ground truth / 公开材料 |
| C19 | LIVA | 作者报告的外部线索 | 未报告 |
| C24 | BountyBench | benchmark ground truth / 公开材料 | 作者报告的外部线索 |
| C27 | AgentFuzz | 作者报告的外部线索 | 未报告 |
| C31 | GONDAR | 作者报告的外部线索 | 未报告 |

## Interpretation Boundary

These metrics are formal pre-adjudication agreement for two auxiliary Core-study fields. They do not imply that every artifact field has been double-coded, and they do not replace the separate strongest-evidence-output report in `reports/FORMAL_SECOND_CODER_AGREEMENT_REPORT.md`. The pilot round remains archived for codebook calibration only. Disagreements should be adjudicated separately if the manuscript later reports adjudicated auxiliary labels.

