# vim: noet

r = /usr/local/bin/rst2html.py

all:  project_list.html tutorial.html

project_list.html:  project_list.rst
	$r $< >$@

tutorial.html:  tutorial.rst
	$r $< >$@
