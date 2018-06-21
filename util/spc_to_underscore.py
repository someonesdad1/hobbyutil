# Copyright (C) 2014 Don Peterson
# Contact:  gmail.com@someonesdad1
 
#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#
import sys
import os
import glob
import getopt

def Usage():
    name = sys.argv[0]
    print('''Usage:  {name} [options] dir1 [dir2...]
  Replace spaces in filenames with underscores.  Note this tool operates on
  whole directories.  Run the script to see what will happen, then use the
  -x option to actually perform the renaming.

Options
    -e      Process directory names too.
    -r      Act recursively.
    -u      Change underscores to spaces.
    -x      Perform the renaming.
'''[:-1].format(**locals()))
    exit(2)

def ParseCommandLine(d):
    d["-d"] = False     # Process directory names too
    d["-r"] = False     # Act recursively
    d["-u"] = False     # Change underscores to spaces
    d["-x"] = False     # Execute
    if len(sys.argv) < 2:
        Usage()
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "drux")
    except getopt.error as str:
        print(str)
        sys.exit(1)
    for opt in optlist:
        if opt[0] == "-d":
            d["-d"] = True
        elif opt[0] == "-r":
            d["-r"] = True
        elif opt[0] == "-u":
            d["-u"] = True
        elif opt[0] == "-x":
            d["-x"] = True
    if len(args) < 1:
        Usage()
    return args

def ProcessFile(root, file, d):
    if root is ".":
        root = ""
    oldfile = os.path.join(root, file)
    if d["-u"]:
        if us not in file:
            return
        newfile = os.path.join(root, file.replace(us, sp))
    else:
        if sp not in file:
            return
        newfile = os.path.join(root, file.replace(sp, us))
        assert sp not in newfile
    if d["-x"]:
        try:
            os.rename(oldfile, newfile)
        except Exception:
            print("Couldn't rename '%s' to '%s'; continuing" %
                  (oldfile, newfile))
    else:
        print(oldfile.replace("\\", "/"), "-->", newfile.replace("\\", "/"))

def ProcessDirectory(dir, d):
    if dir is not ".":
        head, tail = os.path.split(dir)
        if not tail:
            if sp in head:
                head = head.replace(" ", "_")
        else:
            if sp in tail:
                tail = tail.replace(" ", "_")
        newdir = os.path.join(head, tail)
        if d["-x"]:
            try:
                os.rename(dir, newdir)
            except Exception:
                print("Couldn't rename '%s' to '%s'; continuing" %
                      (dir, newdir))
        else:
            print(dir.replace("\\", "/"), "-->", newdir.replace("\\", "/"))
    if d["-r"]:
        for root, dirs, files in os.walk(dir):
            if root not in d["visited_directories"]:
                d["visited_directories"].add(root)
                ProcessDirectory(root, d)
            for file in files:
                ProcessFile(root, file, d)
    else:
        dirglob = os.path.join(dir, "*")
        for file in glob.glob(dirglob):
            if os.path.isfile(file):
                ProcessFile(dir, file, d)

if __name__ == "__main__":
    show = 0   # Show what will be done
    sp, us = " ", "_"
    d = {"visited_directories" : set()}
    for dir in ParseCommandLine(d):
        ProcessDirectory(dir, d)
