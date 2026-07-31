#!/usr/bin/env python3
"""Retry public arXiv PDFs that urllib could not access in the sandbox."""

from __future__ import annotations

import csv
import hashlib
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ACCESS = ROOT / "data" / "final_multisource_search_20260730_fulltext_access.csv"
CACHE = ROOT.parent.parent.parent / "02_literature" / "final_multisource_20260730"


def safe_name(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.-]+", "_", value).strip("_")[:120]


def main() -> int:
    with ACCESS.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = list(reader.fieldnames or [])
        rows = list(reader)
    targets = [
        row
        for row in rows
        if row["access_status"] == "fetch_failed" and row["public_fulltext_url"].startswith("http")
    ]
    success = 0
    for index, row in enumerate(targets, start=1):
        pdf = CACHE / f"{row['discovery_id']}_{safe_name(row['title'])}.pdf"
        text = pdf.with_suffix(".txt")
        url = row["public_fulltext_url"]
        retry_pdf = CACHE / f"{row['discovery_id']}_retry.pdf"
        if retry_pdf.exists() and retry_pdf.read_bytes().startswith(b"%PDF"):
            retry_pdf.replace(pdf)
            curl_error = ""
        else:
            proc = subprocess.run(
                ["curl.exe", "-L", "--fail", "--retry", "2", "--connect-timeout", "30", url, "-o", str(pdf)],
                capture_output=True,
                text=True,
                timeout=180,
            )
            curl_error = proc.stderr[-400:]
            if proc.returncode != 0 or not pdf.exists() or not pdf.read_bytes().startswith(b"%PDF"):
                row["notes"] = f"curl retry failed: exit={proc.returncode}; {curl_error}"
                print(f"[{index}/{len(targets)}] {row['discovery_id']} failed")
                continue
        text_proc = subprocess.run(
            ["pdftotext", "-layout", str(pdf), str(text)],
            capture_output=True,
            text=True,
            timeout=180,
        )
        row["public_fulltext_url"] = url
        row["access_basis"] = "Public arXiv PDF retrieved by exact identifier."
        row["sha256"] = hashlib.sha256(pdf.read_bytes()).hexdigest()
        row["local_review_pdf"] = str(pdf)
        if text_proc.returncode == 0 and text.exists():
            row["access_status"] = "downloaded_and_text_extracted"
            row["local_extracted_text"] = str(text)
            row["notes"] = "Public arXiv PDF and extracted review text."
            success += 1
            print(f"[{index}/{len(targets)}] {row['discovery_id']} downloaded_and_text_extracted")
        else:
            row["access_status"] = "downloaded_pdf_only"
            row["notes"] = f"PDF retrieved; pdftotext exit={text_proc.returncode}."
            print(f"[{index}/{len(targets)}] {row['discovery_id']} downloaded_pdf_only")
    with ACCESS.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"TARGETS={len(targets)} SUCCESS={success}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
