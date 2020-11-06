# Makefile to build the HU repository.  These are files collected from
# around my system that 

# Note that many of the python scripts (like frange.py) that include
# their unit tests also need lwtest.py.

a:elec
all: elec basic html

basic: util/asc.py shop/bucket.zip science/astro.zip

#----------------------------------------------------------------------
# Commonly used variables for directories
p = /pylib
pp = /pylib/pgm

# Project's directories
elec = elec
eng = eng
math = math
misc = misc
prog = prog
science = science
shop = shop
util = util

# Tools
rst = /usr/local/bin/rst2html.py
Z = zip -j

#----------------------------------------------------------------------
html:  project_list.html tutorial.html
*.html:  *.rst
	${rst} $< >$@

#----------------------------------------------------------------------
# Experimental stuff to test the idea of converting hu.py to a plain makefile

# Target with one file
util/asc.py: /pylib/pgm/asc.py
	cp $< util
# Target with more than one file
shop/bucket.zip: ${pp}/bucket.py ${pp}/bucket.pdf
	$J $@ $^
science/astro.zip: $p/meeus.py $p/julian.py $p/kepler.py $p/test/meeus_test.py \
	$p/test/julian_test.py $p/test/kepler_test.py ${pp}/moon.py
	$J $@ $^

#---------------------------------------------------------------------- 
# Electrical 
E = elec
e = /elec
$E: $E/BNC_connector_power.pdf $E/bode.py $E/CurrentSource.pdf \
	$E/fuse_as_shunt.pdf $E/hppn.zip $E/impedance.py \
	$E/ind.zip $E/logic_probe.pdf $E/MeasuringESR.pdf \
	$E/octopus.pdf $E/PartsStorageMethods.pdf \
	$E/PortableVoltageStandard.pdf $E/react.zip $E/res.zip \
	$E/RMS.pdf $E/wave.zip
$E/BNC_connector_power.pdf: $e/components/BNC_connector_power.pdf
	cp $^ $@
$E/bode.py:  ${pp}/bode.py
	cp $^ $@
$E/CurrentSource.pdf: $e/projects/CurrentSource.pdf
	cp $^ $@
$E/fuse_as_shunt.pdf: $e/projects/fuse_as_shunt/fuse_as_shunt.pdf
	cp $^ $@
$E/hppn.zip: $e/hp/0readme $e/hp/hp.py $e/hp/hp_parts
	$Z $@ $^
$E/impedance.py: ${pp}/impedance.py
	cp $^ $@
i = inductance
a = $e/software/coil_$i
$E/ind.zip: $a/$i.ods $a/$i.pdf $a/$i_spreadsheet.pdf
	$Z $@ $^
$E/logic_probe.pdf: $e/projects/logic_probe/logic_probe.pdf
	cp $^ $@
$E/MeasuringESR.pdf: $e/Articles/MeasuringESR.pdf
	cp $^ $@
$E/octopus.pdf: $e/projects/octopus/Octopus_new.pdf
	cp $^ $@
$E/PartsStorageMethods.pdf: $e/projects/PartsStorageMethods.pdf
	cp $^ $@
$E/PortableVoltageStandard.pdf: $e/Articles/PortableVoltageStandard.pdf
	cp $^ $@
a = $e/software/reactance_chart
$E/react.zip: $a/reactance_notes.pdf $a/out/reactance.pdf \
		$a/out/big_reactance.pdf $a/../ohms_law_chart/OhmsLaw1.pdf \
		$a/../ohms_law_chart/OhmsLaw2.pdf
	$Z $@ $^
a = $e/software/resistors
$E/res.zip: $a/makefile $a/resistor.cpp $a/resistor.pdf $a/resistor.test
	$Z $@ $^
$E/RMS.pdf: $e/Articles/RMS.pdf
	cp $^ $@
$E/wave.zip: ${pp}/waveform.py ${pp}/waveform.pdf
	$Z $@ $^

# vim: noet
