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
- A `**mens` perfection mark written after the coloration (`s~id`, the grammar wants `si~d`) was
  read as a note decoration and lost; it is now reported as an error.

### Known gaps

- Pitch-first `**kern` tokens (`a4`, `r2`) are rejected by the grammar shared with mOOsicae; the
  tests that want them accepted are `expectedFailure` until both libraries decide.
