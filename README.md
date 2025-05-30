# Python Humdrum **kern and **mens utilities

## Documentation: <a target="_blank" href="https://kernpy.pages.dev/">https://kernpy.pages.dev/</a>

![kernpy logo](https://static.wixstatic.com/media/7a8a67_90be144dbf384480908c3327b93ba97a~mv2.jpg/v1/fill/w_461,h_354,fp_0.46_0.20,q_80,usm_0.66_1.00_0.01,enc_avif,quality_auto/mending-the-sail-1896_jpg!Large.jpg)

## Index:
- [Code examples](#code-examples)
- [Installation](#installation)
- [Documentation](#documentation)
- [Run tests](#run-tests)
- [Contributing](#contributing)
- [Citation](#citation)


## Code examples

### Basic Usage

Load a `**kern`/`**mens` file into a `kp.Document`.
```python
import kernpy as kp

# Read a **kern file
document, errors = kp.load("path/to/file.krn")
```

Load a `**kern`/`**mens` from a string into a `kp.Document`.
```python
import kernpy as kp

document, errors = kp.loads("**kern\n*clefC3\n*k[b-e-a-]\n*M3/4\n4e-\n4g\n4c\n=1\n4r\n2cc;\n==\n*-")
```

Create a new standardized file from a `kp.Document`.
```python
import kernpy as kp

kp.dump(document, "newfile.krn")
```

Save the document in a string from a `kp.Document`.
```python
import kernpy as kp

content = kp.dumps(document)
````

### Exploring different options when creating new files

Only use the specified spines in `spine_types`.
```python
import kernpy as kp

kp.dump(document, "newfile_core.krn",
        spine_types=['**kern'])
kp.dump(document, "newfile_lyrics.krn",
        spine_types=['**text])
kp.dump(document, "newfile_core_and_lyrics.krn",
        spine_types=['*+text'])
```

- Use `include` for selecting the **kern semantic categories **to use**. The output only contains what is passed. By default, all the categories are included.
```python
import kernpy as kp

kp.dump(document, "newfile_only_clefs.krn",
        include={kp.TokenCategory.CLEF})
kp.dump(document, "newfile_only_durations_and_bounding_boxes.krn",
        include={kp.TokenCategory.DURATION, kp.TokenCategory.BOUNDING_BOXES})
```
- Use `exclude` for selecting the **kern semantic categories **to not use**. The output contains everything except what is passed. By default, any category is excluded.
```python
import kernpy as kp

kp.dump(document, "newfile_without_pitches.krn",
        exclude={kp.TokenCategory.PITCH})
kp.dump(document, "newfile_without_durations_or_rests.krn",
        exclude={kp.TokenCategory.BARLINES, kp.TokenCategory.REST})
```
- Use `include` and `exclude` together to select the **kern semantic categories **to use**. The output combines both.
```python
import kernpy as kp

kp.dump(document, "newfile_custom.krn",
        include=kp.BEKERN_CATEGORIES,  # Preloaded set of simple categories
        exclude={kp.TokenCategory.PITCH})
```

- Use `tokenizer` to select how the categories are split. By default, the `normalizedKern` tokenizer is used.

```python
import kernpy as kp

kp.dump(document, "newfile_normalized.krn",
        tokenizer=kp.Encoding.normalizedKern)  # Default tokenizer
```
Select the proper Humdrum **kern tokenizer:

`kernpy` provides different tokenizers to export the content each symbol in different formats.

| Encoding | Tokenized    | Description                            |
|----------|--------------|----------------------------------------|
| kern     | 2.bb-_L      | Traditional Humdrum **kern encoding    |
| ekern    | 2@.@bb@-·_·L | Extended Humdrum **kern encoding       |

Use the `Encoding` enum class to select the tokenizer:

```python
import kernpy as kp

doc, _ = kp.load('resource_dir/legacy/chor048.krn')

kern_content = kp.dumps(doc, tokenizer=kp.Encoding.normalizedKern)
ekern_content = kp.dumps(doc, tokenizer=kp.Encoding.eKern)
```

- Use `from_measure` and `to_measure` to select the measures to export. By default, all the measures are exported.
```python
import kernpy as kp

kp.dump(document, "newfile_1_to_10.krn",
        from_measure=1,  # First from measure 1
        to_measure=10)   # Last measure exported
```

- Use `spine_ids` to select the spines to export. By default, all the spines are exported.
```python
import kernpy as kp

kp.dump(document, "newfile_1_and_2.krn",
        spine_ids=[0, 1])  # Export only the first and the second spine
```

- Use `show_measure_numbers` to select if the measure numbers are shown. By default, the measure numbers are shown.
```python
import kernpy as kp

kp.dump(document, "newfile_no_measure_numbers.krn",
        show_measure_numbers=False)  # Do not show measure numbers
```

- Use all the options at the same time.

```python
import kernpy as kp

kp.dump(document, "newfile.krn",
        spine_types=['**kern'],  # Export only the **kern spines
        include=kp.BEKERN_CATEGORIES,  # Token categories to include
        exclude={kp.TokenCategory.PITCH},  # Token categories to exclude
        tokenizer=kp.Encoding.eKern,  # Kern encoding
        from_measure=1,  # First from measure 1
        to_measure=10,  # Last measure exported
        spine_ids=[0, 1],  # Export only the first and the second spine
        show_measure_numbers=False,  # Do not show measure numbers
        )
```

## Exploring `kernpy` utilities.


- Spines analysis 
Retrieve all the spine types of the document.
```python
import kernpy as kp

kp.spine_types(document)
# ['**kern', '**kern', '**kern', '**kern', '**root', '**harm']

kp.spine_types(document, spine_types=None)
# ['**kern', '**kern', '**kern', '**kern', '**root', '**harm']

kp.spine_types(document, spine_types=['**kern'])
# ['**kern', '**kern', '**kern', '**kern']
```

- Get specific **kern spines.
```python
import kernpy as kp

def how_many_instrumental_spines(document):
    print(kp.spine_types(document, ['**kern']))
    return len(kp.spine_types(document, ['**kern']))
# ['**kern', '**kern', '**kern', '**kern']
# 4

def has_voice(document):
    return len(kp.spine_types(document, ['**text'])) > 0
# True
```



### How many measures are there in the document? Which measures do you want to export?

After reading the score into the `Document` object. You can get some useful data:
```python
first_measure: int = document.get_first_measure()
last_measure: int = document.measures_count()
```

Iterate over all the measures of the document.
```python
import kernpy as kp

doc, _ = kp.load('resource_dir/legacy/chor048.krn')  # 10 measures score
for i in range(doc.get_first_measure(), doc.measures_count(), 1):  # from 1 to 11, step 1
    # Export only the i-th measure (1 long measure scores)
    content_ith_measure = kp.dumps(doc, from_measure=i, to_measure=i)
    
    # Export the i-th measure and the next 4 measures (5 long measure scores)
    if i + 4 <= doc.measures_count():
        content_longer = kp.dumps(doc, from_measure=i, to_measure=i + 4)
    ...
```

It is easier to iterate over all the measures using the `for measure in doc`: loop
(using the `__ iter__` method):
```python
import kernpy as kp

for measure in doc:
    content = kp.dumps(doc, from_measure=measure, to_measure=measure)
    ...
```

Exploring the page bounding boxes.

```python
import kernpy as kp

# Iterate over the pages using the bounding boxes
doc, _ = kp.load('kern_having_bounding_boxes.krn')

# Inspect the bounding boxes
print(doc.page_bounding_boxes)


def are_there_bounding_boxes(doc):
   return len(doc.get_all_tokens(filter_by_categories=[kp.TokenCategory.BOUNDING_BOXES])) > 0


# True

# Iterate over the pages
for page_label, bounding_box_measure in doc.page_bounding_boxes.items():
   print(f"Page: {page_label}"
         f"Bounding box: {bounding_box_measure}"
         f"from_measure: {bounding_box_measure.from_measure}"
         f"to_measure+1: {bounding_box_measure.to_measure}")  # TODO: Check bounds
   kp.dump(doc, f"foo_{page_label}.ekrn",
           spine_types=['**kern'],
           token_categories=kp.BEKERN_CATEGORIES,
           tokenizer=kp.Encoding.eKern,
           from_measure=bounding_box_measure.from_measure,
           to_measure=bounding_box_measure.to_measure - 1  # TODO: Check bounds            
           )
```

### Merge different full kern scores
```python
import kernpy as kp
# NOT AVAILABLE YET!!!
# Pay attention to `kp.merge` too.

# Concat two valid documents
score_a = '**kern\n*clefG2\n=1\n4c\n4d\n4e\n4f\n*-\n'
score_b = '**kern\n*clefG2\n=1\n4a\n4c\n4d\n4c\n*-\n'
concatenated = kp.merge([score_a, score_b])
```

# Concatenate sorted fragments of the same score
```python
import kernpy as kp

fragment_a = '**kern\n*clefG2\n=1\n4c\n4d\n4e\n4f\n*-\n'
fragment_b = '=2\n4a\n4c\n4d\n4c\n*-\n=3\n4a\n4c\n4d\n4c\n*-\n'
fragment_c = '=4\n4a\n4c\n4d\n4c\n*-\n=5\n4a\n4c\n4d\n4c\n*-\n'
fragment_d = '=6\n4a\n4c\n4d\n4c\n*-\n=7\n4a\n4c\n4d\n4c\n*-\n==*-'
fragments = [fragment_a, fragment_b, fragment_c, fragment_d]

doc_merged, indexes = kp.concat(fragments)
for index_pair in indexes:
    from_measure, to_measure = index_pair
    print(f'From measure: {from_measure}, To measure: {to_measure}')
    print(kp.dumps(doc_merged, from_measure=from_measure, to_measure=to_measure))

# Sometimes is useful having a different separator between the fragments rather than the default one (newline)...
doc_merged, indexes = kp.concat(fragments, separator='')
```

### Inspect the `Document` class functions
```python
import kernpy as kp
doc, _ = kp.load('resource_dir/legacy/chor048.krn')  # 10 measures score

frequencies = doc.frequencies()  # All the token categories
filtered_frequencies = doc.frequencies(filter_by_categories=[kp.TokenCategory.SIGNATURES])
frequencies['*k[f#c#]']
# {
#   'occurrences': 4,
#   'category': SIGNATURES,
# }

# Get all the tokens in the document
all_tokens: [kp.Token] = doc.get_all_tokens()
all_tokens_encodings: [str] = doc.get_all_tokens_encodings()

# Get the unique tokens in the document (vocabulary)
unique_tokens: [kp.Token] = doc.get_unique_tokens()
unique_token_encodings: [str] = doc.get_unique_token_encodings()

# Get the line comments in the document
document.get_metacomments()
# ['!!!COM: Coltrane', '!!!voices: 1', '!!!OPR: Blue Train']
document.get_metacomments(KeyComment='COM')
# ['!!!COM: Coltrane']
document.get_metacomments(KeyComment='COM', clear=True)
# ['Coltrane']
document.get_metacomments(KeyComment='non_existing_key')
# []
```

## Transpose
- Inspect what intervals are available for transposing.
```python
import kernpy as kp

print(kp.AVAILABLE_INTERVALS)
```

- Transpose the document to a specific interval.
```python
import kernpy as kp

doc, err = kp.load('resource_dir/legacy/chor048.krn')  # 10 measures score
higher_octave_doc = doc.to_transposed('octave', 'up')

kp.dump(higher_octave_doc, 'higher_octave.krn')
```

### On your own

- Handle the document if needed.
```python
import kernpy as kp

# Access the document tree
print(document.tree)
# <kernpy.core.document.DocumentTree object at 0x7f8b3b3b3d30>

# View the tree-based Document structure for debugging.
kp.graph(document, '/tmp/graph.dot')
# Render the graph 
# - using Graphviz extension in your IDE
# - in the browser here: https://dreampuf.github.io/GraphvizOnline/
```


## Installation

### Production version:
Just install the last version of **kernpy** using pip:
```shell
pip3 uninstall kernpy     # Uninstall the previous version before installing the new one
pip3 install git+https://github.com/OMR-PRAIG-UA-ES/kernpy.git
```

> [!NOTE]
> This module is downloaded by default in the _/tmp_ directory in Linux. So it is removed when shutdown the machine.

<hr>

### Development version:

> [!IMPORTANT]  
> - Add the development dependencies to the `requirements.txt` file.
> - Add the production dependencies to the `pyproject.toml` file.
> - After every change in the grammar, the next steps are mandatory:
> - - Run the `antlr4.sh` script (JAVA required).
> - - Commit & push the changes to the repository.


- Generate antrl4 grammar:
- For generating the Python code required for parsing the **kern files, the shell script `antlr4.sh` inside the `kernpy` package must be run.

```shell
./antlr4.sh
```

Install all the dependencies using the `requirements.txt` file:
```shell
pip install -r requirements.txt
```

Otherwise, install the required packages manually:


- It requires the `antlr4` package to be installed using:
```shell
pip install antlr4-python3-runtime
```


- For visualizing the bounding boxes, the library, the `Pillow` library is required:
```shell
pip install Pillow
```

- To parse a IIIF (International Image Interoperability Framework) manifest in Python, we use the `requests` library to fetch the manifest file:
```shell
pip install requests
```

- If fetching data from `https` fails, install the following version of `urllib`:
```shell
pip install urllib3==1.26.6
```

It has been tested with version 4.13.1 of the package.


## Documentation
Documentation available at [https://kernpy.pages.dev/](https://kernpy.pages.dev/)


**kernpy** also supports been executed as a module. Find out the available commands:
```shell
python -m kernpy --help
python -m kernpy <command> <options>
```


## Run tests:
```shell
cd tests && python -m pytest
```


## Contributing

We welcome contributions from the community! If you'd like to contribute to the project, please follow these steps:

1. Fork the Repository from GitHub.
2. Clone your own fork repository.
   ```bash
   git clone ...
   cd ...
   ```
3. Create a Branch:
4. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature/your-feature-name
    ```
5. Commit Your Changes:
Commit your changes with a descriptive message:
    ```bash
    git commit -m "feat: add your feature or fix"
     ```

6. Push to Your Branch:
Push your changes to your forked repository:
    ```bash
    git push origin feature/your-feature-name
     ```

7. Create a Pull Request:
Open a pull request to the main repository, describing your changes.


## Citation:
```bibtex
@inproceedings{kernpy_mec_2025,
  title={{kernpy: a Humdrum **Kern Oriented Python Package for Optical Music Recognition Tasks}},
  author={Cerveto-Serrano, Joan and Rizo, David and Calvo-Zaragoza, Jorge},
  booktitle={{Proceedings of the Music Encoding Conference (MEC2025)}},
  address={London, United Kingdom},
  year={2025}
}
```

