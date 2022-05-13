`Home <https://someonesdad1.github.io/hobbyutil/>`_

.. contents:: Table of Contents

r link is file size in units of 1000 bytes.

Unless otherwise noted, the python scripts are written to run with
python 3.6 or later.  If the script contains a line like ``from
__future__ ...``, then it is possible that it will also run under python
2.7.
Electrical
==========

| `elec/BNC_connector_power.pdf <elec/BNC_connector_power.pdf>`_ (1645)
|   Gives some experimental data about using RF coax cables
with BNC connectors for DC and low-frequency power.
| `elec/bode.py <elec/bode.py>`_ (3)
|   Generate a Bode plot with a python script (needs numpy and
matplotlib).  You define the transfer function in a file
passed on the command line.
| `elec/CurrentSource.pdf <elec/CurrentSource.pdf>`_ (201)
|   How to make a battery-operated 1 ampere current source used to
make low resistance measurements.
| `elec/MeasuringESR.pdf <elec/MeasuringESR.pdf>`_ (230)
|   Describes a technique of estimating a capacitor's ESR (equivalent
series resistance) without having to buy a special meter.
| `elec/fuse_as_shunt.pdf <elec/fuse_as_shunt.pdf>`_ (486)
|   Notes on using ATO automobile fuses as poor-man's shunts.
| `elec/hppn.zip <elec/hppn.zip>`_ (23)
|   This is a compilation of various 8-digit HP part numbers
translated into conventional industry part numbers.  This list may
be of use to those with old HP instruments that need to find a
replacement part.
| `elec/impedance.py <elec/impedance.py>`_ (5)
|   This python script will take a complex impedance in polar
coordinates and print out the series and parallel models' values,
reactance, dissipation factor, and quality factor.
| `elec/ind.zip <elec/ind.zip>`_ (971)
|   Provides an Open Office spreadsheet that can calculate the
inductance of common electrical structures.  Includes a PDF
document describing the use and which gives references for
the formulas used.
| `elec/logic_probe.pdf <elec/logic_probe.pdf>`_ (4258)
|   Discusses the use of a logic probe.
| `elec/octopus.pdf <elec/octopus.pdf>`_ (1753)
|   Build an Octopus, a handy electrical troubleshooting tool (you need
an oscilloscope).
| `elec/PartsStorageMethods.pdf <elec/PartsStorageMethods.pdf>`_ (450)
|   Describes one way of storing lots of little electronic parts
and how to find them quickly.
| `elec/react.zip <elec/react.zip>`_ (84)
|   Contains two reactance charts in PDF form along with a short
file describing their use.
| `elec/res.zip <elec/res.zip>`_ (282)
|   Contains two tools that help you deal with resistors.
| `elec/RMS.pdf <elec/RMS.pdf>`_ (133)
|   An article for hobbyists about making RMS electrical measurements.
| `elec/PortableVoltageStandard.pdf <elec/PortableVoltageStandard.pdf>`_ (126)
|   Simple voltage standard you can make with one resistor, an IC
that costs about a buck, and three AA batteries.


Engineering
===========

| `eng/antifreeze.pdf <eng/antifreeze.pdf>`_ (1389)
|   How to calculate how much antifreeze to add to an existing
partially-filled radiator to get a desired concentration.  Also
looks at the refractometer.
| `eng/flow.pdf <eng/flow.pdf>`_ (18)
|   Nomograph for pipe flow.
| `eng/iapws.zip <eng/iapws.zip>`_ (72)
|   Contains C++ and python code that implements the IAPWS95
equations for the thermodynamic properties of water.
| `eng/pqs.zip <eng/pqs.zip>`_ (550)
|   Python scripts to simulate a production process that is inspected
by a measurement process with a significant measurement uncertainty.


Math
====

| `math/AnalyticGeometry.pdf <math/AnalyticGeometry.pdf>`_ (4311)
|   Contains formulas relating to analytic geometry and other
math stuff I need to look up on a regular basis.
| `math/BusinessCardMathTables.pdf <math/BusinessCardMathTables.pdf>`_ (524)
|   A document containing small math tables that will print
out to be about the size of a business card.
| `math/Concise300.pdf <math/Concise300.pdf>`_ (518)
|   Discusses the Concise 300, a circular slide rule still in
production in Japan.
| `math/DinosaurArithmeticSmall.pdf <math/DinosaurArithmeticSmall.pdf>`_ (778)
|   This document discusses doing calculations without using an
electronic calculator.  It's useful for a technical person to know
how to reason quantitatively when a calculator isn't handy.
| `math/dmath.zip <math/dmath.zip>`_ (94)
|   Contains a python module dmath.py that is a drop-in replacement
(nearly) for the python math module when calculating with python's
Decimal numbers.  Using this library, you can calculate elementary
functions to any desired accuracy.
| `math/ElementaryFunctions.pdf <math/ElementaryFunctions.pdf>`_ (1048)
|   Graphs of a variety of elementary math functions, useful
for a quick picture of how they behave or to grab one or two
significant figures of the value.
| `math/frange.zip <math/frange.zip>`_ (18)
|   A python module that provides a floating point analog to
range().  Doesn't suffer from the typical floating point problems
seen in naive implementations.
| `math/fseq.zip <math/fseq.zip>`_ (433)
|   Contains a python script fseq.py that provides general-purpose
sequence generation (arithmetic, geometric, logarithmically-spaced,
etc.).  The script also provides useful random number generation
facilities for doing Monte Carlo calculations at the command
line, along with CDFs and PDFs of some distributions.  Requires
numpy.
| `math/gpaper.zip <math/gpaper.zip>`_ (105)
|   Provides some common graph papers in PDF files that print
on ANSI A paper.
| `math/oo_math.zip <math/oo_math.zip>`_ (268)
|   Introduces the equation-writing capabilities of Open Office
2.0.  Includes a cheatsheet that you can modify.
| `math/primes.zip <math/primes.zip>`_ (20)
|   Some python scripts that deal with primes, factoring, and
integer properties.
| `math/QuickMultDiv.pdf <math/QuickMultDiv.pdf>`_ (111)
|   Discussion of how to do multiplications and divisions
by hand when you only need a specified number of significant
figures in the answer.
| `math/rand.zip <math/rand.zip>`_ (161)
|   A pure python script for generating random numbers from various
distributions to stdout.
| `math/root.zip <math/root.zip>`_ (59)
|   Pure-python root-finding methods such as bisection, Brent's
method, Ridder's method, Newton-Raphson, and a general-purpose
method by Jack Crenshaw that uses inverse parabolic interpolation.
| `math/scale.zip <math/scale.zip>`_ (480)
|   The scale.pdf file contains two sheets of paper with slide rule
type scales on them. You may find it useful for simple technical
calculations.
| `math/seq.zip <math/seq.zip>`_ (19)
|   Python script to send various arithmetical progressions
to stdout.  Handles integers, floating point, and fractions.
| `math/shorttbl.zip <math/shorttbl.zip>`_ (370)
|   A set of tables of elementary math functions intended to
print on half of an ANSI-A sized piece of paper.
| `math/spiral.zip <math/spiral.zip>`_ (15)
|   Python scripts that deal with spirals.
| `math/TrigDegrees.pdf <math/TrigDegrees.pdf>`_ (121)
|   Gives some algebraic expressions for a few special values
of trigonometric functions in degrees.
| `math/triguc.zip <math/triguc.zip>`_ (109)
|   Contains a vector drawing of the trig functions on the unit
circle.  The python script used to generate the graphics is
included, so you can tweak it to your tastes.


Miscellaneous
=============

