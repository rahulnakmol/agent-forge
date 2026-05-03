#!/usr/bin/env python3
"""PRD Output Validator.

Validates PRD documents produced by pm-prd-generator to ensure output
quality, template compliance, and completeness before delivery to
pm-prd-reviewer or engineering teams.

Validation checks:
    1. Template compliance: All 12 required sections present
    2. User story quality: INVEST format, Given-When-Then AC
    3. Feature completeness: Star Level, business value, description
    4. Metric quality: Baselines, targets, measurement methods
    5. Scope clarity: In-scope and out-of-scope defined

Exit codes:
    0 = All validations passed
    1 = Critical failures (missing required sections)
    2 = Warnings only (quality improvements needed)

Usage:
    python validate_prd.py --input epic-prd.md
    python validate_prd.py --input epic-prd.md --report report.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class ValidationIssue:
    severity: str
    category: str
    message: str
    location: str = ""


@dataclass
class ValidationReport:
    input_file: str
    issues: list[ValidationIssue] = field(default_factory=list)
    stats: dict[str, Any] = field(default_factory=dict)

    @property
    def critical_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "critical")

    @property
    def warning_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "warning")

    @property
    def passed(self) -> bool:
        return self.critical_count == 0

    def add(self, severity: str, category: str, message: str, location: str = "") -> None:
        self.issues.append(ValidationIssue(severity, category, message, location))

    def summary(self) -> str:
        status = "PASS" if self.passed else "FAIL"
        lines = [
            f"PRD Validation {status}: {self.input_file}",
            f"  Critical: {self.critical_count}  Warnings: {self.warning_count}",
        ]
        if self.stats:
            lines.append(f"  Stats: {json.dumps(self.stats, indent=2)}")
        for issue in self.issues:
            loc = f" [{issue.location}]" if issue.location else ""
            lines.append(f"    [{issue.severity.upper()}] {issue.category}: {issue.message}{loc}")
        return "\n".join(lines)

    def to_dict(self) -> dict[str, Any]:
        return {
            "input_file": self.input_file,
            "passed": self.passed,
            "critical_count": self.critical_count,
            "warning_count": self.warning_count,
            "stats": self.stats,
            "issues": [
                {"severity": i.severity, "category": i.category, "message": i.message, "location": i.location}
                for i in self.issues
            ],
        }


# The 12 required PRD sections (from epic-prd-template.md)
REQUIRED_SECTIONS = [
    ("Problem Statement", r"problem\s+statement|business\s+context"),
    ("Stakeholders & Personas", r"stakeholder|persona"),
    ("Epic Definition", r"epic\s+definition"),
    ("User Stories", r"user\s+stor"),
    ("Key Features", r"key\s+features|business\s+value"),
    ("Success Metrics", r"success\s+metric"),
    ("Constraints & Assumptions", r"constraint|assumption"),
    ("Technical Considerations", r"technical\s+consideration"),
    ("Process Flow", r"process\s+flow"),
    ("Release & Rollout", r"release|rollout"),
    ("Open Questions", r"open\s+question"),
]


def validate_prd(file_path: Path, report: ValidationReport) -> None:
    """Validate a PRD markdown document."""
    content = file_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    if len(lines) < 30:
        report.add("critical", "structure", f"PRD too short ({len(lines)} lines, expected 100+)")
        return

    content_lower = content.lower()

    # 1. Template compliance: check required sections
    sections_found = 0
    for section_name, pattern in REQUIRED_SECTIONS:
        if re.search(pattern, content_lower):
            sections_found += 1
        else:
            report.add("critical", "template", f"Missing required section: '{section_name}'")

    # 2. Meta section
    if not re.search(r"prd.?id|document\s+id|status.*draft", content_lower):
        report.add("warning", "template", "Missing Meta section (PRD ID, Status)")

    # 3. User story quality
    stories = re.findall(r"(?:^|\n)###?\s*US-\d+", content)
    as_a_count = len(re.findall(r"As an?\s+", content, re.IGNORECASE))
    gwt_count = len(re.findall(r"\bGiven\b", content))

    if len(stories) == 0:
        # Try alternate format
        stories = re.findall(r"(?:^|\n)\*\*US-\d+", content)

    if as_a_count == 0:
        report.add("critical", "story_quality", "No user stories in 'As a [persona]...' format found")
    elif as_a_count < 3:
        report.add("warning", "story_quality", f"Only {as_a_count} user stories found (expected 3+)")

    if gwt_count == 0:
        report.add("critical", "story_quality", "No Given-When-Then acceptance criteria found")
    elif gwt_count < as_a_count:
        report.add("warning", "story_quality", f"Fewer Given-When-Then ({gwt_count}) than stories ({as_a_count})")

    # 4. Priority and complexity
    priority_count = len(re.findall(r"\b(?:MH|SH|CH|WH)\b", content))
    complexity_count = len(re.findall(r"\b(?:^|\s)(?:S|M|L|XL)\b", content))

    if priority_count == 0:
        report.add("warning", "story_quality", "No MOSCOW priority (MH/SH/CH) found in stories")
    if complexity_count == 0:
        report.add("warning", "story_quality", "No complexity sizing (S/M/L/XL) found in stories")

    # 5. Star Level in features
    star_level = re.search(r"star\s*level|star.*1.?11", content_lower)
    if not star_level:
        report.add("warning", "template", "No 'Star Level (1-11)' column found in features table")

    # 6. Success metrics quality
    if re.search(r"success\s+metric", content_lower):
        baseline = re.search(r"baseline", content_lower)
        target = re.search(r"target", content_lower)
        if not baseline:
            report.add("warning", "metrics", "Success metrics missing 'Baseline' column")
        if not target:
            report.add("warning", "metrics", "Success metrics missing 'Target' column")

    # 7. Scope clarity
    in_scope = re.search(r"in\s*scope", content_lower)
    out_scope = re.search(r"out\s*(?:of\s*)?scope", content_lower)
    if not in_scope:
        report.add("warning", "scope", "Missing 'In Scope' definition")
    if not out_scope:
        report.add("warning", "scope", "Missing 'Out of Scope' definition")

    # 8. Process flow diagram
    has_mermaid = "```mermaid" in content
    if not has_mermaid:
        report.add("warning", "template", "No Mermaid process flow diagram found")

    # 9. Risk table
    risk_table = re.search(r"risk.*likelihood|risk.*impact|risk.*mitigation", content_lower)
    if not risk_table:
        report.add("warning", "completeness", "No risk table with likelihood/impact/mitigation found")

    # Stats
    report.stats = {
        "total_lines": len(lines),
        "sections_found": sections_found,
        "sections_required": len(REQUIRED_SECTIONS),
        "user_stories": as_a_count,
        "given_when_then": gwt_count,
        "priority_mentions": priority_count,
        "has_star_levels": bool(star_level),
        "has_mermaid": has_mermaid,
        "has_scope": bool(in_scope and out_scope),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate pm-prd-generator output quality")
    parser.add_argument("--input", required=True, help="Path to PRD markdown file")
    parser.add_argument("--report", help="Optional: write JSON validation report")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: Input file not found: {input_path}")
        return 1

    report = ValidationReport(input_file=str(input_path))
    validate_prd(input_path, report)

    print(report.summary())

    if args.report:
        Path(args.report).write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")

    if report.critical_count > 0:
        return 1
    if args.strict and report.warning_count > 0:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
