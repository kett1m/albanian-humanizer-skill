#!/usr/bin/env python3
"""Validate this package's structure and local links, without network access.

This is not a general YAML parser or a linguistic/CEFR assessment.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "albanian-humanizer"
LINK = re.compile(r"\[([^\]\n]+)\]\(([^\s)]+)\)")
REFERENCES = (
    "editing.md", "albanian.md", "sq-standard.md", "sq-gheg.md",
    "sq-tosk.md", "sq-kosovo.md", "english.md",
    "levels-and-translation.md", "narrative.md", "sources.md",
)


def local_target(origin: Path, href: str) -> Path | None:
    """Resolve a simple local Markdown link, leaving web links and anchors alone."""
    url = urlsplit(href)
    if url.scheme or url.netloc or not url.path:
        return None
    return (origin.parent / unquote(url.path)).resolve()


def validate_links(root: Path, files: list[Path]) -> list[str]:
    errors = []
    root = root.resolve()
    for path in files:
        for _, href in LINK.findall(path.read_text(encoding="utf-8")):
            target = local_target(path, href)
            if target is None:
                continue
            if not target.is_relative_to(root):
                errors.append(f"Link escapes package: {path.name}: {href}")
            elif not target.is_file():
                errors.append(f"Missing link target: {path.name}: {href}")
    return errors


def validate_skill(skill: Path = SKILL) -> list[str]:
    skill = skill.resolve()
    errors = []
    required = ["SKILL.md", "LICENSE", "THIRD_PARTY_NOTICES.md",
                "licenses/blader-MIT.txt", "agents/openai.yaml"]
    required += [f"references/{name}" for name in REFERENCES]
    for name in required:
        path = skill / name
        if not path.is_file() or path.is_symlink():
            errors.append(f"Missing or linked required file: {name}")
    if errors:
        return errors

    paths = sorted(skill.rglob("*"))
    for path in paths:
        if path.is_symlink():
            errors.append(f"Symlink not allowed in distributable skill: {path.name}")
    if errors:
        return errors

    entry = (skill / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", entry, re.S)
    if not match:
        errors.append("SKILL.md requires LF-delimited YAML frontmatter")
    else:
        header = match.group(1)
        name = re.search(r"^name: ([a-z0-9-]+)$", header, re.M)
        if not name or name.group(1) != skill.name or len(name.group(1)) > 64:
            errors.append("Skill name must match its directory and the format spec")
        description = re.search(r"^description: >-\n((?:  [^\n]*\n?)+)", header, re.M)
        if not description or not 1 <= len(description.group(1).strip()) <= 1024:
            errors.append("Expected a nonempty folded description of at most 1024 characters")
    if len(entry.splitlines()) > 500:
        errors.append("SKILL.md exceeds the package's 500-line discovery budget")
    for path in paths:
        if path.is_file():
            try:
                body = path.read_text(encoding="utf-8")
                if not body.endswith("\n"):
                    errors.append(f"Missing final newline: {path.name}")
                if "\ufffd" in body:
                    errors.append(f"Unicode replacement character: {path.name}")
            except UnicodeDecodeError:
                errors.append(f"Non-UTF-8 file in text skill: {path.name}")
    errors += validate_links(skill, list(skill.rglob("*.md")))
    license_text = (skill / "licenses/blader-MIT.txt").read_text(encoding="utf-8")
    if "Copyright (c) 2025 Siqi Chen" not in license_text:
        errors.append("Upstream MIT copyright notice missing")
    if "THE SOFTWARE IS PROVIDED" not in license_text:
        errors.append("Upstream MIT license text incomplete")
    ui = (skill / "agents/openai.yaml").read_text(encoding="utf-8")
    if "$albanian-humanizer" not in ui:
        errors.append("OpenAI default prompt must invoke the canonical skill")
    return errors


def validate_repo(root: Path = ROOT) -> list[str]:
    root = root.resolve()
    errors = validate_skill(root / "skills" / "albanian-humanizer")
    markdown = [root / "README.md", root / "AGENTS.md"]
    markdown += list((root / "docs").glob("*.md"))
    markdown += list((root / "evals").glob("*.md"))
    errors += validate_links(root, markdown)
    try:
        cases = json.loads((root / "evals" / "cases.json").read_text(encoding="utf-8"))
        seen = set()
        for case in cases:
            if not isinstance(case, dict) or not all(case.get(k) for k in ("id", "request", "rubric", "tags")):
                errors.append("Evaluation case missing id, request, rubric, or tags")
                continue
            if case["id"] in seen:
                errors.append(f"Duplicate evaluation ID: {case['id']}")
            seen.add(case["id"])
            if not isinstance(case["rubric"], list) or not isinstance(case["tags"], list):
                errors.append(f"Evaluation rubric/tags must be lists: {case['id']}")
    except (ValueError, OSError) as exc:
        errors.append(f"Cannot read evaluation cases: {exc}")
    if (root / "LICENSE").read_bytes() != (root / "skills/albanian-humanizer/LICENSE").read_bytes():
        errors.append("Repository and skill MIT licenses differ")
    return errors


def main() -> int:
    errors = validate_repo()
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        return 1
    print("Package structure, UTF-8 resources, local links, notices, and case schema: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
