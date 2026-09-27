# Changelog

Release notes up to 1.9.3 are in [GitHub Releases](https://github.com/OMR-PRAIG-UA-ES/kernpy/releases).

## 1.10.0

### Added

- **`**mens` support.** `**mens` spines are parsed with mOOsicae's combined `**kern`/`**mens`
  grammar, vendored verbatim in `kern/kernMensSpine*.g4`, so kernpy and mOOsicae read `**mens`
  alike; before, no mensural note parsed. The mensural duration (figure, perfection, coloration,
  dot) is one subtoken as written, ligature and tie marks are kept, custodes, signa congruentiae,
  layout marks and multirests are read. See `docs/concepts/humdrum-mens.md`.
- Round-trip tests over real `**mens` data: the Willi Apel examples of mOOsicae and two SEILS
  files; `KERNPY_MENS_CORPUS=<dir>` runs them over a whole corpus (all 180 `**mens` files of
  SEILS pass).
- CLI: `--recursive` for `--ekern2kern` and `--kern2ekern` on a directory.
- **Signifiers in any order**, as Humdrum allows (Craig Sapp's humlib and Verovio find each one
  anywhere in a token): `**kern` `a4`, `r2`, `cc#8`, `#8cc`, `qc`; `**mens` `s~id`, `aS`, `sa~`, `sa:`.
  The export writes kernpy's canonical order (`4a`, `si~d`). Done in the grammar shared with mOOsicae
  (`kern/kernSpineParser.g4` rule by rule, `kern/kernMensSpine*.g4` verbatim), which reads a `**mens`
  cell from its own entry rule, `startMens`: the spine type decides what `L`, `S`, `M`, `m`, `X`, `u`,
  `p` and `i` mean, and in `**mens` an `L` or `J` after the figure is a beam (`UaL`).
- `+` altera in `**mens`, and `**kern` `z` (sforzando), `,` (breath), `u`/`v` (bowing), `o`
  (harmonic), `H`/`h` (glissando), `R` (unpitched), `Q` (gruppetto) and the user-assignable `@`, `+`,
  `|` as note decorations.
- `test/test_mens_muret.py`: MuRET's own `**mens` semantic encodings (678 staves holding every
  distinct cell of its 9,948) must be read as mOOsicae reads them, note by note;
  `KERNPY_MURET_CSV=<csv>` parses all 9,948. `test/resources/mens/reference/`: `**mens` in Sapp's
  syntax, signifiers in several orders.

### Fixed

- `kp.load`/`kp.loads` with the default `raise_on_errors=False` raised on the first cell the grammar
  rejected, so the documented `(document, errors)` pair never came back. The cell is kept as an
  `ErrorToken` (exported verbatim) and reported in `errors`; with `raise_on_errors=True` a
  `ValueError` is raised.
- `from_measure`/`to_measure` exports lost the opening barline and gained the first token (or the
  whole) of the next measure. They now export exactly the asked measures.
- A null token in a non-`**kern` spine no longer opens a phantom first measure in scores that start
  with `=1`.
- Exports that start in the middle of a score rebuilt a spine split once per resulting spine
  (`*^ *^`) and wrote the columns of spines filtered out by `spine_types`.
- `kp.merge` put the data of one spine under another spine's header when the headers differed and
  `raise_on_header_mismatch=False`; both merge strategies now refuse it with `ValueError`
  (`Document.add` raises `ValueError` too).
- The CLI crashed when converting a directory (`find_files()` took no `recursive` argument).
- A `**mens` perfection mark written after the coloration (`s~id`) was read as a note decoration
  and lost; it is now read as the perfection mark (`si~d`).
- A `**kern` cell was cut short at the first signifier the grammar did not know (`z`, `,`, `u`, `|`,
  `@`...) and the rest of it silently dropped, chord notes included: `(4.GGGz 4.GGz` lost its second
  note. Such cells are read whole now; fixtures that had recorded the loss were updated.
- The parsers never bailed out of their fast SLL prediction (`parser.errHandler` was set, and the
  runtime reads `parser._errHandler`), so SLL's mistakes were recovered silently. Parsing is now the
  standard two stages: SLL bailing at the first error, then full LL, which reports.
