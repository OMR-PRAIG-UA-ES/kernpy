# Sources of the **mens test data

| Path | Source | Licence |
|---|---|---|
| `mensural_vocabulary.mens` | Written for kernpy: every figure, quality, dot and mark the shared grammar reads | kernpy's |
| `apel/*.krn` | The examples of Willi Apel, *The Notation of Polyphonic Music 900-1600*, encoded for mOOsicae (`tests/io/apel/`, commit `e313bb36`) | kernpy's |
| `seils/*.mns` | [SEILS dataset](https://github.com/SEILSdataset/SEILSdataset) (Il Lauro Secco, 1582), `SEILS_diplomatic_OMRgroundTruth`, commit `00d442f4`: `choral/perue_seitu_choral.mns` and `particellas_codified/belli_amorcon_C.mns`, unmodified | [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/), by the SEILS authors |
| `reference/*.mens` | Written for mOOsicae and kernpy in Craig Sapp's `**mens` syntax (<https://doc.verovio.humdrum.org/humdrum/mens/>), one construct per file, signifiers in several orders; copied from mOOsicae `tests/io/fixtures/mens-reference/authored/` | kernpy's |
| `muret/muret_semantic_sample.json` | MuRET's mensural semantic encodings (mOOsicae `testbed/io/muret/muret_mensural_semantic_23_july_2024.csv`, David Rizo), `@ids` stripped, the 678 rows that hold every distinct cell, with mOOsicae's export of each | kernpy's |

`belli_amorcon_C.mns` is here for its dialect: SEILS writes a bare `*custos` (the grammar wants its
pitch, `*custosG`), which kernpy reports as an error and exports verbatim. Its perfection mark after
the coloration (`s~id`) is valid `**mens` (Humdrum does not fix the order of a token's signifiers)
and is read as `si~d`.
