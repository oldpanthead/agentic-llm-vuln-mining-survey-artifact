#!/usr/bin/env python3
"""Extract explicit traditional-security primitive mentions for new studies."""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
OLD = DATA / "traditional_security_primitives_pre_final_multisource_20260730.csv"
NEW_MATRIX = DATA / "final_multisource_search_20260730_new_study_level_coding.csv"
FIRST_FILES = (
    DATA / "final_multisource_search_20260730_first_coder.csv",
    DATA / "final_multisource_search_20260730_first_coder_addendum.csv",
    DATA / "final_multisource_search_20260730_first_coder_remaining.csv",
)
NEW_OUTPUT = DATA / "final_multisource_search_20260730_traditional_security_primitives.csv"
PROPOSED = DATA / "traditional_security_primitives_proposed_20260730.csv"
SUMMARY = DATA / "traditional_security_primitive_counts_proposed_20260730.csv"


PATTERNS = {
    "static_taint_specification": re.compile(
        r"\b(static analy(?:sis|zer)|taint analy(?:sis|zer)|codeql|semgrep|slither|joern|"
        r"data[- ]flow analy(?:sis|zer)|specification (?:mining|inference)|rule synthesis)\b",
        re.I,
    ),
    "fuzzing_input_harness": re.compile(
        r"\b(fuzz(?:ing|er)?|libfuzzer|afl\+?\+?|honggfuzz|fuzz harness|test harness|"
        r"seed corpus|seed generation|mutation engine|input generation)\b",
        re.I,
    ),
    "symbolic_constraint": re.compile(
        r"\b(symbolic execution|symbolic reasoning|symbolic verifier|formal verification|"
        r"theorem prover|tamarin|concolic execution|constraint solv(?:er|ing)|\bz3\b|\bklee\b|\bangr\b)\b",
        re.I,
    ),
    "runtime_oracle": re.compile(
        r"\b(addresssanitizer|asan|undefinedbehaviorsanitizer|ubsan|memorysanitizer|msan|"
        r"sanitizer|runtime (?:check|monitor|signal|feedback)|execution (?:trace|feedback|result)|"
        r"crash (?:signal|log|report)|coverage feedback|test oracle|vulnerability oracle)\b",
        re.I,
    ),
    "replay_poc_pov": re.compile(
        r"\b(proof[- ]of[- ]concept|proof[- ]of[- ]vulnerability|\bpoc\b|\bpov\b|"
        r"exploit script|replay script|reproduc(?:e|ing|tion) (?:the )?(?:bug|crash|vulnerability)|"
        r"vulnerability reproduction)\b",
        re.I,
    ),
    "patch_build_test": re.compile(
        r"\b(patch validation|patch verification|regression test|test suite|unit test|"
        r"build validation|compilation check|compile(?:s|d|r)? successfully|repair validation|"
        r"post[- ]patch)\b",
        re.I,
    ),
    "recon_scan_pentest": re.compile(
        r"\b(nmap|metasploit|burp suite|sqlmap|nikto|nessus|openvas|masscan|"
        r"reconnaissance|port scan(?:ning)?|vulnerability scanner|penetration test(?:ing)?|"
        r"shell command|ssh session)\b",
        re.I,
    ),
}

LIFECYCLE_GATES = {
    "static_taint_specification": {"candidate analysis"},
    "fuzzing_input_harness": {"path and input exploration"},
    "symbolic_constraint": {"candidate analysis", "path and input exploration"},
    "runtime_oracle": {"execution observation"},
    "replay_poc_pov": {"reproduction and validation"},
    "patch_build_test": {"patch validation"},
}

TOOLS = re.compile(
    r"\b(CodeQL|Semgrep|Slither|Joern|AFL\+\+|AFL|libFuzzer|Honggfuzz|KLEE|angr|Z3|"
    r"AddressSanitizer|ASan|UBSan|MemorySanitizer|MSan|Nmap|Metasploit|Burp Suite|"
    r"sqlmap|Nikto|Nessus|OpenVAS|Masscan|GDB|Valgrind|Docker|Foundry|Hardhat)\b",
    re.I,
)


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def clean(value: str) -> str:
    return " ".join((value or "").strip().split())


def article_body(text: str) -> str:
    match = re.search(r"\n\s*(?:REFERENCES|BIBLIOGRAPHY)\s*\n", text, re.I)
    return text[: match.start()] if match else text


def page_of(text: str, offset: int) -> int:
    return text[:offset].count("\f") + 1


def main() -> int:
    matrix = {row["record_id"]: row for row in read(NEW_MATRIX)}
    first: dict[str, dict[str, str]] = {}
    for path in FIRST_FILES:
        for row in read(path):
            first[row["discovery_id"]] = row
    if not set(matrix) <= set(first):
        raise SystemExit("ERROR: missing first-coder source rows for primitive extraction")

    rows: list[dict[str, str]] = []
    counts: Counter[str] = Counter()
    for record_id in sorted(matrix):
        source = first[record_id]
        text_path = Path(source["local_extracted_text"])
        if not text_path.exists():
            raise SystemExit(f"ERROR: missing extracted text for {record_id}: {text_path}")
        text = text_path.read_text(encoding="utf-8", errors="replace")
        body = article_body(text)
        tags: list[str] = []
        pages: set[int] = set()
        terms: list[str] = []
        lifecycle = {
            value.strip() for value in matrix[record_id]["lifecycle_coverage"].split(";") if value.strip()
        }
        for tag, pattern in PATTERNS.items():
            if tag in LIFECYCLE_GATES and not (LIFECYCLE_GATES[tag] & lifecycle):
                continue
            if (
                tag == "recon_scan_pentest"
                and matrix[record_id]["primary_system_shape"]
                != "long-horizon pentest and CRS agent"
            ):
                continue
            matches = list(pattern.finditer(body))
            if not matches:
                continue
            tags.append(tag)
            counts[tag] += 1
            for match in matches[:2]:
                pages.add(page_of(body, match.start()))
                terms.append(clean(match.group(0)))
        if not tags:
            tags = ["not specified"]
            counts["not specified"] += 1
        tools = sorted({clean(match.group(0)) for match in TOOLS.finditer(body)}, key=str.casefold)
        page_text = ", ".join(str(page) for page in sorted(pages)[:8])
        rows.append(
            {
                "matrix_id": record_id,
                "system": matrix[record_id]["system_alias"],
                "primitive_tags": ";".join(tags),
                "named_tools": ";".join(tools) if tools else "not specified",
                "source_location": f"Public full text, extracted pages {page_text}; {matrix[record_id]['official_url']}",
                "extraction_note": (
                    "Rule-assisted author extraction of explicit workflow/evaluation terminology; "
                    + (
                        f"matched terms: {', '.join(dict.fromkeys(terms))}. "
                        if terms
                        else "no member of the seven controlled primitive families was explicitly located. "
                    )
                    + "Tags do not imply dynamic agent selection."
                ),
            }
        )

    write(NEW_OUTPUT, rows)
    old = read(OLD)
    write(PROPOSED, old + rows)
    summary = [
        {"primitive_tag": tag, "count_new_132": str(counts[tag]), "count_integrated_199": str(counts[tag] + sum(tag in row["primitive_tags"].split(";") for row in old))}
        for tag in (*PATTERNS, "not specified")
    ]
    write(SUMMARY, summary)
    print(f"NEW_ROWS={len(rows)} PROPOSED_ROWS={len(old) + len(rows)}")
    for row in summary:
        print(f"{row['primitive_tag']}={row['count_integrated_199']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
