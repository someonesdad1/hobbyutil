# Makefile to build the elec directory

p = /pylib
P = $p/pgm
Z = zip -j

#---------------------------------------------------------------------- 
e = /elec
all:  BNC_connector_power.pdf \
	bode.py \
	CurrentSource.pdf \
	fuse_as_shunt.pdf \
	hppn.zip \
	impedance.py \
	ind.zip \
	logic_probe.pdf \
	MeasuringESR.pdf \
	octopus.pdf \
	PartsStorageMethods.pdf \
	PortableVoltageStandard.pdf \
	react.zip \
	res.zip \
	RMS.pdf \
	wave.zip 

BNC_connector_power.pdf: $e/components/BNC_connector_power.pdf
	cp $^ $@

bode.py:  $P/bode.py
	cp $^ $@

CurrentSource.pdf: $e/projects/CurrentSource.pdf
	cp $^ $@

fuse_as_shunt.pdf: $e/projects/fuse_as_shunt/fuse_as_shunt.pdf
	cp $^ $@

hppn.zip: $e/hp/0readme $e/hp/hp.py $e/hp/hp_parts
	$Z $@ $^

impedance.py: $P/impedance.py
	cp $^ $@

i = inductance
a = $e/software/coil_$i
ind.zip: $a/$i.ods $a/$i.pdf $a/$i_spreadsheet.pdf
	$Z $@ $^

logic_probe.pdf: $e/projects/logic_probe/logic_probe.pdf
	cp $^ $@

MeasuringESR.pdf: $e/Articles/MeasuringESR.pdf
	cp $^ $@

octopus.pdf: $e/projects/octopus/Octopus_Jul2012.pdf
	cp $^ $@

PartsStorageMethods.pdf: $e/projects/PartsStorageMethods.pdf
	cp $^ $@

PortableVoltageStandard.pdf: $e/Articles/PortableVoltageStandard.pdf
	cp $^ $@

a = $e/software/reactance_chart
react.zip: $a/reactance_notes.pdf $a/out/reactance.pdf \
		$a/out/big_reactance.pdf $a/../ohms_law_chart/OhmsLaw1.pdf \
		$a/../ohms_law_chart/OhmsLaw2.pdf
	$Z $@ $^

a = $e/software/resistors
res.zip: $a/makefile $a/resistor.cpp $a/resistor.pdf $a/resistor.test
	$Z $@ $^

RMS.pdf: $e/Articles/RMS.pdf
	cp $^ $@

wave.zip: $P/waveform.py $P/waveform.pdf
	$Z $@ $^

# vim: noet
