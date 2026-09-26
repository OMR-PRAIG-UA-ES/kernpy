# Mensural Notation: **mens

kernpy reads and writes `**mens` spines, the Humdrum representation of white mensural notation
(roughly 1450-1600), next to `**kern` spines in the same file.

```python
import kernpy as kp

document, errors = kp.loads(
    "**mens\n*clefC1\n*met(C)\nSc\nsd\nMe\nmf\n*-\n")
print(kp.dumps(document))
```

## One grammar, shared with mOOsicae

`**mens` cells are parsed with the combined `**kern`/`**mens` grammar of mOOsicae, the
TypeScript library of the same ecosystem, **vendored verbatim** in `kern/kernMensSpine*.g4`. Both
libraries therefore accept and reject the same `**mens` tokens. The grammar is never edited in
kernpy: it is changed in mOOsicae and copied back (`kern/README-mens.md`). `**kern` spines keep
their own grammar, `kern/kernSpine*.g4`, because in the combined one the mensural figures (`M`,
`m`, `S`...) collide with `**kern` articulations and ornaments.

## What a mensural note looks like

A note is its duration, then its pitch, then its marks:

| Part | Signifiers | Example |
|---|---|---|
| Figure | `X` maxima, `L` longa, `S` breve, `s` semibreve, `M` minima, `m` semiminima, `U` fusa, `u` semifusa | `Sc` |
| Perfection | `p` perfect, `i` imperfect, `I` imperfect by alteration, **right after the figure** | `Sic` |
| Coloration | `~`, after the perfection | `si~d` |
| Dot | `.` augmentation, `:` division, last | `sp:a` |
| Ligature | `<` starts, `>` ends | `<Sa`, `Sg>` |
| Rest | the figure and `r` | `sr` |

kernpy keeps the whole mensural duration (figure, perfection, coloration and dot) as **one**
duration subtoken, as written, so the export never reorders it.

Tandem interpretations include mensurations (`*met(O)`, `*met(C|)`, with the optional
`*met(O)_2232` specification of maximodus, modus, tempus and prolatio), clefs, key signatures,
`*custosG` (a custos with its pitch) and layout marks.

## Export

The export is kernpy's normalised form, the same as for `**kern`:

- global comments (`!!!`) and hidden tokens such as invisible barlines (`=1-`) are not written;
  they still count measures;
- the marks of a note follow its pitch: `<S~a` is written `S~a<`, which the grammar reads as the
  same ligature start.

Exporting what kernpy imported and importing it again gives back the same document: the export is a
fixed point. The test suite checks this, and that every note and rest survives, over the Willi
Apel examples of mOOsicae and over two files of the
[SEILS dataset](https://github.com/SEILSdataset/SEILSdataset); set `KERNPY_MENS_CORPUS` to a
directory to run the same checks over a whole corpus (all 180 `**mens` files of SEILS pass).

## Dialects and errors

Like any token the grammar does not read, a non-standard `**mens` cell is reported in the `errors`
list returned by `kp.load`/`kp.loads` (or raised with `raise_on_errors=True`) and kept verbatim in
the document and in the export. SEILS, for instance, writes:

- a bare `*custos`: the grammar wants its pitch, `*custosG`;
- the perfection mark after the coloration, `s~id`: the grammar wants `si~d`. Read as it stands,
  the `i` would become a note decoration and the note would lose its imperfection, so kernpy
  reports it instead;
- the coloration after the dot, `Mp:~`.

Readers of such sources normalise them before parsing if they want those cells as notes.
