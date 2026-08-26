import fs from "node:fs/promises";
import path from "node:path";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const artifact = path.resolve("C:/Users/oldph/Desktop/ai挖洞/csur-agentic-vuln-mining-survey/work/csur_upgrade_v01/artifact_public_release_candidate");
const dataDir = path.join(artifact, "data");
const provenanceDir = path.resolve("C:/Users/oldph/Desktop/ai挖洞/csur-agentic-vuln-mining-survey/work/csur_upgrade_v01/artifact_provenance_archive_20260807/data");
const oldReviewDir = path.resolve("C:/Users/oldph/Desktop/ai挖洞/csur-agentic-vuln-mining-survey/work/csur_upgrade_v01/artifact_provenance_archive_20260807/local_private_working/unified_second_coder_review");
const outputDir = path.join(artifact, "adjudication");

const fieldSpecs = {
  lifecycle: {
    label: "lifecycle coverage",
    matrix: "lifecycle_coverage",
    first: "first_lifecycle",
    second: "second_lifecycle",
    type: "multi-label",
    rule: "Mark only observable lifecycle actions or outputs. Reporting and audit requires explicit packaging, routing, disclosure, or audit transition; a report name alone is insufficient.",
    allowed: ["candidate analysis", "path and input exploration", "execution observation", "reproduction and validation", "patch validation", "reporting and audit"],
  },
  capability: {
    label: "cross-stage capability",
    matrix: "cross_stage_capabilities",
    first: "first_capability",
    second: "second_capability",
    type: "multi-label",
    rule: "Require an explicit cross-stage connection. Information must guide later action; feedback must alter later action; packaging must assemble prior outputs; governance must enforce an actual gate.",
    allowed: ["context aggregation / rule extraction", "tool routing / strategy routing", "feedback interpretation / loop adjustment", "validation organization / evidence packaging", "long-horizon state management", "failure reuse / strategy update", "governance / human gates / disclosure control"],
  },
  primary_shape: {
    label: "primary system shape",
    matrix: "primary_system_shape",
    first: "first_primary_shape",
    second: "second_primary_shape",
    type: "single-label",
    rule: "Choose the dominant locus and objective of agent control in the main evaluated contribution. Use the evaluation task and primary metrics to resolve ties; do not infer from agent count or system name.",
    allowed: ["candidate-analysis system", "feedback-driven fuzzing agent", "reproduction-, validation-, and repair-centered agent", "long-horizon pentest and CRS agent"],
  },
  principal_evidence: {
    label: "principal reported evidence output",
    matrix: "strongest_evidence_output",
    first: "first_principal_evidence",
    second: "second_principal_evidence",
    type: "single-label",
    rule: "Select the observable result most directly supporting the main finding. Benchmark ground truth or aggregate CVE counts do not automatically establish externally traceable material.",
    allowed: ["candidate judgment", "controlled task completion", "runtime safety signal", "reproducible validation", "externally traceable material"],
  },
  external_traceability: {
    label: "external traceability",
    matrix: "external_traceability",
    first: "first_external_traceability",
    second: "second_external_traceability",
    type: "single-label",
    rule: "Code separately from principal output. Only item-level alignment between a concrete system result and a specific public external record qualifies as publicly aligned external trace.",
    allowed: ["no external trace reported", "author-reported external clue", "benchmark ground truth / public material", "publicly aligned external trace"],
  },
};

function parseCsv(text) {
  const rows = [];
  let row = [];
  let cell = "";
  let quoted = false;
  for (let i = 0; i < text.length; i += 1) {
    const ch = text[i];
    const next = text[i + 1];
    if (quoted) {
      if (ch === '"' && next === '"') { cell += '"'; i += 1; }
      else if (ch === '"') quoted = false;
      else cell += ch;
    } else if (ch === '"' && cell.length === 0) quoted = true;
    else if (ch === ",") { row.push(cell); cell = ""; }
    else if (ch === "\n") { row.push(cell.replace(/\r$/, "")); rows.push(row); row = []; cell = ""; }
    else cell += ch;
  }
  if (cell.length || row.length) { row.push(cell); rows.push(row); }
  const headers = rows.shift() || [];
  return rows.filter((r) => r.some((v) => v !== "")).map((r) => Object.fromEntries(headers.map((h, i) => [h, r[i] ?? ""])));
}

function csvEscape(value) {
  const s = value == null ? "" : String(value);
  return /[",\r\n]/.test(s) ? `"${s.replaceAll('"', '""')}"` : s;
}

function writeCsv(rows, headers) {
  return [headers.map(csvEscape).join(","), ...rows.map((r) => headers.map((h) => csvEscape(r[h])).join(","))].join("\r\n") + "\r\n";
}

function clean(value, limit = 800) {
  return String(value || "").replace(/\s+/g, " ").trim().slice(0, limit);
}

function firstNonempty(...values) {
  return values.map((v) => clean(v)).find(Boolean) || "";
}

function pageMap(text) {
  const pages = new Map();
  const pattern = /^===== PDF PAGE (\d+) =====\s*$/gm;
  const matches = [...String(text || "").matchAll(pattern)];
  for (let i = 0; i < matches.length; i += 1) {
    const start = matches[i].index + matches[i][0].length;
    const end = i + 1 < matches.length ? matches[i + 1].index : text.length;
    pages.set(Number(matches[i][1]), text.slice(start, end).replace(/\s+/g, " ").trim());
  }
  return pages;
}

function reviewedPages(locator, pages) {
  const found = new Set();
  for (const match of String(locator || "").matchAll(/pp?\.\s*(\d+)(?:\s*[–-]\s*(\d+))?/gi)) {
    const start = Number(match[1]);
    const end = Number(match[2] || match[1]);
    for (let page = start; page <= end; page += 1) if (pages.has(page)) found.add(page);
  }
  return found.size ? [...found] : [...pages.keys()];
}

const labelKeywords = {
  "candidate analysis": ["vulnerab", "detect", "analysis", "hypoth", "classif", "localiz", "rank"],
  "path and input exploration": ["input", "seed", "path", "coverage", "explor", "mutation", "fuzz"],
  "execution observation": ["execution", "runtime", "crash", "sanitizer", "oracle", "trace", "coverage"],
  "reproduction and validation": ["reproduc", "validation", "verify", "poc", "pov", "replay", "exploit"],
  "patch validation": ["patch", "repair", "regression", "test", "fix"],
  "reporting and audit": ["report", "audit", "disclos", "finding", "evidence", "package"],
  "context aggregation / rule extraction": ["context", "retriev", "rule", "specification", "knowledge", "aggregate"],
  "tool routing / strategy routing": ["tool", "route", "select", "strategy", "planner", "next action"],
  "feedback interpretation / loop adjustment": ["feedback", "refine", "adjust", "iteration", "loop", "update"],
  "validation organization / evidence packaging": ["validation", "evidence", "poc", "pov", "replay", "report", "package"],
  "long-horizon state management": ["memory", "state", "history", "long-horizon", "multi-step", "context"],
  "failure reuse / strategy update": ["failure", "failed", "retry", "reflection", "learn", "update", "coverage gap"],
  "governance / human gates / disclosure control": ["human", "approval", "permission", "sandbox", "scope", "disclos", "guardrail"],
  "candidate-analysis system": ["analysis", "detect", "hypoth", "candidate", "localiz", "audit"],
  "feedback-driven fuzzing agent": ["fuzz", "feedback", "coverage", "mutation", "seed", "execution"],
  "reproduction-, validation-, and repair-centered agent": ["reproduc", "validation", "poc", "pov", "replay", "patch", "repair"],
  "long-horizon pentest and CRS agent": ["pentest", "cyber", "crs", "long-horizon", "multi-stage", "exploit"],
  "candidate judgment": ["accuracy", "precision", "recall", "classification", "candidate", "detect", "report"],
  "controlled task completion": ["task", "ctf", "benchmark", "success", "flag", "completion"],
  "runtime safety signal": ["crash", "sanitizer", "oracle", "coverage", "runtime", "vulnerab"],
  "reproducible validation": ["reproduc", "validation", "poc", "pov", "replay", "patch", "trigger"],
  "externally traceable material": ["cve", "cnvd", "vendor", "maintainer", "bounty", "disclos", "issue", "commit"],
  "no external trace reported": ["public", "artifact", "external", "disclos", "cve", "vendor"],
  "author-reported external clue": ["cve", "cnvd", "vendor", "maintainer", "bounty", "confirm", "disclos"],
  "benchmark ground truth / public material": ["benchmark", "ground truth", "public", "cve", "dataset"],
  "publicly aligned external trace": ["cve", "cnvd", "vendor", "maintainer", "bounty", "issue", "commit", "confirm", "disclos"],
};

function disputedLabels(x, y) {
  const left = new Set(String(x || "").split(";").map((v) => v.trim()).filter(Boolean));
  const right = new Set(String(y || "").split(";").map((v) => v.trim()).filter(Boolean));
  return [...left, ...right].filter((label, index, all) => all.indexOf(label) === index && !(left.has(label) && right.has(label)));
}

function oldSourceLead(text, locator, x, y) {
  const pages = pageMap(text);
  const candidates = reviewedPages(locator, pages);
  const keywords = [...new Set(disputedLabels(x, y).flatMap((label) => labelKeywords[label] || []))];
  const sentences = [];
  for (const page of candidates) {
    const pageText = pages.get(page) || "";
    for (const sentence of pageText.split(/(?<=[.!?])\s+(?=[A-Z0-9])/)) {
      const normalized = clean(sentence, 700);
      if (normalized.length < 45) continue;
      const lower = normalized.toLowerCase();
      const score = keywords.filter((keyword) => lower.includes(keyword)).length;
      if (score) sentences.push({ page, score, text: normalized });
    }
  }
  sentences.sort((a, b) => b.score - a.score || a.page - b.page || a.text.length - b.text.length);
  const selected = [];
  for (const item of sentences) {
    if (selected.some((x) => x.text === item.text)) continue;
    selected.push(item);
    if (selected.length === 2 || selected.reduce((n, x) => n + x.text.length, 0) > 650) break;
  }
  if (!selected.length) {
    for (const page of candidates) {
      const fallback = clean(pages.get(page), 650);
      if (fallback) { selected.push({ page, score: 0, text: fallback }); break; }
    }
  }
  return {
    excerpt: selected.map((item) => `[p.${item.page}] ${item.text}`).join(" "),
    pages: [...new Set(selected.map((item) => item.page))],
  };
}

async function readCsv(file) {
  return parseCsv(await fs.readFile(file, "utf8"));
}

function fieldEvidence(fieldKey, first, fulltext, matrix, core, v13, oldSecond, oldText, x, y) {
  const url = firstNonempty(fulltext?.public_fulltext_url, first?.public_fulltext_url, matrix?.official_url);
  const role = clean(fulltext?.agent_or_llm_role_snippet, 500);
  const action = clean(fulltext?.tool_or_execution_action_snippet, 500);
  const feedback = clean(fulltext?.feedback_or_state_transition_snippet, 500);
  const validation = clean(fulltext?.validation_or_replay_snippet, 500);
  const evaluation = clean(fulltext?.evaluation_result_snippet, 500);
  const pages = [];
  for (const [name, page] of [["role", fulltext?.agent_or_llm_role_page], ["action", fulltext?.tool_or_execution_action_page], ["feedback", fulltext?.feedback_or_state_transition_page], ["validation", fulltext?.validation_or_replay_page], ["evaluation", fulltext?.evaluation_result_page]]) {
    if (page) pages.push(`${name} p.${page}`);
  }
  let excerpt = "";
  if (fieldKey === "lifecycle") excerpt = firstNonempty(role, action, feedback, validation, evaluation);
  if (fieldKey === "capability") excerpt = firstNonempty(feedback, action, role);
  if (fieldKey === "primary_shape") excerpt = firstNonempty(action, role, evaluation);
  if (fieldKey === "principal_evidence") excerpt = firstNonempty(validation, evaluation, action);
  if (fieldKey === "external_traceability") excerpt = firstNonempty(evaluation, validation, clean(fulltext?.source_locations_used, 500));
  if (excerpt) {
    return {
      status: "machine_prepared_lead",
      location: [url, pages.join("; ")].filter(Boolean).join(" | "),
      excerpt,
      summary: "A source-linked snippet is supplied as a lead. The human reviewer must open the source, verify the wording and locator, and replace the lead with the verified location.",
    };
  }
  if (oldText) {
    const lead = oldSourceLead(oldText, oldSecond?.material_checked, x, y);
    if (lead.excerpt) {
      return {
        status: "machine_prepared_lead",
        location: [matrix?.official_url, clean(oldSecond?.material_checked, 500), lead.pages.length ? `excerpt pages ${lead.pages.join(", ")}` : ""].filter(Boolean).join(" | "),
        excerpt: lead.excerpt,
        summary: "A verbatim source-text lead was extracted from pages previously checked during independent coding. The human reviewer must open the source, verify the quotation and locator, and replace the lead with the verified location.",
      };
    }
  }
  const structured = firstNonempty(core?.[fieldKey === "principal_evidence" ? "e_level_reason" : "a_level_reason"], core?.note, matrix?.claim_boundary);
  const source = firstNonempty(v13?.source_location, core?.note, matrix?.official_url);
  return {
    status: structured ? "locator_only" : "missing_direct_evidence",
    location: source,
    excerpt: "",
    summary: structured ? `Existing structured audit note is available but is not treated as a source excerpt: ${structured}` : "No direct record-level excerpt was found in the current public package; the human reviewer must locate the source evidence.",
  };
}

function sourceSummary(fieldKey, ev) {
  if (ev.status === "machine_prepared_lead") return ev.summary;
  return ev.summary;
}

async function main() {
  await fs.mkdir(outputDir, { recursive: true });
  const comparison = await readCsv(path.join(dataDir, "integrated_199_second_coder_comparison_20260730.csv"));
  const matrixRows = await readCsv(path.join(dataDir, "current_study_level_coding_matrix_harmonized.csv"));
  const matrixById = new Map();
  for (const row of matrixRows) { matrixById.set(row.matrix_id, row); matrixById.set(row.record_id, row); }
  const coreRows = await readCsv(path.join(dataDir, "core_coding.csv"));
  const coreByRecord = new Map(coreRows.map((r) => [r.record_id, r]));
  const v13Rows = await readCsv(path.join(dataDir, "v13_core_synthesis_matrix.csv"));
  const v13ByCore = new Map(v13Rows.map((r) => [r.core_id, r]));

  const firstFiles = ["final_multisource_search_20260730_first_coder.csv", "final_multisource_search_20260730_first_coder_addendum.csv", "final_multisource_search_20260730_first_coder_late_addendum.csv", "final_multisource_search_20260730_first_coder_remaining.csv"];
  const firstRows = (await Promise.all(firstFiles.map((f) => readCsv(path.join(provenanceDir, f))))).flat();
  const firstById = new Map();
  for (const row of firstRows) if (!firstById.has(row.discovery_id)) firstById.set(row.discovery_id, row);
  const evidenceRows = await readCsv(path.join(provenanceDir, "final_multisource_search_20260730_fulltext_evidence.csv"));
  const evidenceById = new Map();
  for (const row of evidenceRows) if (!evidenceById.has(row.discovery_id)) evidenceById.set(row.discovery_id, row);
  const oldSecondRows = await readCsv(path.join(dataDir, "unified_second_coder_final_results.csv"));
  const oldSecondById = new Map(oldSecondRows.map((r) => [r.matrix_id, r]));
  const oldTextById = new Map();
  for (const row of oldSecondRows) {
    const file = path.join(oldReviewDir, "extracted_public_text", `${row.matrix_id}.txt`);
    try { oldTextById.set(row.matrix_id, await fs.readFile(file, "utf8")); } catch { /* Missing text is handled explicitly below. */ }
  }

  const outputHeaders = [
    "disagreement_id", "record_id", "cohort", "title", "field", "field_type",
    "coder_x_label", "coder_y_label", "evidence_status", "evidence_location_lead",
    "evidence_excerpt_lead", "evidence_summary", "codebook_rule",
    "human_final_label", "brief_reason", "evidence_location_verified", "unresolved",
    "reviewer_initials", "review_date", "row_status",
  ];
  const rows = [];
  for (const comparisonRow of comparison) {
    for (const [fieldKey, spec] of Object.entries(fieldSpecs)) {
      const x = comparisonRow[spec.first] || "";
      const y = comparisonRow[spec.second] || "";
      if (x === y) continue;
      const matrix = matrixById.get(comparisonRow.record_id) || {};
      const first = firstById.get(comparisonRow.record_id);
      const fulltext = evidenceById.get(comparisonRow.record_id);
      const core = coreByRecord.get(matrix.record_id);
      const v13 = v13ByCore.get(matrix.matrix_id);
      const oldSecond = oldSecondById.get(comparisonRow.record_id);
      const oldText = oldTextById.get(comparisonRow.record_id);
      const ev = fieldEvidence(fieldKey, first, fulltext, matrix, core, v13, oldSecond, oldText, x, y);
      const id = `${comparisonRow.record_id}__${fieldKey}`;
      rows.push({
        disagreement_id: id,
        record_id: comparisonRow.record_id,
        cohort: comparisonRow.cohort,
        title: comparisonRow.title,
        field: spec.label,
        field_type: spec.type,
        coder_x_label: x,
        coder_y_label: y,
        evidence_status: ev.status,
        evidence_location_lead: ev.location,
        evidence_excerpt_lead: ev.excerpt,
        evidence_summary: sourceSummary(fieldKey, ev),
        codebook_rule: spec.rule,
        human_final_label: "",
        brief_reason: "",
        evidence_location_verified: "",
        unresolved: "",
        reviewer_initials: "",
        review_date: "",
        row_status: "pending",
      });
    }
  }
  if (rows.length !== 410) throw new Error(`Expected 410 field disagreements, found ${rows.length}`);
  await fs.writeFile(path.join(outputDir, "adjudication_form_199_all_disagreements_20260812.csv"), writeCsv(rows, outputHeaders), "utf8");
  await fs.writeFile(path.join(outputDir, "adjudication_allowed_labels.csv"), writeCsv(Object.entries(fieldSpecs).flatMap(([key, spec]) => spec.allowed.map((label) => ({ field_key: key, field: spec.label, field_type: spec.type, allowed_label: label }))), ["field_key", "field", "field_type", "allowed_label"]), "utf8");

  const workbook = Workbook.create();
  const form = workbook.worksheets.add("Adjudication Form");
  const instructions = workbook.worksheets.add("Instructions");
  const rules = workbook.worksheets.add("Field Rules");
  const coverage = workbook.worksheets.add("QC");
  form.showGridLines = false; instructions.showGridLines = false; rules.showGridLines = false; coverage.showGridLines = false;
  form.getRangeByIndexes(0, 0, 1, outputHeaders.length).values = [outputHeaders];
  form.getRangeByIndexes(1, 0, rows.length, outputHeaders.length).values = rows.map((r) => outputHeaders.map((h) => r[h]));
  const statusCol = outputHeaders.indexOf("row_status");
  const finalCol = outputHeaders.indexOf("human_final_label");
  const reasonCol = outputHeaders.indexOf("brief_reason");
  const verifiedLocCol = outputHeaders.indexOf("evidence_location_verified");
  const unresolvedCol = outputHeaders.indexOf("unresolved");
  const excelCol = (n) => { let s = ""; let x = n + 1; while (x) { const r = (x - 1) % 26; s = String.fromCharCode(65 + r) + s; x = Math.floor((x - 1) / 26); } return s; };
  const f = excelCol(finalCol), r = excelCol(reasonCol), l = excelCol(verifiedLocCol), u = excelCol(unresolvedCol), st = excelCol(statusCol);
  form.getRangeByIndexes(1, statusCol, rows.length, 1).formulas = rows.map((_, i) => [`=IF(OR(AND(${f}${i + 2}="unresolved",LEN(${r}${i + 2})>0,LEN(${l}${i + 2})>0,${u}${i + 2}="yes"),AND(LEN(${f}${i + 2})>0,LEN(${r}${i + 2})>0,LEN(${l}${i + 2})>0,OR(${u}${i + 2}="yes",${u}${i + 2}="no"))),"ready","pending")`]);
  form.getRange(`A1:${excelCol(outputHeaders.length - 1)}1`).format = { fill: "#17324D", font: { bold: true, color: "#FFFFFF" }, wrapText: true, verticalAlignment: "Center" };
  form.getRange(`A2:${excelCol(outputHeaders.length - 1)}${rows.length + 1}`).format = { verticalAlignment: "Top", wrapText: true };
  form.getRange(`A1:${excelCol(outputHeaders.length - 1)}${rows.length + 1}`).format.borders = { preset: "inside", style: "thin", color: "#D9E2EC" };
  form.getRange(`A1:${excelCol(outputHeaders.length - 1)}${rows.length + 1}`).format.borders = { outside: { style: "thin", color: "#9FB3C8" } };
  form.getRange(`L2:Q${rows.length + 1}`).format.fill = "#FFF7D6";
  form.getRange(`T2:T${rows.length + 1}`).format.fill = "#E8F1F8";
  form.getRange(`Q2:Q${rows.length + 1}`).dataValidation = { rule: { type: "list", values: ["yes", "no"] } };
  form.freezePanes.freezeRows(1); form.freezePanes.freezeColumns(5);
  const widths = [22, 12, 18, 42, 28, 14, 28, 28, 22, 55, 70, 52, 62, 32, 42, 48, 14, 18, 14, 14];
  widths.forEach((w, i) => form.getRangeByIndexes(0, i, rows.length + 1, 1).format.columnWidth = w);
  form.getRange(`A1:T${rows.length + 1}`).format.rowHeight = 44;

  const instructionRows = [
    ["Purpose", "Resolve every row in the form using source evidence and the prespecified codebook."],
    ["Independence", "Review the evidence without using desired totals, manuscript claims, or coder identity. Coder X/Y are anonymized."],
    ["Required fields", "For every row, complete human_final_label, brief_reason, evidence_location_verified, and unresolved."],
    ["Unresolved", "If the source cannot support a reliable decision, enter human_final_label=unresolved, unresolved=yes, and explain the missing evidence."],
    ["Multi-label fields", "Use only allowed labels, separated by semicolons, in the codebook order. Do not add labels by implication."],
    ["Single-label fields", "Enter exactly one allowed label. Do not use a higher category merely because it sounds stronger."],
    ["Evidence", "Open and verify the lead location. Replace it with a page/section/figure/table/URL locator that another reviewer can follow."],
    ["Reason", "Give one short factual sentence linking the verified evidence to the selected label. Do not write a target number or expected conclusion."],
    ["Completion", "Rows turn to ready only after the four human fields are complete. Return this filled workbook or CSV without renaming the required columns."],
  ];
  instructions.getRange(`A1:B${instructionRows.length}`).values = instructionRows;
  instructions.getRange("A1:B1").format = { fill: "#17324D", font: { bold: true, color: "#FFFFFF" } };
  instructions.getRange(`A1:B${instructionRows.length}`).format.wrapText = true;
  instructions.getRange("A:A").format.columnWidth = 24; instructions.getRange("B:B").format.columnWidth = 110;
  instructions.getRange(`A1:B${instructionRows.length}`).format.rowHeight = 36;

  const ruleRows = [["field_key", "field", "type", "codebook_rule", "allowed_label"]];
  for (const [key, spec] of Object.entries(fieldSpecs)) for (const label of spec.allowed) ruleRows.push([key, spec.label, spec.type, spec.rule, label]);
  rules.getRangeByIndexes(0, 0, ruleRows.length, ruleRows[0].length).values = ruleRows;
  rules.getRange("A1:E1").format = { fill: "#17324D", font: { bold: true, color: "#FFFFFF" }, wrapText: true };
  rules.getRange(`A1:E${ruleRows.length}`).format.wrapText = true; rules.getRange("A:A").format.columnWidth = 24; rules.getRange("B:B").format.columnWidth = 32; rules.getRange("C:C").format.columnWidth = 16; rules.getRange("D:D").format.columnWidth = 85; rules.getRange("E:E").format.columnWidth = 58;
  rules.freezePanes.freezeRows(1);

  coverage.getRange("A1:B8").values = [
    ["QC item", "Formula / status"],
    ["Source rows", rows.length],
    ["Human rows ready", ""],
    ["Human rows pending", ""],
    ["Required return", "Filled Adjudication Form sheet with no pending rows unless explicitly unresolved"],
    ["Original data", "Independent comparison and harmonized matrix are not modified by this package"],
    ["Evidence policy", "Lead evidence is not a final decision; human verification is required"],
    ["Output status", "Pending human third-party review"],
  ];
  coverage.getRange("B3").formulas = [[`=COUNTIF('Adjudication Form'!$T$2:$T$${rows.length + 1},"ready")`]];
  coverage.getRange("B4").formulas = [[`=COUNTIF('Adjudication Form'!$T$2:$T$${rows.length + 1},"pending")`]];
  coverage.getRange("A1:B1").format = { fill: "#17324D", font: { bold: true, color: "#FFFFFF" } };
  coverage.getRange("A1:B8").format.wrapText = true; coverage.getRange("A:A").format.columnWidth = 28; coverage.getRange("B:B").format.columnWidth = 95;

  const preview = await workbook.render({ sheetName: "Instructions", autoCrop: "all", scale: 1, format: "png" });
  await fs.writeFile(path.join(outputDir, "adjudication_instructions_preview.png"), new Uint8Array(await preview.arrayBuffer()));
  const xlsx = await SpreadsheetFile.exportXlsx(workbook);
  await xlsx.save(path.join(outputDir, "adjudication_form_199_all_disagreements_20260812.xlsx"));
  await fs.writeFile(path.join(outputDir, "ADJUDICATION_RULES_20260812.md"), `# Human Third-Party Adjudication Rules\n\nThis package contains one row for every disagreement between the two independent assignments in the current 199-study comparison. The form anonymizes the assignments as coder X and coder Y.\n\n## Required human action\n\n1. Open the cited public source for each row.\n2. Verify or replace the evidence locator and write a brief evidence-based reason.\n3. Enter one allowed single label or a semicolon-separated allowed multi-label set.\n4. If the source cannot resolve the boundary, enter \`unresolved\` and set \`unresolved=yes\`; do not guess.\n\n## Fixed rules\n\n${Object.values(fieldSpecs).map((s) => `- **${s.label}**: ${s.rule} Allowed values: ${s.allowed.map((x) => `\`${x}\``).join(", ")}.`).join("\n")}\n\nThe lead excerpt and lead locator are preparation aids only. They do not constitute a human adjudication. The final matrix must be generated only after the completed form passes validation.\n`, "utf8");
  const report = { rows: rows.length, byField: Object.fromEntries(Object.entries(fieldSpecs).map(([k, spec]) => [spec.label, rows.filter((r) => r.field === spec.label).length])), evidenceStatus: Object.fromEntries([...new Set(rows.map((r) => r.evidence_status))].map((s) => [s, rows.filter((r) => r.evidence_status === s).length])) };
  await fs.writeFile(path.join(outputDir, "adjudication_package_manifest.json"), JSON.stringify(report, null, 2) + "\n", "utf8");
  console.log(JSON.stringify(report));
}

main().catch((error) => { console.error(error.stack || error); process.exitCode = 1; });
