'''
Execute a makefile when a file changes
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
    # Execute a makefile when a file changes
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
    import os
    import getopt
    import time
if 1:   # Custom imports
    from wrap import dedent
    try:
        import color as c
    except ImportError:
        # Dummy object that will swallow calls to the color module
        class C:
            def __setattr__(self, attr, x):
                pass
            def __getattr__(self, attr):
                return None
            def fg(self, *p):
                pass
            def normal(self):
                pass
        c = C()
def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)
def Usage(d, status=1):
    st = d["-s"]
    print(dedent(f'''
    Usage:  {sys.argv[0]} [options] [kfile]
      Monitors the files given on the separate lines of the text file
      kfile and when the source file is newer than the destination file,
      a command is invoked with the indicated target.  The lines of kfile
      must be of the forms (blank lines ignored)
          # This is a comment
          src, dest, cmd
      where src is the name of the source file, dest is the name of the
      destination file, and cmd is a command list to execute when src is
      newer than dest.  cmd can be a list of commands separated by ';'
      characters.
    
      If no kfile is given on the command line, the script's name has
      '.py' removed and '.mk' substituted; this file is looked for in the
      current directory and used if it is found.
    Use case
      I use this script when working on documentation that uses restructured
      text that gets converted to an HTML file.  It works well when you can set
      your browser up to automatically reload a file when it changes.
    Example
        # Example kfile to construct an HTML file when a restructured
        # text file or CSS file change their contents.
        project.rst, project.html, make project.html
        project.css, project.html, make project.html
      will cause make to be called if either project.rst or project.css
      are newer than project.html.
    Options
      -h    Print this message
      -n    Echo the commands that would be executed but don't call
            them.
      -s t  Sleep time t in s between checking file times.  t can be a
            floating point number.  Default is {st} seconds.
    '''))
    exit(status)
def ParseCommandLine(d):
    d["-n"] = False     # Dry run
    d["-s"] = 1.0       # Default sleep time in s
    try:
        optlist, filename = getopt.getopt(sys.argv[1:], "hns:")
    except getopt.GetoptError as e:
        msg, option = e
        print(msg)
        exit(1)
    for opt in optlist:
        if opt[0] == "-n":
            d["-n"] = True
        if opt[0] == "-s":
            try:
                d["-s"] = float(opt[1])
                if d["-s"] < 0:
                    raise ValueError()
            except ValueError:
                msg = "-s option's argument must be a number >= 0"
                Error(msg)
        if opt[0] == "-h":
            Usage(d, status=0)
    if not filename:
        # Construct a default mk file and see if it exists in the
        # current directory.
        path, file = os.path.split(sys.argv[0])
        name, ext = os.path.splitext(file)
        filename = name + ".mk"
        if not os.path.isfile(filename):
            Usage(d)
    return filename
def GetLines(filename, d):
    '''Read in the lines from filename, strip out comments, and build
    the d["lines"] list for periodic checking.
    '''
    d["lines"] = D = []
    for linenum, line in enumerate(open(filename).readlines()):
        s = line.strip()
        if not s or s[0] == "#":
            continue
        fields = [i.strip() for i in s.split(",", 2)]
        if len(fields) != 3:
            msg = "Improper number of fields on line {linenum+1}:\n  {line}"
            Error(msg)
        # Parse the commands
        fields[2] = tuple([i.strip() for i in fields[2].split(";")])
        D.append(tuple(fields))
def GetTime(d):
    t, s = time.time() - d["start"], "s"
    # Change to minutes or hours as needed
    if t > 3600:
        t /= 3600
        s = "hr"
    elif t > 60:
        t /= 60
        s = "min"
    return "%.1f %s" % (t, s)
def Execute(cmd, d):
    '''cmd is of the form (src, dest, cmdlist) where src is the source
    file, dest is the destination file, and cmdlist is the set of
    commands to execute if src is newer than dest.
    '''
    src, dest, cmdlist = cmd
    # Get last modification times
    try:
        tm_src = os.stat(src).st_mtime
        tm_dest = os.stat(dest).st_mtime
    except Exception as e:
        msg = "Couldn't get modification times for '%s' or '%s'"
        c.fg(c.yellow)
        print(msg % (src, dest))
        c.normal()
        return
    if tm_src <= tm_dest:
        return
    # Execute commands because source is newer than destination
    print("'%s' is newer than '%s' [%s]" % (src, dest, GetTime(d)))
    for cmd in cmdlist:
        if d["-n"]:
            print("Dry run: ", cmd, "[%s]" % GetTime(d))
        else:
            status = os.system(cmd)
            if status:
                c.fg(lred)
                print("'%s' returned nonzero status" % cmd)
                c.normal()
if __name__ == "__main__":
    d = {}  # Options dictionary
    d["start"] = time.time()
    filename = ParseCommandLine(d)
    GetLines(filename, d)
    while True:
        for cmd in d["lines"]:
            Execute(cmd, d)
        time.sleep(d["-s"])
