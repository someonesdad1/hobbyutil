'''

This script is used to populate a repository with the files that I want to
archive.  The relevant file information is in a text file that uses YAML
syntax to describe the files, their source and destination names, and their
containers.

The first task is to verify all the source files exist on the hard disk.
Then the script will identify missing or out-of-date destination files.
The destination files will typically be a single PDF document or e.g. a
collection of scripts and a PDF.  The PDF files are typically made from an
Open Office document along with optional bitmap files, but these are not
copied to the repository for space reasons.  A user can ask to have the
source files and the -z option can be used to put the source files into a
zip file so they can be emailed to the user.

'''

from __future__ import print_function
from collections import defaultdict
from columnize import Columnize
import color as c
import getopt
import hashlib
import loo
import os
import pickle
import shutil
import subprocess
import sys
import textwrap
import traceback as TB
import yaml
import zipfile
from textwrap import dedent
from pdb import set_trace as xx

# Copyright (C) 2014 Don Peterson
# Contact:  gmail.com@someonesdad1

#
# Licensed under the Apache License, Version 2.0 (the "License"); you
# may not use this file except in compliance with the License.  You may
# obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.  See the License for the specific language governing
# permissions and limitations under the License.
#
if 0:
    import debug
    debug.SetDebugger()

nl = "\n"
email_address = "someonesdad1@gmail.com"

# Under cygwin, the root directory's actual location is needed
on_windows = True
cygwin = "c:/cygwin" if on_windows else ""

# If a package is to be made with the -z option, this directory is where
# the packages will reside (it's separate from the repository).
package_dir = cygwin + "/home/Don/hobbyutil_packages"

# Text wrapper
tw = textwrap.TextWrapper()
tw.width = int(os.environ.get("COLUMNS", 80)) - 5
tw.replace_whitespace = True
tw.fix_sentence_endings = True
tw.initial_indent = tw.subsequent_indent = " "*4

# Names of the output directories
output_directories = set()

# Name of the project list markdown file
project_list = "project_list.md"

# Map output directories to more meaningful names
output_directories_map = {
    "elec": "Electrical",
    "eng": "Engineering",
    "math": "Math",
    "misc": "Miscellaneous",
    "prog": "Programming",
    "science": "Science",
    "shop": "Shop",
    "util": "Utilities",
}

# YAML data
yamlfile = "projects"   # Where YAML data are saved (never written)

# data will be the repository for project information.  It is a dictionary
# keyed on the project's name.

'''

This is the key data structure of the script; it's an ordered
dictionary so that the entry order can be preserved.

A key must be a string with at least one letter on either side of a
'/' character:  cat/proj.  cat is the top-level subdir of the hu web
page (e.g., elec, math, etc.) and proj is the package name.  The
current implementation only uses the cat/proj form, but cat/proj/other
and deeper structures can be used if desired.

Each value in the dictionary is another dictionary, such as:

{
    "proj" : {
        "subdir" : "cat",             # 'elec', 'math', etc.
        "ignore" : None,                # If not None, ignore this project
        "descr"  : description_string,  # Defaults to None
        "todo"   : todo_string,         # Defaults to None
        "srcdir" : srcdir,              # Source directory
        "files"  : [                    # Files in package
            (filename1_src, filename1_dest),
            (filename2_src, filename2_dest),
            ...
        ],
    },
    ... etc.
}

For the files, if there's only one filename, then the source and
destination filenames are the same.
'''
data = None

class Project(object):
    '''Contain the project's information and provide the requisite
    packaging.  The object's attributes are:

    name        Short name of project
    subdir      Which subdirectory will contain the file(s)
    descr       Description of project
    files       [src, dest] pairs of the project's files
    srcdir      Where the source files reside
    ignore      If not None, the reason this file isn't built

    The class variable projects is a dictionary keyed by each subdir name
    (such as 'math', 'shop', etc.); each key's value is a list of the
    project files that can be linked to in the web page.
    '''
    projects = defaultdict(list)

    def __init__(self, name, project_data_dict):
        self.name = name
        self.data = project_data_dict
        if "ignore" not in self.data:
            self.data["ignore"] = None
        self.validate_data()
    def validate_data(self):
        for key in "subdir descr files srcdir ignore".split():
            if key not in self.data:
                Error("{} data missing key {}".format(self.name, key))
        # Make data attributes
        self.subdir = self.data["subdir"]
        self.descr = self.data["descr"]
        self.files = self.data["files"]
        self.srcdir = self.data["srcdir"]
        self.ignore = self.data["ignore"]
        if self.ignore:
            return
        # Make sure all source files exist and can be read
        srcdir = self.data["srcdir"]
        for SRC, DEST in self.files:
            src = os.path.join(cygwin + srcdir, RemoveAsterisk(SRC))
            if not os.path.isfile(src):
                Error("'{}' doesn't exist".format(src))
            try:
                open(src, "rb").read()
            except Exception:
                Error("'{}' can't be read".format(src))

def Error(msg, status=1):
    c.fg(c.lred)
    print(msg)
    c.normal()
    exit(status)

def Info(back=3):
    '''Return file name and line number of where caller called us.
    You may have to change the stack index back to get the required
    stack frame.
    '''
    stack = TB.extract_stack()[-back:][0]
    return stack[:2]

#----------------------------------------------------------------------
# This section contains the data for the main project web page.

Header = '''

[Home](./README.md)

Click on the links to download a project's file(s).

'''.strip().format(**globals())

#----------------------------------------------------------------------

def Usage(d, status=1):
    name = sys.argv[0]
    s = '''
Usage:  {name} [options] command [args]
  Utility to build the hobbyutil repository's contents.

Commands:
    build       Copy the relevant files to their directories and construct
                the zip files.  Also make the markdown file containing the
                descriptions.  You can specify which projects in args or
                use '.' to build everything.
    list        List active and inactive projects.

Options:
    -i      Ignore the ignore flag in the projects file.  This can be used
            to find missing project files.
    -z      Package the indicated project(s) in args into separate zip
            containers.  These will be located in the directory indicated
            by the global variable package_dir.
'''[1:-1]
    print(s.format(**locals()))
    exit(status)

def ParseCommandLine(d):
    d["-i"]     = False     # If True, zip even if ignored
    d["-z"]     = False     # If True, zip indicated packages
    if len(sys.argv) < 2:
        Usage(d)
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "iz")
    except getopt.GetoptError as e:
        msg, option = e
        print(msg)
        exit(1)
    for opt in optlist:
        if opt[0] == "-i":
            d["-i"] = True
        elif opt[0] == "-z":
            d["-z"] = True
    if not args:
        Usage(d)
    return args

def Message(s, fg, bg=c.black):
    c.fg(fg, bg)
    print(s)
    c.normal()

def ReadProjectData(d):
    '''Get data and update it to ensure all records are present.  The
    input data is in YAML format.
    '''
    global data, output_directories
    # Load information from disk
    tool, filename, mode = yaml, yamlfile, "r"
    # This reads the YAML syntax into a dictionary
    data = tool.load(open(filename, mode))
    # Check each project's entries
    for project in data:
        project_data = data[project]
        if "files" not in project_data:
            Error("'files' record not in {}".format(project))
        # Change one file items to two (allowing the one file form
        # is easier to read, takes less space, and indicates the
        # file won't be renamed).
        files = project_data["files"]
        for i, f in enumerate(files):
            if isinstance(f, str):
                files[i] = [f, f]
            elif isinstance(f, list):
                assert len(f) == 2
            else:
                Error("'{}' unexpected in project '{}'" % (f, proj))
        project_data["files"] = files
        output_directories.add(project_data["subdir"])
        data[project] = Project(project, project_data)

def RemoveAsterisk(s):
    '''Remove a trailing * from a string.
    '''
    if s.endswith("*"):
        return s[:-1]
    return s

def MakeDirectories(d):
    '''If any directory in output_directories is not present, construct it.
    '''
    for dir in output_directories:
        if not os.path.isdir(dir):
            os.mkdir(dir)

def BuildProject(project_object):
    # Make a list of the files without an ending asterisk in name
    file_list = []
    for src, dest in project_object.files:
        if not src.endswith("*"):
            file_list.append((src, dest))
    assert(file_list)
    if len(file_list) == 1:
        # Copy the single file.  Assumes we are in the root of the
        # repository.
        src = os.path.join(cygwin + project_object.srcdir, file_list[0][0])
        dest = os.path.join(project_object.subdir, file_list[0][1])
        shutil.copyfile(src, dest)
    else:
        # Construct a zipfile of these files
        zname = project_object.name + ".zip"
        dest = os.path.join(project_object.subdir, zname)
        zf = zipfile.ZipFile(dest, "w")
        for SRC, DEST in file_list:
            src = os.path.join(cygwin + project_object.srcdir, SRC)
            zf.write(src, DEST)
        zf.close()
    # Update the Project.projects class variable
    entry = (dest, project_object.descr)
    Project.projects[project_object.subdir].append(entry)

def List(d):
    '''List active and inactive projects.
    '''
    active, inactive = [], []
    for project in data:
        if data[project].ignore:
            inactive.append(project)
        else:
            active.append(project)
    w = 80
    s = "{} Inactive projects".format(len(inactive))
    print("{:^{}s}".format(s, w))
    print("{:^{}s}".format("-"*len(s), w))
    for i in Columnize(inactive):
        print(i)
    print()
    s = "{} Active projects".format(len(active))
    print("{:^{}s}".format(s, w))
    print("{:^{}s}".format("-"*len(s), w))
    for i in Columnize(active):
        print(i)

def BuildProjectZip(project_object):
    # Make a list of all the files without an ending asterisk in name
    files = []
    for src, dest in project_object.files:
        files.append((RemoveAsterisk(src), RemoveAsterisk(dest)))
    assert(files)
    # Construct a zipfile of these files
    zname = project_object.name + ".zip"
    dest = os.path.join(package_dir, zname)
    zf = zipfile.ZipFile(dest, "w")
    for SRC, DEST in files:
        src = os.path.join(cygwin + project_object.srcdir, SRC)
        zf.write(src, DEST)
    zf.close()

def Build(projects, d):
    print("Building projects:")
    if projects[0] == ".":
        projects = data.keys()
    for project in projects:
        project_object = data[project]
        if project_object.ignore and not d["-i"]:
            continue
        print(project)
        BuildProject(project_object)
    print()
    # Now build the project list markdown page
    pl = open(project_list, "w")
    pl.write(Header + nl)
    for project in Project.projects:
        pl.write(nl + "## " + output_directories_map[project] + nl + nl)
        # Start a table
        pl.write('''Link | Description
--- | ---
''')
        for name, descr in Project.projects[project]:
            link = "[{}]({})".format(name, name)
            pl.write("{} | {}\n".format(link, descr))
    pl.close()

def BuildZips(projects, d):
    '''Construct zipfiles of the indicated projects.
    '''
    print("Building project zipfiles:")
    if projects[0] == ".":
        projects = data.keys()
    for project in projects:
        project_object = data[project]
        if project_object.ignore and not d["-i"]:
            print("{}'{}' is ignored".format(" "*20, project))
            continue
        print(project)
        BuildProjectZip(project_object)

if __name__ == "__main__":
    d = {} # Options dictionary
    args = ParseCommandLine(d)
    ReadProjectData(d)
    MakeDirectories(d)
    cmd = args[0]
    del args[0]
    if cmd == "build":
        if not args:
            Usage(d)
        BuildZips(args, d) if d["-z"] else Build(args, d)
    elif cmd == "list":
        List(d)
    else:
        Error("'%s' is an unrecognized command" % cmd)
