'''
Script to recursively descend through a directory hierarchy and write
to stdout all the files that should not have their execute bit set.
Files excluded are those that belong to certain directories such as
git, Mercurial, etc., executables such as *.exe, *.com, *.bat, and
those whose first two bytes are #!.
 
The intent is to allow you to pass the output to other programs,
such as xargs.  Note:  for Windows, you'll want to use the -0 option,
which puts a null character after the filename rather than a newline.
This lets GNU xargs handle files with space characters.
'''
 
# Copyright (C) 2009 Don Peterson
# Contact:  gmail.com@someonesdad1
 
#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#
 
from __future__ import print_function, division
import sys
import os
import getopt
import re

dbstream = sys.stderr
nl = "\n"
null = "\x00"

program_name = ""
ignore_dotted_directories = 1       # -d option turns this off
recursive = 0                       # -r option
use_nulls = 0                       # -0 option

ignore = re.compile(r"^.*\.exe$|^.*\.com$|^.*\.bat$")

# Even if we are not ignoring dotted directories, there are some
# we stil want to avoid processing.
directories_to_ignore = {
    ".svn" : 0,
    ".hg" : 0,
    ".git" : 0,
    ".bzr" : 0,
}

def Usage():
    print('''Usage:  {} [options] dir1 [dir2...]
  Prints names of all files under the indicated directories except
  for *.exe, *.com, and *.bat or if the file begins with #!.

  This is aimed at avoiding the "sea of green" on a cygwin system when
  using ls, as most non-cygwin applications write files with
  execute permissions on.

  Note:  the command line objects can be either directories or
  files.

  Example:  to turn off the execute bit on all files in the current
  directory that aren't Windows executables or shell scripts, use the
  command

    python unx.py -0 . | xargs -0 chmod -x

Options:
    -0      Append null characters after the file names.  This lets
            you use 'xargs -0' to process file names with spaces.
    -d      Include dotted (hidden) directories
    -h      Print help
    -r      Descend directories recursively
'''.format(program_name))
    exit(1)

def ProcessCommandLine():
    global program_name
    program_name = os.path.basename(sys.argv[0])
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "0cdhr")
    except getopt.error as str:
        print("getopt error:  %s" % str)
        exit(1)
    for opt in optlist:
        if opt[0] == "-0":
            global use_nulls
            use_nulls = 1
        elif opt[0] == "-d":
            global ignore_dotted_directories
            ignore_dotted_directories = 0
        elif opt[0] == "-h":
            Usage()
        elif opt[0] == "-r":
            global recursive
            recursive = 1
    if len(args) == 0:
        return (".",)
    else:
        return args

def GetFirstTwoBytes(file):
    try:
        return open(file).read(2)
    except Exception:
        return None

def IgnoreDirectory(dirpath, dir):
    if dirpath == dir:
        return 0
    basedir = os.path.basename(dirpath)
    if ignore_dotted_directories and basedir[0] == ".":
        return 1
    if basedir in directories_to_ignore:
        return 1

def ProcessDirectory(dir):
    if recursive:
        for dirpath, dirnames, files in os.walk(dir):
            if IgnoreDirectory(dirpath, dir):
                continue
            for file in files:
                ProcessFile(os.path.join(dirpath, file))
    else:
        for file in os.listdir(dir):
            if os.path.isfile(file):
                ProcessFile(file)

def ProcessObject(object):
    if os.path.isdir(object):
        ProcessDirectory(object)
    elif os.path.isfile(object):
        ProcessFile(object)
    else:
        print("'{}' is not a file or directory".format(object))

def ProcessFile(file):
    if ignore.match(file):
        return
    if GetFirstTwoBytes(file) == "#!":
        return
    file = file.replace("\\", "/")
    if use_nulls:
        sys.stdout.write(file + null)
    else:
        print(file)

if __name__ == "__main__":
    objects_to_process = ProcessCommandLine()
    for object in objects_to_process:
        ProcessObject(object)
