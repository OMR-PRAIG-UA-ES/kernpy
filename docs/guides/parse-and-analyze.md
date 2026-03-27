# Guide: Parse and Analyze

Learn how to load **kern files, inspect their structure, and extract musical information for analysis.

## Loading Files

### Load from Disk

The most common use case—loading a **kern file from your file system:

```python
import kernpy as kp

document, errors = kp.load('path/to/score.krn')

# Handle any parsing errors
if errors:
    print(f"Parser found {len(errors)} issues:")
    for error in errors[:3]:  # Show first 3
        print(f"  {error}")
```

### Load from a String

Useful for working with small **kern snippets or data from APIs:

```python
import kernpy as kp

kern_data = """**kern    **text
*M4/4     *
=1        =1
4c        Do
4d        Re
4e        Mi
4f        Fa
=2        =2
2g        Sol
*-        *-
"""

document, errors = kp.loads(kern_data)
```

### Load with Error Handling

Control how strict the parser should be:

```python
import kernpy as kp

# Tolerant parsing (default)—ignores minor issues
doc, errors = kp.load('score.krn', raise_on_errors=False)

# Strict parsing—raises exception on any error
try:
    doc, errors = kp.load('score.krn', raise_on_errors=True)
except ValueError as e:
    print(f"Parsing failed: {e}")
```

## Understanding Document Structure

### Access Spines

Spines are vertical columns representing voices or instruments:

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Get all spines
spines = doc.get_spines()
print(f"Total spines: {len(spines)}")

# Print spine headers
for i, spine in enumerate(spines):
    print(f"  Spine {i}: {spine.header}")

# Filter to specific types
kern_spines = [s for s in spines if s.header == '**kern']
text_spines = [s for s in spines if s.header == '**text']
print(f"Kern spines: {len(kern_spines)}, Text spines: {len(text_spines)}")
```

### Measure Information

Access measures and their ranges:

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

first_measure = doc.get_first_measure()
total_measures = doc.measures_count()

print(f"Score spans measures {first_measure} to {total_measures}")
print(f"Total measure count: {total_measures - first_measure + 1}")
```

### Get Tokens from a Spine

Access the individual musical elements:

```python
import kernpy as kp

doc, _ = kp.load('score.krn')
spines = doc.get_spines()

# Get tokens from the first kern spine
kern_spine = [s for s in spines if s.header == '**kern'][0]
tokens = kern_spine.get_tokens()

print(f"Total tokens: {len(tokens)}")

# Print first 20 token encodings
for i, token in enumerate(tokens[:20]):
    print(f"  {i:2d}: {token.encoding}")
```

## Analyzing Token Content

### Inspect Individual Tokens

Each token carries rich information:

```python
import kernpy as kp

doc, _ = kp.load('score.krn')
kern_spine = doc.get_spines()[0]
tokens = kern_spine.get_tokens()

# Examine a specific token
token = tokens[4]
print(f"Encoding: {token.encoding}")
print(f"Category: {token.category}")
print(f"Type: {type(token).__name__}")
```

### Filter Tokens by Category

Select only certain types of tokens for analysis:

```python
import kernpy as kp

doc, _ = kp.load('score.krn')
kern_spine = doc.get_spines()[0]
tokens = kern_spine.get_tokens()

# Get only notes and rests
note_rest_tokens = [t for t in tokens 
                    if t.category == kp.TokenCategory.NOTE_REST]

# Get only pitches
pitch_tokens = [t for t in tokens 
                if t.category == kp.TokenCategory.PITCH]

# Get clef information
clef_tokens = [t for t in tokens 
               if t.category == kp.TokenCategory.CLEF]

print(f"Notes/rests: {len(note_rest_tokens)}")
print(f"Pitches: {len(pitch_tokens)}")
print(f"Clef declarations: {len(clef_tokens)}")
```

## Extract Musical Information

### Find Time Signatures

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Get time signatures from all spines
time_sigs = set()
for spine in doc.get_spines():
    for token in spine.get_tokens():
        if token.category == kp.TokenCategory.TIME_SIGNATURE:
            time_sigs.add(token.encoding)

print(f"Time signatures found: {time_sigs}")
```

### Find Key Signatures

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

key_signatures = []
for spine in doc.get_spines():
    for token in spine.get_tokens():
        if token.category == kp.TokenCategory.KEY_SIGNATURE:
            key_signatures.append(token.encoding)

print(f"Key signatures: {key_signatures}")
```

### List All Clefs

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

clefs = {}
for i, spine in enumerate(doc.get_spines()):
    for token in spine.get_tokens():
        if token.category == kp.TokenCategory.CLEF:
            clefs[f"Spine {i}"] = token.encoding
            break  # Usually just one per spine

for spine_name, clef in clefs.items():
    print(f"{spine_name}: {clef}")
```

## Analyze Musical Content

### Count Notes and Rests

```python
import kernpy as kp

doc, _ = kp.load('score.krn')
kern_spine = [s for s in doc.get_spines() if s.header == '**kern'][0]
tokens = kern_spine.get_tokens()

notes = []
rests = []

for token in tokens:
    if token.category == kp.TokenCategory.REST:
        rests.append(token)
    elif token.category == kp.TokenCategory.NOTE_REST:
        notes.append(token)

print(f"Notes: {len(notes)}")
print(f"Rests: {len(rests)}")
print(f"Total: {len(notes) + len(rests)}")
```

### Analyze Pitches

```python
import kernpy as kp

doc, _ = kp.load('score.krn')
kern_spine = doc.get_spines()[0]

pitches = {}
for token in kern_spine.get_tokens():
    if token.category == kp.TokenCategory.PITCH:
        pitch = token.encoding
        pitches[pitch] = pitches.get(pitch, 0) + 1

# Sort by frequency
for pitch, count in sorted(pitches.items(), 
                          key=lambda x: x[1], 
                          reverse=True)[:10]:
    print(f"{pitch}: {count} times")
```

### Calculate Durations

```python
import kernpy as kp
from fractions import Fraction

doc, _ = kp.load('score.krn')
kern_spine = doc.get_spines()[0]

total_duration = Fraction(0)
for token in kern_spine.get_tokens():
    if token.category == kp.TokenCategory.DURATION:
        # Extract numeric duration
        try:
            duration_val = float(token.encoding)
            total_duration += Fraction(1, int(duration_val))
        except (ValueError, ZeroDivisionError):
            pass  # Skip non-numeric or zero values

print(f"Total duration (in quarter notes): {total_duration}")
print(f"As beats: {float(total_duration) * 4}")
```

## Practical Analysis Patterns

### Find All Occurrences of a Pattern

```python
import kernpy as kp

doc, _ = kp.load('score.krn')
kern_spine = doc.get_spines()[0]
tokens = kern_spine.get_tokens()

# Find all instances of a specific note
search_pitch = 'c'
occurrences = [t for t in tokens 
               if t.category == kp.TokenCategory.PITCH 
               and t.encoding == search_pitch]

print(f"Found {len(occurrences)} instances of pitch {search_pitch}")
```

### Extract Lyrics

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Find text spine
text_spine = None
for spine in doc.get_spines():
    if spine.header == '**text':
        text_spine = spine
        break

if text_spine:
    lyrics = []
    for token in text_spine.get_tokens():
        if not token.encoding.startswith('*') and '-' not in token.encoding:
            lyrics.append(token.encoding)
    
    print(f"Lyrics: {' '.join(lyrics)}")
```

### Compare Spines

```python
import kernpy as kp

doc, _ = kp.load('score.krn')
spines = doc.get_spines()

# Compare spine lengths
for i, spine in enumerate(spines):
    tokens = spine.get_tokens()
    print(f"Spine {i} ({spine.header}): {len(tokens)} tokens")
```

##Batch Analysis

Process multiple files:

```python
import kernpy as kp
from pathlib import Path

# Process all .krn files in a directory
score_dir = Path('scores')
results = []

for krn_file in score_dir.glob('*.krn'):
    doc, errors = kp.load(krn_file)
    if not errors:
        num_measures = doc.measures_count()
        num_spines = len(doc.get_spines())
        results.append({
            'file': krn_file.name,
            'measures': num_measures,
            'spines': num_spines
        })

# Display results
for result in results:
    print(f"{result['file']}: {result['measures']} measures, {result['spines']} spines")
```

## Summary

You now know how to:

1. Load **kern files and strings
2. Navigate the document structure (spines, tokens, measures)
3. Filter and extract specific information
4. Analyze musical content (pitches, durations, signatures)
5. Process collections of files

## Next Steps

- **Transform documents?** — See [Transform Documents](transform-documents.md)
- **Build automated workflows?** — See [Build Pipelines](build-pipelines.md)
- **Understand token categories better?** — See [Token Categories](../concepts/token-categories.md)
