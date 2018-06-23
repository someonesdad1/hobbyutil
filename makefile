# vim: noet

p = project_list

$p.html:  $p.rst
	/usr/local/bin/rst2html.py $< >$@
