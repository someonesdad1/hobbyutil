'''
Given a measured impedance in polar coordinates, prints out the
associated parameters that can be calculated.
'''

# Copyright (C) 2014 Don Peterson
# Contact:  gmail.com@someonesdad1

#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#

import getopt
import os
import sys
from math import tan, sin, cos, pi, isinf
from sig import sig
from fpformat import FPFormat

from pdb import set_trace as xx

def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)

def Usage(d, status=1):
    name = sys.argv[0]
    s = f'''
Usage:  {name} [options] Z theta
  Given a measured impedance with magnitude Z in ohms and phase angle
  theta in degrees, prints out the associated parameters.  You can use
  a cuddled SI prefix after the number for Z if you wish (example:
  1.23k means 1230 ohms).
 
Options
    -d digits
        Use the indicated number of significant digits for output.  [{d["-d"]}]
    -f freq_Hz
        Specify measurement frequency in Hz.  You can use a cuddled SI 
        prefix after the number.  [{d["-f"]} Hz]
'''[1:-1]
    print(s.format(**locals()))
    sys.exit(status)

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
    for opt in optlist:
        if opt[0] == "-d":
            try:
                d["-d"] = int(opt[1])
            except ValueError:
                Error("-d option invalid")
            if not(1 <= d["-d"] <= 15):
                Error("-d option must be between 1 and 15")
        if opt[0] == "-f":
            try:
                d["-f"] = Interpret(opt[1])
            except ValueError:
                Error("-f option invalid")
            if d["-f"] <= 0:
                Error("-f option must be > 0")
    sig.digits = d["-d"]
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
    return float(s)*m

if __name__ == "__main__":
    d = {} # Options dictionary
    z, theta_d = ParseCommandLine(d)
    fp = FPFormat(d["-d"])
    theta = float(theta_d)*pi/180  # Convert to radians
    w = 2*pi*d["-f"]        # Angular frequency in radians/s
    Z = Interpret(z)        # Magnitude of impedance in ohms
    Rs = Z*cos(theta)
    Rp = Z/cos(theta)
    try:
        Q = tan(abs(theta))
        D = 1/Q
    except Exception:
        Q = "inf"
        D = "0"
    a = 1/(w*Z)
    try:
        Cs = a/sin(theta)
    except ZeroDivisionError:
        Cs = float("-inf")
    Cp = a*sin(theta)
    a = Z/w
    Ls = a*sin(theta)
    try:
        Lp = a/sin(theta)
    except ZeroDivisionError:
        Lp = float("inf")
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
        if isinstance(Q, float):
            print("  Q  =", sig(Q))
            print("  D  =", sig(D))
        else:
            print("  Q  =", Q)
            print("  D  =", D)
    else:
        # Use f-strings
        o = "Ω"
        Rs = f"{E(Rs)}{o}"
        Rp = f"{E(Rp)}{o}"
        X = E(Z*sin(theta)) + o
        if isinf(Cs):
            Cs = f"∞ F"
        else:
            Cs = f"{E(Cs)}F"
        Cp = f"{E(Cp)}F"
        Ls = f"{E(Ls)}H"
        if isinf(Lp):
            Lp = "∞ H"
        else:
            Lp = f"{E(Lp)}H"
        Q = f"{sig(Q)}"
        D = f"{sig(D)}"
        n = 12
        print(f'''
Impedance({fr}) = {z}Ω @ {theta_d}°
  {Rs:>{n}s}    Rs = Equivalent series resistance
  {Rp:>{n}s}    Rp = Equivalent parallel resistance
  {X :>{n}s}    X  = Reactance
  {Cs:>{n}s}    Cs = Equivalent series capacitance
  {Cp:>{n}s}    Cp = Equivalent parallel capacitance
  {Ls:>{n}s}    Ls = Equivalent series inductance
  {Lp:>{n}s}    Lp = Equivalent parallel inductance
  {Q :>{n}s}    Q  = Quality factor
  {D :>{n}s}    D  = Dissipation factor'''[1:])
