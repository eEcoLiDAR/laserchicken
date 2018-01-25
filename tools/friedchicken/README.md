# friedchicken

Reads las file and writes ply file


# Installation

In **eEcoLiDAR** folder run:
```
pip install --no-cache-dir --force-reinstall ./tools/friedchicken
```


# Usage


## Options
To see the available options:
    $ friedchicken --help

```
Usage: friedchicken [OPTIONS]

  Reads las file and writes as ply file.

Options:
  -l, --lasfile TEXT   Name of the input las file.  [required]
  -p, --plyfile TEXT   Name of the output ply file.  [required]
  --csv
  -d, --csvdelim TEXT  Delimiter for CSV file.
  -v, --verbose
  --version
  --help               Show this message and exit.

```


## Example:

```
    $ friedchicken -l ./testdata/AHN2.las -p test_AHN2.ply
```


## CSV output

In order to save the output file in CSV format with **';'** delimiter, run:

```
    $ friedchicken -l ./testdata/AHN2.las -p test_AHN2.ply --csv -d ';'
```
