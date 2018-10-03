'''
Script to print out the names of python functions and classes in the
file(s) given on the command line.
'''
 
# Copyright (C) 2018 Don Peterson
# Contact:  gmail.com@someonesdad1
 
#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#
 
from __future__ import print_function
import getopt
import os
import re
import sys
from pdb import set_trace as xx 

if len(sys.argv) == 1:
    print('''
{} file1 ...
   Prints out the function and class names found in the python scripts
   given on the command line.  Anonymous functions not printed.

   Warning:  because this script searches for lines with 'def' and 'class',
   it will print out the names of functions or classes given in multiline
   strings, even though they are not part of the script.
'''.strip().format(sys.argv[0]))
    exit(0)
r1 = re.compile('^( *)def +([^(]+) *\(')
r2 = re.compile('^( *)class +([^:]+)')
multiple = (len(sys.argv[1:]) > 1)
for file in sys.argv[1:]:
    print(file)
    for line in open(file):
        if line[-1] == "\n":
            line = line[:-1]
        mo = r1.search(line)
        if mo:
            spc, name = mo.groups()
            print("    {}{}()".format(spc, name))
            continue
        mo = r2.search(line)
        if mo:
            spc, name = mo.groups()
            print("    {}class {}".format(spc, name))
    if multiple:
        print()

