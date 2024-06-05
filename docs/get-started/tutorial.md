# Tutorial: Learning `kernpy` in 5 minutes.

This is a short introduction to `kernpy`. It will guide you through the main concepts and show you how to use the package in a few minutes.

When using `kernpy`, you should be familiar with the Humdrum **kern encodings. You can easily find information in:

- [Verovio Humdrum Viewer](https://verovio.humdrum.org/){:target="_blank"}
- [Verovio Humdrum Viewer Documentation](https://doc.verovio.humdrum.org/humdrum/getting_started/){:target="_blank"}


## Running the code

`kernpy` is able to be run as a normal snippet of code or as a module by command line interface.

<h3> Usually, we recommend the import as: </h3>
```python
import kernpy
```

<h3> Also, you can run the code as a module by command line interface. </h3>
```bash
python -m kernpy --help
```

## What is Humdrum **kern?

First of all, let's see what a Humdrum **kern file looks like:
```kern
**kern
*clefG2
*M4/4
*met(c)
=1
4c
4d
4e
4f
=2
*M3/2
2g
2f
2d
=
*-
```
![Example in **kern](../assets/001.svg)


## Let's code!



We can do some operations with the score.

First of all, let's import the score:

```python
import kernpy as kp
document, errors = kp.read('/path/to/file.krn')
```

Now, we can access the score attributes:

```python
import kernpy as kp
document, _ = kp.read('/path/to/file.krn')
print(document.tree)
# <kernpy.core.document.DocumentTree object at 0x7f8b3b3b3d30>
```

Let's dive into the different ways to export the `Document`.
```python
import kernpy as kp

# Select your measures to export
middle_measures_options = kp.ExportOptions(from_measure=4, to_measure=8)

# Select your voices to export
saxophone_options = kp.ExportOptions(instruments=['saxophone'])

# Select the token categories to export
core_options = kp.ExportOptions(token_categories=[kp.TokenCategory.CORE, kp.TokenCategory.BARLINES, kp.TokenCategory.SIGNATURES])

# Select the token categories to export using the predefined categories
bekern_options = kp.ExportOptions(token_categories=kp.BEKERN_CATEGORIES)

# Select the encoding to export
normalized_kern_options = kp.ExportOptions(kern_type=kp.KernTypeExporter.normalizedKern)

# Select a list of filters to export
all_options = kp.ExportOptions(
    kern_type=kp.KernTypeExporter.eKern,
    instruments=['saxophone'],
    from_measure=1,
    to_measure=2,
    token_categories=kp.BEKERN_CATEGORIES
)
```

Using the `Document` object, we can export the score:
```python
import kernpy as kp
document, errors = kp.read('/path/to/file.krn')
options = kp.ExportOptions()
kp.store(document, '/path/to/export/file.krn', options)
```

Or we can export the score as a string for further processing:
```python
import kernpy as kp
document, errors = kp.read('/path/to/file.krn')
options = kp.ExportOptions()
content = kp.export(document, options)
...  # you can use the content as you want
print(content)
```


<br>

## Let's use low-level functions:

Load the file directly using the content of the file:    
Examples:
```python
import kernpy

importer = kernpy.Importer()
document = importer.import_string('**kern\n*clefG2\n*M4/4\n*met(c)\n=1\n4c\n4d\n4e\n4f\n=2\n*M3/2\n2g\n2f\n2d\n=\n*-')
print(document.get_metacomments())
```

Or load the file using the path to the file:
```python
import kernpy

importer = kernpy.Importer()
document = importer.import_file('path/to/file.krn')
print(document.get_metacomments())
```

Then you can access to the score attributes:

```python
print(type(document))
# <class 'kernpy.core.document.Document'>

print(document.tree)
# <kernpy.core.document.DocumentTree object at 0x7f8b3b3b3d30>

print(document.voices)
# ['saxophone', 'clarinet', 'piano']
```

Now, you can export the score using the `ExportOptions` class:

```python
export_options = kernpy.ExportOptions()
exporter = kernpy.Exporter()
content = exporter.export_string(document, export_options)
print(content)
```

Save the score to a file:
```python
export_options = kernpy.ExportOptions()
exporter = kernpy.Exporter()
content = exporter.export_string(document, export_options)
with open('path/to/file.krn', 'w') as file:
    file.write(content)
```

<h4>Let's filter the export options:</h4>

Select the voices to export:
```python
export_options = kernpy.ExportOptions(voices=['saxophone'])
exporter = kernpy.Exporter()
content = exporter.export_string(document, export_options)
print(content)
```

Select the measures to export:
```python
export_options = kernpy.ExportOptions(from_measure=1, to_measure=2)
exporter = kernpy.Exporter()
content = exporter.export_string(document, export_options)
print(content)
```

Select the token categories to export:
Let's see the `kernpy.TokenCategory` enum class to choose the categories:
```python
export_options = kernpy.ExportOptions(token_categories=[
    kernpy.TokenCategory.STRUCTURAL, 
    kernpy.TokenCategory.CORE, 
    kernpy.TokenCategory.EMPTY, 
    kernpy.TokenCategory.SIGNATURES,
    kernpy.TokenCategory.BARLINES,
])
exporter = kernpy.Exporter()
content = exporter.export_string(document, export_options)
print(content)
```
Actually, you can use the predefined categories:
```python
export_options = kernpy.ExportOptions(token_categories=kernpy.BEKERN_CATEGORIES)
exporter = kernpy.Exporter()
content = exporter.export_string(document, export_options)
print(content)
```

Select the encoding to export:
```python
export_options = kernpy.ExportOptions(kern_type=kernpy.KernTypeExporter.normalizedKern)
exporter = kernpy.Exporter()
content = exporter.export_string(document, export_options)
print(content)
```

Select a list of filters to export:
```python
export_options = kernpy.ExportOptions(
    kern_type=kernpy.KernTypeExporter.eKern,
    instruments=['saxophone'],
    from_measure=1,
    to_measure=2
    token_categories=kernpy.BEKERN_CATEGORIES
)
```


<h3>Let's see the score in a graphical representation:</h3>

Show the graph representation of the score:
Use `Graphviz` to show the score in a graphical representation.

```python
import kernpy

importer = kernpy.Importer()
document = importer.import_string('**kern\n*clefG2\n*M4/4\n*met(c)\n=1\n4c\n4d\n4e\n4f\n=2\n*M3/2\n2g\n2f\n2d\n=\n*-')
dot_exporter = kernpy.GraphvizExporter()
dot_exporter.export_to_dot(document.tree, '/tmp/minimal.dot')
```

You can use Graphviz Dot Online editors to see the graphical representation of the score:
- [Graphviz Online](https://dreampuf.github.io/GraphvizOnline/){:target="_blank"}


## Next steps
Congratulations! You have learned the basics of `kernpy`. Now you can start using the package in your projects.

Go to the [API reference](../reference.md) to learn more about the `kernpy` API.
