'''Produce a list of words visible in a set of HTML files passed on the
command line.  The intent is that this list could e.g. be run through a
spell checker to identify misspelled words in the input HTML files.
'''
 
# Copyright (C) 2005 Don Peterson
# Contact:  gmail.com@someonesdad1
 
#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#
 
from __future__ import print_function, division
import sys
import re
from HTMLParser import HTMLParser

# Dictionary to contain each unique word
all_words = {}

class MyHTMLParser(HTMLParser):
    def remove_punctuation(self, data):
        punct = re.compile("[^a-zA-Z0-9 ]+")
        s, n = punct.subn(" ", data)
        while n and len(s) > 1:
            s, n = punct.subn(" ", s)
        return s
    def handle_data(self, data):
        global all_words
        numbers = re.compile("\d+")
        for word in self.remove_punctuation(data).split():
            if not numbers.match(word):
                all_words[word.lower()] = 0

def ProcessFile(file):
    m = MyHTMLParser()
    m.feed(open(file).read())
    m.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write("Usage:  %s file1 [file2...]\n" % sys.argv[0])
        sys.exit(1)
    for file in sys.argv[1:]:
        ProcessFile(file)
    words = all_words.keys()
    words.sort()
    for word in words:
        print(word)
