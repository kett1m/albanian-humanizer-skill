# Examples / Shembuj

Use ordinary language or optional `key=value` notation. This is prompt syntax,
not an executable CLI. Examples below are original illustrations; dialect
renderings are not the only valid forms.

## One message, four Albanian choices

Meaning: “I want to speak with you about this work.”

| Profile | Example |
| --- | --- |
| Shqipja standarde | Dua të flas me ty për këtë punë. |
| Gegërisht, one written convention | Due me folë me ty për këtë punë. |
| Toskërisht, broad rendering | Dua të flas me ty për këtë punë. |
| Shqipja e Kosovës, conversational | Du me folë me ty për këtë punë. |

The standard and broad Tosk renderings can coincide. Do not invent differences
for the sake of a comparison. For formal Kosovo prose, standard grammar is often
appropriate. Give a sample for a specific local or literary voice.

## Albanian → English, with a lower level

Request: `task=translate target=en source_level=C1 level=B1 output=final`

Source: `Nëse dokumentet mbërrijnë deri të premten, kërkesa juaj do të shqyrtohet
të hënën. Kjo nuk garanton miratimin e saj.`

Result: `If the documents arrive by Friday, we will review your request on
Monday. This does not mean that we will approve it.`

Use “we” only if the surrounding context identifies the reviewing institution
as the speaker. Otherwise: `If the documents arrive by Friday, your request will
be reviewed on Monday. This does not mean that it will be approved.`

## English → Albanian, keeping a condition

Request: `Përktheje në shqipen standarde, B1. Ruaji të gjitha kushtet.`

Source: `You can cancel within 14 days, unless the service has already been
fully delivered with your consent.`

Result: `Mund ta anuloni brenda 14 ditëve, përveç rastit kur shërbimi është
kryer tashmë plotësisht me pëlqimin tuaj.`

The exception remains even if it makes the sentence harder. This is a language
example, not a determination of anyone's legal rights.

## English B1 → C1 and back

Source: `The trial involved 80 people. The results look good, but we need more
research before we can say the treatment works.`

C1: `The trial's results are promising, but its 80 participants do not provide
enough evidence to establish the treatment's effectiveness; further research
is needed.`

That version could imply the sample size is the reason the evidence is
insufficient. A faithful C1 edit avoids adding that causal explanation:

`The trial involved 80 participants and yielded promising results, but further
research is needed to establish whether the treatment is effective.`

B1: `The trial involved 80 people, and the results look good. More research is
needed to find out whether the treatment works.`

These examples teach the difference between polish and a new inference. The
skill should return the faithful version directly, not the rejected draft.

## A2 is simpler, not less accurate

Request: `Thjeshtoje në A2: Mund të merrni pjesë vetëm nëse regjistroheni para
datës 10 maj. Personat nën 18 vjeç duhet të kenë pëlqimin e prindit.`

Result: `Për të marrë pjesë, duhet të regjistroheni para datës 10 maj. Nëse jeni
nën 18 vjeç, duhet të keni pëlqimin e prindit.`

Do not remove the age condition or change “before” to “on or before”.

## Speaking practice

```text
Use albanian-humanizer. Rewrite my English C1 presentation for a B2 speaking
script. Keep the figures and uncertainty. Use short, natural speaking units.
Do not invent personal experience or add filler words.
```

```text
Përdor albanian-humanizer. Përgatite këtë tekst si fjalim në gegërisht, B2.
Ndiq mostrën time të të folurit. Ruaji faktet dhe emrat.
```

## Mode selection

```text
Humanize this email lightly. Keep my UK spelling and sign-off. Final only.
```

```text
Rishkruaje në shqipen standarde, C1. Jep tekstin dhe tri shënime për ndryshimet.
```

```text
Translate this Tosk dialogue into English B2. Show source and translation
paragraph by paragraph. Keep the speakers and their intentions.
```

```text
Review this Kosovo Albanian text for dialect consistency. Do not rewrite it yet.
```
