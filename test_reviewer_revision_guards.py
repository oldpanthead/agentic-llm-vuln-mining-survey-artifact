#!/usr/bin/env python3
"""Regression guards for the five reviewer-driven validity corrections."""

from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

from integrate_third_party_rereview import write_statistics


class ReviewerRevisionGuardTests(unittest.TestCase):
    def test_reporting_and_audit_is_not_a_reportable_prevalence_estimate(self) -> None:
        matrix = [
            {
                "analytical_role": "target_software_study",
                "lifecycle_coverage": "reporting and audit",
                "cross_stage_capabilities": "no qualifying label observed",
                "strongest_evidence_output": "candidate judgment",
                "external_traceability": "no external trace reported",
                "primary_system_shape": "candidate-analysis system",
            }
        ]
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp)
            write_statistics(data, matrix)
            with (data / "adjudicated_synthesis_statistics_199.csv").open(
                encoding="utf-8", newline=""
            ) as handle:
                rows = list(csv.DictReader(handle))

        reporting = next(
            row
            for row in rows
            if row["field"] == "lifecycle coverage"
            and row["label"] == "reporting and audit"
        )
        self.assertEqual(reporting["reportable_point_estimate"], "no")
        self.assertEqual(reporting["interpretation_scope"], "adjudicated descriptive outcome only")


if __name__ == "__main__":
    unittest.main()
