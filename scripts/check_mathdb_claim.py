#!/usr/bin/env python3
"""Check MathDB web-form claims without fetching links or executing issue text.

This checks required fields and category/material consistency, not authorship,
technical acceptance, qualification or the contents of linked review records.
"""

import argparse
import json
import os
from pathlib import Path
import re
from urllib.parse import urlsplit

CATEGORY_FIELDS = {
    "Solution": "Solution material links",
    "Lean": "Lean material links",
    "Exposition": "Exposition material links",
}
REQUIRED_FIELDS = (
    "JSP identifier", "Catalog link", "MathDB problem link", "Contributor",
    "Categories claimed",
)
WEB_MARKERS = ("JSP identifier", "MathDB problem link", "Categories claimed",
               *CATEGORY_FIELDS.values(), "Review record links")
EMPTY_VALUES = {"", "_no response_", "no response", "n/a", "none", "not claimed"}


def sections(body):
    """Return all level-three sections, preserving duplicates for validation."""
    body = re.sub(r"<!--.*?-->", "", body.replace("\r\n", "\n"), flags=re.S)
    pieces = re.split(r"^### ([^\n]+)(?:\n|$)", body, flags=re.M)
    result = {}
    for label, content in zip(pieces[1::2], pieces[2::2]):
        result.setdefault(label.strip(), []).append(content.strip())
    return result


def empty(value):
    return value.strip().lower() in EMPTY_VALUES


def has_link(value):
    for candidate in re.findall(r"https?://[^\s<>\[\]()]+", value):
        try:
            url = urlsplit(candidate.rstrip(".,;"))
            hostname = url.hostname or ""
            if (url.scheme in {"http", "https"} and "." in hostname
                    and all(part for part in hostname.split("."))
                    and not url.username and not url.password):
                return True
        except ValueError:
            continue
    return False


def validate_body(body):
    fields = sections(body)
    errors = []
    known_fields = (*REQUIRED_FIELDS, *CATEGORY_FIELDS.values(), "Review record links",
                    "Related claims or disputes (if any)")
    for label in known_fields:
        if len(fields.get(label, [])) > 1:
            errors.append(f"Duplicate section: {label}.")

    def value(label):
        return fields.get(label, [""])[0]

    for label in REQUIRED_FIELDS:
        if empty(value(label)):
            errors.append(f"Missing required field: {label}.")

    jsp = value("JSP identifier")
    if not empty(jsp) and not re.fullmatch(r"JSP-\d{6}", jsp):
        errors.append("JSP identifier must use the format JSP-000001.")
    for label in ("Catalog link", "MathDB problem link", "Review record links"):
        if not empty(value(label)) and not has_link(value(label)):
            errors.append(f"Provide a valid HTTP(S) link in {label}.")

    selected = []
    if not empty(value("Categories claimed")):
        selected = [part.strip() for part in value("Categories claimed").split(",")]
        if any(category not in CATEGORY_FIELDS for category in selected):
            errors.append("Categories claimed must contain only Solution, Lean or Exposition.")
        if len(set(selected)) != len(selected):
            errors.append("Do not repeat categories in Categories claimed.")

    for category, label in CATEGORY_FIELDS.items():
        material = value(label)
        if category in selected:
            if empty(material) or not has_link(material):
                errors.append(f"{category} is selected: provide a material link in {label}.")
            if category == "Lean" and not re.search(r"\b[0-9a-fA-F]{40}\b", material):
                errors.append("Lean is selected: provide the full commit SHA.")
        elif not empty(material):
            errors.append(f"{label} has content: select {category} or clear this field.")
    return errors


def check_event(event):
    issue = event.get("issue", {})
    body = issue.get("body") or ""
    # API handoffs and legacy claims use different bodies and remain outside this
    # web-form check. Recognize web-form fields even if the title has been edited.
    fields = sections(body)
    if any(marker in fields for marker in WEB_MARKERS):
        return validate_body(body)
    if issue.get("title", "").startswith("[Claim Reward]"):
        if not re.search(r"^## Handoff and actual claimant\s*$", body, flags=re.M):
            return validate_body(body)
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--event", required=True, type=Path,
                        help="GitHub Actions event JSON file")
    args = parser.parse_args()
    errors = check_event(json.loads(args.event.read_text()))
    if errors is None:
        message = "Skipped: this issue is not a MathDB web-form claim."
    elif errors:
        # Diagnostics contain only fixed labels, never untrusted issue contents.
        message = "MathDB claim check failed:\n" + "\n".join(f"- {error}" for error in errors)
    else:
        message = ("MathDB claim completeness check passed. Linked material and review "
                   "contents still require team review.")
    print(message)
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with Path(summary_path).open("a") as summary:
            summary.write(message + "\n")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
