# Python Humdrum **kern and **mens utilities

Docs [here](https://kernpy.pages.dev/)
```shell
https://kernpy.pages.dev/
```

## Index:
- [Installation](#installation)
- [Documentation](#documentation)
- [Run tests](#run-tests)

    
## Installation

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

- To pars- e a IIIF (International Image Interoperability Framework) manifest in Python, we use the `requests` library to fetch the manifest file:
```shell
pip install requests
```

- If the retrieving from `https` fails, the following version of `urllib` must be installed:
```shell
pip install urllib3==1.26.6
```

It has been tested with version 4.13.1 of the package.


## Documentation
Documentation available at [https://kernpy.pages.dev/](https://kernpy.pages.dev/)


Execute the following command to run **kernpy** as a module:
```shell
python -m kernpy --help
python -m kernpy <command> <options>
```

Run `kernpy` from your script:
```python
import kernpy

help(kernpy)
```


## Run tests:
```shell
cd tests && python -m pytest
```
