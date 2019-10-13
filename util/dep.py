'''

Prints out the python library dependencies of the python files given on the
command line.  Currently, this script works with python 3.6 and 2.7.  

IMPORTANT:  This script will NOT find *.pyc or *.pyo files that act as
modules.  It makes the assumption that all modules that are python code
have the file suffix *.py.

WARNING:  The imports are found by discovering the 'import' lines in the
file, so the output does not indicate the other files the import lines may
import.

Example output for a test script:
    a.py
        Addon modules:
            uncertainties.umath
        Modules that couldn't be imported:
            kdjfdfkj
        Standard library modules:
            __future__
            getopt
            os
            pdb
            pickle
            pprint
            re
            sys
        User modules:
            color
            debug
            lwtest
            sig

'''
  
# Copyright (C) 2018 Don Peterson
# Contact:  gmail.com@someonesdad1
 
#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#
 
from __future__ import print_function
from glob import glob
import getopt
import os
import re
import sys
import sysconfig
from collections import defaultdict

try:
    from importlib.util import find_spec
except ImportError:
    # Expected on python 2.7:  will use exec("import ...") in place of
    # find_spec.
    pass

# Only support tested versions (used 3.6.1 and 2.7.6 on cygwin)
v = sys.version_info
version = "{}.{}".format(v.major, v.minor)
py3 = "3.7 3.6 3.5".split()
if version not in py3 + ["2.7"]:
    print("{}:  Python {} is an unsupported version".format(sys.argv[0],
            version))
    exit(1)

def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)

def Usage(d):
    name = sys.argv[0]
    stdlib_dir = sysconfig.get_paths()["stdlib"]
    addon_dir = os.path.join(sysconfig.get_paths()["stdlib"],
                             "site-packages")
    s = '''
Usage:  {name} [options] [file1 ...]
  Determine the python module dependencies of the files given on the
  command line.  IMPORTANT:  it will not find *.pyc or *.pyo files your
  script may depend on, nor will it find the import files used by the files
  it imports (for the latter, run your script and print out sys.modules).

  WARNING:  because this script uses regular expressions for searching,
  lines that look like import lines inside of a multiline string may result
  in output even though there is no real dependency.  Similarly, an import
  inside a false conditional will show as a dependency even though it isn't.

  Standard library modules are in
      {stdlib_dir}
  Addon modules are in
      {addon_dir}

Options:
  -n        Show only the modules that can't be imported.  These are
            typically missing modules or ones that have errors.
'''[1:-1]
    print(s.format(**locals()))
    exit(1)

def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)

def ParseCommandLine(d):
    d["-n"] = False
    try:
        opts, files = getopt.getopt(sys.argv[1:], "hn")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o in ("-h", "--help"):
            Usage(d, status=0)
        elif o in ("-n",):
            d["-n"] = not d["-n"]
    if not files:
        Usage(d)
    return files

def CanBeImported(module):
    if version == "2.7":
        try:
            exec("import " + module)
            return True
        except ImportError:
            return False
    elif version in py3:
        # This method doesn't actually import the file
        try:
            s = find_spec(module)
        except ModuleNotFoundError:
            return False
        except ImportError:
            return False
        else:
            return False if s is None else True
    else:
        Error("{} is an unsupported version".format(version))

def GetModuleListing():
    '''Return a dictionary containing the names of the modules in the
    standard python distribution and the add-ons.  They keys are:
        stdlib
        addon
        compiled
    and the values are a set of the string names of the modules.
    '''
    listing, currdir = {}, os.getcwd()
    # compiled:  Note:  these are manually-built lists.  If you want to
    # support another python version, look at the DLLs in
    # /usr/lib/pythonX.X/lib-dynload.
    if version in py3:
        compiled = set('''
            array asyncio audioop binascii bisect bz2 cmath codecs crypt
            csv ctypes curses datetime dbm decimal fcntl grp hashlib heapq
            itertools json lzma math mmap multiprocessing parser pickle
            posix random readline resource select socket sqlite3 ssl struct
            syslog termios unicodedata zlib
            '''.strip().replace("\n", " ").split())
    elif version == "2.7":
        compiled = set('''
            array audioop binascii bisect bsddb bz2 cPickle cStringIO cmath
            codecs collections crypt csv ctypes curses datetime dbm dl
            fcntl functools gdbm grp hashlib heapq hotshot imageop io
            itertools json locale math mmap multiprocessing operator parser
            random readline resource select socket sqlite3 ssl struct
            syslog termios time unicodedata zlib
            '''.strip().replace("\n", " ").split())
    else:
        print("Python {} is not supported".format(version))
        exit(1)
    listing["compiled"] = compiled
    # stdlib
    dir, files = sysconfig.get_paths()["stdlib"], set()
    os.chdir(dir)
    for i in glob("*"):
        if i.endswith(".py"):
            i = i[:-3]
        files.add(i)
    for i in ("__phello__.foo __pycache__ site-packages pydoc_data "
              "lib-dynload test").split():
        if i in files:
            files.remove(i)
    files.add("sys")  # Must manually add
    listing["stdlib"] = files
    # addons
    if version in py3:
        dir, files = sysconfig.get_paths()["platlib"], set()
        os.chdir(dir)
        for i in glob("*"):
            if not os.path.isdir(i):
                continue
            files.add(i)
        listing["addon"] = files
    elif version == "2.7":
        # Have to break the directory names on the first hyphen, as some
        # distributions included the version number in the directory name.
        dir, files = sysconfig.get_paths()["platlib"], set()
        os.chdir(dir)
        for i in glob("*"):
            if not os.path.isdir(i):
                continue
            if "-" in i:
                i = i[:i.find("-")]
            files.add(i)
        listing["addon"] = files
    # Ready to return
    os.chdir(currdir)
    return listing

def Classify(modules):
    '''Return a dictionary that classifies the module names in the set
    modules.  Keys are
 
        stdlib      Python's standard library module
        compiled    Python's modules in C
        addon       Add-on modules in stdlib/site-packages
        user        User module
        not_found   Module that couldn't be imported
 
    The values will be the sets of modules in that classification.
    '''
    # First, we'll construct sets of those modules that can be found and
    # imported and those that can't.
    found, not_found = set(), set()
    for module in modules:
        if CanBeImported(module):
            found.add(module)
        else:
            not_found.add(module)
    # For the found modules, classify them as stdlib, addon, or user.
    user, addon, compiled = set(), set(), set()
    listing = GetModuleListing()
    for module in found:
        base = module
        # Need to handle imports like 'scipy.stats'; we'll need 'base' to
        # be just 'scipy' to find it in the addons.
        if "." in module:
            base = module.split(".")[0]
        if base in listing["stdlib"]:
            continue
        elif base in listing["addon"]:
            addon.add(module)
        elif base in listing["compiled"]:
            compiled.add(module)
        else:
            user.add(module)
    # Remove the user and addon modules from the found set
    found -= user
    found -= addon
    found -= compiled
    return {
        "addon": addon,
        "compiled": compiled,
        "stdlib": found,
        "user": user,
        "not_found": not_found,
    }

def ProcessFile(file, d):
    '''For the given file, find the lines that match the regular
    expressions '^\s*from\s+ .* import .*' or 'import .*$'.
    '''
    modules = []    # Find the modules imported by this file
    # Use regular expressions to find the import statements
    r1 = re.compile("^\s*import\s+(.*)$")
    r2 = re.compile(r"^\s*from\s+(\w+)\s+import\s+.*$")
    for i, line in enumerate(open(file).readlines()):
        s = line.strip()
        if not s or s[0] == "#":
            continue
        mo1 = r1.match(s)
        mo2 = r2.match(s)
        if mo1:
            for item in mo1.groups():
                modules.extend(mo1.groups())
        elif mo2:
            for item in mo2.groups():
                modules.extend(mo2.groups())
    modules = set([i.split()[0].replace(",", "") for i in modules])
    classified = Classify(modules)
    print(file)
    description = {
        "addon": "Addon modules:",
        "compiled": "Compiled standard library modules:",
        "stdlib": "Standard library modules:",
        "user": "User modules:",
        "not_found": "Modules that couldn't be imported:",
    }
    for key in sorted(classified):
        if classified[key]:
            if d["-n"] and key != "not_found":
                continue
            print("    {}".format(description[key]))
            for item in sorted(classified[key]):
                print("        {}".format(item))

if __name__ == "__main__":
    d = {}      # Options dictionary
    files = ParseCommandLine(d)
    for file in files:
        ProcessFile(file, d)
