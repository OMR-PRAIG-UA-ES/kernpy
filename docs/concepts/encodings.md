# Encoding Formats: How kernpy Represents Music

## What Are Encodings?

When kernpy exports a **kern file, it can use different encodings to represent the data. Each encoding has different strengths:

- **Normalized kern:** Standard **kern format compatible with other tools
- **Extended kern (eKern):** Deconstructs tokens to show internal structure
- **Agnostic kern:** Uses a standardized pitch notation independent of clef
- **Basic kern:** Simplified version with core elements only

## Normalized Kern

The standard **kern format used by Humdrum tools. This is the most compatible format and the default for kernpy.

**Characteristics:**

- Single character tokens (e.g., `4c#`, `4..`, `r`)
- Compact and human-readable
- Compatible with Humdrum tools (Verovio, humdrum-tools, etc.)
- Standard choice for publication and archival

**Example:**

```kern
**kern
*M4/4
*clefG2
=1
4c
4d
4e
4f
=2
2g
2cc
==
*-
```

**Use case:** Export for compatibility with other music software and tools.

```python
import kernpy as kp

doc, _ = kp.load('score.krn')
content = kp.dumps(doc, encoding=kp.Encoding.normalizedKern)
```

## Extended Kern (eKern)

Deconstructs each token into individual subtokens, separating pitch, duration, and articulation information. Uses special delimiters (`@` and `·`) to show internal structure.

**Characteristics:**

- Shows all internal components of a token explicitly
- Uses `@` as the main separator and `·` for decorations
- More verbose but reveals the token structure
- Useful for detailed analysis and debugging
- Compatible with eKern tools

**Example:**

```kern
**ekern
*M4/4
*clefG2
=1
4@c
4@d
4@e
4@f
=2
2@g
2@cc
==
*-
```

For a complex note like `4c#L`:

```
Normalized: 4c#L
eKern:      4@c@#·L
            ↓ ↓ ↓ ↓
            dur pitch alt decoration
```

**Use case:** Debug parsing, inspect internal structure, detailed analysis of notation.

```python
import kernpy as kp

doc, _ = kp.load('score.krn')
ekern_content = kp.dumps(doc, encoding=kp.Encoding.eKern)
print(ekern_content)
```

## Agnostic Kern (aKern)

Normalizes pitch representation to be independent of clef. In agnostic kern, the same pitch in the staff always has the same representation, regardless of which clef is active.

**Characteristics:**

- Pitch notation independent of clef context
- Useful for transposition and analysis
- Standardizes pitch across different clefs
- Maps staff positions to absolute pitches

**Example:**

If a note appears on the middle line of a G2 clef (B), it's always represented as B regardless of clef changes.

**Use case:** Analysis workflows where you want pitch-normalized data.

```python
import kernpy as kp

doc, _ = kp.load('score.krn')
akern_content = kp.dumps(doc, encoding=kp.Encoding.agnosticKern)
```

## Basic Kern (bKern)

A simplified version of **kern containing only essential musical information: notes, rests, durations, pitches, and barlines.

**Characteristics:**

- Excludes articulations, decorations, and fancy symbols
- Keeps basic kern pitch and duration information
- Smaller file size
- Useful for simplified analysis

**Use case:** Simplified export for analysis pipelines that don't need detailed articulation information.

```python
import kernpy as kp

doc, _ = kp.load('score.krn')
bkern_content = kp.dumps(doc, encoding=kp.Encoding.bKern)
```

## Basic Extended Kern (beKern)

Combines basic kern structure with extended tokenization (like eKern).

**Use case:** Detailed structure inspection of core musical elements only.

```python
import kernpy as kp

doc, _ = kp.load('score.krn')
bekern_content = kp.dumps(doc, encoding=kp.Encoding.bEkern)
```

## Choosing an Encoding

| Encoding | Use Case | Compatibility | Size | Detail |
|----------|----------|---------------|------|--------|
| **normalizedKern** | Default, compatibility, archival | Highest | Smallest | Standard |
| **eKern** | Debugging, detailed analysis | Medium | Large | Very high |
| **agnosticKern** | Transposition, pitch analysis | Medium | Medium | Standard |
| **basicKern** | Simplified analysis, smaller files | Medium | Smallest | Low |
| **basicExtendedKern** | Structure inspection of core elements | Low | Medium | High (core only) |

## Converting Between Encodings

You can convert files between encodings easily:

```python
import kernpy as kp

# Load in any format
doc, errors = kp.load('score.krn')

# Convert to eKern
kp.dump(doc, 'score.ekrn', encoding=kp.Encoding.eKern)

# Convert from eKern back to normalized kern
doc2, _ = kp.load('score.ekrn')
kp.dump(doc2, 'score_restored.krn', encoding=kp.Encoding.normalizedKern)
```

## Recommended Practices

1. **Default to normalizedKern** — Unless you have a specific reason, use the standard **kern format
2. **Use eKern for analysis** — When you need to understand token structure
3. **Use agnosticKern for transposition** — When working with pitch operations
4. **Combine with filtering** — Use encodings together with token category filtering for fine control

## Next Steps

- See [concepts/token-categories.md](token-categories.md) to filter which tokens to export
- See [advanced/custom-export.md](../advanced/custom-export.md) for advanced encoding strategies
- See [guides/transform-documents.md](../guides/transform-documents.md) for practical examples
