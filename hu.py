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

# The hash function we'll use to identify equal files.  I picked SHA-1
# because both git and Mercurial use it and it's about twice as fast
# as the SHA-2 algorithms.  It takes roughly 5 us per byte.
Hash = hashlib.sha1

nl = "\n"
py3_char = "3"
test_char = "T"
email_address = "someonesdad1@gmail.com"

# Under cygwin, the root directory's actual location is needed
on_windows = True
cygwin = "c:/cygwin" if on_windows else ""

# If a package is to be made with the -z option, this directory is where
# the packages will reside (it's separate from the repository).
package_dir = cygwin + "/home/Don/hobbyutil_packages"

# Open Office files found (need to be checked for linked pictures)
oo_files = set()

# OpenOffice extensions
oo_ext = set((".odt", ".ods"))

# Text wrapper
tw = textwrap.TextWrapper()
tw.width = int(os.environ.get("COLUMNS", 80)) - 5
tw.replace_whitespace = True
tw.fix_sentence_endings = True
tw.initial_indent = tw.subsequent_indent = " "*4

output_directories = set()

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
    '''
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

This repository is for things I've developed over the years for my various
hobbies.  Each project is a link which you can click on to get the file or
files associated with the project.  For documents, the PDF form is
typically the only file included.  If you would like the source document
(usually constructed from an Open Office document), email me and I'll send
you the source.

For python scripts, I have standardized on python 3.6 for running the
scripts.  Many of these scripts have also been tested on python 2.7, but I
am no longer making the effort to keep things running with python 2.7, as
python 3 is mature and well-supported by the needed libraries.  Where
self-tests are available, they will be python scripts that have the same
name as the script with '_test' appended.

The ./projects file in the repository is used to keep track of the things
that are in this repository.  Note there are more things in this file than
are packaged in the repository.  I do this to keep only the things that
will likely be of interest (this knowledge came from when I used to store
this stuff on Google Code and could see the download counts).  If there's
something in the projects file you'd like to have, you can email me 
at {email_address} for it.

'''.strip().format(**globals())

Trailer = '''
'''.strip()

#----------------------------------------------------------------------

def GetFileHash(file):
    '''The hex digest is returned to avoid binary bytes.

    Note:  the SHA1 output was checked against the Hash executable,
    which was compiled with the 5.6.2 version of the CryptoC++
    library, downloaded & built 23 Jun 2014 (see
    http://www.cryptopp.com/).
    '''
    h = Hash()
    h.update(open(file, "rb").read())
    return h.hexdigest()

def FilesAreDifferent(src, dest, d):
    '''Compare hashes to determine if files are different.  Return 0 if the
    hashes are the same, 1 if they are different, and 2 if the dest file
    doesn't exist.
    '''
    src = RemoveAsterisk(src)
    dest = RemoveAsterisk(dest)
    try:
        src_hash = GetFileHash(src)
    except IOError:
        Error("Can't read source file '%s':\n  " % src)
        msg += str(e)
        Error(msg)
    try:
        dest_hash = GetFileHash(dest)
    except IOError as e:
        # Can't read destination file
        return 2
    return 1 if src_hash != dest_hash else 0

def CopyFile(src, dest, d):
    '''Only copy the files if the destination file is missing or the
    source and destination are different.
    '''
    src = RemoveAsterisk(src)
    dest = RemoveAsterisk(dest)
    if src == dest:
        raise Exception("Bug:  source and destination equal")
    if os.path.isfile(dest):
        copy = FilesAreDifferent(src, dest, d)
    else:
        copy = True     # Destination file not present, so copy it
    # If the file is an Open Office document, then look for
    # its picture files and copy them too.
    ext = os.path.splitext(os.path.split(src)[1])[1]
    if ext in oo_ext:
        oo_files.add(dest)
    if copy:
        if d["show"]:
            # Only print out that the file needs copying
            print(dest)
        else:
            # Actually copy the files
            try:
                bytes = open(src, "rb").read()
                open(dest, "wb").write(bytes)
                if not d["-q"]:
                    print("%s -> %s" % (src, dest))
            except IOError as e:
                msg = "Can't copy '%s' to '%s':\n  " % (src, dest)
                msg += str(e)
                Error(msg)

def OO_PictureFiles(d):
    '''Check each file in oo_files for pictures; print out any that
    are missing (these then need to be added to the project's data).
    Note they are printed out in 'File(...)' form, allowing them to be
    inserted in this script's data verbatim.
    '''
    error = False
    Message("Checking OO picture files", c.yellow)
    for path in oo_files:
        if not os.path.isfile(path):
            Error("OO_PictureFiles():  '%s' doesn't exist" % path)
        image_files = loo.GetImages(path)  # Ignore embedded files
        # The returned container has elements of (path, state) where path
        # is relative to the OO doc's location and state is one of
        # "", "notrel", or "missing".  Print out messages about notrel
        # or missing files.
        dir, name = os.path.split(path)
        # Check each picture file
        missing = []
        for picfile, state in image_files:
            if state == "missing":
                missing.append((picfile, state))
            elif state == "notrel":
                Error("'%s' notrel in '%s'" % (picfile, path))
        if missing:
            if not error:
                print()
                c.fg(c.lred)
                print("One or more OO files missing images:")
                c.normal()
                print("\n")
            print("OO file '%s' missing images:" % path)
            for picfile, state in missing:
                print('        File("%s")' % picfile)
            error = True
    if error:
        exit(1)

def CopyFiles(project, info, d):
    '''Copy this project's files to their destinations.  Note copying
    of files is only done if necessary.
    '''
    perm = int("700", base=8)
    cat = info["subdir"]
    directory = cat + "/" + project
    if not os.path.isdir(directory):
        os.makedirs(directory, perm)
    for src, dest in info["files"]:
        srcfile = os.path.join(info["srcdir"], src)
        if not os.path.isfile(srcfile):
            msg = "For Project at %s[%d]:" % Info()
            Error("The file '%s' doesn't exist" % srcfile)
        destfile = os.path.join(directory, dest)
        # Make sure the destination directory exists
        dir, name = os.path.split(destfile)
        if not os.path.isdir(dir):
            os.makedirs(dir, perm)
        CopyFile(srcfile, destfile, d)

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
    -z      Package the indicated project(s) in args into separate zip
            containers.  These will be located in the directory indicated 
            by the global variable package_dir.
'''[1:-1]
    print(s.format(**locals()))
    exit(status)

def ParseCommandLine(d):
    d["-z"]     = False     # If True, zip indicated packages
    if len(sys.argv) < 2:
        Usage(d)
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "z")
    except getopt.GetoptError as e:
        msg, option = e
        print(msg)
        exit(1)
    for opt in optlist:
        if opt[0] == "-s":
            d["-s"] = True
    if not args:
        Usage(d)
    return args

def Message(s, fg, bg=c.black):
    c.fg(fg, bg)
    print(s)
    c.normal()

def Make(args, d):
    '''Copy each project's files to its destination if a) it isn't
    there or b) the existing destination file has a different hash
    than the source file.
    '''
    count = 0
    if d["show"]:
        Message("Files that will be updated:", c.yellow)
    else:
        Message("Updated files:", c.yellow)
    for project in data:
        if not data[project]["ignore"]:
            CopyFiles(project, data[project], d)
            count += 1
    if not d["show"]:
        MakeSoftlinks(d)
        CheckSoftlinks(d)
        OO_PictureFiles(d)
    print("\n%d projects" % count)

def List(args, d):
    '''Construct a list of the project name followed by the
    description.
    '''
    msg = "{test_char} = has self tests, {py3_char} = runs under python 3\n"
    print(msg.format(**globals()))
    count = 0
    ignored_count = 0
    keys = list(data.keys())
    keys.sort()
    for project in keys:
        item = data[project]
        if item["ignore"] is None:
            t = ""
            if item["tests"]:
                t += test_char
            if item["python3"]:
                t += py3_char
            print("%s %s" % (project, t))
            if not d["-s"]:
                s = data[project]["descr"]
                print(tw.fill(s.strip("\n")))
            count += 1
        else:
            ignored_count += 1
    print("\n%d projects" % count)
    print("%d ignored projects" % ignored_count)

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

def BuildZips(args, d):
    pass

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
        zdest = os.path.join(project_object.subdir, zname)
        zf = zipfile.ZipFile(zdest, "w")
        for SRC, DEST in file_list:
            src = os.path.join(cygwin + project_object.srcdir, SRC)
            zf.write(src, DEST)
        zf.close()

def Build(args):
    assert(args[0] == "build")
    del args[0]
    print("Building projects:")
    if args[0] == ".":
        args = data.keys()
    for project in args:
        project_object = data[project]
        if project_object.ignore:
            continue
        print(project) 
        BuildProject(project_object)
    print()

def List(d):
    pass

if __name__ == "__main__": 
    d = {} # Options dictionary
    args = ParseCommandLine(d)
    ReadProjectData(d)
    MakeDirectories(d)
    cmd = args[0] 
    if cmd == "build":
        BuildZips(args) if d["-z"] else Build(args)
    elif cmd == "list":
        List(d)
    else:
        Error("'%s' is an unrecognized command" % cmd)
