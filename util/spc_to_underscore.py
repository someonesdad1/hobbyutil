'''
Replace spaces in filenames with underscores
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
    # Replace spaces in filenames with underscores
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
    import os
    import getopt
    import pathlib
    from pdb import set_trace as xx 
if 1:   # Custom imports
    from wrap import dedent
if 1:   # Global variables
    P = pathlib.Path
def Usage():
    print(dedent(f'''
    Usage:  {sys.argv[0]} [options] item1 [item2...]
      Replace spaces in filenames with underscores.  The items can be file
      names or directories.  Run the script to show what will happen, then
      use the -x option to actually perform the renaming.
    Options
      -u      Change underscores to spaces
      -x      Perform the renaming
    '''))
    exit(1)
def ParseCommandLine():
    d["-u"] = False     # Change underscores to spaces
    d["-x"] = False     # Execute
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "ux")
    except getopt.error as str:
        print(str)
        exit(1)
    for o, a in optlist:
        if o[1] in "ux":
            d[o] = not d[o]
    if not args:
        Usage()
    return args
def ProcessFile(file):
    '''file is a Path object.  If d[-u] is True, change underscores to
    spaces; otherwise change spaces to underscores.  The action is to
    print what will be done to stdout unless -x is True, in which case 
    the file renaming is done.
    '''
    filename = str(file)
    if d["-u"]:
        if "_" not in filename:
            return
        new_name = filename.replace("_", " ")
    else:
        if " " not in filename:
            return
        new_name = filename.replace(" ", "_")
    if d["-x"]:
        file.rename(new_name)
    else:
        print(filename, "-->", new_name)
def ProcessItem(item):
    p = P(item)
    if p.is_dir():
        for file in p.glob("*"):
            if file.is_file():
                ProcessFile(file)
    elif p.is_file():
        ProcessFile(p)
    else:
        print(f"Item '{item}' not recognized", file=sys.stderr)
if __name__ == "__main__":
    sp, us = " ", "_"
    d = {"visited_directories" : set()}
    for item in ParseCommandLine():
        ProcessItem(item)
