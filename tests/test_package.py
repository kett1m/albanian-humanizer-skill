"""Observable package integrity tests; no network, agents, or global installation."""
from __future__ import annotations

import hashlib
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from package_skill import ARTIFACTS, build, render_prompt
from validate import LINK, ROOT, SKILL, validate_repo, validate_skill


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="albanian-humanizer-test-")
        self.base = Path(self.temp.name)
        self.output = self.base / "dist"

    def tearDown(self):
        self.temp.cleanup()

    def copy_skill(self):
        return Path(shutil.copytree(SKILL, self.base / SKILL.name))

    def test_repository_is_self_contained(self):
        self.assertEqual(validate_repo(ROOT), [])

    def test_archive_round_trip_contains_every_resource(self):
        build(self.output)
        with ZipFile(self.output / ARTIFACTS[0]) as archive:
            expected = {f"{SKILL.name}/{p.relative_to(SKILL).as_posix()}": p.read_bytes()
                        for p in SKILL.rglob("*") if p.is_file()}
            self.assertEqual(set(archive.namelist()), set(expected))
            self.assertIsNone(archive.testzip())
            for name, data in expected.items():
                self.assertEqual(archive.read(name), data)
                self.assertFalse(name.startswith("/") or ".." in Path(name).parts)
            archive.extractall(self.base / "extracted")
        self.assertEqual(validate_skill(self.base / "extracted" / SKILL.name), [])

    def test_flat_prompt_has_no_unresolved_file_links(self):
        prompt = render_prompt().decode("utf-8")
        anchors = re.findall(r'<a id="([^"]+)"', prompt)
        self.assertEqual(len(anchors), len(set(anchors)))
        for _, href in LINK.findall(prompt):
            self.assertTrue(href.startswith(("https://", "http://", "#")), href)
            if href.startswith("#"):
                self.assertIn(href[1:], anchors)
        self.assertIn("Shqipja e Kosovës", prompt)
        self.assertIn("Copyright (c) 2025 Siqi Chen", prompt)
        self.assertIn("Copyright (c) 2026 kett1m", prompt)

    def test_checksums_match_actual_artifacts(self):
        hashes = build(self.output)
        for line in (self.output / "SHA256SUMS").read_text().splitlines():
            digest, name = line.split("  ", 1)
            self.assertEqual(digest, hashlib.sha256((self.output / name).read_bytes()).hexdigest())
            self.assertEqual(hashes[name], digest)

    def test_rebuild_is_deterministic(self):
        build(self.output)
        first = {name: (self.output / name).read_bytes() for name in ARTIFACTS}
        build(self.output, force=True)
        self.assertEqual(first, {name: (self.output / name).read_bytes() for name in ARTIFACTS})

    def test_existing_outputs_are_preserved_without_force(self):
        self.output.mkdir()
        protected = self.output / ARTIFACTS[1]
        protected.write_text("user content", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            build(self.output)
        self.assertEqual(protected.read_text(), "user content")
        self.assertFalse((self.output / ARTIFACTS[0]).exists())

    def test_force_keeps_unrelated_files(self):
        build(self.output)
        unrelated = self.output / "notes.md"
        unrelated.write_text("keep", encoding="utf-8")
        build(self.output, force=True)
        self.assertEqual(unrelated.read_text(), "keep")

    def test_output_inside_skill_is_rejected(self):
        skill = self.copy_skill()
        with self.assertRaises(ValueError):
            build(skill / "dist", skill=skill)
        self.assertFalse((skill / "dist").exists())

    def test_missing_reference_is_rejected_before_build(self):
        skill = self.copy_skill()
        (skill / "references/sq-tosk.md").unlink()
        with self.assertRaises(ValueError):
            build(self.output, skill=skill)
        self.assertFalse(self.output.exists())

    def test_escaping_local_link_is_rejected(self):
        skill = self.copy_skill()
        with (skill / "references/editing.md").open("a", encoding="utf-8") as handle:
            handle.write("\n[Outside](../../../outside.md)\n")
        self.assertTrue(any("escapes" in error for error in validate_skill(skill)))

    def test_symlink_source_is_rejected(self):
        skill = self.copy_skill()
        path = skill / "references/english.md"
        path.unlink()
        try:
            path.symlink_to(SKILL / "references/english.md")
        except (OSError, NotImplementedError):
            self.skipTest("Symlinks not available on this host")
        with self.assertRaises(ValueError):
            build(self.output, skill=skill)

    def test_symlink_output_is_rejected_even_with_force(self):
        self.output.mkdir()
        outside = self.base / "outside.txt"
        outside.write_text("keep", encoding="utf-8")
        try:
            (self.output / ARTIFACTS[0]).symlink_to(outside)
        except (OSError, NotImplementedError):
            self.skipTest("Symlinks not available on this host")
        with self.assertRaises(FileExistsError):
            build(self.output, force=True)
        self.assertEqual(outside.read_text(), "keep")


if __name__ == "__main__":
    unittest.main()
