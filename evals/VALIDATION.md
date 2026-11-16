# Validation record

Release: 1.0.0. Date: 2026-11-16.

This record distinguishes package checks from model-based editorial review.
No execution of every supported agent product, native-speaker certification,
or official CEFR assessment is claimed.

| Check actually run | Result |
| --- | --- |
| Repository validator | Passed: resources, UTF-8, local links, notices, evaluation schema |
| Python packaging suite | 12 tests passed |
| Bash installer suite | 10 terminal-based tests passed; all cataloged project paths checked |
| Shell syntax and lint | `bash -n`, ShellCheck, and all 9 Bash documentation blocks passed |
| PowerShell 7.7 on Linux | Parser and catalog checks passed; interactive installation to all 53 distinct project folders preserved all 15 files |
| Skill-creator `quick_validate.py` | Passed |
| Skills CLI 1.9.0, `skills add <local-repo> --list` | Discovered exactly one skill: `albanian-humanizer` |
| Remote installation documentation follow-up | Installed from GitHub to all 79 CLI project targets on openSUSE Tumbleweed; verified 53 distinct folders |
| Independent model forward-test | All 24 requests executed and reviewed; no blocking fidelity or task-contract failures |
| Isolated saved-file forward-test | Passed: only authorized prose changed; protected spans preserved |

Packaging checks cover complete ZIP resources, flattened-prompt anchors,
checksums, deterministic rebuilds, and refusal to overwrite existing artifacts
without an explicit rebuild flag. The initial CLI discovery check was list-only.
The subsequent remote-install smoke test used an isolated project and checked
parsed frontmatter, instruction bodies, references, and licenses against the
source. One target normalized YAML layout while preserving values. Neither check
installed globally or tested each agent application's runtime behavior.

The current [installation guide](../docs/INSTALL.md) uses raw shell and
PowerShell scripts. The Bash tests exercise a script arriving through a pipe,
explicit choices, invalid input, cancellation/EOF, custom paths with spaces and
shell metacharacters, shared-path deduplication, all profiles, update backups,
symlink refusal, failed downloads, and preview mode. Installed resources and
licenses are byte-identical to the canonical skill. Native global installations
and OS package-manager prerequisite commands were not run.

The previous npm installer and its nine tests were removed when the shell
installer replaced it. The earlier CLI installation checks above are historical.
PowerShell 7.7 was downloaded from Microsoft's official release and run portably
on Linux for syntax and interactive installation checks. Windows PowerShell 5.1,
Windows-specific filesystem behavior, and macOS execution were not tested.
The public raw endpoint remains unavailable while the repository is private.

The full [forward-test report](FORWARD_TEST_RESULTS.md) contains actual responses,
review findings, the saved-file fixture, and comparisons. The reviewing agent
inherited the parent model in the Codex session; no separate model identifier or
native-language credential was asserted. Cases 4–6 and 8 overlap substantially
with examples in the skill; later cases use unseen passages. Cases 17–24 were
generated before the reviewer read their rubrics.

One minor execution weakness remained: a B1 rewrite retained the unexplained
technical word “intervention”. The existing guidance calls for contextual
explanations, but model compliance is not guaranteed. The A2 administrative
example demonstrates preservation of conditions more clearly than learner-tested
accessibility. English `you` and Albanian `kërkesat` also require context for
socially or institutionally exact translation.

These are documented limitations, not reasons to claim perfect language output.
The release offers approximate CEFR targets and broad dialect guidance. Exact
local authenticity and proficiency grading require additional human evidence.
