# Do You Have Questions?

<div style="text-align: center; margin-bottom: 40px;">
  <h2 style="margin-bottom: 10px;">Explore this few ones</h2>
  <p style="color: #666; font-size: 16px; margin-bottom: 20px;">
    Can't find the answer you're looking for? Check our <a href="guides/parse-and-analyze.md">Practical Guides</a>, 
    <a href="examples.md">Code Examples</a>, or <a href="get-started.md">Getting Started</a> documentation.
  </p>
  <img src="https://via.placeholder.com/600x300?text=kernpy+FAQ" alt="kernpy FAQ Illustration" style="max-width: 600px; width: 100%; height: auto; border-radius: 8px;">
</div>

<hr style="margin: 50px 0;">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 40px; margin-bottom: 50px;">
  
  <div style="padding-right: 20px;">
    <ul style="list-style: none; padding: 0;">
      
      <li style="margin-bottom: 25px;">
        <p style="font-weight: bold; margin-bottom: 8px;">
          <span style="color: #007bff;">1.</span> 
          <a href="#installation" style="text-decoration: none; color: #333;">How do I install kernpy?</a>
        </p>
      </li>
      
      <li style="margin-bottom: 25px;">
        <p style="font-weight: bold; margin-bottom: 8px;">
          <span style="color: #007bff;">2.</span> 
          <a href="#import-error" style="text-decoration: none; color: #333;">I get ModuleNotFoundError. What should I do?</a>
        </p>
      </li>
      
      <li style="margin-bottom: 25px;">
        <p style="font-weight: bold; margin-bottom: 8px;">
          <span style="color: #007bff;">3.</span> 
          <a href="#python-versions" style="text-decoration: none; color: #333;">What Python versions does kernpy support?</a>
        </p>
      </li>
      
      <li style="margin-bottom: 25px;">
        <p style="font-weight: bold; margin-bottom: 8px;">
          <span style="color: #007bff;">4.</span> 
          <a href="#file-formats" style="text-decoration: none; color: #333;">What file formats does kernpy support?</a>
        </p>
      </li>

      <li style="margin-bottom: 25px;">
        <p style="font-weight: bold; margin-bottom: 8px;">
          <span style="color: #007bff;">5.</span> 
          <a href="#load-vs-loads" style="text-decoration: none; color: #333;">What's the difference between load() and loads()?</a>
        </p>
      </li>

    </ul>
  </div>

  <div style="padding-left: 20px;">
    <ul style="list-style: none; padding: 0;">
      
      <li style="margin-bottom: 25px;">
        <p style="font-weight: bold; margin-bottom: 8px;">
          <span style="color: #007bff;">6.</span> 
          <a href="#transpose" style="text-decoration: none; color: #333;">How do I transpose a score?</a>
        </p>
      </li>

      <li style="margin-bottom: 25px;">
        <p style="font-weight: bold; margin-bottom: 8px;">
          <span style="color: #007bff;">7.</span> 
          <a href="#filtering" style="text-decoration: none; color: #333;">How do I filter out certain information?</a>
        </p>
      </li>

      <li style="margin-bottom: 25px;">
        <p style="font-weight: bold; margin-bottom: 8px;">
          <span style="color: #007bff;">8.</span> 
          <a href="#single-spine" style="text-decoration: none; color: #333;">How do I extract just one spine or instrument?</a>
        </p>
      </li>

      <li style="margin-bottom: 25px;">
        <p style="font-weight: bold; margin-bottom: 8px;">
          <span style="color: #007bff;">9.</span> 
          <a href="#performance" style="text-decoration: none; color: #333;">The library seems slow. Any tips?</a>
        </p>
      </li>

      <li style="margin-bottom: 25px;">
        <p style="font-weight: bold; margin-bottom: 8px;">
          <span style="color: #007bff;">10.</span> 
          <a href="#deprecated" style="text-decoration: none; color: #333;">What happened to the old API functions?</a>
        </p>
      </li>

    </ul>
  </div>

</div>

<hr style="margin: 50px 0;">

## Detailed Answers

### <a id="installation"></a>1. How do I install kernpy?

The easiest way is to use pip:

```bash
pip install kernpy
```

For the latest development version:

```bash
pip install git+https://github.com/OMR-PRAIG-UA-ES/kernpy.git
```

See [Getting Started](get-started.md) for more options.

---

### <a id="import-error"></a>2. I get `ModuleNotFoundError` when importing kernpy. What should I do?

1. Verify it's installed: `pip show kernpy`
2. Reinstall if needed: `pip install --force-reinstall kernpy`
3. Check your Python environment:
   - If using a virtual environment, ensure it's activated
   - Check `python --version` matches the command you installed with
4. Try importing with absolute path: `python -c "import kernpy; print(kernpy.__version__)"`

---

### <a id="python-versions"></a>3. What Python versions does kernpy support?

kernpy requires Python 3.9 or later. Check your version with:

```bash
python --version
```

---

### <a id="file-formats"></a>4. What file formats does kernpy support?

kernpy primarily supports **kern and **mens notation in Humdrum format (.krn, .mens, .ekrn, etc.). All must be plain text files.

kernpy reports parsing issues as warnings, not fatal errors. You can usually still work with the document:

```python
import kernpy as kp

doc, errors = kp.load('score.krn')
if errors:
    print(f"Found {len(errors)} issues, but loaded doc has {doc.measures_count()} measures")
```

To be strict about errors:

```python
try:
    doc, errors = kp.load('score.krn', raise_on_errors=True)
except ValueError as e:
    print(f"Fatal parsing error: {e}")
```

---

### <a id="load-vs-loads"></a>5. What's the difference between `load()` and `loads()`?

- `load(filename)` — Reads from a file on disk
- `loads(string)` — Parses from a string already in memory

Choose based on your data source:

```python
# From disk
doc, errors = kp.load('score.krn')

# From a string or variable
content = "**kern\n*M4/4\n4c\n*-"
doc, errors = kp.loads(content)
```

---

### <a id="transpose"></a>6. How do I transpose a score?

Use the `to_transposed()` method:

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Transpose up a perfect 4th
transposed = doc.to_transposed('P4', 'up')
kp.dump(transposed, 'transposed.krn')

# Transpose down
transposed_down = doc.to_transposed('M2', 'down')
```

See [Transposition Guide](advanced/transposition.md) for all intervals.

---

### <a id="filtering"></a>7. How do I filter out certain types of information?

Use token categories:

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# Remove decorations (articulations)
kp.dump(doc, 'no_decorations.krn',
        exclude={kp.TokenCategory.DECORATION})

# Keep only core music
kp.dump(doc, 'core_only.krn',
        include={kp.TokenCategory.CORE,
                 kp.TokenCategory.SIGNATURES,
                 kp.TokenCategory.BARLINES})
```

See [Token Categories](concepts/token-categories.md) for details.

---

### <a id="single-spine"></a>8. How do I extract just one spine or instrument?

```python
import kernpy as kp

doc, _ = kp.load('score.krn')

# By type
kp.dump(doc, 'kern_only.krn', spine_types=['**kern'])

# By index
kp.dump(doc, 'first_spine.krn', spine_ids=[0])

# Multiple spines
kp.dump(doc, 'first_two.krn', spine_ids=[0, 1])
```

---

### <a id="performance"></a>9. The library seems slow when processing many files. Any tips?

1. Process in parallel using Python's `multiprocessing`:

```python
from multiprocessing import Pool
import kernpy as kp

def process(filename):
    doc, _ = kp.load(filename)
    # ... do something
    return result

with Pool(4) as p:
    results = p.map(process, file_list)
```

2. Use batch operations instead of loops where possible
3. Profile with Python's built-in profiler:

```python
import cProfile
cProfile.run('kp.load("large_file.krn")')
```

For large files running out of memory:

1. Process by measures instead of loading entire document
2. Use filtering to reduce data size:

```python
kp.dump(doc, 'smaller.krn',
        spine_types=['**kern'],  # Only notes
        exclude={kp.TokenCategory.DECORATION})  # No extra data
```

---

### <a id="deprecated"></a>10. What happened to the old API functions?

These older functions are deprecated. Use the modern API instead:

| Old | New | Purpose |
|-----|-----|---------|
| `read()` | `load()` | Read file from disk |
| `create()` | `loads()` | Parse from string |
| `export()` | `dumps()` | Export to string |
| `store()` | `dump()` | Write to file |

See [API Reference](reference.md) for migration details.

Old code example:

```python
# OLD (deprecated)
doc = HumdrumImporter().import_file('score.krn')

# NEW (recommended)
doc, errors = kp.load('score.krn')
```

---

## Still Have Questions?

If you don't find your answer here:

1. Check the [full documentation](index.md)
2. Search [GitHub Issues](https://github.com/OMR-PRAIG-UA-ES/kernpy/issues) for similar questions
3. Create a new issue if needed

---

<div style="text-align: center; margin-top: 60px; padding: 40px; background-color: #f8f9fa; border-radius: 8px;">
  <h3 style="margin-top: 0;">Don't hesitate to contact us! 😊</h3>
  <p style="color: #666; margin-bottom: 20px;">Found something wrong? Have a suggestion? We'd love to hear from you!</p>
  <p>
    <a href="https://github.com/OMR-PRAIG-UA-ES/kernpy/issues" style="display: inline-block; padding: 10px 20px; background-color: #007bff; color: white; text-decoration: none; border-radius: 4px; font-weight: bold;">
      Open an Issue on GitHub
    </a>
  </p>
  <p style="color: #999; font-size: 14px; margin-top: 15px;">
    Or visit our <a href="https://praig.ua.es/">research group website</a> to learn more about kernpy and related projects.
  </p>
</div>
