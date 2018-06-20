[Home](./README.md)

Click on the links to download a project's file(s).

## Utilities

Link | Description
--- | ---
[util/app.cpp](util/app.cpp) | Handy application if you like to work at a cygwin command line. Given one or more files, it will cause them to be opened with their registered application.
[util/asc.py](util/asc.py) | Console python script to print out ASCII character table in decimal, hex, or octal.
[util/bd.c](util/bd.c) | Performs a comparison between binary files; differences are printed in hex dump format. You can print an ASCII picture that represents where the different bytes in the files are in percentage through the file.
[util/bidict.zip](util/bidict.zip) | Creates a dictionary object in python that lets you treat it in both directions as a mapping. If bd is a bidict, you perform normal dictionary access as 'bd[key]', while getting the key that corresponds to a particular value is gotten via 'bd(value)'. I wrote this because an application needed to get both the number of month names (e.g., Feb to 2 and be able to get the month name associated with a month number). It's an example of a discrete bijective function.
[util/color.py](util/color.py) | Python module to provide color printing to a console window. Should work on both Windows and Linux.
[util/dedent.py](util/dedent.py) | Python script that will remove the common space characters from a set of text lines from files given on the command line or stdin.
[util/ds.zip](util/ds.zip) | Contains python scripts to help you launch datasheets, manuals, and other documentation files from a command line prompt.  I use this script to lauch manuals and ebooks and it quickly finds the ones I want amongst thousands of files.  For example, to open the PDF manual on my HP 3400 voltmeter, I type the command  'ds 3400'  and I'm presented with three document choices that have the string '3400' in the file name. I choose the number of the file I want to open and it's launched.  If there's only one match, the file is opened in less than a second.  This is much faster than using a file system explorer to find a file.  I also describe how I launch various project I'm working on in my cygwin environment on Windows (a UNIX-like working environment).
[util/ext.py](util/ext.py) | This python script will make a list of the extensions used in file names in the directories given on the command line. It can also recurse into each directory given on the command line.
[util/fdiff.zip](util/fdiff.zip) | Contains python scripts that can identify differences in two directory trees and perform updates as needed to synchronize these two trees.  I wrote these utilities in the late 1990's to help keep my work and home computers synchronized; the challenge was that new files that needed to be kept could be generated on either computer, so blind copying couldn't be used -- the script needs to determine the differences, based on such things as timestamp or file contents.  There are more modern tools such as WinMerge at Sourceforge, kdiff3, meld, etc.  that can do these comparisons, but I still sometimes utilize this python code for checking things with scripts.
[util/goto.py](util/goto.py) | Contains a sh-type shell function and a python script that let you navigate around to various directories from a shell command line. I've had a number of UNIX users tell me they couldn't live without this tool once they started using it.
[util/loo.zip](util/loo.zip) | Python script that will print out the image files in Open Office documents.  Image files that are not at or below the same directory as the document file will be marked '[not relative]'. Missing files will be marked '[missing]'.  It can also be used as a module in other python programs.  Uses a heuristic rather than any deep knowledge about OO files.  It is particularly useful if you link image files into OO files (which I always do).
[util/lookup.zip](util/lookup.zip) | Package that contains a python script that can help you look up words in a word dictionary. It can also use the information from WordNet to show synonyms, definitions, and types of words (e.g., adjectives, adverbs, nouns, and verbs).  See the words.pdf file for examples of use and what it can do for you.
[util/mod.py](util/mod.py) | Python script to recursively find files that have changed within a specified time period.  It helps you find that file you know you worked on recently, but can't remember where it was or what its name is.
[util/pfind.py](util/pfind.py) | Python script to find files and directories. Similar to the UNIX find (but not as powerful), but with a somewhat simpler syntax. It can color-code the output to show where things matched. I use this script a lot.
[util/space.py](util/space.py) | See where the space is being consumed in a directory tree and where the biggest files are.
[util/tlc.py](util/tlc.py) | Python script to rename all files in a directory to lower or upper case.
[util/tree.py](util/tree.py) | Python script to print an ASCII representation of a directory tree.  It can optionally decorate the tree with each directory's size in MBytes.
[util/unicode.py](util/unicode.py) | A handy python script to find Unicode characters.  An example is to find the Unicode symbol for a steaming pile of poo.  Run the script with the regular expression 'poo' as an argument. You'll see the symbol you want has a code point of U+1f4a9. Run the script with '1f4a9' on the command line and the PDF containing the symbol will be opened.  You'll need to download the relevant files from the Unicode website (see the comments for the links).
[util/spc_to_underscore.py](util/spc_to_underscore.py) | Python script to replace all space characters in file names with underscores. Can also do the reverse and act recursively.

## Science

Link | Description
--- | ---
[science/astro.zip](science/astro.zip) | Collection of a few astronomical utilities, mostly derived from Meeus' books. meeus.py contains a number of Meeus' algorithms. julian.py contains Julian day routines. moon.py calculates the moon's phases. kepler.py solves the Kepler equation.
[science/mixture.py](science/mixture.py) | A python script to aid in mixture calculations. Adapted from a C program at http://www.myvirtualnetwork.com/mklotz/files/mixture.zip.
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
[shop/chain.zip](shop/chain.zip) | Contains a python script and a document to help with chain drilling holes and disks.
[shop/circ3.zip](shop/circ3.zip) | Python script that calculates the radius/diameter of a circle that passes through three points. You can specify either the Cartesian coordinates of the points or the distances between the points. If you download the python uncertainties library, the script will calculate the uncertainty in the radius/diameter given one or more uncertainties for the points or distances.
[shop/cove.zip](shop/cove.zip) | A python script and documentation that show you how to cut a cove with your table saw.  Use this formula and method when it just has to be done correctly on a workpiece you can't mess up on.
[shop/cut.zip](shop/cut.zip) | Contains a python script that will calculate a solution to the one-dimensional cutting problem.  This problem appears when you have a set of raw materials and need to cut a stated set of workpieces from the stock.  The algorithm used is one called first fit decreasing, which means to sort the stock and pieces to be cut by size, then select the largest piece and cut it from the smallest piece of stock.
[shop/Demagnetizer.pdf](shop/Demagnetizer.pdf) | Describes a simple demagnetizing tool you can make from scrap materials.
[shop/density.zip](shop/density.zip) | Python script to calculate densities of various materials. The script performs the following tasks.  Look up the density of a particular material, find materials that have a density close to a given value, express density information in desired units, and show results relative to a given density.
[shop/fits.py](shop/fits.py) | Python script to calculate the required shaft or hole size given a basic dimension of a shaft or hole.
[shop/LayingOutFrustumWithDividers.pdf](shop/LayingOutFrustumWithDividers.pdf) | Shows how to lay out the frustum of a cone with dividers in your shop.
[shop/gblock.zip](shop/gblock.zip) | A C++ program to print out combinations of gauge blocks that yield a desired composite length (the subset sum problem). Should work with most any set of gauge blocks. Uses brute-force searching to find solutions -- it's not elegant, but it works.  A python script is also included that does the same task and it will probably be fast enough for most folks' needs.  The C++ code runs about an order of magnitude faster than the python code.
[shop/holes.zip](shop/holes.zip) | Contains a python script that will help you lay out holes that are equally-spaced around a circle.
[shop/hose.zip](shop/hose.zip) | Here's an effective way to secure a hose to a hose fitting. It's better than anything I've found in a store.
[shop/mass.zip](shop/mass.zip) | Contains a python script that will calculate the volume and mass of a project constructed from various primitive geometrical objects.  This lets you e.g. evaluate the mass and volume of a prospective design and document it through the datafile describing it.
[shop/pipes.pdf](shop/pipes.pdf) | A document showing a derivation of a formula that can be used to make a template for cutting the end of a pipe so that it can be welded to another pipe.
[shop/refcards.zip](shop/refcards.zip) | Contains some reference cards that will print out on 4 by 6 inch cards. I find these handy to keep in my drafting materials box when I'm doing design work at a drafting board.
[shop/thd.zip](shop/thd.zip) | Prints out various dimensions associated with threads. Calculates the values based on the ASME B1.1-1989 standard document. If you machine threads on a lathe, you may find this program handy.

## Electrical

Link | Description
--- | ---
[elec/bode.py](elec/bode.py) | Generate a Bode plot with a python script (needs numpy and matplotlib).  You define the transfer function in a file which is passed on the command line.
[elec/CurrentSource.pdf](elec/CurrentSource.pdf) | Describes how to make a battery-operated 1 ampere current source used to make low resistance measurements.  You can measure to 0.1 milliohm with the typical digital multimeter.
[elec/esr.zip](elec/esr.zip) | Describes a technique of estimating a capacitor's ESR (equivalent series resistance) without having to buy a special meter.
[elec/RMS.pdf](elec/RMS.pdf) | An article for hobbyists about making RMS electrical measurements.
[elec/PortableVoltageStandard.pdf](elec/PortableVoltageStandard.pdf) | Here's a cheap and simple voltage standard you can make with one resistor, an IC that costs about a buck, and three AAA batteries (and it doesn't need a power switch). The last set of batteries of mine lasted for 4.8 years and the standard deviation of the voltage output was 170 uV including room temperature variations and the variance of the voltmeter over that time period.

## Programming

Link | Description
--- | ---
[prog/columnize.py](prog/columnize.py) | Python script to columnize a sequence into columns. Run it as a script to convert stdin to columns or use the Columnize() function in your own scripts. Somewhat similar to the UNIX pr command, but doesn't do pagination.
[prog/fset.py](prog/fset.py) | Treat lines of files as a set. Allows you to look at the union, intersection, difference, etc. between the lines of various files.
[prog/hg.zip](prog/hg.zip) | Some python scripts that make it easier to work with Mercurial repositories.  delta.py shows you the revision numbers where a file changed; hgs.py shows you things like files that are not in the repository, changed files, etc.  fhg.py will find all Mercurial repositories under a given directory and show those needing a check-in.
[prog/license.zip](prog/license.zip) | This is a python script that will allow you to change the license  you use in your source code files.  This is done by replacing a string between two 'trigger' strings.  A number of open source licenses are included in the script (e.g., BSD, GPL2, etc.) and it's easy to include others.  The script will first check that all the indicated source files have the trigger strings and that backup copies of the source files can first be made.
[prog/PythonFromCalc.pdf](prog/PythonFromCalc.pdf) | A document explaining how to call python functions from Open Office Calc spreadsheets.
[prog/python.zip](prog/python.zip) | Contains a document that discusses why learning the python programming language might be a good thing for technical folks.
[prog/seq.zip](prog/seq.zip) | Python script to send various arithmetical progressions to stdout.  Handles integers, floating point, and fractions. Also see fseq.py.
[prog/sig.zip](prog/sig.zip) | Contains a python script to format floating point numbers to a specified number of significant figures or round to a specified template. Works with floats, integers, python Decimals, fractions, mpmath numbers, numpy arrays, complex numbers, and numbers with uncertainty, including any mix of those number types in a container that can be iterated over.
[prog/stack.zip](prog/stack.zip) | A python module that implements a basic stack.  You have the options of making the stack homogeneous (i.e., it will only allow storage of one type of item) or of fixed size.
[prog/util.zip](prog/util.zip) | Contains a number of miscellaneous python functions I've written and collected from the web.
[prog/wordnum.zip](prog/wordnum.zip) | A python script that can convert back and forth between numbers and their word forms.  Handles short and long scales, ordinals, integers, floats (normal and exponential notation), and fractions.  Easy interface through an object's function call; wordnum(36) gives 'thirty six'; wordnum('thirty six') returns the integer 36.  Tested on python 2.7.6 and 3.4.0.
[prog/xref.cpp](prog/xref.cpp) | A C++ console program that will cross reference the tokens in a set of files -- each token will be listed in alphabetical order with the file it occurs in along with the line numbers it's found on.  It can perform spell checking.  It has a -k option which will split composite tokens in the source code and spell check the individual tokens (this helps identify composite tokens that are misspelled).

## Miscellaneous

Link | Description
--- | ---
[misc/Donor.pdf](misc/Donor.pdf) | Organ donation became an important topic for me after my granddaughter was killed.
[misc/Markup.pdf](misc/Markup.pdf) | Derives the equations for markup and profit used in business.
[misc/shaving.pdf](misc/shaving.pdf) | Some thoughts on shaving your beard.

## Math

Link | Description
--- | ---
[math/ef.zip](math/ef.zip) | Graphs of a variety of elementary math functions, useful for a quick picture of how they behave or to grab one or two significant figures of the value.
[math/frange.zip](math/frange.zip) | A python module that provides a floating point analog to range().  Doesn't suffer from the typical floating point problems seen in naive implementations.
[math/root.zip](math/root.zip) | Pure-python root-finding methods such as bisection, Brent's method, Ridder's method, Newton-Raphson, and a general-purpose method by Jack Crenshaw that uses inverse parabolic interpolation.
[math/rpath.zip](math/rpath.zip) | A python module for a rectilinear path object.  You supply it with a set of points and then you can interpolate to points on the path via a parameter.
[math/spiral.zip](math/spiral.zip) | Python scripts that deal with spirals.  spiral.py is an interactive tool to calculate various spiral parameters. archimedean.py is a python module containing a function that calculates the exact length of an Archimedean spiral.
[math/tri.zip](math/tri.zip) | Python script to solve triangles.
[math/TrigDegrees.pdf](math/TrigDegrees.pdf) | Gives some algebraic expressions for a few special values of trigonometric functions in degrees.
[math/triguc.zip](math/triguc.zip) | Contains a vector drawing of the trig functions on the unit circle.  The python script used to generate the graphics is included, so you can tweak it to your tastes.
[math/xyz.zip](math/xyz.zip) | Contains a python script that provides a mini-language to perform analytical geometry calculations in 2 and 3 dimensions.  Use translations, rotations, and dilatations to transform to different coordinate systems.  Geometric objects provided are points, lines, and planes. The script can calculate their intersections, reflections, and projections and find angles and distances between them.

## Engineering

Link | Description
--- | ---
[eng/pqs.zip](eng/pqs.zip) | This package contains python scripts that make it easy to simulate a production process that is inspected by a measurement process with a significant measurement uncertainty.  Such a situation can result in significant producer's and consumer's risk.  It's easy to understand how this Monte Carlo simulation script works and believe its output.
