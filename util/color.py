'''
Contains functions to set screen color for console applications

There are 16 colors given by names:  black, blue, green, cyan, red,
magenta, brown, white, gray, lblue, lgreen, lcyan, lred, lmagenta,
yellow, and lwhite.

The primary function is fg(), which can be used in the following ways
to set the foreground and background colors:

    fg(white)
        Sets the foreground color to white and leaves the background
        unchanged.
    fg(white, black)
        Sets the foreground color to white and the background to
        black.
    fg((white, black)) or fg([white, black])
        Same as previous call.
    fg(color_byte)
        Sets the foreground and background colors by using the number
        color_byte.  The low nibble gives the foreground color and the
        high nibble gives the background color

The normal() function sets the foreground and background colors back
to their normal values.  Call with arguments the same as fg() to
define the normal foreground and background colors.  Set the
default_colors global variable to the default colors you use.

A ColorContext instance is useful as a context manager to ensure that 
you have normal colors enabled when your script exits.  See the example
at the end of the file.

These functions should work on both Windows and an environment that
uses ANSI escape sequences (e.g., an xterm).

PrintMatch()
PrintMatches()

    These two functions can be used to print color annotations of regular
    expression matches in strings being printed to the console.  I find
    PrintMatch() very helpful when developing a complicated regular
    expression.  Here's an example of how I'd use it in a python script:

    r = re.compile(r"<your regular expression here", re.S)

    # Colorize where the regexp r matches in the file
    s = open(file).read()
    print("-"*70)
    PrintMatch(s, r)
    print("-"*70)
    print()
    # Show the group matches
    mo = r.search(s)
    if mo:
        print("Groups:")
        for i, g in enumerate(mo.groups()):
            print("[{}]:  {}\n".format(i, g))

The Decorate() object is a convenience; an instance of it will return the
escape strings to set the console colors.  An example use would be

    dec = Decorate()
    print("Hello", dec.fg(dec.lred), " there", dec.normal(), sep="")

which would print the word "there" in light red.

The code for Windows console colors was taken from Andre Burgaud's work at
http://www.burgaud.com/bring-colors-to-the-windows-console-with-python/,
downloaded Wed 28 May 2014.

---------------------------------------------------------------------------
Some ANSI control codes for attributes that have an effect in xterms:
    Esc[0m  Attributes off
    Esc[1m  Bold
    Esc[3m  Italics
    Esc[4m  Underline
    Esc[5m  Blinking
    Esc[7m  Reverse video

---------------------------------------------------------------------------
If this module is not available, put the following in your code so that
things will still work.

# Try to import the color.py module; if not available, the script
# should still work (you'll just get uncolored output).
try:
    import color
    _have_color = True
except ImportError:
    # Make a dummy color object to swallow function calls
    class Dummy:
        def fg(self, *p, **kw): pass
        def normal(self, *p, **kw): pass
        def __getattr__(self, name): pass
    color = Dummy()
    _have_color = False

'''

# Copyright (C) 2014 Don Peterson
# Contact:  gmail.com@someonesdad1

#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#

from __future__ import print_function
import os
import sys
from collections.abc import Iterable
from itertools import combinations, permutations
from pdb import set_trace as xx

py3 = sys.version_info[0] == 3
if py3:
    String = (str,)
    Int = (int,)
else:
    String = (str, unicode)
    Int = (int, long)

# To use this under the old cygwin bash, which was derived from a Windows
# console, you must define the environment variable BASH_IS_WIN_CONSOLE.
# The new cygwin bash window is based on mintty and accepts ANSI escape
# codes directly.
bash_is_win_console = os.environ.get("BASH_IS_WIN_CONSOLE", False)
_win = True if (sys.platform == "win32") and bash_is_win_console else False

__all__ = '''
    black blue  green  cyan  red  magenta  brown  white 
    gray  lblue lgreen lcyan lred lmagenta yellow lwhite

    default_colors
    normal
    fg
    SetStyle
    Decorate
    Style
    PrintMatch
    PrintMatches
'''.replace("\n", " ").split()

if _win:
    from ctypes import windll

# Foreground colors; shift left by 4 bits to get background color.
(
    black, blue,  green,  cyan,  red,  magenta,  brown,  white,
    gray,  lblue, lgreen, lcyan, lred, lmagenta, yellow, lwhite
) = range(16)

# Set the default_colors global variable to be the defaults for your system.
default_colors = (white, black)

# Dictionary to translate between color numbers/names and escape sequence.
_cfg = {
    black    : "0;30",
    blue     : "0;34",
    green    : "0;32",
    cyan     : "0;36",
    red      : "0;31",
    magenta  : "0;35",
    brown    : "0;33",
    white    : "0;37",
    gray     : "1;30",
    lblue    : "1;34",
    lgreen   : "1;32",
    lcyan    : "1;36",
    lred     : "1;31",
    lmagenta : "1;35",
    yellow   : "1;33",
    lwhite   : "1;37",
}
_cbg = {
    black    : "40m",
    blue     : "44m",
    green    : "42m",
    cyan     : "46m",
    red      : "41m",
    magenta  : "45m",
    brown    : "43m",
    white    : "47m",
    gray     : "40m",
    lblue    : "44m",
    lgreen   : "42m",
    lcyan    : "46m",
    lred     : "41m",
    lmagenta : "45m",
    yellow   : "43m",
    lwhite   : "47m",
}

# Handle to call into Windows DLL
STD_OUTPUT_HANDLE = -11
_hstdout = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE) if _win else None

def _is_iterable(x):
    '''Return True if x is an iterable that isn't a string.
    '''
    return isinstance(x, Iterable) and not isinstance(x, String)

def _DecodeColor(*c):
    '''Return a 1-byte integer that represents the foreground and
    background color.  c can be
        * An integer
        * Two integers
        * A sequence of two integers
    '''
    if len(c) == 1:
        # It can either be a number or a tuple of two integers
        if _is_iterable(c[0]):
            if len(c[0]) != 2:
                raise ValueError("Must be a sequence of two integers")
            color = ((c[0][1] << 4) | c[0][0]) & 0xff
        else:
            if not isinstance(c[0], Int):
                raise ValueError("Argument must be an integer")
            color = c[0] & 0xff
    elif len(c) == 2:
        color = ((c[1] << 4) | c[0]) & 0xff
    else:
        raise ValueError("Argument must be one or two integers")
    return color

def _GetNibbles(c):
    assert 0 <= c < 256
    return (0x0f & c, (0xf0 & c) >> 4)

def normal(*p, **kw):
    '''If the argument is None, set the foreground and background
    colors to their default values.  Otherwise, use the argument to
    set the default colors.

    If keyword 's' is True, return a string instead of printing.
    '''
    ret_string = kw.setdefault("s", False)
    global default_colors
    if p:
        one_byte_color = _DecodeColor(*p)
        default_colors = _GetNibbles(one_byte_color)
    else:
        if ret_string:
            return fg(default_colors, **kw)
        else:
            fg(default_colors, **kw)

def fg(*p, **kw):
    '''Set the color.  p can be an integer or a tuple of two
    integers.  If it is an integer that is greater than 15, then it
    also contains the background color encoded in the high nibble.
    fgcolor can be a sequence of two integers of length two also.
 
    The keyword 'style' can be:
        normal
        italic
        underline
        blink
        reverse
 
    If the keyword 's' is True, return a string containing the escape
    codes rather than printing it.  Note this won't work if _win is True.
    '''
    style = kw.setdefault("style", None)
    ret_string = kw.setdefault("s", False)
    one_byte_color = _DecodeColor(*p)
    if _win:
        windll.kernel32.SetConsoleTextAttribute(_hstdout, one_byte_color)
    else:
        # Use ANSI escape sequences
        cfg, cbg = _GetNibbles(one_byte_color)
        f, b = _cfg[cfg], _cbg[cbg]
        s = "\x1b[%s;%s" % (f, b)
        if not ret_string:
            print(s, end="")
        if style is not None:
            if ret_string:
                st = SetStyle(style, **kw)
                return s + st
            else:
                SetStyle(style)
        elif ret_string:
            return s

def SetStyle(style, **kw):
    '''If the keyword 's' is True, return a string containing the escape
    codes rather than printing it.  Note this won't work if _win is True.
    '''
    ret_string = kw.setdefault("s", False)
    if _win:
        return
    st = {
        "normal" : 0, "bold" : 1, "italic" : 3, "underline" : 4,
        "blink" : 5, "reverse" : 7,
    }[style]
    if ret_string:
        return "\x1b[%sm" % st
    else:
        print("\x1b[%sm" % st, end="")

class Decorate(object):
    '''A convenience object that will return escape code strings.
    '''
    def __init__(self):
        # Make colors an attribute
        self.black = black
        self.blue = blue
        self.green = green
        self.cyan = cyan
        self.red = red
        self.magenta = magenta
        self.brown = brown
        self.white = white
        self.gray = gray
        self.lblue = lblue
        self.lgreen = lgreen
        self.lcyan = lcyan
        self.lred = lred
        self.lmagenta = lmagenta
        self.yellow = yellow
        self.lwhite = lwhite
        self.kw = {"s": True}
    def fg(self, *p):
        return fg(*p, **self.kw)
    def normal(self, *p):
        return normal(*p, **self.kw)
    def SetStyle(self, style):
        return SetStyle(style, **self.kw)

class Style(object):
    '''Defines foreground and background colors and a particular text style
    (such as bold, italic, etc.).  The class is intended to be a
    convenience container for color information.  Note the escape codes are
    always printed to stdout; use class Decorate if you want the strings
    with the escape codes.
    '''
    def __init__(self, fg=default_colors[0], 
                 bg=default_colors[1], style="normal"):
        self.fg = fg
        self.bg = bg
        self.style = style
    def set(self):
        '''Print our escape codes to stdout.
        '''
        fg(self.fg, self.bg)
        if self.style != "normal":
            # This logic is used because the 'normal' style will undo any
            # foreground color set.
            SetStyle(self.style)
    @classmethod
    def clear(self):
        '''Print the normal style escape codes to stdout.
        '''
        normal()

class ColorContext:
    '''Context manager to ensure the screen colors are reset to desired
    values when the manager exits.
    '''
    def __init__(self, foreground=None, background=None):
        '''If foreground and background are None, the default colors are
        used.
        '''
        self.foreground = foreground
        self.background = background
    def __enter__(self):
        pass
    def __exit__(self, type, value, traceback):
        if self.foreground is None and self.background is None:
            normal()
        if self.foreground is None:
            f = default_colors[0]
        if self.background is None:
            b = default_colors[1]
        fg(f, b)

def PrintMatch(text, regexp, style=Style(yellow, black)):
    '''Print the indicated text in normal colors if there are no matches to
    the regular expression.  If there are matches, print each of them in
    the indicated style.  text can be a multiline string.
    '''
    def out(s):
        print(s, end="")
    mo = regexp.search(text)
    if not mo:
        normal()
        print(text)
        return
    text = mo.string
    while text:
        style.clear()
        out(text[:mo.start()])      # Print non-matching start stuff
        style.set()
        out(text[mo.start():mo.end()])  # Print the match in color
        style.clear()
        # Use the remaining substring
        text = text[mo.end():]
        mo = regexp.search(text)
        if not mo:
            out(text + "\n")
            return

def PrintMatches(line, regexps):
    '''Given a line of text, search for regular expression matches given in
    the sequence of regexps, which contain pairs of regular expressions and
    Style objects, then print the line to stdout with the indicated styles.
    '''
    def out(s):
        print(s, end="")
    def GetShortestMatch(text):
        '''Return (start, end, style) of the earliest match or (None, None,
        None) if there were no matches.
        '''
        matches = []
        for r, style in regexps:
            mo = r.search(line)
            if mo:
                matches.append([mo.start(), mo.end(), style])
        return sorted(matches)[0] if matches else (None, None, None)
    while line:
        start, end, style = GetShortestMatch(line)
        if start is None:
            out(line)           # No matches so print remainder
            return
        style.clear()
        out(line[:start])       # Print non-matching start stuff
        style.set()
        out(line[start:end])    # Print match in chosen style
        style.clear()
        line = line[end:]       # Use the remaining substring

if __name__ == "__main__":
    # Display a table of the color combinations
    names = {
        black    : "black",
        blue     : "blue",
        green    : "green",
        cyan     : "cyan",
        red      : "red",
        magenta  : "magenta",
        brown    : "brown",
        gray     : "gray",
        white    : "white",
        lblue    : "lblue",
        lgreen   : "lgreen",
        lcyan    : "lcyan",
        lred     : "lred",
        lmagenta : "lmagenta",
        yellow   : "yellow",
        lwhite   : "lwhite",
    }
    low = [black, blue, green, cyan, red, magenta, brown, white]
    high = [gray, lblue, lgreen, lcyan, lred, lmagenta, yellow, lwhite]
    # Print title
    fg(yellow)
    msg = ("%s Text Colors" % __file__).center(79)
    print(msg)
    back = "Background --> "
    msg = " black   blue    green   cyan    red    magenta  brown   white"
    fg(lcyan)
    print(back + msg)
    def Table(bgcolors):
        for fgcolor in low + high:
            normal()
            s = names[fgcolor] + " (" + str(fgcolor) + ")"
            print("%-15s" % s, end="")
            for bgcolor in bgcolors:
                fg(fgcolor, bgcolor)
                c = (0xf0 & (bgcolor << 4)) | (0x0f & fgcolor)
                print("wxyz %02x" % c, end="")
                normal()
                print(" ", end="")
            normal()
            print()
    Table(low)
    msg = " gray    lblue   lgreen  lcyan   lred  lmagenta yellow  lWhite"
    fg(lcyan)
    print("\n" + back + msg)
    Table(high)
    # Print in different styles
    print("Styles:  ", end="")
    for i in ("normal", "bold", "italic", "underline", "blink", "reverse"):
        fg(white, style=i)
        print(i, end="")
        SetStyle("normal")
        print(" ", end="")
    fg(white)
    print()

    print("Demo of ColorContext object:")
    with ColorContext():
        s = Style(fg=yellow, style="italic")
        s.set()
        print("  In yellow italics")
    print("  Back to normal")
