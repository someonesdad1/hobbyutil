'''
Calculates the mass and area of a given amount of paper
    Also does conversions between grammage and the screwball US system.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2011 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Calculates the mass and area of a given amount of paper
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
    import os
    import getopt
    import functools
    import time
if 1:   # Custom imports
    from wrap import dedent
    import fpformat
if 1:   # Global variables
    # Conversion factors
    in2mm = 25.4
    mm2in = 1/in2mm
    in2_to_m2 = 6.4516e-4
    g2oz = 0.035274
    kg2lbm = 2.20462
    g2lbm = kg2lbm/1000
    #
    fp = fpformat.FPFormat(num_digits=4)
    fp.trailing_decimal_point(False)
    # The following character is used for an exponent of 2
    ec = "²"
    #
    us = (  # Used to convert screwball US units to grammage
        # Name, width inches, height inches, number of sheets
        ("Cover (500 count)", 20, 26, 500),
        ("Bond, writing, ledger", 17, 22, 500),
        ("Book, text, offset", 25, 38, 500),
        ("Box cover", 20, 24, 500),
        ("Paperboard (all types)", 12, 12, 1000),
        ("Bristol and tag", 22.5, 28.5, 500),
        ("Blotting", 19, 24, 500),
        ("Hanging, waxing, bag, etc.", 24, 36, 500),
        ("Index bristol", 25.5, 30.5, 500),
        ("Manuscript cover", 18, 31, 500),
        ("Newsprint", 24, 36, 500),
        ("Tissue", 24, 36, 480),
    )
def Usage(status=1):
    print(dedent(f'''
    Usage:  {sys.argv[0]} [options] gsm size [count [cost]]
      Prints the mass of a given amount of paper stock.  gsm is grams per
      square meter, size is WxH where W is the width and H is the height; units
      are inches unless -m is given; then they are mm.  You can also use
      case-insensitive names like "a", "letter", "b", "ledger", "A4", etc.
      count defaults to 1 if not given and represents the number of sheets.
      You can use "r" or "R" to represent a ream; the string can also be an
      expression that will be evaluated.  Thus, r/2 means half a ream, 10*r
      means ten reams.  If you include cost, it's interpreted as the cost of
      the indicated number of sheets in dollars; this is used to calculate a
      cost per unit area and cost per unit mass.
    Options
      -g g  Print out the US paper mass equivalents for the grammage g
      -m    Interpret the WxH sizes in mm instead of inches
      -p lb Print out the gsm equivalents for the indicated pound mass
    '''))
    exit(status)
def ParseCommandLine(d):
    d["-m"] = False
    d["-g"] = False
    d["-p"] = False
    if len(sys.argv) < 2:
        Usage()
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "gphmt")
    except getopt.GetoptError as str:
        msg, option = str
        print(msg)
        sys.exit(1)
    for o, a in optlist:
        if o == "-m":
            d["-m"] = True
        elif o == "-g":
            Grammage(args)
        elif o == "-p":
            Poundage(args)
        elif o == "-h":
            Usage(0)
    if len(args) < 2:
        Usage()
    return args
def ParseSize(size, d):
    'Return paper size in mm as (length, width)'
    in2mm = 25.4
    sz, conv = size.lower(), in2mm
    if d["-m"]:
        conv = 1
    if "x" in sz:
        f = sz.split("x")
        if len(f) != 2:
            err("Bad size spec")
            Usage()
        return tuple([float(i)*conv for i in f])
    else:
        s = {
            "letter"    : (11*in2mm, 8.5*in2mm),
            "a"         : (11*in2mm, 8.5*in2mm),
            "legal"     : (14*in2mm, 8.5*in2mm),
            "ledger"    : (11*in2mm, 17*in2mm),
            "b"         : (11*in2mm, 17*in2mm),
            "c"         : (17*in2mm, 22*in2mm),
            "d"         : (22*in2mm, 34*in2mm),
            "e"         : (34*in2mm, 44*in2mm),
            # ISO paper sizes
            "a0"        : (1189, 841),
            "a1"        : (594, 841),
            "a2"        : (594, 420),
            "a3"        : (297, 420),
            "a4"        : (297, 210),
            "a5"        : (148, 210),
            "a6"        : (148, 105),
            "a7"        : (74, 105),
            "a8"        : (74, 52),
            "a9"        : (52, 37),
            "a10"       : (37, 26),
            "b0"        : (1414, 1000),
            "b1"        : (1000, 707),
            "b2"        : (707, 500),
            "b3"        : (500, 353),
            "b4"        : (353, 250),
            "b5"        : (250, 176),
            "b6"        : (176, 125),
            "b7"        : (125, 88),
            "b8"        : (88, 62),
            "b9"        : (62, 44),
            "b10"       : (44, 31),
            "c0"        : (1297, 917),
            "c1"        : (917, 648),
            "c2"        : (648, 458),
            "c3"        : (458, 324),
            "c4"        : (324, 229),
            "c5"        : (229, 162),
            "c6"        : (162, 114),
            "c7"        : (114, 81),
            "c8"        : (81, 57),
            "c9"        : (57, 40),
            "c10"       : (40, 28),
        }
        try:
            return s[sz]
        except KeyError:
            err("'%s' is not a recognized paper size" % size)
            Usage()
def GetNumSheets(s):
    '''s is either a string for an integer or it contains "r", which
    represents a ream.  The "r" form can be a valid python expression.
    '''
    try:
        return int(s)
    except ValueError:
        e = s.lower().replace("r", "500")
        return eval(e)
def GetSize(s):
    '''Return a "nice" form of the size spec.
    '''
    sizes = set((
        "a b c d e a0 a1 a2 a3 a4 a5 a6 a7 a8 a9 a10 b0 b1 b2 b3 b4"
        "b5 b6 b7 b8 b9 b10 c0 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10".split()))
    if s in sizes:
        return s.upper()
    else:
        if "X" in s:
            return s.replace("X", "x")
        else:
            return s
def Grammage(args):
    '''args[0] is the grammage.  Print equivalent US paper masses.
    '''
    in2_to_m2 = 0.00064516
    gsm = float(args[0])
    print("%.3g gsm equivalent US paper mass:" % gsm)
    for name, w, h, count in us:
        area_m2 = w*h*count*in2_to_m2
        mass_lb = gsm*area_m2*g2lbm
        print("%-30s %.1f pound" % (name, mass_lb))
    exit(0)
def Poundage(args):
    '''args[0] is the pounds.  For the different US paper masses, print
    the grammage.
    '''
    lb = float(args[0])
    print("Grammage equivalents of %s pound US paper masses:" % args[0])
    for name, w, h, count in us:
        area_m2 = w*h*count*in2_to_m2
        mass_g = lb/g2lbm
        gsm = mass_g/area_m2
        print("%-30s %.0f gsm" % (name, gsm))
    exit(0)
if __name__ == "__main__":
    d = {}  # Options dictionary
    have_cost = False
    args, num_sheets = ParseCommandLine(d), 1
    length_mm, width_mm = ParseSize(args[1], d)
    if len(args) > 2:
        num_sheets = GetNumSheets(args[2])
    if len(args) > 3:
        have_cost = True
        cost = float(args[3])
    gsm = float(args[0])
    # Output results
    print("gsm = %d g per square meter" % gsm)
    if d["-m"]:
        s = " (in mm)"
    else:
        s = " (in inches)"
    print("Size = ", GetSize(args[1]), s)
    s = " "*4
    if length_mm > width_mm:
        print("%sLength = %.1f mm = %.2f in" % (s, length_mm, length_mm*mm2in))
        print("%sWidth  = %.1f mm = %.2f in" % (s, width_mm, width_mm*mm2in))
    else:
        print("%sLength = %.1f mm = %.2f in" % (s, width_mm, width_mm*mm2in))
        print("%sWidth  = %.1f mm = %.2f in" % (s, length_mm, length_mm*mm2in))
    area_mm2 = width_mm*length_mm
    print("1 sheet:")
    print("%sArea = %s m%s = %s cm%s = %s mm%s = %s in%s" % (
        s,
        fp.sig(area_mm2/1e6),
        ec,
        fp.sig(area_mm2/1e2),
        ec,
        fp.sig(area_mm2),
        ec,
        fp.sig(area_mm2*0.00155),
        ec,
        )
    )
    m_g = gsm*length_mm*width_mm/1000**2
    print("%sMass = %s g = %s oz = %s lb" %
          (s, fp.sig(m_g), fp.sig(m_g*g2oz), fp.sig(m_g*g2oz/16)))
    print("Number of sheets per unit mass:")
    print("%s%s sheets/kg  " % (s, fp.sig(1000/m_g)), end="")
    print("%s%s sheets/lb  " % (s, fp.sig(1/(m_g/1000*kg2lbm))), end="")
    print("%s%s sheets/oz" % (s, fp.sig(1/(m_g/1000*kg2lbm*16))))
    if num_sheets > 1:
        print("%d sheets:" % num_sheets)
        print("%sArea = %s m%s = %s cm%s = %s mm%s = %s in%s" % (
            s,
            fp.sig(area_mm2/10**6*num_sheets),
            ec,
            fp.sig(area_mm2/100*num_sheets),
            ec,
            fp.sig(area_mm2*num_sheets),
            ec,
            fp.sig(area_mm2*0.00155*num_sheets),
            ec))
        print("%sMass = %s g = %s kg = %s oz = %s lb" % (
              s,
              fp.sig(m_g*num_sheets),
              fp.sig(m_g*num_sheets/1000),
              fp.sig(m_g*num_sheets*g2oz),
              fp.sig(m_g*num_sheets*g2oz/16)))
        if have_cost:
            print("%sCost/area = %s $/m%s = %s cents/in%s" % (
                  s,
                  fp.sig(cost/(area_mm2/1000**2*num_sheets)),
                  ec,
                  fp.sig(0.00064516*100*cost/(area_mm2/1000**2*num_sheets)),
                  ec))
            m_kg = m_g/1000*num_sheets
            print("%sCost/mass = %s $/kg = %s $/lb = %s cents/gram" % (
                  s,
                  fp.sig(cost/m_kg),
                  fp.sig(cost/(m_kg*kg2lbm)),
                  fp.sig(100*cost/(1000*m_kg))))
            # Calculate $/(m2*kg)
            cpam = fp.sig(cost/(m_kg*area_mm2/10**6*num_sheets))
            print("%sCost/(area*mass) = %s $/(m%s*kg)" % (
                  s,
                  cpam,
                  ec))
            print("%sCost per sheet = $%s = %s cents" % (
                  s,
                  fp.sig(cost/num_sheets),
                  fp.sig(100*cost/num_sheets)))
