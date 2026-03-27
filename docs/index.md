# kernpy: Symbolic Music Notation in Python

## What is kernpy?

kernpy is a comprehensive Python toolkit for working with Humdrum **kern format—a powerful, text-based system for representing symbolic music notation digitally. Whether you're a music researcher analyzing scores, a developer building music analysis tools, or an educator working with music data, kernpy gives you the tools to parse, analyze, transform, and export symbolic music notation programmatically.

Born from the research community, kernpy makes it easy to:

- Load and parse **kern files from disk or strings
- Navigate and analyze musical scores programmatically
- Transform documents through transposition, filtering, and selective export
- Build automated workflows for batch processing music collections
- Access detailed information about pitches, durations, clefs, key signatures, and more

## Why Use kernpy?

The **kern format has been the standard in music research for decades—used by musicologists, composers, and music technologists worldwide. But working with **kern files requires careful parsing of a text-based format. kernpy removes that burden.

### Problems kernpy Solves

**Working with existing tools**
Many music software packages support **kern, but they often require manual conversion, don't expose the full data structure, or lack batch processing capabilities. kernpy gives you direct, programmatic access to all **kern data.

**Bridging research and implementation**
Music researchers need to analyze scores computationally—extracting pitches, comparing durations, studying harmonic progressions, or searching for patterns. kernpy exposes everything you need without forcing you to parse the format yourself.

**Building custom workflows**
Standard tools can't always do what you need. kernpy lets you write Python code to combine operations (load + filter + transpose + export) in exactly the way your project requires.

**Handling scale**
Processing thousands of files manually is impossible. kernpy's batch processing capabilities let you apply the same transformations to entire score collections.

**Preserving data quality**
When converting between formats or tools, data can be lost. kernpy preserves the full richness of **kern notation, maintaining all information through the processing pipeline.

## Who Uses kernpy?

### Music Researchers and Musicologists

Extract collections of scores for corpus studies, analyze harmonic or melodic patterns, build datasets for machine learning, or study performance practice across historical periods.

**Example:** Analyze key signatures across all Bach chorales to understand his compositional patterns.

### Developers Building Music Tools

Build music analysis platforms, composition assistants, music education software, or analysis plugins that need to read and process **kern files.

**Example:** Create a web-based score editor that preserves all **kern metadata while providing visual notation.

### Music Educators

Prepare teaching materials, build interactive music analysis tools for students, or create assignments that involve programmatic score manipulation.

**Example:** Automatically transpose a collection of folk songs to different keys for ensemble instruction.

### Composers and Music Technologists

Process your own scores or collections, experiment with algorithmic composition, or build tools specialized to your compositional needs.

**Example:** Generate variations of your own compositions through systematic transposition and spine manipulation.

## Getting Started in Minutes

### 1. Installation

```bash
pip install kernpy
```

Or install from the repository for the latest development version:

```bash
pip install git+https://github.com/OMR-PRAIG-UA-ES/kernpy.git
```

### 2. Your First Script

```python
import kernpy as kp

# Load a **kern file
document, errors = kp.load('score.krn')

# Inspect what you loaded
print(f"Loaded score with {document.measures_count()} measures")

# Export to a new file
kp.dump(document, 'output.krn')
```

That's it. You've loaded, inspected, and exported a **kern file.

### 3. Next Steps

Once you've run your first script:

- **Want to understand the basics?** — See the [Getting Started](get-started.md) guide
- **Need a 5-minute walkthrough?** — Check [Quick Start: 5 Minutes](get-started/quick-start-5min.md)
- **Learning by example?** — Browse the [Examples](examples.md) gallery
- **Solving a specific problem?** — Jump to the [Guides](#learning-paths) section below

## Learning Paths

Choose your path based on your goals:

### Analyze and Extract Data

Parse files, inspect structure, search for patterns, and export subsets of information.

- [Parse and Analyze Guide](guides/parse-and-analyze.md) — Load files, navigate documents, access tokens
- [Concept: Humdrum **kern Format](concepts/humdrum-kern.md) — Understand what you're reading
- [Concept: Token Categories](concepts/token-categories.md) — Learn about different types of data

### Transform and Export

Filter spines, change encodings, transpose pitches, select measures, and export customized versions of scores.

- [Transform Documents Guide](guides/transform-documents.md) — Filter, transpose, and slice scores
- [Concept: Encodings](concepts/encodings.md) — Understand export formats
- [Advanced: Custom Export](advanced/custom-export.md) — Fine-grained control over what you export

### Build Workflows

Process collections, combine files, automate repetitive tasks, and integrate kernpy into larger systems.

- [Build Pipelines Guide](guides/build-pipelines.md) — Batch processing and document concatenation
- [Concept: Documents and Spines](concepts/documents-and-spines.md) — Understand the data structure
- [Advanced: Document Structure](advanced/document-structure.md) — Navigate and manipulate the tree

### Command-Line Tools

Use kernpy's utilities from the terminal for format conversion and dataset processing.

- [CLI Utilities Guide](guides/cli-utilities.md) — Format conversion and command-line operations

## Explore the Documentation

### Core Concepts

Understand the foundations:

- [Humdrum **kern Format](concepts/humdrum-kern.md) — What **kern is and how it works
- [Token Categories and Filtering](concepts/token-categories.md) — Control what you export
- [Encoding Formats](concepts/encodings.md) — Different ways to represent music
- [Documents and Spines](concepts/documents-and-spines.md) — How kernpy structures data

### Practical Guides

Learn by doing:

- [Parse and Analyze](guides/parse-and-analyze.md) — Load files, read structure, extract data
- [Transform Documents](guides/transform-documents.md) — Filter, transpose, slice, export
- [Build Pipelines](guides/build-pipelines.md) — Batch processing, concatenation, workflows
- [CLI Utilities](guides/cli-utilities.md) — Command-line tools and format conversion

### API Reference

Full technical documentation:

- [API Reference](reference.md) — Complete function and class documentation
- [Examples Gallery](examples.md) — Copy-paste code snippets

### Advanced Topics

Deep dives into specialized areas:

- [Transposition](advanced/transposition.md) — Pitch operations and interval systems
- [Document Structure](advanced/document-structure.md) — Tree navigation and advanced access
- [Custom Export](advanced/custom-export.md) — Advanced filtering and export strategies

### Help and Resources

- [FAQ](faq.md) — Common questions and troubleshooting
- [Contributing](contributing.md) — How to contribute to kernpy
- [Citation](citation.md) — How to cite kernpy in academic work
- [About](about.md) — The kernpy project and team

## Quick Reference

### Most Common Operations

```python
import kernpy as kp

# Load a file
doc, errors = kp.load('file.krn')

# Load from a string
doc, errors = kp.loads('**kern\n*M4/4\n4c\n4d\n*-')

# Export to a file
kp.dump(doc, 'output.krn')

# Export to a string
content = kp.dumps(doc)

# Filter to specific spines
kp.dump(doc, 'filtered.krn', spine_types=['**kern'])

# Transpose
transposed_doc = doc.to_transposed('P4', 'up')
kp.dump(transposed_doc, 'transposed.krn')

# Select measures
kp.dump(doc, 'excerpt.krn', from_measure=5, to_measure=10)
```

## Installation and Setup

Get started in three commands:

```bash
# Install kernpy
pip install kernpy

# Verify installation
python -c "import kernpy as kp; print('kernpy ready!')"

# Run a quick test
python << 'EOF'
import kernpy as kp
doc, _ = kp.loads('**kern\n*M4/4\n4c 4e 4g\n')
print(f"Loaded chord with {len(doc.get_spines())} spine(s)")
EOF
```

## What's New

kernpy 1.6.0 focuses on:

- Modern Python API with `load`, `loads`, `dump`, `dumps` functions
- Comprehensive support for **kern and **mens notation
- Robust measure signature validation
- Flexible token filtering through the category system
- Support for multiple export formats (kern, ekern, agnostic kern, etc.)

**Note:** Some older functions (`read`, `create`, `export`, `store`) are deprecated. See [reference.md](reference.md) for migration guidance.

## Next Steps

1. **Install kernpy** — Follow the [installation instructions](#installation-and-setup) above
2. **Read Getting Started** — The [Getting Started](get-started.md) guide covers installation and first steps
3. **Run a quick example** — Follow the [Quick Start](get-started/quick-start-5min.md) for a 5-minute introduction
4. **Pick a learning path** — Choose based on your goals (analyze, transform, or build) in the [Learning Paths](#learning-paths) section

## Support and Contributing

- **Questions?** — See [FAQ](faq.md) for common questions
- **Found a bug?** — [Report an issue](https://github.com/OMR-PRAIG-UA-ES/kernpy/issues)
- **Want to contribute?** — See [Contributing](contributing.md) guidelines
- **Citation?** — How to [cite kernpy](citation.md) in your research

## License

kernpy is open-source software licensed under the AGPL-3.0 license. See the repository for details.

---

## Acknowledgments

kernpy is developed by the Pattern Recognition and Artificial Intelligence Group at the University of Alicante. Learn more about our research at [PRAIG](https://praig.ua.es/).
