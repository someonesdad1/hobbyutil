'''
Find all file extensions used
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2012 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Find all file extensions used
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
    import os
    import getopt
    import glob
    from collections import defaultdict
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    from columnize import Columnize
def Usage(d, status=1):
    name = sys.argv[0]
    print(dedent(f'''
    Usage:  {name} [options] dir1 [dir2...]
      Prints out file extensions and their counts used in the files contained
      in the given directories.
    Options:
        -c  Ignore case differences between extensions [{d["-c"]}]
        -C  List the output in columns for a more compact report
        -f  Consider the strings input on the command line as the file list
            itself and print the report for that set
        -h  Include git/Mercurial directories
        -r  Recurse into each directory given
        -s  Sort the output by counts
    '''))
    exit(status)
def ParseCommandLine(d):
    d["-c"] = True      # Extension names are case-sensitive
    d["-C"] = False     # Print in columns
    d["-f"] = False     # Command line contains files
    d["-h"] = False     # Include .hg/.git directories
    d["-r"] = False     # Recurse into directories
    d["-s"] = False     # Sort output by counts
    if len(sys.argv) < 2:
        Usage(d)
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "Ccfhrs")
    except getopt.GetoptError as str:
        msg, option = str
        print(msg)
        sys.exit(1)
    for o, a in optlist:
        if o[1] in "Ccfhrs":
            d[o] = not d[o]
    if not args:
        Usage(d)
    return args
def Reverse(seq):
    '''seq is a list of [a, b] type pairs.  Turn each pair into the form
    [b, a].
    '''
    return [[b, a] for a, b in seq]
def PrintReport(data, d):
    '''data is the defaultdict of counts; d is the options dict.
    '''
    if "" in data:
        del data[""]
    v = data.values()
    if not v:
        # No information to report
        return
    widest_integer = max([len(str(i)) for i in v])
    fmt = "%*d %s"
    items = Reverse([list(i) for i in data.items()])
    if d["-s"]:
        # Sort by count.
        items.sort()
    else:
        # Sort by extension.
        items = Reverse(items)
        # We want to sort by the extension, but have the sort be
        # case-insensitive.  To do this, decorate the list with the
        # lower case extension, sort, then remove it.
        items = [[i[0].lower()] + i for i in items]
        items.sort()
        items = [i[1:] for i in items]
        items = Reverse(items)
    output_data = []
    for i in items:
        output_data.append(fmt % tuple([widest_integer] + i))
    if d["-C"]:
        for line in Columnize(output_data):
            print(line)
    else:
        for i in output_data:
            print(i)
def NormalizePath(path):
    return path.replace("\\", "/")
def ProcessDirectory(dir, data, d):
    assert os.path.isdir(dir)
    p = os.path.split(dir)[1]
    if (p == ".hg" or p == ".git") and not d["-h"]:
        # Ignore revision control directories
        return
    dir = NormalizePath(dir)
    ProcessFiles(glob.glob(dir + "/*"), data, d)
def ProcessFiles(files, data, d):
    '''For each file in the list files, classify the extension into
    the data container.
    '''
    for file in files:
        if os.path.isfile(file):
            name, ext = os.path.splitext(file)
            if ext:
                if not d["-c"]:
                    ext = ext.lower()
                data[ext] += 1
if __name__ == "__main__":
    d = {}  # Options dictionary
    items, data = ParseCommandLine(d), defaultdict(int)
    for item in items:
        if os.path.isdir(item):
            if d["-r"]:
                # Process directories recursively
                for directory, dirnames, files in os.walk(item):
                    directory = NormalizePath(directory)
                    r = "/.hg" in directory or ".git" in directory
                    if r and not d["-h"]:
                        continue
                    ProcessDirectory(directory, data, d)
            else:
                ProcessDirectory(item, data, d)
        else:
            ProcessFiles([item], data, d)
    PrintReport(data, d)
