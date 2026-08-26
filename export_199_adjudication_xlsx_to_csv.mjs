import fs from "node:fs/promises";
import path from "node:path";
import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

function csvEscape(value) {
  const text = value == null ? "" : String(value);
  return /[",\r\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
}

const input = path.resolve(process.argv[2] || "adjudication/adjudication_form_199_all_disagreements_20260812.xlsx");
const output = path.resolve(process.argv[3] || "adjudication/adjudication_form_199_all_disagreements_20260812_completed.csv");

const blob = await FileBlob.load(input);
const workbook = await SpreadsheetFile.importXlsx(blob);
const sheet = workbook.worksheets.getItem("Adjudication Form");
const values = sheet.getUsedRange(true).values;
if (!values?.length) throw new Error("Adjudication Form is empty");

const headers = values[0].map((value) => String(value ?? "").trim());
const required = ["disagreement_id", "human_final_label", "brief_reason", "evidence_location_verified", "unresolved"];
for (const column of required) {
  if (!headers.includes(column)) throw new Error(`Missing required column: ${column}`);
}

const idColumn = headers.indexOf("disagreement_id");
const rows = values.slice(1).filter((row) => String(row[idColumn] ?? "").trim());
const csv = [headers, ...rows].map((row) => headers.map((_, index) => csvEscape(row[index])).join(",")).join("\r\n") + "\r\n";
await fs.mkdir(path.dirname(output), { recursive: true });
await fs.writeFile(output, csv, "utf8");
console.log(`EXPORTED_ADJUDICATION_CSV rows=${rows.length} path=${output}`);
