# V13 Final Synthesis Audit
Scope: 30 vulnerability-mining Core studies plus 1 governance-oriented boundary case (C27). Lifecycle coverage, Agent capabilities, and audit-material fields are overlapping. Strongest evidence output is mutually exclusive.
## lifecycle_coverage
| Category | Count | Core IDs | Field type | Includes governance boundary case | Note |
|---|---:|---|---|---|---|
| 候选发现与优先级排序 | 9 | C07;C09;C10;C14;C15;C16;C18;C19;C24 | overlapping | no |  |
| 路径与输入探索 | 20 | C01;C03;C04;C05;C06;C08;C11;C12;C13;C14;C15;C17;C18;C20;C21;C23;C26;C28;C30;C31 | overlapping | no |  |
| 执行观察与异常解释 | 20 | C01;C03;C04;C05;C06;C07;C08;C11;C12;C13;C14;C15;C18;C20;C21;C23;C26;C28;C30;C31 | overlapping | no |  |
| 复现与验证 | 15 | C02;C04;C07;C13;C16;C17;C20;C22;C24;C25;C26;C28;C29;C30;C31 | overlapping | no |  |
| 修复验证 | 4 | C04;C24;C25;C28 | overlapping | no |  |
| 报告、审计与披露 | 6 | C02;C04;C17;C26;C28;C30 | overlapping | no |  |

## agent_capabilities
| Category | Count | Core IDs | Field type | Includes governance boundary case | Note |
|---|---:|---|---|---|---|
| 上下文聚合与规则提取 | 3 | C09;C10;C19 | overlapping | no |  |
| 工具选择与策略路由 | 3 | C09;C10;C19 | overlapping | no |  |
| 反馈解释与闭环调整 | 15 | C01;C02;C04;C05;C06;C07;C08;C13;C16;C20;C21;C22;C25;C26;C29 | overlapping | no |  |
| 验证组织与证据打包 | 15 | C01;C02;C04;C05;C06;C07;C08;C13;C16;C20;C21;C22;C25;C26;C29 | overlapping | no |  |
| 长程编排与状态管理 | 15 | C03;C04;C11;C12;C13;C14;C15;C17;C18;C23;C24;C26;C28;C30;C31 | overlapping | no |  |
| 失败归纳与策略更新 | 4 | C04;C13;C17;C26 | overlapping | no |  |
| 治理、人机门控与披露控制 | 0 |  | overlapping | no |  |

## strongest_evidence_output
| Category | Count | Core IDs | Field type | Includes governance boundary case | Note |
|---|---:|---|---|---|---|
| 候选判断 | 3 | C09;C10;C19 | mutually_exclusive | no |  |
| 受控任务完成 | 5 | C14;C15;C18;C23;C24 | mutually_exclusive | no |  |
| 运行时安全信号 | 8 | C01;C03;C05;C06;C08;C11;C12;C21 | mutually_exclusive | no |  |
| 可复现验证 | 14 | C02;C04;C07;C13;C16;C17;C20;C22;C25;C26;C28;C29;C30;C31 | mutually_exclusive | no |  |
| 治理风险 | 1 | C27 | mutually_exclusive | yes |  |

## external_audit_reproducibility
| Category | Count | Core IDs | Field type | Includes governance boundary case | Note |
|---|---:|---|---|---|---|
| 可追溯 artifact 或公开系统材料 | 18 | C01;C02;C04;C05;C07;C08;C09;C17;C18;C19;C21;C23;C24;C25;C26;C28;C30;C31 | overlapping | no | conservative count: excludes metadata-only records |
| artifact 不完整、受限或未明确 | 12 | C03;C06;C10;C11;C12;C13;C14;C15;C16;C20;C22;C29 | overlapping | no | complement of public artifact count among 30 vulnerability-mining Core |
| 明确报告目标版本 | 0 |  | overlapping | no | based on version_reported field |
| 明确报告运行环境 | 30 | C01;C02;C03;C04;C05;C06;C07;C08;C09;C10;C11;C12;C13;C14;C15;C16;C17;C18;C19;C20;C21;C22;C23;C24;C25;C26;C28;C29;C30;C31 | overlapping | no | based on environment_reported field |
| 提供 replay package、PoC / PoV 状态或等价验证材料 | 12 | C02;C04;C07;C13;C16;C17;C20;C22;C25;C26;C28;C29 | overlapping | no | keyword-assisted count from audited notes |
| 提供结构化日志、失败样本或完整 trace | 1 | C24 | overlapping | no | keyword-assisted count from audited notes |
| 作者报告的外部线索 | 10 | C07;C08;C09;C11;C19;C20;C21;C28;C30;C31 | overlapping | no | based on external_audit_materials field |
| 可公开追踪的外部材料 | 13 | C07;C08;C09;C11;C19;C20;C21;C24;C26;C28;C29;C30;C31 | overlapping | no | author-reported external traces plus benchmark/public material |
| 声明级材料对齐较充分 | 0 |  | overlapping | no | strict claim-level audit-ready count; expected zero |

## Manual review items

- Counts are derived from the current v13 natural-language Core matrix and public artifact fields.
- Public artifact counts use a conservative rule and do not treat `public metadata status recorded` alone as an artifact.
- Claim-level audit-ready materials remain zero under the current strict policy.
