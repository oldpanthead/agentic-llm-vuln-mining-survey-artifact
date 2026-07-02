# V13 Case Box Manual Review

This note records the representative case boxes inserted into the v13 manuscript. The fields are grounded in the current Core synthesis matrix and existing BibTeX keys. No new external claims or new references were added.

## 案例 A

- 选择的 Core ID：C13
- 系统名称：PBFuzz
- BibTeX key：`zeng2025pbfuzz`
- 选择理由：Compared with DrillAgent, PBFuzz better matches the requested "feedback-driven fuzzing Agent" placement because the current matrix records directed fuzzing, PoV generation, Magma benchmark, and replay-like validation.
- 输入或候选：directed fuzzing 与 PoV 生成任务中的输入探索策略
- 运行时反馈：coverage、触发状态或 PoV 相关反馈
- 策略调整：基于执行反馈修正假设、调整 seed、选择新的输入或触发进一步验证
- 最强证据输出：可复现验证
- 外部审计材料：current matrix records no confirmed external audit materials for this row
- 声明边界：不要声称其发现真实新漏洞；应表述为 PoV 生成和已知漏洞触发
- 论文页码或章节：manuscript §5.2 case box; source matrix row C13
- 仍需人工确认：If the final paper wants page-specific support, verify the exact PBFuzz paper section/page for Magma, PoV, and replay-like validation details.

## 案例 B

- 选择的 Core ID：C30
- 系统名称：OSS-CRS
- BibTeX key：`chin2026osscrs`
- 选择理由：The current matrix records CRS, fuzzing, real OSS projects, source-limited unknown-bug claims, long-horizon orchestration, and reproducible validation, making it suitable for the long-running CRS workflow case.
- 环境：real OSS / AIxCC-style workflow environment
- 任务：跨阶段漏洞发现、触发、验证和报告任务
- 长程编排：CRS 工具链、fuzzing、执行观察、PoV 组织和报告流程
- 反馈：执行结果、验证状态或工具轨迹
- 系统输出：PoV、触发输入、验证结果、报告或 trajectory
- benchmark 背景：AIxCC-style or real OSS background
- 外部确认材料：作者报告的外部线索；specific issue/advisory/maintainer-confirmation chains remain source-limited in the current manuscript
- 声明边界：未知漏洞声明按原文来源限定方式记录；在缺少逐项外部确认链前，不视为声明级审计材料已经充分
- 论文页码或章节：manuscript §5.4 case box; source matrix row C30
- 仍需人工确认：If the final paper wants vulnerability-by-vulnerability external confirmation, verify issue/advisory/maintainer-confirmation links and target-version/environment alignment.
