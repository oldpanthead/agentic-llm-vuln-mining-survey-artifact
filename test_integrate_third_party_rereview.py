#!/usr/bin/env python3
"""Tests for importing the external rereview without mutating raw coder records."""

from __future__ import annotations

import unittest

from integrate_third_party_rereview import build_integration_rows


class ThirdPartyRereviewIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.template = [
            {
                "disagreement_id": "C11__external_traceability",
                "record_id": "C11",
                "field": "external traceability",
                "human_final_label": "",
                "brief_reason": "",
                "evidence_location_verified": "",
                "unresolved": "",
                "reviewer_initials": "",
                "review_date": "",
                "row_status": "pending",
            },
            {
                "disagreement_id": "U09__capability",
                "record_id": "U09",
                "field": "cross-stage capability",
                "human_final_label": "",
                "brief_reason": "",
                "evidence_location_verified": "",
                "unresolved": "",
                "reviewer_initials": "",
                "review_date": "",
                "row_status": "pending",
            },
        ]
        self.key_rows = [
            {
                "r2_task_id": "R2-159",
                "internal_record_id": "C11",
                "field_key": "external_traceability",
                "row_type": "disagreement",
                "case_id": "A104",
                "hidden_reference_label": "",
            },
            {
                "r2_task_id": "R2-062",
                "internal_record_id": "U09",
                "field_key": "capability",
                "row_type": "disagreement",
                "case_id": "A139",
                "hidden_reference_label": "",
            },
            {
                "r2_task_id": "R2-004",
                "internal_record_id": "U27",
                "field_key": "capability",
                "row_type": "qc_agreement",
                "case_id": "A188",
                "hidden_reference_label": "context aggregation / rule extraction",
            },
        ]
        self.review_rows = [
            {
                "task_id": "R2-159",
                "case_id": "A104",
                "field": "external traceability",
                "final_label": "publicly aligned external trace",
                "verified_evidence_locator": "paper p.18, Sec. 5.5",
                "brief_reason": "The paper reports CNVD-2024-16009.",
                "confidence": "high",
                "unresolved": "no",
                "reviewer_initials": "OY",
                "review_date": "2026-08-24",
                "completion_check": "ready",
            },
            {
                "task_id": "R2-062",
                "case_id": "A139",
                "field": "cross-stage capability",
                "final_label": "context aggregation / rule extraction; feedback interpretation / loop adjustment",
                "verified_evidence_locator": "paper p.4, Fig. 2",
                "brief_reason": "Retrieved context changes later generation.",
                "confidence": "high",
                "unresolved": "no",
                "reviewer_initials": "OY",
                "review_date": "2026-08-24",
                "completion_check": "ready",
            },
            {
                "task_id": "R2-004",
                "case_id": "A188",
                "field": "cross-stage capability",
                "final_label": "no qualifying label observed",
                "verified_evidence_locator": "paper p.3, Fig. 2",
                "brief_reason": "No qualifying cross-stage chain was located.",
                "confidence": "medium",
                "unresolved": "no",
                "reviewer_initials": "OY",
                "review_date": "2026-08-24",
                "completion_check": "ready",
            },
        ]

    def test_disagreements_are_imported_and_qc_is_kept_separate(self) -> None:
        decisions, qc_rows = build_integration_rows(
            self.template, self.key_rows, self.review_rows
        )

        self.assertEqual(len(decisions), 2)
        self.assertEqual(len(qc_rows), 1)
        self.assertEqual(qc_rows[0]["task_id"], "R2-004")
        self.assertEqual(decisions[1]["third_party_task_id"], "R2-062")
        self.assertEqual(decisions[1]["reviewer_initials"], "OY")

    def test_cnvd_post_check_overrides_only_the_integrated_decision(self) -> None:
        decisions, _ = build_integration_rows(
            self.template, self.key_rows, self.review_rows
        )
        malf = next(row for row in decisions if row["record_id"] == "C11")

        self.assertEqual(malf["human_final_label"], "author-reported external clue")
        self.assertIn("official-record check", malf["decision_provenance"])
        self.assertIn("not publicly retrievable", malf["brief_reason"])
        self.assertEqual(
            self.review_rows[0]["final_label"], "publicly aligned external trace"
        )

    def test_case_identity_mismatch_is_rejected(self) -> None:
        self.review_rows[0]["case_id"] = "A999"
        with self.assertRaisesRegex(ValueError, "case identity mismatch"):
            build_integration_rows(self.template, self.key_rows, self.review_rows)


if __name__ == "__main__":
    unittest.main()
