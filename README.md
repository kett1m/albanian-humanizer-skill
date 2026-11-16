# Shqip & English Humanizer

Natural Albanian and English, with the writer's meaning intact.

One portable skill for editing, translation, dialect adaptation, and simpler or
more advanced language. Created by **kett1m**. The repository is named
`albanian-humanizer-skill`; the installable skill is **`albanian-humanizer`**.

## Install in one line

Paste into your terminal, choose your AI agent, then type **y**.

**Linux / macOS**, including **openSUSE Tumbleweed**:

```bash
curl -fsSL https://raw.githubusercontent.com/kett1m/albanian-humanizer-skill/main/install.sh | bash
```

**Windows PowerShell**:

```powershell
irm https://raw.githubusercontent.com/kett1m/albanian-humanizer-skill/main/install.ps1 | iex
```

**Availability:** this repository is currently private. These anonymous raw URLs
will work after the owner makes it public. Until then, run `bash install.sh`
from an authorized local checkout; on Windows, run `./install.ps1` where local
script execution is permitted.

The script asks **“Which AI agent or app do you use?”** Choose Codex, Claude Code,
Cursor, Copilot, Gemini CLI, OpenCode, Windsurf, Cline, or type **more** for the
full list. Separate multiple choices with commas. Choice **0** accepts a custom
skills folder. No Node, npm, npx, Git, or Python is needed for the online installer.

The installer shows the destination before writing. It copies the complete skill
and preserves an existing copy in a backup folder before updating it. Restart
your agent afterward and ask it to use **albanian-humanizer**.

[Installation guide](docs/INSTALL.md): distro prerequisites, project installs,
offline setup, updates, and other agents. The shell installer needs Bash 3.2+,
curl, tar, and gzip; Windows uses PowerShell 5.1 or 7.

## Choose a voice

| Profile | Proper name | Use |
| --- | --- | --- |
| `sq-standard` | **Shqipja standarde** — Standard Albanian | General, professional, educational, and formal writing |
| `sq-gheg` | **Gegërisht / Gegnisht** — Gheg Albanian | A coherent Gheg voice, guided by locality or a sample |
| `sq-tosk` | **Toskërisht** — Tosk Albanian | A broad or specified southern Albanian voice |
| `sq-kosovo` | **Shqipja e Kosovës** — Kosovo Albanian | Formal standard usage or conversational Kosovo Albanian, according to context |
| `en` | **English / Anglisht** | Natural English, retaining UK/US conventions or a supplied voice |

These names identify a standard variety, dialect groups, and a regional profile;
they are not four separate Albanian languages. Tosk and standard are not identical
labels, and Kosovo does not automatically mean slang. Strong local rendering
works best with a sample from the intended speaker.

Choose **A1, A2, B1, B2, C1, or C2** for either language, or preserve the existing
complexity. Move up or down, within one language or during translation:

```text
Use albanian-humanizer. Translate this English C1 text into standard Albanian B1.
Keep every condition and number. Return only the translation.

[Your text]
```

```text
Përdor albanian-humanizer. Rishkruaje në shqipen bisedore të Kosovës, niveli B2.
Ruaje kuptimin dhe mos shto zhargon. Kthe vetëm tekstin.

[Teksti yt]
```

```text
Use albanian-humanizer. Rewrite this English B1 text at C2, without adding claims.
```

```text
Përdor albanian-humanizer. Thjeshtoje këtë tekst nga C1 në A2, në shqipen standarde.
```

Levels guide approximate text complexity; they do not certify a person's language
ability. A speaking request produces a speakable script. C2 can be concise and
plain; A1 remains grammatical and respectful.

## Any agent that accepts instructions

The source follows the [Agent Skills format](https://agentskills.io/specification).
For chat tools, custom assistants, local models, or agent frameworks without
native skills, build a standalone prompt:

```bash
python3 scripts/package_skill.py --output dist
```

This produces:

- `dist/albanian-humanizer.zip`: the complete skill in a correctly named folder.
- `dist/albanian-humanizer-prompt.md`: the core instructions and all references
  in one file, with internal links rewritten to in-document anchors.
- `dist/SHA256SUMS`: checksums for both artifacts.

Load the prompt as task instructions where the host permits, then provide the
text and settings separately. The package does not require vendor-specific
tools, shell access, external services, or network access for prose work.
Compatibility is by format and prompt portability; it is not a claim that every
agent or model has been tested. Model quality and context limits still matter.

## What it does

- Preserves facts, quantities, negation, conditions, uncertainty, quotations,
  citations, and protected code or placeholders.
- Edits sentence and paragraph structure, not just a list of “AI words”.
- Preserves dialect and voice unless the user asks for a change.
- Translates Albanian ↔ English and changes CEFR target in either direction.
- Handles prose, emails, public notices, academic and technical text, speeches,
  dialogue, fiction, and personal narrative with different editorial needs.
- Returns the finished text by default; offers annotated, parallel, and review
  modes when requested.

Narrative guidance is conditional: no compulsory subplot, time jump, moral flaw,
or ambiguous ending. It does not invent memoir details or guarantee detector
results. See [bilingual examples](docs/EXAMPLES.md) and the
[complete skill](skills/albanian-humanizer/SKILL.md).

## Validation and development

Python 3.10+ is required only for packaging and local checks. No third-party
Python packages are needed by the repository tools.

```bash
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
python3 scripts/package_skill.py --output dist
```

For shell installer development, run `bash -n install.sh` and
`shellcheck install.sh`. The Python suite also exercises the installer in a real
terminal. Test installations in an isolated project with `--project`.

[Behavioral cases](evals/cases.json) test decisions that file validation cannot
prove. The [evaluation guide](evals/README.md) explains the rubric and limits.
Language examples are editorial illustrations, not CEFR-certified test items.

## Credits and license

Thanks to **[Siqi Chen (blader)](https://github.com/blader/humanizer)** for Humanizer's
prose-editing approach and **[joeinvents](https://github.com/joeinvents/humanizerskill)**
for emphasizing narrative structure. This project combines those complementary
ideas with original Albanian profiles, bilingual workflows, CEFR adaptation,
examples, and portable packaging.

Blader's MIT copyright and permission notice are preserved. The inspected
joeinvents revision has no license file; it is credited as conceptual inspiration,
and its skill text is not copied or redistributed. See the precise revisions,
scope of adaptation, and research credits in
[THIRD_PARTY_NOTICES.md](skills/albanian-humanizer/THIRD_PARTY_NOTICES.md).
Original contributions are [MIT-licensed](LICENSE).
