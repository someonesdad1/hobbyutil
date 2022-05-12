'''
Temporary script to convert projects to projects.py

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
from get import GetLines
from collections import deque
from color import TRM as t
import re
import enum
from pdb import set_trace as xx 
from lwtest import run, raises, assert_equal, Assert

t.always = True
dbg = False

def Index(line, show=False):
    '''Match to the regexps to categorize the line's type and return the
    string matched.  If show is True, decorate the line to stdout.  Note
    we exit on a bad line. 

    Return (line_id, str_match) where line_id is a string identifying the
    field type and str_match is the string data that was matched.

    Returned line_id strings are
        projectname
        filelist
        subdir
        descr
        file
        srcdir
        ignore
        frozen
        todo
        empty
        strcont     (string continuation)
    '''
    matched = False
    for r, c in (
            (rprogjectname, t.pr), 
            (rfile, t.file),
            (rsub, t.sub),
            (rdescr, t.descr),
            (rfiles, t.files),
            (rsrc, t.src),
            (rign, t.ign),
            (rfrz, t.frz),
            (rtodo, t.todo),
            (rempty, None),
            (rstr, t.str),
        ):
        mo = r.match(line)
        if mo and mo.groups():
            s = mo.groups()[0]
            if s:
                t.print(f"{c}{s}")
                matched = True
                break
    if not matched:
        print(f"Bad line:  {line!r}")
        exit(1)
    return

    if rprogjectname.match(line):
        t.print(f"{t.pr}{line}")
    elif rfile.match(line):
        t.print(f"{t.file}{line}")
    elif rsub.match(line):
        t.print(f"{t.sub}{line}")
    elif rdescr.match(line):
        t.print(f"{t.descr}{line}")
    elif rfiles.match(line):
        t.print(f"{t.files}{line}")
    elif rsrc.match(line):
        t.print(f"{t.src}{line}")
    elif rign.match(line):
        t.print(f"{t.ign}{line}")
    elif rfrz.match(line):
        t.print(f"{t.frz}{line}")
    elif rtodo.match(line):
        t.print(f"{t.todo}{line}")
    elif rstr.match(line):
        t.print(f"{t.str}{line}")
    elif rempty.match(line):
        pass
    else:
        t.print(f"{t.bad}'Bad' line:  {line!r}")
        exit(1)
def GetRegexps():
    global rprogjectname, rfile, rsub, rdescr, rfiles, rsrc, rign
    global rfrz, rtodo, rempty, rstr
    # Regex for project name
    rprogjectname = re.compile(r"^([a-z0-9_]*): *$")
    t.pr = t("purl")
    # Regex for a file
    rfile = re.compile(r"^ {8}- (.*)$")
    t.file = t("grn")
    # Regex for 'subdir:'
    rsub = re.compile(r"^ {4}subdir: (.*)$")
    t.sub = t("ornl")
    # Regex for 'descr:'
    rdescr = re.compile(r"^ {4}descr: (.*)$")
    t.descr = t("magl")
    # Regex for 'files:'
    rfiles = re.compile(r"^ {4}files: (.*)$")
    t.files = t("yell")
    # Regex for 'srcdir:'
    rsrc = re.compile(r"^ {4}srcdir: (.*)$")
    t.src = t("trq")
    # Regex for 'ignore:'
    rign = re.compile(r"^ {4}ignore: (.*)$")
    t.ign = t("lip")
    # Regex for 'frozen:'
    rfrz = re.compile(r"^ {4}frozen: (.*)$")
    t.frz = t("cynl")
    # Regex for 'todo:'
    rtodo = re.compile(r"^ {4}todo: (.*)$")
    t.todo = t("yell", "redl")
    # Regex for empty lines
    rempty = re.compile(r"^\s*$")
    # Regex for string continuation lines
    rstr = re.compile(r" {8}(.*)$")
    t.str = t("brn")
    # For 'bad' lines
    t.bad = t("blk", "yell")

def PrintProject(project):
    '''project is a list of this project's lines'''

def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)
def GetState(line):
    if line.startswith("subdir"):
        return State.subdir
    elif line.startswith("descr"):
        return State.descr
    elif line.startswith("files"):
        return State.files
    elif line.startswith("srcdir"):
        return State.srcdir
    elif line.startswith("ignore"):
        return State.ignore
    elif line.startswith("frozen"):
        return State.frozen
    elif line.startswith("todo"):
        return State.todo
    else:
        return state
def GetProject():
    '''Build a dict
    '''
    global state
    rpn = re.compile(r"^([a-z0-9_]*): *$")
    line = lines.popleft()
    mo = rpn.match(line)
    assert(mo)
    name = mo.groups()[0]
    Assert(state == State.header)
    print(f"    {name!r}: {{")
    descr = []
    ignore = []
    todo = []
    files = []
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
                print('\n'.join(descr))
                descr = []
            elif ignore:
                print('\n'.join(ignore))
                ignore = []
            elif todo:
                print('\n'.join(todo))
                todo = []
            elif files:
                print('\n'.join(files))
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
            pass
        elif state == State.srcdir:
            pass
        elif state == State.ignore:
            pass
        elif state == State.frozen:
            pass
        elif state == State.todo:
            pass
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
    print("projects = {")
    while lines:
        project = GetProject()
        PrintProject(project)
