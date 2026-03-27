# Getting Started with kernpy

Welcome to kernpy! This guide will help you install the package and understand the core concepts you need to get started.

## Installation

Choose the installation method that best fits your needs.

### Option 1: Install from PyPI (Recommended)

The easiest way to install kernpy is using pip:

```bash
pip install kernpy
```

To upgrade to the latest version:

```bash
pip install --upgrade kernpy
```

### Option 2: Install from GitHub (Development Version)

To get the latest development version with the most recent features:

```bash
pip install git+https://github.com/OMR-PRAIG-UA-ES/kernpy.git
```

### Option 3: Editable Installation for Development

If you want to contribute to kernpy or develop with the source code directly:

```bash
git clone https://github.com/OMR-PRAIG-UA-ES/kernpy.git
cd kernpy
pip install -e .
```

### Option 4: Install with Documentation Tools

If you want to build the documentation locally:

```bash
pip install kernpy[docs]
```

## Verify Your Installation

After installation, verify that kernpy is installed correctly:

```bash
# Quick test in the Python REPL
python -c "import kernpy as kp; print('kernpy version:', kp.__version__)"
```

Or run a more comprehensive test:

```python
import kernpy as kp

# Try loading from a string
kern_data = """**kern
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

document, errors = kp.loads(kern_data)
print(f"Successfully loaded document with {document.measures_count()} measures")
print(f"Errors: {len(errors)}")
```

If you see output without errors, kernpy is ready to use!

## Core Concepts

Before diving into code, it's helpful to understand three fundamental concepts in kernpy.

### 1. The Document

A **Document** is the main object that represents a complete musical score. It contains everything loaded from a **kern file.

```python
import kernpy as kp

# Load a document
document, errors = kp.load('score.krn')

# A document contains:
# - Multiple spines (voices/instruments)
# - Multiple measures
# - All metadata (clefs, time signatures, key signatures, etc.)
# - Any errors found during parsing
```

### 2. Spines

A **Spine** is a vertical column in a **kern file representing a single voice or instrument. A document can contain multiple spines side-by-side.

Common spine types:

- `**kern` — Musical notation (pitches, durations, articulations)
- `**text` — Lyrics or text underlay
- `**dynam` — Dynamic markings
- `**harm` — Harmonic analysis
- `**mens` — Mensural notation
- And many others

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Access spines
spines = doc.get_spines()
print(f"Number of spines: {len(spines)}")

for i, spine in enumerate(spines):
    print(f"Spine {i}: {spine.header}")  # e.g., **kern, **text, etc.
```

### 3. Tokens and Categories

A **Token** is the smallest unit of musical information within a spine. Examples include:

- A note: `4c` (quarter note, pitch C)
- A rest: `4r` (quarter rest)
- A clef: `*clefG2` (treble clef)
- A time signature: `*M4/4` (4/4 time)

**Token Categories** classify tokens semantically. For example, a note contains information about:

- `PITCH` — The pitch (c, d, e, etc.)
- `DURATION` — The length (4, 8, 16, etc.)
- `DECORATION` — Articulations (staccato, accent, etc.)
- And more...

You can filter exports based on categories:

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Export only pitches and durations (no decorations)
kp.dump(doc, 'output.krn',
        exclude={kp.TokenCategory.DECORATION})
```

## The Basics: Load, Inspect, Export

All kernpy workflows follow this basic pattern:

1. **Load** a document from a file or string
2. **Inspect** the document to understand its structure
3. **Transform** the document if needed
4. **Export** to a new file or string

### Loading

```python
import kernpy as kp

# Load from a file
document, errors = kp.load('score.krn')

# Load from a string
document, errors = kp.loads('**kern\n*M4/4\n4c\n4d\n*-')

# Check for parsing errors
if errors:
    print(f"Parsing found {len(errors)} errors:")
    for error in errors:
        print(f"  - {error}")
```

### Inspecting

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Basic information
print(f"Measures: {doc.get_first_measure()} to {doc.measures_count()}")
print(f"Spines: {len(doc.get_spines())}")

# Information by spine
for i, spine in enumerate(doc.get_spines()):
    print(f"  Spine {i}: {spine.header}")
```

### Exporting

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Export entire document to a new file
kp.dump(doc, 'output.krn')

# Export as a string
content = kp.dumps(doc)
print(content)

# Export with filtering
kp.dump(doc, 'kern_only.krn', spine_types=['**kern'])

# Export specific measures
kp.dump(doc, 'excerpt.krn', from_measure=1, to_measure=10)
```

## Next Steps

You're ready to explore kernpy! Choose your next step:

- **Want a quick 5-minute example?** — See [Quick Start](quick-start-5min.md)
- **Want to learn by example?** — See [Examples Gallery](../examples.md)
- **Want to understand the format?** — See [Humdrum **kern Format](../concepts/humdrum-kern.md)
- **Want to solve a specific problem?** — Jump into [Practical Guides](../guides/parse-and-analyze.md)

## Troubleshooting

### Import Error

If you get `ModuleNotFoundError: No module named 'kernpy'`:

1. Verify installation: `pip show kernpy`
2. Reinstall if needed: `pip install --force-reinstall kernpy`
3. If using a virtual environment, ensure it's activated

### File Not Found

Make sure the file path is correct. Use absolute paths to be safe:

```python
import kernpy as kp
from pathlib import Path

# Use a specific path
score_path = Path.home() / 'Music' / 'scores' / 'score.krn'
doc, errors = kp.load(score_path)
```

### Parsing Errors

Some **kern files might have minor formatting issues. kernpy is tolerant of many variations, but you can check for errors:

```python
import kernpy as kp

doc, errors = kp.load('score.krn')
if errors:
    print(f"Found {len(errors)} issues:")
    for error in errors[:5]:  # Show first 5
        print(f"  {error}")
```

See [FAQ](../faq.md) for more common issues.

## Command-Line Usage

kernpy also includes command-line tools. Try:

```bash
# Get help
python -m kernpy --help

# Convert formats
python -m kernpy --kern2ekern input.krn output.ekrn
python -m kernpy --ekern2kern input.ekrn output.krn
```

For more details, see [CLI Utilities](../guides/cli-utilities.md).

## Summary

You've learned:

1. How to install kernpy
2. The three core concepts: Documents, Spines, and Tokens
3. How to load, inspect, and export documents
4. Where to find more resources

You're ready to start writing kernpy code! See the [Practical Guides](../guides/parse-and-analyze.md) for detailed examples and workflows.


