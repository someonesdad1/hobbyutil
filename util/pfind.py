'''
File finding utility (similar to UNIX find).  It's not especially
fast, but the usage is more convenient than find and the output is
colorized to see the matches.

Run the script with no arguments to get a help message.
'''

# Copyright (C) 2008, 2012 Don Peterson
# Contact:  gmail.com@someonesdad1

#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#

from __future__ import print_function, division
import sys
import re
import getopt
import os
import fnmatch
import subprocess
from collections import OrderedDict as odict
import color as c
from pdb import set_trace as xx
if 0:
    import debug
    debug.SetDebugger()

out = sys.stdout.write
nl = "\n"

# If you're using cygwin, set the following variable to point to the
# cygpath utility.  Otherwise, set it to None or the empty string.
# This tool allows UNIX-style path conversions so that command line
# directory arguments like /home/myname work correctly.
cygwin = "c:/cygwin/bin/cygpath.exe"

# If you have some version control system directories you'd rather
# ignore, create a regexp for them and add a suitable command line
# option.
rcs = re.compile("/RCS$|/RCS")
hg = re.compile("/.hg$|/.hg/")

# The following variable, if True, causes a leading './' to be removed
# from found files and directories.  This shortens things up a bit.
# However, when the -s option is used, leaving rm_dir_tag False causes
# the current directory's entries to be printed last and sorted in
# alphabetical order.  This is how I prefer to see things, as
# sometimes the matches can be quite long and scroll off the top of
# the page.  Usually, I'm only interested in stuff in the current
# directory.
rm_dir_tag = False

# Colors for output; colors available are:
#   black   gray
#   blue    lblue
#   green   lgreen
#   cyan    lcyan
#   red     lred
#   magenta lmagenta
#   brown   yellow
#   white   lwhite

(black, blue, green, cyan, red, magenta, brown, white, gray, lblue,
 lgreen, lcyan, lred, lmagenta, yellow, lwhite) = (
    c.black, c.blue, c.green, c.cyan, c.red, c.magenta, c.brown,
    c.white, c.gray, c.lblue, c.lgreen, c.lcyan, c.lred, c.lmagenta,
    c.yellow, c.lwhite)

c_norm = (white, black)  # Color when finished
c_plain = (white, black)

# The following variable can be used to choose different color styles
colorstyle = 0
if colorstyle == 0:
    c_dir = (lred, black)
    c_match = (yellow, black)
elif colorstyle == 1:
    c_dir = (lred, black)
    c_match = (lwhite, blue)
elif colorstyle == 2:
    c_dir = (lgreen, black)
    c_match = (lred, black)
elif colorstyle == 3:
    c_dir = (lmagenta, black)
    c_match = (yellow, black)
elif colorstyle == 4:
    c_dir = (lgreen, black)
    c_match = (lwhite, magenta)
elif colorstyle == 5:
    c_dir = (lred, black)
    c_match = (black, yellow)

# Glob patterns for source code files
source_code_files = [
    "*.a",
    "*.asm",
    "*.awk",
    "*.bas",
    "*.bash",
    "*.bcc",
    "*.bsh",
    "*.c",
    "*.c++",
    "*.cc",
    "*.cgi",
    "*.cob",
    "*.cobol",
    "*.cpp",
    "*.cxx",
    "*.dtd",
    "*.f",
    "*.f90",
    "*.h",
    "*.hh",
    "*.hxx",
    "*.java",
    "*.js",
    "*.ksh",
    "*.lisp",
    "*.lua",
    "*.m4",
    "*.mac",
    "*.mp",
    "*.pas",
    "*.perl",
    "*.php",
    "*.pl",
    "*.py",
    "*.rb",
    "*.rst",
    "*.sed",
    "*.sh",
    "*.sql",
    "*.src",
    "*.tcl",
    "*.vim",
    "*.xml",
    "*.zsh",
    "[Mm]akefile",
    "*.f95",
    "*.tk",
    "*.csh",
    "*.v",
    "*.ada",
    "*.jav",
    "*.c__",
    "*.d",
    "*.f77",
    "*.lex",
    "*.yacc",
]

# Glob patterns for documentation files
documentation_files = [
    "*.doc", "*.odg", "*.ods", "*.odt", "*.pdf", "*.xls",
]

# Glob patterns for picture files
picture_files = [
    "*.bmp", "*.clp", "*.dib", "*.emf", "*.eps", "*.gif", "*.img",
    "*.jpeg", "*.jpg", "*.pbm", "*.pcx", "*.pgm", "*.png", "*.ppm",
    "*.ps", "*.psd", "*.psp", "*.pspimage", "*.raw", "*.tga", "*.tif",
    "*.tiff", "*.wmf", "*.xbm", "*.xpm",
]

class Swallow():  # Swallow calls to color module when color output is off
    def fg(self, *p, **kw):
        pass

def Usage(d, status=2):
    d["name"] = os.path.split(sys.argv[0])[1]
    d["-s"] = "Don't sort" if d["-s"] else "Sort"
    d["-c"] = "Color" if not d["-c"] else "Don't color"
    out('''Usage:  {name} [options] regex [dir1 [dir2...]]
  Finds files using python regular expressions.  If no directories are
  given on the command line, searches at and below the current
  directory.  Mercurial, git, RCS, and hidden directories are not
  searched by default.

Options:
  -C str    Globbing pattern separation string (defaults to space)
  -D        Show documentation files
  -G        Show git hidden directories and files
  -L        Follow directory soft links (defaults to False)
  -M        Show Mercurial hidden directories and files
  -P        Show picture files
  -R        Show RCS directories and files
  -S        Show source code files
  -c        {-c} code the output
  -d        Show directories only
  -f        Show files only
  -h        Show hidden files/directories that begin with '.'
  -i        Case-sensitive search
  -l n      Limit depth to n levels
  -m patt   Show only files that match glob pattern (can be multiples)
  -p        Show python files
  -r        Not recursive; search indicated directories only
  -s        {-s} the output directories and files
  -x patt   Ignore files that match glob pattern (can be multiples)

Note:  
    regex on the command line is a python regular expression defined by
    the re module.  The globbing patterns in the -m and -x options are
    the standard file globbing patterns in pythons glob module.  The -m
    and -x options can contain spaces if you define a different
    separation string with the -C option

Examples:
  * Find all python scripts at and below the current directory:
        python {name} -p .
  * Find files at and below the current directory containing
    the string "rational" (case-insensitive search) excluding *.bak and
    *.o:
        python {name} -f -x "*.bak *.o" rational
  * Find any directories named TMP (case-sensitive search) in or below
    the current directory, but exclude any with 'cygwin' in the name:
        python {name} -d -i -x "*cygwin*" TMP
  * Find all documentation and source code files starting with 't' in
    the directory foo
        python {name} -DS /t foo
    Note this will also find such files in directories that begin with
    't' also.
'''.format(**d))
    exit(status)

def ParseCommandLine(d):
    d["-C"] = " "       # Separation string for glob patterns
    d["-D"] = False     # Print documentation files
    d["-L"] = False     # Follow directory soft links
    d["-M"] = False     # Show Mercurial hidden directories
    d["-P"] = False     # Print picture files
    d["-R"] = False     # Show RCS directories
    d["-S"] = False     # Print source code files
    d["-c"] = False     # Color code the output
    d["-d"] = False     # Show directories only
    d["-f"] = False     # Show files only
    d["-h"] = False     # Show hidden files/directories
    d["-i"] = False     # Case-sensitive search
    d["-m"] = []        # Only list files with these glob patterns
    d["-l"] = -1        # Limit to this number of levels (-1 is no limit)
    d["-p"] = False     # Show python files
    d["-r"] = False     # Don't recurse into directories
    d["-s"] = False     # Sort the output directories and files
    d["-x"] = []        # Ignore files with these glob patterns
    if len(sys.argv) < 2:
        Usage(d)
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "aC:DLMPRScdfhim:l:prsx:")
    except getopt.GetoptError as str:
        msg, option = str
        out(msg + nl)
        exit(1)
    for opt in optlist:
        if opt[0] == "-C":
            d["-C"] = opt[1]
        elif opt[0] == "-D":
            d["-D"] = True
            d["-m"] += documentation_files
        elif opt[0] == "-h":
            d["-h"] = True
        elif opt[0] == "-i":
            d["-i"] = True
        elif opt[0] == "-L":
            d["-L"] = not d["-L"]
        elif opt[0] == "-M":
            d["-M"] = not d["-M"]
        elif opt[0] == "-P":
            d["-P"] = True
            d["-m"] += picture_files
        elif opt[0] == "-R":
            d["-R"] = not d["-R"]
        elif opt[0] == "-S":
            d["-S"] = True
            d["-m"] += source_code_files
        elif opt[0] == "-c":
            d["-c"] = not d["-c"]
        elif opt[0] == "-d":
            d["-d"] = not d["-d"]
        elif opt[0] == "-f":
            d["-f"] = not d["-f"]
        elif opt[0] == "-m":
            d["-m"] += opt[1].split(d["-C"])
        elif opt[0] == "-l":
            n = int(opt[1])
            if n < 0:
                raise ValueError("-l option must include number >= 0")
            d["-l"] = n
        elif opt[0] == "-p":
            d["-p"] = not d["-p"]
            d["-m"] += ["*.py"]
        elif opt[0] == "-r":
            d["-r"] = not d["-r"]
        elif opt[0] == "-s":
            d["-s"] = not d["-s"]
        elif opt[0] == "-x":
            s, c = opt[1], d["-C"]
            d["-x"] += opt[1].split(d["-C"])
    if len(args) < 1:
        Usage(d)
    if d["-i"]:
        d["regex"] = re.compile(args[0])
    else:
        d["regex"] = re.compile(args[0], re.I)
    args = args[1:]
    if len(args) == 0:
        args = ["."]
    # Store search information in order it was found
    d["search"] = odict()
    return args

def Normalize(x):
    return x.replace("\\", "/")

def TranslatePath(path, to_DOS=True):
    '''Translates an absolute cygwin (a UNIX-style path on Windows) to
    an absolute DOS path with forward slashes and returns it.  Use
    to_DOS set to True to translate from cygwin to DOS; set it to
    False to translate the other direction.
    '''
    direction = "-w" if to_DOS else "-u"
    if to_DOS and path[0] != "/":
        raise ValueError("path is not an absolute cygwin path")
    if "\\" in path:
        # Normalize path (cypath works with either form, but let's not
        # borrow trouble).
        path = path.replace("\\", "/")
    msg = ["Could not translate path '%s'" % path]
    s = subprocess.Popen(
        (cygwin, direction, path),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    errlines = s.stderr.readlines()
    if errlines:
        # Had an error, so raise an exception with the error details
        msg.append("  Error message sent to stderr:")
        for i in errlines:
            msg.append("  " + i)
        raise ValueError(nl.join(msg))
    lines = [i.strip() for i in s.stdout.readlines()]
    if len(lines) != 1:
        msg.append("  More than one line returned by cygpath command")
        raise ValueError(nl.join(msg))
    return lines[0].replace("\\", "/")

def Ignored(s, d):
    '''s is a file name.  If s matches any of the glob patterns in
    d["-x"], return True.
    '''
    for pattern in d["-x"]:
        if d["-i"]:
            if fnmatchcase(s, pattern):
                return True
        else:
            if fnmatch.fnmatch(s, pattern):
                return True
    return False

def Included(s, d):
    '''s is a file name.  If s matches any of the glob patterns in
    d["-m"], return True.
    '''
    for pattern in d["-m"]:
        if d["-i"]:
            if fnmatchcase(s, pattern):
                return True
        else:
            if fnmatch.fnmatch(s, pattern):
                return True
    return False

def PrintMatch(s, d, start, end, isdir=False):
    '''For the match in s, print things out in the appropriate colors.
    '''
    if isdir:
        c.fg(c_dir)
    else:
        c.fg(c_plain)
    out(s[:start])
    c.fg(c_match)
    out(s[start:end])
    if isdir:
        c.fg(c_dir)
    else:
        c.fg(c_plain)

def PrintMatches(s, d, isdir=False):
    '''Print the string s and show the matches in appropriate
    colors.  Note that s can end in '/' if it's a directory.
    We handle this case specially by leaving off the trailing
    '/'.
    '''
    if d["-f"] and not d["-d"]:
        # Files only -- don't print any matches in directory
        dir, file = os.path.split(s)
        out(dir)
        if dir and dir[:-1] != "/":
            out("/")
        s = file
    while s:
        if isdir and s[-1] == "/":
            mo = d["regex"].search(s[:-1])
        else:
            mo = d["regex"].search(s)
        if mo and d["-c"]:
            PrintMatch(s, d, mo.start(), mo.end(), isdir=isdir)
            s = s[mo.end():]
        else:
            # If the last character is a '/', we'll print it in color
            # to make it easier to see directories.
            if s[-1] == "/":
                out(s[:-1])
                c.fg(c_dir)
                out("/")
            else:
                try:
                    out(s)
                except IOError:
                    # Caused by broken pipe error when used with less
                    exit(0)
            s = ""
    c.fg(c_plain)
    out(nl)

def PrintReport(d):
    '''Note we'll put a '/' after directories to flag them as such.
    '''
    D = d["search"]
    if d["-s"]:
        # Print things in sorted form, directories first.
        dirs, files = [], []
        # Organize by directories and files.  Note you need to use keys()
        # to get the original insertion order
        for i in D.keys():
            if D[i]:
                dirs.append(i)
            else:
                files.append(i)
        c.fg(c_plain)
        dirs.sort()
        files.sort()
        if not d["-d"] and not d["-f"]:
            # Both directories and files
            for i in dirs:
                PrintMatches(i + "/", d, isdir=True)
            for i in files:
                PrintMatches(i, d)
        else:
            if d["-d"]:  # Directories only
                for i in dirs:
                    PrintMatches(i + "/", d, isdir=True)
            else:  # Files only
                for i in files:
                    PrintMatches(i, d)
    else:
        # Print things as encountered by os.walk
        for i in D.keys():
            if (d["-f"] and D[i]) or (d["-d"] and not D[i]):
                continue
            PrintMatches(i + "/" if D[i] else i, d, isdir=D[i])
    c.fg(c_norm)

def Join(root, name, d, isdir=False):
    '''Join the given root directory and the file name and store
    appropriately in the d["search"] odict.  isdir will be True if
    this is a directory.  Note we use UNIX notation for the file
    system's files, regardless of what system we're on.
    '''
    # Note we check both the path and the filename with the glob
    # patterns to see if they should be included or excluded.
    is_ignored = Ignored(name, d) or Ignored(root, d)
    is_included = Included(name, d) or Included(root, d)
    if is_ignored:
        return
    if d["-m"] and not is_included:
        return
    root, name = Normalize(root), Normalize(name)
    if not d["-R"]:     # Ignore RCS directories
        mo = rcs.search(root)
        if mo or name == "RCS":
            return
    if not d["-M"]:     # Ignore Mercurial directories
        mo = hg.search(root)
        if mo or name == ".hg":
            return
    # Check if we're too many levels deep.  We do this by counting '/'
    # characters.  If root starts with '.', then that's the number of
    # levels deep; otherwise, subtract 1.  Note if isdir is True, then
    # name is another directory name, so we add 1 for that.
    lvl = root.count("/") + isdir
    if root[0] == ".":
        lvl -= 1
    if d["-l"] != -1 and lvl >= d["-l"]:
        return
    if root == ".":
        root = ""
    elif rm_dir_tag and len(root) > 2 and root[:2] == "./":
        root = root[2:]
    s = Normalize(os.path.join(root, name))
    d["search"][s] = isdir

def Find(dir, d):
    def RemoveHidden(names):
        '''Unless d["-h"] is set, remove any name that begins with
        '.'.
        '''
        if not d["-h"]:
            names = [i for i in names if i[0] != "."]
        return names
    contains = d["regex"].search
    J = lambda root, name: Normalize(os.path.join(root, name))
    find_files = d["-f"] & ~ d["-d"]
    find_dirs = d["-d"] & ~ d["-f"]
    follow_links = d["-L"]
    for root, dirs, files in os.walk(dir, followlinks=follow_links):
        # If any component of root begins with '.' and it's not '..',
        # ignore unless d["-h"] is set.
        has_dot = any([i.startswith(".") and len(i) > 1 and i != ".."
                       for i in root.split("/")])
        if not d["-h"] and has_dot:
            continue
        files = RemoveHidden(files)
        dirs = RemoveHidden(dirs)
        if find_files:
            [Join(root, name, d) for name in files if contains(name)]
        elif find_dirs:
            [Join(root, dir, d, isdir=True) for dir in dirs
                if contains(J(root, dir))]
        else:
            [Join(root, name, d, isdir=True) for name in dirs
                if contains(J(root, name))]
            [Join(root, name, d) for name in files if contains(J(root, name))]
        if d["-r"]:  # Not recursive
            # This works because the search is top-down
            break

if __name__ == "__main__":
    d = {}  # Settings dictionary
    directories = ParseCommandLine(d)
    if not d["-c"]:
        c = Swallow()
    for dir in directories:
        # Following needed on cygwin
        #if dir and dir[0] == "/":
        #    dir = TranslatePath(dir)
        Find(dir, d)
    PrintReport(d)
