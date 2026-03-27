# Custom Export

Advanced filtering and export strategies for creating tailored versions of your scores with precisely controlled content.

## Export Basics

kernpy provides flexible export with control over which content is included or excluded.

### Basic Export

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Simple export
kp.dump(doc, 'output.krn')

# Or get as string
content = kp.dumps(doc)
```

## Token Category Filtering

The `include` and `exclude` parameters let you control which token categories appear in output.

### Include Specific Categories

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Keep only pitch information (melody)
kp.dump(
    doc,
    'pitches_only.krn',
    include={kp.TokenCategory.PITCH}
)

# Keep pitches and durations
kp.dump(
    doc,
    'notes_without_decoration.krn',
    include={
        kp.TokenCategory.PITCH,
        kp.TokenCategory.DURATION,
    }
)

# Keep essential musical elements
kp.dump(
    doc,
    'essential.krn',
    include={
        kp.TokenCategory.CORE,           # Notes and rests
        kp.TokenCategory.SIGNATURES,     # Key, time sigs
        kp.TokenCategory.BARLINES,       # Measure markers
    }
)
```

### Exclude Specific Categories

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Remove articulation marks
kp.dump(
    doc,
    'no_articulation.krn',
    exclude={kp.TokenCategory.DECORATION}
)

# Remove all dynamics
kp.dump(
    doc,
    'no_dynamics.krn',
    exclude={kp.TokenCategory.DYNAMICS}
)

# Keep everything except ornaments
kp.dump(
    doc,
    'no_ornaments.krn',
    exclude={kp.TokenCategory.ORNAMENT}
)
```

## Spine Type Filtering

Control which instrument types or data streams are exported.

### Keep Specific Spine Types

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Keep only kern spines (notes)
kp.dump(
    doc,
    'notes_only.krn',
    spine_types=['**kern']
)

# Keep kern and text (notes + lyrics)
kp.dump(
    doc,
    'notes_and_lyrics.krn',
    spine_types=['**kern', '**text']
)

# Keep kern and harmonic analysis
kp.dump(
    doc,
    'notes_and_harmony.krn',
    spine_types=['**kern', '**harm']
)
```

### Complex Spine Selection

```python
import kernpy as kp

doc, _ = kp.load('orchestral_score.krn')

# Get all kern spines (all instruments)
spines = doc.get_spines()
kern_spine_ids = [i for i, s in enumerate(spines) if s.spine_type() == '**kern']

# Export only kern spines (remove metadata)
kp.dump(
    doc,
    'instruments_only.krn',
    spine_ids=kern_spine_ids
)

# Export specific instrument range
kp.dump(
    doc,
    'woodwinds_section.krn',
    spine_ids=kern_spine_ids[0:3]  # First 3 kern spines
)
```

## Measure Range Filtering

Extract specific sections of a score.

### Export Measures by Number

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Measures 10 to 30
kp.dump(doc, 'section.krn', from_measure=10, to_measure=30)

# First 12 measures (intro)
kp.dump(doc, 'intro.krn', to_measure=12)

# From measure 50 to end
kp.dump(doc, 'ending.krn', from_measure=50)
```

### Extract Multiple Sections

```python
import kernpy as kp

doc, _ = kp.load('sonata.krn')

# Extract sections of a sonata form
sections = {
    'exposition': (1, 50),
    'development': (51, 100),
    'recapitulation': (101, 150),
    'coda': (151, None),
}

for section_name, (start, end) in sections.items():
    kwargs = {'from_measure': start}
    if end:
        kwargs['to_measure'] = end
    
    kp.dump(doc, f'{section_name}.krn', **kwargs)
    print(f"Exported {section_name}")
```

## Encoding Format Control

Export in different formats optimized for different use cases.

### Export as Different Encodings

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Standard normalized kern
kp.dump(doc, 'output.krn', encoding=kp.Encoding.normalizedKern)

# Extended kern (shows internal structure)
kp.dump(doc, 'debug.ekrn', encoding=kp.Encoding.eKern)

# Agnostic format (stripped down)
kp.dump(doc, 'simple.txt', encoding=kp.Encoding.agnosticKern)

# Basic kern only
kp.dump(doc, 'basic.krn', encoding=kp.Encoding.basicKern)
```

## Complex Filtering Strategies

### Combine Multiple Filters

```python
import kernpy as kp

doc, _ = kp.load('complex_score.krn')

# Remove dynamics, keep only kern spines, measures 5-20
kp.dump(
    doc,
    'filtered.krn',
    spine_types=['**kern'],
    exclude={kp.TokenCategory.DYNAMICS},
    from_measure=5,
    to_measure=20
)
```

### Preprocessing Before Export

```python
import kernpy as kp

def prepare_score_for_students(score_file):
    """Create simplified version for students: single spine, no analysis"""
    
    doc, _ = kp.load(score_file)
    
    # Keep only melody (first kern spine)
    spines = doc.get_spines()
    first_kern_idx = next(
        (i for i, s in enumerate(spines) if s.spine_type() == '**kern'),
        None
    )
    
    if first_kern_idx is None:
        print("No kern spine found")
        return None
    
    # Remove ornaments, articulations, and analysis
    kp.dump(
        doc,
        'student_version.krn',
        spine_ids=[first_kern_idx],
        exclude={
            kp.TokenCategory.DECORATION,
            kp.TokenCategory.ORNAMENT,
        }
    )

prepare_score_for_students('full_score.krn')
```

## Practical Export Workflows

### Create Multiple Versions from One Source

```python
import kernpy as kp
from pathlib import Path

def create_score_variants(source_file):
    """Create multiple versions from one source file"""
    
    doc, _ = kp.load(source_file)
    stem = Path(source_file).stem
    
    variants = {
        f'{stem}_full.krn': {},
        f'{stem}_melody_only.krn': {
            'spine_types': ['**kern'],
            'include': {kp.TokenCategory.CORE}
        },
        f'{stem}_no_decoration.krn': {
            'exclude': {kp.TokenCategory.DECORATION}
        },
        f'{stem}_ekern.ekrn': {
            'encoding': kp.Encoding.eKern
        },
        f'{stem}_measures_1_20.krn': {
            'to_measure': 20
        },
    }
    
    for filename, kwargs in variants.items():
        kp.dump(doc, filename, **kwargs)
        print(f"Created {filename}")

create_score_variants('beethoven_op10_no1.krn')
```

### Extract Analysis Layers

```python
import kernpy as kp

doc, _ = kp.load('analyzed_score.krn')

# Layer 1: Harmonic analysis only
kp.dump(
    doc,
    'harmony_only.krn',
    spine_types=['**harm']
)

# Layer 2: Dynamics only
kp.dump(
    doc,
    'dynamics_only.krn',
    spine_types=['**dynam']
)

# Layer 3: Notes with fingering
kp.dump(
    doc,
    'notes_and_fingering.krn',
    spine_types=['**kern', '**fing']
)
```

### Create Performance Editions

```python
import kernpy as kp

def create_performance_edition(score_file, instrument_name):
    """Create performance edition for specific instrument"""
    
    doc, _ = kp.load(score_file)
    spines = doc.get_spines()
    
    # Find kern spine for the instrument (simplified example)
    # In real scenario, look for specific instrument markers
    
    # Create basic performance edition
    kp.dump(
        doc,
        f'{instrument_name}_performance.krn',
        spine_types=['**kern'],  # Notes only
        exclude={
            kp.TokenCategory.ORNAMENT,
            kp.TokenCategory.DYNAMICS,  # Remove dynamics (use another notation)
        }
    )
    
    # Create practice edition with all markings
    kp.dump(
        doc,
        f'{instrument_name}_practice.krn',
        # Keep everything
    )

create_performance_edition('chamber_work.krn', 'violin')
```

## Batch Export Workflows

### Export All Spines Separately

```python
import kernpy as kp
from pathlib import Path

doc, _ = kp.load('score.krn')
spines = doc.get_spines()

output_dir = Path('individual_spines')
output_dir.mkdir(exist_ok=True)

for idx, spine in enumerate(spines):
    spine_type = spine.spine_type()
    
    # Export single spine
    kp.dump(
        doc,
        output_dir / f'spine_{idx}_{spine_type}.krn',
        spine_ids=[idx]
    )
    
    print(f"Exported spine {idx} ({spine_type})")
```

### Create Study Score

```python
import kernpy as kp

def create_study_score(score_file):
    """Create version for musicological study"""
    
    doc, _ = kp.load(score_file)
    
    # Include all content with clear encoding
    kp.dump(
        doc,
        'study_version.ekrn',
        encoding=kp.Encoding.eKern  # Extended kern shows all structure
    )
    
    # Also create simplified
    kp.dump(
        doc,
        'study_simple.krn',
        exclude={kp.TokenCategory.ORNAMENT}
    )

create_study_score('manuscript.krn')
```

## Advanced Filtering Recipes

### Export Only New Music Notation

```python
import kernpy as kp

doc, _ = kp.load('contemporary.krn')

# Keep everything except traditional ornaments
exclude_traditional = {
    kp.TokenCategory.ORNAMENT,
    kp.TokenCategory.NOTATION,  # If present
}

kp.dump(doc, 'modern_notation.krn', exclude=exclude_traditional)
```

### Extract Historical Analysis

```python
import kernpy as kp

doc, _ = kp.load('historically_analyzed.krn')

# Keep harmonic analysis and figured bass
kp.dump(
    doc,
    'harmony_analysis.krn',
    spine_types=['**kern', '**harm', **'fb']  # kern + harmonic + figured bass
)
```

### Create Instrumental Reduction

```python
import kernpy as kp

def create_reduction(full_score_file, reduction_levels=3):
    """Create multiple reduction levels from orchestra score"""
    
    doc, _ = kp.load(full_score_file)
    spines = doc.get_spines()
    kern_ids = [i for i, s in enumerate(spines) if s.spine_type() == '**kern']
    
    # Create reductions at different density levels
    levels = [
        ('full', kern_ids),  # All instruments
        ('main', kern_ids[:len(kern_ids)//2]),  # Half
        ('core', kern_ids[:3]),  # Top 3 staves
        ('essential', [kern_ids[0]]),  # Just top
    ]
    
    stem = full_score_file.rsplit('.', 1)[0]
    
    for level_name, spine_ids in levels:
        kp.dump(
            doc,
            f'{stem}_reduction_{level_name}.krn',
            spine_ids=spine_ids
        )
        print(f"Created {level_name} reduction ({len(spine_ids)} spines)")

create_reduction('brahms_symphony.krn')
```

## Performance and Memory Management

### Efficient Large File Export

```python
import kernpy as kp
from pathlib import Path

# For very large files, process in sections
def export_large_file_in_sections(source_file, section_size=100):
    """Export large file in manageable sections"""
    
    doc, _ = kp.load(source_file)
    total_measures = doc.measures_count()
    
    output_dir = Path('sections')
    output_dir.mkdir(exist_ok=True)
    
    for section_num, start_measure in enumerate(range(1, total_measures + 1, section_size)):
        end_measure = min(start_measure + section_size - 1, total_measures)
        
        kp.dump(
            doc,
            output_dir / f'section_{section_num:03d}.krn',
            from_measure=start_measure,
            to_measure=end_measure
        )
        
        print(f"Exported section {section_num} (measures {start_measure}-{end_measure})")

# Use it
# export_large_file_in_sections('large_work.krn', section_size=50)
```

## Validation and Testing

### Verify Exported Output

```python
import kernpy as kp

def verify_export(source_file, export_kwargs):
    """Verify export works correctly"""
    
    # Load source
    doc, errors = kp.load(source_file)
    if errors:
        print(f"Warning: {len(errors)} issues in source")
    
    # Export with filters
    export_content = kp.dumps(doc, **export_kwargs)
    
    # Verify output can be loaded
    doc_check, check_errors = kp.loads(export_content)
    
    if not doc_check:
        print("ERROR: Exported content cannot be loaded")
        return False
    
    print("✓ Export verified successfully")
    return True

# Use it
verify_export(
    'score.krn',
    {'exclude': {kp.TokenCategory.DECORATION}}
)
```

## See Also

- [Transform Documents Guide](../guides/transform-documents.md) — More filtering patterns
- [Token Categories](../concepts/token-categories.md) — Understanding categories
- [Encodings](../concepts/encodings.md) — Different output formats
- [Document Structure](document-structure.md) — Advanced navigation
