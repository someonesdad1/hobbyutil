'''
This module defines the Tree() function.  This function will return
a list of strings that represent the directory tree for the directory
passed into the function.  The calling syntax is:

    Tree(dir, d, indent=4, leading_char="|"):

The variable indent controls how much each subdirectory is indented
on each line.  The variable leading_char sets the leading character
in the list; '|' might not be a bad choice.

d is a dictionary of options:
    "-m" : boolean      Include Mercurial and git directories
    "-d" : int          Depth to limit to (0 means no limit)

If you call the module as a script, it will print the tree to stdout
for the directory you pass in on the command line.
'''

# Copyright (C) 2005 Don Peterson
# Contact:  gmail.com@someonesdad1

#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#

from __future__ import print_function, division
import sys
import os
import re
import getopt

d = {}  # Options dictionary

def GetSizesInMB(dirname, files):
    size, error, scale = 0, False, 1e6
    for file in files:
        try:
            s = os.stat(os.path.join(dirname, file))
            size += s.st_size
        except Exception:
            error = True
    ratio = size/scale
    if ratio >= d["-t"]:
        s = ("%.2g" % ratio) + "M"
        if s[0] == "0":
            s = s[1:]
        s = "\t" + s
        if error:
            s += "*"
    else:
        s = ""
    return s

def visit(mydirlist, dirname, files, d):
    # Append the directory name to the list mydirlist if appropriate
    if d["-s"]:
        # Decorate this directory with the sizes of its files in MB
        dirname += GetSizesInMB(dirname, files)
    if sys.platform in set(("win32", "cygwin")):
        dirname = dirname.replace("\\", "/")
    if not d["-m"] and ("/.hg" in dirname or "/.git" in dirname):
        return
    else:
        mydirlist.append(dirname)

def Tree(dir, d, indent=4, leading_char="|"):
    mydirlist = []
    # walk calls visit with args (mydirlist, dirname, name) for each
    # directory in the tree encountered at dir.  visit appends the
    # directory name if not a Mercurial directory and decorates it
    # with size in MB if appropriate.  mydirlist will return as a list of
    # directories visited in depth-first order.
    for root, dirs, files in os.walk(dir):
        visit(mydirlist, root, files, d)
    mydirlist.sort()
    head = re.compile("^" + dir)
    indent_str = leading_char + " "*(indent - 1)
    # Decorate the directory list by indenting according to how many
    # '/' characters are in the name.  Leave first entry alone because
    # it's the original directory we entered (i.e., the parameter
    # dir).
    decorations = []
    for directory in mydirlist[1:]:
        if directory == ".":
            continue
        # Remove the leading dir string
        normalized = head.sub("", directory)
        # Split the directory path into components; we only want the
        # last directory, as that's what gets decorated.
        fields = normalized.split("/")
        count = len(fields) - 1 if dir != "/" else len(fields)
        name_to_decorate = fields[-1]
        if name_to_decorate and (not d["-d"] or count <= d["-d"]):
            decorations.append(indent_str*count + name_to_decorate)
    return [dir] + decorations

def Usage(d, status=1):
    name = sys.argv[0]
    char = d["-c"]
    size = d["-t"]
    s = '''Usage:  {name} [options] dir [dir2...]
Print a directory tree for each directory given on the command line.
Mercurial directories are ignored by default.

Options:
-c x    Set the leading character for the trees.  Defaults to
        '{char}'.
-d n    Limit tree depth to n (default is to show all of tree).
-m      Include Mercurial and git directories (.hg, .git).
-s      Decorate each directory with the size of its files in MB.
        The separation character is a tab.
-t n    Threshold size is n MB (default {size}).  Directories with
        a total size less than this won't have the size number printed.
'''
    print(s.format(**locals()))
    exit(status)

def ParseCommandLine(d):
    d["-c"] = "|"       # Leading character
    d["-d"] = 0         # Depth limit
    d["-m"] = False     # Ignore Mercurial directories
    d["-s"] = False     # Decorate with size in MB
    d["-t"] = 0.1       # Threshold in MB for printing size
    if len(sys.argv) < 2:
        Usage(d)
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "c:d:hmst:")
    except getopt.GetoptError as str:
        msg, option = str
        print(msg)
        exit(1)
    for opt in optlist:
        if opt[0] == "-c":
            d["-c"] = opt[1]
        elif opt[0] == "-d":
            d["-d"] = int(opt[1])
        elif opt[0] == "-h":
            Usage(d, 0)
        elif opt[0] == "-m":
            d["-m"] = True
        elif opt[0] == "-s":
            d["-s"] = True
        elif opt[0] == "-t":
            try:
                d["-t"] = float(opt[1])
            except ValueError:
                print("'%s' is not a valid floating point number"
                      % opt[1], file=sys.stderr)
                exit(1)
    if not len(args):
        Usage(d)
    return args

if __name__ == "__main__":
    # d is global variable
    args = ParseCommandLine(d)
    char = d["-c"]
    for dir_to_process in args:
        for dir in Tree(dir_to_process, d, leading_char=char):
            print(dir)
