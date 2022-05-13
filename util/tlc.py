'''
Bugs:
    * Rewrite to use pathlib
    * -eu doesn't work to make extensions uppercase

Rename files to all lower or upper case names
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 1998, 2014 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Rename files to all lower or upper case names
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import os
    import sys
    import getopt
    import pathlib
    from glob import glob
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    from color import C
if 1:   # Global variables
    debug = False   # Set to True to ignore presence of a log file
    ii = isinstance
    P = pathlib.Path
    class g: pass
def UseColor(use=True):
    g.dir = C.lgrn if use else ""
    g.file = C.lmag if use else ""
    g.err = C.lred if use else ""
    g.warn = C.yel if use else ""
    g.n   = C.norm if use else ""
def Expand(filespec):
    "Glob the files in the list filespec and return a flat list"
    list = []
    for arg in filespec:
        expanded = glob(arg)
        if len(expanded) > 0:
            for el in expanded:
                list.append(el)
    return list
def GetNewName(fn):
    'Return the new file name'
    def f(s):  # Change s to desired case
        return s.upper() if d["-u"] else s.lower()
    if d["-e"]:
        path, filename = os.path.split(fn)
        name, ext = os.path.splitext(filename)
        ext = f(ext)
        return os.path.join(path, name + ext)
    else:
        return f(fn)
def FixCygwinNames(files):
    for i in range(len(files)):
        file = files[i]
        new = file.replace("/cygdrive/", "")
        if len(new) != len(file):
            # It was a cygwin type filename
            files[i] = new[0] + ":" + new[1:]
    return files
def Error(*msg, status=1):
    Warn(*msg)
    exit(status)
def Warn(*msg):
    print(*msg, file=sys.stderr)
def Usage(d, status=1):
    print(dedent(f'''
    Usage:  {sys.argv[0]} [options] file1 [file2...]
      Renames files to all lowercase.  The default behavior is to show what
      will be done.  Use the -x option to actually do it.  A recovery file
      is written that can be sourced as a POSIX shell script to undo the
      effects of the rename.  Directories are ignored unless -d is used.
    Options:
      -C   Force use of color in output
      -c   Use color in output unless stdout is not a TTY
      -d   Rename a directory name if it is on the command line, but only
           if it is not a component of one of the files to be renamed
      -e   Only change the case of the extension portion of the file
      -i   Ignore any missing files or directories
      -n   Only change the case of the name portion of the file
      -u   Rename to all uppercase
      -x   Perform the indicated renaming
      -X   Perform the indicated renaming and don't write recovery file
    '''))
    exit(status)
def ParseCommandLine(d):
    d["-C"] = False     # Force use of color in output
    d["-c"] = False     # Use color in output if TTY
    d["-d"] = False     # Include directory names
    d["-e"] = False     # Only change extension, not name
    d["-i"] = False     # Ignore missing files or directories
    d["-n"] = False     # Only change name, not extension
    d["-u"] = False     # Change to uppercase
    d["-x"] = False     # Perform the renamings
    d["-X"] = False     # Perform the renamings; no recovery file
    d["log"] = []       # Record of changes
    d["logfile"] = P("tlc.recover")    # File to record changes
    try:
        opts, args = getopt.getopt(sys.argv[1:], "CcdeinuxX")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o[1] in "CcdeinuxX":
            d[o] = not d[o]
    UseColor(use=False)
    if d["-C"] or (d["-c"] and sys.stdout.isatty()): 
        UseColor(use=True)
    if not args:
        Usage(d)
    return args
def WriteLogFile():
    '''Reverse the list of commands d["log"] so that running them as a
    script will reverse the renaming done.  Write these commands to the
    logfile, which has been opened as d["logfile_handle"].
    '''
    d["log"].reverse()
    for oldname, newname in reversed(d["log"]):
        cmd = "mv {} {}\n".format(newname, oldname)
        d["logfile_handle"].write(cmd)
def ProcessDirectory(dir_name):
    'Rename the directory if the -d option was used'
    if d["-d"]:
        Rename(dir_name)
def Rename(fn):
    '''Rename the file named fn to all upper or lower case.  Also append
    the tuple (oldname, newname) to let us write a command to reverse the
    renamings made.  fn can also be a directory name and will be renamed
    if d["-d"] was set.
 
    NOTE:  we don't save the commands to undo directory name changes because
    there are cases where it's not easy to recover.
    '''
    new_name = GetNewName(fn)
    is_dir = os.path.isdir(fn)
    arrow, s = "-->", "/" if is_dir else ""
    msg = "mv '{}{}' {} '{}{}'".format(fn, s, arrow, new_name, s)
    if fn != new_name:
        # If this is on Windows, then renaming a.JPG to a.jpg looks like
        # it's the same file.  We want to allow this, so we use same to
        # indicate the new and old names are the same ignoring case.
        same = fn.lower() == new_name.lower()
        if is_dir and os.path.isdir(new_name):
            print("Can't " + msg + ":", file=sys.stderr)
            print("  Directory already exists", file=sys.stderr)
        elif not same and os.path.isfile(fn) and os.path.isfile(new_name):
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
def GenerateListOfFiles(args):
    'Return (files, dirs) where both are lists'
    files, dirs = set(), set()
    bad = False
    for arg in args:
        p = P(arg)
        if p.is_file():
            files.add(p)
        elif p.is_dir():
            if d["-d"]:
                dirs.add(p)
            else:
                print(f"{g.warn}Directory '{arg}' ignored{g.n}")
        else:
            bad = True
            print(f"{g.err}'{arg}' isn't a file {g.n}")
    # One or more files/directories on command line missing.  Stop if the
    # -i option wasn't used.
    if bad and not d["-i"]:
        exit(1)
    # Make sure none of the files have any of the directories as components
    resolved = [i.resolve() for i in dirs]
    for file in files:
        f = file.resolve().parent
        if f in resolved:
            Error(f"{g.err}'{file}' affected by directory rename{g.n}")
    f = lambda x: list(sorted(x))
    return f(files), f(dirs)
def Process(files, dirs):
    'Arguments are lists of P objects to rename'
    f = lambda x: x.upper() if d["-u"] else x.lower()
    rename = []
    if files:
        arrow, out = f" {g.file}-->{g.n} ", []
        for file in files:
            old = str(file)
            old = P(file)
            parts = list(file.parts)
            if d["-e"]:     # Only change extension
                new_suffix = f(file.suffix)
                new_name = file.stem
                parts[-1] = new_name + new_suffix
                new = P('/'.join(parts))
            elif d["-n"]:   # Only change name
                new_suffix = file.suffix
                new_name = f(file.stem)
                parts[-1] = new_name + new_suffix
                new = P('/'.join(parts))
            else:
                parts[-1] = f(parts[-1])
                new = P('/'.join(parts))
            if file == new:
                continue
            out.append(f"  {old} {arrow} {new}")
            rename.append((old, new))
        if out:
            print(f"{g.file}Files to be renamed:{g.n}")
            for i in out:
                print(i)
    if dirs:
        arrow, out = f" {g.dir}-->{g.n} ", []
        for dir in dirs:
            old = str(dir)
            old = P(file)
            parts = list(dir.parts)
            parts[-1] = f(parts[-1])
            new = P('/'.join(parts))
            if dir == new:
                continue
            out.append(f"  {old} {arrow} {new}")
        if out:
            print(f"{g.dir}Directories to be renamed:{g.n}")
            for i in out:
                print(i)
    # Do the renaming
    if rename and (d["-x"] or d["-X"]):
        for old, new in rename:
            try:
                old.rename(new)
                d["log"].append((old, new))
            except Exception as e:
                print(f"Couldn't rename '{old}' to '{new}", file=sys.stderr)

if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    execute = d["-x"] or d["-X"]
    files, dirs = GenerateListOfFiles(args)
    if d["logfile"].exists() and not debug:
        lf = d["logfile"]
        Error(f"Log file '{lf}' exists.  Remove it or rename it.")
    else:
        # Open log file for writing
        d["logfile_handle"] = open(d["logfile"], "w")
    Process(files, dirs)
    if d["-x"] and not d["-X"]:
        WriteLogFile()
    else:
        # Remove the log file
        d["logfile_handle"].close()
        os.remove(d["logfile"])
