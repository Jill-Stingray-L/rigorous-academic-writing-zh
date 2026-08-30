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


if __name__ == "__main__":
    unittest.main()
