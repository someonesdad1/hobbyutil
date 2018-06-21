'''This script will generate PostScript to draw an engineering grid on
a piece of letter size paper.  Edit the global variables below, then
run the script as

    python eng_grid.py

You'll get a file containing PostScript commands (the file is named
in the output_file global variable).

If you're unfamiliar with python, go to www.python.org and get a
copy of it for your computer.

The default values are set up to produce an 8 inch by 10 inch 10x10
grid on letter paper.  You can change the grid size, line spacing,
line widths, and line colors.

If you want to view the output, you can convert it to a PDF if you
have ghostscript (http://www.cs.wisc.edu/~ghost/); run the ps2pdf
utility.  You can also use GSView (http://www.ghostgum.com.au) as a
PostScript viewer.  When you print a PDF, make sure you set the
scaling to "None" (i.e., don't allow the PDF viewing program to
scale the page to fit the paper).

GSView also has the ability to save the rendered PostScript file as a
bitmap, which then lets you convert it to a variety of graphic formats
as desired (ghostscript is used to do the actual conversion).
'''

# Copyright (C) 2005 Don Peterson
# Contact:  gmail.com@someonesdad1

#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#

from __future__ import print_function, division


# ------------------- Edit the following settings ------------------------

# Set the following variable to determine units.  PostScript's native
# length unit is points, so setting this to 72.27 means the unit length
# is inches (after a scale transformation); 2.84527 will make the unit
# length millimeters.  If you change this value from 72.27, be aware
# that you'll want to change the values of the other lengths given below.
unit_length_conversion = 72.27

# Make this value nonzero if you want to send the output file directly
# to a LaserJet printer.
wrap_in_PJL = 0

# You can choose the colors of the grid lines here.  This is set up to
# draw grey lines, but the tuples are RGB values, so you can change
# them to colors if you wish.  Light blue is used on vellum because it
# won't print on a blue line machine (and sometimes it won't show up
# on a photocopy).
#
# Change w to a lower value if the lines are too light on your
# printer.
w = 0.8
dw = 0.1
light_line_color = (w - 0*dw, w - 0*dw, w - 0*dw)
medium_line_color = (w - 1*dw, w - 1*dw, w - 1*dw)
heavy_line_color = (w - 2*dw, w - 2*dw, w - 2*dw)

# Widths of the lines in inches
light_line_width = 0.004
medium_line_width = 0.006
heavy_line_width = 0.008

# Spacings of the lines.  Set to zero if you don't want a particular
# line.
light_line_spacing = 0.1
medium_line_spacing = 0.5
heavy_line_spacing = 1.0

# The position of the lower left corner of the grid in inches from the
# lower left corner of the page.
X = 0.23
Y = 0.5

# Width and height of the grid in inches
width = 8
height = 10

# To suppress vertical or horizontal lines, set to zero.
vertical_lines = 1
horizontal_lines = 1

output_file = "eng_grid.ps"

# ------------------- Don't edit beyond this point -----------------------

def CheckData():
    if unit_length_conversion <= 0:
        raise Exception("unit_length_conversion must be > 0")
    def GEZero(x, name):
        if x < 0:
            raise Exception("%s must be >= zero" % name)
    def GreaterThanZero(x, name):
        if x <= 0:
            raise Exception("%s must be greater than zero" % name)
    def Between0And1(x, name):
        if x < 0 or x > 1:
            raise Exception("%s must be between 0 and 1" % name)
    def PowerOfTen(x, name):
        log = abs(log10(x))
        eps = 0.0001
        if log - int(log) > eps:
            raise Exception("%s must be a power of 10" % name)
    Between0And1(light_line_color[0], "light_line_color component")
    Between0And1(light_line_color[1], "light_line_color component")
    Between0And1(light_line_color[2], "light_line_color component")
    GreaterThanZero(light_line_width, "light_line_width")
    GreaterThanZero(medium_line_width, "medium_line_width")
    GreaterThanZero(heavy_line_width, "heavy_line_width")
    GEZero(light_line_spacing, "light_line_spacing")
    GEZero(medium_line_spacing, "medium_line_spacing")
    GEZero(heavy_line_spacing, "heavy_line_spacing")
    GreaterThanZero(width, "width")
    GreaterThanZero(height, "height")

class EngineeringGrid:
    '''Draws an engineering grid by emitting the proper PostScript.
    Assumes dimensions are in inches, but you can change the units
    used by changing the unit_length_conversion global variable.
    '''

    def __init__(self, X_lower_left_corner=0.23, Y_lower_left_corner=0.25,
                 width=8, height=10):
        self.X = X_lower_left_corner
        self.Y = Y_lower_left_corner
        self.width = width
        self.height = height
        self.line_spacings = (light_line_spacing,
                              medium_line_spacing,
                              heavy_line_spacing)
        self.line_widths = (light_line_width,
                            medium_line_width,
                            heavy_line_width)
        self.line_colors = (light_line_color,
                            medium_line_color,
                            heavy_line_color)
        self.uel_begin = '''%s%%-12345X@PJL JOB
@PJL ENTER LANGUAGE=POSTSCRIPT''' % chr(27)
        self.uel_end = "%s%%-12345X" % chr(27)
        self.out = open(output_file, "w")

    def SetSpacings(self, spacings):
        '''spacings must be a tuple with the spacing for the light lines
        first, followed by the medium line spacing, then the heavy
        line spacing.
        '''
        if not isinstance(spacings, tuple):
            raise Exception("spacings must be a 3-tuple")
        self.spacings = spacings

    def SetLineWidths(self, line_widths):
        '''line_widths must be a tuple with the line width for the light
        lines first, followed by the medium line line width, then the
        heavy line line width.
        '''
        if not isinstance(line_widths, tuple):
            raise Exception("line_widths must be a 3-tuple")
        self.line_widths = line_widths

    def SetLineColors(self, line_colors):
        '''line_colors must be a tuple with the color for the light lines
        first, followed by the medium line color, then the heavy line
        color.
        '''
        if not isinstance(line_colors, tuple):
            raise Exception("line_colors must be a 3-tuple")
        self.line_colors = line_colors

    def GenerateGrid(self):
        if wrap_in_PJL:
            self.out.write(uel0 + "\n")
        out = self.out.write
        # Initialize PostScript
        out('''
20 setmiterlimit
initmatrix 0 rotate
%g %g scale
[ ] 0 setdash
0 setlinecap
0 setlinejoin\n''' % (unit_length_conversion, unit_length_conversion))
        # Set the new origin
        out("%g %g translate\n" % (self.X, self.Y))
        # Draw the horizontal lines
        if horizontal_lines:
            for i in xrange(3):
                dy = self.line_spacings[i]
                if dy:
                    y = 0
                    lw = self.line_widths[i]
                    lc = self.line_colors[i]
                    while y <= self.height:
                        self._draw_horizontal_line(y, lw, lc)
                        y += dy
        # Draw the vertical lines
        if vertical_lines:
            for i in xrange(3):
                dx = self.line_spacings[i]
                if dx:
                    x = 0
                    lw = self.line_widths[i]
                    lc = self.line_colors[i]
                    y = 0
                    while x <= self.width:
                        self._draw_vertical_line(x, lw, lc)
                        x += dx
        self.out.close()

    def _draw_vertical_line(self, x, line_width, line_color):
        self.out.write("%g %g moveto\n" % (x, 0))
        self.out.write("%g setlinewidth\n" % line_width)
        self.out.write("%g %g %g setrgbcolor\n" % line_color)
        self.out.write("%g %g rlineto stroke\n" % (0, self.height))

    def _draw_horizontal_line(self, y, line_width, line_color):
        self.out.write("%g %g moveto\n" % (0, y))
        self.out.write("%g setlinewidth\n" % line_width)
        self.out.write("%g %g %g setrgbcolor\n" % line_color)
        self.out.write("%g %g rlineto stroke\n" % (self.width, 0))

CheckData()
eg = EngineeringGrid(X, Y, width, height)
eg.GenerateGrid()
