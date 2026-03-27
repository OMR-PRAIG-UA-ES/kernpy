# Understanding Humdrum **kern Format


## Basic Structure

A **kern file consists of three main components: headers, data tokens, and spine operations.

### Headers

Every **kern file begins with spine headers that declare the type of data in each column:

```kern
**kern    **text    **dynam
```

Standard spine types include:

- `**kern` — Musical notation (pitches and durations)
- `**mens` — Mensural notation (medieval/renaissance music)
- `**text` — Lyrics or text underlay
- `**dynam` — Dynamics (p, f, ff, ppp, etc.)
- `**harm` — Harmonic analysis symbols
- `**fing` — Fingering for instruments
- `**mxhm` — Scale degree notation (tonal analysis)
- `**root` — Root movement analysis

### Spines

A spine is a vertical column of data representing a single voice or instrument. Multiple spines are tab-separated and processed in parallel.

### Tokens

Tokens are the individual units of musical information. In **kern spines, a token might represent:

- A note with pitch and duration: `4c` (quarter note, pitch C)
- A rest: `4r` (quarter rest)
- A chord: `4c 4e 4g` (multiple pitches in one moment)
- Metadata: `*clefG2` (treble clef), `*M4/4` (time signature), `*k[f#]` (key signature)
- Bar lines: `=1` (measure 1 barline)

Tokens are separated by tabs within a spine and by tabs between spines.

## Example **kern File

```kern
**kern    **text
*clefG2   *
*M4/4     *
=1        =1
4c        Do
4d        Re
4e        Mi
4f        Fa
=2        =2
2g        So-
2cc       lus
==        ==
*-        *-
```

In this example:

- Column 1 contains **kern notation (notes and meter)
- Column 2 contains **text (lyrics)
- Both columns share the same barlines
- The `*clefG2` indicates treble clef
- The `*M4/4` indicates 4/4 time signature
- The `==` indicates the end of the piece
- The `*-` ends each spine

## Pitch Representation in **kern

Pitches in **kern are represented using a specific notation:

- Lowercase letters (c–g) represent pitches from C4 to B4
- Uppercase letters (C–G) represent pitches from C3 to B3
- Additional octaves are indicated by repeating letters:
  - `cc` = C5 (one octave above c)
  - `ccc` = C6
  - `C` = C3
  - `CC` = C2
  - `CCC` = C1

Accidentals are appended to the pitch:

- `#` for sharp: `c#` = C4 sharp
- `-` for flat: `c-` = C4 flat
- `##` for double sharp
- `--` for double flat

Rests are represented by `r`.

## Duration Representation

Durations in **kern use numeric values representing note divisions:

- `1` = whole note
- `2` = half note
- `4` = quarter note
- `8` = eighth note
- `16` = sixteenth note
- And so on...

Dotted notes are indicated with a dot (`.`) following the duration:

- `4.` = dotted quarter note (1.5 times the quarter note value)
- `8..` = double-dotted eighth note
- `4...` = triple-dotted quarter note

Tied notes use the `_` (tie) and `]` symbols to indicate ligatures.

Example durations:

```kern
**kern
*M4/4
=1
1c        (whole note C)
2d 2e     (two half notes)
4f 4g 4a 4b  (four quarter notes)
8c 8d 8e 8f 8g 8a 8b 8cc  (eight eighth notes)
=2
4.c 8d    (dotted quarter C, eighth D)
16e 16f   (sixteenth notes)
```

## Spine Operations

Spine operations modify the structure of the data:

- `*+` — Add a new spine to the right
- `*-` — Terminate a spine
- `*^` — Split a spine into two
- `*v` — Merge two spines

These operations allow for dynamic restructuring of the data during playback or analysis.

## Tandem Interpretations

Tandem interpretations are special tokens that provide performance or notational information:

- `*clef**` declarations (e.g., `*clefG2`, `*clefF4`)
- Key signatures: `*k[b-e-a-]` (B-flat major / G minor)
- Time signatures: `*M4/4` (4/4 time)
- Tempo: `*MM120` (120 beats per minute)
- Instrument names: `*Ivioln` (violin)

## Decorations and Articulations

Articulations and additional notations are appended after the pitch and duration:

## Summary

The **kern format provides a comprehensive, machine-readable representation of symbolic music notation. Its simplicity and flexibility make it ideal for digital music research and analysis. kernpy provides tools to parse, analyze, and manipulate **kern files programmatically.

## Next Steps

- See [concepts/token-categories.md](token-categories.md) to understand how kernpy categorizes the different types of tokens
- See [concepts/documents-and-spines.md](documents-and-spines.md) to learn about kernpy's internal data structures
- See [guides/parse-and-analyze.md](../guides/parse-and-analyze.md) for practical examples of loading and analyzing **kern files
