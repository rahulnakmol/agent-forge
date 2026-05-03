#!/usr/bin/env python3
"""
KPMG Skills Test Harness

Comprehensive validation suite for the refactored KPMG skills plugin.
Validates structural integrity, content quality, Unix philosophy compliance,
cross-reference consistency, brand consistency, pipeline integration,
and collateral workflow completeness.

Usage:
    python3 test_harness.py [--verbose] [--report report.json] [--category CATEGORY]

Categories: structural, unix, brand, crossref, content, collateral, pipeline, regression, all (default)

NOT committed to repository — local development/validation tool only.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path


# ─── Configuration ───────────────────────────────────────────────────────────

PLUGIN_DIR = Path(__file__).parent
SKILLS_DIR = PLUGIN_DIR / "skills"
REPO_ROOT = PLUGIN_DIR.parent.parent

EXPECTED_SKILLS = [
    "brand-identity",
    "brand-voice",
    "external-comms",
    "internal-comms",
    "collateral-workflow",
    "metrics",
    "presentation",
    "presentation-planner",
]

# Brand constants that must be consistent across skills
KPMG_BLUE = "#00338D"
COBALT_BLUE = "#1E49E2"
PURPLE = "#7213EA"
PINK = "#FD349C"
DARK_BLUE = "#0C233C"

BRAND_COLOURS = {
    "KPMG Blue": KPMG_BLUE,
    "Cobalt Blue": COBALT_BLUE,
    "Purple": PURPLE,
    "Pink": PINK,
    "Dark Blue": DARK_BLUE,
}

BRAND_FONTS = ["KPMG Bold", "Arial", "Open Sans", "Univers"]

# Skill-specific trigger keywords (must NOT overlap)
SKILL_TRIGGER_DOMAINS = {
    "brand-identity": ["visual identity", "colours", "typography", "Window motif", "imagery", "gradients"],
    "brand-voice": ["voice principles", "insight framework", "writing excellence", "tone calibration"],
    "external-comms": ["external audience", "client-facing", "thought leadership", "press release", "social media"],
    "internal-comms": ["internal audience", "status report", "3P update", "executive briefing", "incident report"],
    "collateral-workflow": ["collateral creation", "DELIVER IT", "orchestrat"],
    "metrics": ["measuring effectiveness", "KPI", "benchmark", "measurement framework"],
    "presentation": ["KPMG presentation", "advisory slides", "template layout", "build PPTX"],
    "presentation-planner": ["all-visuals", "slide selector", "content blueprint", "slide recommendation"],
}

SKILL_LINE_LIMIT_SOFT = 300
SKILL_LINE_LIMIT_HARD = 400


# ─── Test Infrastructure ─────────────────────────────────────────────────────

class TestResult:
    def __init__(self, category, test_name, passed, message=None, severity="FAIL"):
        self.category = category
        self.test_name = test_name
        self.passed = passed
        self.message = message
        self.severity = severity  # FAIL or WARN

    def __str__(self):
        status = "PASS" if self.passed else self.severity
        msg = f"  {status}: [{self.category}] {self.test_name}"
        if self.message and not self.passed:
            msg += f" — {self.message}"
        return msg

    def to_dict(self):
        return {
            "category": self.category,
            "test_name": self.test_name,
            "passed": self.passed,
            "message": self.message,
            "severity": self.severity,
        }


class TestHarness:
    def __init__(self, verbose=False):
        self.results = []
        self.verbose = verbose

    def check(self, category, test_name, passed, message=None, severity="FAIL"):
        result = TestResult(category, test_name, passed, message, severity)
        self.results.append(result)
        if self.verbose or not passed:
            print(result)
        return passed

    def run_category(self, category):
        method = getattr(self, f"test_{category}", None)
        if method:
            print(f"\n{'='*60}")
            print(f"  {category.upper()} TESTS")
            print(f"{'='*60}")
            method()
        else:
            print(f"Unknown category: {category}")

    def run_all(self):
        categories = [
            "structural",
            "unix",
            "brand",
            "crossref",
            "content",
            "collateral",
            "pipeline",
            "regression",
        ]
        for cat in categories:
            self.run_category(cat)

    def summary(self):
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        failed = sum(1 for r in self.results if not r.passed and r.severity == "FAIL")
        warned = sum(1 for r in self.results if not r.passed and r.severity == "WARN")

        by_category = defaultdict(lambda: {"total": 0, "passed": 0, "failed": 0, "warned": 0})
        for r in self.results:
            cat = by_category[r.category]
            cat["total"] += 1
            if r.passed:
                cat["passed"] += 1
            elif r.severity == "FAIL":
                cat["failed"] += 1
            else:
                cat["warned"] += 1

        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "warned": warned,
            "pass_rate": round(passed / max(total, 1) * 100, 1),
            "by_category": dict(by_category),
            "results": [r.to_dict() for r in self.results],
        }

    # ─── Utility Methods ─────────────────────────────────────────────────

    def _read_skill_md(self, skill_name):
        """Read and return SKILL.md content for a skill."""
        path = SKILLS_DIR / skill_name / "SKILL.md"
        if path.exists():
            return path.read_text()
        return None

    def _parse_frontmatter(self, content):
        """Extract YAML frontmatter from SKILL.md."""
        if not content or not content.startswith("---"):
            return {}
        parts = content.split("---", 2)
        if len(parts) < 3:
            return {}
        fm_text = parts[1].strip()
        result = {}
        for line in fm_text.split("\n"):
            if ":" in line and not line.startswith(" ") and not line.startswith("-"):
                key, val = line.split(":", 1)
                result[key.strip()] = val.strip()
        return result

    def _count_lines(self, content):
        """Count non-empty lines in content."""
        return len(content.strip().split("\n"))

    def _find_sections(self, content, level="##"):
        """Find all section headings at a given level."""
        pattern = rf"^{re.escape(level)}\s+(.+)$"
        return re.findall(pattern, content, re.MULTILINE)

    # ─── 1. Structural Integrity Tests ───────────────────────────────────

    def test_structural(self):
        """Every skill has SKILL.md with valid frontmatter, LICENSE.txt, correct structure."""

        for skill in EXPECTED_SKILLS:
            skill_dir = SKILLS_DIR / skill

            # Skill directory exists
            self.check("structural", f"{skill}: directory exists",
                        skill_dir.is_dir(),
                        f"Missing directory: {skill_dir}")

            if not skill_dir.is_dir():
                continue

            # SKILL.md exists
            skill_md = skill_dir / "SKILL.md"
            self.check("structural", f"{skill}: SKILL.md exists",
                        skill_md.exists(),
                        "Missing SKILL.md")

            if not skill_md.exists():
                continue

            content = skill_md.read_text()

            # Frontmatter present
            self.check("structural", f"{skill}: has YAML frontmatter",
                        content.startswith("---"),
                        "SKILL.md must start with ---")

            # Required frontmatter fields
            fm = self._parse_frontmatter(content)
            for field in ["name", "description", "version", "license"]:
                self.check("structural", f"{skill}: frontmatter has '{field}'",
                            field in fm or any(field in line for line in content.split("\n")[:20]),
                            f"Missing frontmatter field: {field}")

            # allowed-tools present
            self.check("structural", f"{skill}: has allowed-tools",
                        "allowed-tools:" in content[:2000],
                        "Missing allowed-tools in frontmatter")

            # Line count within budget
            line_count = self._count_lines(content)
            self.check("structural", f"{skill}: line count ({line_count}) within soft limit",
                        line_count <= SKILL_LINE_LIMIT_SOFT,
                        f"Over {SKILL_LINE_LIMIT_SOFT} line soft limit",
                        severity="WARN")
            self.check("structural", f"{skill}: line count ({line_count}) within hard limit",
                        line_count <= SKILL_LINE_LIMIT_HARD,
                        f"Over {SKILL_LINE_LIMIT_HARD} line hard limit")

            # LICENSE.txt exists
            self.check("structural", f"{skill}: LICENSE.txt exists",
                        (skill_dir / "LICENSE.txt").exists(),
                        "Missing LICENSE.txt")

            # .skillrc exists (expected for all skills)
            self.check("structural", f"{skill}: .skillrc exists",
                        (skill_dir / ".skillrc").exists(),
                        "Missing .skillrc metadata file",
                        severity="WARN")

        # Agent exists
        agent_path = PLUGIN_DIR / "agents" / "agent.md"
        self.check("structural", "agents/agent.md exists",
                    agent_path.exists(),
                    "Missing agent orchestrator")

        # Command exists
        cmd_path = PLUGIN_DIR / "commands" / "agent.md"
        self.check("structural", "commands/agent.md exists",
                    cmd_path.exists(),
                    "Missing agent command shortcut")

        # Plugin.json exists and is valid JSON
        plugin_json = PLUGIN_DIR / ".claude-plugin" / "plugin.json"
        self.check("structural", "plugin.json exists",
                    plugin_json.exists(),
                    "Missing plugin.json")

        if plugin_json.exists():
            try:
                data = json.loads(plugin_json.read_text())
                self.check("structural", "plugin.json is valid JSON", True)
                self.check("structural", "plugin.json has name",
                            "name" in data, "Missing 'name' field")
                self.check("structural", "plugin.json has version",
                            "version" in data, "Missing 'version' field")
            except json.JSONDecodeError as e:
                self.check("structural", "plugin.json is valid JSON",
                            False, str(e))

    # ─── 2. Unix Philosophy Compliance Tests ─────────────────────────────

    def test_unix(self):
        """Single responsibility, progressive disclosure, no content duplication."""

        # Single responsibility: check trigger keyword overlap
        all_triggers = {}
        for skill, keywords in SKILL_TRIGGER_DOMAINS.items():
            content = self._read_skill_md(skill)
            if not content:
                continue
            desc_section = content[:1500]  # frontmatter + first section
            for kw in keywords:
                if kw.lower() in desc_section.lower():
                    all_triggers.setdefault(kw, []).append(skill)

        for kw, skills in all_triggers.items():
            self.check("unix", f"trigger keyword '{kw}' owned by single skill",
                        len(skills) == 1,
                        f"Shared by: {', '.join(skills)}",
                        severity="WARN")

        # Progressive disclosure: SKILL.md compact, detail in references
        for skill in EXPECTED_SKILLS:
            content = self._read_skill_md(skill)
            if not content:
                continue
            line_count = self._count_lines(content)
            ref_dir = SKILLS_DIR / skill / "references"
            has_refs = ref_dir.is_dir() and any(ref_dir.iterdir()) if ref_dir.exists() else False

            if line_count > 250 and not has_refs:
                self.check("unix", f"{skill}: progressive disclosure (long SKILL.md has references)",
                            False,
                            f"SKILL.md is {line_count} lines but has no references/ directory",
                            severity="WARN")
            else:
                self.check("unix", f"{skill}: progressive disclosure",
                            True)

        # No content duplication: colour tables should only be in brand-identity
        colour_table_skills = []
        for skill in EXPECTED_SKILLS:
            content = self._read_skill_md(skill)
            if not content:
                continue
            # Check for full colour table (has HEX column header with colour rows)
            if "| HEX |" in content and ("| RGB |" in content or "| Usage |" in content):
                colour_table_skills.append(skill)

        self.check("unix", "colour tables in single skill only",
                    colour_table_skills == ["brand-identity"],
                    f"Found in: {', '.join(colour_table_skills)}" if colour_table_skills != ["brand-identity"] else None)

        # Voice principles should only be detailed in brand-voice
        voice_detail_skills = []
        for skill in EXPECTED_SKILLS:
            content = self._read_skill_md(skill)
            if not content:
                continue
            if "### Smart\n" in content and "### Clear\n" in content and "### Confident\n" in content:
                voice_detail_skills.append(skill)

        self.check("unix", "voice principles detailed in single skill only",
                    voice_detail_skills == ["brand-voice"],
                    f"Found in: {', '.join(voice_detail_skills)}" if voice_detail_skills != ["brand-voice"] else None)

    # ─── 3. Brand Consistency Tests ──────────────────────────────────────

    def test_brand(self):
        """Brand values consistent across all skills that reference them."""

        # KPMG Blue hex value consistent
        for skill in EXPECTED_SKILLS:
            content = self._read_skill_md(skill)
            if not content:
                continue
            if KPMG_BLUE in content:
                # Check it's not a different value claiming to be KPMG Blue
                self.check("brand", f"{skill}: KPMG Blue is {KPMG_BLUE}",
                            True)
                # Check for competing incorrect values
                wrong_blues = re.findall(r"KPMG Blue.*?(#[0-9A-Fa-f]{6})", content)
                for wb in wrong_blues:
                    if wb.upper() != KPMG_BLUE:
                        self.check("brand", f"{skill}: no conflicting KPMG Blue values",
                                    False, f"Found {wb} claimed as KPMG Blue")

        # Sentence case mandate present in relevant skills
        for skill in ["brand-identity", "brand-voice", "presentation"]:
            content = self._read_skill_md(skill)
            if not content:
                continue
            self.check("brand", f"{skill}: sentence case mandate present",
                        "sentence case" in content.lower() or "Sentence case" in content,
                        "Missing sentence case typography rule")

        # Left-alignment rule in visual-related skills
        for skill in ["brand-identity", "presentation"]:
            content = self._read_skill_md(skill)
            if not content:
                continue
            self.check("brand", f"{skill}: left-alignment rule present",
                        "left-aligned" in content.lower() or "Left-aligned" in content,
                        "Missing left-alignment typography rule")

        # 2-3% accent limit referenced where relevant
        for skill in ["brand-identity"]:
            content = self._read_skill_md(skill)
            if not content:
                continue
            self.check("brand", f"{skill}: accent colour proportion limit referenced",
                        "2-3%" in content,
                        "Missing 2-3% accent colour proportion rule")

        # Font consistency: brand-identity must reference all platform fonts
        bi_content = self._read_skill_md("brand-identity")
        if bi_content:
            for font in BRAND_FONTS:
                self.check("brand", f"brand-identity: references font '{font}'",
                            font in bi_content,
                            f"Missing font reference: {font}")

    # ─── 4. Cross-Reference Validation Tests ─────────────────────────────

    def test_crossref(self):
        """All referenced files exist, skill references are valid."""

        for skill in EXPECTED_SKILLS:
            content = self._read_skill_md(skill)
            if not content:
                continue

            # Check references/*.md files mentioned in SKILL.md exist
            ref_mentions = re.findall(r'`references/([^`]+\.md)`', content)
            ref_dir = SKILLS_DIR / skill / "references"
            for ref_file in ref_mentions:
                ref_path = ref_dir / ref_file
                self.check("crossref", f"{skill}: referenced file exists: references/{ref_file}",
                            ref_path.exists(),
                            f"Missing file: {ref_path}")

            # Check skill references in allowed-tools exist
            allowed_tools_match = re.search(r'allowed-tools:\s*\n((?:\s+-\s+.+\n)*)', content)
            if allowed_tools_match:
                tools_text = allowed_tools_match.group(1)
                skill_refs = re.findall(r'-\s+(\S+)', tools_text)
                builtin_tools = {"Read", "Write", "Edit", "Bash", "Grep", "Glob", "AskUserQuestion"}
                for ref in skill_refs:
                    if ref not in builtin_tools and ref != "humanize":
                        ref_skill_dir = SKILLS_DIR / ref
                        self.check("crossref", f"{skill}: allowed-tool skill '{ref}' exists",
                                    ref_skill_dir.is_dir(),
                                    f"Skill directory missing: {ref_skill_dir}")

        # Check font assets exist in brand-identity
        font_dir = SKILLS_DIR / "brand-identity" / "assets" / "fonts"
        self.check("crossref", "brand-identity: font assets directory exists",
                    font_dir.is_dir(),
                    f"Missing: {font_dir}")

        if font_dir.is_dir():
            font_count = len(list(font_dir.glob("*.ttf")) + list(font_dir.glob("*.otf")))
            self.check("crossref", f"brand-identity: has font files ({font_count})",
                        font_count >= 15,
                        f"Only {font_count} fonts found (expected 15+)")

        # Check critical fonts
        for font_name in ["KPMG-Bold.ttf", "KPMG-Bold_Italic.ttf", "UniversforKPMG-Bold.ttf"]:
            self.check("crossref", f"brand-identity: critical font '{font_name}' exists",
                        (font_dir / font_name).exists() if font_dir.is_dir() else False,
                        f"Missing: {font_name}")

        # Check plugin.json exists and references correct plugin name
        plugin_json_path = PLUGIN_DIR / ".claude-plugin" / "plugin.json"
        if plugin_json_path.exists():
            data = json.loads(plugin_json_path.read_text())
            self.check("crossref", "plugin.json name is 'kpmg'",
                        data.get("name") == "kpmg",
                        f"Expected 'kpmg', got '{data.get('name')}'")

    # ─── 5. Content Quality Tests ────────────────────────────────────────

    def test_content(self):
        """Key content present in correct skills."""

        # brand-identity must have colour system
        bi = self._read_skill_md("brand-identity")
        if bi:
            for colour_name, hex_val in BRAND_COLOURS.items():
                self.check("content", f"brand-identity: has {colour_name} ({hex_val})",
                            hex_val in bi,
                            f"Missing colour: {colour_name} {hex_val}")

            self.check("content", "brand-identity: has Window motif section",
                        "Window" in bi and "7:10" in bi,
                        "Missing Window motif specifications")

            self.check("content", "brand-identity: has typography hierarchy",
                        "Typography Hierarchy" in bi or "typography hierarchy" in bi.lower(),
                        "Missing typography hierarchy")

            self.check("content", "brand-identity: has platform application guidance",
                        "Platform Application" in bi or "platform" in bi.lower(),
                        "Missing platform application guidance")

        # brand-voice must have voice principles and insight framework
        bv = self._read_skill_md("brand-voice")
        if bv:
            self.check("content", "brand-voice: has 'From insights to opportunities'",
                        "From insights to opportunities" in bv,
                        "Missing brand positioning")

            for principle in ["Smart", "Clear", "Confident"]:
                self.check("content", f"brand-voice: has '{principle}' voice principle",
                            f"### {principle}" in bv,
                            f"Missing voice principle: {principle}")

            self.check("content", "brand-voice: has insight framework",
                        "Insight Framework" in bv or "Insight Quality Criteria" in bv,
                        "Missing insight framework")

            self.check("content", "brand-voice: has writing excellence principles",
                        "Writing Excellence" in bv,
                        "Missing writing excellence principles")

            self.check("content", "brand-voice: has AI tells avoidance",
                        "delve into" in bv or "AI Tells" in bv,
                        "Missing AI tells avoidance list")

        # external-comms must have compliance section
        ec = self._read_skill_md("external-comms")
        if ec:
            self.check("content", "external-comms: has compliance section",
                        "Marketing Compliance" in ec or "Compliance" in ec,
                        "Missing compliance section")

            self.check("content", "external-comms: has social media section",
                        "Social Media" in ec or "social media" in ec,
                        "Missing social media section")

            self.check("content", "external-comms: references brand-voice",
                        "brand-voice" in ec,
                        "Should reference brand-voice for voice principles")

        # internal-comms must have format templates
        ic = self._read_skill_md("internal-comms")
        if ic:
            for fmt in ["Status Report", "Executive Briefing", "3P Update", "Incident Report", "Change Management"]:
                self.check("content", f"internal-comms: has format template '{fmt}'",
                            fmt in ic or fmt.lower() in ic.lower(),
                            f"Missing format template: {fmt}")

        # metrics must have channel-specific benchmarks
        met = self._read_skill_md("metrics")
        if met:
            for channel in ["Thought Leadership", "Press Release", "Social Media", "Internal"]:
                self.check("content", f"metrics: has '{channel}' metrics",
                            channel in met,
                            f"Missing channel: {channel}")

        # presentation must have 5 phases
        pres = self._read_skill_md("presentation")
        if pres:
            for phase in ["Gather", "Plan", "Write", "Build", "Validate"]:
                self.check("content", f"presentation: has Phase '{phase}'",
                            phase in pres,
                            f"Missing phase: {phase}")

        # presentation-planner must have core elements
        pp = self._read_skill_md("presentation-planner")
        if pp:
            self.check("content", "presentation-planner: references all-visuals",
                        "all-visuals" in pp.lower() or "all visuals" in pp.lower(),
                        "Must reference the all-visuals catalog")
            self.check("content", "presentation-planner: has blueprint output format",
                        "blueprint" in pp.lower(),
                        "Must describe blueprint output format")
            self.check("content", "presentation-planner: has speaker notes",
                        "speaker notes" in pp.lower() or "Speaker notes" in pp,
                        "Must include speaker notes requirement")

    # ─── 6. Collateral Workflow Completeness Tests ───────────────────────

    def test_collateral(self):
        """Collateral workflow has all 10 steps, correct skill references, checklists."""

        cw = self._read_skill_md("collateral-workflow")
        if not cw:
            self.check("collateral", "collateral-workflow: SKILL.md exists",
                        False, "Cannot read SKILL.md")
            return

        # All 10 steps present
        steps = [
            ("Step 1", "Analyse and clarify"),
            ("Step 2", "Read skills"),
            ("Step 3", "Propose approaches"),
            ("Step 4", "Develop core insight"),
            ("Step 5", "Structure content"),
            ("Step 6", "Draft content"),
            ("Step 7", "Refine voice"),
            ("Step 8", "DELIVER IT"),
            ("Step 9", "Generate and verify"),
            ("Step 10", "Present and flag"),
        ]
        for step_num, step_desc in steps:
            self.check("collateral", f"has {step_num}: {step_desc}",
                        step_num in cw,
                        f"Missing {step_num}")

        # "DELIVER IT" trigger gate present
        self.check("collateral", "DELIVER IT trigger gate present",
                    "DELIVER IT" in cw,
                    "Missing DELIVER IT trigger mechanism")

        # Skill routing table references valid skills
        for skill in ["brand-identity", "brand-voice", "external-comms", "internal-comms", "presentation"]:
            self.check("collateral", f"references skill: {skill}",
                        skill in cw,
                        f"Missing skill reference: {skill}")

        # Insight criteria referenced
        self.check("collateral", "references insight criteria",
                    "five criteria" in cw.lower() or "5 criteria" in cw.lower() or "insight" in cw.lower(),
                    "Missing insight criteria reference")

        # Quality checklists referenced
        self.check("collateral", "references quality checklists",
                    "quality-checklists.md" in cw or "checklist" in cw.lower(),
                    "Missing quality checklists reference")

        # Reference files exist
        ref_dir = SKILLS_DIR / "collateral-workflow" / "references"
        for ref_file in ["insight-criteria.md", "quality-checklists.md"]:
            path = ref_dir / ref_file
            self.check("collateral", f"reference file exists: {ref_file}",
                        path.exists(),
                        f"Missing: {path}")
            if path.exists():
                content = path.read_text()
                self.check("collateral", f"{ref_file} is non-trivial",
                            len(content) > 500,
                            f"File too short ({len(content)} chars)")

    # ─── 7. Pipeline Integration Tests ───────────────────────────────────

    def test_pipeline(self):
        """Skills compose correctly, agent routes to all skills."""

        # collateral-workflow can invoke all referenced skills
        cw = self._read_skill_md("collateral-workflow")
        if cw:
            for skill in ["brand-identity", "brand-voice", "external-comms", "internal-comms", "presentation", "metrics"]:
                self.check("pipeline", f"collateral-workflow: allowed-tool includes '{skill}'",
                            skill in cw[:1500],  # In frontmatter
                            f"Missing from allowed-tools: {skill}")

        # presentation references brand-identity and brand-voice (not old brand-guidelines)
        pres = self._read_skill_md("presentation")
        if pres:
            self.check("pipeline", "presentation: references brand-identity",
                        "brand-identity" in pres[:1500],
                        "Should reference brand-identity, not brand-guidelines")

            self.check("pipeline", "presentation: references brand-voice",
                        "brand-voice" in pres[:1500],
                        "Should reference brand-voice, not brand-guidelines")

            self.check("pipeline", "presentation: does NOT reference old brand-guidelines",
                        "brand-guidelines" not in pres[:1500],
                        "Still referencing deprecated brand-guidelines skill")

        # Agent routes to all skills
        agent_path = PLUGIN_DIR / "agents" / "agent.md"
        if agent_path.exists():
            agent_content = agent_path.read_text()
            for skill in EXPECTED_SKILLS:
                self.check("pipeline", f"agent: routes to '{skill}'",
                            skill in agent_content,
                            f"Agent doesn't reference skill: {skill}")

            # Agent has routing logic
            self.check("pipeline", "agent: has routing logic",
                        "Route" in agent_content or "route" in agent_content,
                        "Missing routing logic")

            # Agent has audience detection
            self.check("pipeline", "agent: has audience detection",
                        "internal" in agent_content.lower() and "external" in agent_content.lower(),
                        "Missing audience detection signals")

        # external-comms and internal-comms reference brand-identity and brand-voice
        for skill in ["external-comms", "internal-comms"]:
            content = self._read_skill_md(skill)
            if content:
                self.check("pipeline", f"{skill}: references brand-identity",
                            "brand-identity" in content[:1500],
                            "Should reference brand-identity as dependency")
                self.check("pipeline", f"{skill}: references brand-voice",
                            "brand-voice" in content[:1500],
                            "Should reference brand-voice as dependency")

    # ─── 8. Regression Tests ─────────────────────────────────────────────

    def test_regression(self):
        """Old brand-guidelines removed, existing tests functional, no orphans."""

        # Old brand-guidelines directory should not exist
        old_dir = SKILLS_DIR / "brand-guidelines"
        self.check("regression", "old brand-guidelines directory removed",
                    not old_dir.exists(),
                    f"Still exists: {old_dir}")

        # Presentation scripts still exist
        scripts_dir = SKILLS_DIR / "presentation" / "scripts"
        for script in ["brand.py", "build_presentation.py", "test_brand_compliance.py"]:
            self.check("regression", f"presentation script exists: {script}",
                        (scripts_dir / script).exists(),
                        f"Missing: {script}")

        # Presentation assets still exist
        assets_dir = SKILLS_DIR / "presentation" / "assets"
        self.check("regression", "presentation advisory-template.pptx exists",
                    (assets_dir / "advisory-template.pptx").exists(),
                    "Missing advisory template")

        self.check("regression", "presentation all-visuals.pptx exists",
                    (assets_dir / "all-visuals.pptx").exists(),
                    "Missing visual catalog")

        # Presentation references still exist
        ref_dir = SKILLS_DIR / "presentation" / "references"
        for ref in ["visual-catalog.md", "slide-matching-guide.md", "brand-specs.md", "st-voice-for-slides.md"]:
            self.check("regression", f"presentation reference exists: {ref}",
                        (ref_dir / ref).exists(),
                        f"Missing: {ref}")

        # No orphaned skill directories (unexpected directories in skills/)
        expected_set = set(EXPECTED_SKILLS)
        actual_dirs = {d.name for d in SKILLS_DIR.iterdir() if d.is_dir()}
        orphans = actual_dirs - expected_set
        self.check("regression", "no orphaned skill directories",
                    len(orphans) == 0,
                    f"Unexpected directories: {', '.join(orphans)}" if orphans else None,
                    severity="WARN")

        # Validate skill.sh exists and is executable-ready
        validate_sh = SKILLS_DIR / "brand-identity" / "scripts" / "validate_skill.sh"
        self.check("regression", "brand-identity validate_skill.sh exists",
                    validate_sh.exists(),
                    "Missing validation script")

        # marketplace.json references kpmg plugin
        marketplace_path = REPO_ROOT / ".claude-plugin" / "marketplace.json"
        if marketplace_path.exists():
            try:
                data = json.loads(marketplace_path.read_text())
                plugins = data.get("plugins", [])
                kpmg_entries = [p for p in plugins if p.get("name") == "kpmg"]
                self.check("regression", "marketplace.json has kpmg plugin entry",
                            len(kpmg_entries) > 0,
                            "Missing kpmg plugin in marketplace.json")
            except (json.JSONDecodeError, KeyError):
                self.check("regression", "marketplace.json is valid",
                            False, "JSON parse error")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="KPMG Skills Test Harness")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Show all test results (not just failures)")
    parser.add_argument("--report", help="Output JSON report path")
    parser.add_argument("--category", "-c", default="all",
                        help="Test category to run (structural, unix, brand, crossref, content, collateral, pipeline, regression, all)")
    args = parser.parse_args()

    harness = TestHarness(verbose=args.verbose)

    print("=" * 60)
    print("  KPMG SKILLS TEST HARNESS")
    print("  Validating refactored KPMG skills plugin")
    print("=" * 60)

    if args.category == "all":
        harness.run_all()
    else:
        for cat in args.category.split(","):
            harness.run_category(cat.strip())

    summary = harness.summary()

    print("\n" + "=" * 60)
    print("  SUMMARY")
    print("=" * 60)
    print(f"  Total checks:  {summary['total']}")
    print(f"  Passed:        {summary['passed']}")
    print(f"  Failed:        {summary['failed']}")
    print(f"  Warnings:      {summary['warned']}")
    print(f"  Pass rate:     {summary['pass_rate']}%")

    print("\n  By category:")
    for cat, stats in sorted(summary["by_category"].items()):
        status = "PASS" if stats["failed"] == 0 else "FAIL"
        warn_str = f" ({stats['warned']} warns)" if stats["warned"] > 0 else ""
        print(f"    {cat:20s}: {stats['passed']}/{stats['total']} [{status}]{warn_str}")

    if summary["failed"] > 0:
        print(f"\n  RESULT: {summary['failed']} TESTS FAILED")
        print("\n  Failures:")
        for r in harness.results:
            if not r.passed and r.severity == "FAIL":
                print(f"    - [{r.category}] {r.test_name}: {r.message}")
    else:
        print(f"\n  RESULT: ALL TESTS PASSED")

    if args.report:
        with open(args.report, "w") as f:
            json.dump(summary, f, indent=2)
        print(f"\n  Report saved to: {args.report}")

    sys.exit(1 if summary["failed"] > 0 else 0)


if __name__ == "__main__":
    main()
