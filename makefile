# vim: noet

a:elec
all: elec basic html

basic: util/asc.py shop/bucket.zip science/astro.zip

#----------------------------------------------------------------------
# Commonly used variables for directories
d = /doc
e = /elec
m = /math
p = /pylib
P = /pylib/pgm
S = /science
s = /shop

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
shop/bucket.zip: $P/bucket.py $P/bucket.pdf
	zip -j $@ $^
science/astro.zip: $p/meeus.py $p/julian.py $p/kepler.py $p/test/meeus_test.py \
	$p/test/julian_test.py $p/test/kepler_test.py $P/moon.py
	zip -j $@ $^

#---------------------------------------------------------------------- 
${elec}: ${elec}/BNC_connector_power.pdf ${elec}/bode.py ${elec}/CurrentSource.pdf \
	${elec}/fuse_as_shunt.pdf ${elec}/hppn.zip ${elec}/impedance.py \
	${elec}/ind.zip ${elec}/logic_probe.pdf ${elec}/MeasuringESR.pdf \
	${elec}/octopus.pdf ${elec}/PartsStorageMethods.pdf \
	${elec}/PortableVoltageStandard.pdf ${elec}/react.zip ${elec}/res.zip \
	${elec}/RMS.pdf ${elec}/wave.zip
${elec}/BNC_connector_power.pdf: $e/components/BNC_connector_power.pdf
	cp $^ $@
${elec}/bode.py:  $P/bode.py
	cp $^ $@
${elec}/CurrentSource.pdf: $e/projects/CurrentSource.pdf
	cp $^ $@
${elec}/fuse_as_shunt.pdf: $e/projects/fuse_as_shunt/fuse_as_shunt.pdf
	cp $^ $@
${elec}/hppn.zip: $e/hp/0readme $e/hp/hp.py $e/hp/hp_parts
	zip -j $@ $^
${elec}/impedance.py: $P/impedance.py
	cp $^ $@
i = inductance
a = $e/software/coil_$i
${elec}/ind.zip: $a/$i.ods $a/$i.pdf $a/$i_spreadsheet.pdf
	zip -j $@ $^
${elec}/logic_probe.pdf: $e/projects/logic_probe/logic_probe.pdf
	cp $^ $@
${elec}/MeasuringESR.pdf: $e/Articles/MeasuringESR.pdf
	cp $^ $@
${elec}/octopus.pdf: $e/projects/octopus/Octopus_new.pdf
	cp $^ $@
${elec}/PartsStorageMethods.pdf: $e/projects/PartsStorageMethods.pdf
	cp $^ $@
${elec}/PortableVoltageStandard.pdf: $e/Articles/PortableVoltageStandard.pdf
	cp $^ $@
a = $e/software/reactance_chart
${elec}/react.zip: $a/reactance_notes.pdf $a/out/reactance.pdf \
		$a/out/big_reactance.pdf $a/../ohms_law_chart/OhmsLaw1.pdf \
		$a/../ohms_law_chart/OhmsLaw2.pdf
	zip -j $@ $^
a = $e/software/resistors
${elec}/res.zip: $a/makefile $a/resistor.cpp $a/resistor.pdf $a/resistor.test
	zip -j $@ $^
${elec}/RMS.pdf: $e/Articles/RMS.pdf
	cp $^ $@
${elec}/wave.zip: $P/waveform.py $P/waveform.pdf
	zip -j $@ $^
