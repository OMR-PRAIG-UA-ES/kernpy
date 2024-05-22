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


Load the file directly using the content of the file:    
Examples:
```python
import kernpy
score = kernpy.load('**kern\n*clefG2\n*M4/4\n*met(c)\n=1\n4c\n4d\n4e\n4f\n=2\n*M3/2\n2g\n2f\n2d\n=\n*-'
```

Or load the file using the path to the file:
```python
import kernpy

score = kernpy.read("path/to/file.krn")
```

Then you can access to the score attributes:

```python
print(type(score))
# <class 'kernpy.core.generic.Score'>

print(score.voices)
# ['saxophone', 'clarinet', 'piano']
```

Now, you can export the score using the `ExportOptions` class:

```python
export_options = kernpy.ExportOptions()
content = score.export(export_options)
print(content)
```

Or you save the score to a file:
```python
export_options = kernpy.ExportOptions()
content = score.save(export_options, "path/to/file.krn")
```

<h4>Let's filter the export options:</h4>

Select the voices to export:
```python
export_options = kernpy.ExportOptions(voices=['saxophone'])
content = score.export(export_options)
print(content)
```

Select the measures to export:
```python
export_options = kernpy.ExportOptions(from_measure=1, to_measure=2)
content = score.export(export_options)
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
content = score.export(export_options)
print(content)
```
Actually, you can use the predefined categories:
```python
export_options = kernpy.ExportOptions(token_categories=kernpy.BEKERN_CATEGORIES)
content = score.export(export_options)
print(content)
```

Select the encoding to export:
```python
export_options = kernpy.ExportOptions(kern_type=kernpy.KernTypeExporter.normalizedKern)
content = score.export(export_options)
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
# TODO: ...

## Next steps
Congratulations! You have learned the basics of `kernpy`. Now you can start using the package in your projects.

Go to the [API reference](../reference.md) to learn more about the `kernpy` API.
