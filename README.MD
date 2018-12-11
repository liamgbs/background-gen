# Liam's Awesome Background Generator

My generator is written in Python and uses a combination of voronoi diagrams and fractal trees.

The VD is implemented using fortunes algorithm: for those interested:
http://blog.ivank.net/fortunes-algorithm-and-implementation.html

There are some sample images in the examples dir

### Windows

Install python.

navigate to the project directory in your favourite command line app and run:

`python -m pip install -r requirements.txt`

Note the shapely dependency doesn't like installing from pip on windows so just
download the whl file from here:  

https://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely

and run:

`python -m pip install <path_to_whl_file>`

### Linux

Same but run:

`pip3 install -r- requirements.txt`

## Running it

To actually run the generator:

just run

`python main.py [tree] [tess]`

The tree and tess arguments just let you choose whether you want one or the other.

For the best results just leave the image dimensions on 4K, but if you want to
use it for your own display then you can easily configure the x and y dimensions
from the variables at the top of the main.py file

As a bonus, you can also add your own RBG colour combinations for the tessellations
by adding to the list in the Colours class in colours.py
