# Token Categories and Filtering

## What Are Token Categories?

When kernpy parses a **kern file, every musical element becomes a token with a semantic category. This categorization system allows you to selectively export, analyze, or filter specific types of musical information.

For example, a single note might contain information about:

- Its pitch (C4, D#5, etc.)
- Its duration (quarter note, dotted eighth, etc.)
- Articulations and decorations (staccato, accent, etc.)
- Performance instructions (pizzicato, tremolo, etc.)

Token categories help you work with each type of information independently.

## The Category Hierarchy

Token categories are organized in a strict hierarchy. Here's the main structure:

```
STRUCTURAL
├── HEADER
└── SPINE_OPERATION

CORE (Musical notes and rests)
├── NOTE_REST
│   ├── NOTE
│   │   ├── PITCH
│   │   ├── DECORATION
│   │   └── ALTERATION
│   ├── REST
│   └── DURATION
├── CHORD
├── EMPTY
└── ERROR

SIGNATURES (Clefs, time/key signatures)
├── CLEF
├── TIME_SIGNATURE
├── METER_SYMBOL
├── KEY_SIGNATURE
└── KEY_TOKEN

ENGRAVED_SYMBOLS
OTHER_CONTEXTUAL
BARLINES
COMMENTS
├── FIELD_COMMENTS
└── LINE_COMMENTS

DYNAMICS (Dynamic markings)
HARMONY (Harmonic analysis)
FINGERING (Fingering instructions)
LYRICS (Text/lyrics)
INSTRUMENTS (Instrument declarations)
IMAGE_ANNOTATIONS
├── BOUNDING_BOXES
└── LINE_BREAK

OTHER
MHXM (Scale degree notation)
ROOT (Root movement analysis)
```

## Common Categories Explained

### CORE

The main musical content:

- `NOTE_REST` — Notes and rests
  - `NOTE` — Pitches, durations, articulations
    - `PITCH` — Pitch information (c, d, e, etc.)
    - `DECORATION` — Articulations (staccato, accent, etc.)
    - `ALTERATION` — Accidentals (#, -, ##, --)
  - `REST` — Silence
  - `DURATION` — Note lengths (4, 8, 16, dotted notes, etc.)
- `CHORD` — Multiple simultaneous pitches
- `EMPTY` — Placeholders or null interpretations
- `ERROR` — Parsing errors

### SIGNATURES

Score-level information:

- `CLEF` — Clef declarations (*clefG2, *clefF4, etc.)
- `TIME_SIGNATURE` — Numerator/denominator of time signature
- `METER_SYMBOL` — Common time (C), cut time (C/), etc.
- `KEY_SIGNATURE` — Key signature (*k[f#c#g#])
- `KEY_TOKEN` — Key center declarations

### DYNAMICS

Dynamic markings: `p`, `f`, `ff`, `ppp`, crescendos, diminuendos, etc.

### HARMONY

Harmonic analysis symbols: Roman numerals, scale degrees, functional labels.

### LYRICS & ANNOTATIONS

- `LYRICS` — Text underlay (words, syllables)
- `FINGERING` — Fingering numbers or positions
- `INSTRUMENTS` — Instrument names and transpositions
- `BOUNDING_BOXES` — Coordinates for image-based scores
- `IMAGE_ANNOTATIONS` — Metadata from optical music recognition

## Using Categories to Filter Exports

### Include Specific Categories

Export only certain types of information:

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Export only pitches and durations
kp.dump(doc, 'pitches_only.krn',
        include={
            kp.TokenCategory.PITCH,
            kp.TokenCategory.DURATION,
            kp.TokenCategory.BARLINES
        })

# Export only with clefs and key signatures
kp.dump(doc, 'signatures_only.krn',
        include={
            kp.TokenCategory.SIGNATURES,
            kp.TokenCategory.BARLINES
        })
```

### Exclude Specific Categories

Export everything except certain types:

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Export without decorations (articulations)
kp.dump(doc, 'no_articulations.krn',
        exclude={kp.TokenCategory.DECORATION})

# Export without dynamics or lyrics
kp.dump(doc, 'no_text.krn',
        exclude={
            kp.TokenCategory.DYNAMICS,
            kp.TokenCategory.LYRICS
        })
```

### Using Pre-defined Category Sets

kernpy provides pre-defined sets for common use cases:

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Export with basic kern information only
kp.dump(doc, 'basic.krn',
        include=kp.BEKERN_CATEGORIES)

# Equivalent to:
# include={STRUCTURAL, CORE, SIGNATURES, BARLINES, IMAGE_ANNOTATIONS}
```

## Hierarchical Matching

The category hierarchy allows flexible filtering. When you include or exclude a parent category, it affects all children:

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Include CORE includes all NOTE, REST, DURATION, CHORD, etc.
kp.dump(doc, 'core_only.krn',
        include={kp.TokenCategory.CORE})

# Include SIGNATURES includes CLEF, TIME_SIGNATURE, KEY_SIGNATURE, etc.
kp.dump(doc, 'signatures.krn',
        include={kp.TokenCategory.SIGNATURES})

# Exclude NOTE_REST excludes PITCH, DECORATION, ALTERATION, REST, DURATION
kp.dump(doc, 'no_notes.krn',
        exclude={kp.TokenCategory.NOTE_REST})
```

## Programmatic Access to Hierarchy

Inspect the token category hierarchy in your code:

```python
import kernpy as kp

# View the hierarchy as a tree
print(kp.TokenCategory.tree())

# Get all categories
all_categories = kp.TokenCategory.all()

# Get immediate children of a category
children = kp.TokenCategory.children(kp.TokenCategory.CORE)

# Check if one category is a child of another
is_child = kp.TokenCategory.is_child(
    child=kp.TokenCategory.PITCH,
    parent=kp.TokenCategory.NOTE
)
```

## Best Practices

1. **Start with parent categories** — Use `CORE`, `SIGNATURES`, `DYNAMICS`, etc. instead of individual leaf categories when possible
2. **Combine include and exclude** — You can use both at the same time for fine-grained control:
   ```python
   kp.dump(doc, 'custom.krn',
           include={kp.TokenCategory.CORE},
           exclude={kp.TokenCategory.DECORATION})
   ```
3. **Understand the hierarchy before filtering** — Use `print(kp.TokenCategory.tree())` to see what children a category has
4. **Test your filters** — Small example files make it easy to verify filtering behavior

## Next Steps

- See [concepts/encodings.md](encodings.md) to understand different export formats (kern, ekern, etc.)
- See [advanced/custom-export.md](../advanced/custom-export.md) for more advanced filtering strategies
- See [guides/transform-documents.md](../guides/transform-documents.md) for practical filtering examples
