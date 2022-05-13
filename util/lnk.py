'''
Use the UNIX 'ls -i' command to compare the files in two directories
and identify any that are hard-linked.
'''

from __future__ import print_function, division
import sys
import subprocess
import os
import getopt
from collections import defaultdict

# Copyright (C) 2014 Don Peterson
# Contact:  gmail.com@someonesdad1

#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#
# You need to set this to the executable of a command that behaves
# like the ls command (it needs to take the -R recursive option and
# the -i option to print the inode).
ls = "c:/cygwin/bin/ls.exe"

def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)

def Usage(d, status=1):
    name = sys.argv[0]
    s = '''
Usage:  {name} [options] dir1 dir2
  Recursively compare the files in two directories and print any that
  refer to the same file (i.e., are hard-linked).  Note that a printed
  line for a particular directory may include more than one file if
  there are two hard links in that directory.

Options
    -r    Don't compare recursively -- just compare the files in the
          two directories.
Notes :
    You need to set the global variable ls in the script so that it
    points to a UNIX-style ls command.

    The GNU find command has a -samefile option to find hard links.
'''[1:-1]
    print(s.format(**locals()))
    sys.exit(status)

def ParseCommandLine(d):
    d["-r"] = True
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "r")
    except getopt.GetoptError as str:
        msg, option = str
        print(msg)
        sys.exit(1)
    for opt in optlist:
        if opt[0] == "-r":
            d["-r"] = True
    if len(args) != 2:
        Usage(d)
    return args

def GetInodes(dir, D):
    '''Run the 'ls -i' command on the directory and return a
    dictionary of the inode numbers keyed to the files.
    '''
    path = os.path.abspath(dir)
    p, d = subprocess.PIPE, defaultdict(list)
    op = "-iR" if D["-r"] else "-i"
    try:
        s = subprocess.Popen((ls, "-i", dir), stdout=p, stderr=p)
    except Exception:
        Error("Couldn't run ls command. Is ls global variable defined?")
    lines = [i.strip() for i in s.stdout.readlines()]
    for line in lines:
        fields = line.split()
        inode = int(fields[0])
        file = ' '.join(fields[1:])
        ap = os.path.join(path, file)
        d[inode].append(ap.replace("\\", "/"))
    return d

if __name__ == "__main__": 
    d = {}  # Options dictionary
    dir1, dir2 = ParseCommandLine(d)
    d1 = GetInodes(dir1, d)
    d2 = GetInodes(dir2, d)
    s = set(d1.keys()) & set(d2.keys())
    if s:
        for i in s:
            print("inode = %d = 0x%x" % (i, i))
            print("    %s" % ', '.join(d1[i]))
            print("    %s" % ', '.join(d2[i]))
