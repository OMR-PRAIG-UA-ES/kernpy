# Python Humdrum **kern and **mens utilities

Docs [here](https://kernpy.pages.dev/)
```shell
https://kernpy.pages.dev/
```

## Index:
- [Code example](#code-example)
- [Installation](#installation)
- [Documentation](#documentation)
- [Run tests](#run-tests)


## Code example

Reading `**kern` files.
```python
import kernpy as kp

# Read a **kern file
document, errors = kp.read("path/to/file.krn")
```

Use `kernpy` utilities.

### Spines analysis
- Get all the spines in the document.
```python
kp.get_spine_types(document)
# ['**kern', '**kern', '**kern', '**kern', '**root', '**harm']

kp.get_spine_types(document, spine_types=None)
# ['**kern', '**kern', '**kern', '**kern', '**root', '**harm']
```

- Get specific **kern spines.
```python
def how_many_instrumental_spines(document):
    print(kp.get_spine_types(document, ['**kern']))
    return len(kp.get_spine_types(document, ['**kern']))
# ['**kern', '**kern', '**kern', '**kern']
# 4

def has_voice(document):
    return kp.get_spine_types(document, ['**text']) > 0
# True
```

### On your own

Handle the document if needed.
```python
# Access the document tree
print(document.tree)
# <kernpy.core.document.DocumentTree object at 0x7f8b3b3b3d30>

# View the tree-based Document structure for debugging.
kp.store_graph(document, '/tmp/graph.dot')
# Render the graph 
# - using Graphviz extension in your IDE
# - in the browser here: https://dreampuf.github.io/GraphvizOnline/
```

### Create the new score using your owb options:

Create your options to export the document.
```
# Create the options to export the document
default_options = kp.ExportOptions()

# Customize the ExportOptions object
your_options = kp.ExportOptions(
    spine_types=['**kern'],  # Export only the **kern spines
    token_categories=kp.BEKERN_CATEGORIES,
    kern_type=kp.KernTypeExporter.eKern,
    from_measure=1,  # Start from measure 1
    to_measure=10,
)
```

Extract the new score using the options.
```

# Store the document in a new file
kp.store(document, "path/to/newfile.ekrn", your_options)

# or store the document as a string
content = kp.export(document, your_options)
```


### How many measures are there in the document? Which measures do you want to export?

After reading the score into the `Document` object. You can get some useful data:
```python
first_measure: int = document.get_first_measure()
last_measure: int = document.measures_count()
```

Iterate over all the measures of the document.
```python
doc, _ = kp.read('resource_dir/legacy/chor048.krn')  # 10 measures score
for i in range(doc.get_first_measure(), doc.measures_count(), 1):  # from 1 to 11, step 1
    # Export only the i-th measure (1 long measure scores)
    options = kp.ExportOptions(from_measure=i, to_measure=i)
    content_ith_measure = kp.export(doc, options)
    
    # Export the i-th measure and the next 4 measures (5 long measure scores)
    if i + 4 <= doc.measures_count():
        options_longer = kp.ExportOptions(from_measure=i, to_measure=i + 4)
        content_longer = kp.export(doc, options_longer)
    ...
```

When iterating over all the measures is easier using the `for measure in doc:` loop.
(using the __ iter__ method):
```python
for measure in doc:
    options = kp.ExportOptions(from_measure=measure, to_measure=measure)
    content = kp.export(doc, options)
    ...
```

Exploring the page bounding boxes. 
```python
# Iterate over the pages using the bounding boxes
doc, _ = kp.read('kern_having_bounding_boxes.krn')

# Inspect the bounding boxes
print(doc.page_bounding_boxes)
def are_there_bounding_boxes(doc):
    return len(doc.get_all_tokens(filter_by_categories=[kernpy.TokenCategory.BOUNDING_BOXES])) > 0
# True

# Iterate over the pages
for page_label, bounding_box_measure in doc.page_bounding_boxes.items():
    print(f"Page: {page_label}"
          f"Bounding box: {bounding_box_measure}"
          f"from_measure: {bounding_box_measure.from_measure}"
          f"to_measure+1: {bounding_box_measure.to_measure}")  # TODO: Check bounds
    options = kp.ExportOptions(
        spine_types=['**kern'],
        token_categories=kp.BEKERN_CATEGORIES,
        kern_type=kp.KernTypeExporter.eKern,
        from_measure=bounding_box_measure.from_measure,
        to_measure=bounding_box_measure.to_measure - 1  # TODO: Check bounds
    )
    kp.store(doc, f"foo_{page_label}.ekrn", options)

```

```python
# NOT AVAILABLE YET!!!
# Concat two documents
score_a = '**kern\n*clefG2\n=1\n4c\n4d\n4e\n4f\n*-\n'
score_b = '**kern\n*clefG2\n=1\n4a\n4c\n4d\n4c\n*-\n'
concatenated = kp.concat(
    contents=[score_a, score_b],
    options=kp.ExportOptions(kern_type=kp.KernTypeExporter.eKern),
)
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

- If the retrieving from `https` fails, the following version of `urllib` must be installed:
```shell
pip install urllib3==1.26.6
```

It has been tested with version 4.13.1 of the package.


- For visualizing the progress bar executing multiple tasks, the `tqdm` library is required:
```shell
pip install tqdm
```

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
