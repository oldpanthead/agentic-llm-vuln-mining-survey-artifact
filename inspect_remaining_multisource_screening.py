import argparse
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"


def read_csv(name):
    with (DATA / name).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--recommendation", default="manual_title_abstract")
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--count", type=int, default=60)
    parser.add_argument("--abstract-chars", type=int, default=500)
    parser.add_argument("--ids", default="")
    parser.add_argument("--rank-agentic", action="store_true")
    args = parser.parse_args()

    rows = read_csv("final_multisource_search_20260730_screening_recommendations.csv")
    assessed = {
        row["discovery_id"]
        for row in read_csv("final_multisource_search_20260730_fulltext_assessment.csv")
    }
    remaining = [
        row
        for row in rows
        if row["ai_assisted_screening_recommendation"] == args.recommendation
        and row["discovery_id"] not in assessed
    ]

    requested_ids = {item.strip() for item in args.ids.split(",") if item.strip()}
    if requested_ids:
        remaining = [row for row in rows if row["discovery_id"] in requested_ids]
    if args.rank_agentic:
        positive = {
            "agent": 4,
            "tool": 3,
            "feedback": 4,
            "iterative": 3,
            "execute": 3,
            "execution": 3,
            "fuzz": 4,
            "test case": 3,
            "testcase": 3,
            "sandbox": 3,
            "static analysis": 2,
            "dynamic analysis": 2,
            "patch": 2,
            "repair": 2,
            "workflow": 2,
            "orchestrat": 4,
            "vulnerabil": 2,
        }
        negative = {
            "survey": -4,
            "systematic review": -5,
            "large language model vulnerabil": -5,
            "prompt injection": -2,
            "jailbreak": -3,
            "voice agent": -3,
            "mobile agent": -3,
        }

        def score(row):
            text = f"{row.get('title', '')} {row.get('abstract', '')}".lower()
            return sum(weight for term, weight in positive.items() if term in text) + sum(
                weight for term, weight in negative.items() if term in text
            )

        remaining.sort(key=lambda row: (-score(row), row["discovery_id"]))

    print(f"RECOMMENDATION={args.recommendation} REMAINING={len(remaining)}")
    for index, row in enumerate(
        remaining[args.start : args.start + args.count], start=args.start
    ):
        abstract = " ".join((row.get("abstract") or "").split())
        print(f"{index:03d} {row['discovery_id']} | {row['title']}")
        print(f"  {abstract[:args.abstract_chars]}")


if __name__ == "__main__":
    main()
