'''
Bugs

    * .define 44 888 =xxxxx
    44888
        produces the output
    xxxxx888
    The space in the name should be an error or the whole thing should
    be used.

A text substitution tool
    Print the man page (mp.py -h) for details.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2002 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # A text substitution tool
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import string
    import sys
    import os
    import re
    from pdb import set_trace as xx 
if 1:   # Custom imports
    from wrap import dedent
if 1:   # Global variables
    script = os.path.split(sys.argv[0])[1]
    verbose = 0                 # Log to stderr if true
    dump_macros = 0
    special_char = "."
    files_to_process = None
    output_on = 1
    current_file = ""
    current_line = 0
    macros = {}
    macro_names = []
    start_dir = os.getcwd()
    cmd_char = "."              # Character that denotes a command line
    include_dirs = []           # Where to search for include files
    included_files = {}         # Which files have already been included
    # Globals to help with evaluating chunks of code
    code_mode = 0               # If true, we're in a code section
    current_code = ""           # String to hold the code lines
    code_names = {}             # Keep track of named sections of code
    # The following regular expression is used to identify lines that contain
    # formatting strings that need to be expanded with the global dictionary.
    need_global_expansion = re.compile(r"%\(([a-zA-Z][a-zA-Z_]*)\)")
    #
    special_macros = '''
    mp_NowDateDMY     Is the current date in DD MMM YYYY format.
    mp_NowDateDD      Is the current date's day in DD form.
    mp_NowDateMM      Is the current date's month in MM (01-12) form.
    mp_NowDateMONTH   Is the current date's month in MMM (Jan-Dec) form.
    mp_NowDateYY      Is the current date's year in YY form.
    mp_NowDateYEAR    Is the current date's year in YYYY form.
    mp_NowTimeHMS     Is the current time in HH:MM:SS AM/PM format.
    mp_NowTimeHH      Is the current time's hour in 24 hour format
    mp_NowTime12HH    Is the current time's hour in 12 hour format
    mp_NowTimeMM      Is the current time's minute (00-59)
    mp_NowTimeSS      Is the current time's second (00-59)
    mp_NowTimeAMPM    Is the current time's AM or PM designator
    mp_GPL_txt        The GNU General Public License Notice (text)
    mp_GPL_html       The GNU General Public License Notice (html)'''[1:]

    GPL_txt = dedent('''This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License as
    published by the Free Software Foundation; either version 2 of
    the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public
    License along with this program; if not, write to the Free
    Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
    MA  02111-1307  USA

    See http://www.gnu.org/licenses/licenses.html for more details.''')
    gnu_url = "http://www.gnu.org/licenses/licenses.html"
    GPL_html = dedent(f'''
    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License as
    published by the Free Software Foundation; either version 2 of
    the License, or (at your option) any later version.<p>

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.<p>

    You should have received a copy of the GNU General Public
    License along with this program; if not, write to the Free
    Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
    MA  02111-1307  USA<p>

    See <a href="{gnu_url}">{gnu_url}</a> for more details.
    ''')
    del gnu_url
def Usage():
    print(dedent(f'''
    Usage:  {sys.argv[0]} [options] file1 [file2...]
      General-purpose macro processor (really, a text substitution tool).
    Options
      -d      Print list of macro definitions found in files
      -h      Print a man page
      -I dir  Define an include directory
    Command lines have the form (whitespace after '.' optional):
        .  command [parameters]
        .. command [parameters]       Macros not expanded in line
    Commands:
        define Macro = Value          Define a new macro
        #                             This line is a comment
        on                            Turn output on
        off                           Turn output off
        code [name]                   Define a [named] section of python code
        endcode                       End of python code section
        include                       Insert a file; error if not found
        sinclude                      Insert a file; no error if not found
        cd [dir]                      Change the current directory
    Special macros'''))
    for i in special_macros.split("\n"):
        print(i)
def ManPage():
    name = sys.argv[0]
    print(dedent(f'''
    NAME
        {name} - Macro processor

    SYNOPSIS
        {name} [options] file1 [file2...]
    
    DESCRIPTION
    
        The {name} script is intended to be used as a macro processor.
        It is primarily a string substitution tool.  However, since it is
        implemented in python, it allows the use of arbitrary python code
        in your text files.
    
        {name} replaces strings in the input files, then prints them
        to stdout.  It knows nothing about things like identifiers or
        tokens in programming languages.  It's a dumb text substitution
        program.  For each line of input, it searches to see if a macro
        name occurs on that line; if it does, then the text is replaced.
        The search starts with the longest macro names and goes to the
        shorter names.  This lets you have two macros named 'mp_MyMacro4'
        and 'mp_MyMacro' and not have mp_MyMacro's value replaced when the
        macro name mp_MyMacro4 occurs in text.
        
        Thus, you must make sure your macro names will not be found in
        text except where you deliberately put them in.  One possible way
        to accomplish this is to name all your macros with a prefix such
        as "mp_".
    
        Programmers probably expect macro names and other things to be
        processed in tokens like other macro tools such as m4.  The
        {name} script doesn't behave this way; it's just no-brainer 
        text substitution.
    
        You can add built-in macros to the script by editting the
        BuildSpecialMacros() function.
    
    Options
        -d
            Print a list of macro definitions found in the input files to
            stdout.
        -h
            Prints this man page.
        -I dir
            Define an include directory.  When a file is included, it
            is first looked for in the current directory (or the
            indicated directory).  If it cannot be found, directories
            specified with the -I option are searched sequentially
            and the first match is used.  More than one -I option
            can be given.
    
    Command lines
        Command lines to the macro processor have a '.' character in the
        first column.  You can edit the IsCommandLine() function in the
        script if you'd like to change this syntax.
    
        The general forms of a command are:
            
            .  token [token's arguments]
            .. token [token's arguments]
    
        There can be optional whitespace between the '.' character and
        the characters of the token.
    
        Note that command lines have embedded macros expanded in them.
        This e.g. allows you to write
    
            .define mp_MY_FILE =abc
            .include mp_MY_FILE
    
        If you do not want macros expanded in the line, use the '..'
        form.
    
        The allowed command tokens are:
    
        .define macro = value
            Defines the value of a macro.  All characters after the '='
            character become part of the macro's value, except for the
            newline.
    
        .cd dir
            Set the current directory of the macro processor to dir.
            If dir is missing, the current directory is set to what it
            was at the start of the script.
    
        .code [code_section_name]
        .endcode
            These two tokens must appear on a line by themselves.  They
            delimit lines of text that will be interpreted as python
            code.  Typically, this is used to define and set some global
            variables that are used for variable expansions in lines.
            See the Examples section below for details.  However,
            arbitrary processing can be done.  Any variables that you
            define in your code section are added to the global variable
            namespace of the {name} script.
    
            If code_section_name is given, it must be encountered only
            once while processing, otherwise an error will occur and
            processing stops.  You can use this feature to avoid
            accidentally including files multiple times (if your code
            in the included file has a name, the {name} script will
            stop executing the second time it is included).
    
        .include file [once]
            Used to include another file at this point.  The behavior is
            to read all the lines of the indicated file and insert them
            at the current location.  It is a fatal error if the file
            cannot be found.
    
            If the token 'once' is present, the file is only included
            once.  This is intended to be used where the include file
            has python code/endcode chunks that you only want executed
            once.
    
        .sinclude file [once]
            Same as include, except it's not an error if the file cannot
            be found.
    
            If the token 'once' is present, the file is only included
            once.  This is intended to be used where the include file
            has python code/endcode chunks that you only want executed
            once.
    
        .#
            If this character follows the command line string (with optional
            preceding whitespace), the line is considered a comment and the
            line as a whole is discarded.
    
        .on
            Turns macro substitution back on if it was off.  Ignored if it is
            already on.
    
        .off
            Turns macro substitution off.  Ignored if it is already off.
    
    Built-in macros
        There are some built-in macros:'''))
    for i in special_macros.split("\n"):
        print(i)
    print(dedent(f'''
    Python variables
        You may use python variable references in your text.  These references
        must be of the form '%%(varname)s', where varname is the name of a
        python variable and s is a formatting string, such as 's', 'd', 'f',
        etc.  These expressions will be evaluated with the global dictionary
        in effect at the time the code is evaluated.
    
        Typical use of this functionality is to make a counter that gets
        incremented or to define multiline strings.
    
    Example
        The following example shows a simple use of python code to
        generate serial numbers for a set of files.  The idea is that the
        serial numbers will be incremented each time they are referenced,
        allowing a set of files to have unique numbers.
    
        File 1 contains:
            .code
            sn = 100 # Starting serial number
            def IncrementSerialNumber():
                global sn
                sn += 1
            .endcode
            This is file 1.  The serial number is %%(sn)d.
            .code
            IncrementSerialNumber()
            .endcode
        
        File 2 contains:
            This is file 2.  The serial number is %%(sn)d.
            .code
            IncrementSerialNumber()
            .endcode
    
        Running the command
    
            python mp.py 1 2
            
        produces the output:
    
            This is file 1.  The serial number is 100.
            This is file 2.  The serial number is 101.
    
        Note:  any global variables and functions you define in your code
        will be put into the {name} script's global namespace.
    '''))
def Log(st):
    if verbose:
        print("+ " + st, file=sys.stderr)
def Initialize():
    global files_to_process
    import getopt
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "dhI:v")
    except getopt.error as st:
        print("getopt error:  %s\n" % st)
        sys.exit(1)
    for opt in optlist:
        if opt[0] == "-d":
            global dump_macros
            dump_macros = 1
        if opt[0] == "-v":
            global verbose
            verbose = 1
        if opt[0] == "-h":
            ManPage()
            sys.exit(0)
        if opt[0] == "-I":
            global include_dirs
            include_dirs.append(opt[1])
    files_to_process = args
    if len(files_to_process) == 0:
        Usage()
    Log("dump_macros        = %d\n" % dump_macros)
    Log("verbose            = %d\n" % verbose)
    Log("files_to_process   = %s\n" % str(files_to_process))
    Log("-" * 70 + "\n")
    BuildSpecialMacros()
    assert(len(cmd_char) == 1)
def BuildSpecialMacros():
    '''Construct the special macros used by the script.  Edit this
    function as needed to add your own built-in macros.
    '''
    global macros, macro_names
    import time
    tm = time.localtime(time.time())
    settings = [
        ["mp_NowDateDMY",    "%d %b %Y"],
        ["mp_NowDateDD",     "%d"],
        ["mp_NowDateMM",     "%m"],
        ["mp_NowDateMONTH",  "%b"],
        ["mp_NowDateYY",     "%y"],
        ["mp_NowDateYEAR",   "%Y"],
        ["mp_NowTimeHMS",    "%H:%M:%S"],
        ["mp_NowTimeHH",     "%H"],
        ["mp_NowTime12HH",   "%I"],
        ["mp_NowTimeMM",     "%M"],
        ["mp_NowTimeSS",     "%S"],
        ["mp_NowTimeAMPM",   "%p"],
    ]
    for setting in settings:
        key = setting[0]
        value = [time.strftime(setting[1], tm), 0, ""]
        macros[key] = value
        if verbose:
            Log("%-20s %s\n" % (key, value))
    # Add the GPL macros.
    macros["mp_GPL_txt"] = [GPL_txt,  0, ""]
    macros["mp_GPL_html"] = [GPL_html, 0, ""]
    macro_names = macros.keys()
    SortMacroNames()
def SortMacroNames():
    '''Decorate and sort the macro names so that the longest macros
    are first.  This lets macros like 'mp_MyMacro4' get substituted
    before 'mp_MyMacro', giving the behavior most of us would expect.
    '''
    global macro_names
    s = [(len(i), i) for i in macro_names]
    s.sort()
    macro_names = [i[1] for i in list(reversed(s))]
def Error(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)
def ProcessCommandLine(line):
    '''The line is a command line, so parse out the command and execute
    it.  If we're in code mode, the line is appended to the current_code
    string.
    '''
    global output_on, macros, macro_names
    global code_mode, current_code, codes_names
    if len(line) > 2 and line[:2] != "..":
        line = ExpandMacros(line)
    else:
        line = line[1:]
    # If we're in code mode, just append the line to current_code and return
    # (unless we're at the code end).
    if code_mode and line[0] != cmd_char:
        Log("Code line: " + line)
        current_code = current_code + line
        return
    st = string.strip(line[1:])
    if len(st) == 0:
        return
    fields = string.split(st)
    Log("Command line: " + line)
    if len(fields) == 0:
        return
    cmd = fields[0]
    if cmd == "define":
        if len(fields) < 3:
            Error("Too few fields in line %d of file '%s'\n" %
                  (current_line, current_file))
        macro_name = fields[1]
        loc_eq = string.find(line, "=")
        if loc_eq < 0:
            Error("Missing '=' in line %d of file '%s'\n" %
                  (current_line, current_file))
        macro_value = line[loc_eq+1:]
        # Remove the trailing newline if it is present
        if macro_value[-1] == "\n":
            macro_value = macro_value[:-1]
        if dump_macros:
            print("%s = '%s'\n" % (macro_name, macro_value))
        if macro_name in macros:
            m = ["Warning:  redefining macro name '%s' in line %d "
                 "of file '%s'\n" %
                 (macro_name, current_line, current_file)]
            m += ["          Previous definition at line %d of file '%s'\n"
                  % (macros[macro_name][1], macros[macro_name][2])]
            print(''.join(m), file=sys.stderr)
        macros[macro_name] = [macro_value, current_line, current_file]
        macro_names = macros.keys()
        SortMacroNames()
        Log("Defined %s to '%s'\n" % (macro_name, macro_value))
    elif cmd == "code":
        # Beginning of a code section.  If it's got a name, let's make
        # sure it hasn't been executed before.
        if len(fields) > 1:
            # It's got a name
            code_name = fields[1]
            if code_name in code_names:
                m = ["Error:  code section named '%s' at line %d of file "
                     "'%s' already defined\n" %
                     (code_name, curr_line, curr_file)]
                m += ["Previous definition line %d in file '%s'\n" %
                      (code_names[code_name][0], code_names[code_name][1])]
                Error(''.join(m))
            else:
                # Add it to the dictionary
                code_names[code_name] = [curr_line, curr_file]
        # Flag that we're now reading code
        code_mode = 1
    elif cmd == "endcode":
        # End of a code section.  Compile and execute the code.
        if not code_mode:
            Error("Error:  endcode at line %d of file '%s' missing "
                  "a matching previous 'code' token\n" %
                  (curr_line, curr_file))
        code_mode = 0
        # Compile and execute.  If we get an exception, the user will
        # know about where the problem is because the file and line
        # number of the endcode statement will be in the traceback.
        loc = "[%s:%d]" % (current_file, current_line)
        co = compile(current_code, loc, "exec")
        exec(co)
        # Save our variables in the global namespace, but remove this
        # function's locals.
        code_variables = locals()
        vars = ["loc", "co", "st", "fields", "line", "cmd"]
        for var in vars:
            del code_variables[var]
        # Now add these to the global dictionary
        g = globals()
        for varname in code_variables.keys():
            g[varname] = code_variables[varname]
    elif cmd == "cd":
        if len(fields) > 1:
            os.chdir(fields[1])
        else:
            os.chdir(start_dir)
    elif cmd[0] == "#":
        # It's a comment - ignore it
        pass
    elif cmd == "on":
        output_on = 1
    elif cmd == "off":
        output_on = 0
    elif cmd == "include":
        if len(fields) < 2:
            Error("Bad include in line %d of file '%s':  missing file\n" %
                  (current_line, current_file))
        file = FindIncludeFile(fields[1])
        if len(fields) > 2:
            once = 1
            if fields[2] != "once":
                Error("Bad include in line %d of file '%s':  third "
                      "token must be 'once'\n" %
                      (current_line, current_file))
        else:
            once = 0
        if file == "":
            Error("Error:  include file '%s' in line %d of file '%s' "
                  "not found\n" %
                  (fields[1], current_line, current_file))
        if once:
            if file not in included_files:
                ProcessFile(file, 0, current_line, current_file)
        else:
            ProcessFile(file, 0, current_line, current_file)
        included_files[file] = 0
    elif cmd == "sinclude":
        if len(fields) != 2:
            Error("Bad sinclude in line %d of file '%s'\n" %
                  (current_line, current_file))
        file = FindIncludeFile(fields[1])
        ProcessFile(file, 1, current_line, current_file)
    else:
        Error("Command '%s' on line %d of file '%s' not recognized\n" %
              (cmd, current_line, current_file))
def FindIncludeFile(file):
    '''Search for the indicated file.  If it is an absolute path, just
    return it.  If it is a relative path, first try the current directory,
    then the directories in the include_dirs list.  If it is not found,
    return an empty string.  Otherwise return the full path name.
    '''
    import os
    if os.path.isfile(file):
        path = os.path.normcase(os.path.abspath(file))
        return path
    # Didn't find it, so search include_dirs
    for dir in include_dirs:
        path = os.path.normcase(os.path.join(dir, file))
        if os.path.isfile(path):
            return os.path.abspath(path)
    # Couldn't find it, so return empty string
    return ""
def IsCommandLine(line):
    '''This function determines if the line is a command line; if so, return
    true.  Otherwise, return false.  Note we always return 1 if we're in
    code mode.
    '''
    if line[0] == cmd_char or code_mode != 0:
        return 1
    else:
        return 0
def ExpandMacros(line):
    '''We look for any macro name matches.  Any that are found are
    replaced, then we start the search over again so we don't miss
    any macros within macros.
    '''
    done = 0
    while not done:
        found = 0  # Flags finding at least one macro
        for macro in macro_names:
            pos = string.find(line, macro)
            if pos != -1:
                # Found a macro name in the line
                found = 1
                old_value = macro
                new_value = macros[macro][0]
                line = string.replace(line, old_value, new_value)
                break
        if found == 0:
            done = 1
    # If current_code is not the null string, we've had at least one
    # code section, so evaluate using the global variables.  We'll only
    # do this if the line has at least one formatting string of the
    # form %(varname)X, where varname is the name of a global variable
    # and X is s, d, etc.
    if len(current_code) > 0:
        mo = need_global_expansion.search(line)
        if mo:
            line = line % globals()
    return line
def ProcessLine(line):
    '''Determine if the line is a command line or not.  If it is, process
    it with ProcessCommandLine().  Otherwise, expand the macros in the
    line and print it to stdout.
    '''
    if IsCommandLine(line):
        ProcessCommandLine(line)
    else:
        if output_on and not dump_macros:
            Output(line)
def Output(line):
    '''Send the line to the output stream.  First, expand all the macros
    in the line.  Then check the character before the trailing newline:
    if it is a '\' character, remove the newline unless the character
    before that is another '\', in which case substitute '\' for the
    '\\' and keep the newline.
    '''
    line = ExpandMacros(line)
    if len(line) < 2:
        print(line)
        return
    if line[-2] == '\\':
        # Second to last character is a backslash
        if len(line) > 2:
            # If the character before the last backslash is a backslash,
            # just output the line as is.
            if line[-3] == "\\":
                print(line)
            else:
                # It's an escaped backslash, so chop off the newline
                print(line[:-2])
        else:
            # It's just a backslash and a newline.
            return
    else:
        print(line)
def ProcessFile(file, ignore_failure_to_open=0, restore_line=0,
                restore_file=""):
    '''Read in and process each line in the file.  The
    ignore_failure_to_open variable is used to handle the sinclude case
    when a file is missing or can't be opened.

    If present, restore_line and restore_file are used to reset the
    current_line and current_file global variables, since we're in a
    recursive call from include or sinclude commands.
    '''
    global current_file
    global current_line
    try:
        ifp = open(file)
    except Exception:
        if ignore_failure_to_open:
            return
        else:
            Error("Couldn't open file '%s' for reading\n" % file)
    st = "\n\n===== %s processing file '%s' =====\n\n"
    Log(st % ("Started", file))
    line = ifp.readline()
    current_file = file
    current_line = 1
    while line:
        ProcessLine(line)
        line = ifp.readline()
        current_line = current_line + 1
    ifp.close()
    if restore_line:
        current_line = restore_line
    if restore_file:
        current_file = restore_file
    Log(st % ("Finished", file))
if __name__ == "__main__":
    Initialize()
    for file in files_to_process:
        ProcessFile(file)
    exit(0)
