# TODO:  Convert Spinner to a class so the instance is thread-safe
#   Debug class should use print()'s arguments
'''Miscellaneous routines in python:
 
Ampacity              Returns NEC ampacity of copper wire
AWG                   Returns wire diameter in inches for AWG gauge number
Batch                 Generator to pick n items at a time from a sequence
BraceExpansion        Brace expansion like modern shells
Cfg                   Execute a sequence of text lines for config use
ConvertToNumber       Convert a string to a number
Debug                 A class that helps with debugging
Dispatch              Class to aid polymorphism
iDistribute           Return an integer sequence equally distributed
fDistribute           Return a float sequence equally distributed
EBCDIC                Return string translation table ASCII <--> EBCDIC
eng                   Convenience function for engineering format
EditData              Edit a str or bytes object with vim
Engineering           Represent a number in engineering notation
execfile              Python 3 replacement for python 2 function
Flatten               Flattens nested sequences to a sequence of scalars
GroupByN              Group items from a sequence by n items at a time
grouper               Function to group data
HeatIndex             Effect of temperature and humidity
Height                Predict a child's adult height
hyphen_range          Returns list of integers specified as ranges
IdealGas              Calculate ideal gas P, v, T (v is specific volume)
IsBinaryFile          Heuristic to see if a file is a binary file
IsConvexPolygon       Is seq of 2-D points a convex polygon?
IsCygwinSymlink       Returns True if a file is a cygwin symlink
IsIterable            Determines if you can iterate over an object
IsTextFile            Heuristic to see if a file is a text file
ItemCount             Summarize a sequence with counts of each item
Now                   Time or datetime as now
Paste                 Return sequence of pasted sequences
PPSeq                 Class for formatting number sequences for pretty printing
ProgressBar           Prints a progress bar to stdout
randq                 Simple, fast random number generator
randr                 Random numbers on [0,1) using randq
RandomIntegers        Return a list of random integers
ReadVariables         Read variables from a file
RemoveIndent          Remove spaces from beginning of multiline string
SignificantFigures    Rounds to specified num of sig figs (returns float)
SignificantFiguresS   Rounds to specified num of sig figs (returns string)
signum                Return -1, 0, or 1 if x < 0, == 0, or > 0
Singleton             Mix-in class to create the singleton pattern
SizeOf                Estimate memory of an object in bytes
SpeedOfSound          Calculate the speed of sound as func of temperature
Spinner               Console spinner to show activity
StringToNumbers       Convert a string to a sequence of numbers
TempConvert           Convert a temperature
Time                  Returns a string giving local time and date
TranslateSymlink      Returns what a cygwin symlink is pointing to
US_states             Dictionary of states keyed by 2-letter abbreviation
VisualCount           Return a list representing a histogram of a sequence
Walker  (deprecated)  Generator to recursively return files or directories
WindChillInDegF       Calculate wind chill given OAT & wind speed
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
    # <utility> Contains over 60 utility functions.
    #∞what∞#
    #∞test∞# run #∞test∞#
    pass
if 1:   # Imports
    from collections import deque, defaultdict, OrderedDict
    from collections.abc import Iterable
    from decimal import Decimal
    from fractions import Fraction
    from heapq import nlargest
    from itertools import chain, combinations, islice, groupby
    from itertools import cycle, zip_longest, product
    from operator import itemgetter
    from pathlib import Path as P
    from pdb import set_trace as xx
    from random import randint, seed
    from reprlib import repr as Repr
    from string import ascii_letters, digits as DIGITS, punctuation

    import cmath
    import glob
    import math
    import os
    import random
    import re
    import struct
    import subprocess
    import sys
    import tempfile
    import time

if 1:   # Custom imports
    import f
    from dpmath import AlmostEqual, SignSignificandExponent, signum
    from sig import sig
    from kolor import C
    from frange import frange
if 1:   # Global variables
    ii = isinstance
    nl = "\n"
    # Note:  this choice of a small floating point number may be
    # wrong on a system that doesn't use IEEE floating point numbers.
    eps = 1e-15
    # Dictionary of US state abbreviations
    a = '''AK AL AR AZ CA CO CT DE FL GA HI IA ID IL IN KS KY LA MA MD ME MI
        MN MO MS MT NC ND NE NH NJ NM NV NY OH OK OR PA RI SC SD TN TX UT
        VA VT WA WI WV WY'''.split()
    b = [i.replace("·", " ") for i in '''Alaska Alabama Arkansas Arizona
        California Colorado Connecticut Delaware Florida Georgia Hawaii
        Iowa Idaho Illinois Indiana Kansas Kentucky Louisiana
        Massachusetts Maryland Maine Michigan Minnesota Missouri
        Mississippi Montana North·Carolina North·Dakota Nebraska
        New·Hampshire New·Jersey New·Mexico Nevada New·York Ohio Oklahoma
        Oregon Pennsylvania Rhode·Island South·Carolina South·Dakota
        Tennessee Texas Utah Virginia Vermont Washington Wisconsin
        West·Virginia Wyoming'''.split()]
    US_states = dict(zip(a, b))
    del a, b
def ItemCount(seq, n=None):
    '''Return a sorted list of the items and their counts in the iterable
    seq, with the largest count first in the tuple.  If n is given, only
    return the largest n counts.  The items in seq must be hashable.
 
    Example:
      If a = (1, 1, 1, 2, 3, 4, 4, 5, 5, 5, 5, 5), then ItemCount(a)
      returns [(5, 5), (1, 3), (4, 2), (2, 1), (3, 1)].
 
      If a = (1.0, 1, 1, 2, 3, 4, 4, 5, 5, 5, 5, 5), then ItemCount(a)
      returns [(5, 5), (1.0, 3), (4, 2), (2, 1), (3, 1)].
 
    Note that 1, 1.0, and Fraction(1, 1) hash to the same value; since a
    dictionary is used as the counting container, these are considered to
    be the same items.  Thus, you can get syntactically different results
    that are semantically the same.
    '''
    items = defaultdict(int)
    for item in seq:
        items[item] += 1
    s = sorted(items.items(), key=itemgetter(1), reverse=True)
    return s if n is None else s[:n]
def VisualCount(seq, n=None, char="*", width=None, indent=0):
    '''Return a list of strings representing a histogram of the items in
    the iterable seq.  If the values in the sequence can be sorted, the
    histogram will be shown by increasing item value; otherwise, the items
    will be shown sorted by frequency.
 
    n       Return the n largest items if n is not None.
    char    String to build the histogram element.
    width   Fit each element into this width.  If none, use the value of
            the COLUMNS environment variable or 79 if it isn't defined.
    indent  Indent each line by this amount.
 
    Note:  the width calculations are only correct if the length of the
    char string is 1.
 
    Example:  
        seq = [1,1,1,1,1,8,8,8,9,9,9,9,9,9,9,9,9,9,9]
        for i in VisualCount(seq, width=40, indent=8):
            print(i)
        prints
            1 *************
            8 ********
            9 ******************************
    '''
    counts = ItemCount(seq, n=n)
    try:
        counts = sorted(counts)     # Sort by item values if possible
    except TypeError:
        pass
    max_obj_len = max([len(str(i[0])) for i in counts])
    max_count = max([i[1] for i in counts])
    if width is None:
        width = int(os.environ.get("COLUMNS", 80)) - 1
    max_hist_len = width - indent - 1 - max_obj_len
    assert(max_hist_len > 0)
    # Scale counts to fit on screen
    counts = [(i, int(j/max_count*max_hist_len)) for i, j in counts]
    # Construct the output list
    output = []
    for item, count in counts:
        s = "{}{:{}s} ".format(" "*indent, str(item), max_obj_len)
        output.append(s + char*count)
    return output
class Singleton(object):
    '''Mix-in class to make an object a singleton.  From 'Python in a
    Nutshell', p 84.
    '''
    _singletons = {}
    def __new__(cls, *args, **kw):
        if cls not in cls._singletons:
            cls._singletons[cls] = object.__new__(cls)
        return cls._singletons[cls]
def RemoveIndent(s, numspaces=4):
    '''Given a multi-line string s, remove the indicated number of
    spaces from the beginning each line.  If that number of space
    characters aren't present, then leave the line alone.
    '''
    if numspaces < 0:
        raise ValueError("numspaces must be >= 0")
    lines = s.split(nl)
    for i, line in enumerate(lines):
        if line.startswith(" "*numspaces):
            lines[i] = lines[i][numspaces:]
    return nl.join(lines)
def Batch(iterable, size):
    '''Generator that gives you batches from an iterable in manageable
    sizes.  Slightly adapted from Raymond Hettinger's entry in the
    comments to
    http://code.activestate.com/recipes/303279-getting-items-in-batches/
 
    Example:
        for n in (3, 4, 5, 6):
            s = tuple(tuple(i) for i in Batch(range(n), 3))
            print(s)
    gives
        ((0, 1, 2),)
        ((0, 1, 2), (3,))
        ((0, 1, 2), (3, 4))
        ((0, 1, 2), (3, 4, 5))
 
    Another way of doing this is with slicing (but you'll need to have
    the whole iterable in memory to do this):
        def Pick(iterable, size):
            i = 0
            while True:
                s = iterable[i:i + size]
                if not s:
                    break
                yield s
                i += size
    '''
    def counter(x):
        counter.n += 1
        return counter.n//size
    counter.n = -1
    for k, g in groupby(iterable, counter):
        yield g
def GroupByN(seq, n, fill=False):
    '''Return an iterator that gives groups of n items from the
    sequence.  If fill is True, return None for any missing items.  In
    other words, if fill is False, groups without the full number of
    elements are discarded.
 
    Example:
        print("fill = False:")
        for i in GroupByN(range(7), 3, fill=False):
            print("  ", i)
        print("fill = True:")
        for i in GroupByN(range(7), 3, fill=True):
            print("  ", i)
    prints
        fill = False:
           (0, 1, 2)
           (3, 4, 5)
        fill = True:
           (0, 1, 2)
           (3, 4, 5)
           (6, None, None)
    '''
    # Inspired by
    # http://code.activestate.com/recipes/303060-group-a-list-into-sequential-n-tuples/
    if fill:
        return zip_longest(*([iter(seq)]*n), fillvalue=None)
    else:
        return zip(*([iter(seq)]*n))
def Cfg(lines, lvars=OrderedDict(), gvars=OrderedDict()):
    '''Allow use of sequences of text strings to be used for
    general-purpose configuration information.  Each string must be
    valid python code.
 
    Each line in lines is executed with the local variables in lvars
    and global variables in gvars.  The lvars dictionary is returned,
    which will contain each of the defined variables and functions.
 
    Any common leading indentation is removed before processing; this
    allows you to indent your configuration lines as desired.
 
    Example:
        lines = """
                from math import sqrt
                a = 44
                b = "A string"
                def X(a):
                    return a/2
                c = a*sqrt(2)
                d = X(a)
            """[1:-1].split("\n")
 
    The code
        d = Cfg(lines)
        for i in d.keys():
            print(i + " = " + str(d[i]))
 
    results in
        sqrt = <built-in function sqrt>
        a = 44
        b = A string
        X = <function X at 0x00B9C9B0>
        c = 62.2253967444
        d = 22.0
    '''
    # Remove any common indent
    indent = os.path.commonprefix(lines)
    if indent:
        lines = [i.replace(indent, "", 1) for i in lines]
    # Put lines into a temporary file so execfile can be used.  I
    # would have used NamedTemporaryFile(), but it doesn't work
    # correctly on Windows XP, so I used the deprecated mktemp.
    exec(nl.join(lines), gvars, lvars)
    # The things defined in the configuration lines are now in the
    # dictionary lvars.
    return lvars
def ReadVariables(file, ignore_errors=False):
    '''Given a file of lines of python code, this function reads in
    each line and executes it.  If the lines of the file are
    assignments to variables, then this results in a defined variable
    in the local namespace.  Return the dictionary containing these
    variables.
 
    file can be a name of a file, a file-like object, a string, or a
    multiline string.
 
    Note that this function will not execute any line that doesn't
    contain an '=' character to cut down on the chance that some
    unforeseen error can occur (but, of course, this protection can
    rather easily be subverted).
 
    This function is intended to be used to allow you to have an
    easy-to-use configuration file for a program.  For example, a user
    could write the configuration file
 
        # This is a comment
        ProcessMean              = 37.2
        ProcessStandardDeviation = 12.1
        NumberOfParts            = 180
 
    When this function returned, you'd have a dictionary with four
    variables in it.
 
    If any line in the input file causes an exception, the offending
    line will be printed to stderr and the program will exit unless
    ignore_errors is True.
    '''
    try:
        lines = file.readlines()
    except AttributeError:
        try:
            lines = open(file).readlines()
        except FileNotFoundError:
            # Assume it's a multiline string
            lines = file.strip().split("\n")
    for i, line in enumerate(lines):
        if "=" not in line:
            continue
        try:
            exec(line)
        except Exception:
            sys.stderr.write("Line %d of file '%s' bad:\n  '%s'\n" %
                             (i+1, file, line.rstrip()))
            if not ignore_errors:
                exit(1)
    d = locals()
    for i in "line lines i file ignore_errors".split():
        del d[i]
    return d
def randq(seed=-1):
    '''The simple random number generator in the section "An Even
    Quicker Generator" from "Numerical Recipes in C", page 284,
    chapter 7, 2nd ed, 1997 reprinting (found on the web in PDF form).
 
    If seed is not -1, it is used to initialize the sequence; it can
    be any hashable value.
    '''
    # The multiplicative constant 1664525 was recommended by Knuth and
    # the additive constant 1013904223 came from Lewis.
    a, c = 1664525, 1013904223
    if seed != -1:
        randq.idum = abs(hash(seed))
    randq.idum = (randq.a*randq.idum + randq.c) % randq.maxidum
    return randq.idum
if 1:   # State variables for randq
    randq.a = 1664525
    randq.c = 1013904223
    randq.idum = 0
    randq.maxidum = 2**32
def randr(seed=-1):
    '''Uses randq to return a floating point number on [0, 1).
    '''
    n = randq(seed=seed) if seed != -1 else randq()
    return n/float(randq.maxidum)
def IsCygwinSymlink(file):
    '''Return True if file is a cygwin symbolic link.
    '''
    s = open(file).read(20)
    if len(s) > 10:
        if s[2:9] == "symlink":
            return True
    return False
def TranslateSymlink(file):
    '''For a cygwin symlink, return a string of what it's pointing to.
    '''
    return open(file).read()[12:].replace("\x00", "")
def IsTextFile(file, num_bytes=100):
    '''Heuristic to classify a file as text or binary.  The algorithm
    is to read num_bytes from the beginning of the file; if there are
    any characters other than the "typical" ones found in plain text
    files, the file is classified as binary.
 
    This won't work on a file that contains Unicode characters but is
    otherwise plain text.  Here, "text" means plain ASCII.
 
    Note:  if file is a string, it is assumed to be a file name and
    opened.  Otherwise it is assumed to be an open stream.
    '''
    text_chars = set([ord(i) for i in "\n\r\b\t\v"] + list(range(32, 127)))
    if isinstance(file, str):
        s = open(file, "rb").read(num_bytes)
    else:
        s = file.read(num_bytes)
    for c in s:
        if ord(c) not in text_chars:
            return False
    return True
def IsBinaryFile(file, num_bytes=100):
    'Heuristic that returns True if a file is a binary file'
    return not IsTextFile(file, num_bytes)
class Dispatch:
    '''The Dispatch class allows different functions to be called
    depending on the argument types.  Thus, there can be one function
    name regardless of the argument type.  Due to David Ascher.
 
    Example:  the following lets us define a function ss which will
    calculate the sum of squares of the contents of an array, whether
    the array is a python sequence or a NumPy array.
    ss = Dispatch((list_ss, (ListType, TupleType)),
                            (array_ss, (numpy.ArrayType)))
    '''
    def __init__(self, *tuples):
        self._dispatch = {}
        for func, types in tuples:
            for t in types:
                if t in self._dispatch.keys():
                    raise ValueError("Can't have two dispatches on " + str(t))
                self._dispatch[t] = func
        self._types = self._dispatch.keys()
    def __call__(self, arg1, *args, **kw):
        if type(arg1) not in self._types:
            raise TypeError("Don't know how to dispatch %s arguments" %
                            type(arg1))
        return apply(self._dispatch[type(arg1)], (arg1,) + args, kw)
def IsIterable(x, ignore_strings=True):
    '''Return True if x is an iterable.  You can exclude strings from the
    things that can be iterated on if you wish.
 
    Note:  if you don't care whether x is a string or not, a simpler way
    is:
        try:
            iter(x)
            return True
        except TypeError:
            return False
    '''
    if ignore_strings and isinstance(x, str):
        return False
    return isinstance(x, Iterable)
def SpeedOfSound(T):
    '''Returns speed of sound in air in m/s as a function of temperature
    T in K.  Assumes sea level pressure.
    '''
    assert(T > 0)
    return 331.4*math.sqrt(T/273.15)
def WindChillInDegF(wind_speed_in_mph, air_temp_deg_F):
    '''Wind Chill for exposed human skin, expressed as a function of
    wind speed in miles per hour and temperature in degrees Fahrenheit.
 
    http://en.wikipedia.org/wiki/Wind_chill.
    '''
    if wind_speed_in_mph <= 3:
        raise ValueError("Wind speed must be > 3 mph")
    if air_temp_deg_F > 50:
        raise ValueError("Air temperature must be < 50 deg F")
    return (35.74 + 0.6215*air_temp_deg_F - 35.75*wind_speed_in_mph**0.16 +
            0.4275*air_temp_deg_F*wind_speed_in_mph**0.16)
def Height(current_height_inches, age_years, sex):
    '''Returns the predicted adult height in inches of a child.
    Unattributed, but found in the C code files of Glenn Rhoads' old
    website http://remus.rutgers.edu/~rhoads/Code/code.html, but which
    was defunct in 2010.
    '''
    if not (0 < current_height_inches < 72):
        raise ValueError("current_height_inches must be between 0 and 72")
    if not (0 < age_years < 20):
        raise ValueError("age_years must be between 0 and 20")
    if sex.lower() not in "mf":
        raise ValueError("sex must be 'm' or 'f'")
    a, h = age_years, current_height_inches
    if sex.lower() == "m":
        return h/(((0.00011*a - 0.0032)*a + 0.0604)*a + 0.3796)
    else:
        return h/(((0.00028*a - 0.0071)*a + 0.0926)*a + 0.3524)
def HeatIndex(air_temp_deg_F, relative_humidity_percent):
    '''From http://www.weather.gov/forecasts/graphical/sectors/idaho.php#tabs.
    See also http://www.crh.noaa.gov/pub/heat.php.
 
    Heat Index combines the effects of heat and humidity. When heat and
    humidity combine to reduce the amount of evaporation of sweat from the
    body, outdoor exercise becomes dangerous even for those in good shape.
 
    Example:  for 90 deg F and 50% RH, the heat index is 94.6.
 
    The equation used is a multiple regression fit to a complicated set of
    equations that must be solved iteratively.  The uncertainty with a
    prediction is given at 1.3 deg F.  See
    http://www.srh.noaa.gov/ffc/html/studies/ta_htindx.PDF for details.
 
    If heat index is:
 
        80-90 degF:  Caution:  fatigue possible with prolonged exposure or
                     activity.
        90-105:      Extreme caution:  sunstroke, muscle cramps and/or heat
                     exhaustion possible with prolonged exposure and/or
                     physical activity.
        105-129:     Danger:  sunstroke, muscle cramps and/or heat exhaustion
                     likely.  Heatstroke possible with prolonged exposure
                     and/or physical activity.
        >= 130       Extreme danger:  Heat stroke or sunstroke likely.
    '''
    RH, Tf = relative_humidity_percent, air_temp_deg_F
    HI = (-42.379 + 2.04901523*Tf + 10.14333127*RH - 0.22475541*Tf*RH -
          6.83783e-3*Tf*Tf - 5.481717e-2*RH*RH + 1.22874e-3*Tf*Tf*RH +
          8.5282e-4*Tf*RH*RH - 1.99e-6*Tf*Tf*RH*RH)
    return HI
class Debug:
    '''Implements a debug class that can be useful in printing debugging
    information.
 
    dbg = Debug()
    dbg.print("Message")
        Will print '+ Message' to stderr
    Turn off printing with 'dbg.on = False'.
    '''
    def __init__(self, stream=sys.stderr, add_nl=True, prefix="+ "):
        self.stream = stream
        self.on = True
        self.add_nl = add_nl
        self.prefix = prefix
    def print(self, s):
        if self.on:
            s = self.prefix + s
            if self.add_nl:
                s += nl
            self.stream.write(s)
def Time():
    '''Returns the current time in the following format:
        '7Jun2021 7:24 am Mon'
    '''
    t, f = time.localtime(), lambda x: x[1:] if x[0] == "0" else x
    day = f(time.strftime("%a", t))
    date = f(time.strftime("%d%b%Y", t))
    clock = f(time.strftime("%I:%M", t))
    ampm = time.strftime("%p", t).lower()
    return ' '.join((date, clock, ampm, day))
def AWG(n):
    '''Returns the wire diameter in inches given the AWG (American Wire
    Gauge) number (also known as the Brown and Sharpe gauge).  Use negative
    numbers as follows:
 
        00    -1
        000   -2
        0000  -3
 
    Reference:  the units.dat file with version 1.80 of the GNU units
    program gives the following statement:
 
        American Wire Gauge (AWG) or Brown & Sharpe Gauge appears to be the
        most important gauge. ASTM B-258 specifies that this gauge is based
        on geometric interpolation between gauge 0000, which is 0.46 inches
        exactly, and gauge 36 which is 0.005 inches exactly.  Therefore,
        the diameter in inches of a wire is given by the formula
                1|200 92^((36-g)/39).
        Note that 92^(1/39) is close to 2^(1/6), so diameter is
        approximately halved for every 6 gauges.  For the repeated zero
        values, use negative numbers in the formula.  The same document
        also specifies rounding rules which seem to be ignored by makers of
        tables.  Gauges up to 44 are to be specified with up to 4
        significant figures, but no closer than 0.0001 inch.  Gauges from
        44 to 56 are to be rounded to the nearest 0.00001 inch.
 
    An equivalent formula is 0.32487/1.12294049**n where n is the
    gauge number (works for n >= 0).
    '''
    if n < -3 or n > 56:
        raise ValueError("AWG argument out of range")
    diameter = 92.**((36 - n)/39)/200
    if n <= 44:
        return round(diameter, 4)
    return round(diameter, 5)
def SignificantFiguresS(value, digits=3, exp_compress=True):
    '''Returns a string representing the number value rounded to
    a specified number of significant figures.  The number is
    converted to a string, then rounded and returned as a string.
    If you want it back as a number, use float() on the string.
    If exp_compress is true, the exponent has leading zeros
    removed.
 
    The following types of printouts can be gotten using this function
    and native python formats:
 
           A              B               C               D
       3.14e-12       3.14e-012       3.14e-012       3.14e-012
       3.14e-11       3.14e-011       3.14e-011       3.14e-011
       3.14e-10       3.14e-010       3.14e-010       3.14e-010
        3.14e-9       3.14e-009       3.14e-009       3.14e-009
        3.14e-8       3.14e-008       3.14e-008       3.14e-008
        3.14e-7       3.14e-007       3.14e-007       3.14e-007
        3.14e-6       3.14e-006       3.14e-006       3.14e-006
        3.14e-5       3.14e-005       3.14e-005       3.14e-005
        3.14e-4       3.14e-004        0.000314        0.000314
        3.14e-3       3.14e-003         0.00314         0.00314
        3.14e-2       3.14e-002          0.0314          0.0314
        3.14e-1       3.14e-001           0.314           0.314
        3.14e+0       3.14e+000            3.14            3.14
        3.14e+1       3.14e+001            31.4            31.4
        3.14e+2       3.14e+002             314           314.0
        3.14e+3       3.14e+003       3.14e+003          3140.0
        3.14e+4       3.14e+004       3.14e+004         31400.0
        3.14e+5       3.14e+005       3.14e+005        314000.0
        3.14e+6       3.14e+006       3.14e+006       3140000.0
        3.14e+7       3.14e+007       3.14e+007      31400000.0
        3.14e+8       3.14e+008       3.14e+008     314000000.0
        3.14e+9       3.14e+009       3.14e+009    3140000000.0
       3.14e+10       3.14e+010       3.14e+010   31400000000.0
       3.14e+11       3.14e+011       3.14e+011  314000000000.0
       3.14e+12       3.14e+012       3.14e+012       3.14e+012
 
    A:  SignificantFiguresS(x, 3)
    B:  SignificantFiguresS(x, 3, 0)
    C:  "%.3g" % x
    D:  float(SignificantFiguresS(x, 3))
    '''
    if digits < 1 or digits > 15:
        msg = "Number of significant figures must be >= 1 and <= 15"
        raise ValueError(msg)
    sign, significand, exponent = SignSignificandExponent(float(value))
    fmt = "%%.%df" % (digits-1)
    neg = "-" if sign < 0 else ""
    e = "e%+d" % exponent if exp_compress else "e%+04d" % exponent
    return neg + (fmt % significand) + e
def SignificantFigures(value, figures=3):
    '''Rounds a value to specified number of significant figures.
    Returns a float.
    '''
    return float(SignificantFiguresS(value, figures))
def EditData(data, binary=False):
    'Edit a str or bytes object using vim'
    if not isinstance(data, (str, bytes)):
        raise TypeError("data must be a str or bytes object")
    if binary and isinstance(data, str):
        raise TypeError("data must be a bytes object")
    if not binary and isinstance(data, bytes):
        raise TypeError("data must be a str")
    vi = "vim"
    with tempfile.NamedTemporaryFile() as temp:
        file = P(temp.name)
        if binary:
            file.write_bytes(data)
            cmd = [vi, "-b", str(file)]
        else:
            file.write_text(data)
            cmd = [vi, str(file)]
        subprocess.call(cmd)
        if binary:
            data = file.read_bytes()
        else:
            data = file.read_text()
    return data
def Engineering(value, digits=3):
    '''Return a tuple (m, e, s) representing a number in engineering
    notation.  m is the significand.  e is the exponent in the form of
    an integer; it is adjusted to be a multiple of 3.  s is the SI
    symbol for the exponent; for "e+003" it would be "k".  s is empty
    if there is no SI symbol.
 
    Engineering(1.2345678901234567890e-88, 4) --> ('123.5', -90, '')
    Engineering(1.2345678901234567890e-8, 4)  --> ('12.35', -9, 'n')
    Engineering(1.2345678901234567890e8, 4)   --> ('123.5', 6, 'M')
    Examples:
    '''
    suffixes = {
        -8: "y", -7: "z", -6: "a", -5: "f", -4: "p", -3: "n",
        -2: "u", -1: "m", 0: "", 1: "k", 2: "M", 3: "G", 4: "T",
        5: "P", 6: "E", 7: "Z", 8: "Y"}
    if digits < 1 or digits > 15:
        raise ValueError("Number of significant digits must be >= 1 and <= 15")
    sign, significand, exponent = SignSignificandExponent(float(value))
    s = suffixes[exponent//3] if exponent//3 in suffixes else ""
    m = sign*(("%%.%dg" % digits) % (significand*10**(exponent % 3)))
    if m.find("e") != -1:
        # digits = 1 or 2 can cause e.g. 3e+001, so the following
        # eliminates the exponential notation
        m = str(int(float(m)))
    return m, 3*(exponent//3), s
def eng(value, digits=3, unit=None, width=0):
    '''Convenience function for engineering representation.  If unit is
    given, then the number of digits is displayed in value with the
    prefix prepended to unit.  Otherwise, "xey" notation is used, except if
    y == 0, no exponent portion is given.  Returns a string for printing.
    If width is nonzero, then returns a string right-justified to that
    width.
    '''
    m, e, p = Engineering(value, digits)
    if unit:
        s = m + " " + p + unit
    else:
        s = m if e == 0 else "%se%d" % (m, e)
    if width:
        if len(s) < width:
            p = (" " * (width - len(s)))
            s = p + s
    return s
def IdealGas(P=0, v=0, T=0, MW=28.9):
    '''Given two of the three variables P, v, and T, calculates the
    third for the indicated gas.  The variable that is unknown should
    have a value of zero.
        P = pressure in Pa
        v = specific volume in m^3/kg
        T = absolute temperature in K
        MW = molecular weight = molar mass in g/mol (defaults to air)
             Note you can also supply a string; if the lower-case
             version of this string is in the dictionary of gas_molar_mass
             below, the molar mass for that gas will be used.
    The tuple (P, v, T) will be returned.
 
    WARNING:  Note that v is the specific volume, not the volume!
 
    The equation used is P*v = R*T where R is the gas constant for this
    particular gas.  It is the universal gas constant divided by the
    molecular weight of the gas.
 
    The ideal gas law is an approximation, but a good one for high
    temperatures and low pressures.  Here, high and low are relative
    to the critical temperature and pressure of the gas; these can be
    found in numerous handbooks, such as the CRC Handbook of Chemistry
    and Physics, the Smithsonian Critical Tables, etc.
 
    Some molar masses and critical values for common gases are:
 
                    Tc       Pc     MW
        air        133.3   37.69   28.9
        ammonia    405.6  113.14   17.03
        argon      151.0   48.00   39.95
        co2        304.2   73.82   44.0099
        helium       5.2    2.25    4.003
        hydrogen    33.3   12.97    2.01594
        methane    190.6   46.04   16.04298
        nitrogen   126.1   33.94   28.0134
        oxygen     154.6   50.43   31.9988
        propane    369.8   42.49   26.03814
        water      647.3  221.2    18.01534
        xenon      289.8   58.00  131.30
 
    Tc is the critical temperature in K, Pc is the critical pressure
    in bar (multiply by 1e5 to get Pa), and MW is the molecular
    weight in daltons (1 Da = 1 g/mol).
    '''
    gas_molar_mass = {
        "air"      : 28.9,
        "ammonia"  : 17.03,
        "argon"    : 39.95,
        "co2"      : 44.0099,
        "helium"   : 4.003,
        "hydrogen" : 2.01594,
        "methane"  : 16.04298,
        "nitrogen" : 28.0134,
        "oxygen"   : 31.9988,
        "propane"  : 26.03814,
        "water"    : 18.01534,
        "xenon"    : 131.30,
    }
    if isinstance(MW, str):
        MW = gas_molar_mass[MW.lower()]
    else:
        assert(P >= 0 and v >= 0 and T >= 0 and MW >= 0)
    molar_gas_constant = 8.3145         # J/(mol*K)
    R = molar_gas_constant/(float(MW)/1000)   # 1000 converts g to kg
    if sum([i == 0 for i in (P, v, T)]) != 1:
        raise ValueError("One and only one of P, v, T must be zero")
    if not P:
        return R*T/v
    elif not v:
        return R*T/P
    else:
        return P*v/R
def Flatten(L, max_depth=None, ltypes=(list, tuple)):
    ''' Flatten every sequence in L whose type is contained in
    "ltypes" to "max_depth" levels down the tree.  The sequence
    returned has the same type as the input sequence.
 
    Written by Kevin L. Sitze on 2010-11-25.  From
    http://code.activestate.com/recipes/577470-fast-flatten-with-depth-control-and-oversight-over/?in=lang-python
    This code may be used pursuant to the MIT License.
 
    Note:  itertools has a flatten() recipe that flattens one level:
 
        def flatten(listOfLists):
            'Flatten one level of nesting'
            return chain.from_iterable(listOfLists)
 
    but every element encountered needs to be an iterable.  This
    Flatten() function works more generally.
    '''
    if max_depth is None:
        make_flat = lambda x: True
    else:
        make_flat = lambda x: max_depth > len(x)
    if callable(ltypes):
        is_sequence = ltypes
    else:
        is_sequence = lambda x: isinstance(x, ltypes)
    r, s = [], []
    s.append((0, L))
    while s:
        i, L = s.pop()
        while i < len(L):
            while is_sequence(L[i]):
                if not L[i]:
                    break
                elif make_flat(s):
                    s.append((i + 1, L))
                    L = L[i]
                    i = 0
                else:
                    r.append(L[i])
                    break
            else:
                r.append(L[i])
            i += 1
    try:
        return type(L)(r)
    except TypeError:
        return r
def TempConvert(t, in_unit, to_unit):
    '''Convert the temperature in t in the unit specified in in_unit to the
    unit specified by to_unit.
    '''
    allowed, k, r, a, b = "cfkr", 273.15, 459.67, 1.8, 32
    def check(unit, orig):
        if len(unit) != 1 and unit not in allowed:
            raise ValueError("'%s' is a bad temperature unit" % orig)
    inu, tou = [i.lower() for i in (in_unit, to_unit)]
    check(inu, in_unit)
    check(tou, to_unit)
    if inu == tou:
        return t
    d = {
        "cf" : lambda t: a*t + b,
        "ck" : lambda t: t + k,
        "cr" : lambda t: a*(t + k),
        "fc" : lambda t: (t - b)/a,
        "fk" : lambda t: (t - b)/a + k,
        "fr" : lambda t: t + r,
        "kc" : lambda t: t - k,
        "kf" : lambda t: a*(t - k) + b,
        "kr" : lambda t: a*t,
        "rc" : lambda t: (t - r - b)/a,
        "rf" : lambda t: t - r,
        "rk" : lambda t: t/a,
    }
    T = d[inu + tou](t)
    e = ValueError("Converted temperature is too low")
    if ((tou in "kr" and T < 0) or (tou == "c" and T < -k) or
            (tou == "f" and T < -r)):
        raise e
    return T
def ConvertToNumber(s, handle_i=True):
    '''This is a general-purpose routine that will return a python number
    for a string if it is possible.  The basic logic is:
        * If it contains 'j' or 'J', it's complex
        * If it contains '/', it's a fraction
        * If it contains ',', '.', 'E', or 'e', it's a float
        * Otherwise it's interpreted to be an integer
    Since I prefer to use 'i' for complex numbers, we'll also allow an 'i'
    in the number unless handle_i is False.
    '''
    s = s.lower()
    if handle_i:
        s = s.replace("i", "j")
    if 'j' in s:
        return complex(s)
    elif '.' in s or 'e' in s or ',' in s:
        return float(s)
    elif '/' in s:
        return Fraction(s)
    else:
        return int(s)
def StringToNumbers(s, sep=" ", handle_i=True):
    '''s is a string; return the sequence (tuple) of numbers it
    represents; number strings are separated by the string sep.  The
    numbers returned are integers, fractions, floats, or complex.  If
    handle_i is True, 'i' or 'I' are allowed as the imaginary unit.
    '''
    seq = []
    for line in s.strip().split(nl):
        if sep is None:
            seq.extend(line.split(sep))
        else:
            seq.extend(line.split())
    return tuple([ConvertToNumber(i, handle_i=handle_i) for i in seq])
def hyphen_range(s, sorted=False, unique=False):
    '''Takes a set of range specifications of the form "a-b" and returns a
    list of integers between a and b inclusive.  Also accepts comma
    separated ranges like "a-b,c-d,f".  Numbers from a to b, a to d and f.
    If sorted is True, the returned list will be sorted.  If unique is
    True, only unique numbers are kept and the list is automatically
    sorted.  In "a-b", a can be larger than b, in which case the
    sequence will decrease until b is reached.
 
    Adapted from routine at
    http://code.activestate.com/recipes/577279-generate-list-of-numbers-from-hyphenated-and-comma/?in=lang-python
    '''
    s = "".join(s.split())    # Removes white space
    r = []
    for x in s.split(','):
        t = [int(i) for i in x.split('-')]
        if len(t) not in (1, 2):
            raise ValueError("'%s' is bad range specifier" % s)
        if len(t) == 1:
            r.append(t[0])
        else:
            if t[0] < t[1]:
                r.extend(range(t[0], t[1] + 1))
            else:
                r.extend(range(t[0], t[1] - 1, -1))
    if sorted:
        r.sort()
    elif unique:
        r = list(set(r))
        r.sort()
    return r
def grouper(data, mapper, reducer=None):
    '''Simple map/reduce for data analysis.
 
    Each data element is passed to a *mapper* function.
    The mapper returns key/value pairs
    or None for data elements to be skipped.
 
    Returns a dict with the data grouped into lists.
    If a *reducer* is specified, it aggregates each list.
 
    >>> def even_odd(elem):                     # sample mapper
    ...     if 10 <= elem <= 20:                # skip elems outside the range
    ...         key = elem % 2                  # group into evens and odds
    ...         return key, elem
 
    >>> grouper(range(30), even_odd)         # show group members
    {0: [10, 12, 14, 16, 18, 20], 1: [11, 13, 15, 17, 19]}
 
    >>> grouper(range(30), even_odd, sum)    # sum each group
    {0: 90, 1: 75}
 
    Note:  from
    http://code.activestate.com/recipes/577676-dirt-simple-mapreduce/?in=lang-python
    I renamed the function to grouper.
    '''
    d = {}
    for elem in data:
        r = mapper(elem)
        if r is not None:
            key, value = r
            if key in d:
                d[key].append(value)
            else:
                d[key] = [value]
    if reducer is not None:
        for key, group in d.items():
            d[key] = reducer(group)
    return d
if 0:
    class Walker(object):
        '''Defines a class that operates as a generator for recursively getting
        files or directories from a starting directory.  The default is to
        return files; if you want directories, set the dir attribute to True.
        The ignore option to the constructor defines directories to ignore.
    
        An example of use to show all the files in the current directory tree:
    
            w = Walker()
            for i in w("."):
                print(i)
        
        Note:  the functionality here is obsolete because
        pathlib.glob("**/*") can do these things.
        '''
        def __init__(self, ignore=".bzr .git .hg .rcs __pycache__".split(),
                    dir=False):
            self.dir = dir
            self._ignore = ignore
            print(f"{C.lyel}{sys.argv[0]}:  Warning:  Walker is deprecated; use "
                f"e.g. pathlib.Path.glob('**/*'){C.norm}")
        def __str__(self):
            return "util.Walker(ignore={}, dir={})".format(self._ignore, self.dir)
        def __repr__(self):
            return str(self)
        def _ignore_this(self, dir):
            for i in dir.split("/"):
                if i in self._ignore:
                    return True
            return False
        def __call__(self, location):
            '''Walk the directory tree starting at location.  This is a
            generator that returns each file or directory found.
            '''
            if not os.path.isdir(location):
                raise ValueError("location must be a directory")
            for root, dirs, files in os.walk(location):
                if self._ignore_this(root):
                    continue
                if self.dir:
                    for dir in dirs:
                        if self._ignore_this(dir):
                            continue
                        p = os.path.join(root, dir)
                        if os.path.isdir(p):
                            yield p
                else:
                    for file in files:
                        p = os.path.join(root, file)
                        if os.path.isfile(p):
                            yield p
def IsConvexPolygon(*p):
    '''Return True if the sequence p of two-dimensional points
    constitutes a convex polygon.  Ref:
    http://stackoverflow.com/questions/471962/how-do-determine-if-a-polygon-is-complex-convex-nonconvex#
 
    The assumption is that the sequence p of points traverses consecutive
    points of the polygon.
 
    The algorithm is to look at the triples of points and calculate the
    sign of the z component of their cross product.  The polygon is
    convex if the signs are either all negative or all positive.
 
    Examples:
        ((0, 0), (1, 0), (1, 1), (1, 0)) will return True.
        ((0, 0), (1, 0), (1, 1), (0.5,         0.5)) will return False.
        ((0, 0), (1, 0), (1, 1), (0.5 - 1e-10, 0.5)) will return True.
    '''
    n = len(p)
    if n < 3:
        raise ValueError("Need at least three points")
    cross_product_signs = []
    for index in range(n + 3):
        # Generate indices of the needed points
        i = index % n
        j = (index + 1) % n
        k = (index + 2) % n
        p1, p2, p3 = p[i], p[j], p[k]
        dx1 = p2[0] - p1[0]
        dy1 = p2[1] - p1[1]
        dx2 = p3[0] - p2[0]
        dy2 = p3[1] - p2[1]
        cross_product_signs.append(signum(dx1*dy2 - dy1*dx2))
    assert(len(cross_product_signs) == n + 3)
    if cross_product_signs[0] and len(set(cross_product_signs)) == 1:
        return True
    return False
def BraceExpansion(s, glob=False):
    '''Generator to perform brace expansion on the string s.  If glob
    is True, then also glob each pattern in the current directory.
    Examples:
    
    * BraceExpansion("a.{a, b}")) returns 
        ['a.a', 'a. b'].
    * BraceExpansion("pictures/*.{jpg, png}")) returns a list of
        all the JPG and PNG files in the pictures directory under the
        current directory.
    * BraceExpansion("{a,b}/*.{jpg,png}") returns
        ['a/*.jpg', 'a/*.png', ' b/*.jpg', ' b/*.png']
    * BraceExpansion("{,a}/{c,d}") returns
        ['/c', '/d', 'a/c', 'a/d']
    * BraceExpansion(r"{,,a}/{c,d}") returns
        ['/c', '/d', '/c', '/d', 'a/c', 'a/d']
    '''
    # Algorithm from http://rosettacode.org/wiki/Brace_expansion#Python
    # The web page's content is available under the GNU Free
    # Documentation license 1.2.
    def getitem(s, depth=0):
        out = [""]
        while s:
            c = s[0]
            if depth and (c == ',' or c == '}'):
                return out, s
            if c == '{':
                x = getgroup(s[1:], depth+1)
                if x:
                    out, s = [a+b for a in out for b in x[0]], x[1]
                    continue
            if c == '\\' and len(s) > 1:
                s, c = s[1:], c + s[1]
            out, s = [a + c for a in out], s[1:]
        return out, s
    def getgroup(s, depth):
        out, comma = [], False
        while s:
            g, s = getitem(s, depth)
            if not s:
                break
            out += g
            if s[0] == '}':
                if comma:
                    return out, s[1:]
                return ['{' + a + '}' for a in out], s[1:]
            if s[0] == ',':
                comma, s = True, s[1:]
        return None
    if glob:
        for i in getitem(s)[0]:
            for j in glob.glob(i):
                yield j
    else:
        for i in getitem(s)[0]:
            yield i
def Spinner(chars=r"-\|/-\|/", delay=0.1):
    '''Show a spinner to indicate that processing is still taking place.
    Set Spinner.stop to True to cause it to exit.  Note this is not
    thread-safe.
 
    Here's some example code that demonstrates how it could be used:
 
        from threading import Thread
        def T():
            Spinner()
            if Spinner.stop:
                return
        t = Thread(target=T)
        t.start()
        time.sleep(2)
        Spinner.stop = True
    '''
    # Idea from https://realpython.com/python-print/#living-it-up-with-cool-animations
    for frame in cycle(chars):
        print('\r', frame, sep='', end='', flush=True)
        time.sleep(delay)
        if Spinner.stop:
            print()
            return
Spinner.stop = False
def ProgressBar(frac=0, width=40, char="#"):
    '''Prints a progress bar to stdout.  frac must be a number on the
    closed interval [0, 1].
 
    Here's an example of use:
        n = 100
        for i in range(n + 1):
            ProgressBar(i/n)
            time.sleep(0.01)
        print()
    '''
    # Idea from https://realpython.com/python-print/#living-it-up-with-cool-animations
    assert(len(char) == 1)
    left = int(width*frac)
    right = width - left
    percent = int(100*frac)
    print("\r[", char*left, " "*right, "]", " {}%".format(percent),
          sep="", end="", flush=True)
def Paste(*seq, missing="", sep="\t"):
    '''Return a list whose elements are each corresponding element of the
    sequences in *seq, separated by the string sep.  If a sequence is too
    short, the missing string will be substituted.  All sequence elements
    will be converted to strings using str().
 
    Example:
        Paste([1, 2, "a"], ["3 4", 5], missing="X")
    will return
        ['1\t3 4', '2\t5', 'a\tX']
    '''
    result = list(zip_longest(*seq, fillvalue=missing))
    for i, item in enumerate(result):   # Convert all elements to strings
        result[i] = [str(j) for j in result[i]]
    return [sep.join(i) for i in result]
def EBCDIC():
    '''Returns two byte-translation tables to use with
    bytes.translate().  The first converts ASCII bytes to EBCDIC and the
    second converts EBCDIC bytes to ASCII.
    '''
    a2e = [
        0, 1, 2, 3, 55, 45, 46, 47, 22, 5, 37, 11, 12, 13, 14, 15, 16,
        17, 18, 19, 60, 61, 50, 38, 24, 25, 63, 39, 28, 29, 30, 31, 64,
        79,127,123, 91,108, 80,125, 77, 93, 92, 78,107, 96, 75, 97,
        240,241,242,243,244,245,246,247,248,249,122, 94, 76,126,110,111,
        124,193,194,195,196,197,198,199,200,201,209,210,211,212,213,214,
        215,216,217,226,227,228,229,230,231,232,233, 74,224, 90, 95,109,
        121,129,130,131,132,133,134,135,136,137,145,146,147,148,149,150,
        151,152,153,162,163,164,165,166,167,168,169,192,106,208,161, 7,
        32, 33, 34, 35, 36, 21, 6, 23, 40, 41, 42, 43, 44, 9, 10, 27,
        48, 49, 26, 51, 52, 53, 54, 8, 56, 57, 58, 59, 4, 20, 62,225,
        65, 66, 67, 68, 69, 70, 71, 72, 73, 81, 82, 83, 84, 85, 86, 87,
        88, 89, 98, 99,100,101,102,103,104,105,112,113,114,115,116,117,
        118,119,120,128,138,139,140,141,142,143,144,154,155,156,157,158,
        159,160,170,171,172,173,174,175,176,177,178,179,180,181,182,183,
        184,185,186,187,188,189,190,191,202,203,204,205,206,207,218,219,
        220,221,222,223,234,235,236,237,238,239,250,251,252,253,254,255
    ]
    e2a = [
        0, 1, 2, 3,156, 9,134,127,151,141,142, 11, 12, 13, 14, 15, 16,
        17, 18, 19,157,133, 8,135, 24, 25,146,143, 28, 29, 30, 31,
        128,129,130,131,132, 10, 23, 27,136,137,138,139,140, 5, 6, 7,
        144,145, 22,147,148,149,150, 4,152,153,154,155, 20, 21,158, 26,
        32,160,161,162,163,164,165,166,167,168, 91, 46, 60, 40, 43, 33,
        38,169,170,171,172,173,174,175,176,177, 93, 36, 42, 41, 59, 94,
        45, 47,178,179,180,181,182,183,184,185,124, 44, 37, 95, 62, 63,
        186,187,188,189,190,191,192,193,194, 96, 58, 35, 64, 39, 61, 34,
        195, 97, 98, 99,100,101,102,103,104,105,196,197,198,199,200,201,
        202,106,107,108,109,110,111,112,113,114,203,204,205,206,207,208,
        209,126,115,116,117,118,119,120,121,122,210,211,212,213,214,215,
        216,217,218,219,220,221,222,223,224,225,226,227,228,229,230,231,
        123, 65, 66, 67, 68, 69, 70, 71, 72, 73,232,233,234,235,236,237,
        125, 74, 75, 76, 77, 78, 79, 80, 81, 82,238,239,240,241,242,243,
        92,159, 83, 84, 85, 86, 87, 88, 89, 90,244,245,246,247,248,249,
        48, 49, 50, 51, 52, 53, 54, 55, 56, 57,250,251,252,253,254,255
    ]
    s, t = bytearray(a2e), bytearray(e2a)
    return s.maketrans(s, t), s.maketrans(t, s)
def Ampacity(dia_mm, insul_degC=60, ambient_degC=30):
    '''Return the NEC-allowed current in a copper conductor at the
    indicated ambient temperature and with the indicated insulation
    temperature rating.  
 
    The data from table 310-16 in the 1998 NEC was fitted to cubic
    polynomials, so the table data won't be reproduced exactly.  Thus,
    the intended use is to estimate safe currents for a given wire size,
    particularly smaller wires than are in the table.  To get the
    ampacity of a smaller wire, the constant term of the regression was
    set to zero.
 
    The data and regressions are in /elec/projects/current_capacity.
    '''
    def AmbientCorrection(ambient_degC, insul_degC):
        if insul_degC not in (60, 75, 90):
            raise ValueError("insul_degC must be 60, 75, or 90 °C")
        if insul_degC == 60:
            i = 0
        elif insul_degC == 75:
            i = 1
        elif insul_degC == 90:
            i = 2
        T = int(ambient_degC)
        if not (21 <= T <= 80):
            raise ValueError("ambient_degC must be between 21 and 80 °C")
        if 21 <= T <= 25:
            return (1.08, 1.05, 1.04)[i]
        elif 26 <= T <= 30:
            return 1
        elif 31 <= T <= 35:
            return (0.91, 0.94, 0.96)[i]
        elif 36 <= T <= 40:
            return (0.82, 0.88, 0.91)[i]
        elif 41 <= T <= 45:
            return (0.71, 0.82, 0.87)[i]
        elif 46 <= T <= 50:
            return (0.58, 0.75, 0.82)[i]
        elif 51 <= T <= 55:
            return (0.41, 0.67, 0.76)[i]
        elif 56 <= T <= 60:
            return (0, 0.58, 0.71)[i]
        elif 61 <= T <= 70:
            return (0, 0.33, 0.58)[i]
        elif 71 <= T <= 80:
            return (0, 0, 0.41)[i]
    max_dia_mm = 11.68
    if not (0 < dia_mm <= max_dia_mm):
        raise ValueError("dia_mm must be in (0, 11.68 mm]")
    if insul_degC not in (60, 75, 90):
        raise ValueError("insul_degC must be 60, 75, or 90 °C")
    constants = {
        60: (10.6841, 0.667284, -0.014032),
        75: (11.0919, 1.25111, -0.0445333),
        90: (12.9412, 1.30463, -0.0441503),
    }
    b1, b2, b3 = constants[insul_degC]
    correction = AmbientCorrection(ambient_degC, insul_degC)
    if correction:
        return correction*(b1*dia_mm + b2*dia_mm**2 + b3*dia_mm**3)
    else:
        raise ValueError("ambient_degC out of range")
def RandomIntegers(n, maxint, seed=None, duplicates_OK=False):
    '''Return a random list of n integers between 0 and maxint - 1.  Set
    seed to be not None to generate a repeatable set of integers.  If
    duplicates_OK is False, the integers are distinct; otherwise, the list
    may contain duplicates.
    '''
    # Check parameters
    if not isinstance(n, int) or not isinstance(maxint, int):
        raise TypeError("n and maxint must be integers")
    if n <= 0:
        raise ValueError("n must be > 0")
    if not maxint and duplicates_OK:
        return [0]*n
    if not duplicates_OK and n > maxint:
        m = f"maxint ({maxint}) is too small to generate {n} distinct integers"
        raise ValueError("maxint is too small to generate n distinct integers")
    #
    s = [] if duplicates_OK else set()
    f = s.append if duplicates_OK else s.add
    numbytes = maxint.bit_length()//8 + 1
    if seed is not None:
        random.seed(seed)
    while len(s) < n:
        if seed is None:
            f(int.from_bytes(os.urandom(numbytes), "big") % maxint)
        else:
            f(random.randint(0, maxint - 1))
    return list(s)
def execfile(filename, globals=None, locals=None, use_user_env=True):
    '''Python 3 substitute for python 2's execfile.  It gets the locals
    and globals from the caller's environment unless use_user_env is
    False.
    '''
    # https://stackoverflow.com/questions/436198/what-is-an-alternative-
    #    to-execfile-in-python-3
    e = sys._getframe(1)
    if globals is None and use_user_env:
        globals = e.f_globals
    if locals is None and use_user_env:
        locals = e.f_locals
    with open(filename, "r") as fh:
        s = fh.read() + "\n"
        exec(s, globals, locals)
def iDistribute(n, a, b):
    '''Generator to return an integer sequence [a, ..., b] with n elements
    equally distributed between a and b.  Raises ValueError if no solution
    is possible.
 
    If you need a sequence of n floating point values, see
    util.fDistribute().
    '''
    if not (ii(a, int) and ii(b, int) and ii(n, int)):
        raise TypeError("Arguments must be integers")
    if a >= b:
        raise ValueError("Must have a < b")
    if n < 2:
        raise ValueError("n must be >= 2")
    if n == 2:
        yield a
        yield b
        return
    dx = Fraction(b - a, n - 1)
    if dx < 1:
        raise ValueError("No solution")
    for i in range(n):
        yield int(round(a + i*dx, 0))
def fDistribute(n, a=0, b=1, impl=f.flt):
    '''Generator to return n impl instances on [a, b] inclusive. A
    common use case is an interpolation parameter on [0, 1].
    Examples:
        fd = fDistribute
        fd(3) --> [0.0, 0.5, 1.0]
        fd(3, 1, 2) --> [1.0, 1.5, 2.0]
        fd(4, 1, 2, Fraction) --> [Fraction(1, 1), Fraction(4, 3),
                                    Fraction(5, 3), Fraction(2, 1)]
    You can use other impl types like decimal.Decimal.  Other types that
    define impl()/impl() to return an impl-type floating point number will
    also work (e.g., mpmath's mpf type).
 
    If you need a sequence of evenly-distributed integers, see
    util.iDistribute().
    '''
    # Check arguments
    msg = "n must be an integer > 1"
    if not ii(n, int):
        raise TypeError(msg)
    if n < 2:
        raise ValueError(msg)
    if not ii(a, (int, impl)) or not ii(b, (int, impl)):
        raise TypeError("a and b must be either an integer or impl")
    if not (a < b):
        raise ValueError("Must have a < b")
    x0 = impl(a)
    dx = impl(b) - x0
    for i in range(n):
        x = x0 + (impl(i)/impl(n - 1))*dx
        # Check invariants
        assert(a <= x <= b)
        assert(ii(x, impl))
        # Return value
        yield x
def signum(x):
    try:
        if x < 0:
            return -1
        elif x > 0:
            return 1
        return 0
    except Exception:
        raise TypeError(f"x = '{x}' not a suitable numerical type")
def SizeOf(o, handlers={}, verbose=False, full=False, title=None):
    '''Returns a string containing the approximate memory in bytes used by
    an object.  Recursively uses sys.getsizeof().
 
    verbose     If True, show the details on each object.
    full        If True, use repr() instead of reprlib.repr()
    title       String for first line in verbose report
    handlers    dict(Class: Handler)
        Example handler for class:
            def Iter(s):
                return s.attr1, s.attr2
            handler = {MyClass: Iter}
    '''
    # DP 11 Apr 2022
    # This is a modified version of
    # https://code.activestate.com/recipes/577504/.  Changes:
    #  - The ability to make verbose a stream
    #  - Indented the verbose output to see the recursion
    #  - Added the full and title keywords
    #  - Used deque to collect output
    dict_handler = lambda d: chain.from_iterable(d.items())
    all_handlers = { 
        tuple: iter,
        list: iter,
        deque: iter,
        dict: dict_handler,
        set: iter,
        frozenset: iter,
    }
    all_handlers.update(handlers)     # User handlers take precedence
    seen = set()                      # Track objects seen
    default_size = sys.getsizeof(0)   # Estimate size without __sizeof__
    Repr_local = repr if full else Repr
    indent, output = 0, deque()
    if verbose:
        output.append(title) if title else output.append("Components:")
    def sizeof(o):
        nonlocal indent
        indent += 2
        if id(o) in seen:       # do not double count the same object
            return 0
        seen.add(id(o))
        sz = sys.getsizeof(o, default_size)
        if verbose:
            i = " "*(indent - 1)
            output.append(' '.join((i, str(sz), str(type(o)), Repr_local(o))))
        for typ, handler in all_handlers.items():
            if isinstance(o, typ):
                sz += sum(map(sizeof, handler(o)))
                break
        indent -= 2
        return sz
    total = sizeof(o)
    if verbose:
        s = output.popleft()
        s = f"{total} {s}"
        output.appendleft(s)
        return '\n'.join(output)
    else:
        return total
class PPSeq:
    'Format sequences for pretty printing'
    def __init__(self, bits_per_number=8):
        self._bpn = bits_per_number
    def __call__(self, seq, **kw):
        'Return a pretty string form of seq'
        # Get keyword arguments
        exp = kw.get("exp", False)              # Show bits exponent
        brackets = kw.get("brackets", True)     # Enclose in brackets
        comma = kw.get("comma", True)           # Separate with commas
        sep = kw.get("sep", " ")                # Element separation string
        # Get the container type and decorators
        if ii(seq, tuple):
            l, r = "(", ")"
        elif ii(seq, list):
            l, r = "[", "]"
        elif ii(seq, set):
            l, r = "{", "}"
        elif ii(seq, deque):
            l, r = "<", ">"
        elif ii(seq, bytes):
            l, r = "«", "»"
        else:
            raise TypeError("Unsupported container type")
        x = self.get_element(seq)
        # Must be an iterable
        if not IsIterable(seq):
            raise TypeError("seq isn't an iterable")
        # Must contain a supported type
        if not self.is_monotype(seq):
            raise TypeError("seq doesn't contain only one numerical type")
        # Get strings
        if ii(x, int):
            myseq = [self.format(i) for i in seq]
        else:
            myseq = [self.format(float(i)) for i in seq]
        s = "," if comma else ""
        s += sep
        t = s.join(myseq)
        if brackets:
            t = f"{l}{t}{r}"
            if exp:
                u = "⁰¹²³⁴⁵⁶⁷⁸⁹"
                t += ''.join(u[int(i)] for i in str(self._bpn))
        return t
    def get_element(self, seq):
        if ii(seq, tuple):
            return seq[0]
        elif ii(seq, list):
            l, r = "[", "]"
            return seq[0]
        elif ii(seq, set):
            l, r = "{", "}"
            x = seq.pop()
            seq.add(x)
            return x
        elif ii(seq, deque):
            l, r = "<", ">"
            x = seq.pop()
            seq.append(x)
            return x
        elif ii(seq, bytes):
            l, r = "«", "»"
            return seq[0]
    def format(self, x):
        'Return the string form of number x (float or int)'
        if ii(x, int):
            w = len(str((2**self._bpn - 1)))
            return f"{x:{w}d}"
        else:
            assert(0 <= x <= 1)
            # Get the number of decimal places to display this float
            w = math.ceil(-math.log10(1/(2**self._bpc - 1)))
            return f"{x:{w + 2}.{w}f}"
    def is_monotype(self, seq):
        'Return True if seq contains only one supported type'
        x = self.get_element(seq)
        # Check the type of each element
        typ = type(x)
        if not all(type(i) == typ for i in seq):
            return False
        # Make sure they are of the allowed types
        if not ii(x, (int, float, f.flt, Decimal, Fraction)):
            try:
                y = float(x)
            except Exception:
                return False
        return True
class Now:
    'Use time(), date(), cdate() methods'
    def __init__(self):
        self._t = t= time.localtime()
        dy = self._rmz(time.strftime("%d", t))
        mo = time.strftime("%b", t)
        yr = time.strftime("%Y", t)
        self._dt = dy, mo, yr
    def _rmz(self, s):
        if s[0] == "0":
            return s[1:]
        return s
    def time(self):
        t = self._t
        hr = self._rmz(time.strftime("%I", t))
        min = time.strftime("%M", t)
        ampm = time.strftime("%p", t).lower()
        return f"{hr}:{min}{ampm}"
    def date(self):
        dy, mo, yr = self._dt 
        return f"{dy} {mo} {yr}"
    def cdate(self):
        dy, mo, yr = self._dt 
        return f"{dy}{mo}{yr}"

if __name__ == "__main__": 
    # Missing tests for: Ignore Debug, Dispatch, GetString
    from io import StringIO
    from lwtest import run, assert_equal, raises, Assert
    from random import seed
    from wrap import dedent
    import itertools
    import math
    import sys
    from itertools import zip_longest
    from pdb import set_trace as xx
    seed(2**64)  # Make test sequences repeatable
    show_coverage = len(sys.argv) > 1
    def Test_PPSeq():
        pp = PPSeq()
        x = (44, 128, 250)
        Assert(pp(tuple(x)) == "( 44, 128, 250)")
        Assert(pp(tuple(x), exp=True) == "( 44, 128, 250)⁸")
        Assert(pp(list(x)) == "[ 44, 128, 250]")
        Assert(pp(set(x)) == "{128, 250,  44}")
        Assert(pp(deque(x)) == "< 44, 128, 250>")
        Assert(pp(bytes(x)) == "« 44, 128, 250»")
    def Test_SizeOf():
        for typ, sz in (
                # These numbers could likely be python version specific
                (tuple, 40),
                (list, 60),
                (deque, 328),
                (set, 124),
                (frozenset, 124),
                ):
            x = typ((0,))
            Assert(SizeOf(x) == sz)
        x = {1:1}
        Assert(SizeOf(x) == 146)
    def Test_AlmostEqual():
        Assert(AlmostEqual(0, 0))
        Assert(AlmostEqual(0, 1e-353))
        Assert(AlmostEqual(1.0, 1.0))
        Assert(AlmostEqual(1, 1 + 2e-15))
        Assert(not AlmostEqual(1, 1 + 2.11e-15))
        Assert(AlmostEqual(1.0, 1.001, 1e-2))
        Assert(not AlmostEqual(1.0, 1.011, 1e-2))
    def Test_SpeedOfSound():
        Assert(AlmostEqual(SpeedOfSound(273.15), 331.4, 1e-5))
    def Test_WindChillInDegF():
        Assert(AlmostEqual(WindChillInDegF(20, 0), -21.9952, 1e-5))
    def Test_HeatIndex():
        Assert(AlmostEqual(HeatIndex(40, 96), 101, 7e-2))
        Assert(AlmostEqual(HeatIndex(100, 90), 132, 4e-1))
    def Test_AWG():
        Assert(AlmostEqual(AWG(12), 0.0808, 8e-4))
    def Test_SignificantFigures():
        Assert(AlmostEqual(float(SignificantFiguresS(1.2345e-6)), 1.23e-6))
        Assert(AlmostEqual(SignificantFigures(1.2345e-6), 1.23e-6))
    def Test_Engineering():
        m, e, s = Engineering(1.2345e-6)
        Assert(float(m) == 1.23 and e == -6 and s == "u")
        m, e, s = Engineering(1.2345e-7)
        Assert(float(m) == 123 and e == -9 and s == "n")
        m, e, s = Engineering(1.2345e-8)
        Assert(float(m) == 12.3 and e == -9 and s == "n")
    def Test_IdealGas():
        P, v, T = 0.101325e6, 0, 300
        v = IdealGas(P, v, T)
        Assert(AlmostEqual(v, 0.85181, 1e-5))
        P = 0
        P = IdealGas(P, v, T)
        Assert(AlmostEqual(P, 0.101325e6))
        T = 0
        T = IdealGas(P, v, T)
        Assert(AlmostEqual(T, 300))
    def Test_ConvertToNumber():
        Assert(ConvertToNumber("1+i") == 1+1j)
        Assert(ConvertToNumber("1+j") == 1+1j)
        Assert(ConvertToNumber("j") == 1j)
        Assert(ConvertToNumber("1.") == 1)
        Assert(ConvertToNumber("1e2") == 1e2)
        Assert(ConvertToNumber("1E2") == 1E2)
        Assert(ConvertToNumber("1/2") == Fraction(1, 2))
        Assert(ConvertToNumber("1") == 1)
        n = 10**50  # Large integer
        Assert(ConvertToNumber(str(n)) == n)
    def Test_Flatten():
        Assert(list(Flatten([])) == [])
        r = list(range(11))
        Assert(list(Flatten(r)) == r)
        a = [0, (1, 2, (3, 4, (5, 6, 7))), (8, (9, 10))]
        Assert(list(Flatten(a)) == r)
    def Test_eng():
        Assert(eng(3456.78) == "3.46e3")
        Assert(eng(3456.78, digits=4) == "3.457e3")
        # kkg is a illegal SI unit, but the code allows it
        Assert(eng(3456.78, unit="kg") == "3.46 kkg")
    def Test_IsIterable():
        Assert(IsIterable("", ignore_strings=False))
        Assert(not IsIterable("", ignore_strings=True))
        Assert(IsIterable([]) and IsIterable(()) )
        Assert(IsIterable({}) and IsIterable(set()))
        Assert(not IsIterable(3))
        Assert(not IsIterable("a"))
        Assert(IsIterable([]))
        Assert(IsIterable((0,)))
        Assert(IsIterable(iter((0,))))
        Assert(not IsIterable(0))
    def Test_hyphen_range():
        s, h = "77", hyphen_range
        Assert(h(s) == [77])
        s = "8-12,14,18"
        Assert(h(s) == [8, 9, 10, 11, 12, 14, 18])
        s = "8 - 12, 14, 18"
        L1 = h(s)
        Assert(L1 == [8, 9, 10, 11, 12, 14, 18])
        s = "12-8,14,18,18"
        L = h(s)
        Assert(L == [12, 11, 10, 9, 8, 14, 18, 18])
        L = h(s, sorted=True)
        Assert(L == L1 + [18])
        L = h(s, unique=True)
        Assert(L == L1)
    def Test_TempConvert():
        k, r = 273.15, 459.67
        Assert(AlmostEqual(TempConvert(0, "c", "f"), 32))
        Assert(AlmostEqual(TempConvert(0, "c", "k"), k))
        Assert(AlmostEqual(TempConvert(0, "c", "r"), 32 + r))
        Assert(AlmostEqual(TempConvert(0, "c", "c"), 0))
        Assert(AlmostEqual(TempConvert(212, "f", "c"), 100))
        Assert(AlmostEqual(TempConvert(212, "f", "f"), 212))
        Assert(AlmostEqual(TempConvert(212, "f", "k"), k + 100))
        Assert(AlmostEqual(TempConvert(212, "f", "r"), r + 212))
    def Test_IsTextFile():
        s = StringIO("Some text")
        Assert(IsTextFile(s))
        s = StringIO("Some text\xf8")
        Assert(not IsTextFile(s))
        # Also test IsBinaryFile()
        s = StringIO("Some text\xf8")
        Assert(IsBinaryFile(s))
    def Test_randq():
        s = [randq(seed=0)]
        for i in range(10):
            s.append(randq())
        s = ["%08X" % i for i in s]
        # Hex strings from "Numerical Recipes in C", page 284
        t = ["3C6EF35F", "47502932", "D1CCF6E9", "AAF95334", "6252E503",
            "9F2EC686", "57FE6C2D", "A3D95FA8", "81FDBEE7", "94F0AF1A",
            "CBF633B1"]
        Assert(s == t)
    def Test_randr():
        m = randq.maxidum
        Assert(randr(0) == (1013904223 % m)/float(m))
    util_simlink = "c:/cygwin/pylib/test/util_simlink.py"
    translated_util_simlink = "../util.py"
    def Test_IsCygwinSymlink():
        if sys.platform == "win32":
            # For this to work, create a cygwin simlink named util_simlink.py
            # in /pylib/test that points to /pylib/util.py.
            Assert(IsCygwinSymlink(util_simlink))
            Assert(not IsCygwinSymlink("c:/cygwin/home/Don/bin/data/notes.txt"))
    def Test_TranslateSymlink():
        if sys.platform == "win32":
            # For this to work, create a cygwin simlink named util_simlink.py
            # in /pylib/test that points to /pylib/util.py.
            Assert(TranslateSymlink(util_simlink) == translated_util_simlink)
    def Test_grouper():
        def even_odd(elem):         # sample mapper
            if 10 <= elem <= 20:    # skip elems outside the range
                key = elem % 2      # group into evens and odds
                return key, elem
        got = grouper(range(30), even_odd)
        expected = {0: [10, 12, 14, 16, 18, 20], 1: [11, 13, 15, 17, 19]}
        Assert(got == expected)
        got = grouper(range(30), even_odd, sum)
        expected = {0: 90, 1: 75}
        Assert(got == expected)
    def Test_Cfg():
        lines = dedent('''
            from math import sqrt
            a = 44
            b = "A string"
            def X(a):
                return a/2
            c = a*sqrt(2)
            d = X(a)
        ''').split("\n")
        d = Cfg(lines)
        Assert(d["a"] == 44)
        Assert(d["b"] == "A string")
        Assert(d["c"] == d["a"]*d["sqrt"](2))
        Assert(d["d"] == 22)
        Assert(str(d["X"])[:11] == "<function X")
    def Test_RemoveIndent():
        s = '''
        This is a test
            Second line
          Third line
        '''
        lines = RemoveIndent(s, numspaces=8).split("\n")
        Assert(lines[0] == "")
        Assert(lines[1] == "This is a test")
        Assert(lines[2] == "    Second line")
        Assert(lines[3] == "  Third line")
        Assert(lines[4] == "")
    def Test_Singleton():
        class A(object): pass
        a, b = A(), A()
        Assert(hash(a) != hash(b))
        class A(Singleton): pass
        a, b = A(), A()
        Assert(hash(a) == hash(b))
    def Test_Batch():
        s = "0123456789"
        r = ("012", "345", "678", "9")
        for i, b in enumerate(Batch(s, 3)):
            Assert(r[i] == ''.join(list(b)))
    def Test_GroupByN():
        n, m = 5, 3
        s = range(n)
        t = ((0, 1, 2),)
        Assert(t == tuple(GroupByN(s, m, fill=False)))
        t = ((0, 1, 2), (3, 4, None))
        u = tuple(GroupByN(s, m, fill=True))
        Assert(t == tuple(GroupByN(s, m, fill=True)))
    def Test_IsConvexPolygon():
        p = ((0, 0), (1, 0), (1, 1), (0, 1))
        Assert(IsConvexPolygon(*p))
        p = ((0, 0), (1, 0), (1, 1), (0.5, 0.5))
        Assert(not IsConvexPolygon(*p))
        # Test with lines slightly above and below the above figure's
        # diagonal.
        d = 1e-10
        p = ((0, 0), (1, 0), (1, 1), (0.5 + d, 0.5))    # Concave
        Assert(not IsConvexPolygon(*p))
        p = ((0, 0), (1, 0), (1, 1), (0.5 - d, 0.5))    # Convex
        Assert(IsConvexPolygon(*p))
        p = ((0, 0), (1, 0), (1, 1), (0.5, 0.5 + d))    # Convex
        Assert(IsConvexPolygon(*p))
        p = ((0, 0), (1, 0), (1, 1), (0.5, 0.5 - d))    # Concave
        Assert(not IsConvexPolygon(*p))
    def Test_StringToNumbers():
        s = "4j 3/5 6. 7"
        Assert(StringToNumbers(s) == (4j, Fraction(3, 5), 6.0, 7))
    def Test_Paste():
        a = ["a", "b", 1]
        b = ["d", "e"]
        c = ["f"]
        s = Paste(a, b, c)
        Assert(s == ['a\td\tf', 'b\te\t', '1\t\t'])
    def Test_ItemCount():
        f, F = ItemCount, Fraction
        raises(Exception, f, 1)
        raises(Exception, f, 1.0)
        raises(Exception, f, F(1, 1))
        raises(Exception, f, object())
        # Empty sequence returns empty string
        Assert(f([]) == [])
        # Elementary counting
        Assert(f([1]) == [(1, 1)])
        Assert(f([1.0]) == [(1.0, 1)])
        Assert(f([1, 1]) == [(1, 2)])
        Assert(f([1, 1, 1]) == [(1, 3)])
        # Two element types
        Assert(f([1, 2]) == [(1, 1), (2, 1)])
        Assert(f([1, 1, 2]) == [(1, 2), (2, 1)])
        Assert(f([1, 2.0]) == [(1, 1), (2.0, 1)])
        Assert(f([1.0, 2.0]) == [(1.0, 1), (2.0, 1)])
        Assert(f([1.0, 2.0, 2]) == [(2.0, 2), (1.0, 1)])
        Assert(f([1.0, 2, 2.0]) == [(2, 2), (1.0, 1)])
        Assert(f([1.0, 2, 2.0, F(2, 1)]) == [(2, 3), (1.0, 1)])
        # Show order can matter.  Thus, the results can be syntactically
        # different but semantically the same.
        Assert(f([1, 2, 1, 2]) == [(1, 2), (2, 2)])
        Assert(f([2, 1, 1, 2]) == [(2, 2), (1, 2)])
        Assert(f([2, 1, F(1, 1), 2]) == [(2, 2), (1, 2)])
        # Item type also matters
        Assert(f([1, F(1, 1)]) == [(1, 2)])
        Assert(f([1.0, F(1, 1)]) == [(1.0, 2)])
        Assert(f([F(1, 1), 1.0]) == [(F(1, 1), 2)])
        Assert(f([F(1, 1), 1]) == [(F(1, 1), 2)])
        # Fractions
        Assert(f([F(1, 2), 1]) == [(F(1, 2), 1), (1, 1)])
        Assert(f([F(1, 2), F(1, 2)]) == [(F(1, 2), 2)])
        # Show that it works with strings
        Assert(f(["a", "b", "a"]) == [("a", 2), ("b", 1)])
        # Any hashable object can be counted
        a, b = object(), object()
        Assert(f([a, b]) == [(a, 1), (b, 1)])
        # Show the n keyword returns the n largest counts
        a = [1, 2, 2, 3, 3, 3]
        Assert(f(a, n=1) == [(3, 3)])
        Assert(f(a, n=2) == [(3, 3), (2, 2)])
        Assert(f(a, n=3) == [(3, 3), (2, 2), (1, 1)])
        Assert(f(a, n=4) == [(3, 3), (2, 2), (1, 1)])
    def Test_ReadVariables():
        code = dedent('''
        a = 3
        b = 4
        c = "5"''')
        s = StringIO(code)
        d = ReadVariables(s)
        Assert(d == {"a": 3, "b": 4, "c": "5"})
    def Test_VisualCount():
        s = (1, 1, 1, 2, "a", "a", (1, 2))
        got = "\n".join(VisualCount(s, width=20))
        expected = dedent('''
        1      *************
        a      ********
        2      ****
        (1, 2) ****''')
        Assert(got == expected)
    def Test_Walker():
        return  # Walker() is commented out
        dir, file = "walker", "a"
        if 0:   # Old method using os.path
            # Construct a dummy directory structure
            path = os.path.join(dir, file)
            try:
                os.mkdir(dir)
            except FileExistsError:
                pass
            open(path, "w").write("hello")
            # Test we see directory
            w = Walker()
            w.dir = True
            for i in w("."):
                # Ignore the test directory (needed after moving util.py to
                # /plib)
                if "test" in i:
                    continue
                Assert(i.replace("\\", "/") == "./walker")
            # Test we see file
            w = Walker()
            w.dir = False
            for i in w("walker"):
                Assert(i.replace("\\", "/") == "walker/a")
            # Remove what we set up
            os.remove(path)
            os.rmdir(dir)
        else:   # Use pathlib
            p = P(".")/dir
            try:
                p.mkdir()
            except Exception:
                if p.is_dir():
                    pass
                else:
                    raise ValueError(f"Couldn't make {p}")
            path = p/file
            path.write_text("hello")
            # Test we see directory
            w = Walker()
            w.dir = True
            for i in w("."):
                # Ignore the test directory (needed after moving util.py to
                # /plib)
                if "test" in i:
                    continue
                Assert(i.replace("\\", "/") == "./walker")
            # Test we see file
            w = Walker()
            w.dir = False
            for i in w("walker"):
                Assert(i.replace("\\", "/") == "walker/a")
            # Remove what we set up
            path.unlink()
            p.rmdir()
    def Test_BraceExpansion():
        # Simple
        s = ' '.join(BraceExpansion("a{d,c,b}e"))
        assert(s == "ade ace abe")
        #
        Assert(list(BraceExpansion("a.{a, b}")) == ['a.a', 'a. b'])
        # Cartesian product
        s = list(BraceExpansion("{A,B,C,D}{A,B,C,D}"))
        t = [i + j for i, j in itertools.product('ABCD', repeat=2)]
        Assert(s == t)
        #
        s = ' '.join(BraceExpansion("{a,b,c}{d,e,f}"))
        t = ' '.join([i + j for i, j in product("abc", "def")])
        Assert(s == t)
        s = str(list(BraceExpansion("{a,b}/*.{jpg,png}")))
        t = "['a/*.jpg', 'a/*.png', 'b/*.jpg', 'b/*.png']"
        Assert(s == t)
        # Nested
        s = ' '.join(BraceExpansion("{,a}{b,{c,d},e}"))
        t = "b c d e ab ac ad ae"
        assert(s == t)
    def Test_EBCDIC():
        a2e, e2a = EBCDIC()
        # Show that these byte translation tables are inverses
        a = bytearray(range(256))
        e = a.translate(a2e)
        a1 = e.translate(e2a)
        Assert(a == a1)
    def Test_Ampacity():
        dia_mm = 11.68
        i = Ampacity(dia_mm, insul_degC=60, ambient_degC=30)
        Assert(i == 193.46399267737598)
        i = Ampacity(dia_mm, insul_degC=75, ambient_degC=30)
        Assert(i == 229.27285356605438)
        i = Ampacity(dia_mm, insul_degC=90, ambient_degC=30)
        Assert(i == 258.78428183511033)
        # Test a derated value
        i = Ampacity(dia_mm, insul_degC=90, ambient_degC=21)
        Assert(i == 1.04*258.78428183511033)
    def Test_RandomIntegers():
        # Random, no duplicates
        n = 10
        maxint = 10     # This means we must get all integers from 0 to 9
        s = RandomIntegers(n, maxint, seed=None, duplicates_OK=False)
        Assert(s == list(range(n)))
        # Random, no duplicates, larger set
        s = RandomIntegers(n, 1000, seed=None, duplicates_OK=False)
        t = RandomIntegers(n, 1000, seed=None, duplicates_OK=False)
        Assert(s != t)
        # maxint is too small --> generates exception
        with raises(ValueError):
            s = RandomIntegers(n, 9, seed=None, duplicates_OK=False)
        # maxint == 0 OK if duplicates allowed
        maxint = 0
        s = RandomIntegers(n, maxint, seed=None, duplicates_OK=True)
        Assert(s == [0]*n)
        # Repeatable sequence
        s = RandomIntegers(n, 1000, seed=0, duplicates_OK=False)
        t = RandomIntegers(n, 1000, seed=0, duplicates_OK=False)
        Assert(s == t)
        s = RandomIntegers(n, 1000, seed=0, duplicates_OK=True)
        t = RandomIntegers(n, 1000, seed=0, duplicates_OK=True)
        Assert(s == t)
    def Test_check_names():
        'Make sure the docstring list of names is up-to-date'
        if not check_names:
            return
        names = set()
        ignore = "Miscellaneous".split()
        for line in __doc__.split("\n"):
            if not line.strip():
                continue
            name = line.split()[0]
            if name in ignore:
                continue
            names.add(name)
            if name not in mnames:
                print(f"{name} in docstring not in module")
        print("-"*70)
        for name in mnames:
            if name.startswith("Test"):
                continue
            if name not in names:
                print(f"{name} in module not in docstring")
        exit()#xx
    def Test_iDistribute():
        def Dist(seq):
            'Return distances between numbers in seq'
            out = []
            for i in range(1, len(seq)):
                out.append(abs(seq[i] - seq[i - 1]))
            return out
        a, b = 0, 255
        if 1: #xx
            for n in range(2, 256):
                s = iDistribute(n, a, b)
                if s is None:
                    print(f"n = {n} no solution")
                    continue
                d = list(set(Dist(list(s))))
                if len(d) > 1 and n > 2:
                    assert_equal(len(d), 2)
                    assert_equal(abs(d[0] - d[1]), 1)
        for n in range(257, 265):
            raises(ValueError, list, iDistribute(n, a, b))
    def TestParameterSequence():
        fd = fDistribute
        expected = [0.0, 1.0]
        got = list(fd(2))
        assert_equal(got, expected)
        #
        expected = [0.0, 0.5, 1.0]
        got = list(fd(3))
        assert_equal(got, expected)
        #
        expected = [Fraction(0, 1), Fraction(1, 2), Fraction(1, 1)]
        got = list(fd(3, impl=Fraction))
        assert_equal(got, expected)
        #
        expected = [1.0, 1.5, 2.0]
        got = list(fd(3, a=1, b=2))
        assert_equal(got, expected)
        # Check type/value violations
        with raises(TypeError) as x:
            list(fd(1.0))
        with raises(ValueError) as x:
            list(fd(1))
        with raises(TypeError) as x:
            list(fd(2, a=""))
        with raises(TypeError) as x:
            list(fd(2, b=""))
        with raises(ValueError) as x:
            list(fd(1, a=2, b=1))
    def Test_signum():
        for i in (-1, -2, -2.2, Fraction(-1, 1), Decimal("-3.7")):
            assert_equal(signum(i), -1)
        for i in (0, 0.0, Fraction(0, 1), Decimal(0)):
            assert_equal(signum(i), 0)
        for i in (1, 2, 2.2, Fraction(1, 1), Decimal("3.7")):
            assert_equal(signum(i), 1)
    check_names = False
    if check_names:
        mnames, delete = set(dir()), []
        ignore = '''
        deque defaultdict OrderedDict Iterable Decimal Fraction nlargest
        chain combinations islice groupby cycle zip_longest itemgetter xx
        randint seed ascii_letters DIGITS punctuation AlmostEqual
        SignSignificandExponent signum cmath glob math os pathlib re struct
        subprocess sys tempfile time sig Test __ Miscellaneous'''.split()
        for name in mnames:
            for s in ignore:
                if name.startswith(s):
                    delete.append(name)
                    break
        for name in delete:
            mnames.discard(name)
    exit(run(globals(), halt=0, verbose=0)[0])
