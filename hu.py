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
from textwrap import dedent
from pdb import set_trace as xx

# Copyright (C) 2014 Don Peterson
# Contact:  gmail.com@someonesdad1

#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
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

# Under cygwin, the root directory's actual location is needed
on_windows = True
cygwin = "c:/cygwin" if on_windows else ""

# If a package is to be made with the -z option, this directory is where
# the packages will reside (it's separate from the repository).
package_dir = cygwin + "/home/Don/hobbyutil_packages"

# Keep track of softlinks created
softlinks = set()

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

# data will be the repository for project information.  It is keyed on
# the project's name.
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
        "ignore" : None,                # If not None, ignore
        "descr"  : description_string,  # Defaults to None
        "todo"   : todo_string,         # Defaults to None
        "srcdir" : srcdir,              # Source directory
        "files"  : [                    # Files in package
            (filename1_src, filename1_dest),
            (filename2_src, filename2_dest),
            ...
        ],
        "softlinks" : set((
            (filename1_src, softlink1_name),
            (filename2_src, softlink2_name),
            ...
        )),
        "tests"  : False,               # True if have self tests
        "python3" : False,              # True if runs on python 3
    },
    ... etc.
}

For the files, if there's only one filename, then the source and
destination filenames are the same.

For the softlinks, the filename1_src must be of the form
cat/proj/filename, which is one of the existing (or soon to be
existing) files in the project tree.

Since the softlink's destination might not exist when the soft link is
created, a final scan is made for orphans before exiting.
'''
data = None

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

def Dump(opt):
    '''Print a listing to stdout.
    '''
    Colors = { 
        0 : {
            "name"      : c.yellow,
            "files"     : c.lmagenta,
            "softlinks" : c.lblue,
            "todo"      : c.lred,
            "srcdir"    : c.lgreen,
        },
        1 : {
            "name"      : c.gray,
            "files"     : c.gray,
            "softlinks" : c.gray,
            "todo"      : c.gray,
            "srcdir"    : c.gray,
        },
    }
    projects = list(data.keys())
    projects.sort()
    for project in projects:
        d = data[project]
        if d["ignore"] is not None and not opt["-i"]:
            continue
        if d["ignore"] is not None:
            C = Colors[1]
            c.normal(c.gray, c.black)
        else:
            C = Colors[0]
            c.normal(c.white, c.black)
        c.fg(C["name"])
        print(project, end="")
        c.normal()
        if d["ignore"] is not None:
            print("  ignored:  %s" % d["ignore"])
        else:
            print()
        keys = list(d.keys())
        keys.sort()
        for k in keys:
            if k == "files":
                c.fg(C["files"])
                print("  Files:")
                for f in d["files"]:
                    c.fg(C["files"])
                    if isinstance(f, (list, tuple)) and len(f) == 1:
                        print("    %s -> %s" % (f, f))
                    elif isinstance(f, str):
                        print("    %s -> %s" % (f, f))
                    else:
                        print("    %s -> %s" % tuple(f))
                c.normal()
            elif k == "softlinks":
                if not d[k]:
                    continue
                c.fg(C["softlinks"])
                print("  Softlinks:")
                for f in d["softlinks"]:
                    c.fg(C["softlinks"])
                    print("    %s -> %s" % tuple(f))
                c.normal()
            elif k == "descr":
                print("  %s =" % k)
                t = dedent(d[k])
                print(tw.fill(t))
                #for line in t.strip().split("\n"):
                #    print("    %s" % line)
            elif k == "todo":
                c.fg(C["todo"])
                if d[k] is not None:
                    print("  %s = %s" % (k, d[k]))
                c.normal()
            elif k == "srcdir":
                print("  srcdir = ", end="")
                c.fg(C["srcdir"])
                print(d[k])
                c.normal()
            elif k == "ignore":
                pass
            elif k in ("subdir", "python3", "tests"):
                print("  %s = %s" % (k, d[k]))
            else:
                Error("Unhandled subdir %s" % k)
                print("  %s = %s" % (k, d[k]))
        print()
    c.fg(c.white, c.black)
    print("%d total packages" % len(data))

#----------------------------------------------------------------------
# This section contains the data for the main project web page.

Header = '''
This project is a repository for things I've developed over the years
for my various hobbies. 

*Update 27 Aug 2014*:  The primary location for the files is now in
the Mercurial repository under the *Source* link above.  The
deprecated files under the *Download* link have been removed; the ones
remaining are the larger files that haven't been changed in a while
(they won't move to the repository until they're updated).

There were around 150 different projects (clumps of files) on
this site and I felt this was too many.  I've kept the popular stuff,
but removed things that weren't downloaded very often.  Now there are
roughly about half the number of projects.

To be able to get the files from the Source link, you'll need to have
Mercurial installed on your system; Mercurial is a version control
system.  If you're intimidated by needing to use some arcane piece of
software, don't be -- it's quite easy: download/install Mercurial,
then type a single command.  See the notes at the bottom of this page
for more detail.

The repository is structured with the directory naming scheme shown in
the table below.  Each project will include the source files used to
construct it and possibly a `0readme` file which will explain the
project's nature and use.  A python script will have its documentation
inside the file.  A project is a collection of one or more files.

Here are some other pages that also might be of interest:

  * Python code to talk to a Radio Shack [http://code.google.com/p/rs22812/ multimeter]
  * Python graphics [http://code.google.com/p/pygraphicsps/ library] that outputs Postscript 
  * Python code for a console-based RPN [http://code.google.com/p/hcpy/ calculator]
  * Lightweight library for typesafe numerical calculations in C++ using physical [http://code.google.com/p/unitscpp/ units]

The projects in the table below have names of the form cat/name where
cat is the subdir and name is a short name identifying the project.
The categories are:

|| elec || Electrical and electronics ||
|| eng || General engineering/technical ||
|| math || Mathematics ||
|| misc || Miscellaneous ||
|| prog || Programming ||
|| science || Science ||
|| shop || Shop-related ||
|| util || Utilities ||

The decorations after the names are:  {test_char} means a self test python
module is included; {py3_char} means the python code will run under python 3.
'''[1:].format(**globals())

Trailer = '''

==Legacy projects==

A few non-deprecated projects remain in the Downloads area because
they are relatively large files.  I won't include them in the
repository until I find the need to change them.  I have deleted the
deprecated files.  The projects are:

fountain_pen_primer_12Dec2011.pdf
    Discusses the care and feeding of fountain pens as writing tools.

DinosaurArithmetic_25Sep2012.zip
    This document discusses doing calculations without using an
    electronic calculator. It also includes a spreadsheet that
    gives the tables that were common in the math books years ago,
    as people don't use this stuff much anymore. I'm not
    advocating that we give up our calculators, but it's useful
    for a technical person to know how to reason quantitatively
    when a calculator isn't handy. This document looks at some of
    the methods for doing this.

diurnal_variations_26Jul2012.pdf 
    Shows a plot of the light from the sky measured with a cheap
    photodiode. Since inexpensive datalogging equipment can be
    purchased that use e.g. the USB interface, this would be a
    great experiment for school kids and parents to do together.
    Because it's so simple to do, I predict you'll get hooked if
    you try it.

Octopus_10Jul2012.pdf 
    If you own an oscilloscope and like to troubleshoot electrical
    things, you'll probably want to build an Octopus tester. One can
    be built from a 6.3 V RMS filament transformer and a single
    resistor, so there's no significant parts costs.  It's a handy
    troubleshooting tool.  People have been using them since the
    1930's.

BNC_connector_power_15Sep2011.pdf 
    Gives some experimental data about using RF coax cables with
    BNC connectors for DC and low-frequency power.

elements_22Sep2011.zip 
    Contains elements.pdf, a document that contains a periodic
    table of the elements, a plot of the vapor pressures of the
    elements, values of physical parameters sorted by value, and
    various physical parameters of the elements plotted as a
    function of atomic number. The raw data are contained in the
    elements.ods Open Office spreadsheet; the zip archive includes
    the python scripts used to generate the plots. If you'd like
    to generate the plots yourself, you can, as the tools are all
    open source or freely available, but be warned that there are
    numerous libraries that you'll need to get. I've wanted a
    document like this for a long time, but I knew that most of
    the work would be in manually typing in all the data from
    various places. I was right... :^)

CartPlatform_10Aug2012.pdf 
    Simple platform for a Harbor Freight garden cart.  I find it quite
    useful as a dirt repository when digging up e.g. sprinklers in the
    yard.

C_snippets_Jan2011.zip 
    This is a zip file of the C snippets code put together by Bob
    Stout; it is the Jul 1997 edition, although I downloaded it 18 Jan
    2011 from somewhere. Apparently Bob Stout died in 2008 and the
    snippets domain wasn't picked up by anyone else (the snippets.org
    now belongs to someone, but it isn't related to Stout's snippet
    collection). I thought it would be useful to make sure there was
    another cache of the Snippets collection.  While some of the code
    is only of interest to archeologists investigating primitive DOS
    cultures, there are numerous useful algorithms in there, so it's
    worth your time to take a look, as there are 416 separate C files.
    We all owe a debt of gratitude to Bob Stout for his dedication in
    writing, collecting, and collating all this stuff.

antifreeze_5Feb2012.pdf 
    How to calculate how much antifreeze to add to an existing
    partially-filled radiator to get a desired concentration.  It also
    discusses the refractometer, a tool to measure antifreeze
    concentrations and a lead-acid battery's sulfuric acid specific
    gravity (which tells you the state of charge).

AnalyticGeometry_5Sep2012.pdf 
    Contains formulas relating to analytic geometry in the
    plane and space, trigonometry, and mensuration. 

drules_16Apr2012.pdf 
    Contains some drafting rules that I've always wanted. These
    are primarily 6 inch scales both in inch and mm divisions. You
    can print them at full scale and glue them to a chunk of wood
    to make some handy scales.

Concise300_7Sep2012.pdf 
    Discusses the Concise 300, a circular slide rule still in
    production in Japan.  If you've never used a slide rule, you
    may be surprised to find that they can be good tools to help
    you with calculations accurate to roughly one percent.

inductance_06Dec2010.zip 
    Provides an Open Office spreadsheet that can calculate the
    inductance of common electrical structures.  Includes a PDF
    document describing the use and which gives references for the
    formulas used.  There is also a PDF file of the spreadsheet so
    that you can see what it looks like without having Open Office --
    this will help you decide if you want to install Open Office to be
    able to use the spreadsheet.

sine_sticks_27Jun2011.pdf 
    How to build a simple device from scrap that will measure
    angles in the shop.  Perhaps surprisingly, it can measure with
    resolution as good or better than a Starrett machinist's
    vernier protractor that costs hundreds of dollars.

help_system_12Aug2012.zip 
    If you use the vim editor, you have a convenient tool for
    accessing textual information. This package contains the tools I
    use to build a help system I've used for the past couple of
    decades (I started building this textual information in the
    1980's). Vim's ability to use "hyperlinks" in its textual help
    files is used to advantage here.  I've used these files on both
    Windows and Linux boxes.

SolarSystemScaleModel_16Sep2011.pdf 
    This document describes a python script that prints out the
    dimensions of a scaled solar system. You can use it to make a
    scale solar system in your yard or on your street. Be warned
    -- things will be smaller and farther apart than you think.
    This would be a good exercise for a parent and a child -- both
    will learn information you can't learn from a book.

nozzle_6Oct2011.pdf 
    Describes a nice hose nozzle you can make if you have a lathe.
    It will work better for cleaning things off than the typical
    store-bought nozzles.

GlendaGuard_10Aug2011.pdf 
    Describes a simple concrete sprinkler guard that my wife
    designed and built. We've used them for over 20 years and they
    work well, are simple to make, and cheap.

PartsStorageMethods_21Nov2012.pdf 
    Describes one way of storing lots of little electronic parts
    and how to find them quickly.

XmasTomatoes_24Nov2012.pdf 
    Using Christmas tree lights to keep tomato plants from
    freezing at night.

PullingFencePosts_25Jul2012.pdf 
    Using a class 2 lever can be a surprisingly effective way to
    pull fence posts out of the ground.
    
scale_27Jan2011.zip 
    The scale.pdf file contains two sheets of paper with slide
    rule type scales on them. If you duplex print this and keep it
    in a binder, you may find it useful for simple technical
    calculations when an electronic calculator isn't handy. The
    other file explains how to use things.

==Getting the source code repository==

To download the hobbyutil source code repository, you need Mercurial
installed on your system.  Mercurial is a revision control tool.  It's
easy to install and use.  To install, go to
http://mercurial.selenic.com/ and download the appropriate package.
Your installation goal is to be able to type *hg* at a console command
prompt and have the Mercurial installation respond with its default
help message, which will look something like

{{{
Mercurial Distributed SCM

basic commands:

 add           add the specified files on the next commit
 annotate      show changeset information by line for each file
    <middle lines deleted>
 summary       summarize working directory state
 update        update working directory (or switch revisions)

use "hg help" for the full list of commands or "hg -v" for details
}}}

On Windows, this usually means running an installer package.  On
UNIX-type systems, see the right-hand pane of Mercurial's download
page for common system installations.  

Once Mercurial is installed, *cd* to a directory where you'd like to
clone the hobbyutil repository and execute the command

{{{
hg clone https://code.google.com/p/hobbyutil
}}}

It will take some time to copy the information.  When completed,
you'll have a directory named *hobbyutil* that contains the source
code for the project.  

The names of the projects in the left-hand side of the table above
correspond to the directory names in the repository.

You can just use the content as-is or adapt it to your needs.  Note
that the documentation files are supplied in both Open Office source
code and associated PDF files.  Some of the packages use
reStructuredText for documentation and an associated HTML file will be
included.  See the [http://docutils.sourceforge.net/ docutils] project
for tools that can turn the reStructuredText file(s) into other
document forms.
'''
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
    update      Update the missing and out of date files for indicated
                projects (you can use 'all', but be careful and ensure that
                all need to be updated).
    active      List the projects that are active.
    inactive    List the projects that are inactive with needed fix.
    md          Construct the project listing markdown file.

Options:
    -s      Short list (no descriptions)
    -z      Package the indicated projects in args into separate zip files.
            These will be located in the directory indicated by the global 
            variable package_dir.
'''[1:-1]
    print(s.format(**locals()))
    exit(status)

def ParseCommandLine(d):
    d["-s"]     = False     # If true, no descriptions for listings
    if len(sys.argv) < 2:
        Usage(d)
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "s")
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

def MakeSoftlinks(d):
    Message("Making softlinks", c.lblue)
    for src, dest in softlinks:
        if not os.path.isfile(src):
            Error("'%s' is missing in MakeSoftlinks()" % src)
        if os.path.islink(dest):
            os.remove(dest)
        elif os.path.isfile(dest):
            Error("'%s' exists in MakeSoftlinks()" % dest)
        try:
            abs_src_dir = os.path.abspath(src)
            dest_dir, dest_file = os.path.split(dest)
            if not dest_dir:
                Error("ln -s '%s' '%s' on empty dir" % (src, dest))
            curdir = os.getcwd()
            try:
                # Remove any existing link or file
                os.remove(dest)
            except OSError:
                pass
            # Change to the destination directory so we can get a
            # relative path to the file we want to point to.
            if dest_dir:
                os.chdir(dest_dir)
            # Get the source directory relative to current directory
            relsrc = os.path.relpath(abs_src_dir)
            # Make the link
            os.symlink(relsrc, dest_file)
            if dest_dir:
                os.chdir(curdir)
            c.fg(c.lblue)
            print("  ln -s '%s' <-- '%s'" % (src, dest))
            c.normal()
        except Exception as e:
            msg = ["Couldn't make softlink '%s' --> '%s'" % (src, dest)]
            msg += ["  %s" % e]
            Error('\n'.join(msg))

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
    global data, softlinks, output_directories
    # Load information from disk
    tool, filename, mode = yaml, yamlfile, "r"
    # This reads the YAML syntax into a dictionary
    data = tool.load(open(filename, mode))
    # Check each project's entries
    for proj in data:
        item = data[proj]
        if "subdir" not in item:
            Error("'subdir' record not in %s" % proj)
        output_directories.add(item["subdir"])
        if "descr" not in item:
            Error("'descr' record not in %s" % proj)
        if "files" not in item:
            Error("'files' record not in %s" % proj)
        else:
            # Change one file items to two (allowing the one file form
            # is easier to read, takes less space, and indicates the
            # file won't be renamed).
            files = item["files"]
            for i, f in enumerate(files):
                if isinstance(f, str):
                    files[i] = [f, f]
                elif isinstance(f, list):
                    assert len(f) == 2
                else:
                    Error("'%s' unexpected in project '%s'" % (f, proj))
        if "ignore" not in item:
            item["ignore"] = None
        if "python3" not in item:
            item["python3"] = False
        if "softlinks" not in item:
            item["softlinks"] = set()
        else:
            # Add to the softlinks list
            for i in item["softlinks"]:
                softlinks.add(tuple(i))
        if "srcdir" not in item:
            Error("'srcdir' record not in %s" % proj)
        if "tests" not in item:
            item["tests"] = False
        if "todo" not in item:
            item["todo"] = None

def RemoveAsterisk(s):
    '''Remove a trailing * from a string.
    '''
    if s.endswith("*"):
        return s[:-1]
    return s

def FindMissingSourceFiles(d):
    missing_file = False
    for project in data:
        p = data[project]
        if p["ignore"]:
            continue
        printed_project_name = False
        for SRC, DEST in p["files"]:
            src = os.path.join(cygwin + p["srcdir"], RemoveAsterisk(SRC))
            if not os.path.exists(src):
                missing_file = True
                if not printed_project_name:
                    print(project)
                    printed_project_name = True
                print("   ", src, "is missing")
    if missing_file:
        exit()

def Update(d):
    pass

def Active(d):
    pass

def Inactive(d):
    pass

def Markdown(d):
    pass

def MakeDirectories(d):
    '''If any directory in output_directories is not present, construct it.
    '''
    for dir in output_directories:
        if not os.path.isdir(dir):
            os.mkdir(dir)

if __name__ == "__main__": 
    d = {} # Options dictionary
    args = ParseCommandLine(d)
    ReadProjectData(d)
    MakeDirectories(d)
    FindMissingSourceFiles(d)
    cmd = args[0] 
    if cmd == "update":
        Update(d)
    elif cmd == "active":
        Active(d)
    elif cmd == "inactive":
        Inactive(d)
    elif cmd == "md":
        Markdown(d)
    else:
        Error("'%s' is an unrecognized command" % cmd)
