# coding: utf-8
'''

Todo:

    * Many searches result in foreign symbols.  Change the default to
      remove codepoints with terms like: 
        
        AEGEAN      CHEROKEE    HANUNOO     LYCIAN      OSMANYA     SYRIAC
        ALCHEMICAL  CJK         HEBREW      LYDIAN      PAHAWH      TAG
        ARABIC      COPTIC      HEXAGRAM    MAHAJANI    PALMYRENE   TAGALOG
        ARMENIAN    CUNEIFORM   HIRAGANA    MAHJONG     PAU         TAGBANWA
        AVESTAN     CYPRIOT     IDEOGRAPHIC MALAYALAM   PHAGS-PA    TAI
        BALINESE    CYRILLIC    IMPERIAL    MANDAIC     PHAISTOS    TAKRI
        BAMUM       DESERET     JAVANESE    MANICHAEAN  PHOENICIAN  TAMIL
        BASSA       DEVANAGARI  KAITHI      MEETEI      PSALTER     TELUGU
        BATAK       DUPLOYAN    KANGXI      MENDE       REJANG      TETRAGRAM
        BENGALI     EGYPTIAN    KANNADA     MEROITIC    RUMI        THAANA
        BOPOMOFO    ELBASAN     KATAKANA    MIAO        RUNIC       THAI
        BRAHMI      ETHIOPIC    KAYAH       MODI        SAURASHTRA  TIBETAN
        BRAILLE     GEORGIAN    KHAROSHTHI  MONGOLIAN   SHARADA     TIFINAGH
        BUGINESE    GLAGOLITIC  KHMER       MRO         SHAVIAN     TIRHUTA
        BUHID       GOTHIC      KHOJKI      MYANMAR     SIDDHAM     UGARITIC
        BYZANTINE   GRANTHA     KHUDAWADI   NABATAEAN   SINHALA     VAI
        CARIAN      GREEK       LAO         NKO         SORA        VEDIC
        CAUCASIAN   GUJARATI    LEPCHA      OGHAM       SUNDANESE   WARANG
        CHAKMA      GURMUKHI    LIMBU       OL          SYLOTI      YI
        CHAM        HANGUL      LISU        ORIYA

NOTE:  Unicode 8.0 came out about the middle of 2015.  UTF-x means
"Unicode Tranformation Format x".
----------------------------------------------------------------------

Utility to help with Unicode.  Run with no arguments to see usage
statement.

Note:  this script should run with either python 2 or 3.  I find it's
about 5 times faster under python 3.4.0 versus python 2.7.6.
'''
# Copyright (C) 2014 Don Peterson
# Contact:  gmail.com@someonesdad1

#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#

from __future__ import print_function
import bisect
import getopt
import glob
import os
import re
import sys
from operator import itemgetter
import subprocess
from ucd import ucd, pickle_file
from pdb import set_trace as xx
if 0:
    import debug
    debug.SetDebugger()

py3 = True if sys.version_info[0] > 2 else False
py2 = not py3
if py2:
    chr = unichr

nl = "\n"

# Global variables you'll need to set
pdf_dir = "/doc/unicode/pdf"            # Where PDFs are located
launch = "/usr/bin/exo-open"            # Program to launch a file

# Common codepoints (in hex) to list with the -c option
common = '''
    00b0 00b1 00b2 00b3 00b7 00b9 00d7 025b 0263 0393 039b 039e 03a6
    03a8 03a9 03b1 03b2 03b4 03b6 03b8 03bb 03bc 03bd 03be 03c0 03c1
    03c3 03c4 03c6 03c7 03c8 03c9 03d5 03f5 03f6 2070 2074 2075 2076
    2077 2078 2079 207a 207b 2102 2110 2115 211a 211b 211d 2124 2200
    221A 223C
    2202 2203 2205 2206 2208 2209 2211 2213 2218 221d 221e 2221 2248
    224c 225d 225f 2260 2261 2262 2282 2283 2284 2285 2286 2287 2288
    2289 2295 2297 2299
'''

def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)

def Usage(d, status=1):
    version = ucd["version"]
    name = sys.argv[0]
    num = len(ucd["chars"])
    s = '''
Usage:  {name} [options] regexp [action]
  Search the Unicode symbol index for a particular symbol.  There are
  {num} symbols in the index.  The searches are case-independent.
  The Unicode version used is {version}.  The output is sorted so that
  the lowest codepoints are printed last.

  If regexp looks like a hex number (or a standard Unicode codepoint
  form such as U+00b1), then it's interpreted as a Unicode code point
  (character) and information on that character is printed.  Otherwise,
  a list of characters whose description matches the regular expression
  is printed.  Numbers can also use the prefixes '0b' for binary, '0o'
  for octal, and '0d' for decimal.

  If regexp looks like a single character, identify it and print out its
  information.  If you want to enter a single digit number, preface it
  with '0'.

  The only action currently supported is 'o', which means to open the
  associated PDF file to let you look at a picture of a glyph
  representing this character.  To use this feature, you'll have to
  download some PDF files from the Unicode website (see the
  documentation file unicode.pdf).

Example:
  Suppose you want the Unicode symbol for a steaming pile of poo.
  Run the script as
    {name} poo
  and you'll get a list of candidates.  The description of interest is
  '1f4a9 PILE OF POO', so run the command
    {name} 1f4a9 o
  and the relevant PDF will be opened, assuming you have downloaded
  the proper PDF file.  Consult the unicode.odt or unicode.pdf files
  for details on how to get these PDFs and how they must be named.

Options:
    -A      Show all characters, including those from foreign languages.
    -a      Sort output alphabetically (default = by codepoint).
    -c      Show common codepoints.
    -r      Reverse sort order
    -t      Force a textual lookup (e.g., without using -t, an argument
            like 'face' will look like a hex number).

Common Unicode characters:
  ° Ω π θ · × ÷ √ μ α β ɣ δ Δ ɛ ϵ ϶ ν ξ ψ φ ϕ ζ λ ρ σ τ χ ω Γ Φ Ξ Λ
  ∞ ∂ ∼ ∝ ± ∓ ∍ ∊ ∈ ∉ ∅ ∃ « » ∀ ∡ ∠ ∟ ∥ ∦ ℝ ℂ ℤ ℕ ℚ ℐ ℛ ⊙ ⊗ ⊕ ⊉ ⊈ ⊇ ⊆ ⊅ ⊄ ⊃ ⊂
  ≤ ≥ ≪ ≫ ≈ ≠ ≡ ≢ ≝ ≟ ∧ ∨ ∩ ∪ ∴ ⁻ ⁺ ¹ ² ³ ⁴ ⁵ ⁶ ⁷ ⁸ ⁹ ⁰ ⅛ ¼ ⅜ ½ ⅝ ¾ ⅞
'''[1:-1]
    print(s.format(**locals()))
    sys.exit(status)

def ParseCommandLine(d):
    d["-A"] = False     # Show all characters
    d["-a"] = False     # Sort alphabetically
    d["-c"] = False     # Common codepoints
    d["-r"] = False     # Reverse sort
    d["-t"] = False     # Force text
    try:
        opts, args = getopt.getopt(sys.argv[1:], "Aacrt")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o in ("-a",):
            d["-a"] = not d["-a"]
        elif o in ("-A",):
            d["-A"] = not d["-A"]
        elif o in ("-c",):
            d["-c"] = not d["-c"]
        elif o in ("-r",):
            d["-r"] = not d["-r"]
        elif o in ("-t",):
            d["-t"] = not d["-t"]
    if not args and not d["-c"]:
        Usage(d)
    return args

def Int(s):
    '''Convert the string s to an integer.  Allowed forms are:
    Hex digits:  hexadecimal is the default
    0d means a decimal number
    0b binary
    0o octal
    Return None if the string can't be converted to a number.
    '''
    try:
        if s.startswith("0b"):
            return int(s, 2)
        elif s.startswith("0o"):
            return int(s, 8)
        elif s.startswith("0d"):
            return int(s[2:], 10)
        else:
            return int(s, 16)
    except Exception:
        return None

def IsHexNumber(regexp, d):
    chars = set(regexp.lower())
    digits, letters = "0123456789", "abcdef"
    if d["-d"]:
        return chars.issubset(set(digits))
    else:
        return chars.issubset(set(digits + letters))

def GetNumberRanges(d):
    '''Read all the PDF files and return a list of tuple pairs
    encoding their range.
    '''
    ranges = []
    for filename in glob.iglob(pdf_dir + "/*.[pP][dD][fF]"):
        loc = filename.rfind("U")
        if loc == -1:
            continue
        s = filename[loc + 1:]
        dp = s.find(".")
        if dp == -1:
            continue
        s = s[:dp]
        x = s.split("-")
        if len(x) != 2:
            continue
        low, high = [int(i, 16) for i in x]
        if low >= high:
            low, high = high, low
        ranges.append((low, high, filename))
    return ranges

def Normalize(num):
    '''num is an integer Unicode codepoint to look for.  Ensure its
    string representation is at least four characters long.  For
    example, the space character is 0x20; return 0020 because the
    Unicode text file uses that string to begin a line that describes
    the symbol.  Return it in uppercase, as that's what the Unicode
    files use.
    '''
    s = hex(num)[2:]
    while len(s) < 4:
        s = "0" + s
    return s.upper()

def OpenTextFile(num, filename, d):
    '''filename is the name of a PDF file.  num is the codepoint to
    search for.  Open the text file, search down to the first form
    feed, then start searching for a line that begins with that
    codepoint number.  Continue to print lines until the next
    codepoint line is reached.
    '''
    # Get the text from the text file corresponding to the PDF
    name, ext = os.path.splitext(filename)
    textfile = name + ".txt"
    if not os.path.isfile(textfile):
        Error("Could not find '%s'" % textfile)
    text = open(textfile, "rb").read().decode("UTF-8")
    # Keep only the text after the second formfeed character
    for i in range(1, 3):
        loc = text.find(chr(0x0c))
        if loc == -1:
            Error("'%s' missing formfeed number %d" % (textfile, i))
        text = text[loc + 1:]
    # Now split on newlines
    lines = text.split(nl)
    # Search down until regexp is found
    codepoint, show = Normalize(int(num, 16)), False
    r = re.compile(r"^[0-9a-f]{4,5}", re.I)
    for line in lines:
        if line.startswith(codepoint):
            show = True
        else:
            mo = r.search(line)
            if show and mo:
                break  # Found next codepoint's line
        if show:
            print(line)

def OpenPDF(regexp, d):
    cp = int(regexp, 16)
    ranges = GetNumberRanges(d)
    for low, high, filename in ranges:
        if low <= cp <= high:
            rc = subprocess.call("%s %s" % (launch, filename), shell=True)
            return
    print("No appropriate file found for %s" % regexp)

def GetCodepoint(line):
    f = line.split()
    return int(f[-1], 16)

def GetCodepointBinary(line):
    '''Return a string representing the codepoint in binary.  Since
    the largest codepoint is 0x10ffff, the binary form of this number
    is 0b100001111111111111111; hence the width of 21 digits.
    '''
    cp = GetCodepoint(line)
    s = list(reversed(bin(cp)[2:]))
    while len(s) < 21:
        s.append("0")
    return ''.join(list(reversed(s)))

def PutCodepointFirst(line, d):
    f = line.split()
    if d["-b"]:
        b = GetCodepointBinary(line)
        return "{0} {1}".format(b, ' '.join(f[:-1]))
    else:
        # 6 is used because the largest codepoint's hex form is 10ffff
        return "{0:6} {1}".format(f[-1], ' '.join(f[:-1]))

def GetBlockName(cp):
    if not (0 <= cp <= 0x10ffff):
        raise ValueError("Codepoint must be in [0, 0x10ffff]")
    # Construct three equal-length arrays for the start cp, end cp,
    # and name.
    starts, ends, names = [], [], []
    for s, e, n in ucd["blocks"]:
        starts.append(s)
        ends.append(e)
        names.append(n)
    # Note they must be sorted in increasing starts order for this to
    # work.
    index = find_le(starts, cp)
    if index is None:
        return None
    assert starts[index] <= cp
    if ends[index] < cp:
        return "None"
    return names[index]

def find_le(a, x):
    '''Return the index of the rightmost value <= x.  Adapted from the
    recipe in python's documentation on the bisect module, section
    8.6.1.
    '''
    index = bisect.bisect_right(a, x)
    if index:
        return index - 1
    return None

def AllowedPythonSymbol(cp):
    '''See if the codepoint cp is allowed in a variable name.  Start
    the name with '_' to allow things like digits.
    '''
    if cp in (9, 12, 32, 35):  # tab, formfeed, space, comment
        return False
    try:
        exec("_%s = 0" % chr(cp))
        return True
    except Exception:
        return False

def DumpCodepointData(cp):
    try:
        group, data = ucd["chars"][cp]
    except KeyError:
        if 0xd800 <= cp <= 0xdfff:
            Error("Codepoint U+%04x illegal" % cp)
        else:
            Error("Codepoint U+%04x not in Unicode Character Database" % cp)
    g = ucd["groups"][group]
    c, i = chr(cp), " "*2
    if cp in (10, 11, 12, 13):
        c = " "
    print("Data on codepoint U+%04X = character %s" % (cp, c))
    print("{i}Decimal = {cp}, octal = {cp:o}, binary = {cp:b}".format(
          i=i, cp=cp))
    if "na" in data and data["na"]:
        print("{0}Name = {1}".format(i, data["na"]))
    if "na1" in data:
        print("{0}Name (alternate) = {1}".format(i, data["na1"]))
    if cp in ucd["aliases"]:
        for a in ucd["aliases"][cp]:
            alias, typ = a["alias"], a["type"]
            print("{0}Alias = {1} (type = {2})".format(i, alias, typ))
    if "age" in g:
        print("{0}Age = {1}".format(i, g["age"]))
    print("{0}Group = {1}".format(i, g["gc"]))
    block = GetBlockName(cp)
    if block is not None:
        print("{0}Block = {1}".format(i, block))
    allowed = "yes" if AllowedPythonSymbol(cp) else "no"
    print("{0}Allowed as python symbol = {1}".format(i, allowed))
    print("{0}Encodings (hex dump format, first byte on left):".format(i))
    encodings = (
        #"utf-7    ",
        "utf-8    ",
        #"utf-8-sig",
        "utf-16   ",
        #"utf-16-be",
        #"utf-16-le",
        "utf-32   ",
        #"utf-32-be",
        #"utf-32-le",
    )
    for enc in encodings:
        print("{0}{0}{1}".format(i, enc), end="  ")
        for b in c.encode(enc):
            print("%02x" % b, end=" ")
        print()
    # If "index" is in ucd, we may have additional information from
    # the CodeCharts.pdf file.
    if "index" in ucd and cp in ucd["index"]:
        print("{0}From CodeCharts.pdf:".format(i))
        for line in ucd["index"][cp]:
            print("{0}{1}".format(2*i, line))

foreign_characters = '''
    AEGEAN      CHEROKEE    HANUNOO     LYCIAN      OSMANYA     SYRIAC
    ALCHEMICAL  CJK         HEBREW      LYDIAN      PAHAWH      TAG
    ARABIC      COPTIC      HEXAGRAM    MAHAJANI    PALMYRENE   TAGALOG
    ARMENIAN    CUNEIFORM   HIRAGANA    MAHJONG     PAU         TAGBANWA
    AVESTAN     CYPRIOT     IDEOGRAPHIC MALAYALAM   PHAGS-PA    TAI
    BALINESE    CYRILLIC    IMPERIAL    MANDAIC     PHAISTOS    TAKRI
    BAMUM       DESERET     JAVANESE    MANICHAEAN  PHOENICIAN  TAMIL
    BASSA       DEVANAGARI  KAITHI      MEETEI      PSALTER     TELUGU
    BATAK       DUPLOYAN    KANGXI      MENDE       REJANG      TETRAGRAM
    BENGALI     EGYPTIAN    KANNADA     MEROITIC    RUMI        THAANA
    BOPOMOFO    ELBASAN     KATAKANA    MIAO        RUNIC       THAI
    BRAHMI      ETHIOPIC    KAYAH       MODI        SAURASHTRA  TIBETAN
    BRAILLE     GEORGIAN    KHAROSHTHI  MONGOLIAN   SHARADA     TIFINAGH
    BUGINESE    GLAGOLITIC  KHMER       MRO         SHAVIAN     TIRHUTA
    BUHID       GOTHIC      KHOJKI      MYANMAR     SIDDHAM     UGARITIC
    BYZANTINE   GRANTHA     KHUDAWADI   NABATAEAN   SINHALA     VAI
    CARIAN                  LAO         NKO         SORA        VEDIC
    CAUCASIAN   GUJARATI    LEPCHA      OGHAM       SUNDANESE   WARANG
    CHAKMA      GURMUKHI    LIMBU       OL          SYLOTI      YI
    CHAM        HANGUL      LISU        ORIYA
'''  # Note I've removed GREEK

def FilterOutForeignCharacters(results, d):
    f = FilterOutForeignCharacters
    if f.r is None:
        s, b = [], "^"
        for i in foreign_characters.split(nl):
            if i.strip():
                s += [b + j.strip() for j in i.split()]
        # Construct regular expression
        t = '|'.join(s)
        f.r = re.compile(t, re.I)
    new_results = []
    for cp, description in results:
        mo = f.r.search(description)
        if not mo:
            new_results.append((cp, description))
    return new_results

FilterOutForeignCharacters.r = None     # Filtering regexp

def Search(regexp, d):
    if regexp.lower().startswith("u+"):
        regexp = regexp[2:]
    # If it's a one-character string, assume we want the information on
    # that particular character.
    if len(regexp) == 1:
        return ord(regexp)
    cp = None if d["-t"] else Int(regexp)
    if cp is not None:
        # It's a valid integer
        return cp
    # It's a string, so compile as a regular expression and search all
    # the codepoint descriptions in ucd.
    r, results = re.compile(regexp, re.I), []
    D = ucd["chars"]
    for cp in D:
        a = D[cp][1]  # The codepoints attributes in XML
        for i in ("na", "na1"):
            if i in a and a[i]:
                mo = r.search(a[i])
                if mo:
                    results.append((cp, a[i]))
        if cp in ucd["aliases"]:
            aliases = ucd["aliases"][cp]
            for alias in aliases:
                mo = r.search(alias["alias"])
                if mo:
                    results.append((cp, alias["alias"]))
    item = 1 if d["-a"] else 0
    reverse = False if d["-a"] else True
    reverse = not reverse if d["-r"] else reverse
    results = sorted(results, key=itemgetter(item), reverse=reverse)
    if not d["-A"]:
        # Filter out most of the foreign language characters
        results = FilterOutForeignCharacters(results, d)
    for cp, line in results:
        print("%04x   %s   %s" % (cp, chr(cp), line))
    return None

def ShowCommon(d):
    chars = []
    for line in common.split(nl):
        loc = line.find("#")
        if loc != -1:
            line = line[:loc].strip()
        if not line:
            continue
        chars.extend(line.split())
    D = ucd["chars"]
    chars = list(set([int(i, 16) for i in chars]))
    chars.sort()
    chars = reversed(chars)
    for cp in chars:
        hx = "{:<5s}".format("{:04x}".format(cp))
        print(hx, chr(cp), "", D[cp][1]["na"].lower())

if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    if d["-c"]:
        ShowCommon(d)
    else:
        regexp, action = args[0], ""
        if len(args) > 1:
            action = args[1]
        cp = Search(regexp, d)
        if cp is not None:
            DumpCodepointData(cp)
            if action:
                if action[0] == "o":
                    OpenPDF(regexp, d)
