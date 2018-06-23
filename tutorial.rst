This document describes the process of using Github for archiving digital
information.  I'll describe things in words without pictures, as the
snapshots of what you'll see on a web page often change over time and
become outdated.

.. contents:: Table of Contents

Get a Github account
====================

Go to `https://github.com/ <https://github.com/>`_ and open an account.
You'll need an email address, a user name, and a password.

Create a Hello World repository
===============================

If you've not used a distributed version control tool before, I suggest you
click on the "Read the Guide" button, which takes you to the
`https://guides.github.com/activities/hello-world/
<https://guides.github.com/activities/hello-world/>`_ page.  This exercise
will create a repository and show you some basic operations like working on
a branch and committing your changes.  You can delete the repository after
you're finished (go to the bottom of the page after you click on the
Settings tab).

Note the tabs at the top of the page.  The two you'll probably use the most
are Code to see the repository's files and content and Settings to change
the project's settings.  I use the Issues tab to keep a to do list.

Get git installed on your system
================================

This step is optional, but if you are an experienced software person,
you'll probably want to do it because you'll be able to work more quickly
than using Github's clunky web interface.  If you have a lot of stuff
to archive and organize, you'll be able to use command line tools, scripts,
and makefiles to automate the tasks.  

I use these command line tools because the things I archive are scattered
all over my computer.  They need to be copied to the repository if the
computer copy is more recent than the repository copy.  Then things need to
be packaged up and checked into the repository.  Since I have hundreds of
packages and documents, this needs to be automated to keep my work to a
minimum.

Go to `https://git-scm.com/downloads <https://git-scm.com/downloads>`_ and
download a suitable git package for your system.  I recommend you learn to
use the command line version of git first.  Once you're familiar with the
basic operations, you can change to a GUI tool if you wish.

I use the Windows package of git under cygwin.  I found I had to create a
hard link to the Windows' ``cmd.exe`` file in my bin directory containing my
tools; otherwise, many of the git commands failed mysteriously.

Get the Pro Git book
====================

I recommend you download a copy of the book "Pro Git", 2nd edition, 2014
and peruse it
`https://git-scm.com/book/en/v2 <https://git-scm.com/book/en/v2>`_.  It will
focus on the command line use of git and will teach you some of the key
things needed to work with a distributed version control system.  

Read the two chapters "Getting Started" and "Git Basics", as these will
give you most of what you need to know about git to construct a repository
to store your digital archives.

With the command line git tool, you can get help in three common ways:
    
* Type the command ``git`` by itself to see a usage statement containing the
  frequently used commands.
* When you know which command you want to use, use ``git <cmd> -h`` to see
  abbreviated help for that command.
* Use ``git help <cmd>`` to have a manpage for that command opened in your
  browser.

Create your archival repository
===============================

Here's where you actually start work on archiving your data.  After you've
logged in to Github, you can press the New repository button to create your
archive repository.  Give it a short meaningful name.  You'll probably want
to check the button to include a README file.  This results in a README.md
file in the root directory of the archive; this is a file that uses
Github's markdown to create a web page.

Choose a suitable license for the repository if you like.

You can consider your first archival repository a prototype to allow
you to experiment.  You don't need to worry about anything being permanent
right now, as you can go to the Settings tab and delete the repository
whenever you want.  You'll lose all your changes, so don't do this until
you're sure.

Create a GitHub Pages interface
===============================

You can provide your users with a web page interface that is hosted from
your repository.  Click on the Settings tab from the project page and
scroll down to the GitHub Pages box.  The Source selection chooses where
the web page data come from and you can select what theme (visual
appearance) to use.

Your README.md file will be the top-level page of your website.  It uses
Github's markdown and you can construct your repository's website as you
wish.  Your website will have a URL such as ``https://xxx.github.io/yyy/``
where ``xxx`` is your login name and ``yyy`` is your repository's name.

Refer to
`https://help.github.com/articles/basic-writing-and-formatting-syntax/
<https://help.github.com/articles/basic-writing-and-formatting-syntax/>`_
for more information on Github markdown syntax.

Development pattern
===================

Here's the development pattern I use for my repository.  Whenever I see
something that needs to be done, I go to the Issues tab on the Github web
interface and enter an Issue for this item (otherwise, I'm likely to forget
this issue if I start working on something else).  This turns it into my to
do list.  Then I pick which issue to work on.

I have a clone of the Github repository on my system and this is where I do
all my work.  The following pattern is repeated over and over:

* I edit, add, and delete files as needed.  When I reach a point where I
  want the changes to be remembered, I go to the next step.
* I tell the repository which changes to include using the ``git add file1
  file2 ...`` command.  This command stages new and changed files for
  inclusion into the next submission to the repository.  
* When I'm satisfied with the instructions on how to change the repository
  (see the pending changes with the ``git status`` command), I commit the
  changes to the repository using ``git commit -a``.
* After one or more commits, I decide it's time to update the repository
  stored on Github.  This is done with the ``git push`` command.

For a simple project like my hobbyutil archive, I don't need things like
branches or tags because I do everything on the master branch.

Other thoughts
==============

For long-term archiving of data, you'll want to pay attention to the file
formats you use and the type of data you archive.  For example, I had a
Lotus 1-2-3 spreadsheet on a 3.5 inch floppy disk I created on an HP 9816
computer in the early 1980's, even before the IBM PC appeared.  That data
might as well be on the far side of the moon because I no longer have the
the hardware nor the software to be able to access it.

You can do some web research about suitable formats for the long-term
archiving of data.  File formats that are probably pretty safe are JPG,
PNG, TIFF, 7-bit ASCII, and some common 8-bit text encodings.  Modern
Unicode encodings (especially in UTF-8) are likely to be pretty safe.

PDF by itself probably isn't a good choice, as there are many clients and
incompatible changes, encryption, etc.  However, look at using the PDF/A
format for documents, as it is an ISO standard aimed at providing
archivability and includes the fonts used in the PDF document.  Its
fundamental goal is to maintain the document's look.

Things like Open Office, Microsoft Office, and RTF are also going to
continue to be used by people, but they are somewhat more risky -- you
don't know when the support of suitable tools will get broken in the
future.  It will eventually happen and you will likely have little to no
warning.

You'll want to be careful with sound and multimedia files too.  Consult
places like the Library of Congress to see which formats are recommended.

Another problem is bit rot.  This is where copies of digital information
get made, but small changes may occur in the file like a DNA mutation --
and you're unaware of the mistake.  Even a single bit change can make a
file unusable.  You won't know this happens unless you regularly check for
such things using hashes and binary compares.  When it happens, you'll get
that horrible feeling in the pit of your stomach like when you smugly think
your disk crash is protected by your backups -- when you try to do a
restore from your backups, you find out they are broken and your data are
totally lost.  That's why the pros **always** verify the complete process of
backing up and restoring **before** an emergency occurs.
