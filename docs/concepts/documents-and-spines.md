# Documents and Spines: Understanding kernpy's Data Structures

## The Document Object

When you load a **kern file using kernpy, you get a `Document` object. This object contains the entire parsed score in a tree-like structure.

```python
import kernpy as kp

# Load a file
document, errors = kp.load('score.krn')

# The document contains everything
print(type(document))  # <class 'kernpy.core.document.Document'>
print(document)        # kernpy.core.document.Document object
```

## Document Structure

The Document object represents a complete musical score. It provides access to:

- The score's tree structure (spines, tokens, barlines)
- Measure information
- Spine metadata (instrument names, clefs, key signatures)
- Error information from parsing

## What Are Spines?

A spine is a vertical column in a **kern file representing a single voice or instrument. When you load a **kern file with multiple columns, each column becomes a separate spine.

Example **kern file with three spines:

```kern
**kern    **text    **dynam
*Ivioln   *         *
*clefG2   *         *
=1        =1        =1
4c        Do        p
4d        Re        <
4e        Mi        (
4f        Fa        (
=2        =2        =2
2g        Sol       f
2cc       -         >
==        ==        ==
*-        *-        *-
```

This file has:

- Spine 0: Musical notation (**kern)
- Spine 1: Lyrics (**text)
- Spine 2: Dynamics (**dynam)

## Accessing Spines

You can access individual spines from the document:

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Get all spines
spines = doc.get_spines()
print(f"Number of spines: {len(spines)}")

# Get a specific spine by index
spine_0 = spines[0]
print(f"Spine 0 type: {spine_0.header}")  # **kern

# Get the header of a spine
spine_type = spine_0.header
print(spine_type)  # **kern, **text, **dynam, etc.
```

## Tokens Within Spines

Each spine contains tokens, which are the individual musical or textual elements:

```python
import kernpy as kp

doc, _ = kp.load('score.krn')
spines = doc.get_spines()

# Get tokens from a spine
kern_spine = spines[0]
tokens = kern_spine.get_tokens()  # or use a similar accessor

for token in tokens:
    print(f"Token: {token.encoding}")  # The raw **kern representation
```

## Measures

Measures are logical divisions of the score marked by barlines. You can work with measures rather than individual tokens:

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Get measure information
first_measure = doc.get_first_measure()
last_measure = doc.measures_count()
print(f"Score spans measures {first_measure} to {last_measure}")

# Export specific measures
kp.dump(doc, 'measure_1.krn', from_measure=1, to_measure=1)
kp.dump(doc, 'measures_5_10.krn', from_measure=5, to_measure=10)
```

## The Document Tree

Internally, the document uses a tree structure. You can visualize and navigate it:

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Export the tree structure for visualization
tree = doc.tree
print(tree)

# Create a graphviz visualization
kp.graph(doc, 'score_tree.dot')
# You can then render this with: dot -Tpng score_tree.dot -o score_tree.png
```

The tree helps you understand:

- The hierarchical structure of the score
- How tokens are organized
- Reference points for navigation and analysis

## Spine Types and Metadata

Different spine types carry different kinds of information:

```python
import kernpy as kp

doc, _ = kp.load('score.krn')
spine_types = kp.spine_types(doc)
print(spine_types)  # List of spine types: ['**kern', '**text', '**dynam', ...]

# Filter to only kern spines
kern_spines = [s for s in doc.get_spines() if s.header == '**kern']
```

See [concepts/humdrum-kern.md](humdrum-kern.md) for the list of common spine types.

## Selecting Spines for Export

When exporting, you can choose which spines to include:

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Export only **kern spines
kp.dump(doc, 'kern_only.krn',
        spine_types=['**kern'])

# Export **kern and **text together
kp.dump(doc, 'kern_and_lyrics.krn',
        spine_types=['**kern', '**text'])

# Export by spine index (0-based)
kp.dump(doc, 'first_two_spines.krn',
        spine_ids=[0, 1])
```

## Working with Document Content

The document gives you many ways to interact with the content:

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Get information about the score
num_measures = doc.measures_count()
first_measure_num = doc.get_first_measure()

# Check what spines exist
spines = doc.get_spines()
kern_count = sum(1 for s in spines if s.header == '**kern')
text_count = sum(1 for s in spines if s.header == '**text')

print(f"Score has:")
print(f"  {num_measures} measures (from measure {first_measure_num})")
print(f"  {len(spines)} spines")
print(f"  {kern_count} kern spine(s)")
print(f"  {text_count} text spine(s)")
```

## Using the Tree for Advanced Navigation

For more advanced analysis, you can work directly with the document tree:

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Access the tree
tree = doc.tree
print(tree)  # DocumentTree object

# Use the tree to navigate nodes
# (Specific tree navigation methods depend on kernpy's API)
```

## Summary

The Document object is your gateway to everything in a **kern file:

- **Spines** — Vertical columns of musical or textual data
- **Tokens** — Individual notes, rests, markings, and metadata
- **Measures** — Logical divisions of the score
- **Metadata** — Information about the score structure and content

By understanding documents and spines, you can effectively load, analyze, filter, and transform musical scores using kernpy.

## Next Steps

- See [guides/parse-and-analyze.md](../guides/parse-and-analyze.md) for practical examples of working with documents
- See [advanced/document-structure.md](../advanced/document-structure.md) for deeper navigation techniques
- See [guides/transform-documents.md](../guides/transform-documents.md) to learn how to modify and export documents
