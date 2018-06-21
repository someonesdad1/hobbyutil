from __future__ import division, print_function
__doc__ = '''
{name} [options] mode [mode_options]
  Manipulate PDF files.

  The modes are:
    cat
    delete
    info
    merge
    rotate
    select
    split
    watermark

Installation
------------

    Copy the {name} file to a directory in your PYTHONPATH.  Your
    python installation's Lib/site-packages directory might be a good
    choice.

    You'll also need the pyPdf module (see [1] below).

Mode details
------------

cat input_file1.pdf [input_file2.pdf ...] output_file.pdf

    Concatenates the pages from the indicated input files into one
    larger PDF file.

delete file.pdf sel1 [sel2...] output_file.pdf

    Acts the same as select, but chooses the pages from the
    complementary set.

info input_file1.pdf [input_file2.pdf ...]

    Print the document info for each input file to stdout.

merge input_file1.pdf [input_file2.pdf ...] output_file.pdf

    Merges the indicated pages into a single-page output file.
    The input files will typically be single-page files, but they
    don't have to be.

rotate angle input_file1.pdf [input_file2.pdf ...] output_file.pdf

    Rotate each page in the input files by the indicated angle and
    concatenate them into the output file.  The angle parameter is a
    case-insensitive string that must be 'L', 'R', or 'U'.  'L' means
    to rotate the pages to the left by a right angle, 'R' means to
    rotate the pages to the right by a right angle, and 'U' means to
    rotate the pages by 180 degrees.

select file.pdf sel1 [sel2...] output_file.pdf

    Choose particular pages or ranges of pages from file.pdf and
    write them to output_file.pdf.  sel1, sel2, ... are selections
    which are either single page numbers or two page numbers
    separated by a hyphen.  Page numbering starts with 1.  You may
    use abbreviated selections like 2- or -2.  The other implied
    limit is either the last page in the file or the first page,
    respectively.  If the ending number is smaller than the starting
    number, then the pages are put into the output file in reverse
    order.  For example, 4-3 means the input file's pages 4 is put
    into the output file followed by page 3.

split prefix file1.pdf [file2.pdf ...]

    Splits the indicated PDF files into PDF files with one page
    each.  prefix is a string that will be the prefix of the
    output file names.  If the prefix is "yy" and there are three
    pages in the input PDF file(s), then the output files will be
    yy_0.pdf, yy_1.pdf, and yy_2.pdf.

watermark input_file.pdf watermark_file.pdf output_file.pdf

    Adds the indicated watermark to each page in the input file.
    The first page of the watermark file is used as the watermark
    unless the -w option is used.

Notes
-----

* The {name} script doesn't support passwords in the input PDF files.
  While this wouldn't be hard to add, I left it out because I
  essentially never come across password-encrypted PDF files.

* Merging and watermarking are operations that can take a lot of time.
  You can use the -d option to cause a sentinel character to be
  printed after each page is read.

Options
-------

-d
    Prints a '.' to stdout for each page processed.  The intent is for
    merging and watermarking tasks, as they can take a long time and
    make you suspect the program is hung.

-n num
    For the split command, you can specify the number to start
    numbering at (defaults to 1).

-o
    Overwrite the output file if it is present.  Normally, {name}
    will exit if the output file exists.

-w page_num
    Specifies which page in the watermark file to use as the
    watermark page.

References
----------

[1]
    To use this script, you'll need to download and install the pyPdf
    module from http://pybrary.net/pyPdf/.  I developed the pdf script
    with version 0.13 of pyPdf (and python version 2.6.5 in April of
    2012).  Decompress pyPdf's files somewhere, then type 'python
    setup.py install'; this will install the package in your python
    installation's Lib/site-packages directory.  Thanks to Mathieu
    Fenniak for a nice tool.

[2]
    This script was inspired by the stapler.py script from Philip
    Stark, version 0.2:  https://github.com/hellerbarde/stapler.
'''.strip()

# Copyright (C) 2012 Don Peterson
# Contact:  gmail.com@someonesdad1

#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#

from pyPdf import PdfFileWriter, PdfFileReader
from math import log10, ceil
import sys
import os
import getopt
import re

err = sys.stderr
class Bug(Exception):
    pass

# Regular expression to recognize valid selection strings
selection_re = re.compile(r'''
    (^\d+-\d*$)     # 1 or more digits, -, 0 or more digits (n- or n-m)
    |               # or
    (^-\d+$)        # -, 1 or more digits (-m only form)
    |               # or
    (^\d+$)         # One or more digits (n form)
''', re.X)

def out(*v, **kw):
    sep = kw.setdefault("sep", " ")
    nl = kw.setdefault("nl", True)
    stream = kw.setdefault("stream", sys.stdout)
    stream.write(sep.join([str(i) for i in v]))
    if nl:
        stream.write("\n")

def Error(msg):
    out(msg, stream=err)
    exit(1)

def PrintManual():
    name = os.path.split(sys.argv[0])[1]
    out(__doc__.format(**locals()))
    sys.exit(0)

def Usage(status=1):
    name = os.path.split(sys.argv[0])[1]
    msg = '''
Usage:  {name} [options] mode mode_options
  Manipulate PDF files.  Use -h to get a man page.  The modes are:

  cat in1.pdf [in2.pdf ...] out.pdf
  delete in.pdf sel1 [sel2...] out.pdf
  info in1.pdf [in2.pdf ...]
  merge in1.pdf [in2.pdf ...] out.pdf
  rotate [L|R|U] in1.pdf [in2.pdf ...] out.pdf
  select in.pdf sel1 [sel2...] out.pdf
  split prefix in1.pdf [in2.pdf ...]
  watermark in.pdf watermark_file.pdf out.pdf

  sel is a selection denoted by page numbers.  It is either a single
  integer or a range of pages indicated by n-m.
'''.strip()
    out(msg.format(**locals()))
    exit(status)

def ParseCommandLine(d):
    d["-d"] = False     # Print processing sentinels
    d["-h"] = False     # Print the manual
    d["-n"] = 1         # Number to start numbering at for split
    d["-o"] = False     # Overwrite output file?
    d["-w"] = 0         # Page in watermark file to use
    d["allowed"] = (    # Allowed modes
        "cat",
        "delete",
        "info",
        "merge",
        "rotate",
        "select",
        "split",
        "watermark",
    )
    d["n"] = os.path.split(sys.argv[0])[1] + ":  "
    if len(sys.argv) < 2:
        Usage()
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "de:hn:otw:")
    except getopt.GetoptError as str:
        msg, option = str
        Error(msg)
    for opt in optlist:
        if opt[0] == "-d":
            d["-d"] = True
        if opt[0] == "-e":
            d["-e"] = opt[1]
        if opt[0] == "-h":
            PrintManual()
        if opt[0] == "-n":
            d["-n"] = int(opt[1])
        if opt[0] == "-o":
            d["-o"] = True
        if opt[0] == "-w":
            d["-w"] = int(opt[1])
            if d["-w"] < 1:
                Error(d["n"] + "-w option needs a page number > 0", stream=err)
    if len(args) < 1:
        Usage()
    return args

def CheckMode(mode, d):
    mode = mode.lower()
    found = []
    for i in d["allowed"]:
        loc = i.find(mode)
        if loc == 0:
            found.append(i)
    if not found:
        Error("Mode '%s' not recognized" % mode)
    elif len(found) == 1:
        d["mode"] = found[0]
        return found[0]
    else:
        s = str(found)[1:-1].replace("'", "")
        Error(d["n"] + "ambiguous mode on command line; could be:\n  " + s,
              stream=err)

def GetPageSet(selections, pages, complement=False):
    '''Return a tuple of the pages indicated by the strings in the
    sequence selections.  pages is the number of pages in the
    document.  If complement is True, return the complement of the
    set.  The numbers in the selections are 1-based, but we will
    return 0-based numbers.
 
    Selection strings are of the forms
        3       Indicates just page 3.
        3-      Page 3 to the last page of the file.
        -3      First page to page 3.
        1-3     Pages 1 to 3, inclusive.
        3-1     Pages 3 to 1, inclusive (reverses order).
 
    Example:  if selections was ["1-3", "3-2", "4-"] and there were 5
    pages in the document, the returned tuple would be
        (0, 1, 2, 2, 1, 3, 4).
 
    If complement is True, we generate a set of the integers from 0 to
    (pages - 1), then remove any pages in the tuple.
 
    Note:  a bad selection spec results in a ValueError exception
    (this allows test code to test this function).
    '''
    s = []
    for item in selections:
        item = item.strip().replace(" ", "")
        msg = "'%s' is a bad page selection" % item
        mo = selection_re.match(item)
        if not mo:
            raise ValueError("'%s' selection not recognized" % item)
        # The non-None group in the match object mo tells us the type
        # of selection spec.
        if mo.groups()[0] is not None:
            # It's of the n- or n-m form
            m = pages - 1
            fields = mo.groups()[0].split("-")
            if not fields[1]:
                # n- form
                n = int(fields[0]) - 1
            elif len(fields) == 2:
                # n-m form
                n = int(fields[0]) - 1
                m = int(fields[1]) - 1
            else:
                raise Bug("Bug 1 in GetPageSet")
            assert isinstance(n, int) and isinstance(m, int)
            if not(0 <= n < pages) or not(0 <= m < pages):
                raise ValueError(msg)
            if n < m:
                # Generate in normal order
                for i in range(n, m + 1):
                    s.append(i)
            elif n == m:
                # Same as single number
                s.append(n)
            else:
                # n > m means generate in reverse order
                for i in range(n, m - 1, -1):
                    s.append(i)
        elif mo.groups()[1] is not None:
            # It's of the -m form
            for i in range(int(mo.groups()[1][1:])):
                if i >= pages:
                    raise ValueError(msg)
                s.append(i)
        elif mo.groups()[2] is not None:
            # It's a single integer
            n = int(mo.groups()[2]) - 1
            if not(0 <= n < pages):
                raise ValueError(msg)
            s.append(int(mo.groups()[2]) - 1)
        else:
            raise Bug("Bug 2 in GetPageSet")
    if complement:
        # Create the complementary set c by removing any page numbers
        # in s from all the allowed page numbers.
        s, c = set(s), range(pages)
        for i in set(s):
            try:
                c.remove(i)
            except ValueError:
                # It's a bug, as s should only contain page numbers
                # from 0 to pages - 1.
                raise Bug("Bug 3 in GetPageSet")
        s = c
    # Check our work
    if s:
        assert max(s) < pages
        assert min(s) >= 0
    else:
        raise Bug("Bug 4 in GetPageSet")
    return tuple(s)

def GetOutputWriter(filename, d):
    '''Return a PdfFileWriter object that will write to the indicated
    file.  An error will occur if the file already exists unless the
    -o option was used.
    '''
    if os.path.exists(filename) and not d["-o"]:
        Error("'%s' already exists" % filename)
    return PdfFileWriter()

def Sentinel(d):
    '''Print a sentinel character.
    '''
    if d["-d"]:
        out(".", nl=False, sep="")

def Info(d):
    args = d["args"]
    if len(args) < 1:
        Error("info needs at least one argument")
    fmt = "  %-9s = %s"
    for filename in args:
        input = PdfFileReader(open(filename, "rb"))
        info = input.getDocumentInfo()
        s = []
        if info.title is not None:
            s.append(fmt % ("Title", info.title))
        if info.subject is not None:
            s.append(fmt % ("Subject", info.subject))
        if info.producer is not None:
            s.append(fmt % ("Producer", info.producer))
        if info.creator is not None:
            s.append(fmt % ("Creator", info.creator))
        if info.author is not None:
            s.append(fmt % ("Author", info.author))
        s.append(fmt % ("Pages", str(input.getNumPages())))
        e = "yes" if input.isEncrypted else "no"
        s.append(fmt % ("Encrypted", e))
        out(filename)
        out("\n".join(s))

def Cat(d, rotate=None):
    # The rotate keyword is so that we can also serve the rotate()
    # functionality.  rotate will be 'l', 'r', or 'u' for left, right,
    # or 180 degree rotations.
    args = d["args"]
    if len(args) < 2:
        Error("cat needs at least two arguments")
    output_file = args[-1]
    writer = GetOutputWriter(output_file, d)
    output_stream = open(output_file, "wb")
    for filename in args[:-1]:
        reader = PdfFileReader(open(filename, "rb"))
        n = reader.getNumPages()
        for i in range(n):
            page = reader.getPage(i)
            Sentinel(d)
            if rotate is not None:
                if rotate == "l":
                    page.rotateCounterClockwise(90)
                elif rotate == "r":
                    page.rotateClockwise(90)
                elif rotate == "u":
                    page.rotateClockwise(180)
                else:
                    raise Bug("'%s' is bad rotation spec" % rotate)
            writer.addPage(page)
        writer.write(output_stream)

def Delete(d):
    args = d["args"]
    if len(args) < 3:
        Error("delete needs at least three arguments")
    reader = PdfFileReader(open(args[0], "rb"))
    output_file = args[-1]
    writer = GetOutputWriter(output_file, d)
    output_stream = open(output_file, "wb")
    selections = args[1:-1]
    pages = reader.getNumPages()
    page_set = set(GetPageSet(selections, pages, complement=True))
    for i in range(pages):
        if i in page_set:
            page = reader.getPage(i)
            Sentinel(d)
            writer.addPage(page)
    writer.write(open(output_file, "wb"))

def Merge(d):
    args = d["args"]
    if len(args) < 2:
        Error("merge needs at least two arguments")
    output_file = args[-1]
    writer = GetOutputWriter(output_file, d)
    output_stream = open(output_file, "wb")
    page = None
    for filename in args[:-1]:
        reader = PdfFileReader(open(filename, "rb"))
        for i in range(reader.getNumPages()):
            Sentinel(d)
            if page is None:
                # This is the page we'll merge the others with
                page = reader.getPage(0)
                assert page is not None
                continue
            else:
                page.mergePage(reader.getPage(i))
    writer.addPage(page)
    writer.write(open(output_file, "wb"))

def Rotate(d):
    args = d["args"]
    if len(args) < 3:
        Error("rotate needs at least three arguments")
    rotate = args[0].lower()
    if len(rotate) != 1 and rotate not in "lru":
        Error("angle must be L, R, or U")
    del args[0]
    d["args"] = args
    Cat(d, rotate=rotate)

def Select(d):
    args = d["args"]
    if len(args) < 3:
        Error("select needs at least three arguments")
    reader = PdfFileReader(open(args[0], "rb"))
    output_file = args[-1]
    writer = GetOutputWriter(output_file, d)
    output_stream = open(output_file, "wb")
    selections = args[1:-1]
    pages = reader.getNumPages()
    for i in GetPageSet(selections, pages):
        page = reader.getPage(i)
        Sentinel(d)
        writer.addPage(page)
    writer.write(open(output_file, "wb"))

def Split(d):
    args = d["args"]
    if len(args) < 2:
        Error("split needs at least two arguments")
    prefix, count = args[0], d["-n"]
    for filename in args[1:]:
        reader = PdfFileReader(open(filename, "rb"))
        numpages = reader.getNumPages()
        # Get a format string that allows the integer numbers to have
        # leading zeros so that they will sort in natural order.
        lt = int(ceil(log10(numpages)))
        assert lt > 0
        fmt = "%%0%dd" % lt
        for i in range(reader.getNumPages()):
            output_file = prefix + (fmt % count) + ".pdf"
            writer = GetOutputWriter(output_file, d)
            output_stream = open(output_file, "wb")
            page = reader.getPage(i)
            Sentinel(d)
            writer.addPage(page)
            writer.write(open(output_file, "wb"))
            count += 1

def Watermark(d):
    args = d["args"]
    if len(args) != 3:
        Error("watermark needs three arguments")
    input_file, watermark_file, output_file = args
    reader = PdfFileReader(open(input_file, "rb"))
    watermark = PdfFileReader(open(watermark_file, "rb")).getPage(d["-w"])
    writer = GetOutputWriter(output_file, d)
    output_stream = open(output_file, "wb")
    for i in range(reader.getNumPages()):
        page = reader.getPage(i)
        Sentinel(d)
        page.mergePage(watermark)
        writer.addPage(page)
    writer.write(output_stream)

if __name__ == "__main__":
    d = {}      # Options dictionary & general carrier of information
    args = ParseCommandLine(d)
    mode = CheckMode(args[0], d)
    d["args"] = args[1:]
    if mode == "cat":
        Cat(d)
    elif mode == "delete":
        Delete(d)
    elif mode == "info":
        Info(d)
    elif mode == "merge":
        Merge(d)
    elif mode == "rotate":
        Rotate(d)
    elif mode == "select":
        Select(d)
    elif mode == "split":
        Split(d)
    elif mode == "watermark":
        Watermark(d)
    else:
        raise Bug("Mode '%s' not recognized" % d["mode"])
    if d["-d"]:
        out("")
