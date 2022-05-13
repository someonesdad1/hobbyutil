'''
Calculate shaft/hole fits
    The fit strings and associated numbers are from page 5.18 of Tubal
    Cain's "Model Engineers Handbook", 3rd ed.

    Here's the text and table from the book [sic]:

    Shaft/hole fits

    The following figures indicate the difference between hole and shaft
    size for the named classes of fit.  These apply from shafts from
    1/8" to 2" dia.  Where the 'hole' is in a wheel boss some
    consideration must be given to the strength of this -- a test
    assembly is advised.  Normally the hole should be made dead to size
    and the shaft diameter adjusted to get the fit desired.  The figures
    are in thousandths of an inch per inch of diameter, to which must be
    added the constant 'C'.  Thus, for a 1" push fit the shaft must be
    0.35 + 0.15 = 0.5 thousandths smaller than the hole ('+' means the
    shaft is larger and '-' , smaller than the hole.)  'C' may be
    converted directly to mm (divide by 25 is near enough) and 'thou/in'
    = micron/mm.
                              'C'
            Fit             (0.001")    thou/in.
        --------------      --------    --------
        Shrink              +0.5        +1.5
        Force               +0.5        +0.75
        Drive               +0.3        +0.45
        Wheel keying        0           0
        Push                -0.15       -0.35
        Slide               -0.3        -0.45
        Prec. run           -0.5        -0.65
        Close run           -0.6        -0.8
        Normal run          -1.0        -1.5
        Easy run            -1.5        -2.25
        Small clearance     -2          -3
        Large clearance     -3          -5

    An allowance for thermal expansion must be made on engine pistons.

    ----------------------------------------------------------------------

    In the script, the constant under the 'C' column is called c and the
    constant under the thou/in column is called m, both divided by 1000 to
    give units in inches and inches/inch, respectively.  Given the hole
    diameter d, the shaft diameter D should be

        D = d - (m*d + c) = d*(1 - m) - c
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Calculate shaft/hole fits
    #∞what∞#
    #∞test∞# ignore #∞test∞#
    pass
if 1:   # Imports
    import sys
    import os
    import getopt
    from pdb import set_trace as xx 
if 1:   # Custom imports
    from wrap import dedent
    from f import flt
    from u import u, ParseUnit
    # Try to import the clr.py module (more up-to-date than color.py);
    # if not available, the script should still work (you'll just get
    # uncolored output).
    try:
        import clr
        c = clr.Clr(bits=4)
        have_color = True
    except ImportError:
        # Make a dummy color object to swallow function calls
        class Dummy:
            def __call__(self, *p, **kw):
                return ""
            def __getattr__(self, name):
                return ""
        c = Dummy()
        have_color = False
if 1:   # Global variables
    fits = (
        # Class of fit, c (in mils), m (in mils/inch)
        # For a given hole diameter d, machine the shaft diameter D to d - x
        # where x = (m/1000)*d + c/1000.
        ("Shrink",             flt(0.5),   flt(1.5)),
        ("Force",              flt(0.5),   flt(0.75)),
        ("Drive",              flt(0.3),   flt(0.45)),
        ("Wheel keying",       flt(0),     flt(0)),
        ("Push",              flt(-0.15), flt(-0.35)),
        ("Slide",             flt(-0.3),  flt(-0.45)),
        ("Precision running", flt(-0.5),  flt(-0.65)),
        ("Close running",     flt(-0.6),  flt(-0.8)),
        ("Normal running",    flt(-1.0),  flt(-1.5)),
        ("Easy running",      flt(-1.5),  flt(-2.25)),
        ("Small clearance",   flt(-2.0),  flt(-3.0)),
        ("Large clearance",   flt(-3.0),  flt(-5.0)),
    )
    in2mm = u("inches")/u("mm")
    thermal_expansion = (   # Units are 1/K
        ("Aluminum", flt(23e-6)),
        ("Brass", flt(19e-6)),
        ("Copper", flt(17e-6)),
        ("Iron", flt(11e-6)),
        ("Steel", flt(12e-6)),
    )
    # Colors
    c.int, c.cl, c.msg = c("lred"), c("lgrn"), c("lcyn")
def Usage(d, status=1):
    name = sys.argv[0]
    print(dedent(f'''
    Usage:  {name} [options] diameter [unit]
      Print a table showing fits for basic hole size and basic shaft
      size (here, "basic" means you've got the hole or shaft size you
      want and you want to calculate the size of the mating part to get
      a desired fit).  The diameter is measured in inches by default.
      You can include a length unit on the command line.  The command
      line can include python expressions; the math module's symbols are
      all in scope.  
    Example: I have a 3/8 inch diameter steel piece I wish to be a
      tight fit into a hole so that I can subsequently cross-drill it
      for a spring pin.  I run the script with the parameters "3/8 inch"
      and choose the results for a "Drive" fit under "Shaft size is
      basic".  I have to bore the hole 0.0005 inches under 3/8 inches to
      get the desired interference.
    Options
      -h    Print more extensive help.
      -m n  Use material factor n (defaults to 1).
    '''))
    if not d["-h"]:
        exit(status)
    print(dedent(f'''
     
    Tubal Cain's (Tom Walshaw) table of fit information is taken from a C
    program by Mark Klotz:
                              c      m
        Shrink               0.5    1.5
        Force                0.5    0.75
        Drive                0.3    0.45
        Push                -0.15  -0.35
        Slide               -0.3   -0.45
        Precision running   -0.5   -0.65
        Close running       -0.6   -0.8
        Normal running      -1.0   -1.5
        Easy running        -1.5   -2.25
        Small clearance     -2.0   -3.0
        Large clearance     -3.0   -5.0

    For a given hole diameter d, machine the shaft diameter D to d - x
    where x = m*d/1000 + c/1000.  c is in mils and m is in mils per inch
    of diameter.

    The -m option is used to adjust fits to other situations.  The
    basic formulas are good for metallic materials like steel and
    brass.  For other materials like plastic, you may want more of an
    interference fit; for such cases, set the n value to a number
    larger than 1.  For very stiff materials, you may want to use n
    values less than 1.  The factor n multiplies the calculated
    interference for metals.
    '''))
    exit(status)
def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)
def GetDiameter(arg, d):
    '''Given the command line arguments collapsed into a space-separated
    string, return the command and the diameter in inches that the user
    requested data for.
    '''
    try:
        s, unit = ParseUnit(arg, allow_expr=True)
        if not s:
            Usage(d)
    except ValueError as e:
        Error(e)
    try:
        diam = float(eval(s))
    except Exception:
        Error(f"Can't evaluate '{s}'")
    if diam <= 0:
        Error("Negative or zero diameter is meaningless.")
    unit = unit if unit else "inches"
    diam_inches = diam*u(unit)/u("inches")
    return arg, diam_inches
def ParseCommandLine(d):
    d["-h"] = False     # Extra help
    d["-m"] = 1         # Adjustment for material (1 = metal)
    if len(sys.argv) < 2:
        Usage(d)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hm:")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o in ("-m",):
            d["-m"] = float(a)
        elif o == "-h":
            d["-h"] = True
            Usage(d)
    return ' '.join(args)
def HoleBasic(D, d):
    '''D is hole size in inches.
    '''
    f = d["-m"]
    shaft_size_in = D
    shaft_size_mm = D*in2mm
    print(f"{c.msg}Hole size is basic:{c.n}")
    hole_size_in = float(D)
    hole_size_mm = in2mm*D
    print('''
                            Shaft size          Clearance
                           in        mm        mils     mm
                        -------   --------    -----   ------  
    '''[1:-4])
    for name, constant, allowance in fits:
        correction = f*(allowance*hole_size_in + constant)/1000
        shaft_size_in = hole_size_in + correction
        shaft_size_mm = shaft_size_in*in2mm
        clearance_mils = f*(hole_size_in - shaft_size_in)*1000
        clearance_mm = clearance_mils*in2mm/1000
        s = "  %-18s %10.4f %10.3f" % (name, shaft_size_in, shaft_size_mm)
        print(s, end=" ")
        s = "%8.1f %8.2f" % (clearance_mils, clearance_mm)
        t = f"{c.int if clearance_mm < 0 else c.cl}"
        print(f"{t}{s}{c.n}")
def ShaftBasic(D, d):
    '''D is hole size in inches.
    '''
    f = d["-m"]
    shaft_size_in = float(D)
    shaft_size_mm = in2mm*D
    print(f"\n{c.msg}Shaft size is basic:{c.n}")
    print('''
                             Hole size          Clearance
                           in        mm        mils     mm
                        -------   --------    -----   ------  
    '''[1:-4])
    for name, constant, allowance in fits:
        correction = -f*(allowance*shaft_size_in + constant)/1000
        hole_size_in = shaft_size_in + correction
        hole_size_mm = hole_size_in*in2mm
        clearance_mils = f*(hole_size_in - shaft_size_in)*1000
        clearance_mm = clearance_mils*in2mm/1000
        s = "  %-18s %10.4f %10.3f" % (name, hole_size_in, hole_size_mm)
        print(s, end=" ")
        s = "%8.1f %8.2f" % (clearance_mils, clearance_mm)
        t = f"{c.int if clearance_mm < 0 else c.cl}"
        print(f"{t}{s}{c.n}")
def CalculateFit(cmdline, D, d):
    '''hole_size_inches is diameter of hole in inches.  d is the
    settings dictionary.
    '''
    Dmm = D*in2mm
    if d["-m"] != 1:
        print("Material factor is", d["-m"])
    print("Diameter = " + cmdline)
    print("         = %.4f" % D, "inches")
    print("         = %.3f" % Dmm, "mm")
    if have_color:
        print(" "*20, "Color coding:  ", end="  ")
        print(f"{c.int}interference", end="  ")
        print(f"{c.cl}clearance{c.n}")
    else:
        print()
    HoleBasic(D, d)
    ShaftBasic(D, d)
def Temperatures(D, d):
    '''Show the temperatures needed to get the shrink fit.
    '''
    hole_size_in = float(D)
    hole_size_mm = in2mm*D
    name, constant, allowance = fits[0]
    f = d["-m"]
    assert(name == "Shrink")
    correction = f*(allowance*hole_size_in + constant)/1000
    shaft_size_in = hole_size_in + correction
    clearance_in = f*(hole_size_in - shaft_size_in)
    print(dedent(f'''
     
    {c.msg}Temperature differential for shrink fit:{c.n}
      Material    alpha, 1/MK            °C         °F
      --------    -----------           -----      -----'''))
    for material, alpha in thermal_expansion:
        δd = abs(clearance_in/hole_size_in)
        # Calculate ΔT in K
        ΔT = int(δd/alpha)
        print(f"  {material:12s} {int(alpha*1e6):6d} {ΔT:18d} {int(ΔT*9/5):10d}")
if __name__ == "__main__":
    d = {}  # Options dictionary
    arg = ParseCommandLine(d)
    cmdline, D = GetDiameter(arg, d)
    CalculateFit(cmdline, D, d)
    Temperatures(D, d)
