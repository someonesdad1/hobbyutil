'''
This module defines the Tree() function.  This function will return
a list of strings that represent the directory tree for the directory
passed into the function.  The calling syntax is:

    Tree(dir, d, indent=4, leading_char="|"):

The variable indent controls how much each subdirectory is indented
on each line.  The variable leading_char sets the leading character
in the list; '|' might not be a bad choice.

d is a dictionary of options:
    "-m" : boolean      Include version control directories
    "-d" : int          Depth to limit to (0 means no limit)

If you call the module as a script, it will print the tree to stdout
for the directory you pass in on the command line.
'''

# TODO
#   * Add color coding for directories/files/links.
#   * Fix sorting order by sorting, then searching each line for the
#     regexp.  The escape sequences mess up the sorting.

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
from pdb import set_trace as xx 

# Decorate searches with color
try:
    from color import Decorate
    C = Decorate()
except ImportError:
    class Dummy(object):    # Swallows function calls
        def __init__(self):
            self.black = 0
            self.blue = 0
            self.green = 0
            self.cyan = 0
            self.red = 0
            self.magenta = 0
            self.brown = 0
            self.white = 0
            self.gray = 0
            self.lblue = 0
            self.lgreen = 0
            self.lcyan = 0
            self.lred = 0
            self.lmagenta = 0
            self.yellow = 0
            self.lwhite = 0
        def fg(self, *p, **kw):
            return ""
        def normal(self, *p, **kw):
            return ""
        def SetStyle(self, style, **kw):
            return ""
    C = Dummy()

d = {}  # Options dictionary

# Show regular expression matches in this color
d["hightlight_color"] = C.lred

# The following directory names are ignored unless the -m option is
# used; they are typically used for a version control system's files.
version_control = set((".bzr", ".git", ".hg", ".svn", "RCS"))

def Usage(d, status=1):
    name = sys.argv[0]
    spc = d["-n"]
    char = d["-l"]
    size = d["-t"]
    s = '''Usage:  {name} [options] dir [dir2...]
  Print a directory tree for each directory given on the command line.

Options:
  -l x    Set the leading character for the trees.  Defaults to '{char}'.
          On a dense listing, '|' can help your eye with alignment.
  -d n    Limit tree depth to n (default is to show all of tree).
  -g r    Search for regular expression r in directory names and color 
          highlight it.
  -i      Ignore case in -g regular expressions.
  -n n    Number of spaces to indent levels. [{spc}]
  -s      Decorate each directory with the size of its files in MB.
          The separation character is a tab.
  -t n    Threshold size is n MB (default {size}).  Directories with a total size
          less than this won't have the size number printed.
  -v      Include version control directories (they are ignored by default).
'''
    print(s.rstrip().format(**locals()))
    exit(status)

def ParseCommandLine(d):
    d["-d"] = 0         # Depth limit
    d["-n"] = 4         # Indent level
    d["-g"] = None      # Regular expression to highlight
    d["-i"] = False     # Ignore case in regular expressions
    d["-l"] = " "       # Leading character
    d["-s"] = False     # Decorate with size in MB
    d["-t"] = 1         # Threshold in MB for printing size
    d["-v"] = False     # Include version control directories
    if len(sys.argv) < 2:
        Usage(d)
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "d:g:hil:n:vst:")
    except getopt.GetoptError as msg:
        print(msg)
        exit(1)
    for opt in optlist:
        if opt[0] == "-d":
            d["-d"] = int(opt[1])
        elif opt[0] == "-g":
            d["-g"] = opt[1]
        elif opt[0] == "-h":
            Usage(d, 0)
        elif opt[0] == "-i":
            d["-i"] = True
        elif opt[0] == "-n":
            d["-n"] = int(opt[1])
        elif opt[0] == "-l":
            d["-l"] = opt[1]
        elif opt[0] == "-s":
            d["-s"] = True
        elif opt[0] == "-t":
            try:
                d["-t"] = float(opt[1])
            except ValueError:
                print("'{}' is not a valid floating point number".format(
                      opt[1]), file=sys.stderr)
                exit(1)
        elif opt[0] == "-v":
            d["-v"] = True
    if not len(args):
        Usage(d)
    return args

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
        s = "{:.2g} MB".format(ratio)
        if s[0] == "0":
            s = s[1:]   # Remove leading '0'
        s = "\t" + s
        if error:
            s += "*"
    else:
        s = ""
    return s

def IsVersionControlDirectory(dirname, d):
    '''Return True if dirname is in a version control directory tree.
    '''
    for i in dirname.split("/"):
        if i in version_control:
            return True
    return False

def Visit(mydirlist, dirname, files, d):
    '''Append the directory name to the list mydirlist if appropriate.
    '''
    if IsVersionControlDirectory(dirname, d) and not d["-v"]:
        return
    # Use '/' for separating directory names
    if sys.platform in set(("win32", "cygwin")):
        dirname = dirname.replace("\\", "/")
    if d["-g"] is not None:
        # Color highlight the regexp by adding escape sequences.
        # TODO Note this causes the sort order to get messed up.
        if d["-i"]:
            r = re.compile(d["-g"], re.I)
        else:
            r = re.compile(d["-g"])
        mo = r.search(dirname)
        if mo:
            start, end = mo.start(), mo.end()
            dirname = (dirname[:start] + C.fg(d["hightlight_color"]) +
                       dirname[start:end] + C.normal() +
                       dirname[end:])
    if d["-s"]:
        # Decorate this directory with the sizes of its files in MB
        dirname += GetSizesInMB(dirname, files)
    mydirlist.append(dirname)

def Tree(dir, d):
    '''Return a string representing a directory tree of the directory dir.
 
    d is a dictionary of options; see Usage() for the supported keys.
    '''
    mydirlist = []
    indent = d["-n"]
    leading_char = d["-l"]
    # walk calls visit() with args (mydirlist, dirname, name) for each
    # directory in the tree encountered at dir.  visit appends the
    # directory name if not a version control directory and decorates it
    # with size in MB if appropriate.  mydirlist will return as a list of
    # directories visited in depth-first order.
    for root, dirs, files in os.walk(dir):
        Visit(mydirlist, root, files, d)
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

if __name__ == "__main__":
    # d is global variable
    args = ParseCommandLine(d)
    for dir_to_process in args:
        for dir in Tree(dir_to_process, d):
            print(dir)
