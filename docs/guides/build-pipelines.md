# Guide: Build Pipelines

Learn how to process collections of scores, batch-transform documents, and build automated workflows.

## Process Multiple Files

### Basic Batch Loop

Process all files in a directory:

```python
import kernpy as kp
from pathlib import Path

score_dir = Path('scores')

# Process all .krn files in a directory
for krn_file in score_dir.glob('*.krn'):
    doc, errors = kp.load(krn_file)
    
    if not errors:
        # Do something with the document
        print(f"Processed: {krn_file.name} ({doc.measures_count()} measures)")
    else:
        print(f"Skipped {krn_file.name}: {len(errors)} errors")
```

### Save Transformed Results

```python
import kernpy as kp
from pathlib import Path

input_dir = Path('original_scores')
output_dir = Path('processed_scores')
output_dir.mkdir(exist_ok=True)

# Process and save each file
for krn_file in input_dir.glob('*.krn'):
    doc, _ = kp.load(krn_file)
    
    # Transform
    doc_transposed = doc.to_transposed('M2', 'up')
    
    # Save with new name
    output_file = output_dir / f'transposed_{krn_file.name}'
    kp.dump(doc_transposed, output_file)
    
    print(f"Saved: {output_file.name}")
```

## Batch Transposition

Create variations in multiple keys:

```python
import kernpy as kp
from pathlib import Path

input_file = 'score.krn'
output_dir = Path('transpositions')
output_dir.mkdir(exist_ok=True)

doc, _ = kp.load(input_file)

# Generate versions in different keys
intervals = ['P1', 'M2', 'M3', 'P4', 'P5', 'M6', 'M7', 'P8']

for interval in intervals:
    transposed = doc.to_transposed(interval, 'up')
    output_file = output_dir / f'transposed_{interval}.krn'
    kp.dump(transposed, output_file)
    print(f"Created: {output_file.name}")
```

## Concatenate Multiple Scores

Combine fragments into a single document:

```python
import kernpy as kp

# Load multiple kern strings or files
fragments = []
for i in range(1, 4):
    with open(f'fragment_{i}.krn') as f:
        fragments.append(f.read())

# Concatenate them
combined_doc, fragment_ranges = kp.concat(fragments)

# Fragment_ranges tells you which measures belong to which fragment
print(f"Combined into {combined_doc.measures_count()} measures")
print(f"Fragment boundaries: {fragment_ranges}")

# Save the result
kp.dump(combined_doc, 'combined.krn')
```

## Merge Multiple Scores

Combine scores with different structures:

```python
import kernpy as kp

# Create a merged document from multiple scores
fragments = [
    open('score1.krn').read(),
    open('score2.krn').read(),
    open('score3.krn').read(),
]

merged_doc, ranges = kp.merge(fragments)

print(f"Merged document: {merged_doc.measures_count()} measures")
kp.dump(merged_doc, 'merged.krn')
```

## Extract and Organize by Measure

### Split Score into Individual Measures

```python
import kernpy as kp
from pathlib import Path

doc, _ = kp.load('score.krn')
output_dir = Path('measures')
output_dir.mkdir(exist_ok=True)

first = doc.get_first_measure()
last = doc.measures_count()

for measure_num in range(first, last + 1):
    # Extract single measure
    kp.dump(doc, output_dir / f'measure_{measure_num}.krn',
            from_measure=measure_num,
            to_measure=measure_num)
    print(f"Extracted measure {measure_num}")
```

### Group Measures by Size

```python
import kernpy as kp
from pathlib import Path

doc, _ = kp.load('score.krn')

first = doc.get_first_measure()
last = doc.measures_count()
group_size = 8  # Group by 8 measures

for group_start in range(first, last + 1, group_size):
    group_end = min(group_start + group_size - 1, last)
    
    output_file = f'section_{group_start:03d}_to_{group_end:03d}.krn'
    kp.dump(doc, output_file,
            from_measure=group_start,
            to_measure=group_end)
    print(f"Saved: {output_file}")
```

## Parallel Processing

Process large collections efficiently (using multiprocessing):

```python
import kernpy as kp
from pathlib import Path
from multiprocessing import Pool

def process_file(krn_file):
    """Process a single file"""
    try:
        doc, errors = kp.load(krn_file)
        if not errors:
            # Save a filtered version
            output_file = f'filtered_{krn_file.stem}.krn'
            kp.dump(doc, output_file,
                   spine_types=['**kern'])
            return (krn_file.name, 'success')
        else:
            return (krn_file.name, f'{len(errors)} errors')
    except Exception as e:
        return (krn_file.name, f'failed: {e}')

# Process all files in parallel
score_files = list(Path('scores').glob('*.krn'))

with Pool(processes=4) as pool:  # Use 4 processes
    results = pool.map(process_file, score_files)

# Print results
for filename, status in results:
    print(f"{filename}: {status}")
```

## Create Dataset Inventory

Analyze and catalog a collection:

```python
import kernpy as kp
from pathlib import Path
import csv

score_dir = Path('scores')
results = []

for krn_file in sorted(score_dir.glob('*.krn')):
    try:
        doc, errors = kp.load(krn_file)
        
        spines = doc.get_spines()
        spine_types = [s.header for s in spines]
        
        results.append({
            'filename': krn_file.name,
            'measures': doc.measures_count(),
            'spines': len(spines),
            'types': ','.join(spine_types),
            'errors': len(errors)
        })
    except Exception as e:
        results.append({
            'filename': krn_file.name,
            'measures': 'N/A',
            'spines': 'N/A',
            'types': 'N/A',
            'errors': str(e)
        })

# Save to CSV
with open('inventory.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['filename', 'measures', 'spines', 'types', 'errors'])
    writer.writeheader()
    writer.writerows(results)

print(f"Cataloged {len(results)} files in inventory.csv")
```

## Conditional Processing

Process files differently based on their content:

```python
import kernpy as kp
from pathlib import Path

output_dir_satb = Path('satb_scores')
output_dir_solo = Path('solo_scores')
output_dir_other = Path('other_scores')

for directory in [output_dir_satb, output_dir_solo, output_dir_other]:
    directory.mkdir(exist_ok=True)

for krn_file in Path('scores').glob('*.krn'):
    doc, _ = kp.load(krn_file)
    spines = doc.get_spines()
    spine_count = len(spines)
    
    if spine_count == 4:
        # SATB score
        kp.dump(doc, output_dir_satb / krn_file.name)
        print(f"→ SATB: {krn_file.name}")
    elif spine_count == 1:
        # Solo score
        kp.dump(doc, output_dir_solo / krn_file.name)
        print(f"→ Solo: {krn_file.name}")
    else:
        # Other
        kp.dump(doc, output_dir_other / krn_file.name)
        print(f"→ Other ({spine_count} spines): {krn_file.name}")
```

## Filter and Archive Subsets

Extract specific types of files:

```python
import kernpy as kp
from pathlib import Path

score_dir = Path('all_scores')
target_measures = Path('short_pieces')
target_measures.mkdir(exist_ok=True)

min_measures = 30
max_measures = 50

for krn_file in score_dir.glob('*.krn'):
    doc, _ = kp.load(krn_file)
    measure_count = doc.measures_count()
    
    if min_measures <= measure_count <= max_measures:
        kp.dump(doc, target_measures / krn_file.name)
        print(f"Archived: {krn_file.name} ({measure_count} measures)")
```

## Build a Transposition Library

Create a library of transpositions of a single work:

```python
import kernpy as kp
from pathlib import Path

work_file = 'my_composition.krn'
library_dir = Path('transposition_library')
library_dir.mkdir(exist_ok=True)

doc, _ = kp.load(work_file)

base_name = Path(work_file).stem

# Create versions in all 12 chromatic transpositions
semitone_intervals = {
    0: ('C', 'P1'),
    1: ('Db', 'm2'),
    2: ('D', 'M2'),
    3: ('Eb', 'm3'),
    4: ('E', 'M3'),
    5: ('F', 'P4'),
    6: ('Gb', 'd5'),
    7: ('G', 'P5'),
    8: ('Ab', 'm6'),
    9: ('A', 'M6'),
    10: ('Bb', 'm7'),
    11: ('B', 'M7'),
}

for semitones, (note_name, interval) in semitone_intervals.items():
    if interval == 'P1':
        transposed = doc  # No transposition needed
    else:
        transposed = doc.to_transposed(interval, 'up')
    
    filename = library_dir / f'{base_name}_in_{note_name}.krn'
    kp.dump(transposed, filename)
    print(f"Created: {filename.name}")

print("Transposition library complete!")
```

## Error Handling in Batch Processing

```python
import kernpy as kp
from pathlib import Path

score_dir = Path('scores')
error_log = []
success_count = 0

for krn_file in score_dir.glob('*.krn'):
    try:
        doc, errors = kp.load(krn_file)
        
        if errors:
            error_log.append((krn_file.name, errors))
            print(f"⚠ {krn_file.name}: {len(errors)} parsing issues")
        else:
            success_count += 1
            # Process the file
            kp.dump(doc, f'processed_{krn_file.name}')
            
    except Exception as e:
        error_log.append((krn_file.name, str(e)))
        print(f"✗ {krn_file.name}: {e}")

print(f"\nSummary: {success_count} successful, {len(error_log)} failed")

# Optionally save error log
with open('error_log.txt', 'w') as f:
    for filename, errors in error_log:
        f.write(f"{filename}:\n")
        f.write(f"  {errors}\n")
```

## Summary

You now know how to:

1. Process collections of files efficiently
2. Create variations in multiple keys
3. Concatenate and merge documents
4. Extract subsets and organize by measures
5. Create indexes and catalogues
6. Build transposition libraries
7. Handle errors in batch workflows

## Next Steps

- **Command-line tools?** — See [CLI Utilities](cli-utilities.md)
- **Learn about document structure?** — See [Document Structure](../advanced/document-structure.md)
