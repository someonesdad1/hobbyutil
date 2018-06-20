# hobbyutil

Click [here](./project_list.md) to go to the projects page where you can download
the individual projects and read their descriptions.

This repository is for things (I'll call them projects here)  I've developed over
the years for my various hobbies.  Each project is a link which you can click on to
get the file(s) associated with the project.  For documents, the PDF form is
typically the only file included.  A project that contains more than one file will
be a zip archive.  If you would like the source documents (usually constructed from
an Open Office document), email me at {email_address} and I'll send you a zip file
containing the information that the project's data are constructed from.

For projects that are python scripts, I have standardized on python 3.6 for running
the scripts.  Many of these scripts have also been tested on python 2.7, but I am
no longer making the effort to keep things running with python 2.7, as python 3 is
mature and well-supported by the needed libraries.  If you see a script contain the
line

```from __future__ import division, print_function```

then it's probable that the script will run under python 2.7 Where self-tests are
available, they will be python scripts that have the same name as the script with
'\_test' appended.

The ./projects file in the repository is used to keep track of the things that are
in this repository (its main function is to map the files on my hard disk to the
file(s) in the project).  Note there are more things in this projects file than are
packaged in the repository; the things that are not included have an 'ignore'
string set, along with the reason for ignoring the project's contents.

This website contains updated information from a Google Code site; Google Code went
defunct in 2014.
