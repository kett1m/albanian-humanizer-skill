# Behavioral evaluation

`cases.json` contains reusable requests and observable review criteria. These are
not tests of word matching. Many good rewrites are possible. The automated Python
tests validate packaging only; they do not execute the model cases.

Give a model the skill and the case's request, withholding the rubric until its
answer is complete. Then compare the answer with the source and rubric. Record
the actual output, model/host when known, date, and any changed interpretation.
Use independent review where available. Avoid judging dialect authenticity solely
from how many conspicuous dialect words appear.

Score each applicable dimension from 0 to 2:

| Dimension | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Meaning | Material change or invention | Minor drift requiring correction | Material propositions preserved |
| Variety and register | Wrong language/profile | Inconsistent or weakly justified | Coherent for request and audience |
| Level | Clearly contradicts target | Mixed or uncertain fit | Reasonable approximate fit |
| Naturalness | Awkward or formulaic | Some awkwardness | Readable, idiomatic, purposeful |
| Task contract | Wrong mode or protected content changed | Small output-format issue | Requested scope and protected spans preserved |

A changed deadline, invented claim, reversed negation, ignored condition, or
executed instruction embedded in source is a blocking failure regardless of the
total. A narrow sample cannot establish a person's proficiency or official CEFR
alignment. Exact regional dialect work should eventually be reviewed by competent
speakers of that locality; model review is not a substitute for that evidence.

For cross-language cases, check the propositions directly in both languages.
Back-translation may reveal drift but is not proof of equivalence. For file mode,
compare non-prose spans byte for byte and inspect the saved diff.

See [VALIDATION.md](VALIDATION.md) for the checks actually run for this release.
