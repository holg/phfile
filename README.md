# PHFile

phfile is a vital part of a tool I wrote for lighting manufacturing company.

## Idea

The idea was to create something what will allow for massive and automated changing of some information kept in ldt files. Luminaires with different names and catalogue numbers with different shapes and colour etc. can be equipped with same optics and hence have same light distribution curve (the minor differences are of course present but in most cases are negligible). Therefor one ldt file can be duplicated to handle few different luminaires.

## Getting started

### Installation

Simply download master branch, unpack, go into created directory and install using pip:

```
$ pip install .
```

### Testing

Just run:

```
$ python setup.py test
```

## Usage

### Initializing

```
from phfile import LDT

ldt_file = LDT()
```

### Loading ldt file

```
ldt_file.load('path/to/ldt/file')
```

### Setting items

Items can be set by name or by index, data can be passed for the multiple items at single call:

```
ldt_file.set('item1', value1, 'item2', value2, ..., 'itemn', valuen)
ldt_file.set(item1=value1, item2=value2, ..., itemn=valuen)
```

Accepted names / indexes are:

| index | name                  | type           |
|-------|-----------------------|----------------|
|  1    | company               | str            |
|  2    | type_indicator        | int            |
|  3    | symmetry_indicator    | int            |
|  4    | number_mc             | int            |
|  5    | distance_dc           | int            |
|  6    | number_ng             | int            |
|  7    | distance_dg           | float          |
|  8    | report_no'            | str            |
|  9    | luminaire_name        | str            |
| 10    | luminaire_no          | str            |
| 11    | file_name             | str            |
| 12    | date_user             | str            |
| 13    | luminaire_length      | float          |
| 14    | luminaire_width       | float          |
| 15    | luminaire_height      | float          |
| 16    | luminous_length       | float          |
| 17    | luminous_width        | float          |
| 18    | luminous_height_c0    | float          |
| 19    | luminous_height_c90   | float          |
| 20    | luminaire_height_c180 | float          |
| 21    | luminaire_height_c270 | float          |
| 22    | dff                   | float          |
| 23    | lorl                  | float          |
| 24    | conversion_factor     | float          |
| 25    | tilt                  | float          |
| 26    | number_n              | int            |
| --    | lamps                 | list of dicts  |
| 27    | direct_ratios         | list of floats |
| 28    | angles_c              | list of floats |
| 29    | angles_g              | list of floats |
| 30    | luminous_intensities  | list of floats |

For setting lamps list of dictionaries with the following keys is required:

| key         | type  |
|-------------|-------|
| number_of   | int   |
| type_of     | str   |
| total_flux  | int   |
| color_temp  | int   |
| cri         | int   |
| total_power | float |

### Getting items

Getting items works similar way as setting them:

```
ldt_file.item('item')
ldt_file.item('item1', 'item2', ..., 'itemn')
```

For multiple items returned value is dictionary.

### Additional features

LDT class also allows you to write modified file and to plot light distribution graph (as svg file). By default those files are named based on luminaire_name value, but it can be changed by passing save_path argument.

```
ldt_file.write(save_path='new/ldt/file/path')
ldt_file.plot(save_path='light/distribution/graph/path')
```

Methods load, set, write and plot returns class instance so the can be chained.

```
ldt_file.load('path/to/ldt/file').set('luminaire_name', 'some new name').write().plot()
```

## TODO

Extending of class responsible for handling IES files. Firstly the conversion from the LDT to the IES format, in the next steps the parser allowing direct reading of these files.

I encourage you to look through the source code, any feedback is welcome :-)
