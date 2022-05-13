'''
Given a measured impedance in polar coordinates, prints out the
associated parameters that can be calculated.
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
    # Calculates various measures from a complex electrical impedance
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import getopt
    import os
    import sys
    #from math import tan, sin, cos, pi, isinf, radians #xx
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    #from sig import sig #xx
    from f import flt, tan, sin, cos, pi, isinf, radians
    from fpformat import FPFormat
    if 1:
        import debug
        debug.SetDebugger()
if 1:   # Global variables
    ii = isinstance
def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)
def Usage(d, status=1):
    print(dedent(f'''
    Usage:  {sys.argv[0]} [options] Z theta
      Given a measured impedance with magnitude Z in ohms and phase angle
      theta in degrees, prints out the associated parameters.  You can use
      a cuddled SI prefix after the number for Z if you wish (example:
      1.23k means 1230 ohms).
    Options
      -d n      Use n significant digits for output [{d["-d"]}]
      -f f      Specify measurement frequency in Hz.  You can use a cuddled SI 
                prefix after the number.  [{d["-f"]} Hz]
    '''))
    exit(status)
def ParseCommandLine(d):
    d["-d"] = 3     # Number of significant digits
    d["-f"] = 1000  # Measurement frequency in Hz
    if len(sys.argv) < 2:
        Usage(d)
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "d:f:")
    except getopt.GetoptError as e:
        msg, option = e
        print(msg)
        exit(1)
    for o, a in optlist:
        if o == "-d":
            try:
                d["-d"] = int(a)
            except ValueError:
                Error("-d option invalid")
            if not(1 <= d["-d"] <= 15):
                Error("-d option must be between 1 and 15")
        if o == "-f":
            try:
                d["-f"] = Interpret(a)
            except ValueError:
                Error("-f option invalid")
            if d["-f"] <= 0:
                Error("-f option must be > 0")
    #sig.digits = d["-d"]
    flt(0).n = d["-d"]
    if len(args) != 2:
        Usage(d)
    return args
def Interpret(s):
    '''Return the value given in the string s as a float.  A single
    trailing character may be an optional SI prefix.
    '''
    prefix = {
        "y": -24, "z": -21, "a": -18, "f": -15, "p": -12, "n": -9, "u":
        -6, "m": -3, "c": -2, "d": -1, "h": 2, "k": 3, "M": 6, "G": 9,
        "T": 12, "P": 15, "E": 18, "Z": 21, "Y":24}
    if not s:
        raise ValueError("Empty string in Interpret()")
    m = 1
    if s[-1] in prefix:
        m = 10**prefix[s[-1]]
        s = s[:-1]
    return flt(s)*m
if __name__ == "__main__":
    d = {} # Options dictionary
    z, theta_d = ParseCommandLine(d)
    fp = FPFormat(d["-d"])
    inf = flt(float("inf"))
    # Check the angle
    t = flt(theta_d)
    theta = radians(t)
    if not (-90 <= t <= 90):
        Error("Angle must be between -90° and 90°")
    w = 2*pi*d["-f"]            # Angular frequency in radians/s
    Z = Interpret(z)            # Magnitude of impedance in ohms
    a = 1/(w*Z)
    if t == 90:
        Rs = 0
        Rp = inf
        Q = inf
        D = 0
        Cs = a/sin(theta)
    elif t == -90:
        Rs = 0
        Rp = -inf
        Q = -inf
        D = 0
        Cs = a/sin(theta)
    else:
        theta = radians(flt(theta_d))
        Rs = Z*cos(theta)
        Rp = Z/cos(theta)
        Q = tan(abs(theta))
        D = inf if not Q else 1/Q
        Cs = inf if not theta else a/sin(theta)
    Cp = a*sin(theta)
    a = Z/w
    Ls = a*sin(theta)
    Lp = inf if not theta else a/sin(theta)
    # Correct capacitances to get conventional sign
    Cs *= -1
    Cp *= -1
    # Print report
    E = fp.engsi
    fr = E(d["-f"]) + "Hz"
    if 0:
        # Old method for python 2.7 and later
        print("Impedance(%s) =" % fr, z, "ohms @", theta_d, "deg")
        X = Z*sin(theta)
        print("  Rs = ", E(Rs), "ohm = ESR", sep="")
        print("  Rp = ", E(Rp), "ohm", sep="")
        print("  X  = ", E(X),  "ohm", sep="")
        if isinf(Cs):
            print("  Cs = inf")
        else:
            print("  Cs = ", E(Cs), "F", sep="")
        print("  Cp = ", E(Cp), "F", sep="")
        print("  Ls = ", E(Ls), "H", sep="")
        if isinf(Lp):
            print("  Lp = inf")
        else:
            print("  Lp = ", E(Lp), "H", sep="")
        if ii(Q, flt):
            print("  Q  =", sig(Q))
            print("  D  =", sig(D))
        else:
            print("  Q  =", Q)
            print("  D  =", D)
    else:
        # Use f-strings
        o = "Ω"
        if isinf(Rs):
            Rs = "∞ {o}"
        else:
            Rs = f"{E(Rs)}{o}"
        if isinf(Rp):
            Rp = f"∞ {o}"
        else:
            Rp = f"{E(Rp)}{o}"
        X = E(Z*sin(theta)) + o
        if isinf(Cs):
            Cs = f"∞ F"
        else:
            Cs = f"{E(Cs)}F"
        Cp = f"{E(Cp)}F"
        if isinf(Ls):
            Ls = "-∞ H" if Ls == -inf else "∞ H"
        else:
            Ls = f"{E(Ls)}H"
        if isinf(Lp):
            Lp = "-∞ H" if Lp == -inf else "∞ H"
        else:
            Lp = f"{E(Lp)}H"
        if isinf(Q):
            Q = "-∞" if Q == -inf else "∞"
        else:
            Q = f"{Q}" 
        if isinf(D):
            D = "-∞" if D == -inf else "∞"
        else:
            D = f"{D}"
        n = 22
        print(dedent(f'''
        Impedance({fr}) = {z}Ω @ {theta_d}°
          {Rs:>{n}s}    Rs = Equivalent series resistance
          {Rp:>{n}s}    Rp = Equivalent parallel resistance
          {X :>{n}s}    X  = Reactance
          {Cs:>{n}s}    Cs = Equivalent series capacitance
          {Cp:>{n}s}    Cp = Equivalent parallel capacitance
          {Ls:>{n}s}    Ls = Equivalent series inductance
          {Lp:>{n}s}    Lp = Equivalent parallel inductance
          {Q :>{n}s}    Q  = Quality factor
          {D :>{n}s}    D  = Dissipation factor'''))
