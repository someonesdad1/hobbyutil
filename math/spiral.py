'''
Calculate parameters of an Archimedean spiral.  The units of length are
arbitrary; the program assumes that the diameters, lengths, and thicknesses
all have the same physical unit.
 
Examples:
    1.  I have a toilet paper roll.  The paper is 0.068 mm thick, the
        roll is 120 mm in outside diameter, and the inside diameter is 44
        mm.  What is the length of paper on the roll?
 
            Choose problem 1; enter t = 0.068, D = 120, d = 44.  Get
                n = 558.824 turns
                L = 143959 mm = 144 m
 
    2.  How big in diameter will be 1000 turns of sheet metal 0.01 units
        thick?
            Choose problem 3; enter number of turns n and thickness t.  Get
                L = 31415.9
                D = 20
 
    3.  I have a piece of 2" steel pipe that has an ID of 2.07 inches.  If
        a US dollar bill is 6.1 inches long, 2.61 inches wide, and
        0.0043 inches thick, how many dollar bills could I roll up and
        put into the pipe?
            Choose problem 1 and input t = 0.004, D = 2.07, d= 0.  Get
                L = 782.6"
                n = 240.7
        If we take int(782.6/6.1), we get 128 bills.  Practically, there
        are some physical limitations that would reduce this number.  The
        bills couldn't be wound tightly starting from zero radius.  You'd
        also probably want to use some tape to hold the ends of the bills
        together; this would add to the thickness, reducing the number of
        bills in the roll.  Finally, bills that had been crumpled probably
        wouldn't lie quite as flat as new bills.  I would thus probably
        reduce the estimate by 10-20% and declare the amount to be 100
        bills.  Thus, if the bills were $100 bills, a 2 inch pipe
        could then store $10k for every 2.7 inches of length.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2010 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Calculate parameters of an Archimedean spiral
    #∞what∞#
    #∞test∞# --test #∞test∞#
    pass
if 1:   # Imports
    import sys
    import getopt
    import os
    import pathlib
    from pdb import set_trace as xx
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    from u import u, fromto, ParseUnit
    from f import flt, pi, sqrt, log, degrees
    from root import NewtonRaphson
    from lwtest import run, Assert, raises, assert_equal
if 1:   # Global variables
    P = pathlib.Path
    ii = isinstance
    problem_description = dedent('''
    Select the problem to solve (enter nothing or q to quit):
        1.  Have D, d, and t; want n and L.
        2.  Have L and t; want n and D.
        3.  Have n and t; want D and L.
        4.  Print the equations that are used.
    ''')
    # Format string for printing results of calculations
    fmt = "%.6g"
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] parameters
          Calculate the parameters of an Archimedean spiral:
            D = outside diameter of spiral
            d = inside diameter of spiral
            t = thickness of spiral's wraps
            n = number of turns
            L = total length of spiral
        Options:
          -1    Solve for n and L given D, d, t on command line
          -2    Solve for n and D given L and t on command line (assumes d = 0)
          -3    Solve for D and L given n and t on command line (assumes d = 0)
          -d n  Number of significant figures for results [{d["-d"]}]
          -h    Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-1"] = False     # Solve problem 1
        d["-2"] = False     # Solve problem 2
        d["-3"] = False     # Solve problem 3
        d["-d"] = 8         # Number of significant digits
        try:
            opts, args = getopt.getopt(sys.argv[1:], "123d:ht", "test")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("123t"):
                d[o] = not d[o]
            elif o in ("-d",):
                try:
                    d["-d"] = int(a)
                    if not (1 <= d["-d"] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = ("-d option's argument must be an integer between "
                        "1 and 15")
                    Error(msg)
            elif o in ("-h", "--help"):
                Manpage()
            elif o == "--test":
                exit(run(globals(), halt=1)[0])
        x = flt(0)
        x.n = d["-d"]
        x.rtz = x.rtdp = True
        if not args:
            Usage()
        return args
if 0:   # Core functionality
    def PrintReport(D, d, t, n, L, theta):
        fig = L.digits
        deg = theta*180/pi
        print(dedent(f'''
        Significant figures = {fig}
        Outside diameter    = {D}
        Inside diameter     = {d}
        Thickness           = {t}
        Number of turns     = {n}
        Length              = {L}
        Angle               = {theta} rad = {deg}°'''))
    def GetNum(msg, zero_ok=False, is_length=True):
        '''Prompt for the number; if is_length is True, the dimension of the
        unit must be a length.  Either a Length() object or float is
        returned.
        '''
        e = "Number must be {} 0".format(">" + "="*zero_ok)
        while True:
            print(msg, end=" ")
            s = input().strip()
            if not s or s.lower() == "q":
                exit(0)
            try:
                if is_length:
                    num = Length(s)
                else:
                    num = float(s)
                if (num < 0) or (not num and not zero_ok):
                    print(e)
                return num
            except Exception:
                print("'{}' is not a valid length".format(s))
    def Problem1():
        '''Given D, d, t find n, L.
    
        Test case:
            D = 1000 m
            d =    0 m
            t =    0.001 m
        gives
            n = 5000000.0
            L = 7.85398e12 mm
            Angle = 3.14159e+07 rad = 1.8e+09°
        '''
        if 1:
            D = GetNum("Outside diameter = D =")
            d = GetNum("Inside diameter  = d =", zero_ok=True)
            t = GetNum("Thickness        = t =")
        else:
            D = PN("1000 m")
            d = PN("0 m")
            t = PN("0.1 mm")
        # Calculation assuming D
        nD = float(D/(2*t))     # float() makes dimensionless
        thetaD = 2*pi*nD
        aD = t/(2*pi)
        AD = sqrt(thetaD*thetaD + 1)
        LD = aD*(thetaD*AD + log(thetaD + AD))/2
        # Calculation assuming d
        nd = float(d/(2*t))
        thetad = 2*pi*nd
        ad = t/(2*pi)
        Ad = sqrt(thetad*thetad + 1)
        Ld = ad*(thetad*Ad + log(thetad + Ad))/2
        # Calculate results
        n = nD - nd
        theta = PN(thetaD - thetad)
        L = LD - Ld
        PrintReport(D, d, t, n, L, theta)
    def Problem2():
        '''Given L, t find n, D.  Assumes d = 0.
        Test case:
            L = 7.85398e12 mm
            t = 0.1 mm
        gives
            Outside diameter    = 1000000 mm
            Number of turns     = 4999999.479889938
            Length              = 7.85398e12 mm
            Angle               = 31415923.26795003 rad = 1799999812.7603774 deg
        '''
        if 1:
            L = GetNum("Length           = L =")
            t = GetNum("Thickness        = t =")
        else:
            L = PN("7.85398e12 mm")
            t = PN("0.1 mm")
        a = t/(2*pi)
        # We need to find a root for theta; use Newton-Raphson.
        f = lambda x: (a/2*(x*sqrt(x*x + 1) + log(x + sqrt(x*x + 1))) - L)
        fd = lambda x: (a/2*(sqrt(x*x+1) + 2*x*x/sqrt(x*x+1) +
                        (1 + 2*x/sqrt(x*x+1))/(x + sqrt(x*x+1))))
        # Initial guess
        theta = sqrt(float(L/(2*a)))
        theta = NewtonRaphson(f, fd, theta)
        n = theta/(2*pi)
        D = 2*n*t
        d = PN(0)
        PrintReport(D, d, t, n, L, theta)
    def Problem3():
        '''Given n, t find L, D.  Assumes d = 0.
        Test case:
            n = 5e6
            t = 0.1 mm
        gives
            Outside diameter    = 1.00000e6 mm
            Inside diameter     = 0.00000
            Length              = 7.85398e12 mm
            Angle               = 31415926.535897933 rad = 1800000000.0 deg
        '''
        if 1:
            n = GetNum("Number of turns  = n =", is_length=False)
            t = GetNum("Thickness        = t =")
        else:
            n = 5e6
            t = PN("0.1 mm")
        a = t/(2*pi)
        theta = 2*pi*n
        A = sqrt(theta*theta + 1)
        L = a/2*(theta*A + log(theta + A))
        D = 2*n*t
        d = PN(0)
        PrintReport(D, d, t, n, L, theta)
    def PrintEquations():
        print(dedent(f'''
                                Equations
                                ---------
        
        The arc length L is gotten from integrating the polar equation
        of an Archimedean spiral:  r = a*theta.
        
            L = a/2*(theta*A + ln(theta + A))   = length
            where A = sqrt(theta*theta + 1)
            theta = 2*pi*n                      = angle of rotation
            D = 2*n*t                           = outside diameter
            t = 2*pi*a                          = thickness of material
        
        While the equations are exact, the numbers are most meaningful when
        t << D.'''))
    def GetDefaultLengthUnit():
        default_unit = "mm"
        print("\nEnter default length unit [{}]:  ".format(default_unit), end="")
        while True:
            s = input().strip()
            if not s:
                s = "mm"
                break
            elif s.lower() == "q":
                exit(0)
            else:
                try:
                    # See if it's a valid length unit
                    if u.dim(s) == u.dim("m"):
                        break
                except Exception as e:
                    pass
                print("Not a valid length unit -- try again:  ", end="")
        return s
    def Interactive():
        print(dedent(f'''
        Dimensions of a Archimedean spiral
        ----------------------------------
            Given a material of uniform thickness t of length L wound in a
            spiral of n turns.  A roll of this material will have an outside
            diameter D and an inside diameter d (can be zero).  Ideally, 
            t << D; if t and D are comparable, then only the calculations for
            θ and L are exact; calculated values for n and D will be approximate.
            Use any common physical length units.
        '''))
        default_unit = GetDefaultLengthUnit()
        Length = PhysicalNumberFactory(default_unit)
        while True:
            print(problem_description)
            problem = GetNum("Problem?", zero_ok=True, is_length=False)
            if problem == 1:
                Problem1()
            elif problem == 2:
                Problem2()
            elif problem == 3:
                Problem3()
            elif problem == 4:
                PrintEquations()
            else:
                print("Unrecognized problem number")
                exit(1)
def Manpage():
    print(dedent(f'''
    The polar equation of an Archimedean spiral is
    
        r = a*θ
    
    The arc length of the spiral is gotten by integrating this equation (the
    arc length formula for polar coordinates can be found in an elementary
    calculus text):
        
        L = a/2*(θ*A + ln(θ + A))
    
    where (the length dimensions must have the same units)
        A = sqrt(θ² + 1)
        θ = 2*π*n = angle of rotation
        t = 2*π*a = thickness of material = distance between successive arcs
        D = 2*n_D*t = outside diameter
        d = inside diameter (can be zero) = 2*n_d*t
 
    While the equations are exact, the numbers are most meaningful when t << D.
 
    The functional forms of L are
 
        L = f(t, θ)
 
    If you're given the length, you have to solve a transcendental equation
    for the other variables.  This is done by a Newton-Raphson root-finding
    routine.
 
    Example:
 
        I have a roll of toilet paper and the paper is 0.068 mm thick.  The
        outside diameter D is 120 mm and the inside diameter d is 44 mm.
        What length of toilet paper is on the roll?  We have
 
            t = 0.068
            D = 120
            d = 44
        
        Calculate n and L for the diameter D:
            n = 882.3529411764705
            a = 0.010822536130248884
            θ = 5543.987035746693
            A = 5543.987125934494
            L = 166319.66417650974
 
        Calculate n and L for the diameter d:
            n = 323.52941176470586
            a = 0.010822536130248884
            θ = 2032.795246440454
            A = 2032.7954924071696
            L = 22360.795385817433
        The desired length is the difference of these two lengths: 
            Length = 166319.66417650974 - 22360.795385817433
                   = 143958.8687906923 mm
            or about 144 meters which is 472 feet.
 
    '''))
    exit(0)
class Spiral(object):
    def __init__(self):
        self.clear()
    def clear(self):
        self._D = None
        self._d = None
        self._t = None
        self._n = None
        self._L = None
    def solve(self, problem):
        'Return dict of variables if solvable; None if not'
        '''Equations:
            L = a/2*(θ*A + ln(θ + A))
            A = sqrt(θ² + 1)
            θ = 2*π*n = angle of rotation
            t = 2*π*a = thickness of material = distance between successive arcs
            D = 2*n_D*t = outside diameter
            d = inside diameter (can be zero) = 2*n_d*t
        '''
        di = {"D": None, "d": None, "t": None, "n": None, "L": None}
        # Functions to use Newton-Raphson to find θ given a and L
        f = lambda x: (a/2*(x*sqrt(x*x + 1) + log(x + sqrt(x*x + 1))) - L)
        fd = lambda x: (a/2*(sqrt(x*x+1) + 2*x*x/sqrt(x*x+1) +
                        (1 + 2*x/sqrt(x*x+1))/(x + sqrt(x*x+1))))
        if problem == 1:
            # Given D, d, t
            if not self.is_solvable(problem):
                return None
            D, d, t = flt(self._D), flt(self._d), flt(self._t)
            if d > D:
                d, D = D, d
            n_D, n_d = D/(2*t), d/(2*t)
            a = t/(2*pi)
            # L for D
            θ = 2*pi*n_D
            A = sqrt(θ*θ + 1)
            L_D = a/2*(θ*A + log(θ + A))
            # L for d
            θ = 2*pi*n_d
            A = sqrt(θ*θ + 1)
            L_d = a/2*(θ*A + log(θ + A))
            L = L_D - L_d
            di["D"] = D
            di["d"] = d
            di["t"] = t
            di["n"] = self.n = n_D - n_d
            di["L"] = self.L = L_D - L_d
        elif problem == 2:
            # Given L, t
            if not self.is_solvable(problem):
                return None
            L, t = flt(self._L), flt(self._t)
            a = t/(2*pi)
            θ0 = sqrt(flt(L/(2*a)))   # Initial guess for θ
            θ = NewtonRaphson(f, fd, θ0, fp=flt)
            n = θ/(2*pi)
            di["D"] = self.D = 2*n*t
            di["d"] = self.d = flt(0)
            di["t"] = t
            di["n"] = self.n = n
            di["L"] = L
        elif problem == 3:
            # Given n, t
            if not self.is_solvable(problem):
                return None
            n, t = flt(self._n), flt(self._t)
            a = t/(2*pi)
            θ = 2*pi*n
            A = sqrt(θ*θ + 1)
            L = a/2*(θ*A + log(θ + A))
            D = 2*n*t
            d = flt(0)
            di["D"] = self.D = D
            di["d"] = self.d = d
            di["t"] = t
            di["n"] = n
            di["L"] = self.L = L
        else:
            raise ValueError(f"{problem} is bad problem number")
        for i in "DdtLn":
            assert i in di and di[i] is not None, f"'{i}' is missing"
        return di
    def is_solvable(self, problem):
        f = lambda x: True if x is not None else False
        if problem == 1:
            return f(self._D) and f(self._d) and f(self._t)
        elif problem == 2:
            return f(self._L) and f(self._t)
        elif problem == 3:
            return f(self._n) and f(self._t)
        else:
            raise ValueError(f"{problem} is bad problem number")
    def PrintReport(self):
        θ = 2*pi*self.n
        print(dedent(f'''
        Outside diameter    = {self.D}
        Inside diameter     = {self.d}
        Thickness           = {self.t}
        Number of turns     = {self.n}
        Length              = {self.L}
        Angle               = {θ} rad = {degrees(θ)}°'''))
    @property
    def D(self):
        return self._D
    @D.setter
    def D(self, value):
        self._D = flt(value)
        if self._D <= 0:
            raise ValueError("Value for D must be > 0")
        if self._d is not None and self._D <= self._d:
            raise ValueError("Value for D must be > d")
    @property
    def d(self):
        return self._d
    @d.setter
    def d(self, value):
        self._d = flt(value)
        if self._d < 0:
            raise ValueError("Value for d must be >= 0")
        if self._D is not None and self._d >= self._D:
            raise ValueError("Value for d must be < D")
    @property
    def t(self):
        return self._t
    @t.setter
    def t(self, value):
        self._t = flt(value)
        if self._t <= 0:
            raise ValueError("Value for t must be > 0")
    @property
    def n(self):
        return self._n
    @n.setter
    def n(self, value):
        self._n = flt(value)
        if self._n <= 0:
            raise ValueError("Value for n must be > 0")
    @property
    def L(self):
        return self._L
    @L.setter
    def L(self, value):
        self._L = flt(value)
        if self._L <= 0:
            raise ValueError("Value for L must be > 0")
def Test_Spiral():
    'Test the basic functionality of the Spiral object'
    s, eps = Spiral(), 1e-6
    flt(0).n = 15
    flt(0).rtz = flt(0).rtdp = True
    D, d, t, n, L = 1000, 0, 0.001, 5e5, 785398163.398734
    # Problem 1:  
    #   D = 1000
    #   d =    0
    #   t =    0.001
    # gives
    #   n = 5e5
    #   L = 7.85398e8
    s.clear()
    s.D = D
    s.d = d
    s.t = t
    di = s.solve(1)
    #s.PrintReport();print()
    assert_equal(di["n"], n, reltol=eps)
    assert_equal(di["L"], L, reltol=eps)
    # Problem 2:  
    #   L = 785398163.398734
    #   t =    0.001
    # gives
    #   D = 1000
    #   d =    0
    s.clear()
    s.L = L
    s.t = t
    di = s.solve(2)
    #s.PrintReport();print()
    assert_equal(di["n"], n, reltol=eps)
    assert_equal(di["D"], D, reltol=eps)
    # Problem 3:  
    #   n = 5e5
    #   t =    0.001 m
    # gives
    #   D = 1000
    #   L = 7.85398e8
    s.clear()
    s.n = n
    s.t = t
    di = s.solve(3)
    #s.PrintReport()
    assert_equal(di["L"], L, reltol=eps)
    assert_equal(di["D"], D, reltol=eps)
if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    s = Spiral()
    if d["-1"]:
        if len(args) != 3:
            Error("Need 3 arguments for problem 1")
        s.D, s.d, s.t = [flt(i) for i in args]
        s.solve(1)
        s.PrintReport()
    elif d["-2"]:
        if len(args) != 2:
            Error("Need 2 arguments for problem 2")
        s.L, s.t = [flt(i) for i in args]
        s.solve(2)
        s.PrintReport()
    elif d["-3"]:
        if len(args) != 2:
            Error("Need 2 arguments for problem 3")
        s.n, s.t = [flt(i) for i in args]
        s.solve(3)
        s.PrintReport()
    else:
        Usage()
if 0:
    #----------------------------------------------------------------------
    # ToDo:  Add an option to plot a spiral:
    # 
    #     from math import sqrt, sin, cos, pi, log
    #     from g import *
    #     def DrawSpiral(file, a, theta1, theta2):
    #         'Generate a PostScript file showing a spiral'
    #         import pdb, sys, string
    #         wrap_in_PJL = 0
    #         def SetUp(file, orientation=portrait, units=inches):
    #             '''Convenience function to set up the drawing environment and
    #             return a file object to the output stream.
    #             '''
    #             ofp = open(file, "w")
    #             ginitialize(ofp, wrap_in_PJL)
    #             setOrientation(orientation, units)
    #             return ofp
    #         def Seq(start, stop, increment):
    #             N = int((stop - start)/increment) + 1
    #             return [start + i*increment for i in range(N)]
    #         def Rect(r, theta):
    #             return (r * cos(theta), r * sin(theta))
    #         def Draw(num_revolutions, a, dtheta, cw=0):
    #             push()
    #             move(0, 0)
    #             xlast, ylast = 0, 0
    #             for theta in Seq(0, num_revolutions*pi, dtheta):
    #                 if cw:
    #                     theta = -theta
    #                 x, y = Rect(r=a*theta, theta=theta)
    #                 line(xlast, ylast, x, y)
    #                 xlast, ylast = x, y
    #             pop()
    #         def main():
    #             ofp = SetUp(file, landscape)
    #             translate(11/2, 8.5/2)
    #             # Polar equation of an archimedian spiral is r = a*theta
    #             Nrevolutions = 10
    #             dtheta = pi/100
    #             Draw(Nrevolutions, a, dtheta)
    #             ofp.close()
    #         main()
    #     DrawSpiral("a.ps", 0.1, 0, 10*pi)
    #     exit()
    pass

