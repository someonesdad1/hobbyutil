'''
Calculate shaft/hole fits.  Adapted from Marv Klotz's fits.c program.

Comments from Marv's data file:
    Entries are:   fit name,constant,allowance
    constant is measured in thousandths of an inch
    allowance is measured in thousandths of an inch per inch of shaft diameter

    Example:  For a push fit on a nominal 1" shaft, machine the hole
    to exactly 1.0000", and machine the shaft to -0.35*(1.0)-0.15 =
    -0.5 thou less than the nominal size (0.9995").
'''

from __future__ import print_function, division
import sys
import os
import getopt
from u import u, ParseUnit
from pdb import set_trace as xx

# All math module symbols are imported to let user use them in command
# line expressions.
from math import *

# Try to import the color.py module; if not available, the script
# should still work (you'll just get uncolored output).
try:
    import color
    have_color = True
except ImportError:
    # Make a dummy color object to swallow function calls
    class Dummy:
        def fg(self, *p, **kw):
            pass
        def normal(self, *p, **kw):
            pass
        def __getattr__(self, name):
            pass
    color = Dummy()
    have_color = False

fits = (
    # Class of fit, c, m
    # For a given hole diameter d, machine the shaft diameter D to d - x
    # where x = m*d/1000 + c/1000.  c is in mils and m is in mils per inch
    # of diameter.
    ("Shrink",             0.5,   1.5),
    ("Force",              0.5,   0.75),
    ("Drive",              0.3,   0.45),
    ("Push",              -0.15, -0.35),
    ("Slide",             -0.3,  -0.45),
    ("Precision running", -0.5,  -0.65),
    ("Close running",     -0.6,  -0.8),
    ("Normal running",    -1.0,  -1.5),
    ("Easy running",      -1.5,  -2.25),
    ("Small clearance",   -2.0,  -3.0),
    ("Large clearance",   -3.0,  -5.0),
)

in2mm = u("inches")/u("mm")

# Colors
interference, clearance = color.lred, color.lgreen

def Usage(d, status=1):
    path, name = os.path.split(sys.argv[0])
    print('''
Usage:  {name} diameter [unit]
  For a given diameter, print a table showing fits for both basic hole
  size and basic shaft size (here, "basic" means you've got the hole
  or shaft size you want and you want to calculate the size of the
  mating part to get a desired fit).  The diameter is measured in
  inches by default.  You can include a unit on the command line.
 
  The command line can include python expressions; the math module's
  symbols are all in scope.  This, for example, lets you use fractions
  for input; suppose you needed a hole for a sliding fit with a shaft
  of diameter in feet of 3/4*cos(80 degrees).  You'd use the command
  line arguments
 
      3/4*cos(80*pi/180) ft
 
  and the needed hole diameter would be 1.5638 inches (39.721 mm); it
  would have 1 mil of clearance (25 um).
 
  The script is based on Tubal Cain's table of fit allowances and
  software written by Marv Klotz.
'''.strip().format(**locals()))
    exit(status)

def ParseCommandLine(d):
    args = sys.argv[1:]
    if len(args) < 1:
        Usage(d)
    return ' '.join(args)

def HoleBasic(D, d):
    '''D is hole size in inches.
    '''
    shaft_size_in = D
    shaft_size_mm = D*in2mm
    print("Hole size is basic:")
    hole_size_in = float(D)
    hole_size_mm = in2mm*D
    print('''
                            Shaft size          Clearance
                           in        mm        mils     mm
                        -------   --------    -----   ------
'''[1:-1])
    for name, constant, allowance in fits:
        correction = (allowance*hole_size_in + constant)/1000
        shaft_size_in = hole_size_in + correction
        shaft_size_mm = shaft_size_in*in2mm
        clearance_mils = (hole_size_in - shaft_size_in)*1000
        clearance_mm = clearance_mils*in2mm/1000
        s = "  %-18s %10.4f %10.3f" % (name, shaft_size_in, shaft_size_mm)
        print(s, end=" ")
        s = "%8.1f %8.2f" % (clearance_mils, clearance_mm)
        color.fg(interference if clearance_mm < 0 else clearance)
        print(s)
        color.normal()

def ShaftBasic(D, d):
    '''D is hole size in inches.
    '''
    shaft_size_in = float(D)
    shaft_size_mm = in2mm*D
    print("\nShaft size is basic:")
    print('''
                             Hole size          Clearance
                           in        mm        mils     mm
                        -------   --------    -----   ------
'''[1:-1])
    for name, constant, allowance in fits:
        correction = -(allowance*shaft_size_in + constant)/1000
        hole_size_in = shaft_size_in + correction
        hole_size_mm = hole_size_in*in2mm
        clearance_mils = (hole_size_in - shaft_size_in)*1000
        clearance_mm = clearance_mils*in2mm/1000
        s = "  %-18s %10.4f %10.3f" % (name, hole_size_in, hole_size_mm)
        print(s, end=" ")
        s = "%8.1f %8.2f" % (clearance_mils, clearance_mm)
        color.fg(interference if clearance_mm < 0 else clearance)
        print(s)
        color.normal()

def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)

def GetDiameter(arg, d):
    '''Given the command line arguments collapsed into a space-separated
    string, return the command and the diameter in inches that the user
    requested data for.
    '''
    try:
        s, unit = ParseUnit(arg, allow_expr=True)
    except ValueError as e:
        Error(e)
    try:
        diam = float(eval(s))
    except Exception:
        Error("Can't evaluate '{}'".format(s))
    if diam <= 0:
        Error("Negative or zero diameter is meaningless.")
    unit = unit if unit else "inches"
    diam_inches = diam*u(unit)/u("inches")
    return arg, diam_inches

def CalculateFit(cmdline, D, d):
    '''hole_size_inches is diameter of hole in inches.  d is the
    settings dictionary.
    '''
    Dmm = D*in2mm
    print("Diameter = " + cmdline)
    print("         = %.4f" % D, "inches")
    print("         = %.3f" % Dmm, "mm")
    if have_color:
        print(" "*20, "Color coding:  ", end="  ")
        color.fg(interference)
        print("interference", end="  ")
        color.fg(clearance)
        print("clearance")
        color.normal()
    else:
        print()
    HoleBasic(D, d)
    ShaftBasic(D, d)

if __name__ == "__main__":
    d = {}  # Options dictionary
    arg = ParseCommandLine(d)
    cmdline, D = GetDiameter(arg, d)
    CalculateFit(cmdline, D, d)
