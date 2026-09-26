# The **mens grammar

`kernMensSpineLexer.g4` and `kernMensSpineParser.g4` are **mOOsicae's** combined `**kern`/`**mens`
grammar (`antlr/humdrum/` in mOOsicae), copied here **verbatim**. kernpy parses `**mens` spines with
it (`kernpy/core/mens_spine_importer.py`), so kernpy and mOOsicae read `**mens` alike by construction.
`**kern` spines keep `kernSpine*.g4`.

- **Never edit these two files here.** Change them in mOOsicae, copy them back, run `./antlr4.sh`
  and commit the regenerated `kernpy/core/generated/kernMensSpine*`.
- Why two grammars and not one: in the combined grammar the mensural figures (`M`, `m`, `S`...)
  collide with `**kern` articulations and ornaments, which mOOsicae strips before the parse. The
  `**kern` grammar is shared too, rule by rule, with its differences declared in mOOsicae's
  `antlr/humdrum/kern-grammar-agreement.json`.
- **Dialects stay out.** The public SEILS dataset writes a bare `*custos` (the grammar wants its
  pitch, `*custosG`), puts the coloration after a division dot (`Mp:~`) and has a stray `ui6G`.
  Readers of such sources normalise them before parsing; the shared grammar reads the standard.
