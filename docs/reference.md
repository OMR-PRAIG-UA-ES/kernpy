# API Reference

Complete reference for kernpy's public API. Use Ctrl+F / Cmd+F to search for specific functions and classes.

## LLM Skill Endpoint

Need machine-readable docs for assistants and pipelines?

- Skill page: [Skill Endpoint](skill.md)
- Plain text endpoint: [/skill/kernpy-docs.txt](skill/kernpy-docs.txt)
- Download artifact name: `kernpy-skills.md`

## API

These are the primary functions you should use for loading and exporting Humdrum **kern files.

### Loading

#### `kp.load(filename) -> (Document, List[Error])`

Load a **kern file from disk.

**Parameters:**
- `filename` (str | Path) — Path to the file
- `raise_on_duration_mismatch` (bool) — If `True`, raises `ValueError` when a measure duration does not match the active meter signature
- `meter_signature_fallback_if_not_found` (str | None) — Fallback time signature (for example `*M4/4`) when the measure has no explicit signature

**Returns:**
- Tuple of (Document object, list of error messages)

**Example:**
```python
import kernpy as kp

doc, errors = kp.load('score.krn')
if errors:
    print(f"Found {len(errors)} issues but loaded {doc.measures_count()} measures")
```

#### `kp.loads(content) -> (Document, List[Error])`

Load a **kern document from a string.

**Parameters:**
- `content` (str) — Humdrum **kern content as string
- `raise_on_duration_mismatch` (bool) — If `True`, raises `ValueError` when a measure duration does not match the active meter signature
- `meter_signature_fallback_if_not_found` (str | None) — Fallback time signature (for example `*M4/4`) when the measure has no explicit signature

**Returns:**
- Tuple of (Document object, list of error messages)

**Example:**
```python
import kernpy as kp

krn_string = """**kern
*M4/4
4c
*-
"""

doc, errors = kp.loads(krn_string)
```

### Exporting

#### `kp.dump(doc, filename, **options)`

Export a Document to a file on disk.

**Parameters:**
- `doc` (Document) — The document to export
- `filename` (str | Path) — Output file path
- `**options` — See options below

**Options:**
- `encoding` (Encoding) — Output format (default: `Encoding.normalizedKern`)
- `spine_types` (List[str]) — Keep only specific spine types (e.g., `['**kern']`)
- `spine_ids` (List[int]) — Keep only spines by index
- `include` (Set[TokenCategory]) — Keep only tokens in these categories
- `exclude` (Set[TokenCategory]) — Remove tokens in these categories
- `from_measure` (int) — Starting measure number
- `to_measure` (int) — Ending measure number

**Example:**
```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Export as extended kern
kp.dump(doc, 'output.ekrn', encoding=kp.Encoding.eKern)

# Export without decorations
kp.dump(doc, 'simple.krn', exclude={kp.TokenCategory.DECORATION})

# Export measures 10-20
kp.dump(doc, 'section.krn', from_measure=10, to_measure=20)
```

#### `kp.dumps(doc, **options) -> str`

Export a Document as a string.

**Parameters:**
- `doc` (Document) — The document to export
- `**options` — Same as `dump()`

**Returns:**
- String containing the exported document

**Example:**
```python
import kernpy as kp

doc, _ = kp.load('score.krn')

content = kp.dumps(doc)
print(content)

# Save to file manually
with open('output.krn', 'w') as f:
    f.write(content)
```

### Document Operations

#### `kp.concat(documents) -> Document`

Concatenate multiple documents sequentially.

**Parameters:**
- `documents` (List[Document]) — Documents to concatenate

**Returns:**
- New combined Document

**Example:**
```python
import kernpy as kp

doc1, _ = kp.load('part1.krn')
doc2, _ = kp.load('part2.krn')

combined = kp.concat([doc1, doc2])
kp.dump(combined, 'both_parts.krn')
```

#### `kp.merge(documents) -> Document`

Merge multiple documents side-by-side (combine spines).

**Parameters:**
- `documents` (List[Document]) — Documents to merge

**Returns:**
- New merged Document

**Example:**
```python
import kernpy as kp

soprano, _ = kp.load('soprano.krn')
alto, _ = kp.load('alto.krn')

merged = kp.merge([soprano, alto])
kp.dump(merged, 'sa.krn')
```

### Visualization

#### `kp.graph(doc, output_file)`

Generate a tree visualization of the document structure.

**Parameters:**
- `doc` (Document) — Document to visualize
- `output_file` (str | Path) — Output image file path (.png, .pdf, etc)

**Example:**
```python
import kernpy as kp

doc, _ = kp.load('score.krn')
kp.graph(doc, 'document_structure.png')
```

## Document Class

Main class representing a Humdrum document.

### Properties and Methods

#### `doc.get_spines() -> List[Spine]`

Get all spines in the document.

**Example:**
```python
spines = doc.get_spines()
for spine in spines:
    print(spine.spine_type())
```

#### `doc.measures_count(from_measure=None, to_measure=None) -> int`

Get the number of measures.

**Example:**
```python
total = doc.measures_count()  # All measures
section = doc.measures_count(from_measure=5, to_measure=20)  # Range
```

#### `doc.get_first_measure() -> int`

Get the first measure number.

#### `doc.get_last_measure() -> int`

Get the last measure number.

#### `doc.to_transposed(interval, direction) -> Document`

Return a transposed version of the document.

**Parameters:**
- `interval` (str) — Interval code (e.g., 'P4', 'M2', 'P5')
- `direction` (str) — 'up' or 'down'

**Returns:**
- New transposed Document

**Example:**
```python
# Transpose up by perfect fourth
transposed = doc.to_transposed('P4', 'up')

# Transpose down by major third
transposed = doc.to_transposed('M3', 'down')
```

See [Transposition Guide](advanced/transposition.md) for all interval codes.

## Spine Class

Represents a vertical column in a Humdrum document.

#### `spine.spine_type() -> str`

Get the spine type (e.g., '**kern', '**dynam', '**text').

#### `spine.get_tokens() -> List[Token]`

Get all tokens in the spine.

## Token Class

Represents a single token (cell) in a Humdrum document.

#### `token.value() -> str`

Get the token's string value.

#### `token.get_categories() -> Set[TokenCategory]`

Get the semantic categories of this token.

**Example:**
```python
if kp.TokenCategory.PITCH in token.get_categories():
    print(f"This is a pitch token: {token.value()}")
```

#### `token.duration() -> Fraction`

Get the duration of this token (if applicable).

**Returns:**
- Fraction object representing the duration (e.g., Fraction(1, 4) for quarter note)

#### `token.is_null() -> bool`

Check if token is null (represented as '.').

## Token Categories

Use these with `include` and `exclude` parameters for filtering.

```python
include={kp.TokenCategory.PITCH}
exclude={kp.TokenCategory.DECORATION}
```

See [Token Categories Concept Guide](concepts/token-categories.md) for detailed explanations and use cases.

**Common categories:**
- `PITCH` — Note pitches
- `DURATION` — Note durations
- `CORE` — Core musical tokens
- `SIGNATURES` — Key and time signatures
- `BARLINES` — Measure markers
- `DECORATION` — Articulations, ornaments
- `DYNAMICS` — Dynamic markings
- `ORNAMENT` — Ornamental notes

## Encodings

Use with the `encoding` parameter in `dump()` and `dumps()`.

```python
kp.dump(doc, 'output.ekrn', encoding=kp.Encoding.eKern)
```

**Available encodings:**
- `Encoding.normalizedKern` (default) — Standard, human-readable format
- `Encoding.eKern` — Extended format showing internal structure
- `Encoding.agnosticKern` — Simplified, portable format
- `Encoding.basicKern` — Minimal format
- `Encoding.basicExtendedKern` — Basic extended format

See [Encodings Concept Guide](concepts/encodings.md) for detailed comparisons and use cases.

## Common Collections

### `kp.BEKERN_CATEGORIES`

Pre-defined set of token categories for basic kern export.

**Example:**
```python
# Export with standard categories
kp.dump(doc, 'output.krn', include=kp.BEKERN_CATEGORIES)
```

---

## ⚠️ Deprecated API (Legacy)

The following functions are **deprecated** and will be removed in a future version. Use the modern API instead.

### Deprecated Functions

| Old Function | Modern Replacement | Migration |
|--------------|-------------------|-----------|
| `read()` | `load()` | Change `read(file)` → `load(file)` |
| `create()` | `loads()` | Change `create(string)` → `loads(string)` |
| `export()` | `dumps()` | Change `export(doc)` → `dumps(doc)` |
| `store()` | `dump()` | Change `store(doc, file)` → `dump(doc, file)` |

### Migration Examples

**Old (Deprecated):**
```python
from kernpy.core import HumdrumImporter

importer = HumdrumImporter()
doc = importer.import_file('score.krn')
exporter = ...
exporter.export(doc, 'output.krn')
```

**New (Modern):**
```python
import kernpy as kp

doc, errors = kp.load('score.krn')
kp.dump(doc, 'output.krn')
```

The old API is still functional but **will not receive updates** and may be removed in kernpy 2.0. Please migrate your code to the modern API.

### Why Migrate?

1. **Simpler** — Fewer imports, cleaner code
2. **Error Handling** — Returns error list instead of exceptions
3. **Flexible** — Modern API has more options (filtering, encoding, etc)
4. **Future-Proof** — Old API will be removed eventually

---

## Detailed Documentation

- **[Core Concepts](concepts/humdrum-kern.md)** — What is **kern?
- **[Token Categories](concepts/token-categories.md)** — Understanding token types
- **[Encodings](concepts/encodings.md)** — Different output formats
- **[Practical Guides](guides/parse-and-analyze.md)** — How to accomplish tasks
- **[Advanced Topics](advanced/transposition.md)** — Deep-dive subjects

---

## Generated API Documentation

::: kernpy

## Modules

::: kernpy.core

::: kernpy.util




