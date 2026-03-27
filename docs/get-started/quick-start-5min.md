# Quick Start: 5 Minutes

Get up and running with kernpy in five minutes with this minimal example.

## 1. Load a File (30 seconds)

```python
import kernpy as kp

# Load a .krn file
document, errors = kp.load('score.krn')

print(f"Loaded {document.measures_count()} measures")
```

## 2. Inspect the Score (1 minute)

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# See what's in the document
spines = doc.get_spines()
print(f"Spines: {[s.header for s in spines]}")

# Measure information
print(f"Measures: {doc.get_first_measure()} to {doc.measures_count()}")
```

## 3. Extract Information (1 minute)

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Get the first kern spine (musical notes)
kern_spine = [s for s in doc.get_spines() if s.header == '**kern'][0]
tokens = kern_spine.get_tokens()

# Print first 10 tokens
for token in tokens[:10]:
    print(token.encoding)
```

## 4. Filter and Export (1.5 minutes)

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Export only kern spines (no lyrics, dynamics, etc.)
kp.dump(doc, 'kern_only.krn',
        spine_types=['**kern'])

# Export measures 5 through 10
kp.dump(doc, 'excerpt.krn',
        from_measure=5,
        to_measure=10)

# Export without decorations
kp.dump(doc, 'plain.krn',
        exclude={kp.TokenCategory.DECORATION})

print("Exports complete!")
```

## 5. Work with Strings (1 minute)

```python
import kernpy as kp

# Load from a string
kern_string = """**kern
*clefG2
*M4/4
=1
4c
4d
4e
4f
=2
2g
*-
"""

doc, errors = kp.loads(kern_string)
print(f"Loaded {doc.measures_count()} measures from string")

# Export to string
output = kp.dumps(doc)
print(output)
```

## Complete Example

Combine everything together:

```python
import kernpy as kp

# 1. Load
doc, errors = kp.load('input.krn')
if errors:
    print(f"Warnings: {errors}")

# 2. Inspect
spines = doc.get_spines()
print(f"Loaded {len(spines)} spines, {doc.measures_count()} measures")

# 3. Transform (transpose up a perfect 4th)
transposed = doc.to_transposed('P4', 'up')

# 4. Export
kp.dump(transposed, 'output.krn')
print("Done!")
```

## Where to Go Next

- **Learning by Example** — See [Examples](../examples.md) for more code snippets
- **Diving Deeper** — Read [Parse and Analyze](../guides/parse-and-analyze.md) guide
- **Understanding the Format** — Learn about [Humdrum **kern](../concepts/humdrum-kern.md)

---

More detailed documentation is available in the [full guides](../guides/parse-and-analyze.md).
