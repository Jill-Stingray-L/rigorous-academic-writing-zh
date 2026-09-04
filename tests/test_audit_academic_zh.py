from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "audit_academic_zh.py"
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def audit_fixture(name: str) -> dict[str, object]:
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), str(FIXTURES / name), "--format", "json"],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return json.loads(completed.stdout)


class AuditAcademicZhRegressionTests(unittest.TestCase):
    def test_application_adjective_and_substantive_table_are_not_false_positives(self) -> None:
        payload = audit_fixture("structured_sections.md")
        codes = {finding["code"] for finding in payload["findings"]}

        self.assertNotIn("METHOD_DECLARATION_LOW_MENTION", codes)
        self.assertNotIn("THIN_SECTION", codes)

    def test_real_single_method_and_thin_section_remain_detectable(self) -> None:
        payload = audit_fixture("real_method_and_thin_section.md")
        codes = {finding["code"] for finding in payload["findings"]}

        self.assertIn("METHOD_DECLARATION_LOW_MENTION", codes)
        self.assertIn("THIN_SECTION", codes)

    def test_heading_review_candidates_are_located_without_automatic_rewrite(self) -> None:
        payload = audit_fixture("heading_candidates.md")
        codes = {finding["code"] for finding in payload["findings"]}

        self.assertIn("HEADING_COORDINATION_DENSE", codes)
        self.assertIn("HEADING_TEMPLATE_REPEAT", codes)
        self.assertIn("HEADING_NUMBER_SPACING", codes)
        self.assertIn("HEADING_STATUS_MIX", codes)
        self.assertNotIn("LONG_DE_CHAIN", codes)

    def test_concrete_parallel_headings_are_not_heading_candidates(self) -> None:
        payload = audit_fixture("heading_precise.md")
        heading_codes = {
            finding["code"]
            for finding in payload["findings"]
            if finding["code"].startswith("HEADING_")
        }

        self.assertEqual(set(), heading_codes)

    def test_plain_text_table_of_contents_is_supported(self) -> None:
        payload = audit_fixture("heading_candidates_plain.txt")
        codes = {finding["code"] for finding in payload["findings"]}

        self.assertIn("HEADING_TEMPLATE_REPEAT", codes)
        self.assertIn("HEADING_NUMBER_SPACING", codes)
        self.assertIn("HEADING_STATUS_MIX", codes)

    def test_forward_review_fixture_reuses_existing_structural_leads(self) -> None:
        payload = audit_fixture("forward_review_report.md")
        findings = payload["findings"]
        codes = {finding["code"] for finding in findings}

        self.assertIn("HEADING_TEMPLATE_REPEAT", codes)
        self.assertIn("HEADING_STATUS_MIX", codes)
        self.assertIn("THIN_SECTION", codes)
        self.assertIn("WORKLOG_FUTURE_TRACE", codes)
        self.assertFalse(
            any(
                finding["code"].startswith("HEADING_")
                and "不同开放时段下近地面空气温度的采样范围与比较边界" in finding["excerpt"]
                for finding in findings
            )
        )

    def test_worklog_theory_leak_and_section_repetition_are_review_leads(self) -> None:
        payload = audit_fixture("semantic_leads_positive.md")
        findings = payload["findings"]
        codes = {finding["code"] for finding in findings}

        self.assertIn("WORKLOG_FUTURE_TRACE", codes)
        self.assertIn("THEORY_PROJECT_LEAK", codes)
        self.assertIn("DEFENSIVE_CLARIFICATION", codes)
        self.assertIn("SECTION_DEFENSIVE_DENSITY", codes)
        self.assertIn("REPEATED_EVIDENCE_BOUNDARY", codes)
        self.assertFalse(
            any(
                finding["code"] == "DEFENSIVE_CLARIFICATION"
                and finding["line"] in {19, 21, 23, 25}
                for finding in findings
            )
        )
        self.assertTrue(
            any(
                finding["code"] == "WORKLOG_FUTURE_TRACE"
                and "分析结果" in finding["message"]
                and finding["excerpt"]
                for finding in findings
            )
        )
        self.assertTrue(
            any(
                finding["code"] == "WORKLOG_FUTURE_TRACE"
                and "取得数据后再计算关联成功率" in finding["excerpt"]
                for finding in findings
            )
        )
        self.assertTrue(
            any(
                finding["code"] == "WORKLOG_FUTURE_TRACE"
                and "下一步核对运行数据" in finding["excerpt"]
                for finding in findings
            )
        )
        self.assertFalse(
            any(
                finding["code"] == "THEORY_PROJECT_LEAK"
                and finding["line"] > 20
                for finding in findings
            )
        )

    def test_normal_transition_rules_methods_and_necessary_limits_are_not_new_leads(self) -> None:
        payload = audit_fixture("semantic_leads_negative.md")
        new_codes = {
            finding["code"]
            for finding in payload["findings"]
            if finding["code"]
            in {
                "WORKLOG_FUTURE_TRACE",
                "THEORY_PROJECT_LEAK",
                "SECTION_DEFENSIVE_DENSITY",
                "REPEATED_EVIDENCE_BOUNDARY",
            }
        }

        self.assertEqual(set(), new_codes)
        self.assertIn("人工复核线索", payload["disclaimer"])


if __name__ == "__main__":
    unittest.main()
