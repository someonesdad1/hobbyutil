'''
Circular segment computations

Translation of Marv Klotz's cseg.c program dated 11/98 (see cseg.zip
at http://www.myvirtualnetwork.com/mklotz/).

TODO:

    * Angle iteration causes a bug when uncertainties are used, as the
      angle will never have an associated uncertainty.
'''

XXXX  This script is not working

# Copyright (C) 2013 Don Peterson
# Contact:  gmail.com@someonesdad1

#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#

from __future__ import print_function, division
import sys
from math import *
from sig import sig

from pdb import set_trace as xx

dbg = False

have_unc = False
try:
    # If you wish to add uncertainties to numbers, you'll need to install
    # the uncertainties library from
    # http://pypi.python.org/pypi/uncertainties/.  The script will
    # operate OK if you do not have this library, but any
    # uncertainties you type in will be ignored.
    from uncertainties import ufloat, AffineScalarFunc
    from uncertainties.umath import cos, sin, asin, acos
    have_unc = True
except ImportError:
    pass

if sys.version_info[0] == 3:
    py3 = True
    Input = input
else:
    py3 = False
    Input = raw_input

d2r = pi/180    # Constant for converting degrees to radians
r2d = 1/d2r

def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)

def Dict(vars):
    '''vars is a dictionary of local variables.  Remove all variable
    names that begin with two underscores and also remove __d.
    '''
    v = vars.copy()
    if "__d" in v:
        del v["__d"]
    keys = list(v.keys())
    rm = []
    for k in keys:
        if len(k) > 2 and k[:2] == "__":
            rm.append(k)
    for i in rm:
        del v[i]
    return v

def InterpretNum(__s, __vars):
    '''__s is a string that can be of the forms e.g. '12.3' or
    '12.3[0.1]' where the second form denotes an uncertainty.  The
    numbers can also be expressions using the variables in the __vars
    dictionary.  Evaluate the string and return either a floating
    point number or a ufloat.

    Note we'll raise an exception if the number is negative.
    '''
    # Get vars into our local namespace
    for __k in __vars:
        exec("%s = __vars['%s']" % (__k, __k))
    try:
        if "[" in __s:
            __locl, __locr = __s.find("["), __s.find("]")
            if __locl > __locr:
                raise Exception("Improperly formed uncertainty")
            __mean = float(eval(__s[:__locl]))
            if __mean < 0:
                raise ValueError("Value must be greater than zero")
            __stddev = float(eval(__s[__locl + 1:__locr]))
            if have_unc:
                return ufloat(__mean, __stddev)
            else:
                return __mean
        else:
            __mean = float(eval(__s))
            if __mean <= 0:
                raise CannotBeZero("Value must be greater than zero")
            return __mean
    except Exception as __e:
        Error("Can't evaluate '%s'\n  Error:  %s" % (__s, str(__e)))

def GetNumber(prompt, default_value="0", __vars=None):
    '''Prompt the user until a number >= 0 has been gotten.  Return a
    float (or a ufloat if an uncertainty has been given).
    '''
    # Get vars into our local namespace
    if __vars is not None:
        for __k in __vars:
            exec("%s = __vars['%s']" % (__k, __k))
    msg = prompt + " [%s]  " % default_value
    while True:
        __s = Input(msg).strip()
        if __s in ("q", "Q"):
            exit(0)
        elif not __s:
            return float(default_value)
        elif "=" in __s:
            try:
                exec(__s)
                print("Assignment OK")
            except Exception as e:
                print("Assignment failed:  %s" % str(e))
        else:
            try:
                __x = InterpretNum(__s, Dict(locals()))
                return __x
            except Exception as e:
                print("Number not correct:  %s" % str(e))

# To utilize Marv's code, here are definitions for the macros and
# constants/variables he uses.
ABS = abs
SGN = lambda a: -1 if a < 0 else 0 if a == 0 else 1
DPR = 180/pi
RPD = pi/180
COSD = lambda a:  cos(a*RPD)
SIND = lambda a:  sin(a*RPD)
ASND = lambda a:  DPR*asin(a if abs(a) < 1 else SGN(a))
ACSD = lambda a:  DPR*acos(a if abs(a) < 1 else SGN(a))

def Calculate(__vars, __d):
    # Get vars into our local namespace
    if __vars is not None:
        for __k in __vars:
            if len(__k) > 2 and __k[:2] == "__":
                continue
            exec("%s = __vars['%s']" % (__k, __k))
    try:
        if radius and angle:
            if dbg:
                print("radius, angle", sig(radius), sig(angle))
            z = radius*COSD(0.5*angle)
            height = radius - z
            chord = 2.*radius*SIND(0.5*angle)
            arc = radius*angle*RPD
        elif radius and chord:
            if dbg:
                print("radius, chord", sig(radius), sig(chord))
            angle = 2.*ASND(0.5*chord/radius)
            z = radius*COSD(0.5*angle)
            height = radius - z
            arc = radius*angle*RPD
        elif radius and height:
            if dbg:
                print("radius, height", sig(radius), sig(height))
            z = radius - height
            angle = 2.*ACSD(z/radius)
            chord = 2.*radius*SIND(0.5*angle)
            arc = radius*angle*RPD
        elif radius and arc:
            if dbg:
                print("radius, arc", sig(radius), sig(arc))
            angle = DPR*arc/radius
            z = radius*COSD(0.5*angle)
            height = radius - z
            chord = 2.*radius*SIND(0.5*angle)
        elif angle and chord:
            if dbg:
                print("angle, chord", sig(angle), sig(chord))
            radius = 0.5*chord/SIND(0.5*angle)
            z = radius*COSD(0.5*angle)
            height = radius - z
            arc = radius*angle*RPD
        elif angle and height:
            if dbg:
                print("angle, height", sig(angle), sig(height))
            radius = height/(1. - COSD(0.5*angle))
            z = radius - height
            chord = 2.*radius*SIND(0.5*angle)
            arc = radius*angle*RPD
        elif angle and arc:
            if dbg:
                print("angle, arc", sig(angle), sig(arc))
            radius = DPR*arc/angle
            z = radius*COSD(0.5*angle)
            height = radius - z
            chord = 2.*radius*SIND(0.5*angle)
        elif chord and height:
            if dbg:
                print("chord, height", sig(chord), sig(height))
            radius = (4.*height*height + chord*chord)/(8.*height)
            z = radius - height
            angle = 2.*ACSD(z/radius)
            arc = radius*angle*RPD
        elif chord and arc:
            if dbg:
                print("chord, arc", sig(chord), sig(arc))
            h, t1, t2, dt, hbest, k = 0, 1, 180, 1, 1e6, 0
            while ABS(h - chord) > 1e-6 and k < 6:
                angle = t1
                while angle <= t2:
                    radius = DPR*arc/angle
                    h = 2.*radius*SIND(0.5*angle)
                    if ABS(h - chord) < hbest:
                        hbest = ABS(h - chord)
                        tbest = angle
                    angle += dt
                t1 = tbest - dt
                t2 = tbest + dt
                dt *= 0.1
                k += 1
            # Note that angle will not have an uncertainty associated
            # with it because it was derived through iteration in the
            # loop.
            angle = tbest
            radius = DPR*arc/angle
            height = radius*(1 - COSD(0.5*angle))
        elif height and arc:
            if dbg:
                print("height, arc", sig(height), sig(arc))
            h, t1, t2, dt, hbest, k = 0, 1, 180, 1, 1e6, 0
            while ABS(h - height) > 1e-6 and k < 6:
                angle = t1
                while angle <= t2:
                    radius = DPR*arc/angle
                    h = radius*(1 - COSD(0.5*angle))
                    if ABS(h - height) < hbest:
                        hbest = ABS(h - height)
                        tbest = angle
                    angle += dt
                t1 = tbest - dt
                t2 = tbest + dt
                dt *= 0.1
                k += 1
            # Note that angle will not have an uncertainty associated
            # with it because it was derived through iteration in the
            # loop.
            angle = tbest
            radius = DPR*arc/angle
            chord = 2.*radius*SIND(0.5*angle)
    except Exception as e:
        if dbg:
            print("Exception in Calculate(): ", str(e))
        return False
    # Put answers into dictionary
    __d["diameter"] = 2*radius
    __d["radius"] = radius
    __d["angle"] = angle
    __d["chord"] = chord
    __d["height"] = height
    __d["arc"] = arc
    return True

def Report(d):
    angle = sig(d["angle"])
    arc = sig(d["arc"])
    chord = sig(d["chord"])
    diameter = sig(d["diameter"])
    height = sig(d["height"])
    radius = sig(d["radius"])
    print('''Results:
  Angle     {angle} deg
  Arc       {arc}
  Chord     {chord}
  Diameter  {diameter}
  Height    {height}
  Radius    {radius}'''.format(**locals()))

def SelfTests():
    '''Run some known cases to make sure the answers are reasonable.
    '''
    def Assert(cond):
        if not cond:
            raise ValueError("Assertion failed -- self-tests thus fail")
    def Get(d):
        angle = d["angle"]
        arc = d["arc"]
        chord = d["chord"]
        height = d["height"]
        radius = d["radius"]
        return angle, arc, chord, height, radius
    eps = 1e-15
    if 1:   # Full circle
        eps = 1e-15
        radius, angle, chord, height, arc, d = 0, 0, 0, 0, 0, {}
        radius, angle = 1, 360
        ok = Calculate(locals(), d)
        Assert(ok)
        angle, arc, chord, height, radius = Get(d)
        Assert(abs(arc - 2*pi*radius) < eps)
        Assert(abs(chord) < eps)
        Assert(abs(height - 2*radius) < eps)
    if 1:    # Semicircle
        # radius, angle
        radius, angle, chord, height, arc, d = 0, 0, 0, 0, 0, {}
        radius, angle = 1, 180
        ok = Calculate(locals(), d)
        Assert(ok)
        angle, arc, chord, height, radius = Get(d)
        Assert(abs(arc - pi*radius) < eps)
        Assert(abs(chord - 2*radius) < eps)
        Assert(abs(height - radius) < eps)
        # radius, chord
        radius, angle, chord, height, arc, d = 0, 0, 0, 0, 0, {}
        radius, chord = 1, 2
        ok = Calculate(locals(), d)
        Assert(ok)
        angle, arc, chord, height, radius = Get(d)
        Assert(abs(arc - pi*radius) < eps)
        Assert(abs(angle - 180) < eps)
        Assert(abs(height - radius) < eps)
        # radius, height
        radius, angle, chord, height, arc, d = 0, 0, 0, 0, 0, {}
        radius, height = 1, 1
        ok = Calculate(locals(), d)
        Assert(ok)
        angle, arc, chord, height, radius = Get(d)
        Assert(abs(arc - pi*radius) < eps)
        Assert(abs(angle - 180) < eps)
        Assert(abs(chord - 2*radius) < eps)
        # radius, arc
        radius, angle, chord, height, arc, d = 0, 0, 0, 0, 0, {}
        radius, arc = 1, pi
        ok = Calculate(locals(), d)
        Assert(ok)
        angle, arc, chord, height, radius = Get(d)
        Assert(abs(height - radius) < eps)
        Assert(abs(angle - 180) < eps)
        Assert(abs(chord - 2*radius) < eps)
        # angle, chord
        radius, angle, chord, height, arc, d = 0, 0, 0, 0, 0, {}
        angle, chord = 180, 2
        ok = Calculate(locals(), d)
        Assert(ok)
        angle, arc, chord, height, radius = Get(d)
        Assert(abs(height - radius) < eps)
        Assert(abs(radius - 1) < eps)
        Assert(abs(arc - pi*radius) < eps)
        # angle, height
        radius, angle, chord, height, arc, d = 0, 0, 0, 0, 0, {}
        angle, height = 180, 1
        ok = Calculate(locals(), d)
        Assert(ok)
        angle, arc, chord, height, radius = Get(d)
        Assert(abs(chord - 2*radius) < eps)
        Assert(abs(radius - 1) < eps)
        Assert(abs(arc - pi*radius) < eps)
        # angle, arc
        radius, angle, chord, height, arc, d = 0, 0, 0, 0, 0, {}
        angle, arc = 180, pi
        ok = Calculate(locals(), d)
        Assert(ok)
        angle, arc, chord, height, radius = Get(d)
        Assert(abs(chord - 2*radius) < eps)
        Assert(abs(radius - 1) < eps)
        Assert(abs(height - radius) < eps)
        # chord, height
        radius, angle, chord, height, arc, d = 0, 0, 0, 0, 0, {}
        chord, height = 2, 1
        ok = Calculate(locals(), d)
        Assert(ok)
        angle, arc, chord, height, radius = Get(d)
        Assert(abs(angle - 180) < eps)
        Assert(abs(radius - 1) < eps)
        Assert(abs(arc - pi) < eps)
        # chord, arc
        radius, angle, chord, height, arc, d = 0, 0, 0, 0, 0, {}
        chord, arc = 2, pi
        ok = Calculate(locals(), d)
        Assert(ok)
        angle, arc, chord, height, radius = Get(d)
        Assert(abs(angle - 180) < eps)
        Assert(abs(radius - 1) < eps)
        Assert(abs(height - radius) < eps)
        # height, arc
        radius, angle, chord, height, arc, d = 0, 0, 0, 0, 0, {}
        height, arc = 1, pi
        ok = Calculate(locals(), d)
        Assert(ok)
        angle, arc, chord, height, radius = Get(d)
        Assert(abs(angle - 180) < eps)
        Assert(abs(radius - 1) < eps)
        Assert(abs(chord - 2*radius) < eps)
    print("Tests passed")
    exit(0)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "-t":
        SelfTests()
    print('''
Circular Segment Calculations
  Input what you know; enter 0 for an unknown (just press return if
  not known.  You must two items to obtain a solution.
'''[1:-1])
    while True:
        __s = Input("How many significant figures in report? [4] ").strip()
        if __s in ("q", "Q"):
            exit(0)
        elif not __s:
            sig.digits = 4
            break
        else:
            try:
                __n = int(__s)
                if not (1 <= __n <= 15):
                    print("Must be between 1 and 15")
                else:
                    sig.digits = __n
                    break
            except Exception:
                print("'%s' is not a valid integer" % __s)
    __vars, __num_params, __ok, __d = {}, 0, False, {}
    radius, angle, chord, height, arc = 0, 0, 0, 0, 0
    radius = GetNumber("Radius of segment", default_value=0, __vars=__vars)
    if radius:
        __num_params += 1
    angle = GetNumber("Segment included angle", default_value=0,
                      __vars=__vars)
    if angle:
        __num_params += 1
    if __num_params == 2:
        __ok = Calculate(Dict(locals()), __d)
    else:
        chord = GetNumber("Chord of segment", default_value=0,
                          __vars=__vars)
        if chord:
            __num_params += 1
        if __num_params == 2:
            __ok = Calculate(Dict(locals()), __d)
        height = GetNumber("Height of segment (sagitta)",
                           default_value=0, __vars=__vars)
        if height:
            __num_params += 1
        if __num_params == 2:
            __ok = Calculate(Dict(locals()), __d)
        else:
            arc = GetNumber("Arc length", default_value=0,
                            __vars=__vars)
            if arc:
                __num_params += 1
            if __num_params == 2:
                __ok = Calculate(Dict(locals()), __d)
    if not __ok:
        print("Insufficient data for solution")
        exit(1)
    Report(__d)
