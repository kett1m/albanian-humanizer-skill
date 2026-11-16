# Maintaining this skill

The canonical skill is `skills/albanian-humanizer/`. Keep it self-contained:
native installers may copy only that directory. Keep credits and license notices
inside every generated distribution.

Use the existing references for language-specific detail. Preserve the distinction
between standard Albanian, dialect groups, and Kosovo regional usage. Level,
register, dialect, and medium remain independent. Do not describe examples as
native-reviewed or CEFR-certified without evidence.

The Python tools use only the standard library. Validate changes with:

```bash
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
python3 scripts/package_skill.py --output dist
```

For installer changes, use Node.js 22.20+ and run `npm ci --ignore-scripts`
followed by `npm test`. The interactive installer uses the pinned Skills API.
Exercise installation in an isolated project with `--project`, preserving real
user-level agent directories.

For behavioral changes, exercise relevant cases from `evals/cases.json` and
report what actually ran. Do not overwrite another project's agent instructions
or install globally as part of packaging. Generated files belong in `dist/`.
