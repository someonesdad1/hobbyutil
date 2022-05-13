'''
 
- ToDo
    - Interface
        - Change to commands on command line
            - v     Validate projects.py data
            - l     List projects and state
            - b     Build (need args or '.')
            - d     Dry run (show what will be done)
            - s     If one PDF, launch
            - p     Show projects with one PDF
            - z     Show projects in zip files
    - Note the Calipers.pdf document has no bookmarks.  This is a real pain
      in large files.  It's probably a "feature" of PDF/1A.
    - Project.IsStale
        - This is naive because it uses date/times.
        - See if it can be done with hashes instead; if not, then use
          direct comparison.  At least make this an option, as it would
          ensure that the repository doesn't get changed unless something
          really is changed.
    - This newer architecture might make it unnecessary to switch to
      makefile construction
    - Once running again, update the web page
    - Color:  this could be used to advantage for
        - Listings
        - Verbose display of processing like ts.py

--------------------------------------------------------------------------------
This script is used to populate a repository with the files that I want to
archive.  The project data come from the python file projects.py, which
contains a dictionary keyed by the project name.  

Tasks of code:
    - Verify all source code files exist and are readable
    - Identify missing or out-of-date destination files
    - Reconstruct any destination files that are out-of-date

'''
if 1:   # Header
    # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright © 2014, 2022 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Populate the files of the github hobbyutil repository.
        #∞what∞#
        #∞test∞# #∞test∞#
    # Standard imports
        from collections import defaultdict, OrderedDict
        from pathlib import Path as P
        from pdb import set_trace as xx
        from textwrap import dedent
        from time import asctime, strftime
        import getopt
        import os
        import shutil
        import subprocess
        import sys
        import textwrap
        import traceback as TB
        import zipfile
    # Custom imports
        from color import Color, TRM as t
        from columnize import Columnize
        from wrap import wrap, dedent
        from projects import HU_Projects, Validate
    # Global variables
        ii = isinstance
        w = int(os.environ.get("COLUMNS", "80")) - 1
        nl = "\n"
        email_address = "someonesdad1@gmail.com"
        Join = os.path.join
        # Under cygwin, the root directory's actual location is needed
        on_windows = True
        cygwin = "c:/cygwin" if on_windows else ""
        # If we need to launch a file with its registered app, we use the following
        # command.
        if on_windows:
            start = Join(cygwin, "/usr/bin/cygstart")
        else:
            start = "exo-open"  # On Linux
        # If a package is to be made with the -z option, this directory is where
        # the packages will reside (it's separate from the repository).
        package_dir = cygwin + "/home/Don/hobbyutil_packages"
        # Escape sequences for colors
        t.fz = t("royl")    # Frozen
        t.st = t("purl")    # Stale
        t.ig = t("mag")     # Ignored
        t.td = t("yell")    # To do
        t.de = t("sky")     # Description
        # Text wrapper
        tw = textwrap.TextWrapper()
        tw.width = w
        tw.replace_whitespace = True
        tw.fix_sentence_endings = True
        tw.initial_indent = tw.subsequent_indent = " "*4
        # Names of the output directories
        output_directories = set()
        # Name of the project list markdown file
        pl = "project_list"
        project_list_markdown = "{}.md".format(pl)
        project_list_rst = "{}.rst".format(pl)
        project_list_css = "{}.css".format(pl)
        del pl
        # Map output directories to more meaningful names
        output_directories_map = OrderedDict((
            ("elec", "Electrical"),
            ("eng", "Engineering"),
            ("math", "Math"),
            ("misc", "Miscellaneous"),
            ("prog", "Programming"),
            ("science", "Science"),
            ("shop", "Shop"),
            ("util", "Utilities"),
        ))
        # This will be our project data dictionary after vetting.  keys
        # will be project name and values will be Project instances.
        data = {}
if 1:   # Classes
    class Project(object):
        '''Contain the project's information and provide the requisite
        packaging.  The object's attributes are:
 
        name        Short name of project
        subdir      Which subdirectory will contain the file(s)
        descr       Description of project
        files       [src, dest] pairs of the project's files
        srcdir      Where the source files reside
        ignore      If not None, the reason this file isn't built
        frozen      If true, it's a big file, so only build when -f option used
        stale       One or more source files is newer than the repository files
        todo        String describing something that needs to be done
 
        The class variable projects is a dictionary keyed by each subdir name
        (such as 'math', 'shop', etc.); each key's value is a list of the
        project files that can be linked to in the web page.
        '''
        projects = defaultdict(list)
        def __init__(self, name, project_data_dict):
            self.name = name
            self.data = project_data_dict
            if "ignore" not in self.data:
                self.data["ignore"] = ""
            if "frozen" not in self.data:
                self.data["frozen"] = False
            self.validate_data()
        def validate_data(self):
            for key in "subdir descr files srcdir ignore".split():
                if key not in self.data:
                    Error("{} data missing key {}".format(self.name, key))
            # Make data attributes
            self.subdir = self.data["subdir"]
            self.descr = self.data["descr"]
            self.files = self.data["files"]
            self.srcdir = self.data["srcdir"]
            self.ignore = self.data["ignore"]
            self.frozen = bool(self.data["frozen"])
            self.stale = self.IsStale()
            self.todo = self.data.get("todo", "")
        def IsStale(self):
            # To see if this is a stale project, the destination will either be
            # a single file or a zip file.  Get the destination's time and the
            # project will be labeled stale if any of the source files' time
            # are larger than the destination's.
            if self.ignore:
                return False
            srcdir = self.data["srcdir"]
            non_asterisked_files = self.GetDestinationFiles()
            if len(non_asterisked_files) == 1:
                # It's a single file
                if 0:
                    SRC, DEST = non_asterisked_files[0]
                    srctime = os.stat(Join(self.srcdir, SRC)).st_mtime
                    try:
                        desttime = os.stat(Join(self.subdir, DEST)).st_mtime
                    except FileNotFoundError:
                        return True
                    if srctime > desttime:
                        return True
                else:
                    # Use more modern pathlib stuff
                    SRC, DEST = non_asterisked_files[0]
                    src = P(self.srcdir)
                    src = src/SRC
                    srctime = src.stat().st_mtime
                    try:
                        dest = P(self.subdir)/DEST
                        desttime = dest.stat().st_mtime
                    except FileNotFoundError:
                        return True
                    if srctime > desttime:
                        return True
            else:
                # It's a zip file
                zip = Join(self.subdir, self.name) + ".zip"
                try:
                    ziptime = os.stat(zip).st_mtime
                except FileNotFoundError:
                    # Zip file has not been made
                    return True
                for SRC, dest in non_asterisked_files:
                    srctime = os.stat(Join(self.srcdir, SRC)).st_mtime
                    if srctime > ziptime:
                        return True
            return False
        def GetDestinationFiles(self):
            '''Return a list of the non-asterisked destination files.  Note we
            return both the source and destination files in list of tuples.
            '''
            files = []
            for src, dest in self.files:
                if dest.endswith("*"):
                    continue
                files.append((src, dest))
            return files
        def __str__(self):
            me = self
            fz = t.fz if self.frozen else ""
            st = t.st if self.stale else ""
            ig = t.ig if self.ignore else ""
            td = t.td if self.todo else ""
            s = dedent(f'''
                {me.name}
                    subdir = {me.subdir}
                    descr  = {t.de}{me.descr!r}{t.n}
                    srcdir = {me.srcdir}
                    {ig}ignore = {me.ignore}{t.n}
                    {fz}frozen = {me.frozen}{t.n}
                    {st}stale  = {me.stale}{t.n}
                    files (src, dest):\n
            '''.format(**locals()))
            for src, dest in self.files:
                s += "        {}, {}\n".format(src, dest)
            return s
        def PDFs(self):
            '''Return a list of the PDF files in this project; the entries will
            point to the source locations.
            '''
            files = []
            for src, dest in self.files:
                u = RemoveAsterisk(src)
                if u.lower().endswith(".pdf"):
                    s = Join(self.srcdir, u)
                    files.append(s)
            return files
if 1:   # Utility
    def Error(msg, status=1):
        c.fg(c.lred)
        print(msg)
        c.normal()
        exit(status)
    def Info(back=3):
        '''Return file name and line number of where caller called us.
        You may have to change the stack index back to get the required
        stack frame.
        '''
        stack = TB.extract_stack()[-back:][0]
        return stack[:2]
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] command [args]
          Utility to build the hobbyutil repository's contents.
        Commands:
          build       Copy the relevant files to their directories and construct the zip
                      files.  Also make the markdown file containing the descriptions.
                      You can specify which projects in args or use '.' to build everything.
          list        List active and inactive projects.  You can specify particular projects
                      on the command line and the projects' details will be printed.  The
                      argument 'PDF' will create a listing of all the source PDFs in all the
                      projects, even the inactive ones.
          show        If the package has one PDF, launch this file.
        Options:
          -i      Ignore the ignore flag in the projects file.  This can be used to find
                  missing project files.
          -f      Build frozen files.  These are the large packages in the repository that
                  shouldn't change very often.  Only those packages given on the command 
                  line will be built.
          -t      Show python test scripts (*_test.py) that are in the projects (used to
                  identify tests that must be run).
          -z      Package the indicated project(s) in args into separate zip containers.
                  These will be located in the directory indicated by the global variable
                  package_dir.
        '''))
        exit(status)
    def ParseCommandLine():
        d["-i"]     = False     # If True, zip even if ignored
        d["-f"]     = False     # If True, build frozen files
        d["-t"]     = False     # If True, print out python test scripts
        d["-z"]     = False     # If True, zip indicated packages
        try:
            optlist, args = getopt.getopt(sys.argv[1:], "fitz")
        except getopt.GetoptError as e:
            msg, option = e
            print(msg)
            exit(1)
        for opt in optlist:
            if opt[0][1] in "fitz":
                d[opt[0]] = not d[opt[0]]
        if not args and not d["-t"]:
            Usage()
        return args
if 1:   # Core functionality
    def ValidateProjectData():
        '''The global variable data contains a dictionary keyed by project
        name.  This function reads that data in and validates it.
        '''
        Validate(warn=True)
        global data, output_directories
        # Check each project's entries
        for project in HU_Projects:
            di = HU_Projects[project]
            # Change one file items to two (allowing the one file form
            # is easier to read, takes less space, and indicates the
            # file won't be renamed).
            files = di["files"]
            for i, f in enumerate(files):
                if isinstance(f, str):
                    files[i] = [f, f]
                elif isinstance(f, list):
                    assert len(f) == 2
                else:
                    Error("'{}' unexpected in project '{}'" % (f, proj))
            di["files"] = files
            output_directories.add(di["subdir"])
            data[project] = Project(project, di)
    def RemoveAsterisk(s):
        '''Remove a trailing * from a string.
        '''
        if s.endswith("*"):
            return s[:-1]
        return s
    def MakeDirectories():
        '''If any directory in output_directories is not present, construct it.
        '''
        for dir in output_directories:
            if not os.path.isdir(dir):
                os.mkdir(dir)
    def GetFileList(project_object):
        ''' Make a list of the files without an ending asterisk in name.
        '''
        file_list = []
        for src, dest in project_object.files:
            if not src.endswith("*"):
                file_list.append((src, dest))
        assert(file_list)
        return file_list
    def BuildProject(project_object):
        file_list = GetFileList(project_object)
        if len(file_list) == 1:
            # Copy the single file.  Assumes we are in the root of the
            # repository.
            src = Join(cygwin + project_object.srcdir, file_list[0][0])
            dest = Join(project_object.subdir, file_list[0][1])
            shutil.copyfile(src, dest)
        else:
            # Construct a zipfile of these files
            zname = project_object.name + ".zip"
            dest = Join(project_object.subdir, zname)
            zf = zipfile.ZipFile(dest, "w")
            for SRC, DEST in file_list:
                src = Join(cygwin + project_object.srcdir, SRC)
                zf.write(src, DEST)
            zf.close()
        # Update the Project.projects class variable
        entry = (dest, project_object.descr)
        Project.projects[project_object.subdir].append(entry)
    def ShowTestScripts():
        '''Print out project names that contain a python script named
        *_test.py.
        '''
        print("Projects with *_test.py test scripts:")
        for project in data:
            po = data[project]
            for src, dest in po.files:
                if dest.endswith(".py"):
                    base = dest[:-3]
                    if base.endswith("_test"):
                        print("  {:20s}  {:30s}  {}".format(project, src, po.srcdir))
                        continue
        exit(0)
    def BuildProjectZip(project_object):
        # Make a list of all the files without an ending asterisk in name
        files = []
        for src, dest in project_object.files:
            files.append((RemoveAsterisk(src), RemoveAsterisk(dest)))
        assert(files)
        # Construct a zipfile of these files
        zname = project_object.name + ".zip"
        dest = Join(package_dir, zname)
        zf = zipfile.ZipFile(dest, "w")
        for SRC, DEST in files:
            src = Join(cygwin + project_object.srcdir, SRC)
            zf.write(src, DEST)
        zf.close()
    def Build(projects):
        print("Building projects:")
        if projects[0] == ".":
            projects = data.keys()
        for project in projects:
            project_object = data[project]
            if project_object.ignore and not d["-i"]:
                continue
            if project_object.frozen and not d["-f"]:
                print("{}   [not built because it is big (use -f)]".format(project))
                continue
            print(project)
            BuildProject(project_object)
        print()
        BuildProjectPage(d)
    def GetLinkName(project_object):
        '''Return the name of the file to link to for this project.  It will be
        a zip file if the project contains more than one file.
        '''
        files = GetFileList(project_object)
        if len(files) == 1:
            file = files[0][1]
        else:
            file = project_object.name + ".zip"
        return "{}/{}".format(project_object.subdir, file)
    def Time():
        '''Return a string showing the current time.
        '''
        def RemoveLeading0(s):
            return s[1:] if s[0] == "0" else s
        day, hour = strftime("%d %I").split()
        ampm = strftime("%p").lower()
        s = strftime("{} %b %Y {}:%M:%S {}")
        return s.format(RemoveLeading0(day), RemoveLeading0(hour), ampm)
    def BuildProjectPage():
        '''This builds the project_list.md file.  Note it has to include all
        the projects that are not ignored.  To do this, we build an OrderedDict
        that has the category names as keys (e.g., Electrical, etc.) and a list
        as value.  Each non-ignored project is then appended to the list as the
        data container is iterated over.
        '''
        # Build a container of Project objects indexed by the category and in
        # alphabetical order under each category.
        project_container = OrderedDict((
            ("elec", []),
            ("eng", []),
            ("math", []),
            ("misc", []),
            ("prog", []),
            ("science", []),
            ("shop", []),
            ("util", []),
        ))
        for project_name in data:
            po = project_object = data[project_name]
            if po.ignore:
                continue
            # The list entry will be a (link_abbrev, description) tuple.
            abbr = GetLinkName(po)
            link = "[{}]({})".format(abbr, abbr)
            description = po.descr
            entry = (link, description)
            project_container[po.subdir].append(entry)
        if 0:
            from pprint import pprint as pp
            pp(project_container)
            exit()
        if 1:
            # Write the project_list.md markdown file (this produces the Github
            # Pages webpage's table).
            pl = open(project_list_markdown, "w")
            pl.write("[Home](./README.md)" + nl + nl)
            for category in project_container:
                # Write heading for category
                pl.write(nl + "## " + output_directories_map[category] + nl + nl)
                # Start a table
                pl.write('''Link | Description
    --- | ---
    ''')
                for link, descr in project_container[category]:
                    pl.write("{} | {}\n".format(link, descr))
            pl.write(nl + "Updated {}".format(Time()) + nl*2)
            if 0:
                # Add a table with project counts
                total_number_of_projects = 0
                pl.write('''Number | Project
        --- | ---
        ''')
                for category in project_container:
                    n = len(project_container[category])
                    name = output_directories_map[category]
                    total_number_of_projects += n
                    pl.write("{} | {}\n".format(n, name))
                pl.write("{} | {}\n".format(total_number_of_projects, "Total"))
                pl.close()
        if 1:
            # Write the project_list.rst file; this is a reStructuredText file
            # that will result in an HTML file with more dense information on
            # the web page).
            hu = open(project_list_rst, "w")
            # Link to home page
            hu.write("`Home <https://someonesdad1.github.io/hobbyutil/>`_" + nl*2)
            # Table of contents
            hu.write(".. contents:: Table of Contents" + nl*2)
            hu.write(dedent(
            '''Integer after link is file size in units of 1000 bytes.
 
            Unless otherwise noted, the python scripts are written to run with
            python 3.6 or later.  If the script contains a line like ``from
            __future__ ...``, then it is possible that it will also run under python
            2.7.
 
            '''))
            for category in project_container:
                # Write heading for category
                heading = output_directories_map[category]
                hu.write(heading + nl)
                hu.write("="*len(heading) + nl + nl)
                # The list of hyperlinks to projects and their descriptions
                for link, descr in project_container[category]:
                    lnk = link[1:link.find("]")]
                    sz = os.stat(lnk).st_size//1000
                    if 1:
                        hu.write("| `{} <{}>`_ ({})\n".format(lnk, lnk, sz))
                    else:
                        print(lnk, sz) #xx
                        hu.write("| `{} <{}>`_\n".format(lnk, lnk))
                    hu.write("|   {}\n".format(descr))
                hu.write(nl*2)
            hu.write(nl + "Updated {}".format(Time()) + nl*2)
            hu.close()
    def BuildZips(projects):
        '''Construct zipfiles of the indicated projects.
        '''
        print("Building project zipfiles:")
        if projects[0] == ".":
            projects = data.keys()
        for project in projects:
            project_object = data[project]
            if project_object.ignore and not d["-i"]:
                print("{}'{}' is ignored".format(" "*20, project))
                continue
            print(project)
            BuildProjectZip(project_object)
    def Show(projects):
        '''If the indicated projects have one PDF, launch this file.
        '''
        for project in projects:
            pdfs = data[project].PDFs()
            if len(pdfs) == 1:
                os.system(start + " " + Join(cygwin, pdfs[0]))
            else:
                print("More than one PDF")
    def List(projects):
        '''projects will be a list of project names; list the project details.
        If projects is empty, show active and inactive projects.
        '''
        if projects:
            if projects[0] == "PDF":
                # List PDFs in all projects
                for project in data:
                    po = data[project]
                    pdfs = po.PDFs()
                    if pdfs:
                        print(project)
                        for i in po.PDFs():
                            print("    {}".format(i))
            elif projects[0].lower() == "all":
                # List all projects
                for project in data:
                    po = data[project]
                    print(po)
            else:
                # List details on given projects
                for project in projects:
                    po = data[project]
                    print(po)
        else:
            y = t("yell")
            # List ignored
            count, out = 0, []
            for project in data:
                p = data[project]
                if p.ignore:
                    count += 1
                    out.append(project)
            if count:
                out = [f"{t.ig}{i}{t.n}" for i in sorted(out)]
                t.print(f"{y}{count} ignored projects:")
                for i in Columnize(out, esc=True, indent=" "*4):
                    print(i)
            # List frozen
            count, out = 0, []
            for project in data:
                p = data[project]
                if p.frozen:
                    count += 1
                    out.append(project)
            if count:
                out = [f"{t.fz}{i}{t.n}" for i in sorted(out)]
                t.print(f"{y}{count} frozen projects:")
                for i in Columnize(out, esc=True, indent=" "*4):
                    print(i)
            # List active
            active, inactive, f = [], [], "*"
            for project in data:
                p = data[project]
                if not (p.ignore or p.frozen):
                    if p.stale:
                        active.append(t.st + project + t.n)
                    else:    
                        active.append(project)
            t.print(f"{y}{len(active)} active projects:")
            for i in Columnize(active, esc=True, indent=" "*4):
                print(i)
            print(f"\nColor key:  {t.fz}frozen{t.n} ", end="")
            print(f"{t.st}stale{t.n}")
if __name__ == "__main__":
    d = {} # Options dictionary
    projects = ParseCommandLine()
    ValidateProjectData()
    if d["-t"]:
        ShowTestScripts()
    MakeDirectories()
    cmd = projects[0]
    del projects[0]
    if cmd in "b bu bui buil build".split():
        if not projects:
            Usage()
        else:
            BuildZips(projects) if d["-z"] else Build(projects)
    elif cmd in "l li lis list".split():
        List(projects)
    elif cmd == "s sh sho show".split():
        Show(projects)
    else:
        Error("'%s' is an unrecognized command" % cmd)
