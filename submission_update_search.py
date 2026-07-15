#!/usr/bin/env python3
"""Fetch and normalize the submission-time arXiv update search.

The historical corpus ledger is retained for provenance. This script records a
separate, reproducible update search over the fast-moving 2026 window and does
not reconstruct raw hit counts from the already screened corpus.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RAW_DIR = DATA / "submission_update_20260715_raw"
RESULTS = DATA / "submission_update_20260715_arxiv_results.csv"
MANIFEST = DATA / "submission_update_20260715_manifest.json"

DATE_FROM = "202601010000"
DATE_TO = "202607152359"
API = "https://export.arxiv.org/api/query"
PAGE_SIZE = 100

QUERIES = {
    "agent_task": (
        f"submittedDate:[{DATE_FROM} TO {DATE_TO}] AND "
        '(ti:vulnerability OR ti:fuzzing OR ti:pentest OR '
        'ti:"cyber reasoning" OR ti:security) AND '
        '(all:"large language model" OR all:LLM) AND '
        '(all:agent OR all:agentic OR all:"multi-agent")'
    ),
    "pov_crs": (
        f"submittedDate:[{DATE_FROM} TO {DATE_TO}] AND "
        '(all:"proof of vulnerability" OR all:PoV OR '
        'all:"cyber reasoning system" OR all:CRS) AND '
        '(all:LLM OR all:agent)'
    ),
    "review_update": (
        f"submittedDate:[{DATE_FROM} TO {DATE_TO}] AND "
        '(ti:review OR ti:survey OR ti:"systematic literature review") AND '
        '(all:LLM OR all:"large language model") AND '
        '(all:vulnerability OR all:fuzzing OR all:"software security")'
    ),
    "execution_validation": (
        f"submittedDate:[{DATE_FROM} TO {DATE_TO}] AND "
        '(ti:vulnerability OR ti:fuzzing OR ti:security) AND '
        '(all:"large language model" OR all:LLM) AND '
        '(all:validation OR all:feedback OR all:execution OR all:tool)'
    ),
}

NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "open": "http://a9.com/-/spec/opensearch/1.1/",
    "arxiv": "http://arxiv.org/schemas/atom",
}


def compact(text: str | None) -> str:
    return " ".join((text or "").split())


def fetch(url: str) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "agentic-llm-vuln-mining-survey/1.0"},
    )
    with urllib.request.urlopen(req, timeout=90) as response:
        return response.read()


def query_url(query: str, start: int, max_results: int) -> str:
    params = {
        "search_query": query,
        "start": str(start),
        "max_results": str(max_results),
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    return API + "?" + urllib.parse.urlencode(params)


def parse_page(payload: bytes) -> tuple[int, list[dict[str, str]]]:
    root = ET.fromstring(payload)
    total = int(root.findtext("open:totalResults", default="0", namespaces=NS))
    rows: list[dict[str, str]] = []
    for entry in root.findall("atom:entry", NS):
        entry_url = compact(entry.findtext("atom:id", namespaces=NS))
        arxiv_id = entry_url.rsplit("/", 1)[-1].split("v", 1)[0]
        authors = [
            compact(node.findtext("atom:name", namespaces=NS))
            for node in entry.findall("atom:author", NS)
        ]
        doi = compact(entry.findtext("arxiv:doi", namespaces=NS))
        categories = [node.attrib.get("term", "") for node in entry.findall("atom:category", NS)]
        rows.append(
            {
                "arxiv_id": arxiv_id,
                "title": compact(entry.findtext("atom:title", namespaces=NS)),
                "authors": "; ".join(authors),
                "published": compact(entry.findtext("atom:published", namespaces=NS)),
                "updated": compact(entry.findtext("atom:updated", namespaces=NS)),
                "abstract": compact(entry.findtext("atom:summary", namespaces=NS)),
                "categories": ";".join(categories),
                "doi": doi,
                "official_url": f"https://arxiv.org/abs/{arxiv_id}",
            }
        )
    return total, rows


def run_fetch() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    merged: dict[str, dict[str, str]] = {}
    manifest_queries: list[dict[str, object]] = []

    for query_id, query in QUERIES.items():
        start = 0
        total = None
        query_rows = 0
        files: list[dict[str, object]] = []
        while total is None or start < total:
            url = query_url(query, start, PAGE_SIZE)
            payload = fetch(url)
            page_total, rows = parse_page(payload)
            total = page_total
            raw_name = f"{query_id}_{start:04d}.xml"
            raw_path = RAW_DIR / raw_name
            raw_path.write_bytes(payload)
            files.append(
                {
                    "file": str(raw_path.relative_to(ROOT)).replace("\\", "/"),
                    "sha256": hashlib.sha256(payload).hexdigest(),
                    "rows": len(rows),
                    "start": start,
                }
            )
            for row in rows:
                existing = merged.setdefault(row["arxiv_id"], row | {"query_ids": query_id})
                ids = set(existing["query_ids"].split(";"))
                ids.add(query_id)
                existing["query_ids"] = ";".join(sorted(ids))
            query_rows += len(rows)
            start += len(rows)
            if not rows:
                break
            time.sleep(3)
        manifest_queries.append(
            {
                "query_id": query_id,
                "query": query,
                "api_total_results": total or 0,
                "rows_downloaded": query_rows,
                "raw_files": files,
            }
        )

    fields = [
        "arxiv_id",
        "title",
        "authors",
        "published",
        "updated",
        "abstract",
        "categories",
        "doi",
        "official_url",
        "query_ids",
    ]
    with RESULTS.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(sorted(merged.values(), key=lambda row: row["published"], reverse=True))

    manifest = {
        "search_type": "submission-time update search",
        "searched_at_utc": datetime.now(timezone.utc).isoformat(),
        "date_range": "2026-01-01 to 2026-07-15",
        "source": "arXiv official API",
        "api": API,
        "queries": manifest_queries,
        "unique_arxiv_records": len(merged),
        "normalized_results_file": str(RESULTS.relative_to(ROOT)).replace("\\", "/"),
        "normalized_results_sha256": hashlib.sha256(RESULTS.read_bytes()).hexdigest(),
        "scope_note": (
            "This update search supplements the reconciled historical screening ledger. "
            "It is a raw-hit export and is not reconstructed from the included corpus."
        ),
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"WROTE {RESULTS} ({len(merged)} unique records)")
    print(f"WROTE {MANIFEST}")


def validate() -> None:
    if not RESULTS.exists() or not MANIFEST.exists():
        raise SystemExit("Missing update-search outputs; run with --fetch first")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    digest = hashlib.sha256(RESULTS.read_bytes()).hexdigest()
    if digest != manifest.get("normalized_results_sha256"):
        raise SystemExit("Normalized results hash does not match manifest")
    with RESULTS.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != manifest.get("unique_arxiv_records"):
        raise SystemExit("Normalized row count does not match manifest")
    for query in manifest.get("queries", []):
        for item in query.get("raw_files", []):
            path = ROOT / item["file"]
            if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest() != item["sha256"]:
                raise SystemExit(f"Raw export missing or changed: {path}")
    print(f"PASS: update search contains {len(rows)} unique arXiv records")
    print("PASS: normalized and raw-export hashes match the manifest")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fetch", action="store_true", help="query the arXiv API and overwrite outputs")
    args = parser.parse_args()
    if args.fetch:
        run_fetch()
    validate()


if __name__ == "__main__":
    main()
