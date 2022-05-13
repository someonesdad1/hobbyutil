'''
Search for a pattern in a binary file
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2009 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Search for a pattern in a binary file
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
    import getopt
    import re
if 1:   # Global variables
    plain_text = False                  # -f
    ignore_case = False                 # -i
    just_show_file_matches = False      # -l
    hex_to_binary = False               # -o
    show_match = False                  # -s
    manual = r'''{0} [options] pattern [file1...]
  Do a pattern search in binary files and print the zero-based offset of
  the located pattern.  Offsets will be printed in decimal, hex, and
  percentage.  If no files are given, stdin is searched.  Python regular
  expressions are used in pattern, not grep-style patterns.

  If you use the -o option, the pattern must consist of pairs of hex
  digits; for example: "6865 6c 6c 6f".  Any space characters will be
  removed, then each pair of hex characters will be converted to a byte.

Options
    -f      Plain text match (i.e., don't use regular expressions)
    -i      Ignore case
    -l      Just print files that have one or more matches
    -o      Convert the hex digits in the pattern to a binary string
    -s      Include the matched binary string in the printout (not with -f)

Some python regular expression special characters:
    \b      Empty string at beginning or end of word
    \B      Empty string not at beginning or end of word.
    \d      Any decimal digit == [0-9]
    \D      Any non decimal digit == [^0-9]
    \s      Any whitespace character == [ \t\n\r\f\v]
    \S      Any nonwhitespace character == [^ \t\n\r\f\v]
    \w      Any alphanumeric character
    \W      Any non-alphanumeric character
    \Z      Matches only at the end of the string

Examples (assumes bash-like command line and program aliased to bgrep):
    bgrep -s "\\d+" file
        Show all numbers and their offsets in the file.
    bgrep -s "0x[\\dA-Fa-f]+" file
        Show all hexadecimal numbers and their offsets in the file.
    bgrep "\\r\\n" file
        Show the offsets of the carriage return/linefeed pairs.
    bgrep -s "\\d{{1,2}}/\\d{{1,2}}/\\d\\d" file
        Show the offsets of all dates in the file of the form
        n1/n1/n2 where n1's are one or two digits numbers and n2
        is a two digit number.
'''.format(sys.argv[0])
def Usage():
    print(manual)
    exit(0)
def Error(msg):
    print(msg, file=sys.stderr)
    exit(1)
def ParseCommandLine():
    if len(sys.argv) < 2:
        Usage()
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "fhilos")
    except getopt.GetoptError as str:
        msg, option = str
        print(msg)
        sys.exit(1)
    for opt in optlist:
        if opt[0] == "-f":
            global plain_text
            plain_text = True
        if opt[0] == "-h":
            print(manual)
            exit(0)
        if opt[0] == "-i":
            global ignore_case
            ignore_case = True
        if opt[0] == "-l":
            global just_show_file_matches
            just_show_file_matches = True
        if opt[0] == "-o":
            global hex_to_binary
            hex_to_binary = True
        if opt[0] == "-s":
            global show_match
            show_match = True
    if len(args) < 1:
        Usage()
    return args
def PrintOffsets(string, file, offsets, match_objects):
    if not offsets:
        return
    indent = ""
    file_size = len(string)
    if file:
        s = " [%d (0x%x) bytes]" % (file_size, file_size)
        print(file + s)
        indent = "  "
    if not match_objects:
        for offset in offsets:
            print(indent, end="")
            print("%12d " % offset, end="")
            s = "0x%x" % offset
            print("  %12s " % s, end="")
            print("  %6.2f%% " % (100*(offset + 1.)/file_size), end="")
            print()
    else:
        for offset, mo in zip(offsets, match_objects):
            print(indent, end="")
            print("%12d " % offset, end="")
            s = "0x%x" % offset
            print("  %12s " % s, end="")
            print("  %6.2f%% " % (100*(offset + 1.)/file_size), end="")
            if show_match and match_objects:
                print(string[mo.start():mo.end()], end="")
            print()
def ProcessString(pattern, string):
    '''If there are matches, return the offsets (as decimal numbers)
    in a list.  An empty list means no matches.
    '''
    offsets = []
    match_objects = []
    L = len(string)
    if plain_text:
        start = 0
        while start < L:
            offset = string.find(pattern, start)
            if offset != -1:
                offsets.append(offset)
                start = offset + 1
                if just_show_file_matches:
                    break
            else:
                start = L
    else:
        if ignore_case:
            reg = re.compile(pattern, re.I)
        else:
            reg = re.compile(pattern)
        start = 0
        while start < L:
            mo = reg.search(string, start)
            if mo:
                offsets.append(mo.start())
                match_objects.append(mo)
                start = mo.end()
                if just_show_file_matches:
                    break
            else:
                start = L
    return offsets, match_objects
def ConvertToBinary(pattern):
    d = {
        "0": 0, "1": 1, "2":  2, "3": 3, "4": 4, "5": 5, "6": 6 , "7":
        7, "8": 8, "9": 9, "a": 10, "b": 11, "c": 12, "d": 13, "e": 14,
        "f": 15}
    L = len(pattern)
    if not L:
        Error("Empty hex pattern not allowed")
    if L % 2 != 0:
        Error("Empty hex pattern not allowed")
    pattern = pattern.lower()
    pattern = pattern.replace(" ", "")
    s = ""
    L = len(pattern)
    for i in range(L):
        if pattern[i] not in d:
            Error("'%s' is not a valid hex digit" % pattern[i])
    for i in range(0, L, 2):
        s += chr(d[pattern[i]]*16 + d[pattern[i+1]])
    return s
if __name__ == "__main__":
    args = ParseCommandLine()
    pattern = args[0]
    if hex_to_binary:
        pattern = ConvertToBinary(pattern)
        plain_text = True
    if len(args) == 1:
        string = sys.stdin.read()
        offsets, match_objects = ProcessString(pattern, string)
        PrintOffsets(string, "stdin", offsets, match_objects)
    else:
        for file in args[1:]:
            string = open(file, "rb").read()
            offsets, match_objects = ProcessString(pattern, string)
            if just_show_file_matches:
                if offsets:
                    print(file)
            else:
                PrintOffsets(string, file, offsets, match_objects)

