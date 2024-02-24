# Python Humdrum **kern and **mens utilities

## Documentation
Documentation is available at [https://OMR-PRAIG-UA-ES.github.io/pykern/](https://OMR-PRAIG-UA-ES.github.io/pykern/)


It requires the `antlr4` package to be installed using:
```shell
pip install antlr4-python3-runtime
```

For generating the Python code required for parsing the **kern files, the shell script `antlr4.sh` inside the `pykern` package must be run

For visualizing the bounding boxes, the library, the `Pillow` library is required:
```shell
pip install Pillow
```

To parse a IIIF (International Image Interoperability Framework) manifest in Python, we use the `requests` library to fetch the manifest file:
```shell
pip install requests
```
If the retrieving from `https` fails, the following version of `urllib` must be installed:
```shell
pip install urllib3==1.26.6
```

It has been tested with version 4.13.1 of the package.


## Run tests:
```shell
make tests
```

