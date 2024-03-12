# Python Humdrum **kern and **mens utilities

## Documentation
Documentation is available at [https://OMR-PRAIG-UA-ES.github.io/kernpy/](https://OMR-PRAIG-UA-ES.github.io/kernpy/)

## Run as module
```shell
python -m kernpy --help
```


## Installation

Generate antrl4 grammar:
```shell
./antlr4.sh
```


It requires the `antlr4` package to be installed using:
```shell
pip install antlr4-python3-runtime
```

For generating the Python code required for parsing the **kern files, the shell script `antlr4.sh` inside the `kernpy` package must be run

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


****************************************************************************************

## Instrucciones basicas kern2ekern
Siempre tener la carpeta kernpy en el directorio raíz. No está publicado aún el paquete pip.

Para ejecutar como módulo, sin escribir código:
****************************************************************************************
## Convertir un solo archivo .krn a .ekern:
### Genera una archivo en la misma ubicación con la extensión ekern
```bash
python -m kernpy --kern2ekern --input_path <input_file>	 <v | --verbose [0-2]>
```

****************************************************************************************
## Convertir un solo archivo .krn a .ekern:
# Insertar la entrada y la salida:
```bash
python -m kernpy --kern2ekern --input_path <input_kern_file> --output_path <output_ekern_file> <v | --verbose [0-2]>
```

****************************************************************************************
## Recursivo
```bash
python -m kernpy --kern2ekern --input_path <input_dir> -r
```

## Convertir todos los .krn a .ekern en su misma ubicación. 
Ejemplo:
```
python -m kernpy --kern2ekern --input_path /home/joanius/projects/humdrum-polish-scores/prueba-kerns/ -r <v | --verbose [0-2]>
```

****************************************************************************************
## Como código fuente:

```python
# script.py
from kernpy import kern_to_ekern, ekern_to_krn

# Convertir un solo archivo .krn a .ekern:
kern_to_ekern('input.krn', 'output.ekern')

# Convertir un solo archivo .ekern a .krn:
ekern_to_krn('input.ekern', 'output.krn')

# Signatura de tipos: 
# def kern_to_ekern(input_file, output_file) -> None:
# def ekern_to_krn(input_file, output_file) -> None:
# No tienen pérdida.



# ¡OJO! Estas dos funciones lanzan una excepción si no se convierten bien. Gestionar erores con try-catch si se van a ejecutar muchos archivos en serie.
```

