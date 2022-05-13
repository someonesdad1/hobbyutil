'''
File finding utility
    Similar to UNIX find, but less powerful.  It's not especially fast, but
    the usage is more convenient than find and the output is colorized to
    see the matches unless it's not going to a TTY.
 
    - TODO
        - Utilize the regex colorizing functions of color.py.
        - It should be able to find files that begin with 'r' by using the
          regex '^r.*'.  Note that currently you have to use '/r' and it
          doesn't color the r of the files in the current directory.
 
'''
if 1:   # Header
    # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2008, 2012 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # File finding utility
        #∞what∞#
        #∞test∞# #∞test∞#
    # Imports
        import sys
        import re
        import getopt
        import os
        import fnmatch
        import subprocess
        from collections import OrderedDict as odict
        from pdb import set_trace as xx
        from pathlib import Path as P
    # Custom imports
        from wrap import dedent
        from color import Color, TRM as t
if 1:   # Global variables
    nl = "\n"
    # If you're using cygwin, set the following variable to point to the
    # cygpath utility.  Otherwise, set it to None or the empty string.
    # This tool allows UNIX-style path conversions so that command line
    # directory arguments like /home/myname work correctly.
    cygwin = "c:/cygwin/bin/cygpath.exe"
    #
    # The following variable, if True, causes a leading './' to be removed
    # from found files and directories.  This shortens things up a bit.
    # However, when the -s option is used, leaving rm_dir_tag False causes
    # the current directory's entries to be printed last and sorted in
    # alphabetical order.  This is how I prefer to see things, as
    # sometimes the matches can be quite long and scroll off the top of
    # the page.  Usually, I'm only interested in stuff in the current
    # directory.
    rm_dir_tag = False
    #
    # Colorizing 
    t.dir = t("redl")
    t.match = t("yell")
    t.end = t.n
if 1:   # Glob patterns and file extensions
    # Glob patterns for source code files
    def GetSet(data, extra=None):
        s = ["*." + i for i in data.replace("\n", " ").split()]
        t = list(sorted(list(set(s))))
        if extra is not None:
            t.extend(extra)
        return t
    # An extensive list of file extensions
    # From https://www.file-extensions.org/filetype/extension/name/source-code-and-script-files
    data_long = '''
        11 19 4ge 4gl 4pk 4th 89x 8xk a a2w a2x a3c a3x a51 a5r a66 a86
        a8s aah aar abap abl abs acgi acm action actionscript actproj
        actx acu ad2 ada aem aep afb agc agi ago ags ahk ahtml aia aidl
        aiml airi ajm akp aks akt alan alg alx aml amos amw an ane
        anjuta apb apg aplt app appcache applescript applet appxmanifest
        appxsym appxupload aps apt arb armx arnoldc aro arq arscript art
        arxml ary as as3 asax asbx asc ascx asf ash asi asic asm asmx
        asp asproj aspx ass asta astx asz atmn atomsvc atp ats au3
        autoplay autosave avc ave avsi awd awk axb axd axe axs b b24 b2d
        ba_ bal bas bash bat bax bb bbc bbf bcc bcf bcp bdh bdsproj bdt
        beam bet beta bgm bhs bi bin_ bml bmo bms borland bp bpo bpr bps
        bpt brml brs brx bs2 bsc bsh bsm bsml bsv bte btproj btq
        bufferedimage build builder buildpath bur bxb bxl bxml bxp bzs c
        c# c++ c-- c3p c86 c__ cal cap capfile cas cb cba cbl cbp cbs cc
        ccbjs ccp ccproj ccs ccxml cd cel cfi cfm cfml cfo cfs cg cgi
        cgvp cgx chd chef chh ck ckm cl cla class classdiagram classpath
        clips clj cljs clm clojure clp cls clw cmake cml cms cnt cob
        cobol cod coffee cola com_ command common con configure
        confluence cord cos coverage coveragexml cp cpb cphd cplist cpp
        cpr cprr cpz cr cr2 creole cs csb csc csdproj csh cshrc csi
        csm csml cson csp cspkg csproj csx ctl ctp cu cuh cuo cx cxe cxl
        cxs cxx cya d d2j d4 daemonscript datasource dba dbg dbmdl dbml
        dbo dbp dbpro dbproj dcf dcr dd ddp deb defi dep depend derp dev
        devpak dfb dfd dfm dg dgml dgsl dht dhtml dia dic diff din dist
        dlg dmb dmc dml dms do dob docstates dor dot dpd dpk dpr dproj
        dqy drc dro ds dsa dsb dsd dse dso dsp dsq dsr dsym dt dtd dtml
        dto dts dtx dvb dwarf dwp dwt dxl e eaf ebc ebm ebs ebs2 ebuild
        ebx ecore ecorediag edml eek egg-info ejs ekm el elc eld ema
        enml entitlements epl eqn es ev3p ew ex exe_ exp exsd exu exv
        exw eze ezg f f03 f40 f77 f90 f95 faces factorypath fas fasl fbp
        fbp6 fbz6 fcg fcgi fcmacro fdo fdt ff fgb fil fmb fmt fmx for
        form fountain fpc fpi frj frs frt fs fsb fscr fsf fsi fsproj fsx
        ftn fuc fus fwactionb fwx fxcproj fxh fxl fxml fzs g1m galaxy
        gbl gc3 gch gcl gcode gdg geany gek gemfile generictest genmodel
        geojson gfa gfe ghc ghp git gla glade gld gls gml gnt go gobj
        goc gp gradle graphml graphmlz greenfoot groovy grxml gs gsb gsc
        gsk gss gst gus gv gvy gxl gyp gypi h h2o h6h h__ haml has hay
        hbm hbs hbx hbz hc hcw hdf hei hh hhh hic history hkp hla hlsl
        hms hoic hom hpf hpp hrh hrl hs hsc hse hsm ht4 htc htd htm
        html5 htr hx hxa hxml hxp hxproj hxx hydra i iap ice idb ide idl
        idle ig ii ijs ik il ilk image iml imp inc ino inp ins install
        io ipb ipch ipf ipp ipr ips irb irbrc irc irobo is isa iss
        isu itcl itmx iwb ix3 ixx j j3d jacl jad jade jak jardesc jav
        java javajet jbi jbp jcl jcm jcs jcw jdp jetinc jex jgc jgs ji
        jks jl jlc jmk jml jpage jpd jpx js jsa jsb jsc jscript
        jsdtscope jse jsf jsfl jsh json jsonp jsp jss jsx jsxinc jtb ju
        judo jug kbs kcl kd ked kex kit kix kl3 kml kmt kodu komodo kon
        kpl ksc ksh kst kt kts kumac kv kx l lamp lap lasso lba lbi lbj
        lds ldz less lex lhs lib licenses licx liquid lisp litcoffee lml
        lmp lmv lng lnk lnp lnx lo loc login lol lols lp lpr lpx lrf lrs
        ls1 ls3proj lsh lsp lss lst lsxtproj lua luac lub luca lxk m m2r
        m3 m4 m4x m51 m6m mab mac magik mak make makefile maki mako maml
        map mash master mat matlab mb mbam mbas mbs mbtemmplate mc mcml
        mcp mcr mdex mdf mdp mec mediawiki mel mex mf mfa mfcribbon-ms
        mfl mfps mg mhl mhm mi mingw mingw32 mk mkb mke ml mli mln mls
        mlsxml mlv mlx mly mm mmb mmbas mmch mmh mmjs mnd mo moc mod
        module mom mpm mpx mq4 mq5 mqt mrc mrd mrl mrm mrs ms msc mscr
        msdl msh1 msh1xml msh2 msh2xml msha msil msl msm msp mss mst
        msvc mtp mvba mvpl mw mwp mx mxe myapp mzp napj nas nbin nbk ncb
        ncx neko nes netboot nhs nk nlc nls nmk nnb nokogiri npi npl nrs
        nse nsi nspj nt nunit nupkg nvi nxc o ob2 obj obr ocb ocr odc
        odh odl ogl ogr ogs ogx okm oks opl oplm oppo opv opx oqy orl
        osas osg ow owd owl owx ox p p4a p5 p6 pag par param pas pawn pb
        pba pbi pbl pbp pbq pbxproj pc pcd pch pd pdb pdl pdml pdo pem
        perl pf0 pf1 pf2 pf3 pf4 pf?  pfa pfx pgm pgml ph phl php php1
        php2 php3 php4 php5 php6 phpproj phps phpt phs phtml pickle pika
        pike pjt pjx pkb pkh pl pl1 pl5 pl6 pl7 plac playground plc pli
        plog pls plx pm pm5 pm6 pmod pmp pnproj po poc pod poix policy
        pom pp pp1 ppa ppam ppml ppo pql pr7 prg pri prl pro proto ps1
        ps2 ps2xml psc1 psc2 psd1 psf psl psm1 psml pspscript psu ptl
        ptx ptxml pwo pxd pxml qac qdl qlc
        qlm qpf qry qs qsc qvs qxm r rake rakefile rb rbf rbp rbs rbt
        rbw rbx rc rc2 rc3 rcc rdf rdoc re reb rej res resjson resources
        resx rex rexx rfs rfx rgs rh rhtml rkt rml rmn rnw rob robo ror
        rpg rpj rpo rpp rpprj rpres rprofile rproj rptproj 
        rqb rqc rqy rrc rrh rs rsl rsm rsp rss rtml rts rub rule run rvb
        rvt rws rxs s s2s s43 s4e s5d saas sal sami sas sasf sass sax sb
        sbh sbml sbr sbs sc sca scala scar scb sce sci scm sconstruct
        scp scpt scptd scr script scriptterminology scs scss sct scz
        sdef sdi sdl sdsb seam ser ses sfl sfm sfx sh shfb shfbproj shit
        simba simple sit sjc sjs skp sl slackbuild slim sln slogt sltng
        sm sma smali sml smm smw smx snapx snippet sno snp spr spt spx
        sqlproj sqo src srz ss ssc ssi ssml ssq stl stm sts styl sus svc
        svn-base svo swg swift swt sxs sxt sxv synw-proj syp t tab tag
        targets tatxtt tcl tcsh tcx tcz tdo tea tec texinfo text textile
        tgml thml thor thtml ti tik tikz tiprogram tk tkp tla tld tlh
        tli tmf tmh tmo toml tpl tplt tpm tpr tql tra trig triple-s trt
        tru ts0 tsc tsq tst ttcn ttinclude ttl tur twig txl txml txx tzs
        ucb udf uem uih uit uix ulp ump usi usp uvproj uvprojx v v3s v4e
        vala vap vb vba vbe vbg vbhtml vbi vbp vbproj vbs vbscript vbw
        vbx vc vc15 vc5 vc6 vc7 vce vcp vcproj vcxproj vd vddproj vdm
        vdp vdproj vgc vic vim vip viw vjp vls vlx vpc vpi vpl vps vrp
        vsixmanifest vsmacros vsprops vssscc vstemplate vtm vup vxml w
        wam was wax wbc wbf wbs wbt wch wcm wdi wdk wdl wdproj wdw wfs
        wiki win32manifest wis wli wml wmlc wmls wmlsc wmw wod wpj wpk
        wpm ws wsc wscript wsd wsdd wsdl wsf wsh wspd wxi wxl wxs wzs x
        xaml xamlx xap xba xbap xbd xbl xblr xbs xcl xcodeproj xcp xda
        xfm xhtm xib xig xin xjb xje xl xla xlm xlm_ xlv xme xml xml-log
        xmla xn xnf xojo_binary_project xoml xpb xpdl xpgt xproj xql xqr
        xr xrc xsc xsd xsl xslt xsql xtxt xui xul xv2 xys yajl yaml ywl
        yxx yyp z zbi zcode zero zfd zh_tw zpd zpk zpl zrx zs zsc zsh
        zts zws'''
    source_code_files_long = GetSet(data_long, extra=["[Mm]akefile"])
    data_short = '''
        a asm awk bas bash bat bsh c c++ cc cpp cxx f f77
        f90 f95 gcode h hh hxx ino jav java json ksh
        l lex lib m m4 mk pas perl php pl rb
        re sh tcl tex tk vim yacc yaml
    '''
    source_code_files = GetSet(data_short, extra=["[Mm]akefile"])
    # Glob patterns for documentation files
    documentation_files = GetSet("doc odg ods odt xls")
    # Glob patterns for picture files
    picture_files = GetSet('''
        bmp clp dib emf eps gif img jpeg jpg pbm pcx pgm png ppm ps psd psp
        pspimage raw tga tif tiff wmf xbm xpm''')
    # Names of version control directories
    version_control = "git hg RCS".split()
if 1:   # Utility
    def Usage(d, status=2):
        d["name"] = os.path.split(sys.argv[0])[1]
        d["-s"] = "Don't sort" if d["-s"] else "Sort"
        usage = r'''
        Usage:  {name} [options] regex [dir1 [dir2...]]
        Finds files using python regular expressions.  If no directories are
        given on the command line, searches at and below the current
        directory.  Color-coding is used if output is to a TTY.  Use -c
        to turn off color-coding.
        Options:
        -C str    Globbing pattern separation string (defaults to space)
        -c        Turn off color coding
        -D        Show documentation files
        -d        Show directories only
        -e glob   Show only files that match glob pattern (can be multiples)
        -f        Show files only
        -F        Show files only (exclude picture files)
        -h        Show hidden files/directories that begin with '.'
        -i        Case-sensitive search
        -L        Follow directory soft links (defaults to False)
        -l n      Limit recursion depth to n levels
        -P        Show picture files
        -p        Show python files
        -r        Not recursive; search indicated directories only
        -S        Show source code files excluding python
        --S       Same as -S, but use long list of source code file extensions
        -s        {-s} the output directories and files
        -x glob   Ignore files that match glob pattern (can be multiples)
        -V        Include revision control directories
        --git     Include git directories only
        --hg      Include Mercurial directories only
        --rcs     Include RCS directories only
        Note:  
        regex on the command line is a python regular expression.
        Globbing patterns in the -e and -x options are the standard file
        globbing patterns in python's glob module.  The -e and -x options
        can contain spaces if you define a different separation string
        with the -C option
        Examples:
        - Find all python scripts at and below the current directory:
                python {name} -p 
        - Find files at and below the current directory containing the string
            "rational" (case-insensitive search) excluding *.bak and *.o:
                python {name} -C "," -f -x "*.bak,*.o" rational
        - Find any directories named TMP (case-sensitive search) in or below
            the current directory, but exclude any with 'cygwin' in the name:
                python {name} -d -i -x "*cygwin*" TMP
        - Find all documentation and source code files starting with 't' in
            the directory foo
                python {name} -DS /t foo
            This will also find files in directories that begin with 't' also.
        - Delete backup files at and below .; the '-u' for invoking python
            causes unbuffered output, allowing xargs use:
                python -u {name} -f bak\$ | xargs rm
            Omit the 'rm' to have xargs echo what will be removed.
        '''[1:].rstrip()
        print(dedent(usage).format(**d))
        exit(status)
    def ParseCommandLine(d):
        d["-C"] = " "       # Separation string for glob patterns
        d["-D"] = False     # Print documentation files
        d["-L"] = False     # Follow directory soft links
        d["-P"] = False     # Print picture files
        d["-S"] = False     # Print source code files
        d["-c"] = True      # Turn off color coding
        d["-d"] = False     # Show directories only
        d["-F"] = False     # Show files only but no picture files
        d["-f"] = False     # Show files only
        d["-h"] = False     # Show hidden files/directories
        d["-i"] = False     # Case-sensitive search
        d["-e"] = []        # Only list files with these glob patterns
        d["-l"] = -1        # Limit to this number of levels (-1 is no limit)
        d["-p"] = False     # Show python files
        d["-r"] = False     # Don't recurse into directories
        d["-s"] = False     # Sort the output directories and files
        d["-x"] = []        # Ignore files with these glob patterns
        d["-V"] = []        # Revision control directories to include
        if len(sys.argv) < 2:
            Usage(d)
        try:
            optlist, args = getopt.getopt(
                    sys.argv[1:], 
                    "C:DLPScde:Ffhil:prsVx:",
                    longopts="S git hg rcs".split()
            )
        except getopt.GetoptError as str:
            msg, option = str
            print(msg)
            exit(1)
        for o, a in optlist:
            if o[1] in "DLPScdFfhiprs":
                d[o] = not d[o]
            if o == "-D":
                d["-e"] += documentation_files
            if o == "-P":
                d["-e"] += picture_files
            if o == "-S":
                d["-e"] += source_code_files
            if o == "-e":
                d[o] += a.split(d["-C"])
            if o == "-l":
                n = int(a)
                if n < 0:
                    raise ValueError("-l option must include number >= 0")
                d[o] = n
            if o == "-p":
                d["-e"] += ["*.py"]
            if o == "-V":
                d["-h"] = True
                d["-V"] = version_control
            if o == "-x":
                s, c = o, d["-C"]
                d["-x"] += a.split(d["-C"])
            # Long options
            if o == "--S":
                d["-S"] = True
                d["-e"] += source_code_files_long
            elif o == "--hg":
                d["-h"] = True
                d["-V"] += ["hg"]
            elif o == "--git":
                d["-h"] = True
                d["-V"] += ["git"]
            elif o == "--rcs":
                d["-h"] = True
                d["-V"] += ["RCS"]
        if len(args) < 1:
            Usage(d)
        if d["-i"]:
            d["regex"] = re.compile(args[0])
        else:
            d["regex"] = re.compile(args[0], re.I)
        args = args[1:]
        if len(args) == 0:
            args = ["."]
        # Store search information in order it was found
        d["search"] = odict()
        # Normalize -V option
        d["-V"] = list(sorted(list(set(d["-V"]))))
        if not d["-c"] or not sys.stdout.isatty():
            # No color is wanted, so turn off escape sequences
            t.dir = t.match = t.end = ""
            # Eventually, the following will work instead
            #t.on = False
        return args
if 1:   # Core functionality
    def Normalize(x):
        return x.replace("\\", "/")
    def TranslatePath(path, to_DOS=True):
        '''Translates an absolute cygwin (a UNIX-style path on Windows) to
        an absolute DOS path with forward slashes and returns it.  Use
        to_DOS set to True to translate from cygwin to DOS; set it to
        False to translate the other direction.
        '''
        direction = "-w" if to_DOS else "-u"
        if to_DOS and path[0] != "/":
            raise ValueError("path is not an absolute cygwin path")
        if "\\" in path:
            # Normalize path (cypath works with either form, but let's not
            # borrow trouble).
            path = path.replace("\\", "/")
        msg = ["Could not translate path '%s'" % path]
        s = subprocess.Popen(
            (cygwin, direction, path),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        errlines = s.stderr.readlines()
        if errlines:
            # Had an error, so raise an exception with the error details
            msg.append("  Error message sent to stderr:")
            for i in errlines:
                msg.append("  " + i)
            raise ValueError(nl.join(msg))
        lines = [i.strip() for i in s.stdout.readlines()]
        if len(lines) != 1:
            msg.append("  More than one line returned by cygpath command")
            raise ValueError(nl.join(msg))
        return lines[0].replace("\\", "/")
    def Ignored(s, d):
        '''s is a file name.  If s matches any of the glob patterns in
        d["-x"], return True.
        '''
        for pattern in d["-x"]:
            if d["-i"]:
                if fnmatchcase(s, pattern):
                    return True
            else:
                if fnmatch.fnmatch(s, pattern):
                    return True
        return False
    def Included(s, d):
        '''s is a file name.  If s matches any of the glob patterns in
        d["-e"], return True.
        '''
        for pattern in d["-e"]:
            if d["-i"]:
                if fnmatch.fnmatchcase(s, pattern):
                    return True
            else:
                if fnmatch.fnmatch(s, pattern):
                    return True
        return False
    def PrintMatch(s, d, start, end, isdir=False):
        'For the match in s, print things out in the appropriate colors'
        if isdir:
            print(f"{t.dir}{s[:start]}", end="")
        else:
            print(s[:start], end="")
        print(f"{t.match}{s[start:end]}", end="")
        if isdir:
            print(f"{t.dir}", end="")
        else:
            print(f"{t.end}", end="")
    def PrintMatches(s, d, isdir=False):
        '''Print the string s and show the matches in appropriate
        colors.  Note that s can end in '/' if it's a directory.
        '''
        if d["-f"] and not d["-d"]:
            # Files only -- don't print any matches in directory
            dir, file = os.path.split(s)
            print(dir, end="")
            if dir and dir[:-1] != "/":
                print("/", end="")
            s = file
        while s:
            if isdir and s[-1] == "/":
                mo = d["regex"].search(s[:-1])
            else:
                mo = d["regex"].search(s)
            if mo:
                PrintMatch(s, d, mo.start(), mo.end(), isdir=isdir)
                s = s[mo.end():]
            else:
                # If the last character is a '/', we'll print it in color
                # to make it easier to see directories.
                if s[-1] == "/":
                    print(s[:-1], end="")
                    print(f"{t.dir}/{t.end}", end="")
                else:
                    try:
                        print(s, end="")
                    except IOError:
                        # Caused by broken pipe error when used with less
                        exit(0)
                s = ""
        print()
    def Join(root, name, d, isdir=False):
        '''Join the given root directory and the file name and store
        appropriately in the d["search"] odict.  isdir will be True if
        this is a directory.  Note we use UNIX notation for the file
        system's files, regardless of what system we're on.
        '''
        # Note we check both the path and the filename with the glob
        # patterns to see if they should be included or excluded.
        is_ignored = Ignored(name, d) or Ignored(root, d)
        is_included = Included(name, d) or Included(root, d)
        if is_ignored:
            return
        if d["-e"] and not is_included:
            return
        root, name = Normalize(root), Normalize(name)
        if d["-V"]:         # Ignore version control directories
            # git
            if "git" not in d["-V"]:
                r = re.compile("/.git$|/.git/")
                mo = r.search(root)
                if mo or name == ".git":
                    return
            # Mercurial
            if "hg" not in d["-V"]:
                r = re.compile("/.hg$|/.hg/")
                mo = r.search(root)
                if mo or name == ".hg":
                    return
            # RCS
            if "RCS" not in d["-V"]:
                r = re.compile("/RCS$|/RCS/")
                mo = r.search(root)
                if mo or name == "RCS":
                    return
        # Check if we're too many levels deep.  We do this by counting '/'
        # characters.  If root starts with '.', then that's the number of
        # levels deep; otherwise, subtract 1.  Note if isdir is True, then
        # name is another directory name, so we add 1 for that.
        lvl = root.count("/") + isdir
        if root[0] == ".":
            lvl -= 1
        if d["-l"] != -1 and lvl >= d["-l"]:
            return
        if root == ".":
            root = ""
        elif rm_dir_tag and len(root) > 2 and root[:2] == "./":
            root = root[2:]
        s = Normalize(os.path.join(root, name))
        d["search"][s] = isdir
    def Find(dir, d):
        def RemoveHidden(names):
            '''Unless d["-h"] is set, remove any name that begins with '.'.
            '''
            if not d["-h"]:
                names = [i for i in names if i[0] != "."]
            return names
        pics = set([i[2:] for i in picture_files])
        def RemovePictures(names):
            '''If d["-F"] is True, remove picture file names
            '''
            if d["-F"]:
                keep = []
                for i in names:
                    p = P(i)
                    ext = p.suffix[1:]
                    if ext not in pics:
                        keep.append(i)
                return keep
            return names
        contains = d["regex"].search
        J = lambda root, name: Normalize(os.path.join(root, name))
        find_files = d["-f"] & ~ d["-d"]
        find_dirs = d["-d"] & ~ d["-f"]
        follow_links = d["-L"]
        for root, dirs, files in os.walk(dir, followlinks=follow_links):
            # If any component of root begins with '.' and it's not '..',
            # ignore unless d["-h"] is set.
            has_dot = any([i.startswith(".") and len(i) > 1 and i != ".."
                        for i in root.split("/")])
            if not d["-h"] and has_dot:
                continue
            files = RemoveHidden(files)
            files = RemovePictures(files)
            dirs = RemoveHidden(dirs)
            if find_files:
                [Join(root, name, d) for name in files if contains(name)]
            elif find_dirs:
                [Join(root, dir, d, isdir=True) for dir in dirs
                    if contains(J(root, dir))]
            else:
                [Join(root, name, d, isdir=True) for name in dirs
                    if contains(J(root, name))]
                [Join(root, name, d) for name in files if contains(J(root, name))]
            if d["-r"]:  # Not recursive
                # This works because the search is top-down
                break
    def PrintReport(d):
        'Note we put a "/" after directories to flag them as such'
        D = d["search"]
        if d["-s"]:
            # Print things in sorted form, directories first.
            dirs, files = [], []
            # Organize by directories and files.  Note you need to use keys()
            # to get the original insertion order
            for i in D.keys():
                if D[i]:
                    dirs.append(i)
                else:
                    files.append(i)
            print(f"{t.end}", end="")
            dirs.sort()
            files.sort()
            if not d["-d"] and not d["-f"]:
                # Both directories and files
                for i in dirs:
                    PrintMatches(i + "/", d, isdir=True)
                for i in files:
                    PrintMatches(i, d)
            else:
                if d["-d"]:  # Directories only
                    for i in dirs:
                        PrintMatches(i + "/", d, isdir=True)
                else:  # Files only
                    for i in files:
                        PrintMatches(i, d)
        else:
            # Print things as encountered by os.walk
            for i in D.keys():
                if (d["-f"] and D[i]) or (d["-d"] and not D[i]):
                    continue
                PrintMatches(i + "/" if D[i] else i, d, isdir=D[i])
        print(f"{t.end}", end="")
if __name__ == "__main__":
    d = {}  # Settings dictionary
    directories = ParseCommandLine(d)
    for dir in directories:
        # Following needed on cygwin
        #if dir and dir[0] == "/":
        #    dir = TranslatePath(dir)
        Find(dir, d)
    PrintReport(d)
