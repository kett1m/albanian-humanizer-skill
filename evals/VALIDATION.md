# Validation record

Release: 1.0.0. Date: 2026-11-16.

This record distinguishes package checks from model-based editorial review.
No live installation across every supported agent, native-speaker certification,
or official CEFR assessment is claimed.

| Check actually run | Result |
| --- | --- |
| Repository validator | Passed: resources, UTF-8, local links, notices, evaluation schema |
| Python packaging suite | 12 tests passed |
| Skill-creator `quick_validate.py` | Passed |
| Skills CLI 1.9.0, `skills add <local-repo> --list` | Discovered exactly one skill: `albanian-humanizer` |
| Independent model forward-test | All 24 requests executed and reviewed; no blocking fidelity or task-contract failures |
| Isolated saved-file forward-test | Passed: only authorized prose changed; protected spans preserved |

Packaging checks cover complete ZIP resources, flattened-prompt anchors,
checksums, deterministic rebuilds, and refusal to overwrite existing artifacts
without an explicit rebuild flag. The CLI check was list-only; it did not install
the skill globally or test each agent's runtime behavior.

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
