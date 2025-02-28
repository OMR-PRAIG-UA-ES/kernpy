"""
# kernpy

=====


Python Humdrum kern and mens utilities package.



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

While the package is not published in `pip`, the `kernpy` module must be in the root directory.

## 🎯 **kern2ekern**: Convertir un solo archivo .krn a .ekern:

```bash
python -m kernpy --kern2ekern --input_path <input_file>	 <v | --verbose [0-2]>
```

The command has the following arguments:
* **input_path**: Ruta del archivo .krn a convertir.
* **output_path**: Ruta del archivo .ekern a generar (opcional). Si no se especifica, se generará en la misma ubicación.
* **-r**: Recursivo (opcional).
* **--verbose[0-2]**: Nivel de verbosidad (opcional).


📌 Basic usage running **kernpy** as a module:
```shell
python -m kernpy --input_path /my/path/to/file.krn # New ekern generated in /my/path/to/file.ekern
```

📌 Generate an _ekrn_ file in specific location running **kernpy** as a module:
```shell
python -m kernpy --input_path /my/path/to/file.krn --output_path /new/output.ekern
```

📌 Converting all the .krn files in a directory to .ekern files running **kernpy** as a module:
* Every .krn file in the directory will be converted to .ekern in the same location.
* Using, at least, one additional directory level is required.
```
root
├─ kern-folder
│   ├── 1.krn
│   ├── 2.krn
│   └── 3.krn
├── more-kerns
│   ├── 1.krn
│   ├── ...
```
Run:
```shell
python -m kernpy --input_path /my/path/to/directory/ -r
```

✏️ This function is also available as a python function:
```python
# converter.py
from kernpy import kern_to_ekern

kern_to_ekern('/my/path/to/input.krn', '/to/my/output.ekrn')

# Many files
files = ['file1.krn', 'file2.krn', 'file3.krn']
[kern_to_ekern(f) for f in files]

# This function raises an exception if the conversion fails.
# Handle the errors using try-except statement if many files are going to be converted in series.
```

****************************************************************************************
## 🎯 **ekern2kern**: Convertir un solo archivo .ekern a .krn:

```bash
python -m kernpy --ekern2kern --input_path <input_file>	 <--verbose [0-2]>
```

The command has the following arguments:
* **input_path**: Ruta del archivo .ekern a convertir.
* **output_path**: Ruta del archivo .krn a generar (opcional). Si no se especifica, se generará en la misma ubicación.
* **-r**: Recursivo (opcional).
* **--verbose[0-2]**: Nivel de verbosidad (opcional).

* Basic usage running **kernpy** as a module:
```shell
python -m kernpy --input_path /my/path/to/file.ekern # New krn generated in /my/path/to/file.krn
```

📌 Generate a _krn_ file in specific location running **kernpy** as a module:
```shell
python -m kernpy --input_path /my/path/to/file.ekern --output_path /new/output.krn
```

📌 Converting **all** the .ekern files in a directory to .krn files running **kernpy** as a module:

* Every .ekrn file in the directory will be converted to .krn in the same location.
* Using, at least, one additional directory level is required.
```
root
├─ ekern-folder
│   ├── 1.ekrn
│   ├── 2.ekrn
│   └── 3.ekrn
├── more-ekerns
│   ├── 1.ekrn
│   ├── ...
```
Run:
```shell
python -m kernpy --input_path /my/path/to/directory/ -r
```

✏️ This function is also available as a python function:
```python
# converter.py
from kernpy import ekern_to_krn

# Only one file
ekern_to_krn('/my/path/to/input.ekrn', '/to/my/output.krn')

# Many files
files = ['file1.ekrn', 'file2.ekrn', 'file3.ekrn']
[ekern_to_krn(f) for f in files]

# This function raises an exception if the conversion fails.
# Handle the errors using try-except statement if many files are going to be converted in series.
```


****************************************************************************************
## 🎯 **create fragments**
Generate new valid _kern_ files from an original _kern_ file. Every new fragment will be a subset of the original file.

Explore the documentation website for more information about the parameters.


Use:
- **create_fragments_from_kern** to generate using always the same measure length.
- **create_fragments_from_directory** to generate using a Gaussian distribution for the measure length. Static measure is also available if the standard deviation is set to 0.


📌 Create new scores from one original _kern_ directory running **kernpy** as a module:
```shell
python -m kernpy --generate_fragments --input_directory /from/my/kerns --output_directory /to/my/fragments --log_file log.csv  --verbose 2 --mean 4.2 --std_dev 1.5 --offset 1 --num_processes 12
```


✏️ Create new scores from one original _kern_ file:
```python
# generator.py
from kernpy import create_fragments_from_kern

# View docs:
help(create_fragments_from_kern)

create_fragments_from_kern('/my/path/to/input.krn', '/to/my/output_dir/',
                           measure_length=4, offset=1,
                           log_file='/dev/null')
```

✏️ Create new scores from one original _kern_ directory:
- Using, at least, one additional directory level is required.
```
root
├─ kern-folder
│   ├── 1.krn
│   ├── 2.krn
│   └── 3.krn
├── more-kerns
│   ├── 1.krn
│   ├── ...
```

Run:
```python
# generator.py
from kernpy import create_fragments_from_directory

# View docs:
help(create_fragments_from_directory)

create_fragments_from_directory('/my/path/to/input_dir/', '/to/my/output_dir/',
                                mean=4.1, std_dev=0.2, offset=2,
                                log_file='/logs/fragments.csv',
                                num_processes=12)
```



"""


from .core import *

from .io import *

from .util import *

from .polish_scores import *





