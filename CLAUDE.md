# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

`kernpy` is a Python package for parsing, manipulating, and exporting symbolic music notation in the Humdrum `**kern` and `**mens` formats, oriented toward Optical Music Recognition (OMR) and machine-learning tasks. Parsing of `**kern` spines is driven by an ANTLR4 grammar.

## Commands

```shell
# Install + run tests (uv is the canonical workflow; CI uses it too)
uv sync --group test
uv run pytest test

# Run a single test file / class / case
uv run pytest test/test_exporter.py
uv run pytest test/test_exporter.py::TestClass::test_method

# Tests run with coverage by default (see pytest.ini: --cov=kernpy). Disable with:
uv run pytest test --no-cov

# Build/serve docs
uv sync --group docs
uv run mkdocs serve   # or: uv run mkdocs build

# Run as a CLI module
python -m kernpy --help

# Release: bump version, commit, push; GitHub release publishes to PyPI
uv version --bump patch|minor|major
```

### Regenerating the ANTLR grammar (required after editing the `.g4` files)

The grammar lives in `kern/kernSpineLexer.g4` and `kern/kernSpineParser.g4`. After any grammar change you **must** regenerate the Python parser and commit the result — the generated code is checked in and imported at runtime:

```shell
./antlr4.sh   # requires Java; uses the bundled antlr-4.13.1-complete.jar
```

This writes generated lexer/parser/listener/visitor code into `kernpy/core/generated/`. Do not hand-edit files in that directory.

## Architecture

### Public API layers
There are three layers that wrap the same engine; prefer the topmost when writing new code:

1. **`kernpy.io.public`** — the current public API: `load`/`loads` (file/string → `Document`), `dump`/`dumps` (`Document` → file/string), `graph`, `concat`, `merge`, `spine_types`, `is_monophonic`. These return `(Document, errors)` tuples and accept keyword-only export options.
2. **`kernpy.core.generic.Generic`** — classmethod implementations behind the public API (`read`, `create`, `export`, `store`, `merge`, `concat`, `parse_options_to_ExportOptions`).
3. **Deprecated top-level functions** (`read`, `create`, `export`, `store`, `store_graph`, `get_spine_types` in `generic.py`) — kept for backward compatibility via the `@deprecated` decorator. New code should use the `load`/`loads`/`dump`/`dumps` names instead.

Everything is re-exported at package root, so users write `import kernpy as kp; kp.load(...)`.

### Import pipeline (`**kern` text → `Document`)
- `core/importer.py` `Importer` reads the file row-by-row, building a `MultistageTree` where each row is a "stage". It handles metacomments (`!!`), spine operations (split/join/terminate `*-`), and header rows.
- For each spine column, `core/importer_factory.py::createImporter(spine_type)` dispatches to a per-spine-type importer (`KernSpineImporter`, `MensSpineImporter`, `TextSpineImporter`, `HarmSpineImporter`, `MxhmSpineImporter`, `RootSpineImporter`, `DynSpineImporter`, `DynamSpineImporter`, `FingSpineImporter`). Unknown spine types fall back to `BasicSpineImporter`, which only recognizes structural/basic token categories.
- All spine importers subclass `core/spine_importer.py::SpineImporter` (ABC). `**kern`/`**mens` importers parse individual tokens through the ANTLR-generated lexer/parser in `core/generated/` driven by an ANTLR `Listener` (`base_antlr_spine_parser_listener.py`) and `ErrorListener` (`core/error_listener.py`). Parsing uses `PredictionMode.SLL` + `BailErrorStrategy` for speed.
- Optional duration validation (`raise_on_duration_mismatch`, `meter_signature_fallback_if_not_found`) is enforced via `core/measure_signature_validators.py`.

### Document model (`core/document.py`)
- `Document` wraps a `MultistageTree` of `Node`s (one stage per source row). Most user-facing queries live here: `get_all_tokens`, `get_unique_tokens`, `frequencies`, `get_metacomments`, `measures_count`, `get_first_measure`, iteration (`for measure in doc`), `clone`, `add`, `match`, `to_transposed`, and `page_bounding_boxes`.
- Tree traversals are pluggable via `TraversalFactory` (`MetacommentsTraversal`, `TokensTraversal`).

### Tokens (`core/tokens.py`)
- `Token` hierarchy (`SimpleToken`, `ComplexToken`, `CompoundToken`, `NoteRestToken`, `HeaderToken`, `SpineOperationToken`, etc.) plus `Subtoken`s.
- `TokenCategory` is a hierarchical enum (see `TokenCategory.tree()`); export filtering is done by category. `TokenCategoryHierarchyMapper.valid(include=, exclude=)` resolves an include/exclude set into the concrete leaf categories used by `ExportOptions.token_categories`. `BEKERN_CATEGORIES` is a preset.

### Export pipeline (`Document` → text)
- `core/exporter.py`: `ExportOptions` holds all filters (`spine_types`, `token_categories`, `from_measure`/`to_measure`, `kern_type` encoding, `instruments`, `show_measure_numbers`, `spine_ids`). `Exporter.export_string` walks the tree applying these.
- `core/tokenizers.py::Encoding` (enum) selects the output dialect; `TokenizerFactory` produces the matching `Tokenizer`: `kern`, `extended_kern` (`@`-tokenised), `basic_kern`, `basic_extended_kern`, `agnostic_kern`/`agnostic_extended_kern`. Agnostic encodings place all pitches in G-clef position regardless of the source clef (see `core/gkern.py`, `PositionInStaff`, `Clef` hierarchy).

### Other modules
- `core/transposer.py` + `core/pitch_models.py`: transposition (`Document.to_transposed(interval, direction)`, `AVAILABLE_INTERVALS`), pitch import/export (`HumdrumPitchImporter`/`AmericanPitchImporter`), `AgnosticPitch`.
- `core/graphviz_exporter.py`: dumps the document tree to Graphviz `.dot` for debugging (`kp.graph`).
- `polish_scores/`: dataset downloader (`download_polish_dataset`) + IIIF manifest fetching; exposed through `python -m kernpy --polish`.
- `util/`: `helpers.py` (`@deprecated`), `store_cache.py`.

## Conventions & gotchas

- `core/generated/` and the `kern/` `.tokens` files are build artifacts of `antlr4.sh` — regenerate, don't edit. The repo also contains a top-level `gen/` and `kern/gen/` and `legacy-parsers-not-used/`; the live grammar source is `kern/*.g4`.
- Production dependencies go in `pyproject.toml`; per the contributing notes dev deps are tracked alongside (`requirements.txt` is referenced in older docs, but dependency groups in `pyproject.toml` / `uv.lock` are authoritative).
- Importer functions return a list of grammar `errors` rather than raising by default; pass `raise_on_errors=True` (public API) / `strict=True` (`Generic`) to raise instead.
- Test resources live under `test/resources/`; many tests load `.krn` fixtures from there (e.g. `test/resources/legacy/chor048.krn`).
- Branch from `main` for changes (CI runs pytest on Python 3.9–3.12 for pushes/PRs to `main`).
