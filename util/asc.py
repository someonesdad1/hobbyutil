'''
Prints out ASCII characters
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2009, 2014 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Prints out ASCII characters
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
    import getopt
    from textwrap import dedent
    from os import environ
    from pdb import set_trace as xx 
if 1:   # Custom imports
    from columnize import Columnize
if 1:   # Global variables
    class Global: pass
    g = Global()
    g.decimal = False
    g.octal = False
    g.binary = False
    g.Binary = False
    g.offset = 0
    g.column_width = 9
    g.number_of_columns = 8
def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)
def Usage():
    name = sys.argv[0]
    print(dedent(f'''
    Usage: {name} [options] [offset [numchars]]
      Prints the ASCII/Unicode character set starting at the indicated offset 
      for the indicated number of characters (default 0x100).  Options:
        -B    Print the 256 binary characters
        -b    Print a binary listing
        -d    Print in decimal
        -h    Print this help
        -l    Print the lower 128 characters
        -o    Print octal characters
        -u    Print the upper 128 characters
        -x    Print in hex (default)
      offset and numchars can be expressions.  Prefix hex numbers with '0x' and
      octal numbers with '0b'.
    
    Example:
         {name} 0x10a8*2
      will print a table of characters starting at 0x2150.  These are Unicode
      fractions symbols such as 1/7, 1/9, 1/10, etc. and a variety of arrows
      and math symbols.'''[1:]))
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
    #global Binary, binary, decimal, octal, offset
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "Bbdhloux")
    except getopt.GetoptError as st:
        msg, option = st
        print(msg)
        sys.exit(1)
    lower, upper = 0, 256
    for opt in optlist:
        if opt[0] == "-B":
            g.Binary = True
        elif opt[0] == "-b":
            g.binary = True
        elif opt[0] == "-d":
            g.decimal = True
        elif opt[0] == "-h":
            Usage()
        elif opt[0] == "-l":
            lower, upper = 0, 128
        elif opt[0] == "-o":
            g.octal = True
        elif opt[0] == "-u":
            lower, upper = 128, 256
        elif opt[0] == "-x":
            g.Binary = g.binary = g.decimal = g.octal = False
    # Get codepoint if present
    if args:
        try:
            g.offset = min(max(0, eval(args[0])), 0x10ffff)
        except Exception:
            Error("'{}' is not a valid integer for offset".format(args[0]))
        if offset < 0:
            Error("Hex offset must be >= 0")
        if len(args) > 1:
            try:
                numchars = eval(args[1])
                upper = lower + numchars
            except Exception:
                Error("'{}' is not a valid integer for numchars".format(args[1]))
    return lower, upper
def PrintBinary():
    for i in range(lower, upper):
        c = i + g.offset
        print(f"{c:3d} 0x{c:02x} 0o{c:03o} 0b{c:08b} {chr(c)}")
def PrintBinaryListing():
    for i in range(0x100):
        c = i + g.offset
        print(chr(c))
    print()
def PrintTable(fmt, lower, upper):
    ctrl = ("nul", "soh", "stx", "etx", "eot", "enq", "ack", "bel", "bs",
            "ht", "nl", "vt", "ff", "cr", "so", "si", "dle", "dc1", "dc2",
            "dc3", "dc4", "nak", "syn", "etb", "can", "em", "sub", "esc",
            "fs", "gs", "rs", "us", "sp",)
    s = []
    for i in range(lower, upper):
        c = i + g.offset
        if c <= ord(" "):
            t = fmt.format(c, ctrl[c])
        else:
            t = fmt.format(c, chr(c))
        s.append(t)
    for i in Columnize(s, col_width=g.column_width, columns=g.number_of_columns):
        print(i)
if __name__ == "__main__": 
    lower, upper = ParseCommandLine()
    if g.decimal:
        PrintTable("{:03d} {:3s}", lower, upper)
    elif g.octal:
        PrintTable("{:03o} {:3s}", lower, upper)
    elif g.binary:
        PrintBinary()
    elif g.Binary:
        PrintBinaryListing()
    else:
        PrintTable("{:02x} {:3s}", lower, upper)
