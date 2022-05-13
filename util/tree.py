'''

Print a directory tree in hierarchical form
    - Options to consider
        - -a option to show files
        - -h to include hidden directories
        - -H to only show hidden directories
        - -v to include VC directories
        - -V to only show VC directories
        - -c for compact file display
        - -L to follow soft links
        - -p glob only show these files, can have more than one
        - -x glob exclude these files
    - Consider making each of the vertical columns of | characters
        different colors to make it easier to trace them

'''
if 1:  # Header
    # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2005 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Print a directory tree
        #∞what∞#
        #∞test∞# #∞test∞#
    # Imports
        from pathlib import Path as P
        import getopt
        import math
        import os
        import sys
        from pdb import set_trace as xx 
    # Custom imports
        from wrap import dedent
        from dppath import IsVCDir
        from color import Color, TRM as t
        if 0:
            import debug
            debug.SetDebugger()
    # Global variables
        ii = isinstance
        w = int(os.environ.get("COLUMNS", "80")) - 1
if 1:   # Utility
    def Usage(status=1):
        name = sys.argv[0]
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] dir1 [dir2...]
          Print a directory tree for each directory given on the command line.
 
          The -s option is useful to show the log of the size of the
          directory (large numbers will blink).  
        Options:
          -c      Toggle colorizing
          -l x    Indentation string for level.  [{d["-l"]!r}]
                  On a dense listing, '|' can help your eye with alignment
          -d n    Limit tree depth to n (default is to show all of tree)
          -s      Decorate name with log size (lack may mean permission error)
          -v      Include version control directories (they are ignored by default)
        '''))
        exit(status)
    def ParseCommandLine():
        d["-c"] = False     # Enable colorizing
        d["-d"] = 0         # Depth limit
        d["-l"] = "|   "    # Indentation string
        d["-s"] = False     # Decorate directory names with log(size)
        d["-v"] = False     # Include version control directories
        try:
            optlist, args = getopt.getopt(sys.argv[1:], "cd:hl:sv")
        except getopt.GetoptError as msg:
            print(msg)
            exit(1)
        for o, a in optlist:
            if o[1] in "csv":
                d[o] = not d[o]
            elif o == "-d":
                d[o] = int(a)
            elif o == "-h":
                Usage(0)
            elif o == "-l":
                d[o] = a
        if not len(args):
            Usage()
        return args
if 1:   # Core functionality
    def IsVCDir(dir):
        'Return True if dir is in a version control directory tree'
        if d["-v"]:
            return False
        if not hasattr(IsVCDir, "vc"):
            IsVCDir.vc = set((".bzr", ".git", ".hg", ".svn", "RCS"))
        for i in dir.parts:
            if i in IsVCDir.vc:
                return True
        return False
    def ShortSize(b):
        '''b is number of bytes.  Return a shortened version with an SI
        prefix as a suffix.
        '''
        assert(ii(b, int) and b >= 0)
        if not b:
            return "0"
        characteristic = int(math.log10(b))
        n, rem = divmod(characteristic, 3)
        ltr = {0:"", 1:"k", 2:"M", 3:"G", 4:"T", 5:"P", 6:"E",
               7:"Z", 8:"Y"}[n]
        s = f"{b:.6e}" 
        digits = s.split("e")[0]
        u = round(float(digits), rem)
        v = str(u).replace(".", "")
        return v[:rem + 1] + ltr
    def GetFileSize(file):
        assert(ii(file, P))
    def GetDirSize(dir):
        'Return size of files in bytes'
        assert(ii(dir, P))
        size = 0
        for item in os.scandir(dir):
            size += os.path.getsize(item)
        return size
    def ColorSize(s: int):
        '''Return the colorized integer giving the characteristic of the
        size.  The empty string is returned for s < 10.
        '''
        i = int(round(math.log10(s), 0)) if s else 0
        if not i:
            return ""
        elif i in (1, 2):
            return f"{t.c1}{i}{t.n}"
        elif i in (3, 4, 5):
            return f"{t.c3}{i}{t.n}"
        elif i in (6,):
            return f"{t.c6}{i}{t.n}"
        elif i in (7,):
            return f"{t.c7}{i}{t.n}"
        elif i in (8,):
            return f"{t.c8}{i}{t.n}"
        elif i in (9,):
            return f"{t.c9}{i}{t.n}"
        else:
            return f"{t.c10}{i}{t.n}"
    def Logsize(size_in_bytes):
        if size_in_bytes:
            return len(str(int(round(math.log10(size_in_bytes), 0))))
        else:
            return 0
    def Tree(dir):
        '''Return (maxsz, out) where maxsz is the longest directory string
        to print and out is a tuple of (decorated_str, sz, decorated_sz)
        elements  where decorated_str is the colorized string to print and
        decorated_sz is the colorized size number to print justified on the
        right.  sz is the length of the uncolored header + directory name,
        which allows the decorated_sz string to be positioned so that it
        lines up on the right.
        '''
        Tree.size = 0
        out, limit, maxsz = [], d["-d"], 0
        # Build the first element of out, which will be the directory for
        # Tree()'s argument
        s1 = f"{t.d}{dir}{t.n}"
        size_in_bytes = GetDirSize(dir)
        logsize = Logsize(size_in_bytes)
        s2 = ""
        sz = len(str(dir))
        n = w - sz - logsize
        if n > 1 and d["-s"]:
            # Can fit in the colored logsize number
            s2 = f"{ColorSize(size_in_bytes)}{t.n}"
        out.append((s1, sz, s2))
        for p in sorted(dir.rglob("*")):
            if p.is_dir():
                if IsVCDir(p) and not d["-v"]:
                    # It's a version control directory; ignore unless -v was set
                    continue
                depth = len(p.relative_to(dir).parts)
                if not limit or (limit and depth <= limit):
                    try:
                        size_in_bytes = GetDirSize(p)
                    except PermissionError:
                        continue
                    Tree.size += size_in_bytes 
                    hdr = f"{d['-l']*depth}"
                    # Get the characteristic of the size in bytes
                    logsize = Logsize(size_in_bytes)
                    maxsz = max(maxsz, len(hdr) + len(p.name) + logsize)
                    s1 = f"{hdr}{t.d}{p.name}{t.n}"
                    sz = len(hdr) + len(p.name)     # Size of first string
                    s2 = ""
                    n = w - len(hdr) - len(p.name) - logsize
                    if n > 1 and d["-s"]:
                        # Can fit in the colored logsize number
                        s2 = f"{ColorSize(size_in_bytes)}{t.n}"
                    out.append((s1, sz, s2))
        return maxsz, tuple(out)
    def GetColors():
        t.on = d["-c"]
        t.d = t(Color(255, 64, 64))     # Directories (same red as ls)
        # Colors for sizes
        t.c1 = t("gryd")
        t.c3 = t("wht")
        t.c6 = t("grn")
        t.c7 = t("roy")
        t.c8 = t("yell", None, "rb")
        t.c9 = t("magl", None, "rb")
        t.c10 = t("redl", None, "rb")

if 0:   # Test area xx
    d={"-c":0}
    GetColors()
    for i in range(12):
        print(ColorSize(10**i))
    exit()

if __name__ == "__main__":
    d = {}   # Options dictionary
    dirs = [P(i) for i in ParseCommandLine()]
    GetColors()
    for dir in dirs:
        n, out = Tree(dir)  # n is maximum width of 1st str in out
        for s1, sz, s2 in out:
            s = " "*(n - sz) if sz else ""
            print(f"{s1}{s}{s2}")
