# vim: noet

p = project_list
t = tutorial
r = /usr/local/bin/rst2html.py

all:  $p.html $t.html

$p.html:  $p.rst
	$r $< >$@
$t.html:  $t.rst
	$r $< >$@
