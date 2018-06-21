'''
Finds files modified within a specified time frame.
----------------------------------------------------------------------
TODO:
 
* There are numerous searches that one might like to make:
 
    - Find files that last changed at the date D +/- t.  Let the
      date be defined in various ways:
        - Jan8,2015-3:10:14
        - 8Jan2015-3:10:14
        - 8Jan2015-3:10:14
        - 20150108-3:10:14
        - 1/8/15-3:10:14
        - 1/8/2015-3:10:14
    - The last two forms need an option to let you use D/M/Y if you
      wish.
    - The above form using a hyphen might not be desired because
      you'd want to use it to indicate an interval.  For example,
      you could specify the time parameter as '8Jan2015-16Jan2015'
      to designate an interval.
 
* Look at man stat for some other info to use.  atime is last
  access, mtime is last mod time, ctime is last owner/group/perm
  change on UNIX (creation time on Windows).
 
  - Thus there might be two searches:  modification time and access
    time.
  - Use -s option with letter:  a, c, or m
 
'''
# Copyright (C) 2011, 2016 Don Peterson
# Contact:  gmail.com@someonesdad1
 
#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#
 
from __future__ import print_function, division
import sys
import os
import os.path
import getopt
import time
import re
from sig import sig
from pprint import pprint as pp

# The color.py module is used to get color output when the -D option is
# used, but it's not required.
try:
    import color
    _have_color = True
except ImportError:
    # Make a dummy color object to swallow function calls
    class Dummy:
        def fg(self, *p, **kw):
            pass
        def normal(self, *p, **kw):
            pass
        def __getattr__(self, name):
            pass
    color = Dummy()
    _have_color = False
C = color

manual = '''
Usage:  {name} [options] [age [dir [dir2...]]]
  Recursively print out changed files younger than the given age in the
  indicated directories (defaults to current directory).  age is a
  number with an optional letter suffix (defaults to 1d):
      s   seconds       M   minutes         h   hours
      w   weeks         m   months          y   years
      d   days [default]                    i   infinity
  age can contain a hyphen specifying a time interval to which the
  printed files must belong (example: '1y-2y' means the file changed
  between 1 and 2 years ago).
{verbose}
Options
    -c  Include commonly-named files
    -D  Turn debug printing on
    -H  Verbose help
    -h  This help
    -l  Decorate output with time since last change
    -m  Include ignored directories (repositories, etc.)
    -n  Show files that have not changed
    -p  Ignore picture files
    -r  Do not recurse
    -t  Sort the output names by age (most-recently changed last)
    -w  Make names case insensitive (for Windows)
    -x regexp    Ignore files that match regexp (more than one -x OK)
'''.strip()

manual_extra = '''
  Certain files and directories are ignored (see the default containers
  in the ParseCommandLine() function).  For example, the common source
  code control repository directories such as .hg, .git, and .bzr are
  ignored.

  The -l option causes the file's age to be appended; note that the
  indentation is a function of the time unit used:  the farther to the
  right it is, the older the file is.

Examples (doc is the directory to search):

    * Find all files:
            {short_name} i doc
    * Find files that changed in the last week:
            {short_name} 1w doc
    * Find files that changed between one and two weeks ago:
            {short_name} 1w-2w doc     or       {short_name} 2w-1w doc
    * Find files that changed more than 1 week ago:
            {short_name} 1w-i doc      or       {short_name} i-1w doc
    * Find files that didn't change more than 1 week ago:
            {short_name} -n 1w-i doc
'''

details = '''
Details
  The primary use case for the {short_name} script is to help me find
  files that I have recently worked on.  With tens of thousands of my
  non-system files in thousands of directories (30+ years of saving
  data), it can be hard to remember where something is that I recently
  worked on.  But if I can pin down the date I did the work, then this
  script is useful in presenting me with a list of files that changed
  during that time. 
  
  For more fine-grained searches, use find(1).'''

def ParseCommandLine(d):
    d["-c"] = False
    d["-H"] = False
    d["-l"] = False
    d["-m"] = False
    d["-n"] = False
    d["-p"] = False
    d["-r"] = False
    d["-t"] = False
    d["-w"] = False
    d["-x"] = []
    d["dbg"] = False
    # Edit the following containers as needed
    d["directories_to_ignore"] = set(('''
        .hg .git .bzr .cache .mozilla __pycache__ .local tmp-donp-linux
    '''.replace(nl, " ").split()))
    d["picture_extensions"] = set(('''
        .bmp .dib .emf .eps .gif .ipc .ipk .j2c .j2k .jif .jp2 .jpeg
        .jpg .pbm .pct .pgm .pic .png .ppm .ps .psp .pspframe .pspimage
        .pspshape .psptube .svg .tif .tiff .tub .xbm .xpm
    '''.replace(nl, " ").split()))
    # Regular expressions for common files that should be ignored.
    d["common_files"] = set((
        re.compile(r"^\.vi$", re.I),
        re.compile(r"^\.z$", re.I),
        re.compile(r"^.*\.swp$", re.I),
        re.compile(r"^log$", re.I),
        re.compile(r"^tags$", re.I),
        re.compile(r"^[abz]$", re.I),
        re.compile(r"^.*\.pyc$", re.I),
        re.compile(r"^.*\.pyo$", re.I),
        re.compile(r"^.*\.o$", re.I),
        re.compile(r"^.*\.obj$", re.I),
    ))
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "cDHhlmnprtx:")
    except getopt.GetoptError as e:
        print(str(e))
        sys.exit(1)
    for o, a in optlist:
        if o == "-c":
            d["-c"] = not d["-c"]
        elif o == "-D":
            d["dbg"] = True
        elif o == "-H":
            d["-H"] = True
            Usage(d, 0)
        elif o == "-h":
            Usage(d, 0)
        elif o == "-l":
            d["-l"] = not d["-l"]
        elif o == "-m":
            d["-m"] = not d["-m"]
        elif o == "-n":
            d["-n"] = not d["-n"]
        elif o == "-p":
            d["-p"] = not d["-p"]
        elif o == "-r":
            d["-r"] = not d["-r"]
        elif o == "-t":
            d["-t"] = not d["-t"]
        elif o == "-w":
            d["-w"] = not d["-w"]
        elif o == "-x":
            d["-x"].append(a)
    if len(args) == 0:
        args = ["1d", "."]  # Default age and directory
    elif len(args) == 1:
        args.append(".")    # Default directory
    # Compile any regular expressions
    for i, r in enumerate(d["-x"]):
        try:
            d["-x"][i] = re.compile(r)
        except Exception:
            Error("'{}' is a bad regexp".format(r))
            exit(1)
    if d["dbg"]:     # Debug print the settings
        fg = C.lmagenta
        Dbg("Settings:", fg=fg)
        for key in sorted("dbg -n now -t -w -m -H -p -l -x -r -c".split()):
            Dbg("  {} =".format(key), d[key], fg=fg)
    return args

def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)

def Usage(d, status=1):
    name = sys.argv[0]
    short_name = os.path.split(name)[1]
    verbose = manual_extra.format(**locals()) if d["-H"] else ""
    print(manual.format(**locals()))
    print(details.format(**locals()))
    exit(status)

def GetTime(age):
    '''age is a string representing a number (integer or floating point)
    with an optional letter suffix or a time interval separated by a
    hyphen.  Return the tuple (start, end) representing this age; if no
    hyphen is present, (start,) will be returned.  Examples:
 
        age     Returned
       ------   --------
        1s      (1,)
        1       (24*3600,)          # Default unit of days
        1d      (24*3600,)
        1d-2d   (24*3600, 2*24*3600)
        2d-1d   (24*3600, 2*24*3600)
        i       (10000000000.0,)    # Note default coefficient of 1
    'i' is intended to represent an infinite time in the past.
    '''
    digits, days_per_year, s_per_hr = "1234567890", 365.25, 3600
    s_per_day = 24*s_per_hr
    age = age.strip()
    if not age:
        Usage()
    suffixes = {
        "s" : 1, "S" : 1,
        "M" : 60,
        "h" : s_per_hr, "H" : s_per_hr,
        "d" : s_per_day, "D" : s_per_day,
        "w" : 7*s_per_day, "W" : 7*s_per_day,
        "m" : days_per_year/12*s_per_day,
        "y" : days_per_year*s_per_day, "Y" : days_per_year*s_per_day,
        "i" : inf, "Y" : inf,
    }
    fmt = "'{}' is a bad age specification"
    def Translate(a):
        '''Convert the age a to a time in seconds.  The form is [n][s]
        where n is a number (defaults to 1) and s is a character
        indicating a time unit (defaults to 'd').
        '''
        a = a.strip()
        if not a:
            Error("Empty age specification in '{}'".format(age))
        if len(a) == 1 and a[-1] in suffixes:
            a = "1" + a          # Implied 1
        if a[-1] in digits:  # No letter suffix
            a += "d"
        elif a[-1] not in suffixes:
            Error("'{}' is an illegal time suffix".format(a[-1]))
        try:
            t = float(a[:-1])*suffixes[a[-1]]
        except ValueError:
            Error(fmt.format(a))
        return t
    #---------------------
    if "-" in age:
        f = age.split("-")
        if len(f) != 2:
            Error(err)
        start, end = [Translate(i) for i in f]
        return (start, end) if start <= end else (end, start)
    else:
        return (Translate(age),)

def ShouldBeIgnored(name, d):
    '''Check against the to-be-ignored regular expressions.
    '''
    for regexp in d["common_files"]:
        if regexp.match(name):
            return True
    return False

def IgnoreThisFile(file, d):
    '''If the indicated file is a picture file (indicated by its extension)
    or it matches one of the -x regular expressions, return True.
    Otherwise, return False.
    '''
    if not d["-c"]:
        name = os.path.split(file)[1]
        if d["-w"]:
            name = name.lower()
        if ShouldBeIgnored(name, d):
            return True
    if d["-x"]:
        for r in d["-x"]:
            if r.search(file):
                return True
    if d["-p"]:
        ext = os.path.splitext(os.path.split(file)[1])[1]
        if d["-w"]:
            ext = ext.lower()
        if ext in d["picture_extensions"]:
            return True
    return False

def FmtTimeDiff(td):
    '''Return s, minutes, hours, days, weeks, months, years for
    a time difference td in seconds.
    '''
    fmt, s = "{}{:.1f} {}", " "*2
    if abs(td) < 60:
        return fmt.format(s*0, td, "s")
    td /= 60
    if abs(td) < 60:
        return fmt.format(s*1, td, "min")
    td /= 60
    if abs(td) < 24:
        return fmt.format(s*2, td, "hr")
    td /= 24
    if abs(td) < 7:
        return fmt.format(s*3, td, "days")
    td /= 7
    if abs(td) < 30:
        return fmt.format(s*4, td, "wk")
    td /= 4
    if abs(td) < 12:
        return fmt.format(s*5, td, "mo")
    td /= 12
    return fmt.format(s*6, td, "yr")

def IgnoreDirectory(components, d):
    '''Return True if one of the elements of the list components is a
    directory to ignore.
    '''
    for i in components:
        if d["-w"]:
            if i.lower() in d["directories_to_ignore"]:
                return True
        else:
            if i in d["directories_to_ignore"]:
                return True
    return False

def Dbg(*s, **kw):
    if d["dbg"]:
        fg = kw.setdefault("fg", C.lblue)
        if "fg" in kw:
            del kw["fg"]
        C.fg(fg)
        print(*s, **kw)
        C.normal()

def ProcessFiles(dir, files, d):
    '''For each file in dir, determine if it has changed in the
    indicated age interval.
    '''
    Dbg("Processing directory", dir)
    filelist, now = [], d["now"]
    age0 = 0
    if len(d["age_interval"]) == 1:
        age1 = d["age_interval"][0]
    else:
        age0, age1 = d["age_interval"]
    Dbg("  age0, age1 =", age0, age1)
    for file in files:
        file = os.path.join(dir, file).replace("\\", "/")
        if file[:2] == "./":
            file = file[2:]
        if IgnoreThisFile(file, d):
            Dbg("  ", file, "--> ignored", fg=C.red)
            continue
        try:
            t = last_change_time = os.stat(file).st_mtime
            age = now - t
            in_interval = (age0 <= age <= age1)
            if d["-n"] and not in_interval:
                filelist.append((age, file))
                Dbg("  ", file, "not in interval", fg=C.lred)
            elif not d["-n"] and in_interval:
                filelist.append((age, file))
                Dbg("  ", file, "in interval", fg=C.yellow)
        except Exception:
            Dbg("  Exception on file '{}'".format(file))
            pass
    return filelist

def ProcessDirectory(dir, d):
    '''Find all files at and below dir.
    '''
    filelist = []
    for root, dirs, files in os.walk(dir):
        root = root.replace("\\", "/")
        components = root.split("/")
        if IgnoreDirectory(components, d) and not d["-m"]:
            continue
        filelist.extend(ProcessFiles(root, files, d))
        if d["-r"]:
            break
    return filelist

def PrintReport(results, d):
    '''results = (
        (age, file),
        ...
    '''
    if d["-t"]:
        results = sorted(results, reverse=True)
    if not results:
        return
    maxlen = max([len(i[1]) for i in results])
    for age_s, file in results:
        age_str = FmtTimeDiff(age_s) if d["-l"] else ""
        n = maxlen - len(file)
        print(file, " "*n, age_str)

if __name__ == "__main__":
    nl, inf = "\n", 1e20   # inf is infinite time into the past
    d = {}  # Options dictionary
    d["now"] = time.time()
    args = ParseCommandLine(d)
    d["age_interval"] = GetTime(args[0])
    results = []
    for dir in args[1:]:
        results.extend(ProcessDirectory(dir, d))
    PrintReport(results, d)
