# Practical Guides

Learn how to accomplish specific tasks with kernpy. These guides provide step-by-step instructions, code examples, and common patterns.

## Getting Started

New to kernpy? Start here:

- [Getting Started](get-started.md) — Installation and core concepts
- [Quick Start (5 min)](get-started/quick-start-5min.md) — Minimal examples to get you rolling

## Core Workflows

### Parse and Analyze

Load **kern files, inspect structure, and extract musical information.

- **Guide:** [Parse and Analyze](guides/parse-and-analyze.md)
- **Learn:** How to load files, navigate the document structure, filter tokens by category
- **Use when:** You need to extract information from scores (pitches, durations, time signatures, etc.)
- **Examples:** Count notes in a score, analyze rhythmic patterns, batch process multiple files

### Transform Documents

Filter, transpose, and modify scores to create new versions.

- **Guide:** [Transform Documents](guides/transform-documents.md)
- **Learn:** How to filter spines, select measures, transpose, change encodings
- **Use when:** You need to create variations (transpositions, arrangements, simplifications)
- **Examples:** Transpose to new keys, extract single instruments, remove decorations

### Build Processing Pipelines

Automate workflows for batch processing and complex data operations.

- **Guide:** [Build Pipelines](guides/build-pipelines.md)
- **Learn:** Batch processing, document concatenation, parallel processing, dataset creation
- **Use when:** You need to process many files or combine files in sophisticated ways
- **Examples:** Convert entire directories, transpose files in multiple keys, create CSV inventories

### Command-Line Utilities

Work with kernpy from the shell without writing Python code.

- **Guide:** [CLI Utilities](guides/cli-utilities.md)
- **Learn:** Command-line commands, batch conversion, integration with shell scripts
- **Use when:** You prefer shell commands or need to integrate with bash/zsh scripts
- **Examples:** Convert kern to ekern, process Polish dataset, recursive directory processing

## Advanced Topics

Sophisticated patterns and deep-dive topics.

- [Transposition](advanced/transposition.md) — All interval notation, batch transposition, key modulation
- [Document Structure](advanced/document-structure.md) — Tree navigation, token manipulation, analysis patterns
- [Custom Export](advanced/custom-export.md) — Complex filtering, multi-version creation, study editions

## Quick Reference

| Task | Guide | Key Functions |
|------|-------|---|
| Load and inspect a file | [Parse and Analyze](guides/parse-and-analyze.md) | `kp.load()`, `doc.get_spines()` |
| Transpose a score | [Transform Documents](guides/transform-documents.md) | `doc.to_transposed()` |
| Remove decoration marks | [Transform Documents](guides/transform-documents.md) | `kp.dump(..., exclude={...})` |
| Extract single spine | [Transform Documents](guides/transform-documents.md) | `kp.dump(..., spine_ids=[0])` |
| Batch process files | [Build Pipelines](guides/build-pipelines.md) | `Path.glob()`, `multiprocessing.Pool` |
| Count pitches | [Parse and Analyze](guides/parse-and-analyze.md) | Loop + `TokenCategory.PITCH` |
| Convert format | [CLI Utilities](guides/cli-utilities.md) | `python -m kernpy --kern2ekern` |

## Code Examples

Ready-to-use snippets for common tasks:

- **[Code Examples](examples.md)** — 40+ complete, copy-paste examples organized by task

## Troubleshooting

- **[FAQ](faq.md)** — Solutions for common problems and questions

## Learning Paths by Goal

**Want to analyze music data?**
→ [Parse and Analyze](guides/parse-and-analyze.md) → [Document Structure](advanced/document-structure.md) → [Code Examples](examples.md)

**Want to create score variations?**
→ [Transform Documents](guides/transform-documents.md) → [Transposition](advanced/transposition.md) → [Custom Export](advanced/custom-export.md)

**Want to automate workflows?**
→ [Build Pipelines](guides/build-pipelines.md) → [Code Examples](examples.md) → [CLI Utilities](guides/cli-utilities.md)

**Want to learn the fundamentals?**
→ [Getting Started](get-started.md) → [Core Concepts](concepts/humdrum-kern.md), [Token Categories](concepts/token-categories.md), [Encodings](concepts/encodings.md) → [Your chosen guide above]
