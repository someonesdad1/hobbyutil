'''
Prints out combinations & permutations of command line arguments.
'''
 
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Program description string
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Standard imports
    import getopt
    from pathlib import Path as P
    import sys
    from math import factorial
    from itertools import combinations, permutations
    from pdb import set_trace as xx
if 1:   # Custom imports
    from columnize import Columnize
    from wrap import wrap, dedent
    if 1:
        import debug
        debug.SetDebugger()
if 1:   # Global variables
    ii = isinstance
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        which = "combinations" if comb else "permutations"
        formula = "C(n, k)" if comb else "P(n, k)"
        k = None if comb else "n"
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] A [B...]
            Prints out {which} of command line arguments.  A is a
            string and if the only argument, then its letters are used as
            the elements.  Otherwise the set of n arguments (A, B, ...) is
            used.  If the number of the results is larger than 10!, the
            calculation time is long, so just the numbers will be printed
            unless -f is used.
        Notation
            n = number of letters in A or number of arguments if > 1
            k = items to take for each subset'''))
        if comb:
            print(dedent(f'''
            C(n, k) = combinations of n objects taken k at a time
                    = n!/((n - k)!*k!)''', n=8))
        else:
            print(dedent(f'''
            P(n, k) = all permutations of the size k subsets taken from
                      all the n elements
                    = n!/(n - k)!
            P(n)    = P(n, n) = n!''', n=8))
        print(dedent(f'''
        Options (default in square brackets):
            -c      Don't print in columns
            -h      Print some examples
            -k k    Number of objects in {formula} [{k}]
            -q      Quote the output strings
            -s x    Separator string for grouped items [""]
        '''))
        exit(status)
    def Manpage():
        print(dedent(f'''
        Print the permutations of the letters 'rgb'
            python perm.py rgb
            prints
                rgb rbg grb gbr brg bgr
                6 permutations
        Print the permutations of the letters 'rgbhsv' taken 3 at a time
            python perm.py -k 3 rgbhsv
            prints
                rgb rbv rsh grh ...
                rgh rhg rsv grs ...
                ...
                120 permutations
        Print the combinations of the letters 'rgbhsv' taken 3 at a time
            python comb.py -k 3 rgbhsv
            prints
                rgb rgs rgv rbh rbs ...
                rgh
                20 combinations
        '''))
        exit(0)
    def ParseCommandLine(d):
        d["-c"] = True      # Print in columns
        d["-k"] = None      # Choose number
        d["-q"] = False     # Quote output strings
        d["-s"] = ""        # Separator string
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "chk:qs:", "help")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        global n, k
        n = len(args[0]) if len(args) == 1 else len(args)
        for o, a in opts:
            if o[1] in list("cq"):
                d[o] = not d[o]
            elif o == "-k":
                d[o] = k = int(a)
                if k < 1 or k > n:
                    Error(f"k must be between 1 and {n}")
            elif o == "-s":
                d[o] = a
            elif o in ("-h", "--help"):
                Manpage()
        return args
if 1:   # Core functionality
    def Work(func, name, objects):
        k, count = d["-k"], 0
        if k is None and func == combinations:
            Error(f"Must use -k option with {name}")
        out = []
        for i in func(objects, k):
            t = d["-s"].join(i)
            if d["-q"]:
                t = f"'{t}'"
            out.append(t)
            count += 1
        if d["-c"]:
            for i in Columnize(out):
                print(i)
        else:
            for i in out:
                print(i)
        print(f"{count} {name}")
    def IntFactorial(n):
        assert(ii(n, int) and n >= 0)
        if n == 0:
            return 1
        if n > 50000:
            Error("Number of objects is too large")
        f = 1
        for i in range(2, n + 1):
            f *= i
        return f
    def IsLarge(objects):
        'Return number of objects if overly large, else 0'
        n = len(objects)
        k = d["-k"] if d["-k"] is not None else n
        try:
            p = int(factorial(n)/factorial(n - k))
        except OverflowError:
            # Floating point calculation overflowed
            if n > 10000:
                Error(f"{n} objects is too large")
            p = IntFactorial(n)//IntFactorial(n - k)
        if comb:
            try:
                fk = int(factorial(k))
            except OverflowError:
                fk = IntFactorial(k)
            p //= fk
        return p if p > limit else 0
    def Magnitude(n):
        assert(ii(n, int) and n > 0)
        s = str(n)
        m, e = s[0], len(s)
        e = len(s)
        return f"{m}e{e}"

if __name__ == "__main__":
    n, k = None, None
    limit = int(factorial(10))
    # Options dictionary
    d = {"name": P(sys.argv[0]).name.replace(".py", "")}
    comb = True if d["name"] == "comb" else False
    args = ParseCommandLine(d)
    objects = list(args[0]) if len(args) == 1 else args
    large = IsLarge(objects)
    if large:
        e = Magnitude(large)
    l = f"Answer too large (limit is {Magnitude(limit)}):  "
    if d["name"] == "perm":
        if large:
            print(f"{l}number of permutations = {e}")
        else:
            Work(permutations, "permutations", objects)
    else:
        if large:
            print(f"{l}number of combinations = {e}")
        else:
            Work(combinations, "combinations", objects)
