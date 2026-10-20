"""Exercise category/link consistency using GitHub Issue Form body formatting."""

import importlib.util
from itertools import combinations
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/check_mathdb_claim.py"
SPEC = importlib.util.spec_from_file_location("check_mathdb_claim", SCRIPT)
claim = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(claim)


class MathDBClaimTests(unittest.TestCase):
    def body(self, selected=("Solution",), overrides=None):
        fields = {
            "JSP identifier": "JSP-000001",
            "Catalog link": "https://github.com/TheJustinSunPrize/awards/blob/main/"
                            "problems/catalog-0001-0100.md#JSP-000001",
            "MathDB problem link": "https://mathdb.com/p/315854/riemann-hypothesis",
            "Contributor": "Alice; MathDB user 123; solution author",
            "Categories claimed": ", ".join(selected),
            "Solution material links": "_No response_",
            "Lean material links": "_No response_",
            "Exposition material links": "_No response_",
            "Review record links": "[Shared review](https://mathdb.com/reviews/123)",
            "Related claims or disputes (if any)": "_No response_",
        }
        for category in selected:
            if category in claim.CATEGORY_FIELDS:
                fields[claim.CATEGORY_FIELDS[category]] = "https://example.org/material"
        fields.update(overrides or {})
        return "\n\n".join(f"### {label}\n\n{value}" for label, value in fields.items())

    def test_all_seven_category_combinations(self):
        for count in (1, 2, 3):
            for selected in combinations(claim.CATEGORY_FIELDS, count):
                with self.subTest(selected=selected):
                    self.assertEqual(claim.validate_body(self.body(selected)), [])

    def test_selected_material_is_required_even_when_other_material_is_present(self):
        for category, label in claim.CATEGORY_FIELDS.items():
            for missing in ("", "_No response_", "N/A", "None", "See the proof", "https://..."):
                with self.subTest(category=category, missing=missing):
                    errors = claim.validate_body(self.body(
                        tuple(claim.CATEGORY_FIELDS), {label: missing}))
                    self.assertTrue(any(f"{category} is selected" in error for error in errors))

    def test_unselected_material_must_be_added_to_selection_or_cleared(self):
        errors = claim.validate_body(self.body(overrides={
            "Lean material links": "https://github.com/author/proof"}))
        self.assertTrue(any("select Lean or clear this field" in error for error in errors))

    def test_empty_unknown_and_repeated_categories_fail(self):
        for selected in ((), ("Both",), ("Solution", "Solution")):
            with self.subTest(selected=selected):
                self.assertTrue(claim.validate_body(self.body(selected)))

    def test_required_fields_cannot_be_removed_on_edit(self):
        for label in claim.REQUIRED_FIELDS:
            with self.subTest(label=label):
                body = self.body(overrides={label: ""})
                self.assertIn(f"Missing required field: {label}.", claim.validate_body(body))
        body = self.body().replace("### Review record links", "### Deleted review heading")
        self.assertIn("Missing required field: Review record links.", claim.validate_body(body))

    def test_review_requires_a_link_and_shared_review_only_needs_one(self):
        self.assertEqual(claim.validate_body(self.body(tuple(claim.CATEGORY_FIELDS))), [])
        errors = claim.validate_body(self.body(overrides={"Review record links": "Passed"}))
        self.assertIn("Provide a valid HTTP(S) link in Review record links.", errors)

    def test_duplicate_sections_are_rejected(self):
        body = self.body() + "\n\n### Solution material links\n\nhttps://example.org/other"
        self.assertIn("Duplicate section: Solution material links.", claim.validate_body(body))

    def test_crlf_and_empty_final_heading(self):
        self.assertEqual(claim.validate_body(self.body().replace("\n", "\r\n")), [])
        body = self.body() + "\n\n### Exposition material links"
        self.assertIn("Duplicate section: Exposition material links.", claim.validate_body(body))

    def test_html_comments_do_not_supply_missing_links(self):
        body = self.body(overrides={"Solution material links": "<!-- https://example.org -->"})
        self.assertTrue(claim.validate_body(body))

    def test_edited_title_does_not_bypass_web_form_check(self):
        event = {"issue": {"title": "Renamed issue", "body": self.body(overrides={
            "Solution material links": "_No response_"})}}
        self.assertTrue(claim.check_event(event))

    def test_legacy_api_and_unrelated_bodies_are_outside_web_form_scope(self):
        api_body = (ROOT / "docs/templates/mathdb-claim-reward.md").read_text()
        for body in (None, "A regular issue", api_body):
            with self.subTest(body=body):
                self.assertIsNone(claim.check_event({"issue": {"body": body}}))
        self.assertIsNone(claim.check_event({"issue": {
            "title": "[Claim Reward] JSP-000001 — Alice", "body": api_body}}))

    def test_removing_entire_claim_body_does_not_pass(self):
        for body in (None, "", "Please award my proof"):
            with self.subTest(body=body):
                self.assertTrue(claim.check_event({"issue": {
                    "title": "[Claim Reward] JSP-000001 — Alice", "body": body}}))

    def test_jsp_format_and_link_syntax(self):
        self.assertTrue(claim.validate_body(self.body(overrides={"JSP identifier": "JSP-XXXXXX"})))
        for candidate in ("javascript:alert(1)", "https://...", "http://[broken", "No URL"):
            with self.subTest(candidate=candidate):
                self.assertFalse(claim.has_link(candidate))

    def test_cli_exit_status_and_summary(self):
        with tempfile.TemporaryDirectory() as directory:
            event_path = Path(directory) / "event.json"
            summary_path = Path(directory) / "summary.md"
            env = dict(os.environ, GITHUB_STEP_SUMMARY=str(summary_path))
            for expected, overrides in ((0, {}), (1, {"Solution material links": ""})):
                with self.subTest(expected=expected):
                    event_path.write_text(json.dumps({"issue": {"body": self.body(overrides=overrides)}}))
                    result = subprocess.run([sys.executable, str(SCRIPT), "--event", str(event_path)],
                                            env=env, capture_output=True, text=True)
                    self.assertEqual(result.returncode, expected, result.stderr)
                    self.assertIn("MathDB claim", summary_path.read_text())


if __name__ == "__main__":
    unittest.main()
