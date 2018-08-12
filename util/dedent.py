'''
Dedent a chunk of text, which means to remove the common beginning
space characters.
'''

from __future__ import division, print_function
import sys
import os
import getopt
import textwrap

# Copyright (C) 2014 Don Peterson
# Contact:  gmail.com@someonesdad1

#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#

def _Usage(d, status=1):
    name = sys.argv[0]
    s = '''
Usage:  {name} [options] [file1 [file2...]]
  Remove the common space characters from the lines in the
  concatenated files (or stdin if no files given).

Options:
    -h
        Print a manpage.
'''[1:-1]
    print(s.format(**locals()))
    exit(status)

def _ParseCommandLine(d):
    try:
        optlist, filenames = getopt.getopt(sys.argv[1:], "h")
    except getopt.GetoptError as e:
        msg, option = e
        print(msg)
        exit(1)
    for opt in optlist:
        if opt[0] == "-h":
            _Usage(d, status=0)
    return filenames

def Dedent(lines):
    '''Remove the common space characters from a sequence of lines.  Each line
    should end with a newline character.
    '''
    s = ''.join(lines)
    return textwrap.dedent(''.join(text))

if __name__ == "__main__": 
    opt, text = {}, []
    filenames = _ParseCommandLine(opt)
    if not filenames:
        text.append(sys.stdin.read())
    else:
        for filename in filenames:
            with open(filename, "rU") as f:
                text.append(f.read())
    print(Dedent(text))

