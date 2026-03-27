# Transposition

Advanced transposition capabilities in kernpy, including interval notation, batch transposition, and complex key changes.

## What is Transposition?

Transposition is the process of moving all pitches in a musical piece up or down by a fixed interval. kernpy provides powerful transposition tools supporting all common intervals.

## Interval Notation

kernpy uses **Humdrum interval notation** for transposition. Intervals consist of:

1. **Quality**: Major (M), minor (m), Perfect (P), Augmented (A), Diminished (d)
2. **Direction**: Positive for up, negative for down
3. **Semitones**: The actual pitch movement

### Common Intervals (Ascending)

| Interval | Semitones | Example Use |
|----------|-----------|-------------|
| P1 | 0 | Unison (no change) |
| m2 | 1 | Half step up |
| M2 | 2 | Whole step up |
| m3 | 3 | Minor third up |
| M3 | 4 | Major third up |
| P4 | 5 | Perfect fourth up |
| A4 | 6 | Augmented fourth (tritone) up |
| P5 | 7 | Perfect fifth up |
| m6 | 8 | Minor sixth up |
| M6 | 9 | Major sixth up |
| m7 | 10 | Minor seventh up |
| M7 | 11 | Major seventh up |
| P8 | 12 | Octave up |
| M9 | 14 | Major ninth up |
| M10 | 16 | Major tenth up |

## Basic Transposition

### Transpose Up

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Transpose up by a perfect fourth
transposed = doc.to_transposed('P4', 'up')

# Transpose up by a major second
transposed = doc.to_transposed('M2', 'up')
```

### Transpose Down

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Transpose down by a perfect fifth
transposed = doc.to_transposed('P5', 'down')

# Transpose down by a minor third
transposed = doc.to_transposed('m3', 'down')
```

### Generate All 12 Transpositions

```python
import kernpy as kp
from pathlib import Path

doc, _ = kp.load('score.krn')

# All chromatic transpositions
intervals = [
    'P1',   # C (original)
    'M2',   # D
    'M3',   # E
    'P4',   # F
    'A4',   # F#/Gb
    'P5',   # G
    'M6',   # A
    'm7',   # Bb
    'P8',   # C (octave)
]

output_dir = Path('transpositions')
output_dir.mkdir(exist_ok=True)

for interval in intervals:
    transposed = doc.to_transposed(interval, 'up')
    pitch_name = ['C', 'D', 'E', 'F', 'F#', 'G', 'A', 'Bb', 'C'][intervals.index(interval)]
    kp.dump(transposed, output_dir / f'score_{pitch_name}.krn')
    print(f"Created score_{pitch_name}.krn")
```

## Common Transposition Scenarios

### Transposing for Different Concert Pitches

Musical transposition is often needed to match different instruments:

```python
import kernpy as kp

doc, _ = kp.load('original.krn')

transposition_map = {
    'C': 'P1',       # Concert pitch
    'Bb': 'M2',      # Bb instrument
    'Eb': 'm6',      # Eb instrument
    'F': 'P4',       # F instrument
}

for concert_pitch, interval in transposition_map.items():
    transposed = doc.to_transposed(interval, 'up')
    kp.dump(transposed, f'for_{concert_pitch}.krn')
```

### Modulation (Key Changes)

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Modulate from C major to G major (up a perfect fifth)
modulated = doc.to_transposed('P5', 'up')
kp.dump(modulated, 'modulated_to_G.krn')

# Modulate to D major (up a major second)
modulated = doc.to_transposed('M2', 'up')
kp.dump(modulated, 'modulated_to_D.krn')
```

### Creating Transposition Sets

```python
import kernpy as kp
from pathlib import Path

def create_transposition_set(score_file, output_dir='transpositions'):
    """
    Create transpositions in all 12 keys from a given score.
    """
    doc, _ = kp.load(score_file)
    
    Path(output_dir).mkdir(exist_ok=True)
    
    keys = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
    intervals = ['P1', 'A1', 'M2', 'm3', 'M3', 'P4', 'A4', 'P5', 'm6', 'M6', 'm7', 'M7']
    
    for key, interval in zip(keys, intervals):
        transposed = doc.to_transposed(interval, 'up')
        output_file = f'{Path(score_file).stem}_in_{key}.krn'
        kp.dump(transposed, f'{output_dir}/{output_file}')
        print(f"Created {output_file}")

# Use it
create_transposition_set('cantus.krn', output_dir='all_keys')
```

## Batch Transposition

### Transpose Multiple Files

```python
import kernpy as kp
from pathlib import Path

score_dir = Path('scores')

# Transpose all files up by a perfect fourth
for score_file in score_dir.glob('*.krn'):
    doc, errors = kp.load(score_file)
    if errors:
        print(f"Skipping {score_file.name} due to errors")
        continue
    
    transposed = doc.to_transposed('P4', 'up')
    output_file = f'transposed/{score_file.stem}_p4.krn'
    kp.dump(transposed, output_file)
    print(f"Transposed {score_file.name}")
```

### Parallel Transposition

```python
from multiprocessing import Pool
import kernpy as kp
from pathlib import Path

def transpose_single_file(args):
    """Worker function for parallel processing"""
    filepath, interval = args
    doc, _ = kp.load(filepath)
    transposed = doc.to_transposed(interval, 'up')
    output = f'transposed/{Path(filepath).stem}_{interval}.krn'
    kp.dump(transposed, output)
    return f"Processed {filepath.name}"

# Create work list
interval = 'M2'
files = [(str(f), interval) for f in Path('scores').glob('*.krn')]

# Process in parallel
with Pool(4) as pool:
    results = pool.map(transpose_single_file, files)
    for result in results:
        print(result)
```

## Advanced Transposition Patterns

### Transpose with Filtering

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Transpose and remove decorations
transposed = doc.to_transposed('P5', 'up')

kp.dump(
    transposed,
    'output.krn',
    exclude={kp.TokenCategory.DECORATION}
)
```

### Transpose Specific Spines Only

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Load, transpose, then export only kern spines
transposed = doc.to_transposed('P4', 'up')

kp.dump(
    transposed,
    'kern_only_transposed.krn',
    spine_types=['**kern']
)
```

### Transpose with Measure Selection

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Transpose and export only measures 10-30
transposed = doc.to_transposed('M3', 'up')

kp.dump(
    transposed,
    'measures_10_30_transposed.krn',
    from_measure=10,
    to_measure=30
)
```

## Interval Calculation Helper

Create a utility function to help with interval calculations:

```python
import kernpy as kp

def transpose_diatonic_steps(doc, steps, direction='up'):
    """
    Transpose by diatonic steps (1-7).
    
    steps=1 means second (M2), steps=4 means fourth (P4), etc.
    """
    # Interval mapping (diatonic steps to kernpy intervals)
    diatonic_intervals = {
        1: 'M2',   # Second
        2: 'M3',   # Third
        3: 'P4',   # Fourth
        4: 'P5',   # Fifth
        5: 'M6',   # Sixth
        6: 'M7',   # Seventh
        7: 'P8',   # Octave
    }
    
    if steps not in diatonic_intervals:
        raise ValueError(f"Steps must be 1-7, got {steps}")
    
    interval = diatonic_intervals[steps]
    return doc.to_transposed(interval, direction)

# Usage
doc, _ = kp.load('score.krn')

# Transpose up by third
result = transpose_diatonic_steps(doc, steps=2, direction='up')
kp.dump(result, 'up_by_third.krn')

# Transpose down by fifth
result = transpose_diatonic_steps(doc, steps=4, direction='down')
kp.dump(result, 'down_by_fifth.krn')
```

## Limitations and Edge Cases

### Chromatic Alterations

Transposition preserves chromatic alterations (sharps, flats, naturals):

```python
import kernpy as kp

doc, _ = kp.load('with_accidentals.krn')

# Sharps and flats are preserved when transposing
transposed = doc.to_transposed('M2', 'up')

kp.dump(transposed, 'transposed_with_accidentals.krn')
```

### Microtones

kernpy supports microtone notation in transposition:

```python
import kernpy as kp

doc, _ = kp.load('microtones.krn')

# Microtones are preserved
transposed = doc.to_transposed('P4', 'up')

kp.dump(transposed, 'transposed_microtones.krn')
```

### Non-Pitched Material

Non-pitched elements (rests, text, time signatures) are preserved:

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Rests and other non-pitched notes remain unchanged
transposed = doc.to_transposed('P5', 'up')

kp.dump(transposed, 'transposed_with_preservation.krn')
```

## Performance Considerations

For large batch transpositions:

```python
import kernpy as kp
from pathlib import Path
from multiprocessing import Pool

def process_batch(batch_size=100):
    """Process files in batches to manage memory"""
    files = list(Path('scores').glob('*.krn'))
    
    for i in range(0, len(files), batch_size):
        batch = files[i:i+batch_size]
        
        for filepath in batch:
            doc, _ = kp.load(filepath)
            transposed = doc.to_transposed('P4', 'up')
            kp.dump(transposed, f'transposed/{filepath.stem}.krn')
        
        print(f"Processed {min(i+batch_size, len(files))}/{len(files)} files")

process_batch(batch_size=50)
```

## Use Cases

### Adapting Music for Different Voicings

```python
import kernpy as kp

original = 'original_treble.krn'
doc, _ = kp.load(original)

# Create versions for different instruments
instruments = {
    'soprano': ('P1', 'up'),
    'alto': ('P4', 'down'),
    'tenor': ('M3', 'down'),
    'bass': ('P8', 'down'),
}

for voice, (interval, direction) in instruments.items():
    transposed = doc.to_transposed(interval, direction)
    kp.dump(transposed, f'{voice}_part.krn')
```

### Creating Transposition Exercises

```python
import kernpy as kp
from pathlib import Path

def create_exercise_set(melody_file, workout_dir='transposition_exercises'):
    """Create transposition exercises in all 12 keys"""
    doc, _ = kp.load(melody_file)
    
    Path(workout_dir).mkdir(exist_ok=True)
    
    intervals = ['P1', 'M2', 'M3', 'P4', 'A4', 'P5', 'M6', 'm7', 'P8', 'M9', 'M10', 'M11']
    
    for i, interval in enumerate(intervals, 1):
        transposed = doc.to_transposed(interval, 'up')
        kp.dump(transposed, f'{workout_dir}/exercise_{i:02d}_{interval}.krn')

# Create exercises
create_exercise_set('melody.krn')
```

## See Also

- [Transform Documents Guide](../guides/transform-documents.md) — More on document manipulation
- [Build Pipelines Guide](../guides/build-pipelines.md) — Batch processing patterns
- [Encoding Concepts](../concepts/encodings.md) — Different output formats
