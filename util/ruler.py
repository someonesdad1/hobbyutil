'''
Return a ruler for ASCII printing
    Run as a script for a demo
'''
#∞test∞# ignore #∞test∞#
# Copyright (C) 2009, 2021 Don Peterson
# Contact:  gmail.com@someonesdad1
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
import os
class Ruler(object):
    '''Return ruler strings.  Initialize with either an integer or
    ones/tens strings.  Call the object to get a ruler string; if the
    call has an argument, it is an integer representing the maximum
    width of the ruler.  For no argument, the width is defined by the
    COLUMNS environment variable or is 79 if COLUMNS is not defined.
    '''
    # You can define your own choices here
    choices = (
        "····+····|", # 0
        "----+----|", # 1
        "┰┰┰┰┴┰┰┰┰┋", # 2
        "1234·67890", # 3
        "         |", # 4
        "    +    |", # 5
        "    ·    |", # 6
        "====+====█", # 7
    )
    def __init__(self, num=None, ones=None, tens=True, zb=False):
        '''If num is not None, then it must be a number that indicates
        which ruler you want.  You can also specify the ones string;
        supplying ones overrides supplying num.  If tens is True, then
        a tens line is also produced.  If zb is True, make the ruler
        zero-based.
        '''
        self.tens = tens
        self.zb = bool(zb)
        if num is None and ones is None:
            num = 0
        if num is not None:
            self.ones = Ruler.choices[num]
        else:
            self.ones = ones
            if len(self.ones) != 10:
                raise ValueError("ones must be a string of length 10")
    def __call__(self, columns=None, choice=None, ones=None):
        if ones is not None:
            if len(ones) != 10:
                raise ValueError("ones must be a string of length 10")
        elif choice is not None:
            ones = Ruler.choices[int(choice)]
        else:
            ones = self.ones
        if columns is None:
            columns = self._ncols()
        else:
            columns = abs(int(columns))
        if not columns:
            return ""
        s = ""
        n, remainder = divmod(columns, 10)
        if self.tens:
            s = ''.join(["%10d" % i for i in range(1, n + 1)]) + " "
            if self.zb:
                s = "0" + s[:-1]
            if len(s) > columns:
                s = s[:columns]
            s += "\n"
        if self.zb:
            sepchar = ones[9]
            s += sepchar + ones*n
            if remainder:
                s += ones[:remainder - 1]
        else:
            s += ones*n + ones[:remainder]
        return s
    def _ncols(self):
        columns = 80
        if "COLUMNS" in os.environ:
            columns = int(os.environ["COLUMNS"])
        # Reduce so we don't get a second line because of the newline
        columns -= 1
        return columns
if __name__ == "__main__":
    import sys
    r = Ruler()
    z = Ruler(zb=True)
    if len(sys.argv) > 1:
        # Show rulers that were chosen on the command line
        for n in sys.argv[1:]:
            print(r(choice=int(n)))
        print()
        for n in sys.argv[1:]:
            print(z(choice=int(n)))
    else:
        # Show all rulers
        for i in range(len(Ruler.choices)):
            print("Ruler type = " + str(i))
            print(r(choice=i))
        print()
        for i in range(len(Ruler.choices)):
            print("Ruler type = " + str(i) + " (zero-based)")
            print(z(choice=i))
