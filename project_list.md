[Home](./README.md)

Click on the links to download a project's file(s).

## Electrical

Link | Description
--- | ---
[elec/BNC_connector_power.pdf](elec/BNC_connector_power.pdf) | Gives some experimental data about using RF coax cables with BNC connectors for DC and low-frequency power.
[elec/bode.py](elec/bode.py) | Generate a Bode plot with a python script (needs numpy and matplotlib).  You define the transfer function in a file which is passed on the command line.
[elec/CurrentSource.pdf](elec/CurrentSource.pdf) | Describes how to make a battery-operated 1 ampere current source used to make low resistance measurements.  You can measure to 0.1 milliohm with the typical digital multimeter.
[elec/MeasuringESR.pdf](elec/MeasuringESR.pdf) | Describes a technique of estimating a capacitor's ESR (equivalent series resistance) without having to buy a special meter.
[elec/hppn.zip](elec/hppn.zip) | This is a compilation of various 8-digit HP part numbers translated into more identifiable numbers. For example, a typical line is 1820-0839 TTL IC SN74175N.  This list may be of use to those with old HP instruments that need to find a replacement part. There are only about 2700 parts in this list, so it cannot be considered complete.  A python script can do the lookup tasks.
[elec/impedance.py](elec/impedance.py) | This python script will take a complex impedance in polar coordinates and print out the series and parallel models' values, reactance, dissipation factor, and quality factor.  I find this handy with an LCR meter -- I usually have the LCR meter measure the impedance and write that down; this script lets me then see all the other related parameters.  The measurement frequency is 1 kHz, but you can change this with a command line option.
[elec/ind.zip](elec/ind.zip) | Provides an Open Office spreadsheet that can calculate the inductance of common electrical structures.  Includes a PDF document describing the use and which gives references for the formulas used.  There is also a PDF file of the spreadsheet so that you can see what it looks like without having Open Office -- this will help you decide if you want to download and install Open Office to be able to use the spreadsheet.
[elec/oct.zip](elec/oct.zip) | If you own an oscilloscope and like to troubleshoot electrical things, you'll probably want to build an Octopus tester.  One can be built from a 6.3 V RMS filament transformer and a single resistor, so there's no significant parts costs.  It's a handy troubleshooting tool.  People have been using them since the 1930's.
[elec/PartsStorageMethods.pdf](elec/PartsStorageMethods.pdf) | Describes one way of storing lots of little electronic parts and how to find them quickly.
[elec/react.zip](elec/react.zip) | Contains two reactance charts in PDF form along with a short file describing their use. Update 20 May 2013 - added similar charts for Ohm's Law.
[elec/RMS.pdf](elec/RMS.pdf) | An article for hobbyists about making RMS electrical measurements.
[elec/PortableVoltageStandard.pdf](elec/PortableVoltageStandard.pdf) | Here's a cheap and simple voltage standard you can make with one resistor, an IC that costs about a buck, and three AAA batteries (and it doesn't need a power switch). The last set of batteries of mine lasted for 4.8 years and the standard deviation of the voltage output was 170 uV including room temperature variations and the variance of the voltmeter over that time period.
[elec/wave.zip](elec/wave.zip) | Provides a python script (uses numpy and scipy) that lets you construct various waveforms used in engineering and science tasks. The design and semantics allow you to construct more complex composite waveforms.  It's also easy to add new waveform definitions.

## Engineering

Link | Description
--- | ---
[eng/antifreeze.pdf](eng/antifreeze.pdf) | How to calculate how much antifreeze to add to an existing partially-filled radiator to get a desired concentration.  It also looks at the refractometer, a tool to measure antifreeze concentrations and a lead-acid battery's sulfuric acid specific gravity (which tells you the state of charge).
[eng/eng_grid.py](eng/eng_grid.py) | This python script will generate most any linear isotropic graph paper by creating a PostScript file.
[eng/iapws.zip](eng/iapws.zip) | This zipfile contains C++ and python code that implements the IAPWS95 equations for the thermodynamic properties of water. See http://www.iapws.org/relguide/IAPWS-95.htm IAPWS95
[eng/flow.pdf](eng/flow.pdf) | Nomograph for pipe flow.
[eng/pqs.zip](eng/pqs.zip) | This package contains python scripts that make it easy to simulate a production process that is inspected by a measurement process with a significant measurement uncertainty.  Such a situation can result in significant producer's and consumer's risk.  It's easy to understand how this Monte Carlo simulation script works and believe its output.

## Math

Link | Description
--- | ---
[math/AnalyticGeometry.pdf](math/AnalyticGeometry.pdf) | Contains formulas relating to analytic geometry in the plane. Well, it started out this way, but it now includes trig, mensuration, and other stuff that I need to look up on a regular basis.
[math/BusinessCardMathTables.pdf](math/BusinessCardMathTables.pdf) | A document containing small math tables that will print out to be about the size of a business card.
[math/Concise300.pdf](math/Concise300.pdf) | Discusses the Concise 300, a circular slide rule still in production in Japan. If you've never used a slide rule, you may be surprised to find that they can be good tools to help you with calculations accurate to roughly one percent.
[math/DinosaurArithmeticSmall.pdf](math/DinosaurArithmeticSmall.pdf) | This document discusses doing calculations without using an electronic calculator.  I'm not advocating that we give up our calculators, but it's useful for a technical person to know how to reason quantitatively when a calculator isn't handy.
[math/dmath.zip](math/dmath.zip) | Contains a python module dmath.py that is a drop-in replacement (nearly) for the python math module when calculating with python's Decimal numbers.  Using this library, you can calculate elementary functions to any desired accuracy.  To make the switch, just change e.g.  'import math' to 'import dmath as math'.
[math/ElementaryFunctions.pdf](math/ElementaryFunctions.pdf) | Graphs of a variety of elementary math functions, useful for a quick picture of how they behave or to grab one or two significant figures of the value.
[math/frange.zip](math/frange.zip) | A python module that provides a floating point analog to range().  Doesn't suffer from the typical floating point problems seen in naive implementations.
[math/fseq.zip](math/fseq.zip) | Contains a python script fseq.py that provides general-purpose sequence generation (arithmetic, geometric, logarithmically-spaced, etc.).  The script also provides useful random number generation facilities for doing Monte Carlo calculations at the command line, along with CDFs and PDFs of some distributions. It's easy to add support for other distributions.  See seq.py for a simpler script that just provides arithmetic series.
[math/gpaper.zip](math/gpaper.zip) | Provides some common graph papers in PDF files that print on ANSI  A paper.  The python script that made them is included, so you can hack things if you e.g. want to change to A4 paper or modify colors or line widths.
[math/oo_math.zip](math/oo_math.zip) | Introduces the equation-writing capabilities of Open Office 2.0.  I find that I have no need for LaTeX given the equation-handling abilities of Open Office. While not as powerful as TeX or LaTeX, it's adequate for my needs and provides a variety of other tools.  Also includes a cheatsheet that you can modify.
[math/parse_complex.py](math/parse_complex.py) | Python module that allows you to parse complex numbers when they are written in the ways humans like to write them.
[math/QuickMultDiv.pdf](math/QuickMultDiv.pdf) | Short discussion of how to do multiplications and divisions by hand when you only need a specified number of significant figures in the answer. The methods reduce the amount of work needed over the methods taught in grammar school. Also includes a short blurb on additions.
[math/root.zip](math/root.zip) | Pure-python root-finding methods such as bisection, Brent's method, Ridder's method, Newton-Raphson, and a general-purpose method by Jack Crenshaw that uses inverse parabolic interpolation.
[math/rpath.zip](math/rpath.zip) | A python module for a rectilinear path object.  You supply it with a set of points and then you can interpolate to points on the path via a parameter.
[math/scale.zip](math/scale.zip) | The scale.pdf file contains two sheets of paper with slide rule type scales on them. If you duplex print this and keep it in a binder, you may find it useful for simple technical calculations when an electronic calculator isn't handy. The other file explains how to use things.
[math/seg.py](math/seg.py) | Python script to calculate parameters of a circular segment. Translated from a program written by Marv Klotz.
[math/shorttbl.zip](math/shorttbl.zip) | A set of tables of elementary math functions intended to print on half of an ANSI-A sized piece of paper. These tables are intended for use when a calculator isn't available. The original is an Open Office spreadsheet -- email me if you'd like a copy of it.
[math/spiral.zip](math/spiral.zip) | Python scripts that deal with spirals.  spiral.py is an interactive tool to calculate various spiral parameters. archimedean.py is a python module containing a function that calculates the exact length of an Archimedean spiral.
[math/tri.zip](math/tri.zip) | Python script to solve triangles.
[math/TrigDegrees.pdf](math/TrigDegrees.pdf) | Gives some algebraic expressions for a few special values of trigonometric functions in degrees.
[math/triguc.zip](math/triguc.zip) | Contains a vector drawing of the trig functions on the unit circle.  The python script used to generate the graphics is included, so you can tweak it to your tastes.
[math/xyz.zip](math/xyz.zip) | Contains a python script that provides a mini-language to perform analytical geometry calculations in 2 and 3 dimensions.  Use translations, rotations, and dilatations to transform to different coordinate systems.  Geometric objects provided are points, lines, and planes. The script can calculate their intersections, reflections, and projections and find angles and distances between them.

## Miscellaneous

Link | Description
--- | ---
[misc/Donor.pdf](misc/Donor.pdf) | Organ donation became an important topic for me after my granddaughter was killed.
[misc/fountain_pen_primer.pdf](misc/fountain_pen_primer.pdf) | Discusses the care and feeding of fountain pens as writing tools.
[misc/Markup.pdf](misc/Markup.pdf) | Derives the equations for markup and profit used in business.
[misc/Mortgage.pdf](misc/Mortgage.pdf) | Gives a table that lets you estimate your mortgage's monthly payment.  Doesn't include taxes or insurance.
[misc/paper.py](misc/paper.py) | Contains a python script to calculate various things about paper.  You input the grammage in grams per square meter, size of the paper sheet, number of sheets, and an optional cost and various metrics about the paper are printed out. Lets you compare paper purchases by e.g.  looking at the cost in $ per square meter. I wrote this script to help me evaluate whether I should start a specialty paper business (the results convinced me I shouldn't).
[misc/paper_sizes.pdf](misc/paper_sizes.pdf) | Shows a scale drawing of various ISO and US paper sizes.
[misc/shaving.pdf](misc/shaving.pdf) | Some thoughts on shaving your beard.
[misc/XmasTomatoes.pdf](misc/XmasTomatoes.pdf) | Using Christmas tree lights to keep tomato plants from freezing at night.

## Programming

Link | Description
--- | ---
[prog/columnize.py](prog/columnize.py) | Python script to columnize a sequence into columns. Run it as a script to convert stdin to columns or use the Columnize() function in your own scripts. Somewhat similar to the UNIX pr command, but doesn't do pagination.
[prog/comb.py](prog/comb.py) | A python script that will produce permutations and combinations of the lines in a file. Can be useful for generating test cases.
[prog/fset.py](prog/fset.py) | Treat lines of files as a set. Allows you to look at the union, intersection, difference, etc. between the lines of various files.
[prog/hg.zip](prog/hg.zip) | Some python scripts that make it easier to work with Mercurial repositories.  delta.py shows you the revision numbers where a file changed; hgs.py shows you things like files that are not in the repository, changed files, etc.  fhg.py will find all Mercurial repositories under a given directory and show those needing a check-in.
[prog/license.zip](prog/license.zip) | This is a python script that will allow you to change the license  you use in your source code files.  This is done by replacing a string between two 'trigger' strings.  A number of open source licenses are included in the script (e.g., BSD, GPL2, etc.) and it's easy to include others.  The script will first check that all the indicated source files have the trigger strings and that backup copies of the source files can first be made.
[prog/manufy.py](prog/manufy.py) | A short python script that will convert text lines to have double quotes and a newline at the end. This is useful to allow you to quickly write manpages for C or C++ code. The script also has a -u option to unmanufy some text.
[prog/PythonFromCalc.pdf](prog/PythonFromCalc.pdf) | A document explaining how to call python functions from Open Office Calc spreadsheets.
[prog/out.zip](prog/out.zip) | Contains a python module that provides a utility object for printing string representations of objects to a stream.  I've used something like this for years and it's a good tool to replace the print command/function, which causes a bit of friction between python 2 and 3 code.  This module has been tested with both python 2 and 3.
[prog/python.zip](prog/python.zip) | Contains a document that discusses why learning the python programming language might be a good thing for technical folks.
[prog/seq.zip](prog/seq.zip) | Python script to send various arithmetical progressions to stdout.  Handles integers, floating point, and fractions. Also see fseq.py.
[prog/shuffle.c](prog/shuffle.c) | C program to randomly shuffle the bytes of a file. You can use either the internal simple linear congruential generator or an external source of random bytes (i.e., a file) to do the shuffling.
[prog/sig.zip](prog/sig.zip) | Contains a python script to format floating point numbers to a specified number of significant figures or round to a specified template. Works with floats, integers, python Decimals, fractions, mpmath numbers, numpy arrays, complex numbers, and numbers with uncertainty, including any mix of those number types in a container that can be iterated over.
[prog/stack.zip](prog/stack.zip) | A python module that implements a basic stack.  You have the options of making the stack homogeneous (i.e., it will only allow storage of one type of item) or of fixed size.
[prog/sumbytes.cpp](prog/sumbytes.cpp) | A short C++ program that will read all the bytes from the files given on the command line and compute various statistics from them. Outputs the number of bytes read, sum, sum of squares, mean, standard deviation, and minimum/maximum values.
[prog/ts.zip](prog/ts.zip) | The ts.py script provides facilities for text substitution in text files.  It has only 3 basic commands (define a substitution, turn  the output on/off, and include a file) and the ability to include blocks of python code in the text file.  Though it's relatively simple to use, it can provide a fair bit of power.
[prog/util.zip](prog/util.zip) | Contains a number of miscellaneous python functions I've written and collected from the web.
[prog/wordnum.zip](prog/wordnum.zip) | A python script that can convert back and forth between numbers and their word forms.  Handles short and long scales, ordinals, integers, floats (normal and exponential notation), and fractions.  Easy interface through an object's function call; wordnum(36) gives 'thirty six'; wordnum('thirty six') returns the integer 36.  Tested on python 2.7.6 and 3.4.0.
[prog/wrap.zip](prog/wrap.zip) | Two python scripts to wrap and unwrap text files. The unwrap.py script will take a typical text file with two line breaks between paragraphs and change the text to one long line per paragraph. This makes it suitable for importing into word processing programs. wrap.py does the opposite and turns text files with long lines into text files with lines wrapped at a given number of columns.
[prog/xor.zip](prog/xor.zip) | C++ program to XOR a data file and key file together to encrypt a file. While you'd want a cryptographically-secure one time pad for serious encryption work, a file compressed by e.g. zip, gzip, or bzip could be a practical substitute for the key file. Read the xor.pdf file for further thoughts. Also includes two python utilities that can generate one-time pads and create files with fixed or random bytes.
[prog/xref.cpp](prog/xref.cpp) | A C++ console program that will cross reference the tokens in a set of files -- each token will be listed in alphabetical order with the file it occurs in along with the line numbers it's found on.  It can perform spell checking.  It has a -k option which will split composite tokens in the source code and spell check the individual tokens (this helps identify composite tokens that are misspelled).

## Science

Link | Description
--- | ---
[science/astro.zip](science/astro.zip) | Collection of a few astronomical utilities, mostly derived from Meeus' books. meeus.py contains a number of Meeus' algorithms. julian.py contains Julian day routines. moon.py calculates the moon's phases. kepler.py solves the Kepler equation.
[science/chemical_names.pdf](science/chemical_names.pdf) | A list of archaic chemical names with their modern equivalents and chemical formulas.
[science/diameters.pdf](science/diameters.pdf) | Plots of circles showing the relative mean diameters of planets and moons in the solar system.
[science/diurnal_variations.pdf](science/diurnal_variations.pdf) | Shows a plot of the light from the sky measured with a cheap photodiode.  Since inexpensive datalogging equipment can be purchased that uses e.g. the USB interface, this would be a great experiment for school kids and parents to do together. Because it's so simple to do, I predict you'll get hooked if you try it.
[science/elements.zip](science/elements.zip) | Contains elements.pdf, a document that contains a periodic table of the elements, a plot of the vapor pressures of the elements, values of physical parameters sorted by value, and various physical parameters of the elements plotted as a function of atomic number.  I've wanted a document like this since the 1970's, but I knew that most of the work would be in manually typing in all the data from various places.  I was right...  :^)
[science/irr.py](science/irr.py) | Calculate irradiance over a wavelength band from a spectral irradiance data file. It is written to work with StellarNet spectroradiometer files, but it can easily be modified to work with other data files.
[science/mixture.py](science/mixture.py) | A python script to aid in mixture calculations. Adapted from a C program at http://www.myvirtualnetwork.com/mklotz/files/mixture.zip.
[science/novas.py](science/novas.py) | Translation into python of some C code from the US Naval Observatory (http://aa.usno.navy.mil/software/novas/novas_c/novasc_info.html) It contains routines that are nearly identical to those used for calculations of the Astronomical Almanac.
[science/SolarSystemScaleModel.pdf](science/SolarSystemScaleModel.pdf) | This document describes a python script that prints out the dimensions of a scaled solar system. You can use it to make a scale solar system in your yard or on your street. Be warned -- things will be smaller and farther apart than you think. This would be a good exercise for a parent and a child -- both will learn information you can't learn from a book.
[science/SphericalShell.pdf](science/SphericalShell.pdf) | Discusses gravitation and electrostatics inside a uniform spherical shell and why there is no force on a particle. Also looks at Henry Cavendish's elegant experiment in the 1700's showing that the exponent in Coulomb's Law is 2.
[science/u.zip](science/u.zip) | A lightweight python library module that provides conversion factors for various physical units.  Using a clever idea by Steve Byrnes, it can also perform dimensional checking to determine dimensional consistency of numerical calculations. Easy to use -- an experienced scientist or engineer will be using it in a few minutes after seeing an example (see the PDF in the package for details).
[science/GNU_units.pdf](science/GNU_units.pdf) | A short blurb on the capabilities of the useful GNU units program.  This is one of the most-used programs on my computer because I am constantly converting between various units. It can also help you do back-of-the-envelope type calculations and avoid making dumb unit mistakes that invalidate everything.

## Shop

Link | Description
--- | ---
[shop/ball.py](shop/ball.py) | Python script to calculate steps to turn a ball on a lathe.
[shop/bar.zip](shop/bar.zip) | Python script to print out a table of the masses of bar stock in different sizes. You can choose diameters of either inches or mm and get the table in units of kg/m, lbf/ft, or lbm/in. Use the -c option to get conversion factors for other materials.
[shop/bc.zip](shop/bc.zip) | Contains a python script that will calculate the Cartesian coordinates of holes on a bolt circle.
[shop/bucket.zip](shop/bucket.zip) | Shows how to calculate bucket volumes and mark volume calibration marks on nearly any bucket.  It turns out there's a reasonably simple closed formula for this, regardless of the cross-sectional shape of the bucket.  Includes a python script that will do the calculations for you (you'll have to modify the script if the bucket isn't round or square).
[shop/Calipers.pdf](shop/Calipers.pdf) | Discussion and use of old-style machinist calipers.
[shop/CartPlatform.pdf](shop/CartPlatform.pdf) | Simple platform for Harbor Freight garden cart.
[shop/chain.zip](shop/chain.zip) | Contains a python script and a document to help with chain drilling holes and disks.
[shop/circ3.zip](shop/circ3.zip) | Python script that calculates the radius/diameter of a circle that passes through three points. You can specify either the Cartesian coordinates of the points or the distances between the points. If you download the python uncertainties library, the script will calculate the uncertainty in the radius/diameter given one or more uncertainties for the points or distances.
[shop/MachinistClamp.pdf](shop/MachinistClamp.pdf) | Discusses machinist's parallel clamps, why they're useful, and how to make your own.
[shop/cove.zip](shop/cove.zip) | A python script and documentation that show you how to cut a cove with your table saw.  Use this formula and method when it just has to be done correctly on a workpiece you can't mess up on.
[shop/cut.zip](shop/cut.zip) | Contains a python script that will calculate a solution to the one-dimensional cutting problem.  This problem appears when you have a set of raw materials and need to cut a stated set of workpieces from the stock.  The algorithm used is one called first fit decreasing, which means to sort the stock and pieces to be cut by size, then select the largest piece and cut it from the smallest piece of stock.
[shop/Demagnetizer.pdf](shop/Demagnetizer.pdf) | Describes a simple demagnetizing tool you can make from scrap materials.
[shop/density.zip](shop/density.zip) | Python script to calculate densities of various materials. The script performs the following tasks.  Look up the density of a particular material, find materials that have a density close to a given value, express density information in desired units, and show results relative to a given density.
[shop/DitchPump_pub.pdf](shop/DitchPump_pub.pdf) | Comments and tips on using a ditch pump to water your lawn.
[shop/DraftingTriangleTip.pdf](shop/DraftingTriangleTip.pdf) | This is a simple modification to a 30-60-90 drafting triangle that lets you use it to draw 45 degree angles.
[shop/drules.pdf](shop/drules.pdf) | Contains some drafting rules that I've always wanted. These are primarily 6 inch scales both in inch and mm divisions. You can print them at full scale and glue them to a chunk of wood to make some handy scales.
[shop/fits.py](shop/fits.py) | Python script to calculate the required shaft or hole size given a basic dimension of a shaft or hole.
[shop/LayingOutFrustumWithDividers.pdf](shop/LayingOutFrustumWithDividers.pdf) | Shows how to lay out the frustum of a cone with dividers in your shop.
[shop/gblock.zip](shop/gblock.zip) | A C++ program to print out combinations of gauge blocks that yield a desired composite length (the subset sum problem). Should work with most any set of gauge blocks. Uses brute-force searching to find solutions -- it's not elegant, but it works.  A python script is also included that does the same task and it will probably be fast enough for most folks' needs.  The C++ code runs about an order of magnitude faster than the python code.
[shop/glendag.zip](shop/glendag.zip) | Describes a simple concrete sprinkler guard that my wife designed and built. We've used them for over 20 years and they work well, are simple to make, and cheap.
[shop/hammer.pdf](shop/hammer.pdf) | Discusses the common hammer types and making a new handle for one.
[shop/holes.zip](shop/holes.zip) | Contains a python script that will help you lay out holes that are equally-spaced around a circle.
[shop/HoseFitting.pdf](shop/HoseFitting.pdf) | Here's an effective way to secure a hose to a hose fitting. It's better than anything I've found in a store.
[shop/LittleVise.pdf](shop/LittleVise.pdf) | Describes a snall vise that is straightforward to make with a milling machine.  I made mine from some 1 inch square aluminum bar stock and it has proven useful.  Scale it up or down as needed.
[shop/mass.zip](shop/mass.zip) | Contains a python script that will calculate the volume and mass of a project constructed from various primitive geometrical objects.  This lets you e.g. evaluate the mass and volume of a prospective design and document it through the datafile describing it.
[shop/nozzle.pdf](shop/nozzle.pdf) | Describes a nice hose nozzle you can make if you have a lathe. It will work better for cleaning things off than the typical store-bought nozzles.
[shop/pipes.pdf](shop/pipes.pdf) | A document showing a derivation of a formula that can be used to make a template for cutting the end of a pipe so that it can be welded to another pipe.
[shop/PullingFencePosts.pdf](shop/PullingFencePosts.pdf) | Using a class 2 lever can be a surprisingly effective way to pull fence posts out of the ground.
[shop/refcards.zip](shop/refcards.zip) | Contains some reference cards that will print out on 4 by 6 inch cards. I find these handy to keep in my drafting materials box when I'm doing design work at a drafting board.
[shop/SawBuck.pdf](shop/SawBuck.pdf) | Describes a simple and easy to make sawbuck that's made from eight identical pieces of 2x4.  I made mine so that I could cut it from two 8 foot long  2x4s.  It should cost less than $10 and take less than an hour to make.  All you need to make it are a hand saw, drill/bits, and a screwdriver.
[shop/sine_sticks.pdf](shop/sine_sticks.pdf) | How to build a simple device from scrap that will measure angles in the shop.  Perhaps surprisingly, it can measure with resolution as good or better than a Starrett machinist's vernier protractor that costs hundreds of dollars.
[shop/square.pdf](shop/square.pdf) | How to use a carpenter's square to lay out angles from 1 degree to 44 degrees. The fractional values given will result in angles accurate to 0.01 degree, assuming your square and your layouts are accurate enough. I find an angle square a much handier tool for carpentry layout than the carpenter's square and it's accurate enough for the usual purposes.
[shop/thd.zip](shop/thd.zip) | Prints out various dimensions associated with threads. Calculates the values based on the ASME B1.1-1989 standard document. If you machine threads on a lathe, you may find this program handy.
[shop/weigh.pdf](shop/weigh.pdf) | Demonstrates how I weighed our trailer with a lever. With a 12 foot long 4x4, I was able to measure 2500 pounds.
[shop/YankeePushDrill.pdf](shop/YankeePushDrill.pdf) | Discusses the Yankee screwdriver, a useful tool that has been in production for more than 100 years.  Also called a push-drill, it's a mechanically-sophisticated tool that can drive screws and drill small holes.  While cordless drills are now the preferred tool for many shop tasks, you'll find that a Yankee screwdriver can still be handy.  This document shows you how to make bits for it, make an adapter that lets the Yankee use 1/4 inch hex bits, or make an adapter for 1/4 inch square drive sockets.  It also shows you how to take one of these screwdrivers apart so it can be cleaned.  Dimensional sketches are included of some parts that might need to be made.

## Utilities

Link | Description
--- | ---
[util/app.cpp](util/app.cpp) | Handy application if you like to work at a cygwin command line. Given one or more files, it will cause them to be opened with their registered application.
[util/asc.py](util/asc.py) | Console python script to print out ASCII character table in decimal, hex, or octal.
[util/bd.c](util/bd.c) | Performs a comparison between binary files; differences are printed in hex dump format. You can print an ASCII picture that represents where the different bytes in the files are in percentage through the file.
[util/bgrep.py](util/bgrep.py) | Python script to search for regular expressions and strings in binary files.
[util/bidict.zip](util/bidict.zip) | Creates a dictionary object in python that lets you treat it in both directions as a mapping. If bd is a bidict, you perform normal dictionary access as 'bd[key]', while getting the key that corresponds to a particular value is gotten via 'bd(value)'. I wrote this because an application needed to get both the number of month names (e.g., Feb to 2 and be able to get the month name associated with a month number). It's an example of a discrete bijective function.
[util/cnt.zip](util/cnt.zip) | Command-line utility to count the number of bytes in a file and present a histogram of the results. It can optionally present a 256x256 table of the counts of one byte that follows another byte. A command line option allows various filters to be applied before doing the counting.
[util/color.py](util/color.py) | Python module to provide color printing to a console window. Should work on both Windows and Linux.
[util/dedent.py](util/dedent.py) | Python script that will remove the common space characters from a set of text lines from files given on the command line or stdin.
[util/ds.zip](util/ds.zip) | Contains python scripts to help you launch datasheets, manuals, and other documentation files from a command line prompt.  I use this script to lauch manuals and ebooks and it quickly finds the ones I want amongst thousands of files.  For example, to open the PDF manual on my HP 3400 voltmeter, I type the command  'ds 3400'  and I'm presented with three document choices that have the string '3400' in the file name. I choose the number of the file I want to open and it's launched.  If there's only one match, the file is opened in less than a second.  This is much faster than using a file system explorer to find a file.  I also describe how I launch various project I'm working on in my cygwin environment on Windows (a UNIX-like working environment).
[util/ext.py](util/ext.py) | This python script will make a list of the extensions used in file names in the directories given on the command line. It can also recurse into each directory given on the command line.
[util/fdiff.zip](util/fdiff.zip) | Contains python scripts that can identify differences in two directory trees and perform updates as needed to synchronize these two trees.  I wrote these utilities in the late 1990's to help keep my work and home computers synchronized; the challenge was that new files that needed to be kept could be generated on either computer, so blind copying couldn't be used -- the script needs to determine the differences, based on such things as timestamp or file contents.  There are more modern tools such as WinMerge at Sourceforge, kdiff3, meld, etc.  that can do these comparisons, but I still sometimes utilize this python code for checking things with scripts.
[util/fit.py](util/fit.py) | Provides a python function to fit a string of words into a given number of columns. When run as a script, can act as a simple text formatter.  You can control the number of spaces after a sentence and it won't recognize common abbreviations with a trailing period as the end of a sentence.
[util/goto.py](util/goto.py) | Contains a sh-type shell function and a python script that let you navigate around to various directories from a shell command line. I've had a number of UNIX users tell me they couldn't live without this tool once they started using it.
[util/lib.zip](util/lib.zip) | Python script command line tool to provide a facility for keeping snippets of code handy.  If you develop code at a command line, you may want to use this script to keep often-used chunks of code at hand.  A handy feature is that it will highlight the items in color to indicate the language each snippet is implemented in (only works on Windows, but would be easy to hack the color.py module to work on other systems).
[util/lnk.py](util/lnk.py) | Python script to list the files in two directory trees that are hard-linked together. When you see an 'ls -l' listing that shows a file with 2 or more links, this script can help you find where those other links are without delving into the filesystem structure. If you have GNU find, the -samefile option can be used to do this too.
[util/lookup.zip](util/lookup.zip) | Package that contains a python script that can help you look up words in a word dictionary. It can also use the information from WordNet to show synonyms, definitions, and types of words (e.g., adjectives, adverbs, nouns, and verbs).  See the words.pdf file for examples of use and what it can do for you.
[util/mk.py](util/mk.py) | This is a python script that is invoked with a file that contains lines of file pairs and a recipe.  When the first file is newer than the second, the recipe is executed.  I use it, for example, when editing a restructured text and CSS files used to make an HTML file.  When I save the RST or CSS file from my editor, the mk.py script detects that the source file is newer than the HTML file and executes the recipe, which in this case is 'make project.html'.  My browser is set to automatically load changed files, so I can see the changed HTML file immediately.  It's a handy efficiency improvement because you don't have to reach for the mouse, move to another window, run a command, then move back.
[util/mod.py](util/mod.py) | Python script to recursively find files that have changed within a specified time period.  It helps you find that file you know you worked on recently, but can't remember where it was or what its name is.
[util/mp.py](util/mp.py) | This is a macro processor that is a string substitution tool. You can also include arbitrary python code in your text files. Use mp.py -h to read the man page.
[util/pdf.py](util/pdf.py) | This is a python script that can manipulate PDF files. Typical operations are to concatenate a number of PDF files to another PDF file, select certain pages of a PDF file and write them to another PDF file, rotating pages, watermarking. etc. You'll also need to download the pyPdf library to use this script.
[util/pfind.py](util/pfind.py) | Python script to find files and directories. Similar to the UNIX find (but not as powerful), but with a somewhat simpler syntax. It can color-code the output to show where things matched. I use this script a lot.
[util/readability.zip](util/readability.zip) | Will calculate various readability indexes for text files, such as the Gunning Fog Index, the Flesch-Kinkaid Grade Level, etc.
[util/scramble.zip](util/scramble.zip) | Contains a python script to scramble letters in words, leaving the first and last characters alone. I wrote this because an intriguing email that's been circulating the web for years seemed to indicate that only the first and last letters of a word are really important for reading comprehension. You can make up your own mind about the truth of this statement by using the script on a variety of text.
[util/space.py](util/space.py) | See where the space is being consumed in a directory tree and where the biggest files are.
[util/split_cat.zip](util/split_cat.zip) | Python scripts to split a file into chunks, print out SHA1 hashes of each chunk, and allow you to recombine the chunks later back into the original file. Useful for band-limited tools like email and floppy disks.
[util/tlc.py](util/tlc.py) | Python script to rename all files in a directory to lower or upper case.
[util/html_tokens.py](util/html_tokens.py) | Will produce a list of readable words from an HTML file, all in lower case, one per line. You could then run the list of words through a spell checker.
[util/tree.py](util/tree.py) | Python script to print an ASCII representation of a directory tree.  It can optionally decorate the tree with each directory's size in MBytes.
[util/unicode.py](util/unicode.py) | A handy python script to find Unicode characters.  An example is to find the Unicode symbol for a steaming pile of poo.  Run the script with the regular expression 'poo' as an argument. You'll see the symbol you want has a code point of U+1f4a9. Run the script with '1f4a9' on the command line and the PDF containing the symbol will be opened.  You'll need to download the relevant files from the Unicode website (see the comments for the links).
[util/unx.py](util/unx.py) | Produces a list of files that are candidates for turning their execute bit permission off. Handy in cygwin, since most Windows programs don't know how to behave properly with respect to the execute bit.
[util/spc_to_underscore.py](util/spc_to_underscore.py) | Python script to replace all space characters in file names with underscores. Can also do the reverse and act recursively.

Updated Thu Jun 21 13:49:45 2018

Number | Project
--- | ---
13 | Electrical
5 | Engineering
22 | Math
8 | Miscellaneous
20 | Programming
12 | Science
35 | Shop
31 | Utilities
146 | Total
