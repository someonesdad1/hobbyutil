'''
Provides a function that will fit a string into a specified
number of columns, wrapping as appropriate.  It will do a
reasonable job, but it's impossible to handle all the
vagaries of English without understanding the semantics.
 
If called as a script, acts as a simple text formatter.
 
For another tool which you might find preferable, see the
python library module textwrap.
'''
 
# Copyright (C) 2009 Don Peterson
# Contact:  gmail.com@someonesdad1
 
#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#
 
from __future__ import print_function, division
import sys
import getopt

from pdb import set_trace as xx
if 1:
    import debug
    debug.SetDebugger()

nl = "\n"

# The abbr dictionary will contain abbreviations that should only get one
# space after themselves when encountered with a period character at the
# end.
abbr = {}
a = (
    "a", "a.b", "a.c", "a.d", "a.m", "adm", "al", "apr", "assn", "at",
    "aug", "ave", "b", "b.a", "b.c", "b.p", "b.s", "c", "capt", "co",
    "col", "com", "comdr", "corp", "cpl", "d", "d.c", "dec", "dept",
    "dist", "div", "dr", "e", "e.g", "ea", "ed", "esq", "est", "et",
    "et.al", "etc", "f", "feb", "g", "gen", "gov", "grad", "h", "hon", "i",
    "i.e", "inc", "inst", "j", "jan", "jr", "jul", "jun", "k", "l", "lat",
    "long", "lt", "ltd", "m", "m.a", "m.s", "maj", "mar", "may", "mme",
    "mr", "mrs", "ms", "msgr", "mt", "mts", "n", "n.a", "n.b", "nb", "no",
    "nov", "o", "oct", "op", "p", "p.m", "pg", "ph.d", "pl", "pop",
    "pseud", "pub", "q", "r", "r.n", "rd", "ref", "rev", "s", "sep",
    "sept", "seq", "sgt", "sic", "so", "sq", "sr", "st", "ste", "t", "u",
    "u.s", "u.s.a", "u.s.a.f", "u.s.c.g", "u.s.m.c", "u.s.n", "u.s.s.r",
    "univ", "v", "vol", "vs", "w", "x", "y", "z",
)
for i in a:
    abbr[i] = ""
# The following abbreviations came from
# http://www.aresearchguide.com/comabb.html.  I've pruned a few out (mostly
# physical units that I don't want treated as abbreviations).
a = (
    "abbr", "abr", "acad", "adj", "adm", "adv", "agr", "anon", "app",
    "approx", "assn", "bact", "bap", "bib", "bibliog", "biog", "biol",
    "bk", "bkg", "bldg", "blvd", "bot", "bp", "brig", "bro", "bur", "c",
    "c.c", "cal", "cap", "capt", "cath", "cc", "cent", "cf", "ch", "chap",
    "chem", "chm", "chron", "cir", "cit", "civ", "clk", "co", "col",
    "colloq", "com", "comdr", "comp", "comr", "con", "cond", "conf",
    "cong", "consol", "constr", "cont", "corp", "cp", "cpl", "cr", "crit",
    "ct", "cu", "cwt", "d", "dec", "def", "deg", "dep", "dept", "der",
    "diag", "dial", "dict", "dim", "dipl", "dir", "disc", "dist", "distr",
    "div", "dm", "do", "doc", "doz", "dpt", "dr", "dup", "dwt", "ea",
    "eccl", "ecol", "econ", "ed", "elec", "elev", "emp", "enc", "ency",
    "eng", "entom", "esp", "est", "etc", "ex", "exch", "exec", "fac",
    "fed", "fem", "ff", "fig", "fin", "fl", "fn", "fr", "fwd", "gall",
    "gaz", "gen", "geog", "geol", "geom", "gloss", "gov", "govt", "gr",
    "gram", "hab", "her", "hist", "hort", "ht", "ib", "id", "illus", "imp",
    "inc", "ins", "inst", "intl", "introd", "is", "jour", "jr", "jud", "k",
    "kilo", "lab", "lang", "lat", "lb", "lib", "lieut", "lit", "loc",
    "lon", "ltd", "m", "mach", "mag", "maj", "mas", "math", "mdse", "mech",
    "med", "mem", "mfg", "mfr", "mgr", "misc", "mo", "mod", "ms", "mt",
    "mus", "narr", "natl", "nav", "neg", "no", "obit", "obj", "op", "orch",
    "orig", "p", "par", "pat", "pct", "pen", "perf", "philos", "phys",
    "pl", "ppd", "pref", "prin", "pro", "prod", "pron", "pseud", "psych",
    "pub", "q", "qr", "qtd", "ques", "quot", "r", "rec", "ref", "reg",
    "rel", "rev", "riv", "rpt", "sc", "sch", "sci", "sculp", "sec", "ser",
    "serg", "sing", "sol", "sp", "sq", "sub", "subj", "sup", "supt",
    "surg", "sym", "syn", "t", "tbs", "tel", "tem", "temp", "terr",
    "theol", "topog", "trans", "treas", "trig", "tsp", "twp", "ult",
    "univ", "usu", "v", "var", "vb", "vers", "vet", "viz", "vol", "vox",
    "vs", "wpm", "writ", "wt",
)
for i in a:
    abbr[i] = ""
del a

def Fit(string, columns=75, indent=0, eos_spaces=2,
        abbreviations=abbr, keep_paragraphs=True):
    '''Fits string into the indicated number of columns and returns the
    resulting string.

    indent          If nonzero, that many spaces are added to the beginning
                    of each line.
    eos_spaces      Controls how many space characters are placed after
                    the period at the end of a line.
    abbreviations   A dictionary that contains words that are commonly
                    abbreviated and will only get one space after the
                    period.
    keep_paragraphs If true, paragraphs (as indicated by double newlines)
                    are kept separated.
    '''
    def Check(word):
        '''Append a space to the word except if it ends with a '.' or ':'.
        If word ends with a '.', append the appropriate number of
        spaces.  If it ends with ':', append two spaces.
        '''
        if word[-1] == ".":
            # Strip off leading nonalphanumerics.  This handles text like
            # 'Mr. Smith' and won't allow two spaces to be put after Mr.
            prefix = ""
            while word and not word[0].isalpha():
                prefix += word[0]
                word = word[1:]
            if word[:-1].lower() in abbreviations:
                word += " "
            else:
                word += " "*eos_spaces
            word = prefix + word
        elif word[-1] == ":":
            word += "  "
        else:
            word += " "
        return word
    def ProcessParagraph(string):
        words, s, line = string.split(), "", " "*indent
        for word in words:
            word = Check(word)
            if len(word) + len(line) > columns:
                s += line + nl
                line = " "*indent
                while len(word) > columns:
                    s += word[:columns + 1] + nl
                    word = word[columns + 1:]
            line += word
        if line:
            s += line + nl
        return s
    s = ""
    if keep_paragraphs:
        paragraphs = string.split(nl + nl)
        s = nl.join([ProcessParagraph(p) for p in paragraphs])
    else:
        s = ProcessParagraph(string)
    return s

if __name__ == "__main__":
    # Act as a simple formatter for text.
    columns = 75
    indent = 0
    eos_spaces = 2
    def Error(msg, status=1):
        print(msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        name = sys.argv[0]
        s = '''Usage:  {name} [options] [file1 ...]
  Does simple text formatting to fit text into a given number of columns.
  Paragraphs are separated by two consecutive newlines and are maintained.
  The indicated files are read and the output is sent to stdout.  If no files
  are given, stdin is read.
 
Options:
  -c columns
      Set the number of columns to fit the text into.  Defaults to 75.
  -i indent
      Set the indent for each line (defaults to 0).
  -p spaces
      Put the indicated number of spaces after each sentence.  Defaults
      to 2.
  -w columns
      Same as -c option.
'''[:-1]
        print(s.format(**locals()))
        exit(status)
    def ParseCommandLine():
        try:
            optlist, args = getopt.getopt(sys.argv[1:], "c:hi:p:w:")
        except getopt.GetoptError as str:
            msg, option = str
            print(msg + nl)
            sys.exit(1)
        for opt in optlist:
            if opt[0] in ("-c", "-w") :
                global columns
                try:
                    columns = int(opt[1])
                    if columns <= 0:
                        Error("-c:  columns must be > 0")
                except ValueError:
                    Usage(1)
            if opt[0] == "-h":
                Usage(0)
            if opt[0] == "-i":
                global indent
                try:
                    indent = int(opt[1])
                    if indent < 0:
                        Error("-i:  indent must be >= 0")
                except ValueError:
                    Usage(1)
            if opt[0] == "-p":
                global eos_spaces
                try:
                    eos_spaces = int(opt[1])
                    if eos_spaces < 0:
                        Error("-p:  spaces after sentence must be >= 0")
                except ValueError:
                    Usage(1)
        return args
    #
    args = ParseCommandLine()
    if args:
        for file in args:
            s = Fit(open(file).read(), columns, indent, eos_spaces)
            print(s)
    else:
        s = Fit(sys.stdin.read(), columns, indent, eos_spaces)
        print(s)
