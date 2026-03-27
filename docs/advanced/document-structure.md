# Document Structure

Deep dive into kernpy's Document, Spine, Measure, and Token architecture. Understanding these concepts enables advanced workflows and custom processing.

## Document Object

A Document represents a complete Humdrum file with all its musical content and metadata.

### Creating Documents

```python
import kernpy as kp

# Load from file
doc, errors = kp.load('score.krn')

# Load from string
content = """**kern	**kern
*M4/4	*M4/4
4c	4e
=1	=1
*-	*-
"""
doc, errors = kp.loads(content)
```

### Basic Document Properties

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Get basic information
measures = doc.measures_count()
print(f"Total measures: {measures}")

# Get first/last measures
first_measure = doc.get_first_measure()
last_measure = doc.get_last_measure()
print(f"Measures {first_measure} to {last_measure}")

# Count measures in range
measures_in_range = doc.measures_count(from_measure=5, to_measure=20)
print(f"Measures 5-20: {measures_in_range} measures")
```

## Spines

A Spine is a vertical column in a Humdrum file, containing a sequence of tokens for one instrument or data stream.

### Accessing Spines

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Get all spines
spines = doc.get_spines()
print(f"Total spines: {len(spines)}")

# Get spine by index
first_spine = spines[0]
print(f"First spine type: {first_spine.spine_type()}")

# Check specific spine type
for spine in spines:
    if spine.spine_type() == '**kern':
        print(f"Found kern spine")
```

### Spine Types

Humdrum defines many spine types. Common ones in musical scores:

| Spine Type | Content |
|-----------|---------|
| `**kern` | Standard note notation |
| `**mens` | Medieval/Renaissance notation |
| `**dynam` | Dynamics |
| `**harm` | Harmonic analysis |
| `**fing` | Fingering |
| `**text` | Lyrics, text annotation |
| `**time` | Temporal measurements |

### Filtering by Spine Type

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Get only kern spines
kern_spines = [s for s in doc.get_spines() if s.spine_type() == '**kern']
print(f"Found {len(kern_spines)} kern spines")

# Get only dynamics spines
dynam_spines = [s for s in doc.get_spines() if s.spine_type() == '**dynam']
print(f"Found {len(dynam_spines)} dynamics spines")

# Count all spine types
spine_types = {}
for spine in doc.get_spines():
    spine_type = spine.spine_type()
    spine_types[spine_type] = spine_types.get(spine_type, 0) + 1

print("Spine inventory:")
for spine_type, count in spine_types.items():
    print(f"  {spine_type}: {count}")
```

## Tokens

Tokens are the smallest units in Humdrum, representing individual notes, rests, metadata, or other musical information.

### Accessing Tokens

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Get tokens from a spine
spines = doc.get_spines()
spine = spines[0]

tokens = spine.get_tokens()
print(f"Total tokens in first spine: {len(tokens)}")

# Access specific token
first_token = tokens[0]
print(f"First token value: {first_token.value()}")

# Iterate through tokens
for i, token in enumerate(tokens[:10]):
    print(f"Token {i}: {token.value()}")
```

### Token Properties

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

spine = doc.get_spines()[0]
tokens = spine.get_tokens()

# Token categories tell us what kind of information this token contains
for token in tokens[:5]:
    categories = token.get_categories()
    print(f"{token.value()}: {categories}")

# Check specific categories
for token in tokens:
    if kp.TokenCategory.PITCH in token.get_categories():
        print(f"Pitch token: {token.value()}")
    
    if kp.TokenCategory.DURATION in token.get_categories():
        duration = token.duration()
        print(f"Duration: {duration}")

# Check if token is null
if tokens[0].is_null():
    print("First token is null (.)")
```

## Measures

A Measure is a logical grouping of tokens across all spines, typically bounded by barlines.

### Working with Measures

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Get measure boundaries
first_measure = doc.get_first_measure()
last_measure = doc.get_last_measure()
print(f"Measures: {first_measure} to {last_measure}")

# Count measures
total = doc.measures_count()
print(f"Total measures: {total}")

# Get tokens for a specific measure range
# Note: This requires iterating through spines
for spine in doc.get_spines():
    tokens = spine.get_tokens()
    
    # Filter tokens in measure range manually
    measure_tokens = []
    current_measure = 0
    
    for token in tokens:
        if token.value().startswith('='):
            # This is a barline token
            current_measure = int(token.value()[1:])
        
        if current_measure >= 5 and current_measure <= 10:
            measure_tokens.append(token)
```

## Tree Structure Navigation

kernpy documents have an internal tree structure that can be navigated for advanced processing.

### Understanding the Document Tree

```
Document
├── Spine 0 (kern)
│   ├── Token 0
│   ├── Token 1
│   └── ...
├── Spine 1 (kern)
│   ├── Token 0
│   ├── Token 1
│   └── ...
└── Spine 2 (dyn)
    ├── Token 0
    ├── Token 1
    └── ...
```

### Advanced Navigation

```python
import kernpy as kp

doc, _ = kp.load('complex_score.krn')

# Build a map of content
spine_info = []

for spine_idx, spine in enumerate(doc.get_spines()):
    spine_type = spine.spine_type()
    tokens = spine.get_tokens()
    
    # Categorize tokens
    pitches = [t for t in tokens if kp.TokenCategory.PITCH in t.get_categories()]
    rests = [t for t in tokens if t.value() == '.']
    barlines = [t for t in tokens if t.value().startswith('=')]
    
    spine_info.append({
        'index': spine_idx,
        'type': spine_type,
        'total_tokens': len(tokens),
        'pitches': len(pitches),
        'rests': len(rests),
        'barlines': len(barlines),
    })

# Print analysis
for info in spine_info:
    print(f"Spine {info['index']} ({info['type']}): "
          f"{info['pitches']} notes, "
          f"{info['rests']} rests, "
          f"{info['barlines']} barlines")
```

## Extracting Content

### Extract All Pitches from a Document

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

all_pitches = []

for spine in doc.get_spines():
    if spine.spine_type() == '**kern':
        tokens = spine.get_tokens()
        
        for token in tokens:
            if kp.TokenCategory.PITCH in token.get_categories():
                all_pitches.append(token.value())

print(f"Found {len(all_pitches)} pitch events")
print(f"Unique pitches: {len(set(all_pitches))}")
print(f"Most common: {max(set(all_pitches), key=all_pitches.count)}")
```

### Extract Rhythmic Pattern

```python
import kernpy as kp
from fractions import Fraction

doc, _ = kp.load('score.krn')

# Get durations from first kern spine
for spine in doc.get_spines():
    if spine.spine_type() == '**kern':
        tokens = spine.get_tokens()
        
        durations = []
        for token in tokens:
            if kp.TokenCategory.DURATION in token.get_categories():
                try:
                    dur = token.duration()
                    durations.append(dur)
                except:
                    pass
        
        print(f"Rhythmic durations: {durations}")
        break
```

### Extract Metadata

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Find key signature
key_sig = None

for spine in doc.get_spines():
    tokens = spine.get_tokens()
    
    for token in tokens:
        if token.value().startswith('*['):
            # Key signature token
            key_sig = token.value()
            break
    
    if key_sig:
        break

print(f"Key signature: {key_sig}")

# Find time signature
time_sig = None
for spine in doc.get_spines():
    tokens = spine.get_tokens()
    
    for token in tokens:
        if token.value().startswith('*M'):
            time_sig = token.value()
            break
    
    if time_sig:
        break

print(f"Time signature: {time_sig}")
```

## Filtering and Subset Creation

### Create Filtered Document

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Export only specific spines
first_three_spines = kp.dump(
    doc,
    'first_three.krn',
    spine_ids=[0, 1, 2]
)

# Export without decorations
kp.dump(
    doc,
    'no_decorations.krn',
    exclude={kp.TokenCategory.DECORATION}
)

# Export only certain measures
kp.dump(
    doc,
    'measures_10_20.krn',
    from_measure=10,
    to_measure=20
)
```

### Create Document Intersection

```python
import kernpy as kp

# Load two documents
doc1, _ = kp.load('version1.krn')
doc2, _ = kp.load('version2.krn')

# Get common spines (by index)
num_spines = min(len(doc1.get_spines()), len(doc2.get_spines()))

# Extract first N spines from each
common_extent = list(range(num_spines))

kp.dump(doc1, 'common1.krn', spine_ids=common_extent)
kp.dump(doc2, 'common2.krn', spine_ids=common_extent)
```

## Advanced Document Manipulation

### Combine Multiple Documents

```python
import kernpy as kp

# Load documents
doc1, _ = kp.load('soprano.krn')
doc2, _ = kp.load('alto.krn')
doc3, _ = kp.load('tenor.krn')

# Merge spines side-by-side
merged = kp.merge([doc1, doc2, doc3])
kp.dump(merged, 'satb_merged.krn')

# Or concatenate sequentially
concatenated = kp.concat([doc1, doc2, doc3])
kp.dump(concatenated, 'satb_sequential.krn')
```

### Analyze Document Complexity

```python
import kernpy as kp

def analyze_complexity(doc):
    """Quantify document complexity"""
    
    metrics = {
        'num_spines': len(doc.get_spines()),
        'num_measures': doc.measures_count(),
        'total_tokens': 0,
        'spine_types': {},
        'token_categories': {},
    }
    
    for spine in doc.get_spines():
        spine_type = spine.spine_type()
        metrics['spine_types'][spine_type] = metrics['spine_types'].get(spine_type, 0) + 1
        
        tokens = spine.get_tokens()
        metrics['total_tokens'] += len(tokens)
        
        for token in tokens:
            categories = token.get_categories()
            for cat in categories:
                metrics['token_categories'][cat] = metrics['token_categories'].get(cat, 0) + 1
    
    return metrics

# Use it
doc, _ = kp.load('score.krn')
analysis = analyze_complexity(doc)

print(f"Spines: {analysis['num_spines']}")
print(f"Measures: {analysis['num_measures']}")
print(f"Total tokens: {analysis['total_tokens']}")
print(f"Spine types: {analysis['spine_types']}")
```

## Performance Considerations

### Efficient Iteration

```python
import kernpy as kp

doc, _ = kp.load('large_score.krn')

# Cache results when iterating multiple times
spines = doc.get_spines()
spine_count = len(spines)

# More efficient than repeatedly calling doc.get_spines()
for i in range(spine_count):
    spine = spines[i]
    # ... process spine
```

### Memory-Efficient Processing

```python
import kernpy as kp
from pathlib import Path

# Process many files without keeping all in memory
for krn_file in Path('scores').glob('*.krn'):
    doc, _ = kp.load(krn_file)
    
    # Process and export immediately
    result = process_document(doc)
    kp.dump(result, f'output/{krn_file.stem}.krn')
    
    # doc is garbage collected here
    del doc

def process_document(doc):
    """Your processing logic"""
    return doc
```

## Use Cases

### Pattern Finding

```python
import kernpy as kp
from collections import Counter

doc, _ = kp.load('score.krn')

# Find note sequences (bigrams)
sequences = []

for spine in doc.get_spines():
    if spine.spine_type() == '**kern':
        tokens = spine.get_tokens()
        pitches = [t.value() for t in tokens 
                   if kp.TokenCategory.PITCH in t.get_categories()]
        
        # Create bigrams
        for i in range(len(pitches) - 1):
            sequences.append((pitches[i], pitches[i+1]))

# Find most common patterns
counter = Counter(sequences)
print("Most common pitch pairs:")
for pair, count in counter.most_common(10):
    print(f"  {pair}: {count} occurrences")
```

### Statistical Analysis

```python
import kernpy as kp
import statistics

doc, _ = kp.load('score.krn')

# Collect pitch heights
pitch_height_map = {
    'c': 0, 'd': 2, 'e': 4, 'f': 5, 'g': 7, 'a': 9, 'b': 11,
}

heights = []

for spine in doc.get_spines():
    if spine.spine_type() == '**kern':
        tokens = spine.get_tokens()
        
        for token in tokens:
            if kp.TokenCategory.PITCH in token.get_categories():
                # Extract pitch class (C, D, E, etc)
                pitch = token.value()[0].lower()
                if pitch in pitch_height_map:
                    heights.append(pitch_height_map[pitch])

if heights:
    print(f"Average pitch height: {statistics.mean(heights):.1f}")
    print(f"Median: {statistics.median(heights)}")
    print(f"Std dev: {statistics.stdev(heights):.1f}")
```

## See Also

- [Core Concepts: Documents and Spines](../concepts/documents-and-spines.md) — Foundational overview
- [Token Categories](../concepts/token-categories.md) — Understanding token types
- [Parse and Analyze Guide](../guides/parse-and-analyze.md) — Practical analysis patterns
- [Custom Export](custom-export.md) — Advanced filtering strategies
