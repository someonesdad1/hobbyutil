'''
Treat lines of a file like a set
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2005, 2009 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Treat lines of a file like a set
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
    import getopt
    import re
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
if 1:   # Global variables
    element_string = None   # For el operation
def Usage(status):
    print(dedent(f'''
    Usage:  {sys.argv[0]} [options] op file1 file2 [file3 ...]
      where op is the operation:
        ne               Lines in file1 are != to the lines in following files
        eq[ual]          Lines in file1 are == to the lines in following files
        el[ement]        file1 contains the string given as file2 as an element
        di[fference]     Lines in file1 that are not in the following files
        sd[ifference]  * Lines that are in file1 or the remaining files, but
                            not both (symmetric difference)
        in[tersection]   Lines that are common to all files
        is[subset]     * Determine whether file1 is a proper subset of
                            remaining files
        un[ion]          Lines that are in any of the files
      Performs operations on the lines of a file as if they were members of
      a set.  In the operations marked with '*', file2 and subsequent files
      will be collapsed into one set of lines.
    
      ne, eq, el, and is return Boolean values and also indicate the state by
      returning 0 for true and 1 for false (i.e., their exit codes).  The other
      operations return the resulting lines.  They will be stripped of leading
      and trailing whitespace if you use the -w option.
    
      Output is sent to stdout and is sorted; use the -s option if you don't
      want the lines sorted (they will be in an indeterminate order, however,
      as a set has no notion of ordering).
    Options
      -i regexp     Ignore lines that contain the regexp.  More than one of
                    these options may be given.
      -s            Do not sort the output lines
      -w            Ignore leading and trailing whitespace
    '''))
    exit(status)
def CheckArgs(args):
    if len(args) < 3:
        Usage(1)
    try:
        op = args[0][:2]
        if op not in ("ne", "eq", "el", "di", "sd", "in", "is", "un"):
            print("'%s' is not a recognized operation" % args[0],
                  file=sys.stderr)
            exit(1)
    except Exception:
        Usage(1)
    args[0] = op
    if op in ("sd", "is", "el"):
        if len(args) != 3:
            Usage(1)
    return args
def ParseCommandLine(d):
    d["-i"] = []        # Regexps of lines to ignore
    d["-s"] = True      # Sort output
    d["-w"] = False     # Ingore leading and trailing whitespace
    if len(sys.argv) < 2:
        Usage(1)
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "i:sw")
    except getopt.GetoptError as e:
        msg, option = e
        print(msg)
        sys.exit(1)
    for opt in optlist:
        if opt[0] == "-i":
            r = re.compile(opt[1])
            d["-i"].append(r)
        elif opt[0] == "-s":
            d["-s"] = False
        elif opt[0] == "-w":
            d["-w"] = True
    if len(args) < 2:
        Usage()
    return CheckArgs(args)
def GetLines(op, files, d):
    'Note the returned lines include the newline'
    def do_not_ignore(line, r):
        return not r.search(line)
    lines1 = open(files[0]).readlines()
    lines2 = []
    if op == "el":
        lines2 = []
        global element_string
        element_string = files[1] + "\n"
    else:
        for file in files[1:]:
            lines2 += open(file).readlines()
        if d["-i"]:
            for r in d["-i"]:
                lines1 = [line for line in lines1 if do_not_ignore(line, r)]
                lines2 = [line for line in lines2 if do_not_ignore(line, r)]
        if d["-w"]:
            lines1 = [line.strip() for line in lines1]
            lines2 = [line.strip() for line in lines2]
    return frozenset(lines1), frozenset(lines2)
if __name__ == "__main__":
    d = {}
    args = ParseCommandLine(d)
    op = args[0]
    del args[0]
    files = args
    lines1, lines2 = GetLines(op, files, d)
    status = 0
    if op == "di":
        results = lines1 - lines2
    elif op == "sd":
        results = lines1 ^ lines2
    elif op == "in":
        results = lines1 & lines2
    elif op == "un":
        results = lines1 | lines2
    elif op == "ne":
        print(str(lines1 != lines2))
        if lines1 == lines2:
            status = 1
    elif op == "eq":
        print(str(lines1 == lines2))
        if lines1 != lines2:
            status = 1
    elif op == "el":
        if element_string in lines1:
            print(str(True))
        else:
            print(str(False))
            status = 1
    elif op == "is":
        print(str(lines1 < lines2))
        if not lines1 < lines2:
            status = 1
    if op in ("di", "sd", "in", "un"):
        eol = "\n" if d["-w"] else ""
        if d["-s"]:
            results = list(results)
            results.sort()
        for line in results:
            print(line, end=eol)
