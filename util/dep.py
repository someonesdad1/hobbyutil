'''
Find python library dependencies
    Prints out the python library dependencies of the python files given on the
    command line.  This is done by scanning the files with regular
    expressions, so it can miss things.  But it will find lines like 

        import x
        from x import a, b, c
        import x, y, z

    IMPORTANT:  This script will NOT find *.pyc or *.pyo files that act as
    modules.  It makes the assumption that all modules that are python code
    have the file suffix *.py.

        If you really want a list of modules, look at modulefinder.py in the
        standard library, running it as a script.  However, I usually find
        it produces far more output than I want, especially on fairly
        complex scripts.  For my needs, the regular expression scanning
        works OK.

    Example output for a test script:
        a.py
            Addon modules:
                uncertainties.umath
            Modules that couldn't be imported:
                kdjfdfkj
            Standard library modules:
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
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2018 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Show python import dependencies
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Standard imports
    from glob import glob
    import getopt
    import os
    import re
    import sys
    import sysconfig
    from collections import defaultdict
    from pdb import set_trace as xx 
    from importlib.util import find_spec
if 1:   # Custom imports
    from wrap import dedent
if 1:   # Global variables
    version = None
if 1:   # Utility
    def Error(msg, status=1):
        print(msg, file=sys.stderr)
        exit(status)
    def CheckVersion():
        v = sys.version_info
        msg = "Python version must be >= 3.7"
        if v.major < 3 or (v.major == 3 and v.minor < 7):
            Error(msg)
        global version
        version = f"{v.major}.{v.minor}"
    def Usage(d):
        name = sys.argv[0]
        stdlib_dir = sysconfig.get_paths()["stdlib"]
        addon_dir = os.path.join(sysconfig.get_paths()["stdlib"],
                                "site-packages")
        print(dedent(f'''
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
        '''))
        exit(1)
    def ParseCommandLine(d):
        CheckVersion()
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
if 1:   # Core functionality
    def CanBeImported(module):
        # This method doesn't actually import the file
        try:
            s = find_spec(module)
        except ModuleNotFoundError:
            return False
        except ImportError:
            return False
        else:
            return False if s is None else True
    def GetModuleListing() -> dict:
        '''Return a dictionary containing the names of the modules in the
        standard python distribution and the add-ons.  They keys are:
            stdlib
            addon
            compiled
        and the values are a set of the string names of the modules.
        '''
        listing, currdir = {}, os.getcwd()
        # compiled:  Note:  these are manually-built lists.  If you want to
        # support another python version, look at the DLL names in
        # /usr/lib/pythonX.X/lib-dynload.  This list was updated for
        # python 3.7.7 on cygwin on 6 May 2021.
        listing["compiled"] = set('''
            asyncio bisect blake2 bz2 codecs_cn codecs_hk codecs_iso2022
            codecs_jp codecs_kr codecs_tw contextvars crypt csv ctypes
            curses curses_panel datetime dbm decimal elementtree gdbm
            hashlib heapq json lsprof lzma md5 multibytecodec
            multiprocessing opcode pickle posixsubprocess queue random
            sha1 sha256 sha3 sha512 socket sqlite3 ssl struct tkinter
            uuid array audioop binascii cmath fcntl grp math mmap parser
            pyexpat readline resource select syslog termios unicodedata
            zlib'''.split())
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
        dir, files = sysconfig.get_paths()["platlib"], set()
        os.chdir(dir)
        for i in glob("*"):
            if not os.path.isdir(i):
                continue
            files.add(i)
        listing["addon"] = files
        # Ready to return
        os.chdir(currdir)
        return listing
    def Classify(modules: set) -> dict:
        '''Return a dictionary that classifies the module names in the set
        modules.  Keys are
    
            addon       Add-on modules in stdlib/site-packages
            compiled    Python's modules in C
            stdlib      Python's standard library module
            user        User module
            not_found   Module that couldn't be imported
    
        The values will be the sets of modules in that classification.
        '''
        # Construct sets of those modules that can be found and imported and
        # those that can't.
        found, not_found = set(), set()
        for module in modules:
            if CanBeImported(module):
                found.add(module)
            else:
                not_found.add(module)
        # Classify the found modules
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
        # Remove the user, addon, and compiled modules from the found set
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
        for line in open(file):
            s = line.strip()
            if not s or s[0] == "#":
                continue
            mo1, mo2 = r1.match(s), r2.match(s)
            if mo1:
                for item in mo1.groups():
                    modules.extend(mo1.groups())
            elif mo2:
                for item in mo2.groups():
                    modules.extend(mo2.groups())
        # Handle lines like 'import a, b, c'
        modules = set([i.split()[0].replace(",", "") for i in modules])
        # Put into a dict with classifications like 'addon', 'stdlib',
        # 'user', etc.
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
                #print("    {}".format(description[key]))
                print(f"    {description[key]}")
                for item in sorted(classified[key]):
                    print(f"        {item}")
if __name__ == "__main__":
    d = {}      # Options dictionary
    files = ParseCommandLine(d)
    for file in files:
        ProcessFile(file, d)
