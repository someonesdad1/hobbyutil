'''
Finds duplicate files in directory trees
    The algorithm used is to walk the directory tree(s) using os.walk().
    The files found then have their (hash, size) saved in a dictionary
    whose elements are lists.  The default hash size is 4 kbytes, which
    is a typical block size for a filesystem.  Files that have the same
    dictionary (hash, size) keys are likely to be identical files and
    are so reported.  Use the '-b 0' option to calculate the hash for
    all the bytes in the file to be more sure of identity -- the
    tradeoff is that this can increase the time the program runs by
    about an order of magnitude.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2011 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Program description string
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
    import os
    import getopt
    import hashlib
    import stat
    import re
    from collections import defaultdict
    from pdb import set_trace as xx 
if 1:   # Custom imports
    from wrap import dedent
    try:
        import color as C
        have_color = True
    except ImportError:
        have_color = False
if 1:   # Global variables
    _debug = False
    # Hashing method to use on files
    hash = hashlib.sha1
class IgnoreThisFile(Exception):
    pass
def Usage(d, status=1):
    name = sys.argv[0]
    dashb = d["-b"]
    print(dedent(f'''
    Usage:  {name} dir1 [dir2...]
      Display duplicate files in directories.  In the output, 1: means
      dir1, 2: means dir2, etc.  Hard links are reported (turn off with
      -L); use -l to have soft links reported also.
    
      For speed, only the first {dashb} bytes of a file are read to
      calculate the hash.  Thus, two files that are reported to be the
      same are probably the same, but it's not guaranteed.  Use '-b 0' to
      hash all of the files' bytes (takes longer to process).
    Options
      -b s    Read s bytes to compute hash.  0 = compare all bytes
      -c      Use color in output
      -d      Debug output to stderr
      -F      Same as -f, but print full path to file
      -f      Find duplicate file names
      -g      Include git directories in the search
      -h      Include hidden directories (implies -g and -m)
      -L      Don't report hard links
      -l      Follow symbolic links
      -m      Include Mercurial directories
      -r      Do not act recursively.
      -t n    Ignore files <= n bytes (OK to append k, M, G, T)
      -x re   Ignore specified file regexp.  Can have multiple -x's.
      -X re   Ignore specified directory regexp.  Can have multiple -X's.
      -z      Do not ignore zero-length files
    '''))
    exit(status)
def Debug(*s, **kw):
    stream = kw.setdefault("file", sys.stderr)
    ends = kw.setdefault("end", "\n")
    if _debug:
        print(*s, **kw)
def Error(*s, **kw):
    stream = kw.setdefault("file", sys.stderr)
    ends = kw.setdefault("end", "\n")
    print(*s, file=stream, end=ends)
    exit(1)
def ParseCommandLine(d):
    d["-b"] = 4096      # Bytes to read to compute hash
    d["-c"] = False     # Use color if True
    d["-d"] = False     # Show debug information
    d["-F"] = False     # Find duplicate file names, print full path
    d["-f"] = False     # Find duplicate file names
    d["-g"] = False     # Do not ignore git directories
    d["-h"] = False     # Do not ignore hidden directories
    d["-L"] = False     # Do not report hard links
    d["-l"] = False     # Dereference symbolic links
    d["-m"] = False     # Do not ignore Mercurial directories
    d["-r"] = False     # Disable recursion
    d["-t"] = -1        # Threshold for size, in bytes
    d["-x"] = set()     # File regexps to ignore
    d["-X"] = set()     # Directory regexps to ignore
    d["-z"] = False     # Do not ignore zero-length files
    # Ignore some common files I use
    d["-x"].add(re.compile(r"\.vi"))
    d["-x"].add(re.compile(r"\.z"))
    d["-x"].add(re.compile(r"\.todo"))
    d["-x"].add(re.compile(r"z"))
    d["-x"].add(re.compile(r"a"))
    try:
        optlist, dirs = getopt.getopt(sys.argv[1:], "b:cdFfghLlmrt:x:X:z")
    except getopt.GetoptError as str:
        msg, option = str
        sys.stderr.write(msg + nl)
        sys.exit(1)
    for o, a in optlist:
        if o[1] in "cdfgLlmrz":
            d[o] = not d[o]
        elif o == "-b":
            try:
                d["-b"] = int(opt[1])
            except Exception:
                Error("'%s' is a bad integer" % opt[1])
            if d["-b"] < 0:
                Error("-b option's argument must be >= 0" % opt[1])
        elif o == "-F":
            d["-F"] = True
            d["-f"] = True
        elif o == "-h":
            d["-h"] = d["-g"] = d["-m"] = True
        elif o == "-t":
            d["-t"] = GetSize(opt[1])
        elif o == "-x":
            try:
                d["-x"].add(re.compile(opt[1]))
            except Exception:
                Error("'%s' is a bad regular expression" % opt[1])
        elif o == "-X":
            try:
                d["-X"].add(re.compile(opt[1]))
            except Exception:
                Error("'%s' is a bad regular expression" % opt[1])
    if d["-d"]:
        global _debug
        _debug = True
    if not have_color:
        d["-c"] = False
    if not dirs:
        Usage(d, 1)
    Debug("Options set from command line:")
    keys = list(d.keys())
    keys.sort()
    for k in keys:
        Debug("%4s%-4s %s" % (" ", k, d[k]))
    return dirs
def GetSize(s):
    '''Return the size in bytes from the string s.  Note s can have k,
    M, G, or T appended (interpret as decimal SI prefixes).
    '''
    msg = "'%s' is a bad threshold specification" % s
    si = {"k": 3, "M": 6, "G": 9, "T": 12}
    s, factor = s.replace(" ", ""), 1
    if s[-1] in si:
        factor = int(10**si[s[-1]])
        s = s[:-1]
    try:
        i = float(s)
    except Exception:
        Error(msg)
    return int(factor*i)
def ProcessDir(dirnum, dir, d):
    '''Return a dictionary containing the information on the files in
    the directory dir.  dirnum is an integer indicating the order on
    the command line.  dir is a single directory.  d is the settings
    dictionary.
 
    The returned dictionary has the form (s=string, i=integer, b=bool):
    {
        (hash1, size1) : [
            (filename(s), inode(i), dirnum(i), islink(b)),
            ...
        ],
        (hash2, size2) : [
            (filename(s), inode(i), dirnum(i), islink(b)),
            ...
        ],
        ...
    }
    '''
    # Get a list of all the files
    dirfiles = []
    for root, dirs, files in os.walk(dir):
        root = root.replace("\\", "/")
        # Check to see if any of the components of the root path are
        # directories we should ignore.
        dir_fields = root.split("/")
        try:
            for regex in d["-X"]:
                for field in dir_fields:
                    if regex.search(field):
                        raise IgnoreThisFile()
        except IgnoreThisFile:
            Debug("Ignoring directory (-X):  ", root)
            continue
        dir_fields = set(dir_fields)
        # Check for directories that we'll ignore by default
        if ".hg" in dir_fields and not d["-m"]:
            Debug("Ignoring Mercurial directory:  ", root)
            continue    # Ignore Mercurial directories
        if ".git" in dir_fields and not d["-g"]:
            Debug("Ignoring git directory:  ", root)
            continue    # Ignore Mercurial directories
        dotted = lambda x:  x.startswith(".") and x != "."
        if any([dotted(i) for i in dir_fields]) and not d["-h"]:
            Debug("Ignoring hidden directory:  ", root)
            continue    # Ignore hidden directories
        # Check that each file doesn't match the -X regexps -- if no
        # matches, then add to the dirfiles sequence.
        for f in files:
            # If it's a soft link, ignore it unless d["-l"] is set
            s = os.path.join(root, f).replace("\\", "/")
            if os.path.islink(s) and not d["-l"]:
                Debug("Ignoring soft link:  ", s)
                continue
            found = False
            for regex in d["-x"]:
                if regex.search(f):
                    found = True
            if not found:
                if s[0:2] == "./":
                    # Remove any leading './' (makes a little easier
                    # to read the names).
                    s = s[2:]
                dirfiles.append(s)
            else:
                Debug("Ignoring file (-x):  ", s)
        if d["-r"]:
            break
    if d["-f"]:
        # Create a dictionary keyed by the file's name
        filedict = defaultdict(list)
        for i in dirfiles:
            path, name = os.path.split(i)
            filedict[name] += [path]
        return filedict
    else:
        # Create a dictionary with the file's (hash, size) as the key.
        # The values are (filename, inode_number, dirnum, is_softlink).
        hashdict = defaultdict(list)
        count = 0
        for filename in dirfiles:
            count += 1
            m = hash()
            try:
                if d["-b"]:
                    m.update(open(filename, "rb").read(d["-b"]))
                else:
                    m.update(open(filename, "rb").read())
            except IOError:
                # Either the file isn't readable or it's an orphaned soft
                # link.
                print("Couldn't open '%s'" % filename, file=sys.stderr)
                continue
            st = os.stat(filename) if d["-l"] else os.lstat(filename)
            size = st[stat.ST_SIZE]
            digest = m.hexdigest()
            inode = st[stat.ST_INO]
            islink = os.path.islink(filename)
            key = (digest, size)
            value = (filename, inode, dirnum, islink)
            Debug(key, value)
            if not size:
                # Zero-length file
                if d["-z"] and size > d["-t"]:
                    hashdict[key].append(value)
                else:
                    Debug("Ignoring zero-length file:  ", filename)
            else:
                # Nonzero length
                if size > d["-t"]:
                    hashdict[key].append(value)
                else:
                    # It's below the size threshold in d["-t"]
                    Debug("Ignoring file below threshold:  ", filename)
        return hashdict
def GetColor(size):
    '''Return a color indicating file size.
    '''
    if size < 10**5:
        return C.white
    elif size < 10**6:
        return C.yellow
    else:
        return C.lred
def PrintSize(size, stream, d):
    if d["-c"]:
        C.fg(GetColor(size))
    print("%d" % size, file=stream, end="")
    if d["-c"]:
        C.normal()
def ReportDuplicate(item, d, stream):
    '''item is a list of tuples (length > 1) that contain duplicated
    information.  Print this information to the indicated stream and
    end with a blank line.
 
        item = [
            (filename, lstat_info, dirnumber, islink),
            ...
        ]
 
    Note the lstat() info is stat() instead if the -l option is used
    because -l means to follow symbolic links.
    '''
    if not d["-L"]:
        # Get a list of hard links (soft links also look like hard
        # links if the -l option was used).
        links = defaultdict(list)
        for filename, inode, dirnumber, islink in item:
            links[inode].append((filename, dirnumber, islink))
        for inode in links:
            if len(links[inode]) > 1:
                size = os.stat(links[inode][0][0]).st_size
                if d["-c"]:
                    C.fg(C.yellow)
                if d["-l"]:
                    print("Hard-linked [inode] or soft-linked <inode> files "
                          "(-l option used) (", file=stream, end="")
                else:
                    print("Hard-linked files [inode number] (",
                          file=stream, end="")
                PrintSize(size, stream, d)
                print("):")
                if d["-c"]:
                    C.normal()
                for filename, dirnumber, islink in links[inode]:
                    t = (dirnumber, inode, filename)
                    if islink:
                        print("  %d:<%d>:  %s" % t, file=stream)
                    else:
                        print("  %d:[%d]:  %s" % t, file=stream)
                print(file=stream)
    # Print out the true duplicates
    size = os.stat(item[0][0]).st_size
    if d["-c"]:
        C.fg(C.lcyan)
    print("Duplicate files ", file=stream, end="")
    if d["-c"]:
        C.normal()
    print("(", file=stream, end="")
    # Set color of size number based on size
    PrintSize(size, stream, d)
    print(" bytes):", file=stream)
    for filename, lstat_info, dirnumber, islink in item:
        print("  %d:  %s" % (dirnumber, filename), file=stream)
    # Make sure there's a blank line to separate duplicate information
    print("", file=stream)
def ReportDuplicates(fileinfo, d, stream=sys.stdout):
    '''fileinfo is a dictionary with keys (hash, size) and values that
    are a list of tuples(filename, lstat_info, dirnumber).  d is the
    options dictionary.  stream is where to print the results.

    If a value list contains more than one tuple, this is duplicated
    information.  It can be due to either a copy of a file or a hard
    link.
    '''
    for i in fileinfo:
        if len(fileinfo[i]) > 1:
            ReportDuplicate(fileinfo[i], d, stream)
def ReportDuplicateFilenames(fileinfo, d, stream=sys.stdout):
    duplicates = []
    for key, value in fileinfo.items():
        if len(value) > 1:
            duplicates.append((key, value))
    duplicates.sort()
    for name, files in duplicates:
        if d["-F"]:
            for i in files:
                if not i:
                    i = "."
                print("%s" % os.path.join(i, name), file=stream)
        else:
            print("'%s' is duplicated in directories:" % name, file=stream)
            for i in files:
                if not i:
                    i = "."
                print("    %s" % i, file=stream)
        print(file=stream)
if __name__ == "__main__":
    d = {}  # Options dictionary
    dirs = ParseCommandLine(d)
    fileinfo = defaultdict(list)
    for dirnum, dir in enumerate(dirs):
        t = ProcessDir(dirnum + 1, dir, d)
        if t:
            for key, value in t.items():
                fileinfo[key] += value
    if d["-f"]:
        ReportDuplicateFilenames(fileinfo, d)
    else:
        ReportDuplicates(fileinfo, d)
