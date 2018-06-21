'''
Prints out ASCII characters.
'''

# Copyright (C) 2009, 2014 Don Peterson
# Contact:  gmail.com@someonesdad1

#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#

from __future__ import print_function
import sys
import getopt
from os import environ

nl = "\n"
decimal = False
octal = False
binary = False
Binary = False
offset = 0

column_width = 9
number_of_columns = 8

manual = '''Usage: {name} [options] [offset [numchars]]
Prints ASCII character set starting at the indicated offset for the
indicated number of characters (default 0x100).  Options:
    -B    Print the 256 binary characters
    -b    Print a binary listing
    -d    Print in decimal
    -h    Print this help
    -l    Print the lower 128 characters
    -o    Print octal characters
    -u    Print the upper 128 characters
    -x    Print in hex (default)
offset and numchars can be expressions.

Example:
    {name} 0x10a8*2
  will print a table of characters starting at 0x2150.  These are
  fractions symbols such as 1/7, 1/9, 1/10, etc. and a variety of
  arrows and math symbols.
'''[:-1]

def ListInColumns(list, col_width=0, num_columns=0, space_betw=0, truncate=0):
    '''Returns a list of strings with the elements of list (must be
    strings) printed in columnar format.  Elements of list that won't
    fit in a column either generate an exception if truncate is 0
    or get truncated if truncate is nonzero.  The number of spaces
    between columns is space_betw.
 
    If col_width and num_columns are 0, then the program will set them
    by reading the COLUMNS environment variable.  If COLUMNS doesn't
    exist, col_width will default to 80.  num_columns will be chosen
    by finding the length of the largest element so that it is not
    truncated.
 
    Caveat:  if there are a small number of elements in the list, you
    may not get what you expect.  For example, try a list size of 1 to
    10 with num_columns equal to 4:  for lists of 1, 2, 3, 5, 6, and 9,
    you'll get fewer than four columns.
    '''
    # Make all integers
    col_width = int(col_width)
    num_columns = int(num_columns)
    space_betw = int(space_betw)
    truncate = int(truncate)
    lines = []
    N = len(list)
    # Get the length of the longest line in the list
    maxlen = 0
    for line in list:
        if len(line) > maxlen:
            maxlen = len(line)
    if maxlen == 0:
        return [""]
    if col_width == 0:
        if "COLUMNS" in environ:
            columns = int(environ["COLUMNS"])
        else:
            columns = 80
        col_width = maxlen
    if num_columns == 0:
        try:
            num_columns = int(columns/maxlen)
        except:
            return [""]
        if num_columns < 1:
            raise Exception("A line is too long to display")
        space_betw = 1
    if col_width < 1 or num_columns < 1 or space_betw < 0:
        raise Exception("Error: invalid parameters")
    if N == 0:
        return [""]
    num_rows = int(N//num_columns + (N % num_columns != 0))
    for row in range(num_rows):
        st = ""
        for column in range(num_columns):
            ix = int(num_rows*column + row)
            if 0 <= ix <= (N-1):
                if len(list[ix]) > col_width:
                    if truncate:
                        st = st + list[ix][:col_width] + " "*space_betw
                    else:
                        raise Exception("Error:  element %d too long" % ix)
                else:
                    st += (list[ix] + " " * (col_width - len(list[ix]))
                           + " " * space_betw)
        lines.append(st)
    assert(len(lines) == num_rows)
    return lines

def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)

def Usage():
    name = sys.argv[0]
    print(manual.format(**locals()))
    exit(1)

def Integer(s):
    '''Convert the string s to an integer.  Allow prefixes such as 0x,
    0b, 0o.
    '''
    s, base = s.lower(), 10
    if s.startswith("0b"):
        base = 2
    elif s.startswith("0o"):
        base = 8
    elif s.startswith("0x"):
        base = 16
    return int(s, base)

def ParseCommandLine():
    global Binary, binary, decimal, octal, offset
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "Bbdhloux")
    except getopt.GetoptError as st:
        msg, option = st
        print(msg)
        sys.exit(1)
    lower, upper = 0, 256
    for opt in optlist:
        if opt[0] == "-B":
            Binary = True
        elif opt[0] == "-b":
            binary = True
        elif opt[0] == "-d":
            decimal = True
        elif opt[0] == "-h":
            Usage()
        elif opt[0] == "-l":
            lower, upper = 0, 128
        elif opt[0] == "-o":
            octal = True
        elif opt[0] == "-u":
            lower, upper = 128, 256
        elif opt[0] == "-x":
            Binary = binary = decimal = octal = False
    # Get codepoint if present
    if args:
        try:
            offset = min(max(0, eval(args[0])), 0x10ffff)
        except Exception:
            Error("'%s' is not a valid integer for offset" % args[0])
        if offset < 0:
            Error("Hex offset must be >= 0")
        if len(args) > 1:
            try:
                numchars = eval(args[1])
                upper = lower + numchars
            except Exception:
                Error("'%s' is not a valid integer for numchars" % args[1])
    return lower, upper

def PrintBinary():
    for i in range(0x100):
        c = i + offset
        sys.stdout.write(str(c) + " " + chr(c) + nl)

def PrintBinaryListing():
    for i in range(0x100):
        c = i + offset
        sys.stdout.write(chr(c))
    sys.stdout.write(nl)

def PrintTable(format, lower, upper):
    ctrl = ("nul", "soh", "stx", "etx", "eot", "enq", "ack", "bel", "bs",
            "ht", "nl", "vt", "ff", "cr", "so", "si", "dle", "dc1", "dc2",
            "dc3", "dc4", "nak", "syn", "etb", "can", "em", "sub", "esc",
            "fs", "gs", "rs", "us", "sp",)
    s = []
    L = len(format % (0, ctrl[0]))
    for i in range(lower, upper):
        c = i + offset
        if c <= ord(" "):
            t = format % (c, ctrl[c])
        else:
            t = format % (c, chr(c))
        s.append(t)
    for i in ListInColumns(s, col_width=column_width,
                           num_columns=number_of_columns):
        print(i.rstrip())

def main():
    lower, upper = ParseCommandLine()
    if decimal:
        PrintTable("%03d %-3s", lower, upper)
    elif octal:
        PrintTable("%03o %-3s", lower, upper)
    elif binary:
        PrintBinary()
    elif Binary:
        PrintBinaryListing()
    else:
        PrintTable("%02x %-3s", lower, upper)

main()
