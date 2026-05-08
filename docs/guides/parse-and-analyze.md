# Guide: Parse and Analyze

Learn how to load **kern files, inspect their structure, and extract musical information for analysis.

## Loading Files

### Load from Disk

The most common use case—loading a **kern file from your file system:

```python
import kernpy as kp

document, errors = kp.load('path/to/score.krn')

# Handle any parsing errors
if len(errors) > 0:
    print(f"Parser found {len(errors)} issues:")  # Usually renders like Verovio althouh these errors
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

### Inspect Spine Metadata

The public API exposes spine metadata, not individual spine objects:

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

spine_types = kp.spine_types(doc)
spine_ids = doc.get_spine_ids()
print(f"Total spines: {doc.get_spine_count()}")
print(f"Spine ids: {spine_ids}")
print(f"Spine types: {spine_types}")
```

### Measure Information

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

first_measure = doc.get_first_measure()
last_measure = doc.measures_count()

print(f"Score spans measures {first_measure} to {last_measure}")
```

### Get Tokens from the Document

```python
import kernpy as kp

doc, _ = kp.load('score.krn')
tokens = doc.get_all_tokens()
token_encodings = doc.get_all_tokens_encodings()

print(f"Total tokens: {len(tokens)}")
print(f"First 20 encodings: {token_encodings[:20]}")

for i, token in enumerate(tokens[:20]):
    print(f"  {i:2d}: {token.encoding}")
```

## Analyzing Token Content

### Inspect Individual Tokens

```python
import kernpy as kp

doc, _ = kp.load('score.krn')
tokens = doc.get_all_tokens()

token = tokens[4]
print(f"Encoding: {token.encoding}")
print(f"Category: {token.category}")
print(f"Type: {type(token).__name__}")
```

### Filter Tokens by Category

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

note_rest_tokens = doc.get_all_tokens(filter_by_categories=[kp.TokenCategory.NOTE_REST])
pitch_tokens = doc.get_all_tokens(filter_by_categories=[kp.TokenCategory.PITCH])
clef_tokens = doc.get_all_tokens(filter_by_categories=[kp.TokenCategory.CLEF])

print(f"Note/rest tokens: {len(note_rest_tokens)}")
print(f"Pitch subtokens: {len(pitch_tokens)}")
print(f"Clef tokens: {len(clef_tokens)}")
```

### Count Token Frequencies

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

frequencies = doc.frequencies()
note_rest_frequencies = doc.frequencies(token_categories=[kp.TokenCategory.NOTE_REST])

print(f"Total unique tokens: {len(frequencies)}")
print(f"Note/rest frequencies: {note_rest_frequencies}")
```

## Extract Musical Information

### Find Time Signatures

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

time_sigs = doc.get_all_tokens(filter_by_categories=[kp.TokenCategory.TIME_SIGNATURE])
print(f"Time signatures found: {[token.encoding for token in time_sigs]}")
```

### Find Key Signatures

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

key_signatures = doc.get_all_tokens(filter_by_categories=[kp.TokenCategory.KEY_SIGNATURE])
print(f"Key signatures: {[token.encoding for token in key_signatures]}")
```

### List All Clefs

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

clef_tokens = doc.get_all_tokens(filter_by_categories=[kp.TokenCategory.CLEF])
print(f"Clefs: {[token.encoding for token in clef_tokens]}")
```

## Analyze Musical Content

### Count Note and Rest Tokens

```python
import kernpy as kp

doc, _ = kp.load('score.krn')
note_rest_tokens = doc.get_all_tokens(filter_by_categories=[kp.TokenCategory.NOTE_REST])

rest_count = sum(
    1 for token in note_rest_tokens
    if any(subtoken.category == kp.TokenCategory.REST for subtoken in token.pitch_duration_subtokens)
)
note_count = len(note_rest_tokens) - rest_count

print(f"Notes: {note_count}")
print(f"Rests: {rest_count}")
print(f"Total: {len(note_rest_tokens)}")
```

## Practical Analysis Patterns

### Extract Lyrics

```python
import kernpy as kp

doc, _ = kp.load('score.krn')
lyrics = doc.get_all_tokens(filter_by_categories=[kp.TokenCategory.LYRICS])

print(f"Lyrics: {' '.join(token.encoding for token in lyrics)}")
```

### Compare Spine Metadata

```python
import kernpy as kp
from collections import Counter

doc, _ = kp.load('score.krn')
spine_types = kp.spine_types(doc)
spine_ids = doc.get_spine_ids()

for spine_type, count in Counter(spine_types).items():
    print(f"{spine_type}: {count}")

print(f"Spine ids: {spine_ids}")
```

## Batch Analysis

Process multiple files:

```python
import kernpy as kp
from pathlib import Path

score_dir = Path('scores')
results = []

for krn_file in score_dir.glob('*.krn'):
    doc, errors = kp.load(krn_file)
    if not errors:
        results.append({
            'file': krn_file.name,
            'measures': doc.measures_count(),
            'spines': doc.get_spine_count(),
            'types': ','.join(kp.spine_types(doc)),
            'errors': len(errors),
            'tokens': len(doc.get_all_tokens()),
            'frequencies': doc.frequencies(),
        })

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
