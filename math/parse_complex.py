'''
Changes needed:

    * Making a class doesn't make sense.  Change to a single function.
    * 4-i fails.
    * A state machine might be a better implementation.
    * Need a set of test cases that exhibit the range of things that
      will be seen.
    * A composite number will be split on a + or - sign in the middle.

      0 +0 -0 1 +1 -1 1e1 1e-1 +1e1 -1e1 -1e-1 1e-1 
      1e1 1E1 1d1 1D1
      i j I J
      i -i +i 2i -2i +2i i2 -i2 +i2
      1+i 1-i -1+i -1-i 
      1+2i 1-2i -1+2i -1-2i 
      1+i2 1-i2 -1+i2 -1-i2 
      2i+1 -2i+1 2i-1 -2i-1
      i2+1 -i2+1 i2-1 -2i-1
      2.3e5i+1 2.3e+5i+1 2.3e-5i+1
      i2.3e5i+1 i2.3e+5i+1 i2.3e-5+1


    * States
        s   Read a sign
        p   Read a decimal point
        d   Reading digits of a number
        e   Reading an 'e' to start an exponent
        i   Read complex unit
        x   End of input

                    Allowed
        State       Transitions
        s           s p d i
        d           s d e s x
        e           s d
        i           s d x

'''
'''
Class to parse complex numbers represented by strings such as:
 
    1, i, j, -i, +3i
    1-3J, 1-J3
    -3i + 1, -j 3 +\\n 1
    4-i (current fails on this)
 
Note all whitespace in the string will be removed before trying to
parse it as a complex number.
 
The reasons you might want to use this module are:
 
    * The string can contain whitespace.
    * i,j, I, or J can be used as the imaginary unit.
    * The imaginary unit can precede or follow the imaginary part.
    * You can specify the floating point number type to use, allowing
      no loss of precision when desired.
 
Example:  suppose you wanted to parse the following string
representing a complex number:
 
0.333333333333333333333333333333333 - i3.444444444444444444444444444444
 
If you use python, you'll have to change the i to a j and put it after
the 3.444...; then it can be parsed using
 
eval("0.333333333333333333333333333333333-3.44444444444444444444444444444j")
 
yielding
 
    (0.33333333333333331-3.4444444444444446j)
 
Note the loss of numerical precision by using the platform's floating
point numbers.  This module, however, can return two Decimal numbers
representing the real and imaginary parts; note the initialization of
the ParseComplex class with the desired floating point type (python
fractions.Fraction also work):
 
    c = ParseComplex(Decimal)
    rp = "0.333333333333333333333333333333333"
    ip = "3.44444444444444444444444444444"
    r, i = c(rp + "\n-i" + ip)  # Note inclusion of a newline
    assert r == Decimal(rp)
    assert i == Decimal("-" + ip)
 
The ability to specify the floating point number type allows you to
maintain the problem's resolution.
'''
 
# Copyright (C) 2008, 2012 Don Peterson
# Contact:  gmail.com@someonesdad1
 
#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#
 
import re
from pdb import set_trace as xx 

class ParseComplex(object):
    '''Parses complex numbers in the ways humans like to write them.
    Instantiate the object, then call it with the string to parse; the
    real and imaginary parts are returned as a tuple.  You can pass in a
    number type to the constructor (you can also use fractions.Fraction)
    and the returned tuple will be composed of that type of number.
    '''
    _cre = r'''
        %s                          # Match at beginning
        ([+-])%s                    # Optional leading sign
        %s                          # Placeholder for imaginary unit
        (\.\d+|\d+\.?|\d+\.\d+)     # Required digits and opt. decimal point
        (e[+-]?\d+)?                # Optional exponent
        %s                          # Match at end
    '''
    # Pure imaginary, xi or ix
    _I1 = _cre % ("^", "?", "", "[ij]$")
    _I2 = _cre % ("^", "?", "[ij]", "$")
    # Reals
    _R = _cre % ("^", "?", "", "$")
    # Complex number:  x+iy
    _C1 = (_cre % ("^", "?", "", "")) + (_cre % ("", "", "", "[ij]$"))
    # Complex number:  x+yi
    _C2 = (_cre % ("^", "?", "", "")) + (_cre % ("", "", "[ij]", "$"))
    # Complex number:  iy+x
    _C3 = (_cre % ("^", "?", "[ij]", "")) + (_cre % ("", "?", "", "$"))
    # Complex number:  yi+x
    _C4 = (_cre % ("^", "?", "", "[ij]")) + (_cre % ("", "?", "", "$"))
    # Regular expressions (Flags:  I ignore case, X allow verbose)
    _imag1 = re.compile(_I1, re.X | re.I)
    _imag2 = re.compile(_I2, re.X | re.I)
    _real = re.compile(_R, re.X | re.I)
    _complex1 = re.compile(_C1, re.X | re.I)
    _complex2 = re.compile(_C2, re.X | re.I)
    _complex3 = re.compile(_C3, re.X | re.I)
    _complex4 = re.compile(_C4, re.X | re.I)
    def __init__(self, number_type=float):
        self.number_type = number_type
    def __call__(self, s):
        '''Return a tuple of two real numbers representing the real
        and imaginary parts of the complex number represented by
        s.  The allowed forms are (x and y are real numbers):
            Real:               x
            Pure imaginary      iy, yi
            Complex             x+iy, x+yi
        Space characters are allowed in the s (they are removed before
        processing).
        '''
        nt = self.number_type
        # Remove any whitespace, use lowercase, and change 'j' to 'i'
        s = re.sub(r"\s+", "", s).lower().replace("j", "i")
        # Imaginary unit is a special case
        if s in ("i", "+i"):
            return nt(0), nt(1)
        elif s in ("-i",):
            return nt(0), nt(-1)
        # "-i+3", "i+3" are special cases
        if s.startswith("i") or s.startswith("-i") or s.startswith("+i"):
            li = s.find("i")
            if s[li + 1] == "+" or s[li + 1] == "-":
                rp = nt(s[li + 1:])
                ip = -nt(1) if s[0] == "-" else nt(1)
                return rp, ip
        # "n+i", "n-i" are special cases
        if s.endswith("+i") or s.endswith("-i"):
            if s.endswith("+i"):
                return nt(s[:-2]), 1
            else:
                return nt(s[:-2]), -1
        # Parse with regexps
        mo = ParseComplex._imag1.match(s)
        if mo:
            return nt(0), self._one(mo.groups())
        mo = ParseComplex._imag2.match(s)
        if mo:
            return nt(0), self._one(mo.groups())
        mo = ParseComplex._real.match(s)
        if mo:
            return self._one(mo.groups()), nt(0)
        mo = ParseComplex._complex1.match(s)
        if mo:
            return self._two(mo.groups())
        mo = ParseComplex._complex2.match(s)
        if mo:
            return self._two(mo.groups())
        mo = ParseComplex._complex3.match(s)
        if mo:
            return self._two(mo.groups(), flip=True)
        mo = ParseComplex._complex4.match(s)
        if mo:
            return self._two(mo.groups(), flip=True)
        raise ValueError("'%s' is not a proper complex number" % s)
    def _one(self, groups):
        s = ""
        for i in range(3):
            if groups[i]:
                s += groups[i]
        return self.number_type(s)
    def _two(self, groups, flip=False):
        nt = self.number_type
        s1 = self._one(groups)
        s2 = ""
        for i in range(3, 6):
            if groups[i]:
                s2 += groups[i]
        if flip:
            return nt(s2), nt(s1)
        else:
            return nt(s1), nt(s2)

