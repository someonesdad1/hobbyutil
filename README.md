# hobbyutil

Click [here](./project_list.html) to go to the projects page to read their
descriptions and download them.  

This repository is for projects I've developed over the years for my
various hobbies.  Each project is a link which you can click on to get the
file(s) associated with the project.  For documents, the PDF form is
typically the only file included.  A project that contains more than one
file will be a zip archive.  If you would like the source documents
(usually constructed from an Open Office document), email me at
someonesdad1@gmail.com and I'll send you a zip file containing the
information that the project's data are constructed from.

For projects that are python scripts, I have standardized on python 3.6 for
running the scripts.  Many of these scripts have also been tested on python
2.7, but I am no longer making the effort to keep things running with
python 2.7, as python 3 is mature and well-supported by the needed
libraries.  If you see a script contain the line

```from __future__ import division, print_function```

then it's probable that the script will run under python 2.7.  Where
self-tests are available, they will be python scripts that have the same
name as the script with '\_test' appended.

The ./projects file in the repository is used to keep track of the things
that are in this repository (its main function is to map the files on my
hard disk to the file(s) in the project).  Note there are more things in
this projects file than are packaged in the repository; the things that are
not included have an 'ignore' string set, along with the reason for
ignoring the project's contents.  Over time, I'll get more of these
projects on-line, but they require maintenance.  

This website contains updated information from a Google Code site; Google
Code went defunct in 2014.

## Archival

This is the third website that I have hosted this stuff on and I'm sure it
won't be the last.  My wish is that I could just leave it in one place and
be confident that it would remain available to interested folks for a few
decades, even after I'm dead.  But that's just not going to happen because
a few years is a long time on the web.  Who can foresee what will happen to
Github a few years down the road after Microsoft purchases it?  I don't
have a good solution to this problem.  About the most pragmatic thing that
could happen is that lots of people copy this repository to other places
and share it with other folks.  Feel free to mirror this site if you wish.

## License

Currently, most of the scripts are under the Open Software License version
3.0.  This is a copyleft license; I am contemplating putting everything
under the Apache 2.0 license, which is not a copyleft license.  Regardless,
my basic intent is that this stuff should be free to whomever wants it as
long as they keep the copyright message and clearly mark it as modified if
they change the content.

## Mechanics

I use the [hu.py](./hu.py) script to maintain this site.  A local clone of
this repository on my computer is used to build things by running a command
like ```python hu.py build .```.  This reads the [projects](./projects)
file (which uses YAML syntax to describe the projects), then constructs the
[projects page](./project_list.md) and copies the needed files to the
repository.  When things look right, they are committed and pushed to the
Github server.  Feel free to use this script and project file structure to
build your own website to archive things.  You'll also need the pyyaml
library from
[https://github.com/yaml/pyyaml](https://github.com/yaml/pyyaml).
