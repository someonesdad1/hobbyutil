'''
Bug:
    * 'tlc -r -d *' fails because the directory name gets renamed, then
      the files aren't found.  The files should be renamed first, then
      the directories processed.

Rename files to all lower or upper case names.
'''

# Copyright (C) 1998, 2014 Don Peterson
# Contact:  gmail.com@someonesdad1

#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#

from __future__ import print_function, division
import os
import sys
import getopt
import color as c

from pdb import set_trace as xx
if 1:
    import debug
    debug.SetDebugger()

# python 2/3 adaptations
py3 = True if sys.version_info[0] == 3 else False
py2 = True if sys.version_info[0] == 2 else False
if py3:
    Int = (int,)
    long = int
    raw_input = input
    from io import StringIO
elif py2:
    Int = (int, long)
    chr = unichr
    from StringIO import StringIO
else:
    raise RuntimeError("Unsupported python version")

nl = "\n"
ii = isinstance

dbg = 0     # Set to nonzero to get debugging printouts
db = "="   # Debugging string header

# Variables to hold option states
incdirs = 0
recursive = 0
uppercase = 0

def Expand(filespec):
    "Glob the files in the list filespec and return a flat list"
    from glob import glob
    list = []
    for arg in filespec:
        expanded = glob(arg)
        if len(expanded) > 0:
            for el in expanded:
                list.append(el)
    return list

def GetNewName(fn, d):
    '''Return the new file name.
    '''
    def f(s):  # Change s to desired case
        return s.upper() if d["-u"] else s.lower()
    if d["-e"]:
        path, filename = os.path.split(fn)
        name, ext = os.path.splitext(filename)
        ext = f(ext)
        return os.path.join(path, name + ext)
    else:
        return f(fn)

def FixCygwinNames(files, d):
    for i in range(len(files)):
        file = files[i]
        new = file.replace("/cygdrive/", "")
        if len(new) != len(file):
            # It was a cygwin type filename
            files[i] = new[0] + ":" + new[1:]
    return files

def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)

def Usage(d, status=1):
    name = sys.argv[0]
    s = '''
Usage:  {name} [options] file1 [file2...]
  Renames files to all lowercase.  The default behavior is to show what
  will be done.  Use the -x option to actually do it.

Options:
    -d   Include directory names
    -e   Only change the case of the extension
    -u   Rename to all uppercase
    -x   Perform the indicated renaming
    -X   Perform the indicated renaming; don't write recovery file.
'''[1:-1]
    print(s.format(**locals()))
    exit(status)

def ParseCommandLine(d):
    d["-d"] = False     # Include directory names
    d["-e"] = False     # Only change extension
    d["-u"] = False     # Change to uppercase
    d["-x"] = False     # Perform the renamings
    d["-X"] = False     # Perform the renamings; no recovery file
    d["log"] = []       # Record of changes
    d["logfile"] = "tlc.recover"    # File to record changes
    if len(sys.argv) < 2:
        Usage(d)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "deux")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o in ("-d",):
            d["-d"] = True
        elif o in ("-e",):
            d["-e"] = True
        elif o in ("-u",):
            d["-u"] = True
        elif o in ("-x",):
            d["-x"] = True
        elif o in ("-X",):
            d["-X"] = True
    if not args:
        Usage(d)
    return args

def CheckLogFile(d):
    '''Check that the file d["log"] doesn't exist and that we are able to
    write to it.
    '''
    if os.path.exists(d["logfile"]):
        Error("Log file {} exists.  Stop.".format(d["log"]))
    try:
        d["logfile_handle"] = open(d["logfile"], "w")
    except Exception:
        Error("Couldn't open logfile '{}' for writing".format(d["logfile"]))

def WriteLogFile(d):
    '''Reverse the list of commands d["log"] so that running them as a
    script will reverse the renaming done.  Write these commands to the
    logfile, which has been opened as d["logfile_handle"].
    '''
    d["log"].reverse()
    for oldname, newname in reversed(d["log"]):
        cmd = "mv {} {}\n".format(newname, oldname)
        d["logfile_handle"].write(cmd)

def ProcessDirectory(dir_name, d):
    '''Rename the directory if the -d option is used.
    '''
    if d["-d"]:
        Rename(dir_name, d)

def ProcessFiles(file_list, d):
    '''file_list is a list of files or directories to rename.
    '''
    for item in file_list:
        if not item:
            continue
        if os.path.isdir(item):
            ProcessDirectory(item, d)
        else:
            Rename(item, d)

def Rename(fn, d):
    '''Rename the file named fn to all upper or lower case.  Also append
    the tuple (oldname, newname) to let us write a command to reverse the
    renamings made.  NOTE:  we don't save the commands to undo directory
    name changes because there are cases where it's not easy to recover.
    '''
    new_name = GetNewName(fn, d)
    is_dir = os.path.isdir(fn)
    arrow, s = "-->", "/" if is_dir else ""
    msg = "mv '{}{}' {} '{}{}'".format(fn, s, arrow, new_name, s)
    if fn != new_name:
        if is_dir and os.path.isdir(new_name):
            print("Can't " + msg + ":", file=sys.stderr)
            print("  Directory already exists", file=sys.stderr)
        elif os.path.isfile(fn) and os.path.isfile(new_name):
            print("Can't " + msg + ":", file=sys.stderr)
            print("  File already exists", file=sys.stderr)
        if d["-x"] or d["-X"]:
            try:
                os.rename(fn, new_name)
                s = msg.replace(arrow, "")
                if not is_dir:
                    d["log"].append((fn, new_name))
            except os.error:
                c.fg(c.lblue)
                print("Couldn't {}".format(msg))
                c.normal()
        else:
            if is_dir:
                c.fg(c.lred)
            print(msg)
            c.normal()

if __name__ == "__main__":
    d = {}  # Options dictionary
    files = ParseCommandLine(d)
    CheckLogFile(d)
    if sys.platform in set(("win32", "cygwin")):
        files = FixCygwinNames(files, d)
    ProcessFiles(files, d)
    if d["-x"] and not d["-X"]:
        WriteLogFile(d)
    else:
        # Remove the log file
        d["logfile_handle"].close()
        os.remove(d["logfile"])
