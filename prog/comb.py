'''
Generate combinations and permutations of the lines of a file.
'''

# Copyright (C) 2014 Don Peterson
# Contact:  gmail.com@someonesdad1

#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#
import sys
import os
import getopt
from itertools import combinations, permutations

def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)

def Usage(d, status=1):
    name = sys.argv[0]
    s = '''
Usage:  {name} [options] m [file]
  Generate the combinations of the lines of a file taken m at a time.
  The m items are put on one line of the output.  Input is taken from
  stdin if no file is given.  Whitespace is stripped from the trailing
  end of each line.

Options:
    -n N
        The elements are the integers from 1 to N.
    -p
        Generate permutations instead of combinations.
    -q
        Put double quotes around each line element on the output
        lines.
    -Q
        Same as -q, but use single quotes.
    -s
        Strip whitespace from the front of each line too.
    -u
        Only keep the unique lines.
    -z N
        The elements are the integers from 0 to N-1.
'''[1:-1]
    print(s.format(**locals()))
    sys.exit(status)

def ParseCommandLine(d):
    d["-Q"] = False
    d["-n"] = None
    d["-p"] = False
    d["-q"] = False
    d["-s"] = False
    d["-u"] = False
    d["-z"] = None
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "n:pQqsuz:")
    except getopt.GetoptError as e:
        msg, option = e
        print(msg)
        exit(1)
    for opt in optlist:
        if opt[0] == "-n":
            d["-n"] = int(opt[1])
        if opt[0] == "-p":
            d["-p"] = True
        if opt[0] == "-Q":
            d["-Q"] = True
        if opt[0] == "-q":
            d["-q"] = True
        if opt[0] == "-s":
            d["-s"] = True
        if opt[0] == "-u":
            d["-u"] = True
        if opt[0] == "-z":
            d["-z"] = int(opt[1])
    if len(args) not in (1, 2):
        Usage(d)
    return args

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    m = int(args[0])
    if m < 2:
        Error("m must be > 1")
    if d["-n"] is not None:
        N = int(d["-n"])
        lines = [str(i) for i in range(1, N + 1, 1)]
    elif d["-z"] is not None:
        N = int(d["-z"])
        lines = [str(i) for i in range(N)]
    else:
        if len(args) == 2:
            lines = [i.rstrip() for i in open(args[1]).readlines()]
        else:
            lines = [i.rstrip() for i in sys.stdin.readlines()]
    if d["-s"]:
        # Strip leading whitespace
        lines = [i.lstrip() for i in lines]
    if d["-u"]:
        # Only keep unique lines.  Keep entry order.
        seen, keep = set(), []
        for line in lines:
            if line in seen:
                continue
            seen.add(line)
            keep.append(line)
        lines = keep
    lines = tuple(lines)
    F = permutations if d["-p"] else combinations
    for c in F(lines, m):
        if d["-q"]:
            c = ['"' + i + '"' for i in c]
        elif d["-Q"]:
            c = ["'" + i + "'" for i in c]
        print(' '.join(c))
