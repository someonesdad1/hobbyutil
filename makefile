# Makefile to build the HU repository

# TODO:  

# Need to write a makefile in each of the directories:  elec, eng,
# math, misc, prog, science, shop, util

# Need to have the project_list.html file generated.  This comes from
# the hu.py script, so a suitable substitute needs to be designed.

#----------------------------------------------------------------------

all: html basic
	cd elec; make

basic: util/asc.py shop/bucket.zip science/astro.zip
html:  project_list.html tutorial.html

#----------------------------------------------------------------------
# Experimental stuff to test the idea of converting hu.py to a plain makefile
#   $@ is file name of target rule
#   $^ is all dependencies with a space between them
#   $? is all dependencies newer than target
#   $< is first dependency

p = /pylib
P = $p/pgm
Z = zip -j

# Target with one file
util/asc.py: /pylib/pgm/asc.py
	cp $< util
# Target with two files
shop/bucket.zip: $P/bucket.py $P/bucket.pdf
	$Z $@ $^
# Multiple files
science/astro.zip: $p/meeus.py $p/julian.py $p/kepler.py $p/test/meeus_test.py \
	$p/test/julian_test.py $p/test/kepler_test.py $P/moon.py
	$Z $@ $^

#----------------------------------------------------------------------
# Recipes

rst = /usr/local/bin/rst2html.py

*.html:  *.rst
	${rst} $< >$@

# vim: noet
