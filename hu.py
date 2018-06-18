'''

This script will copy files from various locations in my data
directories to the hobbyutil repository.  The projects file is a yaml
datafile that defines the "projects" and the files that make it up.
This script is intended to run under python 3.6.

The primary behavior is to populate the repository with the project's PDF
file or python file.  If more than one file is in the project, then a
zipfile is created.

To keep the repository a reasonable size, I've decided that only the PDF
file is included by default.  There will occasionally be people who want
the original source files; the command line option -z can be used to create
a zipfile containing the source files that can be emailed to the interested
person.

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

# Pickling vs. use of YAML
need_to_pickle = False
yamlfile = "projects"   # Where YAML data are saved (never written)
picklefile = yamlfile + ".pickle"  # Pickled data for speed

# data will be the repository for project information.  It is keyed on
# the project's name.
'''

This is the key data structure of the script; it's an ordered
dictionary so that the entry order can be preserved.

A key must be a string with at least one letter on either side of a
'/' character:  cat/proj.  cat is the top-level category of the hu web
page (e.g., elec, math, etc.) and proj is the package name.  The
current implementation only uses the cat/proj form, but cat/proj/other
and deeper structures can be used if desired.

Each value in the dictionary is another dictionary, such as:

{
    "proj" : {
        "category" : "cat",             # 'elec', 'math', etc.
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
            elif k in ("category", "python3", "tests"):
                print("  %s = %s" % (k, d[k]))
            else:
                Error("Unhandled category %s" % k)
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
cat is the category and name is a short name identifying the project.
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
    # Compare hashes to determine if files are different
    try:
        src_hash = GetFileHash(src)
    except IOError:
        Error("Can't read file '%s':\n  " % src)
        msg += str(e)
        Error(msg)
    try:
        dest_hash = GetFileHash(dest)
    except IOError as e:
        msg = "Can't read file '%s':\n  " % dest
        msg += str(e)
        Error(msg)
    return True if src_hash != dest_hash else False

def CopyFile(src, dest, d):
    '''Only copy the files if the destination file is missing or the
    source and destination are different.
    '''
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
    cat = info["category"]
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
Usage:  {name} [options] command
  Utility to build, erase, etc. the hobbyutil repository.

Commands:
    scan        Identify missing and out of date files.
    update      Update the missing and out of date files.
    active      List the projects that are active.
    inactive    List the projects that are inactive with needed fix.
    md          Construct the project listing markdown file with its links.

Options:
    -s      Short list (no descriptions)
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

if 0:
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
                # Change to the destination diretory so we can get a
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

def PrintProjectDescription(category, project, item, d):
    '''Print the Google wiki form of a table as:
        || category/project || description ||
    '''
    if item["ignore"]:
        return
    s, t = item["descr"].strip(), ""
    if item["tests"]:
        t += test_char
    if item["python3"]:
        t += py3_char
    print("|| %s/%s %s || %s ||" % (category, project, t, s))

if 0:
    def Web(args, d):
        '''Output the main project web page to stdout.
        '''
        # Make a new dictionary using categories as the first
        # keys and project name as the second.
        info = {}
        for proj in data:
            category = data[proj]["category"]
            if category not in info:
                info[category] = {}
            else:
                info[category][proj] = data[proj]
        print(Header)
        categories = list(info.keys())
        categories.sort()
        for category in categories:
            projects = list(info[category].keys())
            projects.sort()
            for project in projects:
                item = info[category][project]
                PrintProjectDescription(category, project, item, d)
        print(Trailer)

    def EraseFiles(project, info, d):
        '''Erase this project's destination files.
        project is project's name like 'elec/bnc'.
        info is d["data"][project].
        '''
        d["top_level_dirs"].add(os.path.split(project)[0])
        if d["-F"]:
            # Force removal of directory and all files, even those that
            # were not copied by this script.
            shutil.rmtree(project, ignore_errors=True)
            return
        subdirs = set()  # Keep track of subdirectories
        for src, dest in info["files"]:
            destfile = os.path.join(project, dest)
            try:
                subdirs.add(os.path.split(destfile)[0])
                if os.path.isfile(destfile):
                    os.remove(destfile)
                    if not d["-q"]:
                        print("Removed %s" % destfile)
            except Exception:
                c.fg(c.lred)
                print("Couldn't remove '%s'" % destfile)
                c.normal()
        # Remove subdirectories
        for subdir in subdirs:
            try:
                os.rmdir(subdir)
                if not d["-q"]:
                    print("Removed directory %s" % subdir)
            except Exception:
                if os.path.isdir(subdir):
                    print("Couldn't remove directory %s" % subdir)
        # All files erased, now remove project directory.  An exception
        # means the directory probably isn't empty.
        try:
            os.rmdir(project)
            if not d["-q"]:
                print("Removed directory %s" % project)
        except Exception:
            if os.path.isdir(project):
                print("Couldn't remove directory %s" % project)

    def CheckSoftlinks(d):
        Message("Checking softlinks", c.yellow)
        for src, dest in softlinks:
            src_hash = GetFileHash(src)
            dest_hash = GetFileHash(dest)
            if src_hash != dest_hash:
                print("Bad softlink:  '%s' to '%s'" % (dest, src))

    def Duplicates(args, d):
        '''Find the files that are duplicates in the packages and print
        them out.
        '''
        raise Exception("Not impl")

    def Outlaw(args, d):
        '''Show files in repository that are not part of defined data.
        '''
        ignore = set((
            ".vi",   
            ".z",   
            "0readme",   
            "0readme.html",   
            "a",   
            "history.rst",   
            "hu.py",   
            "makefile",   
            "mk.clean",   
            "tags",   
            "z",   
        ))
        # Get a list of files that are in the directory; use the 'find'
        # command.
        p = subprocess.PIPE
        s = subprocess.Popen(('/usr/bin/find', ".", "-type", "f"), 
                             stdout=p, stderr=p)
        on_disk_files = set()
        for name in s.stdout.readlines():
            if name.startswith("./"):
                name = name[2:]
            name = name.rstrip()
            if (name.startswith(".hg") or 
                name.startswith("doc/") or 
                name in ignore):
                continue
            if name.endswith(".swp"):
                continue
            on_disk_files.add(name)
        # Find project files that are not in the set of found files
        projects = list(data.keys())
        projects.sort()
        for project in projects:
            info = data[project]
            for src, dest in info["files"]:
                f = os.path.join(project, dest)
                on_disk_files.discard(f)
        if on_disk_files:
            print("Outlaw files:")
            for f in on_disk_files:
                print("  ", f)
        else:
            print("No outlaw files found")

    def Ignored(args, d):
        '''Show ignored projects with their ignore string.
        '''
        print("Ignored projects:")
        for project in data.keys():
            s = data[project]["ignore"]
            if s is not None:
                print("  %-20s  %s" % (project, s))

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

def UpdateData(d):
    '''Get data and update it to ensure all records are present.  The
    strategy is to use YAML for the input data, but only parse it when
    it has changed.  This is done by using a secondary data file in
    pickle format.  The pickled file is used if its timestamp is later
    than the YAML file; otherwise, the YAML file is used.
    '''
    global data, softlinks, need_to_pickle
    # Load information from disk
    tool, filename, mode = yaml, yamlfile, "r"
    if 0:  # Don't bother with pickling
        if os.path.isfile(picklefile):
            stp, sty = os.stat(picklefile), os.stat(yamlfile)
            if stp.st_mtime >= sty.st_mtime:
                tool, filename = pickle, picklefile
                mode += "b"
            else:
                need_to_pickle = True
        else:
            need_to_pickle = True
    data = tool.load(open(filename, mode))
    # Check each project's entries
    for proj in data:
        item = data[proj]
        if "category" not in item:
            Error("'category' record not in %s" % proj)
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

if 0:
    def Pickle(d):
        '''Save the key data structure to a pickled data file.  This is
        done for performance, as loading pickled data is about 500 times
        faster than YAML information.
        '''
        pickle.dump(data, open(picklefile, "wb"))

def Scan(d):
    for project in data:
        print(project, ' '.join(data[project].keys()))
        print()

def Update(d):
    pass

def Active(d):
    pass

def Inactive(d):
    pass

def Markdown(d):
    pass

if __name__ == "__main__": 
    d = {} # Options dictionary
    args = ParseCommandLine(d)
    UpdateData(d)
    cmd = args[0] 
    if cmd == "scan":
        Scan(d)
    elif cmd == "update":
        Update(d)
    elif cmd == "active":
        Active(d)
    elif cmd == "inactive":
        Inactive(d)
    elif cmd == "md":
        Markdown(d)
    #elif cmd == "docs":
    #    Docs(args, d)
    #elif cmd == "dump":
    #    Dump(d)
    #elif cmd == "dup":
    #    Duplicates(args, d)
    #elif cmd == "ignored":
    #    Ignored(args, d)
    #elif cmd == "list":
    #    List(args, d)
    #elif cmd == "outlaw":
    #    Outlaw(args, d)
    #elif cmd == "show":
    #    d["show"] = True
    #    Make(args, d)
    #elif cmd == "stats":
    #    Stats(args, d)
    #elif cmd == "make":
    #    d["show"] = False
    #    Make(args, d)
    #elif cmd == "web":
    #    Web(args, d)
    else:
        Error("'%s' is an unrecognized command" % cmd)
    #Pickle(d)
