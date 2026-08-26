import fs from "node:fs/promises";
import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const input = process.argv[2];
const output = process.argv[3];
if (!input || !output) {
  throw new Error("usage: node export_third_party_rereview_csv.mjs INPUT.xlsx OUTPUT.csv");
}

const workbook = await SpreadsheetFile.importXlsx(await FileBlob.load(input));
const sheet = workbook.worksheets.getItem("Adjudication Form");
const values = sheet.getRange("A1:R461").values;
const headers = values[0].map(String);
const rows = values.slice(1).map((row) =>
  Object.fromEntries(headers.map((header, i) => [header, row[i] == null ? "" : String(row[i])]))
);
const expected = [
  "task_id", "case_id", "study_title", "field", "field_type", "allowed_labels",
  "source_url", "included_local_file", "evidence_location_lead", "evidence_excerpt_lead",
  "final_label", "verified_evidence_locator", "brief_reason", "confidence", "unresolved",
  "reviewer_initials", "review_date", "completion_check",
];
if (headers.join("|") !== expected.join("|")) {
  throw new Error(`unexpected workbook headers: ${headers.join("|")}`);
}
if (rows.length !== 460) throw new Error(`expected 460 rows, got ${rows.length}`);
const csvCell = (value) => {
  const text = value == null ? "" : String(value);
  return /[",\r\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
};
const csv = [expected.join(","), ...rows.map((row) => expected.map((h) => csvCell(row[h])).join(","))].join("\n") + "\n";
await fs.writeFile(output, csv, "utf8");
console.log(JSON.stringify({ output, rows: rows.length, headers }, null, 2));
