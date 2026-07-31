#!/usr/bin/env python3
"""Build an auditable, provisional full-text assessment for the final search.

The output records AI-assisted recommendations only. It does not convert those
recommendations into author decisions or study-level coding. New study-level
records require accessible full text, author confirmation, and human
second-coder review under the current codebook.
"""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RECOMMENDATIONS = DATA / "final_multisource_search_20260730_screening_recommendations.csv"
ACCESS = DATA / "final_multisource_search_20260730_fulltext_access.csv"
EVIDENCE = DATA / "final_multisource_search_20260730_fulltext_evidence.csv"
OUTPUT = DATA / "final_multisource_search_20260730_fulltext_assessment.csv"


STUDY_LEVEL = {
    "FMS0120", "FMS0412", "FMS0443", "FMS0558", "FMS0659", "FMS0752",
    "FMS0961", "FMS1081", "FMS1228",
    "FMS0219", "FMS0347", "FMS0488", "FMS0614", "FMS0742", "FMS0775",
    "FMS0782", "FMS0800", "FMS0913", "FMS0916", "FMS1041", "FMS1076",
    "FMS1155", "FMS1233", "FMS1265", "FMS1283", "FMS1334", "FMS1530",
    "FMS1592",
    "FMS0090", "FMS0100", "FMS0105", "FMS0109", "FMS0134", "FMS0135",
    "FMS0145", "FMS0151", "FMS0152", "FMS0212", "FMS0214", "FMS0226",
    "FMS0239", "FMS0254", "FMS0257", "FMS0260",
    "FMS0267", "FMS0269", "FMS0270", "FMS0271", "FMS0272", "FMS0275",
    "FMS0281", "FMS0284", "FMS0288", "FMS0297", "FMS0362", "FMS0372",
    "FMS0376", "FMS0389", "FMS0401", "FMS0435", "FMS0479", "FMS0489",
    "FMS0500", "FMS0509", "FMS0533", "FMS0538", "FMS0541",
    "FMS0575", "FMS0577", "FMS0598", "FMS0606", "FMS0619", "FMS0648",
    "FMS0650", "FMS0676", "FMS0677",
    "FMS0684", "FMS0698", "FMS0718", "FMS0733", "FMS0734", "FMS0741",
    "FMS0747", "FMS0753", "FMS0768", "FMS0842", "FMS0850", "FMS0885", "FMS0890",
    "FMS0904", "FMS0911", "FMS0914", "FMS0922", "FMS0925", "FMS0927",
    "FMS0933", "FMS0935", "FMS0945", "FMS0957", "FMS0964", "FMS0966",
    "FMS0969", "FMS1017", "FMS1024", "FMS1034", "FMS1055", "FMS1063",
    "FMS1083",
    "FMS1084", "FMS1085", "FMS1087", "FMS1088", "FMS1093", "FMS1095",
    "FMS1096", "FMS1098", "FMS1135", "FMS1136", "FMS1148", "FMS1149",
    "FMS1161", "FMS1227", "FMS1239", "FMS1261", "FMS1275", "FMS1279",
    "FMS1321",
    "FMS1338", "FMS1394", "FMS1398", "FMS1473", "FMS1492", "FMS1509", "FMS1514", "FMS1561",
    "FMS1586", "FMS1605", "FMS1607", "FMS1613", "FMS1618", "FMS1635",
    "FMS1639", "FMS1640",
    # Retrieved after removing the erroneous historical-arXiv skip rule.
    "FMS0206", "FMS0258", "FMS0494", "FMS0651", "FMS0968", "FMS1299",
    "FMS1316", "FMS1571", "FMS1573",
}

EXTENDED = {
    "FMS0209", "FMS0307", "FMS0419", "FMS0513", "FMS0707", "FMS0755",
    "FMS0825", "FMS0844", "FMS0899", "FMS0928", "FMS1002", "FMS1128",
    "FMS1219", "FMS1315", "FMS1325", "FMS1326", "FMS1390", "FMS1602",
    "FMS1637", "FMS1641",
    "FMS0233", "FMS0327", "FMS0374", "FMS0384", "FMS0426",
    "FMS0642", "FMS0686", "FMS0691", "FMS0888", "FMS0947", "FMS1090",
    "FMS1103", "FMS1125", "FMS1154", "FMS1166", "FMS1174", "FMS1193",
    "FMS1223", "FMS1381", "FMS1435", "FMS1491", "FMS1512", "FMS1549",
    "FMS1600", "FMS1601", "FMS1638",
    "FMS0048", "FMS0143", "FMS0205", "FMS0253", "FMS0274", "FMS0279", "FMS0280",
    "FMS0364", "FMS0604",
    "FMS0457", "FMS0605", "FMS0613", "FMS0678",
    "FMS0744", "FMS0789", "FMS0831", "FMS0886", "FMS0891", "FMS0902",
    "FMS0948", "FMS0994", "FMS1031", "FMS1040", "FMS1054", "FMS1144",
    "FMS1175", "FMS1218", "FMS1312", "FMS1323", "FMS1389", "FMS1495",
    "FMS1577",
    "FMS0049", "FMS0410", "FMS0600", "FMS0944", "FMS1021", "FMS1399",
    "FMS1469", "FMS1489", "FMS1630",
}

BACKGROUND = {
    "FMS0146", "FMS0148", "FMS0230", "FMS0263", "FMS0335", "FMS0578",
    "FMS0615", "FMS0618", "FMS0637", "FMS0705", "FMS0946", "FMS0998",
    "FMS1082",
    "FMS1164", "FMS1464",
    "FMS0128", "FMS0140", "FMS0661", "FMS0664", "FMS0990", "FMS1004",
    "FMS1236", "FMS1461", "FMS1518",
}

EXCLUDED = {
    "FMS0016", "FMS0166", "FMS0266", "FMS0367", "FMS0530", "FMS0568",
    "FMS0580", "FMS0584", "FMS0713", "FMS1127", "FMS1196", "FMS1293",
    "FMS1307",
    "FMS0717",
}

VERSION_RELATIONS = {
    "FMS0444": ("alternate_version_existing", "U10", "ContraFix title/version variant of the current study-level record."),
    "FMS0708": ("alternate_version_new", "FMS0457", "Formal CovRL version; count once with the formal version preferred."),
    "FMS1318": ("alternate_version_existing", "C11", "Formal MALF journal version of the current study-level record."),
}

SPECIFIC_NOTES = {
    "FMS0120": "AEGIS uses a clue detector, on-demand code-property-graph slicing, a verifier agent, and an audit agent so intermediate hypotheses determine later repository evidence retrieval and verdict review.",
    "FMS0209": "APPATCH stages semantic slicing, exemplar selection, patch generation, and ensemble LLM validation, but follows a fixed orchestration without execution feedback changing a later tool-mediated action.",
    "FMS0307": "The LLM predicts target call stacks before directed fuzzing; runtime feedback remains inside the fuzzer and does not return to an LLM-controlled decision.",
    "FMS0412": "Codexity returns Infer or CppCheck findings to the LLM and iterates repair until the analyzer accepts the generated program or the attempt limit is reached.",
    "FMS0419": "CommitShield combines static-analysis output with LLM-generated descriptions and patch context in a fixed detector rather than an adaptive Agent-runtime loop.",
    "FMS0443": "ContractTinker combines static program context with successive LLM roles; a validator's rejection and recommendations trigger another LLM refinement before downstream compilation and manual checks.",
    "FMS0513": "deepSURF uses static analysis and LLM-selected constructor context to augment Rust fuzzing harnesses, while coverage and crash feedback remain within the downstream fuzzer.",
    "FMS0558": "DREA separates a planning agent from an explorer agent so vulnerability hypotheses trigger on-demand repository-context retrieval and later reasoning updates.",
    "FMS0659": "The OSS-Fuzz repair workflow uses agent-selected repository context, patch generation, oracle execution, and iteration feedback to revise later patches.",
    "FMS0707": "The BusyBox study uses LLM-generated initial seeds and replays crashes from related targets, but does not return runtime feedback to an LLM-controlled next action.",
    "FMS0752": "HarnessAgent routes source-retrieval, compilation, repair, and harness-validation tools; build and validation failures change subsequent harness-generation actions.",
    "FMS0755": "The OpenCV workflow uses documentation to generate fuzzing inputs before execution, without an observable feedback transition back to the LLM.",
    "FMS0825": "The study uses LLMs to enhance metamorphic fuzzing oracles, while the evaluated execution path remains a fixed testing pipeline.",
    "FMS0844": "KQFuzz grounds LLM seed generation in codebase knowledge, then applies fitness evaluation and deterministic mutations without returning fuzzing feedback to the LLM.",
    "FMS0899": "LLAMAFUZZ uses an LLM to improve structured-input generation for greybox fuzzing, but the reviewed workflow does not expose adaptive Agent-runtime control of later executions.",
    "FMS0928": "LLM4Fuzz converts LLM predictions into smart-contract fuzzing guidance; runtime exploration proceeds without a later LLM-controlled feedback step.",
    "FMS0961": "The study executes tool-using agents in Docker sandboxes across controlled prompt conditions and records their multi-step vulnerability-exploitation trajectories.",
    "FMS1002": "MirrorFuzz uses LLM-derived shared-bug knowledge to generate deep-learning API tests before fuzz execution, without an LLM-controlled runtime feedback loop.",
    "FMS1081": "Pen-Strategist converts generated strategies into actionable steps, integrates with pentesting frameworks and MCP tools, and records iterative execution outcomes on vulnerable machines.",
    "FMS1128": "ProphetFuzz predicts risky option combinations from documentation and then launches fuzzing; runtime outcomes do not control another LLM decision.",
    "FMS1219": "SAFuzz uses LLM-based semantic prediction to allocate fuzzing resources and define oracles, while runtime feedback is not interpreted by an LLM agent.",
    "FMS1228": "SCAFFOLD-CEGIS runs tests, static analysis, and anchor checks after each candidate; structured failures are retained and passed to later implementation attempts.",
    "FMS1315": "SeedAIchemy uses LLM workflows to construct an initial seed corpus, but the subsequent fuzzer does not feed execution observations back to the LLM.",
    "FMS1325": "ConSeT uses an LLM to infer cross-field protocol constraints before deterministic semantic test generation and execution; observed crashes do not alter a later LLM action.",
    "FMS1326": "SemFuzz uses LLM-derived protocol semantics to guide fuzzing, but the reviewed control path does not expose LLM interpretation of runtime feedback.",
    "FMS1390": "StatePre uses an LLM-produced protocol state representation to prepare fuzzing, without evidence that runtime results change a later LLM-controlled action.",
    "FMS1602": "VWAttacker uses LLM-assisted property extraction and test generation, followed by deterministic mutation and oracles rather than an adaptive LLM feedback loop.",
    "FMS1637": "DFUZZ extracts transferable edge cases with an LLM and applies them in deep-learning API fuzzing, while runtime feedback remains outside LLM control.",
    "FMS1641": "zkCraft uses an LLM as a zero-shot mutation-pattern oracle before deterministic ZK-circuit fuzzing; execution results do not trigger a later LLM decision.",
    "FMS0219": "The black-box arm evaluates a shared-state Agentic Reasoning Graph with bounded tool execution, proof gates, and evidence-backed reporting on web targets.",
    "FMS0233": "Assertain iterates LLM generation and self-reflection over RTL context, but the evaluated workflow does not feed formal-tool execution results back into a later LLM-controlled action.",
    "FMS0327": "LSAST supplies retrieved vulnerability knowledge to an LLM-supported static scan in a fixed pipeline without observable adaptive tool or execution control.",
    "FMS0347": "Bulkhead agents recover paths, generate PoCs, use validation results to guide patching, and formally check the resulting container-escape repairs.",
    "FMS0374": "VSP applies structured chain-of-thought prompts to vulnerability identification, discovery, and patching without an observable Agent runtime or tool-feedback transition.",
    "FMS0384": "ChiralDetector combines path extraction, LLM semantic judgment, strict validation, and root-cause reporting in a staged pipeline, but validation does not change a later LLM-controlled action.",
    "FMS0426": "The MCP analysis combines static slicing with LLM semantic checks and separate exploitation analysis; the LLM does not control an adaptive tool-feedback loop.",
    "FMS0488": "CVE-Bench executes LLM agents in sandboxed web applications and judges their multi-step exploit actions against vulnerability-specific success conditions.",
    "FMS0614": "The study launches repository-aware CLI agents in isolated plugin workspaces and evaluates the reports produced after agent-selected code inspection across repeated runs.",
    "FMS0642": "FSTab analyzes recurring vulnerabilities in agent-generated applications, but the vulnerability-mining method is a black-box prediction and validation study rather than an adaptive Agentic workflow.",
    "FMS0686": "The paper develops severity reporting for vulnerabilities in LLM-generated code without an observable Agent runtime controlling analysis or validation tools.",
    "FMS0691": "RSA uses human-driven multi-round prompting to obtain exploits for known CVEs; the prompting rounds are not an autonomous Agent runtime or tool-feedback loop.",
    "FMS0742": "CodeQL findings and LLM-produced explanations are returned as structured feedback for later code repair, yielding an observable analysis-to-repair transition.",
    "FMS0775": "The study directly executes and compares established autonomous repair agents, then evaluates the security properties of their repository patches.",
    "FMS0782": "The secure-code agent repeatedly runs Bandit, returns findings to the LLM, and repairs generated Python code until the security condition or iteration limit is reached.",
    "FMS0800": "Compiler, CodeQL, and KLEE results drive iterative LLM repair, with successful prior repairs retrieved to guide later candidates.",
    "FMS0888": "The LLM produces command-injection findings and test suggestions, while execution validation is performed as a downstream study procedure rather than an adaptive Agentic loop.",
    "FMS0913": "The study executes project-scale LLM and agent-centric detectors, including multi-agent repository analysis, and compares their observable findings and resource use.",
    "FMS0916": "SAST-Genius passes Semgrep findings into an LLM triage and PoC-generation workflow so candidate decisions determine later validation actions.",
    "FMS0947": "The study evaluates prompt-based smart-contract vulnerability classification without an Agent runtime, adaptive tool selection, or target-execution feedback.",
    "FMS1041": "TMV-Hunter uses GUI agents to explore Android applications, observe network behavior, and expose TLS-validation failures before downstream attribution.",
    "FMS1076": "PatchEval executes code and repair agents on CVE tasks and validates their patches with security and functionality tests in runtime sandboxes.",
    "FMS1090": "The empirical component evaluates static analyzers and human labels; persistent human-feedback retrieval is proposed as a conceptual framework rather than an evaluated Agentic workflow.",
    "FMS1103": "The paper evaluates an LLM-supported human collaboration process for remediation, not an autonomous Agent runtime that controls target-software tools or validation.",
    "FMS1125": "PromptAudit fixes the dataset and execution pipeline while varying prompts for vulnerability classification; it is an evaluation study rather than an Agentic control workflow.",
    "FMS1154": "RealSec-bench constructs and validates secure-code-generation tasks; its LLM filtering and human validation belong to benchmark construction rather than an evaluated Agentic miner.",
    "FMS1155": "RealVuln runs general-purpose LLM scanners in tool-using agent mode, including iterative repository exploration and shell-mediated analysis, and compares their findings.",
    "FMS1166": "ReDetect applies LLM-extracted rules, graph learning, and static or taint checks in a fixed hybrid detector without adaptive Agent-runtime control.",
    "FMS1174": "The framework localizes a vulnerable regex symbolically, invokes an LLM once for repair, and validates afterward without feeding validation results into another LLM-controlled action.",
    "FMS1193": "ReVul-CoT is a retrieval-augmented vulnerability assessment model evaluated as a fixed prediction pipeline, not an Agentic tool-feedback workflow.",
    "FMS1223": "SALLM is a secure-code-generation benchmark and execution environment; it does not evaluate an LLM that adaptively controls the security checks.",
    "FMS1233": "SCGAgent selects relevant security guidance, generates tests, and iteratively revises code while preserving functional and security state across steps.",
    "FMS1265": "SecureVibeBench executes repository-editing code agents and checks their patches with functionality tests, PoCs, SAST, and dynamic security oracles.",
    "FMS1283": "The supply-chain analysis agent uses a teacher-verifier-student loop to revise semantic lifting before graph-based global vulnerability reasoning.",
    "FMS1334": "ShadowProbe uses LLM-assisted execution-context reconstruction and test-input synthesis, then runs candidates and interprets timing growth to validate complexity vulnerabilities.",
    "FMS1381": "Soley trains and evaluates a transformer-based logic-vulnerability detector; its iterative training procedure is not an Agentic vulnerability-mining workflow.",
    "FMS1435": "The Code Whisperer presents a fixed graph-and-LLM detection and repair pipeline; logged CI feedback is described as a future improvement path rather than evaluated Agent control.",
    "FMS1491": "The study applies prompting strategies to filter SAST findings without an observable Agent runtime or feedback-driven tool transition.",
    "FMS1512": "TraceLLM maps collected Ethereum traces and contract code into anomaly findings and reports through a fixed analysis pipeline rather than adaptive Agent control.",
    "FMS1530": "TypePilot assigns generation, vulnerability review, and refinement to successive LLM roles so earlier findings change the retained code passed to later roles.",
    "FMS1549": "USCSA performs AST differencing followed by LLM-assisted attribution in a fixed staged analyzer without tool feedback changing later LLM action.",
    "FMS1592": "VULEUT converts reachability results and vulnerability context into generated unit tests that are executed to verify third-party-library triggerability.",
    "FMS1600": "VulStamp is a reinforcement-learning vulnerability-severity model; its training feedback is not Agent-runtime control over target-software analysis or validation.",
    "FMS1601": "VulWeaver builds dependency graphs and performs LLM-based vulnerability classification in a fixed detector without adaptive tool or execution feedback.",
    "FMS1638": "Zer0n combines LLM analysis with blockchain report hashing, but active exploitation is out of scope and the evaluated workflow does not expose adaptive tool-feedback control.",
    "FMS0090": "Two execution validators return payload and path feedback to an adaptive prompting loop that iteratively revises generated web-vulnerability PoCs.",
    "FMS0100": "A generator and validator form a bounded repair loop; validator feedback revises the role-permission patch until it passes or the attempt limit is reached.",
    "FMS0135": "The title indicates a multimodal smart-contract vulnerability-detection agent, but no public full text was retrieved; do not count or code it without full-text review.",
    "FMS0205": "Repository-scale prioritization and comparative validation are relevant, but the available description does not establish adaptive tool or execution control by the LLM.",
    "FMS0239": "ATLANTIS combines LLM agents with static analysis, symbolic execution, directed fuzzing, PoV generation, patching, and fallback scheduling in an evaluated CRS.",
    "FMS0253": "The visible workflow is a fixed EMBA-to-Ghidra-to-LLM pipeline; no LLM decision changes a later tool action or retained state.",
    "FMS0279": "The two-stage detector and LLM localization pipeline provides adjacent candidate-analysis evidence but does not establish an Agentic tool-feedback loop.",
    "FMS0297": "JitVul evaluates ReAct agents that request interprocedural context, observe retrieved code, and iteratively refine repository-level vulnerability judgments.",
    "FMS0362": "FDSP feeds compiler and Bandit findings back to the LLM so that later patch candidates respond to external tool results.",
    "FMS0364": "Snitch recursively applies a fixed prompt to repository files and is compared with Bandit; the evaluated agent does not control Bandit or adapt later actions from execution feedback.",
    "FMS0376": "Chaintrix routes LLM-generated findings through deterministic structural checks and selected symbolic-execution or fuzz validation before reporting.",
    "FMS0389": "The LLM produces executable graph queries and an auxiliary model refines query generation; full text shows an observable analysis-tool transition.",
    "FMS0444": "The current corpus already counts ContraFix; retain this title/version as provenance rather than a new study.",
    "FMS0479": "Agents iteratively formalize protocols, invoke Tamarin, and adapt to prover feedback until a counterexample is found or the call budget is exhausted.",
    "FMS0533": "VIC-RAGENT passes structured intermediate judgments through specialized agents and uses audit-supervisor validation feedback before the final commit classification.",
    "FMS0541": "LLM-produced security markings change KLEE path prioritization and KLEE emits replayable test inputs.",
    "FMS0575": "The title and abstract describe an AutoPentester LLM agent framework, but public full text is still needed before eligibility can be confirmed.",
    "FMS0604": "ETrace interprets already-collected transaction traces in a fixed analysis path; no feedback from target execution changes a later LLM-controlled action.",
    "FMS0619": "The title and abstract describe multi-agent vulnerable-code repair, but public full text is still needed to verify executable validation or tool-mediated state transitions.",
    "FMS0677": "The study executes existing pentesting agents against expert-annotated real-world targets and evaluates their multi-step tool trajectories and validated findings.",
    "FMS0684": "The ReAct agent selects interprocedural context tools, observes their output, and iterates before classifying a patch.",
    "FMS0708": "Same CovRL study as FMS0457; prefer the formal ACM version for metadata while preserving the arXiv source.",
    "FMS0733": "The graph-of-thought workflow combines dynamic reasoning-path exploration with static-analysis operations; full-text access is still needed for coding.",
    "FMS0734": "GPTScan couples LLM-selected variables and statements to static confirmation, so the LLM decision changes a later tool-mediated validation action.",
    "FMS0831": "The LLM generates the initial seed corpus, but runtime feedback does not return to the LLM or agent runtime.",
    "FMS0885": "VulTrial passes vulnerability arguments among specialized agents over multiple discussion rounds before a review-board verdict.",
    "FMS0886": "GPT-4 generates vulnerability-witnessing tests in a one-shot/semi-automated workflow whose validation remains manual.",
    "FMS0891": "The agents assess ecosystem and project risk rather than discover or validate target-software vulnerabilities.",
    "FMS0902": "The evaluated system is a fixed retrieval-detection-report pipeline, while a feedback mechanism is described as future work; retain it as adjacent synthesis rather than study-level evidence.",
    "FMS0925": "LLM-SmartAudit uses specialized conversational agents and iterative feedback to move from contract analysis through vulnerability identification to a final audit report.",
    "FMS0948": "LogicScan performs contrastive, LLM-assisted auditing, but the available material does not establish an adaptive Agent runtime controlling tools or execution.",
    "FMS0957": "Generator and discriminator agents exchange vulnerability feedback and retain difficult cases; full text is still needed before study-level coding.",
    "FMS1031": "The LLM labels a batch prioritization substrate for later analysts or agents; the paper does not itself perform downstream vulnerability mining.",
    "FMS1054": "LLMs synthesize reusable generators as a one-time setup step; the subsequent fuzzer is not controlled by an LLM agent.",
    "FMS1055": "LASiR uses LLM-selected semantic variables and warning review to guide static taint analysis and symbolic path-reachability verification.",
    "FMS1144": "QuiLL is an LLM evaluation framework and explicitly leaves agentic extension to future work.",
    "FMS1239": "SEC-bench Pro evaluates long-horizon software-security agents, but public full text is still needed before study-level coding.",
    "FMS1275": "Security agents use fuzzing, static analysis, runtime monitoring, and iterative patch prompts; full text is needed for coding.",
    "FMS1318": "MALF is already counted as C11; update the canonical metadata to the formal journal version after verification.",
    "FMS1323": "The paper presents semantic input mutation, while dynamic feedback to an LLM-controlled next action is described as future work.",
    "FMS1338": "Agent frameworks inspect repository context and tool findings to filter SAST alerts; full text is needed for coding.",
    "FMS1389": "STAF iteratively refines generated security tests, but executable tool feedback is proposed as future work.",
    "FMS1394": "StealthBench executes tool-calling offensive agents in containerized targets and retains complete action-observation trajectories for judged task outcomes.",
    "FMS1473": "Compiler, CodeQL, and KLEE results drive iterative LLM repair, while successful repair patterns are retained across tasks and final candidates undergo symbolic validation.",
    "FMS1495": "The study contributes an LLM-assisted 5G vulnerability-detection and repair case, but the available material does not establish an adaptive Agent runtime controlling execution feedback.",
    "FMS1613": "The LLM translates program logic into a formal model that is checked by a verifier; full text is needed to confirm whether verification affects later action.",
    "FMS1640": "The benchmark evaluates agents on finding and patching unseen vulnerabilities; full text is needed for study-level coding.",
    "FMS0049": "The contribution is prompt-based vulnerability detection; the reviewed workflow does not show an LLM decision changing a later security-tool or execution action.",
    "FMS0128": "Agent-Fence evaluates the security of deep-research agents and therefore contributes governance and agent-security context rather than target-software vulnerability mining.",
    "FMS0140": "The work studies agentic adversarial rewriting against black-box NLP pipelines, outside the target-software vulnerability-mining denominator.",
    "FMS0206": "Antiproof uses LLM agents to refine static detectors from verifier feedback and generate executable PoV/PoE artifacts checked by deterministic oracles.",
    "FMS0258": "STITCH agents configure builds, refine specifications from compilation and test outcomes, triage crashes, and prepare minimized reproducers and reports.",
    "FMS0410": "CodeHacker supplies an adjacent iterative code-and-test generation mechanism, but its evaluated target is competitive-programming correctness rather than vulnerability mining.",
    "FMS0494": "CyberChainBench evaluates coding agents in a tool call/result loop that detects, exploits, and patches smart contracts on block-anchored historical forks.",
    "FMS0600": "ESAA-Security proposes an event-sourced agent-assisted audit architecture with executable checks, but the reviewed material does not establish an evaluated target-software workflow sufficient for study-level coding.",
    "FMS0651": "Favia uses a ReAct agent and repository tools to iteratively judge causal alignment between CVEs and candidate vulnerability-fixing commits.",
    "FMS0661": "FLARE fuzzes LLM multi-agent applications; it is relevant to the security of agent systems rather than an Agentic LLM mining vulnerabilities in target software.",
    "FMS0664": "FlowSteer attacks multi-agent planning workflows and therefore supplies agent-security context rather than target-software evidence.",
    "FMS0717": "The paper concerns gameplay video question answering and is unrelated to software vulnerability discovery or validation.",
    "FMS0944": "CLAWAUDIT audits agent-runtime source code, but the auditing method is a static analysis pipeline rather than an observable Agentic tool-feedback workflow.",
    "FMS0968": "Mastermind repeatedly plans, executes, verifies, and updates strategy for repository-scale PoC reproduction and patched-build checking.",
    "FMS0990": "MESA addresses security of multi-agent communication and contributes governance context rather than target-software vulnerability-mining evidence.",
    "FMS1004": "SPELLSMITH mitigates MCP tool-description taint in agent applications; it is retained as agent-security background rather than target-software discovery evidence.",
    "FMS1021": "MulVul provides retrieval-augmented multi-agent vulnerability classification and prompt refinement without an observable target execution or security-tool feedback loop.",
    "FMS1236": "ScopeJudge is a pre-execution policy gate for offensive agents and informs governance controls rather than target-software study-level coding.",
    "FMS1299": "The CrewAI workflow passes state across Planner, Analyzer, Fixer, and Verifier roles, with an MCP CodeQL variant evaluated on curated CVE tasks.",
    "FMS1316": "SeedSmith agents query code context, generate seeds, execute them against sanitizer-instrumented binaries, and correct later seeds from execution feedback.",
    "FMS1399": "The multi-agent debate framework evaluates code-vulnerability classification without target execution or an observable security-tool feedback transition.",
    "FMS1461": "PhishNChips evaluates attacks on agentic systems and is retained as agent-security background rather than target-software evidence.",
    "FMS1469": "ReasonVul uses multi-agent reasoning and revision for code-vulnerability detection but does not establish tool-mediated target execution or validation.",
    "FMS1489": "The work evaluates compositional LLM reasoning for smart-contract vulnerability detection without an observable Agent runtime controlling tools or execution feedback.",
    "FMS1518": "The paper studies thought-transition injection attacks against LLMs and is outside target-software vulnerability mining.",
    "FMS1571": "VEXAIoT agents plan and execute offensive tools, observe command results, validate success or failure, and adapt retries and subsequent attacks in controlled testbeds.",
    "FMS1573": "VIPER-MCP feeds static call chains and execution fitness into an evolutionary prompt-fuzzing loop that produces sandboxed end-to-end exploit traces.",
    "FMS1630": "The study analyzes failures of LLM-based vulnerability patching and contributes adjacent repair-evaluation evidence rather than a new Agentic target-software workflow.",
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def index(path: Path) -> dict[str, dict[str, str]]:
    return {row["discovery_id"]: row for row in read_rows(path)}


def source_locations(evidence: dict[str, str], access: dict[str, str], url: str) -> str:
    pages = []
    for field in (
        "agent_or_llm_role_page",
        "tool_or_execution_action_page",
        "feedback_or_state_transition_page",
        "validation_or_replay_page",
        "evaluation_result_page",
    ):
        page = evidence.get(field, "").strip()
        if page and page not in pages:
            pages.append(page)
    if pages:
        return f"public full text pp. {', '.join(pages)}; {access.get('public_fulltext_url') or url}"
    return f"title/abstract and source metadata; {url}"


def main() -> None:
    recommendations = index(RECOMMENDATIONS)
    access = index(ACCESS)
    evidence = index(EVIDENCE)
    candidate_ids = set(access)

    groups = {
        "study_level": STUDY_LEVEL,
        "extended": EXTENDED,
        "background": BACKGROUND,
        "excluded": EXCLUDED,
        "version_relation": set(VERSION_RELATIONS),
    }
    memberships: dict[str, list[str]] = {}
    for group_name, group_ids in groups.items():
        for discovery_id in group_ids:
            memberships.setdefault(discovery_id, []).append(group_name)
    overlap = {
        discovery_id: group_names
        for discovery_id, group_names in memberships.items()
        if len(group_names) > 1
    }
    if overlap:
        raise SystemExit(f"ERROR overlapping assessment groups: {overlap}")
    assigned = set(memberships)
    missing = candidate_ids - assigned
    extra = assigned - candidate_ids
    if missing or extra:
        raise SystemExit(
            "ERROR assessment coverage mismatch: "
            f"missing={sorted(missing)} extra={sorted(extra)}"
        )

    output_rows: list[dict[str, str]] = []
    for discovery_id in sorted(candidate_ids):
        rec = recommendations[discovery_id]
        acc = access[discovery_id]
        ev = evidence[discovery_id]
        version_status = ""
        version_target = ""

        if discovery_id in VERSION_RELATIONS:
            version_status, version_target, reason = VERSION_RELATIONS[discovery_id]
            proposed_decision = "version_reconciliation"
            proposed_layer = "not_counted_as_separate_study"
            assessment_status = "version_relation_identified"
            second_coder = "no"
        elif discovery_id in STUDY_LEVEL:
            proposed_decision = "study_level_candidate"
            proposed_layer = "target_software_study"
            if acc["access_status"] == "downloaded_and_text_extracted":
                assessment_status = "full_text_reviewed_ai_assisted"
                second_coder = "yes_after_author_inclusion"
                reason = (
                    "Public full text shows an observable LLM-mediated change to a "
                    "tool action, execution input, feedback interpretation, retained "
                    "state, validation step, or reporting decision."
                )
            else:
                assessment_status = "manual_full_text_review_needed"
                second_coder = "pending_full_text_and_author_inclusion"
                reason = (
                    "Title/abstract indicates a potentially eligible Agentic "
                    "target-software workflow, but public full text was not retrieved; "
                    "do not count or code until full-text review is completed."
                )
        elif discovery_id in EXTENDED:
            proposed_decision = "extended_synthesis_candidate"
            proposed_layer = "extended_synthesis"
            assessment_status = (
                "full_text_reviewed_ai_assisted"
                if acc["access_status"] == "downloaded_and_text_extracted"
                else "title_abstract_reviewed_ai_assisted"
            )
            second_coder = "no"
            reason = (
                "The study contributes an adjacent mechanism, benchmark, evaluation, "
                "or one-way LLM-assisted analysis, but does not establish the "
                "observable Agentic workflow control required for study-level coding."
            )
        elif discovery_id in BACKGROUND:
            proposed_decision = "background_reference_candidate"
            proposed_layer = "background_reference"
            assessment_status = (
                "full_text_reviewed_ai_assisted"
                if acc["access_status"] == "downloaded_and_text_extracted"
                else "title_abstract_reviewed_ai_assisted"
            )
            second_coder = "no"
            reason = (
                "The record supplies background on agent security, evaluation, "
                "traditional mechanisms, or governance rather than target-software "
                "Agentic vulnerability discovery or validation."
            )
        else:
            proposed_decision = "exclude_near_neighbor"
            proposed_layer = "excluded_near_neighbor"
            assessment_status = (
                "full_text_reviewed_ai_assisted"
                if acc["access_status"] == "downloaded_and_text_extracted"
                else "title_abstract_reviewed_ai_assisted"
            )
            second_coder = "no"
            reason = (
                "The record is outside target-software vulnerability discovery and "
                "validation or uses vulnerability in a non-software sense."
            )

        reason = SPECIFIC_NOTES.get(discovery_id, reason)
        output_rows.append(
            {
                "discovery_id": discovery_id,
                "title": rec["title"],
                "publication_dates": rec["publication_dates"],
                "doi": rec["doi"],
                "arxiv_id": rec["arxiv_id"],
                "source_ids": rec["source_ids"],
                "access_status": acc["access_status"],
                "assessment_status": assessment_status,
                "ai_assisted_proposed_decision": proposed_decision,
                "ai_assisted_proposed_layer": proposed_layer,
                "decision_reason": reason,
                "source_location": source_locations(ev, acc, rec["urls"]),
                "version_status": version_status,
                "version_target": version_target,
                "second_coder_required": second_coder,
                "author_final_decision": "",
                "author_final_reason": "",
                "human_confirmation_status": "pending",
            }
        )

    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(output_rows[0]))
        writer.writeheader()
        writer.writerows(output_rows)

    counts: dict[str, int] = {}
    for row in output_rows:
        key = row["ai_assisted_proposed_decision"]
        counts[key] = counts.get(key, 0) + 1
    print(f"WROTE {OUTPUT} ({len(output_rows)} records)")
    for key in sorted(counts):
        print(f"{key}: {counts[key]}")
    print(
        "study-level candidates with retrieved full text: "
        + str(
            sum(
                row["ai_assisted_proposed_decision"] == "study_level_candidate"
                and row["access_status"] == "downloaded_and_text_extracted"
                for row in output_rows
            )
        )
    )


if __name__ == "__main__":
    main()
