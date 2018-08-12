'''

Function to turn a sequence into columns

Run the module as a script to columnize stdin.  Use -h to get a usage
statement.
'''

# Copyright (C) 2012 Don Peterson
# Contact:  gmail.com@someonesdad1

#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#

from __future__ import print_function, division
import os
import re
from pdb import set_trace as xx

if 0:
    import debug
    debug.SetDebugger()

def Columnize(seq, **kw):
    '''Returns a list of strings with the elements of the sequence seq
    (if components are not strings, they will be converted to strings
    using str) formatted in columnar format.  Elements of seq that
    won't fit in a column either generate an exception if trunc is
    False or get truncated if trunc is True.
 
    The keyword arguments are (default values are in square brackets):
 
    align  [left]   How to align the string in each column.  Can be
                    "left" or "<", "center" or "^", or "right" or ">".
 
    col_width [0]   Specify the column width to use.  If nonzero, then
                    this overrides the calculation of the column width.
 
    columns [0]     Number of columns to format the strings into.  If
                    it's zero, it will be figured out from the length
                    of the largest string and the screen width.
 
    esc [True]      Strip out ANSI escape sequences when calculating string
                    lengths.  This allows you to display colored text in
                    columns.
 
    horiz   [False] If True, the sequence is listed from
                    left-to-right; the default is top-to-bottom.  The
                    "shape" of both outputs will be the same.
 
    ignore [False]  If True, return an identity transformation.
 
    indent [None]   If defined, then it is a string to prepend to each
                    line.
 
    sep     [" "]   String to use to separate columns.
 
    to_string [False]  If true, convert the array that would be
                    returned to a single string with the rows
                    separated by newlines.
 
    trunc   [False] If True, truncate a string to get it to fit into a
                    column.  If False, an exception is raised if a
                    string is too long for a column.
 
    width   [0]     Specify the width of the screen.  If it's zero,
                    then get it from the COLUMNS environment variable
                    if it exists; if it doesn't exist, use 79.  If
                    columns is given instead, then width is set to
                    accommodate the desired output.
    '''
    '''
    Implementation details:  the formatting of the left-to-right
    format is straightforward.  The top-to-bottom format is a little
    more difficult.  Here's an example that shows how the algorithm
    was gotten.  Suppose we want to print the numbers in range(18) in
    7 columns of a specified width.  The output will need to look as
    follows, as this shape matches the left-to-right output:
 
        0   3   6   9   12  14  16
        1   4   7   10  13  15  17
        2   5   8   11  .   .   .
 
    where '.' denotes the gap.  The number of full rows is
    int(n/columns) where n = len(seq) and columns is the number of
    columns).  Here, clearly, we need 3 rows to properly print; thus,
    the gap is (rows*columns - n).  Then we need to account for the
    number of numbers to print in each column; the vector for this is
    [3, 3, 3, 3, 2, 2, 2] (see the code for how it's constructed).
    Finally, in the iteration loop, we need to use a correction factor
    for when we append the empty string for the gap rather than a
    sequence element.
    '''
    if not seq:
        return [""]
    # Check keywords
    allowed = set(("align", "col_width", "columns", "esc", "horiz", "ignore",
                   "indent", "sep", "to_string", "trunc", "width",))
    for k in kw:
        if k not in allowed:
            raise ValueError("'%s' is unknown keyword" % k)
    # Get keyword parameters
    align = kw.setdefault("align", "left")
    col_width = abs(int(kw.setdefault("col_width", 0)))
    columns = abs(int(kw.setdefault("columns", 0)))
    esc = kw.setdefault("esc", True)
    horiz = kw.setdefault("horiz", False)
    ignore = kw.setdefault("ignore", False)
    if ignore:
        return [str(i) for i in seq]
    indent = kw.setdefault("indent", None)
    sep = kw.setdefault("sep", " ")
    to_string = kw.setdefault("to_string", False)
    trunc = kw.setdefault("trunc", False)
    width = abs(int(kw.setdefault("width", 0)))
    d = {"left": "<", "right": ">", "center": "^", "<": "<", ">": ">",
         "^": "^"}
    if align not in d:
        raise ValueError("align must be left, right, center, <, >, or ^")
    if indent is not None and not isinstance(indent, str):
        raise ValueError("indent must be a string")
    align = d[align]
    if esc:
        # Regular expression to recognized ANSI escape sequences
        r = re.compile(r"(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]")
        def Len(s):
            '''Returns the length of a string s after removing the escape
            sequences.
            '''
            return len(r.sub("", s))
    else:
        Len = len
    # Turn seq into a sequence of strings
    sseq = [str(i) for i in seq]
    n, maxlen, lsep = len(sseq), max([Len(i) for i in sseq]), len(sep)
    # Pick reasonable defaults if width and columns not given
    if not width :
        if not columns:
            width = 79
            if "COLUMNS" in os.environ:
                width = int(os.environ["COLUMNS"]) - 1
            columns = width//(maxlen + len(sep))
            if not columns:
                msg = "Cannot fit longest string ({} characters) on screen"
                raise ValueError(msg.format(maxlen))
        else:
            if columns < 1:
                raise ValueError("'%s' is bad value for columns" % columns)
            sw = lsep*(columns - 1)
            width = (columns*col_width if col_width else columns*maxlen) + sw
    if indent is not None:
        width -= len(indent)
        if width < 1:
            raise ValueError("indent is too large")
    # Get the number of columns we should print into
    e = ValueError("The width won't allow one column (try trunc=True)")
    if not columns:
        if col_width:
            columns = abs(int(width//(col_width + lsep)))
        else:
            columns = abs(int(width//(maxlen + lsep)))
            col_width = maxlen
    if not col_width:
        col_width = abs(int((width - (columns - 1)*lsep)/columns))
    # Ensure we're below the width of the screen
    total_width = col_width*columns + lsep*(columns - 1)
    while total_width > width:
        columns -= 1
        total_width = col_width*columns + lsep*(columns - 1)
    if not columns and not trunc:
        raise e
    # Set up number of rows and counts of number of items in each
    # column for non-horiz formatting.
    if not columns:
        columns = 1
    rows = int(n//columns) + (n % columns > 0)
    num_in_column, gap = [rows]*columns, rows*columns - n
    # Correct for gap
    for i in range(gap):
        num_in_column[-(i + 1)] -= 1
    if 0:
        nl = "\n"
        print(str(kw) + nl)
        print("screen width  = ", width)
        print("col_width     = ", col_width)
        print("total_width   = ", total_width)
        print("lsep          = ", lsep)
        print("columns       = ", columns)
        print("rows          = ", rows)
        print("gap           = ", rows*columns - n)
        print("num_in_column = ", num_in_column)
        print()
    s, fmt = [], "{0:" + align + str(col_width) + "}"
    I = indent if indent is not None else ""
    if horiz:
        for i, item in enumerate(sseq):
            row, col = divmod(i, columns)
            if not col:
                srow = []  # Start a new row
            item = fmt.format(item)
            if not trunc and Len(item) > col_width:
                msg = "'%s' too long for formatting" % item
                raise ValueError(msg)
            srow.append(item[:col_width] if trunc else item)
            if col >= columns - 1:
                s.append(sep.join(srow))
                srow = []
        if srow:
            s.append(sep.join(srow))
        s = [I + i for i in s]
    else:
        # Construct each column.  We use a correction to account for
        # columns that don't require the full number of rows; this
        # ensures that we iterate over all items in sseq.
        cols, correction = [], 0
        for col in range(columns):
            scol = []  # Start a new column
            for row in range(rows):
                # Get index into sseq
                i = col*rows + row
                if i > n - 1 + correction or row >= num_in_column[col]:
                    item = ""
                    correction += 1
                else:
                    item = sseq[i - correction]
                item = fmt.format(item)
                if not trunc and Len(item) > col_width:
                    msg = "'%s' too long for formatting" % item
                    raise ValueError(msg)
                # Append spaces if Len is < col_width
                if Len(item) < col_width:
                    item += " "*(col_width - Len(item))
                # Note truncation may damage ANSI sequences in some
                # cases.
                scol.append(item[:col_width] if trunc else item)
            cols.append(scol)
        # Get transpose of the just-constructed matrix
        mat = []
        for i in range(rows):
            mat.append([""]*columns)
        for col in range(columns):
            for row in range(rows):
                mat[row][col] = cols[col][row]
        # Now build an array of the row strings
        for i in mat:
            s.append(I + sep.join(i))
    # Remove trailing spaces
    for i, x in enumerate(s):
        s[i] = x.rstrip()
    if to_string:
        s = "\n".join(s)
    return s

if __name__ == "__main__":
    # Running as a script provides a utility similar to pr.
    import sys
    import getopt
    err = sys.stderr.write
    nl = "\n"
    requested_columns = 0
    column_width = 0
    alignment = "left"
    separator = " "
    truncate = False
    def Usage(status=1):
        name = sys.argv[0]
        print('''
Usage:  %(name)s [options] [file1 ...]
  Prints in columns.  The number of columns is made a maximum to fit
  into the current screen width given in the COLUMNS environment
  variable less one character.  If no files are given on the command
  line, input is taken from stdin.
 
Options
    -a s
        Align each column as indicated by s:  left or <, center or ^,
        right or >.
    -c n
        Force number of columns to be n.  Resulting line length
        ignores COLUMNS; no strings are truncated.
    -e
        Ignore ANSI escape sequences (e.g., terminal color codes).
    -f
        Adjust column width and number of columns to attempt to get
        the output within the given number of LINES and COLUMNS.
    -h
        Print this help message
    -i s
        Indent each output line with the string s.
    -s s
        Separate each column with the string s.
    -t
        Truncate each string if needed to fit into the column width.
    -w n
        Set the column width.'''[1:] % locals())
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = "left"        # Alignment
        d["-c"] = 0             # Requested number of columns
        d["-e"] = False         # Ignore ANSI escape sequences
        d["-f"] = False         # Fit into available screen
        d["-i"] = None          # Indent string
        d["-s"] = " "           # Separator
        d["-t"] = False         # Truncate
        d["-w"] = 0             # Column width
        try:
            optlist, args = getopt.getopt(sys.argv[1:], "a:c:efhi:s:tw:")
        except getopt.GetoptError as str:
            msg, option = str
            print(msg)
            exit(1)
        for o, a in optlist:
            if o == "-a":
                d["-a"] = a
            elif o == "-c":
                d["-c"] = int(a)
                if d["-c"] <= 0:
                    err("Number of columns must be > 0" + nl)
                    exit(1)
            elif o == "-e":
                d["-e"] = not d["-e"]
            elif o == "-f":
                d["-f"] = not d["-f"]
            elif o == "-h":
                Usage(0)
            elif o == "-i":
                d["-i"] = a
            elif o == "-s":
                d["-s"] = a
            elif o == "-t":
                d["-t"] = not d["-t"]
            elif o == "-w":
                d["-w"] = abs(int(a))
        return args
    def GetInput(files):
        if not files:
            lines = [i.rstrip() for i in sys.stdin.readlines()]
        else:
            lines = []
            for file in files:
                lines += [i.rstrip() for i in open(file).readlines()]
        return lines
    def Fit(lines, d):
        '''Find out how many LINES and COLUMNS we have for the screen.
        Then adjust the parameters to Columnize to get the lines to
        fit on the screen; truncate as necessary.
 
        The basic task will be to get the resulting lines of the
        output to fit into LINES - 3 lines, as I use a prompt of 2
        lines (this lets me see an empty line at top, so that I know
        something hasn't scrolled off screen).  The canonical example
        of use of this feature is to get a long ls listing to fit on
        the screen.
        '''
        separator = " "
        width = int(os.environ["COLUMNS"]) - 1
        length = int(os.environ["LINES"]) - 2
        maxlen = max([len(i) for i in lines])
        n = int(len(lines)//length)
        # Calculate truncation.  The formula for total width W is
        # n*cw+(n-1)*sep where n is number of columns, cw is column
        # width, and sep is the length of the separator.  This solves
        # to give cw = (W - (n-1)*sep)/n.
        cw = int((width - (n - 1)*len(separator))/n)
        msg = "Can't fit the requested information"
        assert cw > 0, msg
        kw = {
            "align"     : d["-a"],
            "col_width" : cw,
            "esc"       : d["-e"],
            "sep"       : separator,
            "trunc"     : True,
            "width"     : width,
        }
        s = Columnize(lines, **kw)
        while len(s) > length:
            kw["col_width"] -= 1
            assert kw["col_width"] > 1, msg
            s = Columnize(lines, **kw)
        for i in s:
            print(i)
        exit(0)
    d = {}
    files = ParseCommandLine(d)
    lines = GetInput(files)
    if d["-f"]:
        Fit(lines, d)
    else:
        if d["-c"]:
            kw = {
                "align"     : d["-a"],
                "col_width" : d["-w"],
                "columns"   : d["-c"],
                "esc"       : d["-e"],
                "indent"    : d["-i"],
                "sep"       : d["-s"],
                "trunc"     : d["-t"],
            }
        else:
            kw = {
                "align"     : d["-a"],
                "col_width" : d["-w"],
                "esc"       : d["-e"],
                "indent"    : d["-i"],
                "sep"       : d["-s"],
                "trunc"     : d["-t"],
                "width"     : int(os.environ["COLUMNS"]) - 1,
            }
        s = Columnize(lines, **kw)
        for i in s:
            print(i)
