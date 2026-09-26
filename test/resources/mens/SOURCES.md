# Sources of the **mens test data

| Path | Source | Licence |
|---|---|---|
| `mensural_vocabulary.mens` | Written for kernpy: every figure, quality, dot and mark the shared grammar reads | kernpy's |
| `apel/*.krn` | The examples of Willi Apel, *The Notation of Polyphonic Music 900-1600*, encoded for mOOsicae (`tests/io/apel/`, commit `e313bb36`) | kernpy's |
| `seils/*.mns` | [SEILS dataset](https://github.com/SEILSdataset/SEILSdataset) (Il Lauro Secco, 1582), `SEILS_diplomatic_OMRgroundTruth`, commit `00d442f4`: `choral/perue_seitu_choral.mns` and `particellas_codified/belli_amorcon_C.mns`, unmodified | [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/), by the SEILS authors |

`belli_amorcon_C.mns` is here for its dialect: SEILS writes a bare `*custos` (the grammar wants its
pitch, `*custosG`) and puts the perfection mark after the coloration (`s~id`, the grammar wants
`si~d`). kernpy reports those cells as errors and exports them verbatim.
