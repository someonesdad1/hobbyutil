# Makefile to build the HU repository

# The work is done by the hu.py script.  Edit the projects.py script to
# define what's included.  Run make to build the files.  The tasks done
# are: 
# 	- Runs 'python hu.py build .' to build everything
# 	- Runs the mk script 

all: build html 

html:  project_list.html tutorial.html
build: hu.py projects.py
	${PYTHON} hu.py build .

project_list.html: project_list.rst
tutorial.html:  tutorial.rst

#----------------------------------------------------------------------
# Recipes

rst = /bin/rst2html.py

%.html:  %.rst
	${rst} $< >$@

# vim: noet
