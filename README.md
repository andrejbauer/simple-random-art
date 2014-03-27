# Simple Random Art in Python

I get asked every so often to release the source code for my [random 
art](http://www.random-art.org/). The original source is written in Ocaml
and is not publicly available, but here is a simple example of how you can get
random art going in Python in 250 lines of code.

The idea is to generate expression trees that describe an image. For each
point `(x,y)` of the image we evaluate the expression and get a color. A color
is represented as a triple `(r,g,b)` where the red, green, blue components are
numbers between `-1` and `1`. In computer graphics it is more usual to use the
range `[0,1]`, but since many operations are symmetric with respect to the
origin it is more convenient to use the interval `[-1,1]`.

I kept the program as simple as possible, and independent of any non-standard
Python libraries. Consequently, a number of improvements and further
experiments are possible:

* The most pressing problem right now is that the image is displayed as a
  large number of rectangles of size 1x1 on the tkinter Canvas, which
  consumes a great deal of memory. You will not be able to draw large images
  this way. An improved version would use the Python imagining library (PIL)
  instead.

* The program uses a simple RGB (Red Green Black) color model. We could also
  use the HSV model (Hue Value Saturation), and others. One possibility is
  to generate a palette of colors and use only colors that are combinations
  of those from the palette.

* Of course, you can experiment by introducing new operators. If you are going
  to play with the source, your first exercise should be a new operator.

* The program uses cartesian coordinates. You could experiment with polar
  coordinates.

For more information and further discussion, see http://math.andrej.com/category/random-art/

You need Python 2.7 or later to run the program. To start the program, run `randomart.py` from command-line or from the Python IDE *IDLE*.