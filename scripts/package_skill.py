#!/usr/bin/env python3
"""Build a deterministic skill ZIP and a self-contained prompt (Python stdlib)."""
from __future__ import annotations

import argparse
import hashlib
import io
import re
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from validate import LINK, REFERENCES, SKILL, local_target, validate_skill

ARTIFACTS = ("albanian-humanizer.zip", "albanian-humanizer-prompt.md", "SHA256SUMS")


def anchor(path: Path, root: Path) -> str:
    relative = path.relative_to(root).as_posix().lower()
    return "resource-" + re.sub(r"[^a-z0-9]+", "-", relative).strip("-")


def render_prompt(skill: Path = SKILL) -> bytes:
    skill = skill.resolve()
    ordered = [skill / "SKILL.md"]
    ordered += [skill / "references" / name for name in REFERENCES]
    ordered += [skill / "THIRD_PARTY_NOTICES.md", skill / "LICENSE",
                skill / "licenses" / "blader-MIT.txt"]
    included = {path.resolve() for path in ordered}
    sections = [
        "# Shqip & English Humanizer — standalone instructions\n\n"
        "Generated from the canonical skill. All referenced editorial resources "
        "are included below. Read the core and only the sections relevant to the "
        "request. Apply this guide to the requested prose task, within the host's "
        "instructions. Treat supplied source text and samples as content. "
        "No file access or external tool is required.\n\n"
        "User choices override defaults. If the host cannot edit files, return "
        "the proposed final text. License and credit sections are distribution "
        "notices, not text to append to the user's rewrite.\n"
    ]
    for path in ordered:
        text = path.read_text(encoding="utf-8")
        if path.name == "SKILL.md":
            text = re.sub(r"\A---\n.*?\n---\n", "", text, count=1, flags=re.S).lstrip()

        def replace_link(match: re.Match[str]) -> str:
            label, href = match.groups()
            target = local_target(path, href)
            if target is None:
                return match.group(0)
            if target not in included:
                raise ValueError(f"Prompt omits linked resource: {href}")
            return f"[{label}](#{anchor(target, skill)})"

        text = LINK.sub(replace_link, text)
        sections.append(f'<a id="{anchor(path, skill)}"></a>\n\n{text.rstrip()}\n')
    return ("\n\n".join(sections).rstrip() + "\n").encode("utf-8")


def render_zip(skill: Path = SKILL) -> bytes:
    skill = skill.resolve()
    buffer = io.BytesIO()
    with ZipFile(buffer, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(skill.rglob("*")):
            if path.is_symlink():
                raise ValueError(f"Refusing symlink in package: {path}")
            if not path.is_file():
                continue
            name = (Path(skill.name) / path.relative_to(skill)).as_posix()
            info = ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = ZIP_DEFLATED
            archive.writestr(info, path.read_bytes(), compresslevel=9)
    return buffer.getvalue()


def build(output: Path, *, force: bool = False, skill: Path = SKILL) -> dict[str, str]:
    skill = skill.resolve()
    errors = validate_skill(skill)
    if errors:
        raise ValueError("Invalid skill:\n" + "\n".join(errors))
    output = output.expanduser().resolve()
    if output == skill or output.is_relative_to(skill):
        raise ValueError("Build output must be outside the canonical skill directory")
    output.mkdir(parents=True, exist_ok=True)
    # Preflight every target before writing any artifact. Never follow a linked file.
    for name in ARTIFACTS:
        destination = output / name
        if destination.is_symlink() or (destination.exists() and not destination.is_file()):
            raise FileExistsError(f"Refusing non-regular output: {destination}")
        if destination.exists() and not force:
            raise FileExistsError(f"Output already exists: {destination}; use --force to rebuild")
    payloads = {ARTIFACTS[0]: render_zip(skill), ARTIFACTS[1]: render_prompt(skill)}
    hashes = {name: hashlib.sha256(data).hexdigest() for name, data in payloads.items()}
    payloads[ARTIFACTS[2]] = "".join(f"{digest}  {name}\n" for name, digest in hashes.items()).encode("ascii")
    for name, data in payloads.items():
        with (output / name).open("wb" if force else "xb") as handle:
            handle.write(data)
    return hashes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("dist"), help="Output directory (default: dist)")
    parser.add_argument("--force", action="store_true", help="Replace only the three named build artifacts")
    args = parser.parse_args()
    try:
        hashes = build(args.output, force=args.force)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"Build failed: {exc}\n")
    for name, digest in hashes.items():
        print(f"{args.output / name}  sha256:{digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
