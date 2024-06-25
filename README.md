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

```python
import kernpy.core
import kernpy as kp

# Read a **kern file
document, errors = kp.read("path/to/file.krn")

# Handle the document if needed
print(document.tree)
kp.get_spine_types(document)
# ['**kern', '**kern', '**kern', '**kern', '**root', '**harm']

kp.get_spine_types(document, None)
# ['**kern', '**kern', '**kern', '**kern', '**root', '**harm']

kp.get_spine_types(document, ['**kern'])
# ['**kern', '**kern', '**kern', '**kern']

# Create the options to export the document
default_options = kp.ExportOptions()

# Explore the ExportOptions class
your_options = kp.ExportOptions(
    spine_types=['**kern'],  # Export only the **kern spines
    token_categories=kp.BEKERN_CATEGORIES,
    kern_type=kp.KernTypeExporter.eKern,
    from_measure=1,  # Start from measure 1
    to_measure=10,
)

# Store the document in a new file
kp.store(document, "path/to/newfile.ekrn", your_options)

# or store the document as a string
content = kp.export(document, your_options)

# Iterate over the document
doc, _ = kp.read('resource_dir/legacy/chor048.krn')  # 10 measures score
for i in range(doc.get_first_measure(), doc.measures_count() + 1, 1):  # from 1 to 11, step 1
    # Export only the i-th measure (1 long measure scores)
    options = kp.ExportOptions(from_measure=i, to_measure=i)
    # Export the i-th measure and the next 4 measures (5 long measure scores)
    options_longer = kp.ExportOptions(from_measure=i, to_measure=i + 4)
    content = kp.export(doc, options)
    ...

# Or use the __iter__ method
for measure in doc:
    options = kp.ExportOptions(from_measure=measure, to_measure=measure)
    content = kp.export(doc, options)
    ...

# Iterate over the pages using the bounding boxes
doc, _ = kp.read('kern_having_bounding_boxes.krn')

# Inspect the bounding boxes
print(doc.page_bounding_boxes)
print(len(doc.get_all_tokens(filter_by_categories=[kernpy.TokenCategory.BOUNDING_BOXES])) > 0)

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


# Concat two documents
score_a = '**kern\n*clefG2\n=1\n4c\n4d\n4e\n4f\n*-\n'
score_b = '**kern\n*clefG2\n=1\n4a\n4c\n4d\n4c\n*-\n'
concatenated = kp.concat(score_a, score_b)
```


## Installation

### Production version:
Just install the last version of **kernpy** using pip:
```shell
pip install git+https://github.com/OMR-PRAIG-UA-ES/kernpy.git 
```

> [!NOTE]
> This module is downloaded by default in the _/tmp_ directory. So it is removed when shutdown the machine.

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
