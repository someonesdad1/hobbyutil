'''
Convert a text file for including into a C program
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Convert a text file for including into a C program
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
    import os
    import getopt
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
def Usage(status=1):
    print(dedent(f'''
    Usage:  {sys.argv[0]} [options] [file1 [file2...]]
      Convert the text lines in the files to lines suitable for use in a
      C/C++ program by surrounding them with double quotes, putting \\n at
      the end of the line, and escaping double quotes.  The results are sent
      to stdout.  Use '-' for stdin.
    
      This lets you format the text with your text editor, manufy it, then
      paste it into your program.  For example, a whole manual page could be
      printed by formatting it in your editor, then running manufy on it;
      the output could be used as printf( "This is a sample\\n" "man page
      that has\\n" "been manufy'd.\\n");
    Options:
        -h      Show this help message.
        -u      Remove the leading/trailing quotes, unescape the double quotes,
                and remove the ending \\n.
    '''))
    exit(status)
def ParseCommandLine(d):
    d["-u"] = False
    try:
        optlist, files = getopt.getopt(sys.argv[1:], "hu")
    except getopt.GetoptError as str:
        msg, option = str
        print(msg)
        sys.exit(1)
    for o, a in optlist:
        if o == "-u":
            d["-u"] = True
        elif o == "-h":
            Usage(0)
    if not files:
        Usage()
    return files
def ProcessFile(stream, d):
    for line in stream:
        if d["-u"]:
            line = line.strip().replace('\\"', '"')
            if line[0] == '"':
                line = line[1:]
            if line[-1] == '"':
                line = line[:-1]
            if line[-2:] == '\\n':
                line = line[:-2]
        else:
            line = line.rstrip().replace('"', '\\"')
            line = '"{}\\n"'.format(line)
        print(line)
if __name__ == "__main__":
    d = {}  # Options dictionary
    files = ParseCommandLine(d)
    for file in files:
        stream = sys.stdin if file == "-" else open(file)
        ProcessFile(stream, d)
