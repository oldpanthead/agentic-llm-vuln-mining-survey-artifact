#!/usr/bin/env python3
"""Fetch publicly accessible full texts for final-search review candidates.

PDFs are stored in a local review cache outside the public artifact. The
artifact records only source URLs, status, file hashes, and extracted-text
availability.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
import time
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RECOMMENDATIONS = DATA / "final_multisource_search_20260730_screening_recommendations.csv"
OUTPUT = DATA / "final_multisource_search_20260730_fulltext_access.csv"
CACHE = ROOT.parent.parent.parent / "02_literature" / "final_multisource_20260730"
USER_AGENT = "agentic-llm-vuln-mining-survey/2.0 (mailto:fangjingran25@mails.ucas.ac.cn)"
MANUAL_PROMOTIONS = {
    "FMS0090",
    "FMS0100",
    "FMS0120",
    "FMS0135",
    "FMS0205",
    "FMS0209",
    "FMS0219",
    "FMS0233",
    "FMS0239",
    "FMS0253",
    "FMS0279",
    "FMS0297",
    "FMS0307",
    "FMS0327",
    "FMS0347",
    "FMS0362",
    "FMS0364",
    "FMS0374",
    "FMS0376",
    "FMS0384",
    "FMS0389",
    "FMS0412",
    "FMS0419",
    "FMS0426",
    "FMS0443",
    "FMS0479",
    "FMS0488",
    "FMS0513",
    "FMS0533",
    "FMS0541",
    "FMS0558",
    "FMS0604",
    "FMS0614",
    "FMS0642",
    "FMS0659",
    "FMS0677",
    "FMS0684",
    "FMS0686",
    "FMS0691",
    "FMS0707",
    "FMS0733",
    "FMS0734",
    "FMS0742",
    "FMS0752",
    "FMS0755",
    "FMS0775",
    "FMS0782",
    "FMS0800",
    "FMS0825",
    "FMS0768",
    "FMS0842",
    "FMS0844",
    "FMS0885",
    "FMS0888",
    "FMS0899",
    "FMS0913",
    "FMS0914",
    "FMS0916",
    "FMS0925",
    "FMS0928",
    "FMS0947",
    "FMS0948",
    "FMS0961",
    "FMS1031",
    "FMS1002",
    "FMS1041",
    "FMS1076",
    "FMS1081",
    "FMS1090",
    "FMS1095",
    "FMS1096",
    "FMS1103",
    "FMS1125",
    "FMS1128",
    "FMS1136",
    "FMS1144",
    "FMS1154",
    "FMS1155",
    "FMS1166",
    "FMS1174",
    "FMS1193",
    "FMS1219",
    "FMS1228",
    "FMS1223",
    "FMS1233",
    "FMS1239",
    "FMS1265",
    "FMS1275",
    "FMS1283",
    "FMS1315",
    "FMS1325",
    "FMS1326",
    "FMS1321",
    "FMS1334",
    "FMS1338",
    "FMS1381",
    "FMS1389",
    "FMS1390",
    "FMS1394",
    "FMS1435",
    "FMS1473",
    "FMS1491",
    "FMS1495",
    "FMS1509",
    "FMS1512",
    "FMS1530",
    "FMS1549",
    "FMS1592",
    "FMS1602",
    "FMS1600",
    "FMS1601",
    "FMS1613",
    "FMS1638",
    "FMS1637",
    "FMS1641",
    "FMS1640",
}
MANUAL_PUBLIC_PDFS = {
    "FMS0120": "https://arxiv.org/pdf/2603.20637",
    "FMS0209": "https://www.usenix.org/system/files/usenixsecurity25-nong.pdf",
    "FMS0109": "https://daoyuan14.github.io/papers/TSE25_LLM-SmartAudit.pdf",
    "FMS0307": "https://arxiv.org/pdf/2510.23101",
    "FMS0412": "https://arxiv.org/pdf/2405.03927",
    "FMS0443": "https://arxiv.org/pdf/2409.09661",
    "FMS0489": "https://aclanthology.org/2025.naacl-long.212.pdf",
    "FMS0513": "https://arxiv.org/pdf/2506.15648",
    "FMS0558": "https://arxiv.org/pdf/2607.13439",
    "FMS0659": "https://yuntongzhang.github.io/assets/pdf/icse26-seip.pdf",
    "FMS0707": "https://www.usenix.org/system/files/usenixsecurity24-asmita.pdf",
    "FMS0752": "https://arxiv.org/pdf/2512.03420",
    "FMS0619": "https://www.scitepress.org/Papers/2026/144804/144804.pdf",
    "FMS0842": "https://spectrum.library.concordia.ca/id/eprint/996544/1/Dai_MA_F2025.pdf",
    "FMS0844": "https://arxiv.org/pdf/2607.25647",
    "FMS0961": "https://arxiv.org/pdf/2604.04561",
    "FMS1002": "https://arxiv.org/pdf/2510.15690",
    "FMS1081": "https://arxiv.org/pdf/2605.04499",
    "FMS1219": "https://arxiv.org/pdf/2602.11209",
    "FMS1228": "https://arxiv.org/pdf/2603.08520",
    "FMS0902": "https://www.researchgate.net/publication/390823751_LLM_Agentic_Workflow_for_Automated_Vulnerability_Detection_and_Remediation_in_Infrastructure-as-Code/fulltext/67ff726fbfbe974b23aaba57/LLM-Agentic-Workflow-for-Automated-Vulnerability-Detection-and-Remediation-in-Infrastructure-as-Code.pdf",
    "FMS0922": "https://mdpi-res.com/d_attachment/electronics/electronics-15-00954/article_deploy/electronics-15-00954.pdf",
    "FMS0945": "https://obj.umiacs.umd.edu/locus/2508.21302v3.pdf",
    "FMS1024": "https://chenbihuan.github.io/paper/fse25-wu-mystique.pdf",
    "FMS1088": "https://assets-eu.researchsquare.com/files/rs-7582841/v1_covered_6b896846-7fe1-4369-88c9-9aba18c15e3f.pdf",
    "FMS1637": "https://arxiv.org/pdf/2501.04312",
}


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def norm_title(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (value or "").lower()).strip()


def arxiv_id(value: str) -> str:
    value = (value or "").strip().lower()
    if re.fullmatch(r"\d{4}\.\d{4,5}(?:v\d+)?", value):
        return re.sub(r"v\d+$", "", value)
    match = re.search(
        r"(?:arxiv(?:\.org/(?:abs|pdf)/|:|\.)|10\.48550/arxiv\.)"
        r"(\d{4}\.\d{4,5})(?:v\d+)?",
        value,
    )
    return match.group(1) if match else ""


def safe_name(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.-]+", "_", value).strip("_")[:120]


def fetch(url: str, timeout: int = 45) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def openalex_pdf(doi: str) -> tuple[str, str]:
    if not doi:
        return "", "No DOI or arXiv identifier."
    work_id = urllib.parse.quote(f"https://doi.org/{doi}", safe="")
    url = f"https://api.openalex.org/works/{work_id}?mailto=fangjingran25@mails.ucas.ac.cn"
    try:
        payload = json.loads(fetch(url).decode("utf-8"))
    except Exception as exc:
        return "", f"OpenAlex lookup failed: {type(exc).__name__}: {exc}"
    locations = []
    for key in ("best_oa_location", "primary_location"):
        location = payload.get(key)
        if isinstance(location, dict):
            locations.append(location)
    locations.extend(
        location
        for location in payload.get("locations", [])
        if isinstance(location, dict)
    )
    for location in locations:
        pdf_url = location.get("pdf_url")
        if pdf_url:
            return str(pdf_url), "OpenAlex open-access PDF location."
    return "", "No open-access PDF URL reported by OpenAlex."


def write_audit(audit: list[dict[str, str]]) -> None:
    if not audit:
        return
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(audit[0]))
        writer.writeheader()
        writer.writerows(audit)


def main() -> None:
    CACHE.mkdir(parents=True, exist_ok=True)
    candidates = []
    for row in rows(RECOMMENDATIONS):
        if (
            row["ai_assisted_screening_recommendation"]
            not in {"full_text_priority", "manual_full_text_needed"}
            and row["discovery_id"] not in MANUAL_PROMOTIONS
        ):
            continue
        if row["triage_status"] == "existing_study_or_version":
            continue
        candidates.append(row)

    audit: list[dict[str, str]] = []
    for index, row in enumerate(candidates, start=1):
        identifier = (
            arxiv_id(row["arxiv_id"])
            or arxiv_id(row.get("urls", ""))
            or arxiv_id(row.get("doi", ""))
        )
        if row["discovery_id"] in MANUAL_PUBLIC_PDFS:
            pdf_url = MANUAL_PUBLIC_PDFS[row["discovery_id"]]
            if not identifier:
                identifier = arxiv_id(pdf_url)
            pdf_urls = [pdf_url]
            basis = "Public author, repository, or publisher PDF located by exact-title follow-up."
        elif identifier:
            pdf_urls = [
                f"https://arxiv.org/pdf/{identifier}",
                f"https://export.arxiv.org/pdf/{identifier}",
            ]
            pdf_url = pdf_urls[0]
            basis = "arXiv public PDF; official export endpoint used as fallback."
        else:
            pdf_url, basis = openalex_pdf(row["doi"])
            pdf_urls = [pdf_url] if pdf_url else []

        status = "not_available"
        sha256 = ""
        local_pdf = ""
        local_text = ""
        note = basis
        if pdf_urls:
            pdf_path = CACHE / f"{row['discovery_id']}_{safe_name(row['title'])}.pdf"
            text_path = pdf_path.with_suffix(".txt")
            try:
                if pdf_path.exists() and pdf_path.read_bytes().startswith(b"%PDF"):
                    payload = pdf_path.read_bytes()
                else:
                    last_error: Exception | None = None
                    payload = b""
                    for candidate_url in pdf_urls:
                        try:
                            candidate_payload = fetch(candidate_url)
                            if not candidate_payload.startswith(b"%PDF"):
                                raise ValueError("Downloaded content is not a PDF.")
                            payload = candidate_payload
                            pdf_url = candidate_url
                            break
                        except Exception as exc:
                            last_error = exc
                            time.sleep(1.0)
                    if not payload:
                        if last_error is None:
                            raise ValueError("No PDF endpoint was available.")
                        raise last_error
                if not payload.startswith(b"%PDF"):
                    raise ValueError("Downloaded content is not a PDF.")
                pdf_path.write_bytes(payload)
                sha256 = hashlib.sha256(payload).hexdigest()
                local_pdf = str(pdf_path)
                proc = subprocess.run(
                    ["pdftotext", "-layout", str(pdf_path), str(text_path)],
                    capture_output=True,
                    text=True,
                    timeout=180,
                )
                if proc.returncode == 0 and text_path.exists():
                    local_text = str(text_path)
                    status = "downloaded_and_text_extracted"
                else:
                    status = "downloaded_pdf_only"
                    note += f" pdftotext exit={proc.returncode}: {proc.stderr.strip()}"
            except Exception as exc:
                status = "fetch_failed"
                note += f" Fetch failed: {type(exc).__name__}: {exc}"
        audit.append(
            {
                "discovery_id": row["discovery_id"],
                "title": row["title"],
                "doi": row["doi"],
                "arxiv_id": identifier,
                "public_fulltext_url": pdf_url,
                "access_basis": basis,
                "access_status": status,
                "sha256": sha256,
                "local_review_pdf": local_pdf,
                "local_extracted_text": local_text,
                "notes": note,
            }
        )
        # Preserve progress so an interrupted network run remains resumable.
        write_audit(audit)
        print(f"[{index}/{len(candidates)}] {row['discovery_id']} {status}")
        time.sleep(0.7)

    write_audit(audit)
    print(f"WROTE {OUTPUT} ({len(audit)} candidates)")


if __name__ == "__main__":
    main()
