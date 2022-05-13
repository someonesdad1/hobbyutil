'''

TODO
    - Convert multiline strings to use """...""" form.  These can then have
      the common leading whitespace removed by dedent() and are trivially
      converted to the requisite markup. 

--------------------------------------------------------------------------------
Python script to convert the projects file to projects.py.  This is on the
branch 'eliminate_yaml' and will mean that the hobbyutil projects'
information is kept up to date in a python dictionary, so reading the data
in will be fast and the reading code can check types and data.

Each project has the following attributes (* means optional):
    - subdir:str    Location in hu directory tree
    - descr:str     Description
    - files:list    List of files making package
    - srcdir:str    Where source files are
    - ignore:str *  If not empty, gives reason to ignore
    - frozen:str *  Yes/no
    - todo:str   *  Things to do

A * after a name in files: means that file is not needed for the project
image in the hobbyutil directory.  A *'d file is only needed to construct
the project's files.  Still, what's needed is that the script should verify
that each of the needed project files exist so that the project could be
built if needed.

The [a, b] form of the files: entry is that a is the actual location of the
file relative to srcdir and b is the location of it in the zipfile.

If a files: entry has only one unstarred file, then it's the contents of
this project under the project directory.  Otherwise, the non-starred files
go into a zipfile.

- Does it make sense to change this to files: and srcfiles:

'''
if 1:   # Header
    # Standard imports
        from collections import deque
        import re
        import time
        import enum
        from pathlib import Path as P
        from pdb import set_trace as xx 
    # Custom imports
        from iso import ISO
        from get import GetLines
        from lwtest import Assert 
        from wrap import dedent 
def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)
def GetState(line):
    if line.startswith("subdir:"):
        return State.subdir
    elif line.startswith("descr:"):
        return State.descr
    elif line.startswith("files:"):
        return State.files
    elif line.startswith("srcdir:"):
        return State.srcdir
    elif line.startswith("ignore:"):
        return State.ignore
    elif line.startswith("frozen:"):
        return State.frozen
    elif line.startswith("todo:"):
        return State.todo
    else:
        return state
def PrintItem(name, item):
    '''Print the dict item with key name and sequence item's strings.
    '''
    s = " "*8
    u = s + " "*4
    print(f"{s}{name!r}: ", end="")
    if len(item) == 1:
        print(f"{item[0]!r},")
    else:
        print()
        while item:
            i = item.pop(0)
            # Note we add a space character to the end of each string.
            # This ensures they won't be run together words in the output.
            # Since the ultimate output will be html, the extra whitespace
            # isn't significant.
            print(f"{u}{i + ' '!r}", end="")
            print(",") if not item else print()
def PrintFiles(name, item):
    '''Print the dict item with key name and a tuple of item's elements.
    Each line can be either a string representing a file name or a list of
    two strings, representing two file names.
    '''
    s, u = " "*8, " "*16
    print(f"{s}{name!r}: ", end="")
    nop = lambda x: None
    if len(item) == 1:
        print(f"[{item[0]!r}],")
    else:
        print("[")
        while item:
            i = item.pop(0)
            if i.startswith("- ["):
                i = i[3:-1]
                file1, file2 = [j.strip() for j in i.split(",")]
                print(f"{u}[{file1!r}, {file2!r}],")
            else:
                Assert(i.startswith("- "))
                i = i[2:]
                print(f"{u}{i!r},")
            print(f"{u}],") if not item else nop(0)
def PrintBeginningOfFile():
    i = ISO()
    print(dedent(f'''
    # This file was constructed by the mkprojects.py python script on
    # {i.dt}.

    from wrap import dedent

    projects = {{
    '''))
def PrintEndOfFile():
    pass
def MakeDict():
    'Build the output dict for the current project'
    global state
    if 1:
        # The first line must be a project name followed by a colon
        rpn = re.compile(r"^([a-z0-9_]*): *$")
        line = lines.popleft()
        mo = rpn.match(line)
        Assert(mo)
        name = mo.groups()[0]
    Assert(state == State.header)
    # Output the dict key
    print(f"    {name!r}: {{")
    # Containers for strings
    descr = []
    ignore = []
    todo = []
    files = []
    # This is basically a state machine to process the project's lines
    while True:
        line = lines.popleft()
        if not lines:   # Last line read
            state = State.done
            print(f"{' '*8}}},")
            print("}")
            return
        mo = rpn.match(line)
        if mo:
            # This is part of next project, so put it back in the deque
            lines.appendleft(line)
            state = State.header
            print(f"{' '*8}}},")
            return
        line = line.strip()
        prev_state = state
        state = GetState(line)
        if state != prev_state:
            # Need to output accumulated data
            if descr:
                PrintItem("descr", descr)
                descr = []
            elif ignore:
                PrintItem("ignore", ignore)
                ignore = []
            elif todo:
                PrintItem("todo", todo)
                todo = []
            elif files:
                PrintFiles("files", files)
                files = []
        if state == State.header:
            Error(f"Cannot be header state after line {line!r}")        
        elif state == State.subdir:
            _, dir = line.split()
            print(f"{' '*8}'subdir': {dir!r},")
        elif state == State.descr:
            if line.startswith("descr: "):
                descr = [line[7:]]
            else:
                descr += [line]
        elif state == State.files:
            if not line.startswith("files:"):
                files.append(line)
        elif state == State.srcdir:
            _, dir = line.split()
            print(f"{' '*8}'srcdir': {dir!r},")
        elif state == State.ignore:
            if line.startswith("ignore: "):
                ignore = [line[8:]]
            else:
                ignore += [line]
        elif state == State.frozen:
            _, val = line.split()
            s = "True" if val.strip() == "yes" else "False"
            print(f"{' '*8}'frozen': {s},")
        elif state == State.todo:
            if line.startswith("todo: "):
                todo = [line[5:]]
            else:
                todo += [line]
        elif state == State.done:
            Error(f"Cannot be done state here")        

if __name__ == "__main__":
    # Project states
    @enum.unique
    class State(enum.Enum):
        header = enum.auto()
        subdir = enum.auto()
        descr = enum.auto()
        files = enum.auto()
        srcdir = enum.auto()
        ignore = enum.auto()
        frozen = enum.auto()
        todo = enum.auto()
        done = enum.auto()
    state = State.header
    lines = deque(GetLines("projects", script=True, nonl=True))
    PrintBeginningOfFile()
    while lines:
        MakeDict()
    PrintEndOfFile()
