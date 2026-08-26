#!/usr/bin/env python3
"""Build and validate a clean public artifact export."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
RELEASE_MANIFEST = ROOT / "manifests" / "release_manifest.json"


def read_manifest(path: Path) -> tuple[list[str], list[str]]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    manuscript = payload.get("manuscript_artifact_paths", [])
    static = payload.get("static_release_files", [])
    if not isinstance(manuscript, list) or not isinstance(static, list):
        raise SystemExit("ERROR: release manifest sections must be lists")
    return manuscript, static


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path, help="new, empty export directory")
    args = parser.parse_args()

    output = args.output.resolve()
    root = ROOT.resolve()
    if output == root or root in output.parents:
        raise SystemExit("ERROR: export directory must be outside the source artifact")
    if output.exists():
        raise SystemExit(f"ERROR: export target already exists: {output}")

    try:
        manuscript_paths, static_paths = read_manifest(RELEASE_MANIFEST)
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"ERROR: cannot read {RELEASE_MANIFEST}: {exc}") from exc
    paths = static_paths + manuscript_paths
    duplicates = sorted({path for path in paths if paths.count(path) > 1})
    if duplicates:
        raise SystemExit(f"ERROR: duplicate release path(s): {duplicates}")

    missing = [path for path in paths if not (ROOT / path).is_file()]
    if missing:
        raise SystemExit(f"ERROR: missing release path(s): {missing}")

    for relative in paths:
        source = ROOT / relative
        destination = output / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

    result = subprocess.run(
        [sys.executable, "reproduce_tables.py"],
        cwd=output,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit("ERROR: exported artifact failed validation")

    total_bytes = sum(path.stat().st_size for path in output.rglob("*") if path.is_file())
    print(f"RELEASE_FILES={len(paths)}")
    print(f"RELEASE_BYTES={total_bytes}")
    print(f"RELEASE_OUTPUT={output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
