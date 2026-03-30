# Code Examples

A collection of ready-to-use code snippets organized by task. Copy and paste these examples into your projects.

## Installation and Setup

### Basic Installation

```python
# Install kernpy
# bash: pip install kernpy

import kernpy as kp
print(f"Using kernpy version {kp.__version__}")
```

## Loading and Inspecting

### Load from File

```python
import kernpy as kp

doc, errors = kp.load('score.krn')
print(f"Loaded document with {doc.measures_count()} measures")
print(f"Found {len(errors)} parsing issues" if errors else "No errors")
```

### Load from String

```python
import kernpy as kp

content = """**kern	**kern
*M4/4	*M4/4
*c:	*c:
4c	4e
4d	4f
4e	4g
4f	4a
=1	=1
*-	*-
"""

doc, errors = kp.loads(content)
print(f"Loaded {doc.measures_count()} measures")
```

### Inspect Document Structure

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Basic info
print(f"Measures: {doc.measures_count()}")
print(f"Spines: {len(doc.get_spines())}")

# List spine types
spines = doc.get_spines()
for i, spine in enumerate(spines):
    spine_type = spine.spine_type()
    print(f"Spine {i}: {spine_type}")
```

### Print Musical Content

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Get first measure
measure = doc.get_first_measure()
print(f"First measure number: {measure}")

# Access spines
spines = doc.get_spines()
for spine in spines:
    tokens = spine.get_tokens()
    print(f"First 5 tokens: {[t.value() for t in tokens[:5]]}")
```

## Token Filtering

### Keep Only Pitch Information

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Export with only pitch information
kp.dump(
    doc,
    'pitches_only.krn',
    include={kp.TokenCategory.PITCH}
)
```

### Remove Decorations and Articulations

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Remove ornaments, articulations, etc
kp.dump(
    doc,
    'no_decorations.krn',
    exclude={kp.TokenCategory.DECORATION}
)
```

### Complex Filtering

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Keep core music elements: notes, rests, time signatures, key signatures
kp.dump(
    doc,
    'core_only.krn',
    include={
        kp.TokenCategory.CORE,
        kp.TokenCategory.SIGNATURES,
        kp.TokenCategory.BARLINES
    }
)
```

### Use Predefined Filters

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Use built-in filter sets
kp.dump(doc, 'output.krn', include=kp.BEKERN_CATEGORIES)
```

## Spine Operations

### Extract Single Instrument

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Keep only **kern spines (melody/harmony)
kp.dump(doc, 'kern_only.krn', spine_types=['**kern'])
```

### Extract Multiple Specific Spines

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Keep first two spines only
kp.dump(doc, 'first_two.krn', spine_ids=[0, 1])
```

### Analyze All Spines

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

spines = doc.get_spines()
for idx, spine in enumerate(spines):
    spine_type = spine.spine_type()
    tokens = spine.get_tokens()
    non_null = [t for t in tokens if t.value() != '.']
    print(f"Spine {idx} ({spine_type}): {len(non_null)} active tokens")
```

## Transposition

### Transpose Up by Perfect 4th

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

transposed = doc.to_transposed('P4', 'up')
kp.dump(transposed, 'transposed_up_p4.krn')
```

### Transpose Down by Major 2nd

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

transposed = doc.to_transposed('M2', 'down')
kp.dump(transposed, 'transposed_down_m2.krn')
```

### Generate All 12 Transpositions

```python
import kernpy as kp
from pathlib import Path

doc, _ = kp.load('score.krn')

intervals = ['P1', 'M2', 'M3', 'P4', 'A4', 'P5', 'M6', 'M7',
             'm2', 'm3', 'm6', 'm7']

for interval in intervals:
    transposed = doc.to_transposed(interval, 'up')
    kp.dump(transposed, f'transposed_{interval}.krn')
    print(f"Created transposed_{interval}.krn")
```

## Measure Operations

### Extract Measure Range

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Export only measures 5-20
kp.dump(doc, 'measures_5_20.krn', from_measure=5, to_measure=20)
```

### Extract First N Measures

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Export first 10 measures
kp.dump(doc, 'first_10.krn', to_measure=10)
```

## Export Formats

### Export as Extended Kern (ekern)

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

kp.dump(doc, 'output.ekrn', encoding=kp.Encoding.eKern)
```

### Export as Agnostic Format

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

kp.dump(doc, 'output_agnostic.txt', encoding=kp.Encoding.agnosticKern)
```

### Get String Instead of File

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Export as string
output = kp.dumps(doc)
print(output)
```

## Batch Processing

### Process Multiple Files

```python
import kernpy as kp
from pathlib import Path

krn_files = Path('scores').glob('*.krn')

for filepath in krn_files:
    doc, errors = kp.load(filepath)
    if not errors:
        transposed = doc.to_transposed('M2', 'up')
        kp.dump(transposed, filepath.stem + '_transposed.krn')
    print(f"Processed {filepath.name}")
```

### Batch Conversion

```python
import kernpy as kp
from pathlib import Path

# Convert all **kern files to ekern
for krn_file in Path('input').glob('*.krn'):
    doc, _ = kp.load(krn_file)
    kp.dump(doc, f'output/{krn_file.stem}.ekrn', encoding=kp.Encoding.eKern)
    print(f"Converted {krn_file.name}")
```

### Parallel Processing

```python
from multiprocessing import Pool
import kernpy as kp
from pathlib import Path

def process_file(filepath):
    doc, _ = kp.load(filepath)
    transposed = doc.to_transposed('P4', 'up')
    output = f'transposed/{Path(filepath).stem}.krn'
    kp.dump(transposed, output)
    return f"Processed {filepath}"

files = list(Path('scores').glob('*.krn'))
with Pool(4) as pool:
    results = pool.map(process_file, files)
    for result in results:
        print(result)
```

## Analysis Patterns

### Count Pitches in Score

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

pitch_counts = {}
spines = doc.get_spines()

for spine in spines:
    if spine.spine_type() == '**kern':
        tokens = spine.get_tokens()
        for token in tokens:
            if kp.TokenCategory.PITCH in token.get_categories():
                pitch = token.value()
                pitch_counts[pitch] = pitch_counts.get(pitch, 0) + 1

print("Pitch distribution:")
for pitch, count in sorted(pitch_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"  {pitch}: {count}")
```

### Calculate Total Duration

```python
import kernpy as kp
from fractions import Fraction

doc, _ = kp.load('score.krn')

total_duration = Fraction(0)

for spine in doc.get_spines():
    if spine.spine_type() == '**kern':
        tokens = spine.get_tokens()
        for token in tokens:
            if kp.TokenCategory.DURATION in token.get_categories():
                try:
                    duration = token.duration()
                    total_duration += duration
                except:
                    pass

print(f"Total duration: {float(total_duration)} beats")
```

### Find Time Signatures

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

time_sigs = []
for spine in doc.get_spines():
    tokens = spine.get_tokens()
    for token in tokens:
        if token.value().startswith('*M'):
            time_sigs.append(token.value())
            break

print(f"Time signatures found: {list(set(time_sigs))}")
```

### Extract All Notes as List

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

notes = []
for spine in doc.get_spines():
    if spine.spine_type() == '**kern':
        tokens = spine.get_tokens()
        for token in tokens:
            if kp.TokenCategory.PITCH in token.get_categories():
                notes.append(token.value())

print(f"Found {len(notes)} notes")
print(f"First 20: {notes[:20]}")
```

## Document Manipulation

### Concatenate Multiple Files

```python
import kernpy as kp

doc1, _ = kp.load('score1.krn')
doc2, _ = kp.load('score2.krn')

# Concatenate documents
combined = kp.concat([doc1, doc2])
kp.dump(combined, 'combined.krn')
```

### Merge Documents

```python
import kernpy as kp

with open('melody.krn', 'r') as f:
    doc1_content = f.read()
with open('harmony.krn', 'r') as f:
    doc2_content = f.read()

# Merge side-by-side
merged_doc, merge_indexes = kp.merge([doc1_content, doc2_content])
kp.dump(merged_doc, 'merged.krn')
print(merge_indexes)
```

## Visualization

### Create Score Graph

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Generate graphviz visualization
kp.graph(doc, 'output.png')
print("Graph saved to output.png")
```

## Error Handling

### Robust File Loading

```python
import kernpy as kp
from pathlib import Path

def safe_load(filepath):
    try:
        doc, errors = kp.load(filepath)
        if errors:
            print(f"Warnings in {filepath}:")
            for error in errors[:3]:  # Show first 3 errors
                print(f"  - {error}")
        return doc
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return None
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None

# Use it
doc = safe_load('score.krn')
if doc:
    print(f"Successfully loaded: {doc.measures_count()} measures")
```

### Batch Processing with Error Recovery

```python
import kernpy as kp
from pathlib import Path

results = {'success': [], 'failed': []}

for filepath in Path('scores').glob('*.krn'):
    try:
        doc, errors = kp.load(filepath)
        # Process...
        results['success'].append(filepath.name)
    except Exception as e:
        results['failed'].append((filepath.name, str(e)))

print(f"Success: {len(results['success'])}")
print(f"Failed: {len(results['failed'])}")
for filename, error in results['failed'][:5]:
    print(f"  {filename}: {error}")
```

## CLI Usage

### Convert kern to ekern

```bash
python -m kernpy --kern2ekern score.krn score.ekrn
```

### Batch Conversion

```bash
python -m kernpy --kern2ekern *.krn
```

### Convert with Output Directory

```bash
python -m kernpy --kern2ekern scores/*.krn -o output/
```

## Next Steps

- See [Practical Guides](guides/parse-and-analyze.md) for detailed tutorials
- Check [API Reference](reference.md) for all available functions
- Visit [Advanced Topics](advanced/transposition.md) for sophisticated workflows
- Ask questions in [FAQ](faq.md) if something isn't clear
