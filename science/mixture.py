'''
Program to calculate mixtures
    Modeled after a C program by Marv Klotz.
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
    # Calculate mixture concentrations
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
    import getopt
    import pathlib
    from functools import partial
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    from get import GetNumber
    from f import flt
    from color import C
if 1:   # Global variables
    Get = partial(GetNumber, num_type=flt, low=0)
    class g: pass
    g.VolA = flt(0)
    g.VolB = flt(0)
    g.VolMixture = flt(0)
    g.ConcA = flt(0)
    g.ConcB = flt(0)
    g.ConcMixture = flt(0)
def ParseCommandLine(d):
    d["-d"] = 3         # Number of significant digits
    d["-g"] = False     # Turn on debug printing
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:h")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o[1] in list(""):
            d[o] = not d[o]
        elif o in ("-d",):
            try:
                d["-d"] = int(a)
                if not (1 <= d["-d"] <= 15):
                    raise ValueError()
            except ValueError:
                msg = ("-d option's argument must be an integer between "
                    "1 and 15")
                print(msg, file=sys.stderr)
                exit(1)
        elif o in ("-h", "--help"):
            ShowFormulas()
    flt(0).n = d["-d"]
    return args
def ShowFormulas():
    print(dedent('''
    Assumptions:
        * The solute in both solutions A and B are the same.
        * One or both solutions can be pure solvent.
        * The solute and solvent are mixed well.
        * There are no volume or temperature changes when the solutions are mixed.
        * Works best for dilute solutions.
        * The concentration fractions are volume fractions.  This means both
        the solvent and solute are liquids (example:  water and antifreeze
        for your car).
    
    Symbols:
        C = concentration fraction
        V = volume
    
    The six variables in the problem are thus:
        Solution A:  Ca, Va
        Solution B:  Cb, Vb
        Mixture:     C, V
    
    Solution A has a solute volume of Ca*Va.
    Solution B has a solute volume of Cb*Vb.
    
    After mixing, the resulting solution has a solute volume faction of
    
        C = (Ca*Va + Cb*Vb)/V
    
    where the volume is
    
        V = Va + Vb
    
    Note that this formulation is an approximation; real solutions sometimes
    don't satisfy the above assumptions.  Example:  ethanol and water mixed
    together will have a lower volume than their component sum because the
    water and ethanol molecules "interlock" somewhat because of close-range
    polar electrical forces.
    
    You can check the following cases for reasonableness:
        * Mix two unit-volume solutions of 0% concentration to get 2 units
          of volume of 0% concentration.
        * Mix two unit-volume solutions of 100% concentration to get a 100%
          volume of 2 units.
        * Mix one unit volume of p% concentration and one unit volume of 0%
          concentration to get 2 units of (p/2)% concentration.
    '''))
    exit(0)
def GetData():
    # Set all numbers to 0
    g.ConcA = g.ConcB = flt(0)
    g.VolA = g.VolB = g.VolMixture = g.ConcMixture = flt(0)
    #
    print(dedent(f'''
    Script is {pathlib.Path(sys.argv[0]).resolve()}

    Calculate the resulting concentration of a solution gotten by mixing
    two solutions of differing concentrations.  Use -h on the command line
    to see the formulas used.  Use -d to set the number of significant
    digits (defaults to {d["-d"]}).

    '''))
    print(dedent('''
    Specify concentrations of both solutions.  If one solution is a
    dilutant (e.g., pure water), enter its concentration as 0%.

    '''))
    g.ConcA = Get("  Concentration of solution A in %? ", high=100, default=0)
    g.ConcB = Get("  Concentration of solution B in %? ", high=100, default=0)
    print(dedent('''

    Enter what you know; press return if not known.  You must enter two data
    items to obtain a solution.

    '''))
    data_items_entered = 0
    while True:
        g.VolA = Get("  Volume of solution A? ", default=g.VolA)
        if g.VolA:
            data_items_entered += 1
        g.VolB = Get("  Volume of solution B? ", default=g.VolB)
        if g.VolB:
            data_items_entered += 1
        if data_items_entered != 2:
            g.VolMixture = Get("  Volume of mixture? ", default=g.VolMixture)
            if g.VolMixture:
                data_items_entered += 1
            if data_items_entered != 2:
                g.ConcMixture = Get("  Concentration of mixture in %? ",
                                    high=100, default=g.ConcMixture)
                if g.ConcMixture:
                    data_items_entered += 1
                if data_items_entered != 2:
                    print("Insufficient data.  Try again.")
                break
            else:
                break
        else:
            break
    if d["-g"]:
        print(dedent(f'''

        {C.lcyn}Entered data:
            VolA            {g.VolA!r}
            VolB            {g.VolB!r}
            VolMixture      {g.VolMixture!r}
            ConcA           {g.ConcA!r}
            ConcB           {g.ConcB!r}
            ConcMixture     {g.ConcMixture!r}{C.norm}'''))
def PrintResults():
    pa, pb, pm = g.ConcA/100, g.ConcB/100, g.ConcMixture/100
    if g.VolA and g.VolB:
        g.VolMixture = flt(g.VolA + g.VolB)
        g.ConcMixture = flt(100*(g.VolA*pa + g.VolB*pb)/(g.VolA + g.VolB))
    elif g.VolA and g.ConcMixture:
        g.VolMixture = flt(g.VolA*(pa - pb)/(pm - pb))
        g.VolB = flt(g.VolMixture - g.VolA)
    elif g.VolA and g.VolMixture:
        g.VolB = flt(g.VolMixture - g.VolA)
        g.ConcMixture = flt(100*(g.VolA*pa + g.VolB*pb)/(g.VolA + g.VolB))
    elif g.VolB and g.ConcMixture:
        g.VolMixture = flt(g.VolB*(pb - pa)/(pm - pa))
        g.VolA = flt(g.VolMixture - g.VolB)
    elif g.VolB and g.VolMixture:
        g.VolA = flt(g.VolMixture - g.VolB)
        g.ConcMixture = flt(100*(g.VolA*pa + g.VolB*pb)/g.VolMixture)
    elif g.VolMixture and g.ConcMixture:
        g.VolA = flt(g.VolMixture*(pm - pb)/(pa - pb))
        g.VolB = flt(g.VolMixture - g.VolA)
    else:
        print("Not enough information")
        exit(1)
    # Print results
    n, k, s = 8, 14, " "*8
    print(dedent(f'''
    
    Results:
        Solution            Volume            Concentration
        --------        --------------        -------------
        {"A":^{n}s}{s}{g.VolA!s:^{k}s}{s}{g.ConcA!s:^{k}s}
        {"B":^{n}s}{s}{g.VolB!s:^{k}s}{s}{g.ConcB!s:^{k}s}
        {"Mixture":^{n}s}{s}{g.VolMixture!s:^{k}s}{s}{g.ConcMixture!s:^{k}s}
    '''))
if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    GetData()
    PrintResults()
