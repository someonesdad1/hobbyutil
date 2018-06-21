'''
TODO:
    * Add a -m option that makes it ignore Mercurial directories
    * Add a -x option that lets it ignore everything at and below a
      particular directory; more than one -x option allowed.
 
This module provides a function that constructs a list containing
the sizes of directories under a specified directory.
 
If you run it as a script and want to see a list of all files >=
a specified size in MB, add a second integer or float parameter to
the command line.
'''
 
# Copyright (C) 2005 Don Peterson
# Contact:  gmail.com@someonesdad1
 
#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#
 
from __future__ import print_function, division
import os
import getopt
import sys
from pdb import set_trace as xx

nl = "\n"

# Contains directory name and total size
DirSizes = []

# Data for finding biggest files
NumBigFiles = 10    # How many to track
BigFiles = []       # List of (size, filename)
Threshold = 0       # MB threshold

# If true, list the sizes of each directory under given directory
directories_only = 0


def Usage(d, status=1):
    '''d is the options dictionary.
    '''
    numbigfiles = NumBigFiles
    name = sys.argv[0]
    threshold = d["-p"]
    manual = '''
Usage:  {name} [options] directory
  Prints a recursive listing of the largest files in and under the given
  directory.  If the directory is large, it can take a significant
  amount of time.

Options
  -d
      Change behavior to print the size of the files underneath each
      directory in the given directory.
  -n num
      How big to make the list of biggest files.  Default = {numbigfiles}.
  -p pct
      Only print directories that are >= pct in percent.  Defaults to
      {threshold}%.  Here, the percentage is of the total number of
      bytes in all the directories.
'''[1:-1]
    print(manual.format(**locals()))
    exit(status)

def TrimBigFiles():
    '''Trim the container.  If Threshold is nonzero, we keep all
    files larger than the threshold.  Otherwise, just keep the
    specified number.
    '''
    global BigFiles
    BigFiles.sort()
    if Threshold:
        BigFiles = [x for x in BigFiles if x[0] > Threshold*1e6]
    else:
        BigFiles = BigFiles[-NumBigFiles:]

def GetTotalFileSize(directory, list_of_files):
    '''Given a list of files and the directory they're in, add the
    total size and directory name to the global list DirSizes.
    '''
    global DirSizes, BigFiles
    currdir = os.getcwd()
    os.chdir(directory)
    total_size = 0
    if len(list_of_files) != 0:
        for file in list_of_files:
            if file == ".." or file == ".":
                continue
            # The following is needed because (apparently) cygwin changed
            # from using nul to /dev/null, yet if there is a file called
            # 'nul', it causes a problem in the os.stat command.
            if file == "nul":
                continue
            try:
                size = os.stat(file)[6]
            except OSError:
                continue
            total_size = total_size + size
            BigFiles.append((size, os.path.join(directory, file)))
    DirSizes.append([total_size, directory])
    TrimBigFiles()
    os.chdir(currdir)

def GetSize(directory, d):
    '''Returns a list of the form [ [a, b], [c, d], ... ] where
    a, c, ... are the number of total bytes in the directory and
    b, d, ... are the directory names.  The indicated directory
    is recursively descended and the results are sorted by directory
    size with the largest directory at the beginning of the list.
    '''
    global DirSizes
    DirSizes = []
    for root, dirs, files in os.walk(directory):
        GetTotalFileSize(root, files)
    DirSizes.sort()
    DirSizes.reverse()
    return DirSizes

def ParseCommandLine(d):
    d["-d"] = False     # Directories only
    d["-n"] = 20        # Length of big files list
    d["-p"] = 1         # Percent threshold
    if len(sys.argv) < 2:
        Usage(d)
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "dhn:p:")
    except getopt.error as s:
        print(str(s))
        exit(1)
    for opt in optlist:
        if opt[0] == "-d":
            d["-d"] = True
        elif opt[0] == "-h":
            Usage(d)
        elif opt[0] == "-n":
            global NumBigFiles
            NumBigFiles = int(opt[1])
        elif opt[0] == "-p":
            try:
                d["-p"] = float(opt[1])
            except ValueError:
                msg = "'{0}' is not a valid percentage".format(opt[1])
                print(msg, file=sys.stderr)
                exit(1)
    if not args:
        Usage(d)
    return args

def DirectoriesOnly(dir, d):
    # Get list of directories under dir
    from glob import glob
    dirs = filter(os.path.isdir, glob(os.path.join(dir, "*")))
    dirs += filter(os.path.isdir, glob(os.path.join(dir, ".*")))
    Normalize(dirs)
    results = []
    for dir in dirs:
        sizes = GetSize(dir, d)
        bytes = [x[0] for x in sizes]
        results.append((sum(bytes)/1e6, dir))
    results.sort()
    results.reverse()
    print("Size, MB   Directory")
    print("--------   ---------")
    total_size_in_MB = 0
    for size, dir in results:
        s = dir.replace("\\", "/")
        print("{0:8.1f}   {1}".format((size, s)))
        total_size_in_MB += size
    print("Total size = {0:.1f} MB".format(total_size_in_MB))

def Normalize(dirs):
    '''Replace backslashes with forward slashes.
    '''
    for i in range(len(dirs)):
        dirs[i] = dirs[i].replace("\\", "/")

def NormalizeDecorated(dirs):
    '''Replace backslashes with forward slashes.  The list dirs contains
    tuples whose second element is the directory name.
    '''
    for i in range(len(dirs)):
        dirs[i][1] = dirs[i][1].replace("\\", "/")

def ShowBiggestDirectories(directory, d):
    GetSize(directory, d)
    # Get total number of bytes
    total_size = 0
    NormalizeDecorated(DirSizes)
    for dir in DirSizes:
        total_size = total_size + dir[0]
    if total_size != 0:
        print("For directory '{0}':    ".format(directory), end=" ")
        print("[total space = {0:.1f} MB]".format((total_size / 1e6)))
        print("   %     MB   Directory")
        print("------ -----  " + "-"*50)
        not_shown_count = 0
        for dir in DirSizes:
            percent = 100.0 * dir[0] / total_size
            dir[1] = dir[1].replace("\\\\", "/")
            if percent >= d["-p"]:
                print("{0:6.1f} {1:5d}  {2}".format(percent,
                      int(dir[0]/1e6), dir[1]))
            else:
                not_shown_count = not_shown_count + 1
        if not_shown_count > 0:
            msg = "  [{0} {1} not shown]"
            di = "directories" if not_shown_count > 1 else "directory"
            print(msg.format(not_shown_count, di))

if __name__ == "__main__":
    d = {}
    args = ParseCommandLine(d)
    if d["-d"]:
        DirectoriesOnly(args[0], d)
        exit(0)
    if len(args) == 2:
        Threshold = float(args[1])
    ShowBiggestDirectories(args[0], d)
    if d["-d"]:
        print("\nFiles >= " + args[1] + " MB:")
    else:
        print("\n{0} biggest files in MB:".format(NumBigFiles))
    BigFiles.reverse()
    total = 0
    for size, file in BigFiles:
        print("{0:8.2f}  {1}".format(size/1e6, file.replace("\\", "/")))
        total += size
    print("Total size of these files = {0:.1f} MB".format(total/1e6))
