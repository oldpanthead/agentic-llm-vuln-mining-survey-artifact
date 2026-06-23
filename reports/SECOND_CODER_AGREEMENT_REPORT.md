# Second-Coder Agreement Report

This report summarizes completed independent second-coder decisions for the 31 Core studies. It reports agreement before adjudication; it does not contain adjudicated final labels.

## Scope

- Coding task: strongest evidence output for all 31 Core studies.
- Coder2 input file: `data/core31_second_coder_blind.csv`.
- Published coder2 result file: `data/core31_second_coder_results.csv`.
- Baseline comparison file: `data/core31_second_coder_adjudication_template.csv`, using `original_strongest_evidence_output`.
- Adjudication status: pending; `adjudication_result` remains blank.

## Agreement

- Rows compared: 31
- Raw agreement: 0.581
- Cohen's kappa: 0.470
- Disagreements requiring adjudication: 13

Interpretation note: the kappa value should be described conservatively as moderate agreement. Final manuscript wording should distinguish this pre-adjudication agreement from any later adjudicated labels.

## Label Counts

| Evidence-output label | Original baseline | Coder2 |
|---|---:|---:|
| candidate judgment | 3 | 1 |
| controlled task completion | 5 | 5 |
| runtime safety signal | 8 | 4 |
| reproducible validation | 14 | 10 |
| externally traceable material | 0 | 10 |
| claim-level audit material | 0 | 0 |
| governance boundary case | 1 | 1 |

## Confusion Matrix

| Original \ Coder2 | candidate judgment | controlled task completion | runtime safety signal | reproducible validation | externally traceable material | claim-level audit material | governance boundary case |
|---|---:|---:|---:|---:|---:|---:|---:|
| candidate judgment | 1 | 0 | 0 | 0 | 2 | 0 | 0 |
| controlled task completion | 0 | 4 | 0 | 1 | 0 | 0 | 0 |
| runtime safety signal | 0 | 1 | 3 | 0 | 4 | 0 | 0 |
| reproducible validation | 0 | 0 | 1 | 9 | 4 | 0 | 0 |
| externally traceable material | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| claim-level audit material | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| governance boundary case | 0 | 0 | 0 | 0 | 0 | 0 | 1 |

## Disagreement Rows

| Core ID | System alias | Original baseline | Coder2 decision | Coder2 uncertainty note |
|---|---|---|---|---|
| C05 | Mut4All | runtime safety signal | externally traceable material | 未逐个核验外部 issue/修复链接；未记录任何触发 testcase 或敏感输入。 |
| C08 | BSFuzzer | runtime safety signal | externally traceable material | 未逐个打开 CVE 或 bounty 页面；公开论文只提供汇总性外部追踪信息。 |
| C09 | RFCAUDIT | candidate judgment | externally traceable material | 未逐个核验开发者记录；其主要输出仍是规范一致性 bug 报告。 |
| C11 | MALF | runtime safety signal | externally traceable material | CNVD 记录未逐项核验；工业靶场材料限制了公开复现性。 |
| C12 | NeTestLLM | runtime safety signal | controlled task completion | 其目标偏网络协议测试自动化，不是逐项目标软件漏洞复现；未检查每个历史 bug 的 replay。 |
| C17 | Multi-Agent Harnesses | reproducible validation | externally traceable material | 未打开 CVE 页面逐项核验；标签依据论文公开的外部 CVE 追踪材料。 |
| C19 | LIVA | candidate judgment | externally traceable material | 未逐个核验 CVE/CNVD；闭源 firmware 也限制完全复现。 |
| C20 | FirmAgent | reproducible validation | externally traceable material | 未逐项打开 CVE；不写入任何 PoC 或设备细节。 |
| C21 | PANGOLIN | runtime safety signal | externally traceable material | 未逐个核验厂商公告；公开材料主要提供汇总性外部追踪。 |
| C24 | BountyBench | controlled task completion | reproducible validation | 未运行 CI 或核验每个 bounty；理由不含 exploit 细节。 |
| C28 | FuzzingBrain V2 | reproducible validation | externally traceable material | 未逐个核验 maintainer/CVE 链接；不记录漏洞细节。 |
| C30 | OSS-CRS | reproducible validation | externally traceable material | 公开 claim chain 因披露窗口/细节保护并不完整；未写入 PoV 或补丁细节。 |
| C31 | GONDAR | reproducible validation | runtime safety signal | Zotero 未匹配全文，仅依据 arXiv 摘要；零日/OSS-CRS 外部链未独立核验，故保守不升到外部追踪。 |

## Security Boundary

The report records category-level agreement only. It does not include exploit payloads, undisclosed PoCs, sensitive crash inputs, private targets, credentials, or private communication.
