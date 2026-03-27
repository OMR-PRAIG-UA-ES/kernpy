# Guide: Transform Documents

Learn how to filter, modify, transpose, and export customized versions of your scores.

## Filter by Spine Type

Keep only the musical information you need:

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Export only kern spines (notes, no lyrics)
kp.dump(doc, 'notes_only.krn',
        spine_types=['**kern'])

# Export kern and text together
kp.dump(doc, 'with_lyrics.krn',
        spine_types=['**kern', '**text'])

# Export all dynamics
kp.dump(doc, 'with_dynamics.krn',
        spine_types=['**kern', '**dynam'])
```

## Filter by Token Category

Control which types of musical information are exported:

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Export without decorations (articulations, such as staccato)
kp.dump(doc, 'no_articulations.krn',
        exclude={kp.TokenCategory.DECORATION})

# Export without dynamics
kp.dump(doc, 'no_dynamics.krn',
        exclude={kp.TokenCategory.DYNAMICS})

# Export only core musical content
kp.dump(doc, 'core_only.krn',
        include={kp.TokenCategory.CORE,
                 kp.TokenCategory.SIGNATURES,
                 kp.TokenCategory.BARLINES})

# Complex: Export pitches and durations only
kp.dump(doc, 'notes_and_durations.krn',
        include={kp.TokenCategory.PITCH,
                 kp.TokenCategory.DURATION,
                 kp.TokenCategory.REST,
                 kp.TokenCategory.BARLINES})
```

## Select Specific Spines by Index

Work with specific instruments or voices:

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Export first two spines
kp.dump(doc, 'soprano_alto.krn',
        spine_ids=[0, 1])

# Export just the middle spine
kp.dump(doc, 'middle.krn',
        spine_ids=[1])

# Export 1st and 3rd spine
kp.dump(doc, 'outer_voices.krn',
        spine_ids=[0, 2])
```

## Select Measure Ranges

Extract specific sections of the score:

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Export first 10 measures
kp.dump(doc, 'intro.krn',
        from_measure=1,
        to_measure=10)

# Export measures 20-40
kp.dump(doc, 'middle_section.krn',
        from_measure=20,
        to_measure=40)

# Export from measure 50 to the end
last_measure = doc.measures_count()
kp.dump(doc, 'ending.krn',
        from_measure=50,
        to_measure=last_measure)
```

## Transpose Pitches

Transposition is one of the most powerful transformations:

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Transpose up a perfect 4th
transposed_up = doc.to_transposed('P4', 'up')
kp.dump(transposed_up, 'transposed_up_P4.krn')

# Transpose down a major 2nd
transposed_down = doc.to_transposed('M2', 'down')
kp.dump(transposed_down, 'transposed_down_M2.krn')

# Common intervals:
# P1 = Unison
# m2/M2 = Minor/Major 2nd
# m3/M3 = Minor/Major 3rd
# P4 = Perfect 4th
# P5 = Perfect 5th
# m6/M6 = Minor/Major 6th
# m7/M7 = Minor/Major 7th
# P8 = Octave
```

### See All Available Intervals

```python
import kernpy as kp

print("Available intervals:")
print(kp.AVAILABLE_INTERVALS)

# Or use in transposition:
doc, _ = kp.load('score.krn')
for interval in kp.AVAILABLE_INTERVALS[:5]:
    transposed = doc.to_transposed(interval, 'up')
    kp.dump(transposed, f'transposed_{interval}.krn')
```

## Combine Multiple Transformations

The real power comes from combining transformations:

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# 1. Keep only kern and text spines
# 2. Remove decorations
# 3. Extract measures 10-20
# 4. Transpose up a major 3rd
doc = doc.to_transposed('M3', 'up')

kp.dump(doc, 'custom.krn',
        spine_types=['**kern', '**text'],
        exclude={kp.TokenCategory.DECORATION},
        from_measure=10,
        to_measure=20)
```

## Change Encoding Format

Export in different formats:

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Normalized kern (standard, default)
kp.dump(doc, 'standard.krn',
        encoding=kp.Encoding.normalizedKern)

# Extended kern (shows token structure)
kp.dump(doc, 'extended.ekrn',
        encoding=kp.Encoding.eKern)

# Agnostic kern (clef-independent pitches)
kp.dump(doc, 'agnostic.akrn',
        encoding=kp.Encoding.agnosticKern)

# Basic kern (simplified, core elements only)
kp.dump(doc, 'basic.krn',
        encoding=kp.Encoding.bKern)
```

## Working with the Full Transformation Pipeline

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Step 1: Load document
print(f"Original: {doc.measures_count()} measures, {len(doc.get_spines())} spines")

# Step 2: Transpose
doc_transposed = doc.to_transposed('P5', 'up')

# Step 3: Export with multiple filters
kp.dump(doc_transposed, 'variation.krn',
        spine_types=['**kern'],
        exclude={kp.TokenCategory.DYNAMICS},
        from_measure=doc.get_first_measure(),
        to_measure=min(doc.measures_count(), doc.get_first_measure() + 25),
        encoding=kp.Encoding.eKern)

print("Transformation complete!")
```

## Practical Workflows

### Create Different Arrangements

```python
import kernpy as kp
from pathlib import Path

doc, _ = kp.load('original.krn')

# Soprano line only
sopranos = doc.get_spines()[0]  # Assuming first spine is soprano
kp.dump(doc, 'soprano_only.krn', spine_ids=[0])

# SATB arrangement
kp.dump(doc, 'full_satb.krn')

# Keyboard score (treble and bass)
# This depends on your specific document structure
kp.dump(doc, 'keyboard.krn', spine_ids=[0, 3])
```

### Generate Transpositions for Different Keys

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Generate versions in multiple keys
keys = [('unison', 'P1'), ('up major 2nd', 'M2'), 
        ('up major 3rd', 'M3'), ('up perfect 4th', 'P4')]

for key_name, interval in keys:
    transposed = doc.to_transposed(interval, 'up')
    kp.dump(transposed, f'transposed_{key_name.replace(" ", "_")}.krn')

print("Transposition variations created!")
```

### Simplify Complex Scores

```python
import kernpy as kp

doc, _ = kp.load('complex_score.krn')

# Remove all articulations and dynamics
kp.dump(doc, 'simplified.krn',
        exclude={
            kp.TokenCategory.DECORATION,
            kp.TokenCategory.DYNAMICS,
            kp.TokenCategory.FINGERING
        })
```

### Create Study Scores

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Extract a section with specific instruments
measures = (doc.get_first_measure(), doc.get_first_measure() + 8)

kp.dump(doc, 'study_excerpt.krn',
        spine_types=['**kern'],  # Notes only
        from_measure=measures[0],
        to_measure=measures[1])
```

## String Export

Get transformed content as a string:

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Export as string with transformations
content = kp.dumps(doc,
                   spine_types=['**kern'],
                   encoding=kp.Encoding.eKern)

print(content)

# Or save to a variable and process further
lines = content.split('\n')
filtered_lines = [l for l in lines if not l.startswith('*')]
```

## Summary

You now know how to:

1. Filter spines and tokens by type or category
2. Select specific measures
3. Transpose pitches in different intervals
4. Change encoding formats
5. Combine multiple transformations
6. Create variations and arrangements

## Next Steps

- **Build batch workflows?** — See [Build Pipelines](build-pipelines.md)
- **Learn about token categories?** — See [Token Categories](../concepts/token-categories.md)
- **Understand encodings better?** — See [Encodings](../concepts/encodings.md)
