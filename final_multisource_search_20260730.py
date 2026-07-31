#!/usr/bin/env python3
"""Run the final multi-source discovery search through 2026-07-30.

This script captures raw source responses and normalized source occurrences.
It does not assign analytical layers or modify the current corpus.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RAW = DATA / "final_multisource_search_20260730_raw"
RESULTS = DATA / "final_multisource_search_20260730_results.csv"
MANIFEST = DATA / "final_multisource_search_20260730_manifest.json"
ACCESS_LOG = DATA / "final_multisource_search_20260730_access_log.csv"

DATE_FROM = "2023-01-01"
DATE_TO = "2026-07-30"
ARXIV_FROM = "202301010000"
ARXIV_TO = "202607302359"
USER_AGENT = (
    "agentic-llm-vuln-mining-survey/2.0 "
    "(mailto:fangjingran25@mails.ucas.ac.cn)"
)

QUERY_FAMILIES = {
    "agent_task": {
        "plain": (
            '"large language model" agent agentic multi-agent vulnerability '
            "fuzzing penetration testing cyber reasoning"
        ),
        "arxiv": (
            f'submittedDate:[{ARXIV_FROM} TO {ARXIV_TO}] AND '
            '(ti:vulnerability OR ti:fuzzing OR ti:pentest OR '
            'ti:"penetration testing" OR ti:"cyber reasoning" OR ti:security) '
            'AND (all:"large language model" OR all:LLM) '
            'AND (all:agent OR all:agentic OR all:"multi-agent")'
        ),
        "web": (
            '("large language model" OR LLM) '
            '(agent OR agentic OR "multi-agent") '
            '(vulnerability OR fuzzing OR "penetration testing" OR '
            '"cyber reasoning")'
        ),
    },
    "execution_validation": {
        "plain": (
            '"large language model" vulnerability fuzzing software security '
            "execution feedback validation tool crash coverage sanitizer "
            "oracle replay harness"
        ),
        "arxiv": (
            f'submittedDate:[{ARXIV_FROM} TO {ARXIV_TO}] AND '
            '(ti:vulnerability OR ti:fuzzing OR ti:security) '
            'AND (all:"large language model" OR all:LLM) '
            'AND (all:validation OR all:feedback OR all:execution OR all:tool '
            'OR all:crash OR all:coverage OR all:sanitizer OR all:oracle '
            'OR all:replay OR all:harness)'
        ),
        "web": (
            '("large language model" OR LLM) '
            '(vulnerability OR fuzzing OR "software security") '
            '(validation OR feedback OR execution OR tool OR crash OR coverage '
            'OR sanitizer OR oracle OR replay OR harness)'
        ),
    },
    "pov_crs": {
        "plain": (
            '"proof of vulnerability" PoV "cyber reasoning system" CRS '
            "LLM agent"
        ),
        "arxiv": (
            f'submittedDate:[{ARXIV_FROM} TO {ARXIV_TO}] AND '
            '(all:"proof of vulnerability" OR all:PoV OR '
            'all:"cyber reasoning system" OR all:CRS) '
            'AND (all:LLM OR all:"large language model" OR all:agent)'
        ),
        "web": (
            '("proof of vulnerability" OR PoV OR "cyber reasoning system" '
            'OR CRS) (LLM OR "large language model" OR agent)'
        ),
    },
    "review_context": {
        "plain": (
            'review survey "large language model" LLM vulnerability fuzzing '
            '"software security"'
        ),
        "arxiv": (
            f'submittedDate:[{ARXIV_FROM} TO {ARXIV_TO}] AND '
            '(ti:review OR ti:survey OR ti:"systematic literature review") '
            'AND (all:LLM OR all:"large language model") '
            'AND (all:vulnerability OR all:fuzzing OR all:"software security")'
        ),
        "web": (
            '(review OR survey) ("large language model" OR LLM) '
            '(vulnerability OR fuzzing OR "software security")'
        ),
    },
}

PUBLISHER_PREFIXES = {
    "acm_crossref": ("ACM publisher metadata", "10.1145"),
    "ieee_crossref": ("IEEE publisher metadata", "10.1109"),
    "springer_crossref": ("Springer publisher metadata", "10.1007"),
    "elsevier_crossref": ("Elsevier publisher metadata", "10.1016"),
}

WEB_SOURCES = {
    "acm_web": ("ACM Digital Library pages", "dl.acm.org"),
    "ieee_web": ("IEEE Xplore pages", "ieeexplore.ieee.org"),
    "springer_web": ("SpringerLink pages", "link.springer.com"),
    "sciencedirect_web": ("ScienceDirect pages", "sciencedirect.com"),
    "usenix_web": ("USENIX pages", "usenix.org"),
    "ndss_web": ("NDSS pages", "ndss-symposium.org"),
    "dblp_web": ("DBLP pages", "dblp.org"),
}

ARXIV_API = "https://export.arxiv.org/api/query"
CROSSREF_API = "https://api.crossref.org/works"
OPENALEX_API = "https://api.openalex.org/works"
BING_SEARCH = "https://www.bing.com/search"
SCHOLAR_SEARCH = "https://scholar.google.com/scholar"

ARXIV_NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "open": "http://a9.com/-/spec/opensearch/1.1/",
    "arxiv": "http://arxiv.org/schemas/atom",
}


@dataclass
class AccessEvent:
    source_id: str
    query_id: str
    interface: str
    query: str
    attempted_at_utc: str
    status: str
    http_status: str
    raw_file: str
    records_returned: int
    total_reported: str
    notes: str


def compact(value: Any) -> str:
    return " ".join(str(value or "").split())


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def safe_name(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.-]+", "_", value).strip("_")


def fetch(url: str, *, timeout: int = 180, retries: int = 3) -> tuple[bytes, int]:
    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": USER_AGENT,
                    "Accept": "application/json, application/xml, text/html;q=0.9, */*;q=0.8",
                },
            )
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return response.read(), int(response.status)
        except Exception as exc:  # network failures are logged by the caller
            last_error = exc
            if attempt + 1 < retries:
                time.sleep(3 * (attempt + 1))
    assert last_error is not None
    raise last_error


def save_raw(source_id: str, query_id: str, page: int, suffix: str, payload: bytes) -> Path:
    path = RAW / source_id / f"{safe_name(query_id)}_{page:04d}.{suffix}"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)
    return path


def parse_date_parts(message: dict[str, Any]) -> str:
    for key in ("published-online", "published-print", "published", "issued", "created"):
        value = message.get(key, {})
        parts = value.get("date-parts") if isinstance(value, dict) else None
        if parts and parts[0]:
            vals = [str(v) for v in parts[0]]
            return "-".join(vals + ["01"] * (3 - len(vals)))
    return ""


def normalize_doi(value: str) -> str:
    value = compact(value).lower()
    value = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", value)
    return value


def normalize_arxiv(value: str) -> str:
    value = compact(value)
    value = re.sub(r"^https?://arxiv\.org/(?:abs|pdf)/", "", value)
    value = re.sub(r"\.pdf$", "", value)
    return re.sub(r"v\d+$", "", value)


def arxiv_rows(query_id: str, query: str, access: list[AccessEvent]) -> list[dict[str, str]]:
    merged: dict[str, dict[str, str]] = {}
    start = 0
    page = 0
    page_size = 100
    total: int | None = None
    while total is None or start < total:
        params = urllib.parse.urlencode(
            {
                "search_query": query,
                "start": start,
                "max_results": page_size,
                "sortBy": "submittedDate",
                "sortOrder": "descending",
            }
        )
        url = f"{ARXIV_API}?{params}"
        payload, status = fetch(url)
        raw_path = save_raw("arxiv", query_id, page, "xml", payload)
        root = ET.fromstring(payload)
        total = int(root.findtext("open:totalResults", "0", ARXIV_NS))
        entries = root.findall("atom:entry", ARXIV_NS)
        for entry in entries:
            entry_url = compact(entry.findtext("atom:id", "", ARXIV_NS))
            arxiv_id = normalize_arxiv(entry_url.rsplit("/", 1)[-1])
            authors = [
                compact(node.findtext("atom:name", "", ARXIV_NS))
                for node in entry.findall("atom:author", ARXIV_NS)
            ]
            doi = normalize_doi(entry.findtext("arxiv:doi", "", ARXIV_NS))
            merged[arxiv_id] = {
                "source_id": "arxiv",
                "query_id": query_id,
                "source_record_id": arxiv_id,
                "title": compact(entry.findtext("atom:title", "", ARXIV_NS)),
                "authors": "; ".join(authors),
                "publication_date": compact(entry.findtext("atom:published", "", ARXIV_NS))[:10],
                "year": compact(entry.findtext("atom:published", "", ARXIV_NS))[:4],
                "abstract": compact(entry.findtext("atom:summary", "", ARXIV_NS)),
                "venue_or_source": "arXiv",
                "publisher": "",
                "doi": doi,
                "arxiv_id": arxiv_id,
                "url": f"https://arxiv.org/abs/{arxiv_id}",
                "record_type": "preprint",
                "raw_file": relative(raw_path),
            }
        access.append(
            AccessEvent(
                "arxiv",
                query_id,
                "official API",
                query,
                datetime.now(timezone.utc).isoformat(),
                "ok",
                str(status),
                relative(raw_path),
                len(entries),
                str(total),
                "",
            )
        )
        if not entries:
            break
        start += len(entries)
        page += 1
        time.sleep(3)
    return list(merged.values())


def crossref_rows(
    source_id: str,
    query_id: str,
    query: str,
    access: list[AccessEvent],
    *,
    prefix: str | None = None,
    max_records: int = 500,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    cursor = "*"
    page = 0
    total = ""
    while True:
        filters = [f"from-pub-date:{DATE_FROM}", f"until-pub-date:{DATE_TO}"]
        if prefix:
            filters.append(f"prefix:{prefix}")
        remaining = max_records - len(rows)
        if remaining <= 0:
            break
        params = {
            "query.bibliographic": query,
            "filter": ",".join(filters),
            "rows": str(min(500, remaining)),
            "cursor": cursor,
            "select": (
                "DOI,title,author,published-online,published-print,published,"
                "issued,created,URL,abstract,publisher,type,container-title,subject"
            ),
            "mailto": "fangjingran25@mails.ucas.ac.cn",
        }
        url = f"{CROSSREF_API}?{urllib.parse.urlencode(params)}"
        payload, status = fetch(url)
        raw_path = save_raw(source_id, query_id, page, "json", payload)
        message = json.loads(payload)["message"]
        total = str(message.get("total-results", ""))
        items = message.get("items", [])
        for item in items:
            doi = normalize_doi(item.get("DOI", ""))
            title = compact((item.get("title") or [""])[0])
            authors = "; ".join(
                compact(" ".join(filter(None, [a.get("given", ""), a.get("family", "")])))
                for a in item.get("author", [])
            )
            date = parse_date_parts(item)
            rows.append(
                {
                    "source_id": source_id,
                    "query_id": query_id,
                    "source_record_id": doi or compact(item.get("URL", "")),
                    "title": title,
                    "authors": authors,
                    "publication_date": date,
                    "year": date[:4],
                    "abstract": compact(re.sub(r"<[^>]+>", " ", item.get("abstract", ""))),
                    "venue_or_source": compact((item.get("container-title") or [""])[0]),
                    "publisher": compact(item.get("publisher", "")),
                    "doi": doi,
                    "arxiv_id": "",
                    "url": compact(item.get("URL", "")),
                    "record_type": compact(item.get("type", "")),
                    "raw_file": relative(raw_path),
                }
            )
        access.append(
            AccessEvent(
                source_id,
                query_id,
                "Crossref REST API",
                query,
                datetime.now(timezone.utc).isoformat(),
                "ok",
                str(status),
                relative(raw_path),
                len(items),
                total,
                (
                    f"publisher DOI prefix={prefix}; ranked supplementary metadata "
                    f"lookup capped at {max_records} records"
                    if prefix
                    else f"ranked supplementary metadata lookup capped at {max_records} records"
                ),
            )
        )
        next_cursor = compact(message.get("next-cursor", ""))
        if (
            not items
            or len(rows) >= max_records
            or len(items) < min(500, remaining)
            or not next_cursor
            or next_cursor == cursor
        ):
            break
        cursor = next_cursor
        page += 1
        time.sleep(1)
    return rows


def openalex_rows(query_id: str, query: str, access: list[AccessEvent]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    cursor = "*"
    page = 0
    total = ""
    while True:
        params = {
            "search": query,
            "filter": f"from_publication_date:{DATE_FROM},to_publication_date:{DATE_TO}",
            "per-page": "200",
            "cursor": cursor,
            "mailto": "fangjingran25@mails.ucas.ac.cn",
        }
        url = f"{OPENALEX_API}?{urllib.parse.urlencode(params)}"
        payload, status = fetch(url)
        raw_path = save_raw("openalex", query_id, page, "json", payload)
        data = json.loads(payload)
        total = str(data.get("meta", {}).get("count", ""))
        items = data.get("results", [])
        for item in items:
            primary = item.get("primary_location") or {}
            source = primary.get("source") or {}
            ids = item.get("ids") or {}
            doi = normalize_doi(ids.get("doi", ""))
            arxiv_id = normalize_arxiv(ids.get("arxiv", ""))
            authors = "; ".join(
                compact((entry.get("author") or {}).get("display_name", ""))
                for entry in item.get("authorships", [])
            )
            rows.append(
                {
                    "source_id": "openalex",
                    "query_id": query_id,
                    "source_record_id": compact(item.get("id", "")),
                    "title": compact(item.get("display_name", "")),
                    "authors": authors,
                    "publication_date": compact(item.get("publication_date", "")),
                    "year": str(item.get("publication_year") or ""),
                    "abstract": "",
                    "venue_or_source": compact(source.get("display_name", "")),
                    "publisher": compact(source.get("host_organization_name", "")),
                    "doi": doi,
                    "arxiv_id": arxiv_id,
                    "url": compact(primary.get("landing_page_url", "") or ids.get("openalex", "")),
                    "record_type": compact(item.get("type", "")),
                    "raw_file": relative(raw_path),
                }
            )
        access.append(
            AccessEvent(
                "openalex",
                query_id,
                "OpenAlex API",
                query,
                datetime.now(timezone.utc).isoformat(),
                "ok",
                str(status),
                relative(raw_path),
                len(items),
                total,
                "",
            )
        )
        next_cursor = compact(data.get("meta", {}).get("next_cursor", ""))
        if not items or not next_cursor or next_cursor == cursor:
            break
        cursor = next_cursor
        page += 1
        time.sleep(1)
    return rows


class BingParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.results: list[dict[str, str]] = []
        self._in_result = False
        self._capture_title = False
        self._capture_snippet = False
        self._href = ""
        self._title: list[str] = []
        self._snippet: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = dict(attrs)
        classes = set((attr.get("class") or "").split())
        if tag == "li" and "b_algo" in classes:
            self._in_result = True
            self._href = ""
            self._title = []
            self._snippet = []
        elif self._in_result and tag == "a" and not self._href:
            self._href = attr.get("href") or ""
            self._capture_title = True
        elif self._in_result and tag == "p":
            self._capture_snippet = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "a":
            self._capture_title = False
        elif tag == "p":
            self._capture_snippet = False
        elif tag == "li" and self._in_result:
            title = compact(html.unescape("".join(self._title)))
            if self._href and title:
                self.results.append(
                    {
                        "url": self._href,
                        "title": title,
                        "snippet": compact(html.unescape("".join(self._snippet))),
                    }
                )
            self._in_result = False

    def handle_data(self, data: str) -> None:
        if self._capture_title:
            self._title.append(data)
        if self._capture_snippet:
            self._snippet.append(data)


def bing_rows(
    source_id: str,
    source_name: str,
    domain: str,
    query_id: str,
    query: str,
    access: list[AccessEvent],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    seen: set[str] = set()
    full_query = f"site:{domain} {query} after:2022-12-31 before:2026-07-31"
    for page, first in enumerate((1, 51)):
        params = urllib.parse.urlencode({"q": full_query, "count": "50", "first": str(first)})
        url = f"{BING_SEARCH}?{params}"
        try:
            payload, status = fetch(url)
            raw_path = save_raw(source_id, query_id, page, "html", payload)
            parser = BingParser()
            parser.feed(payload.decode("utf-8", errors="replace"))
            added = 0
            for result in parser.results:
                if domain not in result["url"].lower() or result["url"] in seen:
                    continue
                seen.add(result["url"])
                added += 1
                rows.append(
                    {
                        "source_id": source_id,
                        "query_id": query_id,
                        "source_record_id": result["url"],
                        "title": result["title"],
                        "authors": "",
                        "publication_date": "",
                        "year": "",
                        "abstract": result["snippet"],
                        "venue_or_source": source_name,
                        "publisher": "",
                        "doi": "",
                        "arxiv_id": "",
                        "url": result["url"],
                        "record_type": "source-restricted web result",
                        "raw_file": relative(raw_path),
                    }
                )
            access.append(
                AccessEvent(
                    source_id,
                    query_id,
                    "Bing source-restricted web search",
                    full_query,
                    datetime.now(timezone.utc).isoformat(),
                    (
                        "supplementary_web_results_retrieved"
                        if added
                        else "supplementary_web_check_no_exportable_results"
                    ),
                    str(status),
                    relative(raw_path),
                    added,
                    "",
                    (
                        "Supplementary source-restricted web discovery; this is not represented as a complete "
                        "publisher-database export."
                    ),
                )
            )
            if len(parser.results) < 45:
                break
            time.sleep(2)
        except Exception as exc:
            access.append(
                AccessEvent(
                    source_id,
                    query_id,
                    "Bing source-restricted web search",
                    full_query,
                    datetime.now(timezone.utc).isoformat(),
                    "blocked_or_failed",
                    "",
                    "",
                    0,
                    "",
                    compact(exc),
                )
            )
            break
    return rows


def record_blocked_interfaces(access: list[AccessEvent]) -> None:
    checks = [
        (
            "google_scholar",
            SCHOLAR_SEARCH
            + "?"
            + urllib.parse.urlencode(
                {
                    "q": '"agentic" LLM vulnerability fuzzing',
                    "as_ylo": "2023",
                    "as_yhi": "2026",
                    "num": "20",
                }
            ),
            "Google Scholar supplementary search",
        ),
        ("scopus", "", "Scopus authenticated database"),
        ("web_of_science", "", "Web of Science authenticated database"),
    ]
    for source_id, url, interface in checks:
        if not url:
            access.append(
                AccessEvent(
                    source_id,
                    "access_check",
                    interface,
                    "",
                    datetime.now(timezone.utc).isoformat(),
                    "not_accessible_without_authenticated_subscription",
                    "",
                    "",
                    0,
                    "",
                    "No authenticated API key or institutional session was available in the execution environment.",
                )
            )
            continue
        try:
            payload, status = fetch(url, retries=1)
            raw_path = save_raw(source_id, "access_check", 0, "html", payload)
            access.append(
                AccessEvent(
                    source_id,
                    "access_check",
                    interface,
                    url,
                    datetime.now(timezone.utc).isoformat(),
                    "ok",
                    str(status),
                    relative(raw_path),
                    0,
                    "",
                    "Availability check only; no result export was inferred from the page.",
                )
            )
        except Exception as exc:
            access.append(
                AccessEvent(
                    source_id,
                    "access_check",
                    interface,
                    url,
                    datetime.now(timezone.utc).isoformat(),
                    "blocked_or_failed",
                    "",
                    "",
                    0,
                    "",
                    compact(exc),
                )
            )


def write_rows(rows: Iterable[dict[str, str]]) -> int:
    fields = [
        "source_id",
        "query_id",
        "source_record_id",
        "title",
        "authors",
        "publication_date",
        "year",
        "abstract",
        "venue_or_source",
        "publisher",
        "doi",
        "arxiv_id",
        "url",
        "record_type",
        "raw_file",
    ]
    rows = list(rows)
    with RESULTS.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


def write_access(events: list[AccessEvent]) -> None:
    fields = list(AccessEvent.__dataclass_fields__)
    with ACCESS_LOG.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(event.__dict__ for event in events)


def run_fetch() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, str]] = []
    access: list[AccessEvent] = []

    for query_id, family in QUERY_FAMILIES.items():
        rows.extend(arxiv_rows(query_id, family["arxiv"], access))
        rows.extend(openalex_rows(query_id, family["plain"], access))
        rows.extend(crossref_rows("crossref", query_id, family["plain"], access))
        for source_id, (source_name, prefix) in PUBLISHER_PREFIXES.items():
            rows.extend(
                crossref_rows(
                    source_id,
                    query_id,
                    family["plain"],
                    access,
                    prefix=prefix,
                )
            )
        for source_id, (source_name, domain) in WEB_SOURCES.items():
            rows.extend(
                bing_rows(
                    source_id,
                    source_name,
                    domain,
                    query_id,
                    family["web"],
                    access,
                )
            )

    record_blocked_interfaces(access)
    row_count = write_rows(rows)
    write_access(access)
    manifest = {
        "search_type": "final multi-source coverage search",
        "executed_at_utc": datetime.now(timezone.utc).isoformat(),
        "coverage_window": f"{DATE_FROM} to {DATE_TO}",
        "query_families": QUERY_FAMILIES,
        "publisher_prefixes": PUBLISHER_PREFIXES,
        "web_sources": WEB_SOURCES,
        "source_occurrences": row_count,
        "results_file": relative(RESULTS),
        "results_sha256": digest(RESULTS.read_bytes()),
        "access_log_file": relative(ACCESS_LOG),
        "access_log_sha256": digest(ACCESS_LOG.read_bytes()),
        "raw_files": [
            {
                "file": relative(path),
                "sha256": digest(path.read_bytes()),
                "bytes": path.stat().st_size,
            }
            for path in sorted(RAW.rglob("*"))
            if path.is_file()
        ],
        "counting_note": (
            "Rows are source occurrences, not canonical studies. Corpus counts "
            "change only after deduplication, screening, and version reconciliation."
        ),
    }
    MANIFEST.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"WROTE {RESULTS} ({row_count} source occurrences)")
    print(f"WROTE {ACCESS_LOG} ({len(access)} access events)")
    print(f"WROTE {MANIFEST}")


def validate() -> None:
    required = [RESULTS, ACCESS_LOG, MANIFEST]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise SystemExit(f"Missing search outputs: {missing}")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if digest(RESULTS.read_bytes()) != manifest.get("results_sha256"):
        raise SystemExit("Results hash does not match manifest")
    if digest(ACCESS_LOG.read_bytes()) != manifest.get("access_log_sha256"):
        raise SystemExit("Access-log hash does not match manifest")
    with RESULTS.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != int(manifest.get("source_occurrences", -1)):
        raise SystemExit("Result row count does not match manifest")
    for item in manifest.get("raw_files", []):
        path = ROOT / item["file"]
        if not path.exists() or digest(path.read_bytes()) != item["sha256"]:
            raise SystemExit(f"Raw source response missing or changed: {path}")
    print(f"PASS: {len(rows)} source occurrences match the manifest")
    print("PASS: normalized results, access log, and raw responses match recorded hashes")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fetch", action="store_true")
    args = parser.parse_args()
    if args.fetch:
        run_fetch()
    validate()


if __name__ == "__main__":
    main()
