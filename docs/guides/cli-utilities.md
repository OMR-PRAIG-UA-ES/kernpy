# Guide: Command-Line Utilities

Use kernpy's command-line tools to convert formats and process files from the terminal without writing Python code.

## Overview

kernpy includes several command-line utilities for common tasks:

- `kern2ekern` — Convert **kern files to extended **ekern format
- `ekern2kern` — Convert extended **ekern files back to **kern
- `polish` — Process Polish score datasets

Run kernpy from the command line using:

```bash
python -m kernpy [command] [options]
```

## Get Help

View all available commands:

```bash
python -m kernpy --help
```

View help for a specific command:

```bash
python -m kernpy --help kern2ekern
python -m kernpy --help ekern2kern
python -m kernpy --help polish
```

## Convert kern to eKern

Convert standard **kern files to extended **ekern format, which shows internal token structure.

### Single File Conversion

```bash
python -m kernpy --kern2ekern input.krn output.ekrn
```

This creates `output.ekrn` with all tokens deconstructed to show structure.

### Batch Conversion in Directory

Convert all `.krn` files in a directory:

```bash
python -m kernpy --kern2ekern path/to/scores path/to/output
```

All `.krn` files in `path/to/scores` will be converted and saved as `.ekrn` files in `path/to/output`.

### Recursive Directory Conversion

Process nested directories:

```bash
python -m kernpy --kern2ekern path/to/scores path/to/output --recursive
```

### Verbose Output

See details about each file being processed:

```bash
python -m kernpy --kern2ekern path/to/scores path/to/output -v
```

Or multiple `-v` flags for more detail:

```bash
python -m kernpy --kern2ekern path/to/scores path/to/output -vv
```

**Output example:**

```
kern2ekern: Processing 5 files
Converted: score1.krn → score1.ekrn (156 measures)
Converted: score2.krn → score2.ecn (203 measures)
...
```

## Convert eKern to kern

Convert extended **ekern files back to standard **kern format.

### Single File Conversion

```bash
python -m kernpy --ekern2kern input.ekrn output.krn
```

This removes all `@` and `·` delimiters, producing standard **kern.

### Batch Conversion

```bash
python -m kernpy --ekern2kern path/to/ekern path/to/output
```

Convert all `.ekrn` files in the directory.

### Recursive Conversion

```bash
python -m kernpy --ekern2kern path/to/ekern path/to/output --recursive -v
```

## Polish Dataset Processing

Process the Polish Musical Scores (PMD) dataset:

```bash
python -m kernpy --polish --input_directory /path/to/input --output_directory /path/to/output
```

**Options:**

- `--input_directory` — Input directory containing **kern files
- `--output_directory` — Where to save processed files
- `--kern-spines-filter N` — Keep only spine N (default: 2)
- `--kern-type` — Output format: `krn` or `ekrn` (default: `ekrn`)
- `--remove-empty-dirs` — Clean up empty directories after processing
- `-v`, `--verbose` — Show processing details

**Example:**

```bash
python -m kernpy --polish \
    --input_directory ~/music_data/polish_scores \
    --output_directory ~/processed_polish \
    --kern-type krn \
    --remove-empty-dirs \
    -vv
```

## Practical Workflows

### Convert an Entire Music Library

```bash
# Convert all krn to ekrn in one directory
python -m kernpy --kern2ekern ~/Music/scores ~/Music/scores_extended

# Convert back
python -m kernpy --ekern2kern ~/Music/scores_extended ~/Music/scores_standard
```

### Process Nested Score Collections

```bash
# Recursively convert all files
python -m kernpy --kern2ekern \
    ~/collections/by_composer \
    ~/collections/by_composer_ekern \
    --recursive \
    -v
```

### Inspect Extended Format

Convert to eKern to understand the internal structure:

```bash
python -m kernpy --kern2ekern test_score.krn test_score.ekrn
cat test_score.ekrn | head -20
```

This shows how tokens are broken down internally.

### Batch Processing with Logging

```bash
# Process with maximum verbosity, pipe to log file
python -m kernpy --kern2ekern input_dir output_dir --recursive -vv > conversion.log 2>&1
```

Then review the log:

```bash
grep "Error" conversion.log
grep "Converted" conversion.log | wc -l
```

## Exit Codes

Commands exit with different codes to indicate success or failure:

- `0` — Success
- `1` — General error
- `2` — File not found
- `127` — Unknown command

Use in scripts:

```bash
#!/bin/bash

python -m kernpy --kern2ekern input.krn output.ekrn

if [ $? -eq 0 ]; then
    echo "Conversion successful"
else
    echo "Conversion failed"
    exit 1
fi
```

## Integration with Scripts

### Bash Script for Bulk Processing

```bash
#!/bin/bash

INPUT_DIR="original_scores"
OUTPUT_DIR="converted_scores"

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Convert all files
python -m kernpy --kern2ekern "$INPUT_DIR" "$OUTPUT_DIR" --recursive

# Count results
CONVERTED=$(ls -1 "$OUTPUT_DIR"/**/*.ekrn 2>/dev/null | wc -l)
echo "Converted $CONVERTED files"
```

### Python Script Calling CLI

```python
import subprocess
import sys

# Convert a file using the CLI
result = subprocess.run([
    sys.executable, '-m', 'kernpy',
    '--kern2ekern', 'input.krn', 'output.ekrn'
], capture_output=True, text=True)

if result.returncode == 0:
    print("Successfully converted")
    print(result.stdout)
else:
    print("Conversion failed:")
    print(result.stderr)
```

## Tips and Tricks

### Speed Up Conversion

For large batches, use the recursive option with all files at once:

```bash
# Fast: single command
python -m kernpy --kern2ekern big_dir output_dir --recursive

# Slower: multiple commands
for f in big_dir/*.krn; do
    python -m kernpy --kern2ekern "$f" "output_dir/$(basename $f .krn).ekrn"
done
```

### Verify Conversions

Check that conversions were successful:

```bash
# Count source files
SOURCE_COUNT=$(find input_dir -name "*.krn" | wc -l)

# Count output files
OUTPUT_COUNT=$(find output_dir -name "*.ekrn" | wc -l)

echo "Converted $OUTPUT_COUNT of $SOURCE_COUNT files"
```

### Create Detailed Logs

```bash
# Run conversion with logs
python -m kernpy --kern2ekern input output --recursive -vv 2>&1 | tee conversion_$(date +%s).log

# Analyze the log
grep "Error" conversion*.log | sort | uniq
```

## Limitations

- Command-line tools work best for simple format conversions
- For complex processing with filtering, transposition, etc., use Python scripts instead
- Large batch operations may require substantial disk space

## Hybrid Approach

Combine CLI and Python for powerful workflows:

```bash
#!/bin/bash

# Step 1: Convert all files to ekern (use CLI)
python -m kernpy --kern2ekern input_krn output_ekern --recursive

# Step 2: Run custom Python analysis (would need custom script)
python process_ekern.py output_ekern

# Step 3: Convert back to kern (use CLI)
python -m kernpy --ekern2kern output_ekern final_krn --recursive
```

## Summary

You now know how to:

1. Convert files between kern and ekern formats
2. Batch process directories
3. Use recursive processing for collections
4. Export with verbose logging
5. Integrate CLI commands into scripts

## Next Steps

- **More complex processing?** — Use Python API with [Build Pipelines](build-pipelines.md)
- **Need format details?** — See [Encodings](../concepts/encodings.md)
