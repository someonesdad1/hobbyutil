'''
 
This dictionary describes the hobbyutil projects.  The keys are the
project's name and the values describe the project's files and locations.
The code following the dictionary's definition validates the contents.
 
'''
from wrap import dedent
from pathlib import Path as P
from pdb import set_trace as xx 
import sys
from lwtest import Assert
from color import TRM as t
t.always = True
ii = isinstance
plib = "/plib"
pgm = f"{plib}/pgm"
 
HU_Projects = {
    'ag': {
        'subdir': 'math',
        'descr': dedent('''
            Contains formulas relating to analytic geometry and other
            math stuff I need to look up on a regular basis.
            '''),
        'files': [
                'AnalyticGeometry.odt*',
                'AnalyticGeometry.pdf',
                'pictures/trig_quadrants.png*',
                'pictures/trig_functions.png*',
                ],
        'srcdir': '/math/AnalyticGeometry',
        'frozen': True,
        },
    'antif': {
        'subdir': 'eng',
        'descr': dedent('''
            How to calculate how much antifreeze to add to an existing
            partially-filled radiator to get a desired concentration.  Also
            looks at the refractometer.
            '''),
        'files': [
                'antifreeze.odt*',
                'antifreeze.pdf',
                'pictures/freezing_point_depression_ethylene_glycol.png*',
                'pictures/refractometer.jpg*',
                'pictures/misco_side.jpg*',
                'pictures/misco_side_open.jpg*',
                'pictures/misco_bottom.jpg*',
                'pictures/refractometer_display.jpg*',
                'pictures/misco_scales.jpg*',
                'pictures/sulfuric_acid_density.png*',
                'pictures/sulfuric_acid_density_residuals.png*',
                ],
        'srcdir': '/science/antifreeze',
        'frozen': True,
        },
    'app': {
        'subdir': 'util',
        'descr': dedent('''
            Handy application if you like to work at a cygwin command
            line. Given one or more files, it will cause them to be opened
            with their registered application.
            '''),
        'files': [
                'app.cpp',
                ],
        'srcdir': '/projects/tools/0keep',
        'ignore': "Typical OS's have equivalent commands",
        },
    'asc': {
        'subdir': 'util',
        'descr': dedent('''
            Python script to print out an ASCII character table in decimal,
            hex, or octal.  Useful at a command line to see your terminal's
            encoding.
            '''),
        'files': [
                'asc.py',
                ],
        'srcdir': pgm,
        },
    'astro': {
        'subdir': 'science',
        'descr': dedent('''
            Collection of a few astronomical utilities, mostly derived
            from Meeus' books.
            '''),
        'files': [
                'meeus.py',
                'julian.py',
                'kepler.py',
                ['pgm/moon.py', 'moon.py'],
                ],
        'srcdir': plib,
        },
    'ball': {
        'subdir': 'shop',
        'descr': 'Python script to calculate steps to turn a ball on a lathe.',
        'files': [
                'ball.py',
                ],
        'srcdir': pgm,
        },
    'bar': {
        'subdir': 'shop',
        'descr': 'Python script to print out a table of the masses of bar stock.',
        'files': [
                'bar.py',
                ['../sig.py', 'sig.py'],
                ['../columnize.py', 'columnize.py'],
                ],
        'srcdir': pgm,
        'todo': "Remove need for sig",
        },
    'bc': {
        'subdir': 'shop',
        'descr': dedent('''
            Contains a python script that will calculate the Cartesian
            coordinates of holes on a bolt circle.
            '''),
        'files': [
                'bc.py',
                ['../sig.py', 'sig.py'],
                ],
        'srcdir': pgm,
        },
    'bcmt': {
        'subdir': 'math',
        'descr': dedent('''
            A document containing small math tables that will print
            out to be about the size of a business card.
            '''),
        'files': [
                'BusinessCardMathTables.odt*',
                'BusinessCardMathTables.pdf',
                'out/small_log_table.png*',
                'out/small_math_tables.page1.png*',
                'out/small_math_tables.page2.png*',
                ],
        'srcdir': '/math/BusinessCardMathTables',
        },
    'bd': {
        'subdir': 'util',
        'descr': dedent('''
            Performs a comparison between binary files; differences
            are printed in hex dump format.
            '''),
        'files': [
                'bd.c',
                ],
        'srcdir': '/projects/tools/0keep/misc',
        },
    'bgrep': {
        'subdir': 'util',
        'descr': dedent('''
            Python script to search for regular expressions and strings
            in binary files.
            '''),
        'files': [
                'bgrep.py',
                ],
        'srcdir': pgm,
        },
    'bidict': {
        'subdir': 'util',
        'descr': dedent('''
            Creates a dictionary object in python that lets you treat
            it in both directions as a mapping.
            '''),
        'files': [
                'bidict.py',
                ],
        'srcdir': plib,
        },
    'bnc': {
        'subdir': 'elec',
        'descr': dedent('''
            Gives some experimental data about using RF coax cables
            with BNC connectors for DC and low-frequency power.
            '''),
        'files': [
                'BNC_connector_power.odt*',
                'BNC_connector_power.pdf',
                'pictures/CenTech_IR_Thermometer.jpg*',
                'pictures/bnc_cable_measuring_short_resistance.jpg*',
                'pictures/bnc_cable_HP_cable_resistance.jpg*',
                'pictures/bnc_cable.png*',
                'pictures/connector_dimensions.jpg*',
                'pictures/bnc_connector_parts.jpg*',
                'pictures/bnc_outside_resistance.jpg*',
                ],
        'srcdir': '/elec/components',
        'frozen': True,
        },
    'bode': {
        'subdir': 'elec',
        'descr': dedent('''
            Generate a Bode plot with a python script (needs numpy and
            matplotlib).  You define the transfer function in a file
            passed on the command line.
            '''),
        'files': [
                'bode.py',
                ],
        'srcdir': pgm,
        },
    'bucket': {
        'subdir': 'shop',
        'descr': dedent('''
            Shows how to calculate bucket volumes and mark volume calibration
            marks on nearly any bucket.  Includes a python script that will do
            the calculations for you.
            '''),
        'files': [
                'bucket.py',
                'bucket.odt*',
                'bucket.pdf',
                ],
        'srcdir': pgm,
        },
    'calipers': {
        'subdir': 'shop',
        'descr': 'Discussion and use of old-style machinist calipers.',
        'files': [
                'Calipers.odt*',
                'Calipers.pdf',
                'pictures/caliper_types_1.jpg*',
                'pictures/transfer_calipers_substitute.jpg*',
                'pictures/calipers_for_woodworking.jpg*',
                'pictures/stevens_thread_calipers_1.png*',
                'pictures/Homemade_inside_firm_joint.jpg*',
                ['../../projects/pictures/filing_3_flats_1.png*', 'pictures/filing_3_flats_1.png*'],
                ['../../projects/pictures/filing_3_flats_2.png*', 'pictures/filing_3_flats_2.png*'],
                ['../../projects/pictures/filing_3_flats_4.png*', 'pictures/filing_3_flats_4.png*'],
                ['../../projects/pictures/rotary_table_1.jpg*', 'pictures/rotary_table_1.jpg*'],
                ['../../projects/pictures/rotary_table_2.jpg*', 'pictures/rotary_table_2.jpg*'],
                ['../../projects/pictures/hammers_cross_pein.jpg*', 'pictures/hammers_cross_pein.jpg*'],
                ['patents/starrett_fay_1895_lock_joint_US539759.png*', '/patents/starrett_fay_1895_lock_joint_US539759.png*'],
                ],
        'srcdir': '/shop/LengthMeasurement/calipers',
        'frozen': True,
        'todo': 'Need to fix relative pictures',
        },
    'cart': {
        'subdir': 'shop',
        'descr': 'Simple platform for Harbor Freight garden cart.',
        'files': [
                'CartPlatform.odt*',
                'CartPlatform.pdf',
                'pictures/green_cart_platform1.jpg*',
                'pictures/green_cart_platform2.jpg*',
                'pictures/green_cart_platform4.jpg*',
                'pictures/green_cart_platform5.jpg*',
                ],
        'srcdir': '/shop/projects/CartPlatform',
        },
    'chain': {
        'subdir': 'shop',
        'descr': 'Python script to help with chain drilling holes and disks.',
        'files': [
                'chain.odt*',
                'chain.pdf',
                'chain.py',
                ['../get.py', 'get.py'],
                ['../sig.py', 'sig.py'],
                ],
        'srcdir': pgm,
        'ignore': 'Raises an exception',
        'todo': 'Eliminate sig, fix errors',
        },
    'cheat': {
        'subdir': 'shop',
        'descr': dedent('''
            Contains various spreadsheets in Open Office format and
            PDFs of tables that I find handy to have in the shop.
            '''),
        'files': [
                '0readme.odt',
                'common_threads.ods',
                'cutting_info.ods',
                'decimal_equivalents.ods',
                'diameter_to_rpm.ods',
                'fractions.ods',
                'pipe_threads.ods',
                'tap_drills.ods',
                'thread_depths.ods',
                'TorxGauging.ods',
                'TorxSizes.odt',
                'TurningSpeeds.odt',
                'weights_bar_stock1.ods',
                'wrench_sizes.ods',
                'pdf/0readme.pdf',
                'pdf/common_threads.pdf',
                'pdf/cutting_info.pdf',
                'pdf/decimal_equivalents.pdf',
                'pdf/diameter_to_rpm.pdf',
                'pdf/fractions.pdf',
                'pdf/pipe_threads.pdf',
                'pdf/tap_drills.pdf',
                'pdf/thread_depths.pdf',
                'pdf/TorxGauging.pdf',
                'pdf/TorxSizes.pdf',
                'pdf/TurningSpeeds.pdf',
                'pdf/weights_bar_stock1.pdf',
                'pdf/wrench_sizes.pdf',
                ],
        'ignore': 'Pretty specialized',
        'srcdir': '/shop/cheat_sheets',
        },
    'chemname': {
        'subdir': 'science',
        'descr': dedent('''
            A list of archaic chemical names with their modern equivalents
            and chemical formulas.
            '''),
        'files': [
                'chemical_names.ods*',
                'chemical_names.pdf',
                ],
        'srcdir': '/help/science',
        },
    'circ3': {
        'subdir': 'shop',
        'descr': dedent('''
            Python script that calculates the radius/diameter of a circle
            that passes through three points.
            '''),
        'files': [
                'circ3.py',
                'circ3.odt*',
                'circ3.pdf',
                ['../sig.py', 'sig.py'],
                ],
        'srcdir': pgm,
        'todo': "Remove need for sig",
        },
    'clamps': {
        'subdir': 'shop',
        'descr': dedent('''
            Discusses machinist's parallel clamps, why they're useful,
            and how to make your own.
            '''),
        'files': [
                'MachinistClamp.odt*',
                'MachinistClamp.pdf',
                'pictures/toolmaker_clamp3.png*',
                'pictures/machinist_clamp_CS_1910_pg_11.png*',
                'pictures/toolmaker_clamp2.png*',
                'pictures/toolmaker_clamp4a.png*',
                'pictures/toolmaker_clamp4b.png*',
                'pictures/machinist_clamp_3.png*',
                'pictures/Jorgensen_woodworker_clamp.png*',
                'pictures/old_man_3.png*',
                ['pictures/small/finger_clamp1.png*', 'pictures/finger_clamp1.png*'],
                ['pictures/small/finger_clamp2.png*', 'pictures/finger_clamp2.png*'],
                ['pictures/small/finger_clamp3.png*', 'pictures/finger_clamp3.png*'],
                ['pictures/small/machinist_clamp.png*', 'pictures/machinist_clamp.png*'],
                ['pictures/small/machinist_clamp_4.png*', 'pictures/machinist_clamp_4.png*'],
                ['pictures/small/machinist_clamp_5.png*', 'pictures/machinist_clamp_5.png*'],
                ['pictures/small/machinist_clamp_6_aluminum.png*', 'pictures/machinist_clamp_6_aluminum.png*'],
                ['pictures/small/machinist_clamp_7_jaws.png*', 'pictures/machinist_clamp_7_jaws.png*'],
                ['pictures/small/toolmaker_clamp1.png*', 'pictures/toolmaker_clamp1.png*'],
                ],
        'srcdir': '/shop/projects',
        'frozen': True,
        },
    'cnt': {
        'subdir': 'util',
        'descr': dedent('''
            cnt.py is a command line utility to count the number of bytes in
            the file arguments and present a histogram of the results.  Processes
            files on the order of 10 MB/s.
            '''),
        'files': [
                'cnt.py',
                #['/tools/misc/cnt_new.c', 'cnt.c'],
                ['../fpformat.py', 'fpformat.py'],
                ['../columnize.py', 'columnize.py'],
                ],
        'srcdir': pgm,
        'todo': "Remove need for fpformat; put C file back in",
        },
    'color': {
        'subdir': 'util',
        'descr': dedent('''
            Python module to provide color printing to a console window.
            Should work on both Windows and Linux.  Includes functions to show
            regular expression matches in text printed to the console; these
            functions are helpful when you are developing complicated regular
            expressions.
            '''),
        'files': [
                'color.py',
                ],
        'srcdir': plib,
        },
    'columnize': {
        'subdir': 'prog',
        'descr': dedent('''
            Python function to print a sequence in columns.  The order can be
            down (default) or across.
            '''),
        'files': [
                'columnize.py',
                ],
        'srcdir': plib,
        },
    'comb': {
        'subdir': 'prog',
        'descr': dedent('''
            A python script that will produce permutations and combinations
            of the lines in a file. Can be useful for generating test cases.
            '''),
        'files': [
                'comb.py',
                ],
        'srcdir': pgm,
        },
    'concise': {
        'subdir': 'math',
        'descr': dedent('''
            Discusses the Concise 300, a circular slide rule still in
            production in Japan.
            '''),
        'files': [
                'Concise300.odt*',
                'Concise300.pdf',
                'Concise/Concise_300.jpg*',
                ],
        'srcdir': '/math/SlideRules',
        },
    'cove': {
        'subdir': 'shop',
        'descr': dedent('''
            Python script shows you how to cut a cove with your table saw.
            Use this formula and method when it just has to be done correctly
            on a workpiece you can't mess up on.
            '''),
        'files': [
                'cove.odt*',
                'cove.pdf',
                'cove.py',
                ],
        'srcdir': pgm,
        },
    'cpi': {
        'subdir': 'misc',
        'descr': dedent('''
            Calculate the effects of inflation on prices for the years 1914
            to the present using the consumer price index.  For example, $1
            to purchase food in 1960 is equivalent to about $8.5 in 2018.
            '''),
        'files': [
                'cpi.py',
                ],
        'srcdir': pgm,
        },
    'cs': {
        'subdir': 'elec',
        'descr': dedent('''
            How to make a battery-operated 1 ampere current source used to
            make low resistance measurements.
            '''),
        'files': [
                ['CurrentSource_pub.odt*', 'CurrentSource.odt*'],
                'CurrentSource.pdf',
                'pictures/current_source_1.png*',
                'pictures/current_source_schematic.png*',
                ],
        'srcdir': '/elec/projects',
        'todo': 'Pictures not correct per loo',
        },
    'cut': {
        'subdir': 'shop',
        'descr': dedent('''
            Python script that will calculate a solution to the one-dimensional
            cutting problem.  This problem appears when you have a set of raw
            materials and need to cut a stated set of workpieces from the
            stock.
            '''),
        'files': [
                'cut.odt*',
                'cut.pdf',
                'cut.py',
                ['../sig.py', 'sig.py'],
                ],
        'srcdir': pgm,
        'todo': "Remove need for sig, fix color",
        },
    'dbm': {
        'subdir': 'elec',
        'descr': dedent('''
            Table of dBm to voltage conversions for 50, 600, and 75
            ohm impedances.
            '''),
        'files': [
                'dbm.odt*',
                'dbm.ods*',
                'dbm.pdf',
                ],
        'ignore': 'Limited interest',
        'srcdir': '/elec/spreadsheets',
        },
    'demag': {
        'subdir': 'shop',
        'descr': 'A simple demagnetizing tool made from scrap materials.',
        'files': [
                'Demagnetizer.odt*',
                'Demagnetizer.pdf',
                'pictures/demagnetizer_gap.jpg*',
                'pictures/demagnetizer1.jpg*',
                'pictures/demagnetizer2.jpg*',
                'pictures/demagnetizer4.jpg*',
                'pictures/demagnetizer3.jpg*',
                'pictures/demagnetizer5.jpg*',
                'pictures/magnet_on_screwdriver_trick.png*',
                ],
        'srcdir': '/elec/projects',
        },
    'density': {
        'subdir': 'shop',
        'descr': 'Python script to display densities of various materials.',
        'files': [
                'density.odt*',
                'density.pdf',
                'density.py',
                ['../sig.py', 'sig.py'],
                ],
        'srcdir': pgm,
        },
    'dep': {
        'subdir': 'util',
        'descr': dedent('''
            Script to display a python program's module dependencies.
            The modules are classified by type (standard library modules and
            user modules).  It won't find .pyc/.pyo files nor modules the
            imports depend on.  It uses regular expressions to find import
            lines in the script, so it may show lines that aren't true imports
            (e.g., an import line inside a conditional that's always false).
            '''),
        'files': [
                'dep.py',
                ],
        'srcdir': pgm,
        },
    'diam': {
        'subdir': 'science',
        'descr': dedent('''
            Plots of circles showing the relative mean diameters of
            planets and moons in the solar system.
            '''),
        'files': [
                'diameters.pdf'
                ],
        'srcdir': '/science/astronomy/diameters',
        },
    'dino': {
        'subdir': 'math',
        'descr': dedent('''
            This document discusses doing calculations without using an
            electronic calculator.  It's useful for a technical person to know
            how to reason quantitatively when a calculator isn't handy.
            '''),
        'files': [
                'DinosaurArithmeticSmall.odt*',
                'DinosaurArithmeticSmall.pdf',
                'pictures/trig_approx.png*',
                ],
        'srcdir': '/math/Dinosaur_Arithmetic',
        'frozen': True,
        },
    'ditchpump': {
        'subdir': 'shop',
        'descr': 'Comments and tips on using a ditch pump to water your lawn.',
        'files': [
                'DitchPump_pub.odt*',
                'DitchPump_pub.pdf',
                'pictures/internal_pipe_wrench.jpg*',
                'pictures/pump_house.png*',
                'pictures/cimg1743.jpg*',
                ['pictures/small/2_inch_suction_17Jun2013_1.png*', 'pictures/2_inch_suction_17Jun2013_1.png*'],
                ['pictures/small/2_inch_suction_17Jun2013_2.png*', 'pictures/2_inch_suction_17Jun2013_2.png*'],
                ['pictures/small/float_switch_1.png*', 'pictures/float_switch_1.png*'],
                ['pictures/small/pipe_shield_2.png*', 'pictures/pipe_shield_2.png*'],
                'pictures/small/pump_house.png*',
                ['pictures/small/pump_rear_5Aug2012.png*', 'pictures/pump_rear_5Aug2012.png*'],
                ],
        'srcdir': '/doc/home/sprinklers',
        'frozen': True,
        },
    'diurnal': {
        'subdir': 'science',
        'descr': dedent('''
            Shows a plot of the light from the sky measured with a cheap
            photodiode.  This is a simple experiment that would be fun do to
            with a child.
            '''),
        'files': [
                'diurnal_variations.odt*',
                'diurnal_variations.pdf',
                'pictures/photodiode.png*',
                'pictures/experimental_setup.jpg*',
                'pictures/held_in_vise.jpg*',
                'pictures/2.8_days_of_data.png*',
                'pictures/soffit_mounting.jpg*',
                'pictures/21Jul2011_all_points.jpg*',
                'pictures/21Jul2011_evening4.jpg*',
                'pictures/21Jul2011_evening5.jpg*',
                'pictures/mounting_with_tube2.jpg*',
                'pictures/28Jul2011_effects.jpg*',
                'pictures/mounting_geometry.jpg*',
                'pictures/collimated_detector_view.jpg*',
                ],
        'srcdir': '/science/diurnal_optics',
        'frozen': True,
        },
    'dmath': {
        'subdir': 'math',
        'descr': dedent('''
            Contains a python module dmath.py that is a drop-in replacement
            (nearly) for the python math module when calculating with python's
            Decimal numbers.  Using this library, you can calculate elementary
            functions to any desired accuracy.
            '''),
        'files': [
                'dmath.py',
                'dmath_test.py',
                ['readme', '0readme'],
                ],
        'srcdir': '/math/dmath',
        },
    'donor': {
        'subdir': 'misc',
        'descr': "Why I have organ donor checked on my driver's license.",
        'files': [
                'Donor.odt*',
                'Donor.pdf',
                'pictures/organ_donation_2.png*',
                ],
        'srcdir': '/doc',
        },
    'drtri': {
        'subdir': 'shop',
        'descr': dedent('''
            This is a simple modification to a 30-60-90 drafting triangle
            that lets you draw 45 degree angles.
            '''),
        'files': [
                ['drafting_triangle_tip.odt*', 'DraftingTriangleTip.odt*'],
                ['drafting_triangle_tip.pdf', 'DraftingTriangleTip.pdf'],
                'pictures/drafting_triangle_tip.png*',
                ],
        'srcdir': '/shop/projects',
        },
    'drules': {
        'subdir': 'shop',
        'descr': dedent('''
            PDFs containing some drafting rules that I've always wanted.
            You can print them at full scale and glue them to a chunk of
            wood to make some handy scales.
            '''),
        'files': [
                'drules.pdf',
                ],
        'srcdir': '/shop/drafting_rules',
        },
    'ds': {
        'subdir': 'util',
        'descr': dedent('''
            Contains python scripts to help you launch datasheets, manuals,
            and other documentation files from a command line prompt.  I
            use this script to launch manuals and ebooks and it quickly
            finds the ones I want amongst thousands of files.
            '''),
        'files': [
                'ds.py',
                'ds.odt*',
                'ds.pdf',
                'abspath.py',
                'goto.py',
                ['../color.py', 'color.py'],
                ],
        'srcdir': pgm,
        },
    'dupfile': {
        'subdir': 'util',
        'descr': 'Python script to find duplicated files in a directory tree.',
        'files': [
                'dup.py',
                ],
        'srcdir': pgm,
        },
    'ef': {
        'subdir': 'math',
        'descr': dedent('''
            Graphs of a variety of elementary math functions, useful
            for a quick picture of how they behave or to grab one or two
            significant figures of the value.
            '''),
        'files': [
                'ElementaryFunctions.odt*',
                'ElementaryFunctions.pdf',
                'images/elem.png*',
                'images/trig_deg.png*',
                'images/trig_rad.png*',
                'images/invtrig_deg.png*',
                'images/invtrig_rad.png*',
                'images/versed_deg.png*',
                'images/versed_rad.png*',
                'images/hyp1.png*',
                'images/hyp2.png*',
                'images/invhyp1.png*',
                'images/invhyp2.png*',
                'images/gud.png*',
                'images/gamma1.png*',
                'images/gamma2.png*',
                'images/normal_cdf.png*',
                'images/bessel.png*',
                'images/elliptic1_deg.png*',
                'images/elliptic1_rad.png*',
                'images/elliptic2_deg.png*',
                'images/elliptic2_rad.png*',
                ],
        'srcdir': '/math/elementary_functions',
        },
    'elements': {
        'subdir': 'science',
        'descr': dedent('''
            Contains elements.pdf, a document that contains a periodic
            table of the elements, a plot of the vapor pressures of the
            elements, values of physical parameters sorted by value, and
            various physical parameters of the elements plotted as a function
            of atomic number.
            '''),
        'files': [
                '0readme*',
                'elements.ods*',
                'elements.pdf',
                'elements.py*',
                'elements_doc.odt*',
                'elements_doc.pdf',
                'periodic_table.py*',
                'plot_page.py*',
                'property_plots.py*',
                'raw.py*',
                'sorted_properties.py*',
                'vapor_pressure.py*',
                'pictures/elastic_constants.jpg*',
                ['/plib/fpformat.py*', 'fpformat.py*'],
                ],
        'srcdir': '/science/elements',
        'frozen': True,
        'todo': "Remove need for fpformat",
        },
    'esr': {
        'subdir': 'elec',
        'descr': dedent('''
            Describes a technique of estimating a capacitor's ESR (equivalent
            series resistance) without having to buy a special meter.
            '''),
        'files': [
                'MeasuringESR.odt*',
                'MeasuringESR.pdf',
                'pictures/fluke83_freq_response.png*',
                'pictures/ESR_estimate_pulse.png*',
                ],
        'srcdir': '/elec/Articles',
        },
    'ext': {
        'subdir': 'util',
        'descr': dedent('''
            Python script to make a list of the extensions used
            in file names and their counts in the directories given on the
            command line.
            '''),
        'files': [
                'ext.py',
                ],
        'srcdir': pgm,
        },
    'fdiff': {
        'subdir': 'util',
        'descr': dedent('''
            Contains python scripts that can identify differences in
            two directory trees and perform updates as needed to synchronize
            these two trees.
            '''),
        'files': [
                'ddiff.py',
                'ddiffcp.py',
                'ddiff.readme',
                ],
        'srcdir': '/pylib/other',
        'ignore': "pp/ddiff.py exists and should be fixed and used if it's OK",
        },
    'fits': {
        'subdir': 'shop',
        'descr': dedent('''
            Python script to calculate the required shaft or hole size
            given a basic dimension of a shaft or hole.
            '''),
        'files': [
                'fits.py',
                ],
        'srcdir': pgm,
        },
    'flow': {
        'subdir': 'eng',
        'descr': 'Nomograph for pipe flow.',
        'files': [
                'flow.pdf',
                ],
        'srcdir': '/science/nomographs',
        },
    'fpen': {
        'subdir': 'misc',
        'descr': dedent('''
            Discusses the care and feeding of fountain pens as writing
            tools.
            '''),
        'files': [
                'fountain_pen_primer.odt*',
                'fountain_pen_primer.pdf',
                'pictures/fountain_pen_point.jpg*',
                'pictures/pen_writing.jpg*',
                'pictures/parker_slimline_pen.jpg*',
                'pictures/hero616_disassembled.jpg*',
                'pictures/converter.jpg*',
                'pictures/shading.jpg*',
                'pictures/artist_nibs_speedball.jpg*',
                'pictures/artist_nibs_speedball_doodling.jpg*',
                'pictures/vanishing_point.jpg*',
                'pictures/pilot_varsity_disassembled.jpg*',
                'pictures/pencil_vs_ink.jpg*',
                'pictures/black_ink_water_test_26Nov2011.jpg*',
                'pictures/waterproofness_test.jpg*',
                'pictures/skrip_ink_bottle.jpg*',
                'pictures/mont_blanc_shoe_bottle1.jpg*',
                'pictures/small_ink_bottle.jpg*',
                'pictures/small_ink_bottle1.jpg*',
                'pictures/small_ink_bottle_holder.jpg*',
                'mixing_inks.jpg*',
                'color_wheel1.jpg*',
                'color_wheel2.jpg*',
                'pictures/toothpick_pen_flash.jpg*',
                'pictures/feathering.jpg*',
                'pictures/toothpick_pen_north_light.jpg*',
                'pictures/international_cartridge.jpg*',
                'pictures/international_cartridge_seal.jpg*',
                'ink_costs_us.png*',
                'pictures/paper_testing.jpg*',
                'pictures/japanese_pen_holder.png*',
                'pictures/pen_case.jpg*',
                'pictures/pen_wrap_Elizabeth_Boling.jpg*',
                'pictures/pen_holder.jpg*',
                'pictures/storage.jpg*',
                'pictures/belt_holder.jpg*',
                'pictures/blotter.jpg*',
                'pictures/bench_block.jpg*',
                'pictures/pen_disassembly_1.jpg*',
                'pictures/pen_disassembly_2.jpg*',
                'pictures/pen_disassembly_3.jpg*',
                'pictures/pen_disassembly_4.jpg*',
                'pictures/pen_dewaterer.jpg*',
                'pictures/ink_syringe_kit.jpg*',
                'pictures/parker_slimfold_shading.jpg*',
                'pictures/micromike.jpg*',
                'pictures/ohaus_balance.jpg*',
                'pictures/ink_density_with_no_flash.jpg*',
                ],
        'srcdir': '/doc/pens',
        'frozen': True,
        'todo': "Doesn't match loo list of pictures",
        },
    'frange': {
        'subdir': 'math',
        'descr': dedent('''
            A python module that provides a floating point analog to
            range().  Doesn't suffer from the typical floating point problems
            seen in naive implementations.
            '''),
        'files': [
                ['../frange.py', 'frange.py'],
                ['../test/frange_test.py', 'frange_test.py'],
                ],
        'srcdir': pgm,
        },
    'frustum': {
        'subdir': 'shop',
        'descr': dedent('''
            Shows how to lay out the frustum of a cone with dividers
            in your shop.
            '''),
        'files': [
                'LayingOutFrustumWithDividers.odt*',
                'LayingOutFrustumWithDividers.pdf',
                'pictures/layout_an_arc_with_dividers.png*',
                ],
        'srcdir': '/shop/IntroToMetalShop/techniques',
        },
    'fseq': {
        'subdir': 'math',
        'descr': dedent('''
            Contains a python script fseq.py that provides general-purpose
            sequence generation (arithmetic, geometric, logarithmically-spaced,
            etc.).  The script also provides useful random number generation
            facilities for doing Monte Carlo calculations at the command
            line, along with CDFs and PDFs of some distributions.  Requires
            numpy.
            '''),
        'files': [
                'fseq.py',
                'fseq.odt*',
                'fseq.pdf',
                ['../cmddecode.py', 'cmddecode.py'],
                'pictures/sampling_wor.png*',
                ],
        'srcdir': pgm,
        'ignore': "Needs numpy, see if could remove numpy dep",
        },
    'fset': {
        'subdir': 'prog',
        'descr': dedent('''
            Treat lines of files as a set. Allows you to look at the
            union, intersection, difference, etc. between the lines of
            various files.
            '''),
        'files': [
                'fset.py',
                ],
        'srcdir': pgm,
        },
    'fuse': {
        'subdir': 'elec',
        'descr': "Notes on using ATO automobile fuses as poor-man's shunts.",
        'files': [
                'fuse_as_shunt.odt*',
                'fuse_as_shunt.pdf',
                ],
        'srcdir': '/elec/projects/fuse_as_shunt',
        },
    'gblock': {
        'subdir': 'shop',
        'descr': dedent('''
            A C++ program to print out combinations of gauge blocks
            that yield a desired composite length (the subset sum problem).
            Uses brute-force searching to find solutions.  Includes a python
            script that solves the same problem.
            '''),
        'files': [
                'gauge.cpp',
                ['/plib/pgm/gb.py', 'gb.py'],
                ],
        'srcdir': '/shop/software/gauge_blocks',
        },
    'glendag': {
        'subdir': 'shop',
        'descr': dedent('''
            Describes a simple concrete sprinkler guard that my wife
            designed and built.
            '''),
        'files': [
                'GlendaGuard.odt*',
                'GlendaGuard.pdf',
                'pictures/glenda_guard_2.jpg*',
                'pictures/glenda_guard_1.jpg*',
                ],
        'srcdir': '/shop/projects/GlendaGuard',
        },
    'goto': {
        'subdir': 'util',
        'descr': dedent('''
            Uses a python script and shell functions to launch project files
            and navigate to various directories from a command line.  A number
            of UNIX users have told me they couldn't live without this tool once
            they started using it.
            '''),
        'files': [
                'goto.py',
                'goto.odt*',
                'goto.pdf',
                ],
        'srcdir': pgm,
        },
    'gpaper': {
        'subdir': 'math',
        'descr': dedent('''
            Provides some common graph papers in PDF files that print
            on ANSI A paper.
            '''),
        'files': [
                'graph_paper.py',
                '5mm_A.pdf',
                'dots_2tenths_A.pdf',
                'drafting_A.pdf',
                'engineering_A.pdf',
                'letter_ruled_A.pdf',
                'quarter_inch_A.pdf',
                ],
        'srcdir': '/doc/graph_paper',
        },
    'hammer': {
        'subdir': 'shop',
        'descr': 'Discusses the common hammer types and making a new handle for one.',
        'files': [
                'hammer.odt*',
                'hammer.pdf',
                'pictures/hammers_cross_pein.jpg*',
                'pictures/cut_masonry_nail.jpg*',
                'pictures/punch_holder.png*',
                'pictures/hammers.jpg*',
                'pictures/hammer_handle_prototype_1.jpg*',
                'pictures/hammer_handle_prototype_2.jpg*',
                ],
        'srcdir': '/shop/projects',
        'frozen': True,
        },
    'help': {
        'subdir': 'prog',
        'descr': dedent('''
            If you use the vim editor, you have a convenient tool for
            accessing textual information. This package contains the tools
            I use to build a help system I've used for the past couple
            of decades (I started building this textual information in
            the 1980's).
            '''),
        'files': [
                ],
        'ignore': 'Should be updated to newhelp stuff',
        'srcdir': '/newhelp/help',
        },
    'holes': {
        'subdir': 'shop',
        'descr': dedent('''
            Contains a python script that will help you lay out holes
            that are equally-spaced around a circle.
            '''),
        'files': [
                'holes.py',
                'holes.drills',
                'holes.odt*',
                'holes.pdf',
                'pictures/drill_layout.png*',
                ['../sig.py', 'sig.py'],
                ],
        'srcdir': pgm,
        'ignore': 'Get working',
        },
    'hose': {
        'subdir': 'shop',
        'descr': dedent('''
            Here's an effective way to secure a hose to a hose fitting.
            It's better than anything I've found in a store.
            '''),
        'files': [
                'HoseFitting.odt*',
                'HoseFitting.pdf',
                'pictures/constrictor_knot_on_hose_fitting.png*',
                ],
        'srcdir': '/shop/projects',
        },
    'hppn': {
        'subdir': 'elec',
        'descr': dedent('''
            This is a compilation of various 8-digit HP part numbers
            translated into conventional industry part numbers.  This list may
            be of use to those with old HP instruments that need to find a
            replacement part.
            '''),
        'files': [
                '0readme',
                'hp.py',
                'hp_parts',
                ],
        'srcdir': '/elec/hp',
        },
    'hsm': {
        'subdir': 'shop',
        'descr': dedent('''
            This python script searches metalworking titles for regular
            expressions.  Contains the indexes from Village Press and Joe
            Landau's index from 2000.
            '''),
        'files': [  
                'hsm.zip',
                ],
        'srcdir': pgm,
        },
    'iapws': {
        'subdir': 'eng',
        'descr': dedent('''
            Contains C++ and python code that implements the IAPWS95
            equations for the thermodynamic properties of water.
            '''),
        'files': [
                'iapws95.cpp',
                'iapws95.h',
                'iapws95.py',
                'test.py',
                ],
        'srcdir': '/science/john_pye/py',
        },
    'imp': {
        'subdir': 'elec',
        'descr': dedent('''
            This python script will take a complex impedance in polar
            coordinates and print out the series and parallel models' values,
            reactance, dissipation factor, and quality factor.
            '''),
        'files': [
                'impedance.py',
                ],
        'srcdir': pgm,
        },
    'ind': {
        'subdir': 'elec',
        'descr': dedent('''
            Provides an Open Office spreadsheet that can calculate the
            inductance of common electrical structures.  Includes a PDF
            document describing the use and which gives references for
            the formulas used.
            '''),
        'files': [
                'inductance.ods',
                'inductance.odt*',
                'inductance.pdf',
                'inductance_spreadsheet.pdf',
                'pictures/screenshot.jpg*',
                ],
        'srcdir': '/elec/software/coil_inductance',
        'frozen': True,
        },
    'lib': {
        'subdir': 'util',
        'descr': dedent('''
            Python script command line tool to provide a facility for
            keeping snippets of code handy.
            '''),
        'files': [
                'lib.py',
                ['lib.dat.sample', 'lib.dat'],
                ],
        'srcdir': pgm,
        },
    'license': {
        'subdir': 'prog',
        'descr': dedent('''
            This is a python script that will allow you to change the
            license you use in your source code files.
            '''),
        'files': [
                'license.py',
                'color.py',
                ],
        'srcdir': plib,
        },
    'lnk': {
        'subdir': 'util',
        'descr': dedent('''
            Python script to list the files in two directory trees that are
            hard-linked together.  If you have GNU find, the -samefile option
            can be used to do this too.
            '''),
        'files': [
                'lnk.py',
                ],
        'srcdir': pgm,
        },
    'logicprobe': {
        'subdir': 'elec',
        'descr': 'Discusses the use of a logic probe.',
        'files': [
                'logic_probe.pdf',
                'logic_probe.odt*',
                ],
        'srcdir': '/elec/projects/logic_probe',
        },
    'loo': {
        'subdir': 'util',
        'descr': dedent('''
            Python script that will print out the image files in Open
            Office documents.  Image files that are not at or below the same
            directory as the document file will be marked '[not relative]'.
            Missing files will be marked '[missing]'.  It is useful if you link
            image files into OO files.
            '''),
        'files': [
                'loo.py',
                'color.py',
                ],
        'srcdir': plib,
        },
#    'lookup': {
#        'subdir': 'util',
#        'descr': dedent('''
#            Package that contains a python script that can help you
#            look up words in a word dictionary and use the information
#            from WordNet to show synonyms, definitions, and types of words
#            (e.g., adjectives, adverbs, nouns, and verbs).
#            '''),
#        'files': [
#                'lookup.py',
#                'mkwords.py',
#                'simple.py',
#                'wrap.py',
#                ['/pylib/pgm/words.odt*', 'words.odt*'],
#                'words.pdf',
#                'makefile',
#                ['/pylib/pgm/pictures/lookup_results.png*', 'pictures/lookup_results.png*'],
#                ['../../../color.py', 'color.py'],
#                ],
#        'srcdir': '/pylib/types_of_words/WordNet/lookup',
#        },
    'lvise': {
        'subdir': 'shop',
        'descr': dedent('''
            Describes a small vise made from 1 inch square bar stock.  It slips
            into a pocket and is handy for small tasks around the shop and home.
            '''),
        'files': [
                'LittleVise.odt*',
                'LittleVise.pdf',
                'pictures/LittleVise_1.png*',
                'pictures/LittleVise_2.png*',
                'pictures/starrett/starrett_160_clamp.png*',
                ],
        'srcdir': '/shop/projects',
        },
    'lwtest': {
        'subdir': 'prog',
        'descr': dedent('''
            Lightweight python script testing framework based on some work by
            Raymond Hettinger.  Python's unittest module is unfriendly to the
            test/debug process because it intercepts the standard streams, which
            doesn't let you use the python debugger to examine your code.
            '''),
        'files': [
                'lwtest.odt*',
                'lwtest.pdf',
                ['test/lwtest_test.py', 'lwtest_test.py'],
                ],
        'srcdir': plib,
        },
    'manufy': {
        'subdir': 'prog',
        'descr': dedent('''
            Python script to convert text lines to have double quotes and
            a newline at the end. This is useful to allow you to quickly write
            text manpages for C or C++ code.
            '''),
        'files': [
                'manufy.py',
                ],
        'srcdir': pgm,
        'todo': 'Has a bug when used to process its manpage output',
        },
    'markup': {
        'subdir': 'misc',
        'descr': 'Derives the equations for markup and profit used in business.',
        'files': [
                'Markup.odt*',
                'Markup.pdf',
                'pictures/markup.png*',
                'pictures/multiplier.png*',
                ],
        'srcdir': '/doc',
        },
    'mass': {
        'subdir': 'shop',
        'descr': dedent('''
            Python script to calculate the volume and mass of a project
            constructed from various primitive geometrical objects.
            '''),
        'files': [
                'mass.bolt',
                'mass.bucket',
                'mass.earth',
                'mass.fishtank',
                'mass.frame',
                'mass.house',
                'mass.odt*',
                'mass.pdf',
                'mass.py',
                'mass.simple',
                'mass.test',
                ['../asme.py', 'asme.py'],
                ['../cmddecode.py', 'cmddecode.py'],
                ['../columnize.py', 'columnize.py'],
                ['../get.py', 'get.py'],
                ['../sig.py', 'sig.py'],
                ['../u.py', 'u.py'],
                ],
        'srcdir': pgm,
        'ignore': "Need to get working with get.py, rm sig",
        },
    'mixture': {
        'subdir': 'science',
        'descr': dedent('''
            A python script to aid in mixture calculations. Adapted
            from a C program at http://www.myvirtualnetwork.com/mklotz/files/mixture.zip.
            '''),
        'files': [
                'mixture.py',
                ],
        'srcdir': pgm,
        },
    'mk': {
        'subdir': 'util',
        'descr': dedent('''
            Python script that is invoked with a file that
            contains lines of file pairs and a recipe.  When the first
            file is newer than the second, the recipe is executed.
            '''),
        'files': [
                'mk.py',
                ],
        'srcdir': pgm,
        },
    'mkfile': {
        'subdir': 'util',
        'descr': dedent('''
            Python script to make files of a given size.  The -u and -t
            options construct allegedly cryptographically-secure random
            bytes.  On my older computer, it takes a few seconds to
            construct a 1 GB file of random bytes.
            '''),
        'files': [
                'mkfile.py',
                ],
        'srcdir': pgm,
        },
    'mod': {
        'subdir': 'util',
        'descr': dedent('''
            Python script to recursively find files that have changed
            within a specified time period.
            '''),
        'files': [
                'mod.py',
                ],
        'srcdir': pgm,
        },
    'mortgage': {
        'subdir': 'misc',
        'descr': dedent('''
            Gives a table that lets you estimate your mortgage's monthly
            payment.  Doesn't include taxes or insurance.
            '''),
        'files': [
                'Mortgage.odt*',
                'Mortgage.pdf',
                ],
        'srcdir': '/math/mortgage',
        },
    'mp': {
        'subdir': 'util',
        'descr': dedent('''
            This is a macro processor that is a string substitution
            tool. You can also include arbitrary python code in your text
            files. Use mp.py -h to read the man page.
            '''),
        'files': [
                'mp.py',
                ],
        'srcdir': pgm,
        },
    'novas': {
        'subdir': 'science',
        'descr': dedent('''
            Translation into python of some C code from the US Naval
            Observatory (http://aa.usno.navy.mil/software/novas/novas_c/novasc_info.html).
            '''),
        'files': [
                'novas.py',
                ],
        'srcdir': plib,
        },
    'nozzle': {
        'subdir': 'shop',
        'descr': 'Nice hose nozzle you can make if you have a lathe.',
        'files': [
                'nozzle.odt*',
                'nozzle.pdf',
                'nozzle.jpg*',
                'nozzle2.jpg*',
                ],
        'srcdir': '/shop/projects/hose_nozzle',
        },
    'oct': {
        'subdir': 'elec',
        'descr': dedent('''
            Build an Octopus, a handy electrical troubleshooting tool (you need
            an oscilloscope).
            '''),
        'files': [
                'Octopus_new.odt*',
                ['Octopus_new.pdf', 'octopus.pdf'],
                'pictures/octopus_non_sine.png*',
                ['pictures/small/BNC_connectors.png*', 'pictures/BNC_connectors.png*'],
                ['pictures/small/octopus_100_nF.png*', 'pictures/octopus_100_nF.png*'],
                ['pictures/small/octopus_3.3V_zener_diode.png*', 'pictures/octopus_3.3V_zener_diode.png*'],
                ['pictures/small/octopus_3H_inductor.png*', 'pictures/octopus_3H_inductor.png*'],
                ['pictures/small/octopus_520_mH.png*', 'pictures/octopus_520_mH.png*'],
                ['pictures/small/octopus_E3615A_swept.png*', 'pictures/octopus_E3615A_swept.png*'],
                ['pictures/small/octopus_E_B_2N2222.png*', 'pictures/octopus_E_B_2N2222.png*'],
                ['pictures/small/octopus_E_B_2N2222_10volts.png*', 'pictures/octopus_E_B_2N2222_10volts.png*'],
                ['pictures/small/octopus_E_C_2N2222_10_volts.png*', 'pictures/octopus_E_C_2N2222_10_volts.png*'],
                ['pictures/small/octopus_blue_LED.png*', 'pictures/octopus_blue_LED.png*'],
                ['pictures/small/octopus_diode_cap_parallel.png*', 'pictures/octopus_diode_cap_parallel.png*'],
                ['pictures/small/octopus_diode_resistor.png*', 'pictures/octopus_diode_resistor.png*'],
                ['pictures/small/octopus_inductor_diode_composite.png*', 'pictures/octopus_inductor_diode_composite.png*'],
                ['pictures/small/octopus_res_cap_parallel.png*', 'pictures/octopus_res_cap_parallel.png*'],
                ['pictures/small/octopus_res_diode_components.png*', 'pictures/octopus_res_diode_components.png*'],
                ['pictures/small/octopus_res_diode_composite.png*', 'pictures/octopus_res_diode_composite.png*'],
                ],
        'srcdir': '/elec/projects/octopus',
        'frozen': True,
        },
#    'odict': {
#        'subdir': 'prog',
#        'descr': dedent('''
#            A bare-bones ordered dictionary for python. You won't need
#            this if you are on python 2.7 or later because there's a built-in
#            ordered  dictionary.
#            '''),
#        'files': [
#                'odict.py',
#                ['test/odict_test.py', 'odict_test.py'],
#                ],
#        'srcdir': plib,
#        },
    'oo_math': {
        'subdir': 'math',
        'descr': dedent('''
            Introduces the equation-writing capabilities of Open Office
            2.0.  Includes a cheatsheet that you can modify.
            '''),
        'files': [
                'OO_math.odt*',
                'OO_math.pdf',
                'math_cheatsheet.odt*',
                'math_cheatsheet.pdf',
                ],
        'srcdir': '/doc',
        },
    'oopy': {
        'subdir': 'prog',
        'descr': 'How to call python functions from Open Office Calc spreadsheets.',
        'files': [
                'PythonFromCalc.odt*',
                'PythonFromCalc.pdf',
                ],
        'srcdir': '/doc',
        },
    'oring': {
        'subdir': 'shop',
        'descr': 'Utility to find/show o-ring sizes on-hand.',
        'files': [
                'oring.py',
                ['../get.py', 'get.py'],
                ['../f.py', 'f.py'],
                ],
        'srcdir': pgm,
        },
#    'out': {
#        'subdir': 'prog',
#        'descr': dedent('''
#            Contains a python module that provides a utility object
#            for printing string representations of objects to a stream.  I've
#            used something like this for years and it's a good tool to
#            replace the print command/function, which causes a bit of friction
#            between python 2 and 3 code.  This module has been tested with
#            both python 2 and 3.
#            '''),
#        'files': [
#                'out.odt*',
#                'out.pdf',
#                'out.py',
#                ['test/out_test.py', 'out_test.py'],
#                ],
#        'srcdir': plib,
#        },
    'paper': {
        'subdir': 'misc',
        'descr': dedent('''
            Contains a python script to calculate various things about
            paper to compare paper purchases.
            '''),
        'files': [
                'paper.py',
                ],
        'srcdir': pgm,
        },
    'papersz': {
        'subdir': 'misc',
        'descr': 'Shows a scale drawing of various ISO and US paper sizes.',
        'files': [
                'paper_sizes.py*',
                'paper_sizes.pdf',
                ],
        'srcdir': pgm,
        },
    'parts': {
        'subdir': 'elec',
        'descr': dedent('''
            Describes one way of storing lots of little electronic parts
            and how to find them quickly.
            '''),
        'files': [
                'PartsStorageMethods.odt*',
                'PartsStorageMethods.pdf',
                ],
        'srcdir': '/elec/projects',
        },
#    'pcmplx': {
#        'subdir': 'math',
#        'descr': dedent('''
#            Parse complex numbers when they are written in the ways humans
#            like to write them.  The floating point type can be specified, which
#            allows you to keep the full precision of the problem.
#            '''),
#        'files': [
#                'parse_complex.py',
#                ],
#        'srcdir': plib,
#        },
#    'pdf': {
#        'subdir': 'util',
#        'descr': dedent('''
#            This is a python script that can manipulate PDF files. It can
#            concatenate a number of PDF files, select certain pages and write
#            them to another PDF file, rotating pages, watermarking. etc. You'll
#            also need to download the pyPdf library to use this script.
#            '''),
#        'files': [
#                ['pdf_.py', 'pdf.py']
#                ],
#        'srcdir': plib,
#        },
    'pfind': {
        'subdir': 'util',
        'descr': dedent('''
            Python script to find files and directories. Similar to
            the UNIX find (but not as powerful), but with a simpler syntax.
            '''),
        'files': [
                'pfind.py',
                ],
        'srcdir': pgm,
        },
#    'pills': {
#        'subdir': 'misc',
#        'descr': "Calculate the dates you'll run out of prescription pills.",
#        'files': [
#                'pills.py',
#                ],
#        'srcdir': pgm,
#        },
    'pipes': {
        'subdir': 'shop',
        'descr': dedent('''
            Derivation of a formula that can be used to make a template for cutting
            the end of a pipe so that it can be welded to another pipe.
            '''),
        'files': [
                'pipes.odt*',
                'pipes.pdf',
                ],
        'srcdir': '/math/AnalyticGeometry',
        },
    'posts': {
        'subdir': 'shop',
        'descr': dedent('''
            Using a class 2 lever can be a surprisingly effective way
            to pull fence posts out of the ground.
            '''),
        'files': [
                'PullingFencePosts.odt*',
                'PullingFencePosts.pdf',
                'pictures/fence_post_driver.png*',
                'pictures/hi_lift_jack_and_plate.png*',
                'pictures/chain_with_hooks.png*',
                'pictures/chain_grab.png*',
                ],
        'srcdir': '/shop/projects/PullingFencePosts',
        },
    'pqs': {
        'subdir': 'eng',
        'descr': dedent('''
            Python scripts to simulate a production process that is inspected
            by a measurement process with a significant measurement uncertainty.
            '''),
        'files': [
                'ProcessSimulator.odt*',
                'ProcessSimulator.pdf',
                'manufacture.py',
                'process.py',
                'pqs.py',
                'pictures/actual_bad.png',
                'pictures/apparent_bad.png',
                'pictures/bad_meas_as_bad.png',
                'pictures/good_meas_as_bad.png',
                'pictures/actual_good.png',
                'pictures/apparent_good.png',
                'pictures/bad_meas_as_good.png',
                'pictures/good_meas_as_good.png',
                ['/plib/sig.py', 'sig.py'],
                ],
        'srcdir': '/math/ProcessAnalyzer',
        'todo': "Remove need for sig",
        },
    'primes': {
        'subdir': 'math',
        'descr': dedent('''
            Some python scripts that deal with primes, factoring, and
            integer properties.
            '''),
        'files': [
                'primes.py',
                ['pgm/int.py', 'int.py'],
                ['/projects/tools/_math/primes_fast.cpp', 'primes_fast.cpp'],
                ],
        'srcdir': plib,
        'ignore': "Find C++ file",
        },
    'python': {
        'subdir': 'prog',
        'descr': dedent('''
            Discusses why learning the python programming language might be a
            good thing for technical folks.
            '''),
        'files': [
                ['/doc/Python.odt*', 'Python.odt*'],
                ['/doc/Python.pdf', 'Python.pdf'],
                ['/pylib/other/ellipse_circumference.py', 'ellipse_circumference.py'],
                ['pgm/resistor.py', 'resistor.py'],
                'frange.py',
                ],
        'srcdir': plib,
        },
    'qmd': {
        'subdir': 'math',
        'descr': dedent('''
            Discussion of how to do multiplications and divisions
            by hand when you only need a specified number of significant
            figures in the answer.
            '''),
        'files': [
                'QuickMultDiv.odt*',
                'QuickMultDiv.pdf',
                ],
        'srcdir': '/math/Dinosaur_Arithmetic',
        },
    'rand': {
        'subdir': 'math',
        'descr': dedent('''
            A pure python script for generating random numbers from various
            distributions to stdout.
            '''),
        'files': [
                'rand.py',
                ['../sig.py', 'sig.py'],
                ['../columnize.py', 'columnize.py'],
                ],
        'srcdir': pgm,
        },
    'random_phrase': {
        'subdir': 'util',
        'descr': dedent('''
            A python script for generating random phrases of words.  Useful
            for generating pass phrases.
            '''),
        'files': [
                'random_phrase.py',
                ],
        'srcdir': pgm,
        },
    'react': {
        'subdir': 'elec',
        'descr': dedent('''
            Contains two reactance charts in PDF form along with a short
            file describing their use.
            '''),
        'files': [
                'reactance_notes.pdf',
                ['out/reactance.pdf', 'reactance.pdf'],
                ['out/big_reactance.pdf', 'big_reactance.pdf'],
                ['../ohms_law_chart/OhmsLaw1.pdf', 'OhmsLaw1.pdf'],
                ['../ohms_law_chart/OhmsLaw2.pdf', 'OhmsLaw2.pdf'],
                ],
        'srcdir': '/elec/software/reactance_chart',
        },
    'readability': {
        'subdir': 'util',
        'descr': dedent('''
            Will calculate various readability indexes for text files,
            such as the Gunning Fog Index, the Flesch-Kinkaid Grade Level,
            etc.
            '''),
        'files': [
                'readability.py',
                'readability.readme',
                'words_syllables.py',
                ],
        'srcdir': pgm,
        'frozen': True,
        },
    'refcards': {
        'subdir': 'shop',
        'descr': dedent('''
            Contains some reference cards that will print out on 4 by
            6 inch cards. I find these handy to keep in my drafting materials
            box when I'm doing design work at a drafting board.
            '''),
        'files': [
                ['pdf/cards.pdf', 'reference_cards.pdf'],
                'decimal_equiv.ods',
                'densities_liquids.ods',
                'densities_metal.ods',
                'densities_miscellaneous.ods',
                'densities_plastics_woods.ods',
                'double_depths.ods',
                'drills1.ods',
                'grains_to_g.ods',
                'metric_taps_dies.ods',
                'metric_threads.ods',
                'mm_to_inch1.ods',
                'mm_to_inch2.ods',
                'mm_to_inch3.ods',
                'pipe_sizes.ods',
                'pipe_threads.ods',
                'pvc_pipe.ods',
                'screw_heads.ods',
                'screw_heads_metric.ods',
                'screw_threads.ods',
                'screws_wood_Torx.ods',
                'self_threading_screws.ods',
                'shcs.ods',
                'slope_to_angle_deg.ods',
                'slope_to_angle_rad.ods',
                'spring_pins.ods',
                'surface_speeds_SFPM.ods',
                'tap_drills.ods',
                'weight_bar_stock_kg.ods',
                'weight_bar_stock_lb.ods',
                'wrench_sizes.ods',
                'pictures/self_tapping_screws1.jpg*',
                'pictures/self_tapping_screws2.jpg*',
                ],
        'srcdir': '/shop/ReferenceCards',
        'frozen': True,
        },
    'res': {
        'subdir': 'elec',
        'descr': 'Contains two tools that help you deal with resistors.',
        'files': [
                'makefile',
                'resistor.cpp',
                'resistor.odt*',
                'resistor.pdf',
                'resistor.test',
                ],
        'srcdir': '/elec/software/resistors',
        },
    'rms': {
        'subdir': 'elec',
        'descr': 'An article for hobbyists about making RMS electrical measurements.',
        'files': [
                'RMS.pdf',
                ],
        'srcdir': '/elec/Articles/RMS',
        },
    'root': {
        'subdir': 'math',
        'descr': dedent('''
            Pure-python root-finding methods such as bisection, Brent's
            method, Ridder's method, Newton-Raphson, and a general-purpose
            method by Jack Crenshaw that uses inverse parabolic interpolation.
            '''),
        'files': [
                'root.py',
                ['test/root_test.py', 'root_test.py'],
                ],
        'srcdir': plib,
        },
#    'rpath': {
#        'subdir': 'math',
#        'descr': dedent('''
#            A python module for modeling rectilinear path object in
#            n-dimensional spaces.  You supply it with a set of points and
#            then you can interpolate to points on the path via a parameter.
#            You can do things like calculate line integrals and complex path
#            integrals.
#            '''),
#        'files': [
#                'path.py',
#                'path.odt*',
#                'path.pdf',
#                ['test/path_test.py', 'path_test.py'],
#                ],
#        'srcdir': plib,
#        },
    'ruler': {
        'subdir': 'util',
        'descr': dedent('''
            For console windows; prints a variety of rulers to stdout.
            It's easy to modify to get different ruler types.
            '''),
        'files': [
                'ruler.py',
                ],
        'srcdir': plib,
        },
    'sawbuck': {
        'subdir': 'shop',
        'descr': dedent('''
            A simple and easy to make sawbuck that's made from eight identical
            pieces of 2x4.
            '''),
        'files': [
                'SawBuck.odt*',
                'SawBuck.pdf',
                'pictures/sawbuck_oblique_open.jpg*',
                'pictures/sawbuck_side_folded.jpg*',
                ],
        'srcdir': '/shop/projects',
        },
    'scale': {
        'subdir': 'math',
        'descr': dedent('''
            The scale.pdf file contains two sheets of paper with slide rule
            type scales on them. You may find it useful for simple technical
            calculations.
            '''),
        'files': [
                'scale.pdf',
                'OnePageCalculator.odt*',
                'OnePageCalculator.pdf',
                'pictures/sfpm.png*',
                ],
        'srcdir': '/math/one_page_calculator',
        },
    'scramble': {
        'subdir': 'util',
        'descr': dedent('''
            Contains a python script to scramble letters in words, leaving
            the first and last characters alone.
            '''),
        'files': [
                'scramble.py',
                'scramble.html',
                ],
        'srcdir': pgm,
        },
    'seg': {
        'subdir': 'math',
        'descr': dedent('''
            Python script to calculate parameters of a circular segment.
            Translated from a program written by Marv Klotz.
            '''),
        'files': [
                'seg.py'
                ],
        'srcdir': pgm,
        'ignore': 'Need to vet first',
        },
    'seq': {
        'subdir': 'math',
        'descr': dedent('''
            Python script to send various arithmetical progressions
            to stdout.  Handles integers, floating point, and fractions.
            '''),
        'files': [
                ['pgm/seq.py', 'seq.py'],
                'frange.py',
                ],
        'srcdir': plib,
        },
    'shave': {
        'subdir': 'misc',
        'descr': 'Some thoughts on shaving your beard.',
        'files': [
                'shaving.odt*',
                'shaving.pdf',
                ],
        'srcdir': '/doc',
        },
    'shoulder': {
        'subdir': 'misc',
        'descr': dedent('''
            A document describing my experiences with shoulder surgeries
            to help others understand some of the things one goes through.
            A shoulder injury is one of the more inconvenient injuries
            because it gets in the way of so many of life's activities.
            '''),
        'files': [
                'shoulder_surgery.html',
                ],
        'srcdir': '/doc/medical/shoulderJun2018',
        },
    'shorttbl': {
        'subdir': 'math',
        'descr': dedent('''
            A set of tables of elementary math functions intended to
            print on half of an ANSI-A sized piece of paper.
            '''),
        'files': [
                'ShortTables.ods*',
                'ShortTables.odt*',
                'ShortTables.pdf',
                'ShortTables_doc.pdf',
                ],
        'srcdir': '/math/tables',
        },
    'shuffle': {
        'subdir': 'prog',
        'descr': dedent('''
            C program to randomly shuffle the bytes of a file.  It
            reads all the bytes of a file into memory, so it cannot be used
            on arbitrarily large files.
            '''),
        'files': [
                'shuffle.c',
                ],
        'srcdir': '/tools/shuffle',
        },
    'sig': {
        'subdir': 'prog',
        'descr': dedent('''
            A python module to format floating point numbers
            to a specified number of significant figures or round to a
            specified template.
            '''),
        'files': [
                'sig.py',
               #'sig.odt*',
               #'sig.pdf',
               #['test/sig_test.py', 'sig_test.py'],
                ],
        'srcdir': plib,
        'ignore': "It's time to retire this",
        },
    'sinesticks': {
        'subdir': 'shop',
        'descr': dedent('''
            How to build a simple device from scrap that will measure
            angles in the shop.
            '''),
        'files': [
                'sine_sticks.odt*',
                'sine_sticks.pdf',
                ],
        'srcdir': '/shop/projects',
        },
    'solar': {
        'subdir': 'science',
        'descr': dedent('''
            Python script that prints out the dimensions of a scaled solar
            system.  You can use it to make a scale solar system in your yard
            or on your street.
            '''),
        'files': [
                'SolarSystemScaleModel.odt*',
                'SolarSystemScaleModel.pdf',
                'pictures/zoom_from_neptune.jpg*',
                'pictures/zoom_from_saturn.jpg*',
                ],
        'srcdir': '/science/astronomy/diameters',
        },
    'space': {
        'subdir': 'util',
        'descr': dedent('''
            See where the space is being consumed in a directory tree and where the
            biggest files are.
            '''),
        'files': [
                'space.py',
                ],
        'srcdir': pgm,
        },
    'sphshell': {
        'subdir': 'science',
        'descr': dedent('''
            Discusses gravitation and electrostatics inside a uniform
            spherical shell and why there is no force on a particle. Also
            looks at Henry Cavendish's elegant experiment in the 1700's showing
            that the exponent in Coulomb's Law is 2.
            '''),
        'files': [
                'SphericalShell.odt*',
                'SphericalShell.pdf',
                ],
        'srcdir': '/science',
        },
    'spiral': {
        'subdir': 'math',
        'descr': 'Python script that deals with Archimedean spirals.',
        'files': [
                'spiral.py',
                ],
        'srcdir': pgm,
        },
    'split_cat': {
        'subdir': 'util',
        'descr': dedent('''
            Python scripts to split a file into chunks, print out SHA1
            hashes of each chunk, and allow you to recombine the chunks
            later back into the original file.
            '''),
        'files': [
                'split.py',
                'cat.py',
                ],
        'srcdir': pgm,
        },
    'square': {
        'subdir': 'shop',
        'descr': dedent('''
            How to use a carpenter's square to lay out angles from 1
            degree to 44 degrees.
            '''),
        'files': [
                ['angles_and_carpenters_square.odt*', 'square.odt*'],
                ['pdf/angles_and_carpenters_square.pdf', 'square.pdf'],
                ],
        'srcdir': '/shop/cheat_sheets',
        },
    'stack': {
        'subdir': 'prog',
        'descr': dedent('''
            A python module that implements a thread-safe and
            process-safe basic stack.  Works on python 2.7 and 3
            (copy() only works on python 3.5 or later).
            '''),
        'files': [
                'stack.py',
                ['test/stack_test.py', 'stack_test.py'],
                ],
        'srcdir': plib,
        },
#    'sumbytes': {
#        'subdir': 'prog',
#        'descr': dedent('''
#            A short C++ program that will read all the bytes from the
#            files given on the command line and compute various statistics
#            from them.
#            '''),
#        'files': [
#                'sumbytes.cpp',
#                ],
#        'srcdir': '/tools',
#        },
    'sz': {
        'subdir': 'util',
        'descr': dedent('''
            Python script to print out sizes of subdirectories.  The output
            is to one significant figure and is color-coded for quickly seeing
            where most of the storage space is being taken.
            '''),
        'files': [
                'sz.py',
                ['../color.py', 'color.py'],
                ],
        'srcdir': pgm,
        },
    'thd': {
        'subdir': 'shop',
        'descr': dedent('''
            Prints out various dimensions associated with threads per ASME
            B1.1-1989.  If you machine threads on a lathe, you may find this
            program handy.
            '''),
        'files': [
                'thd.py',
                ['../asme.py', 'asme.py'],
                ],
        'srcdir': pgm,
        },
#    'tips1': {
#        'subdir': 'misc',
#        'descr': 'DIY/shop tips.',
#        'files': [
#                'tips1.pdf',
#                'tips1.odt*',
#                ],
#        'srcdir': '/doc',
#        'frozen': True,
#        },
#    'tips2': {
#        'subdir': 'misc',
#        'descr': 'DIY/shop tips.',
#        'files': [
#                'tips2.pdf',
#                'tips2.odt*',
#                ],
#        'srcdir': '/doc',
#        'frozen': True,
#        },
#    'tips3': {
#        'subdir': 'misc',
#        'descr': 'DIY/shop tips.',
#        'files': [
#                'tips3.pdf',
#                'tips3.odt*',
#                ],
#        'srcdir': '/doc',
#        'frozen': True,
#        },
    'tlc': {
        'subdir': 'util',
        'descr': dedent('''
            Python script to rename all files in a directory to lower
            or upper case.
            '''),
        'files': [
                'tlc.py',
                ],
        'srcdir': pgm,
        },
    'tokens': {
        'subdir': 'util',
        'descr': dedent('''
            Will produce a list of readable words from an HTML file,
            all in lower case, one per line. You could then run the list
            of words through a spell checker.
            '''),
        'files': [
                'html_tokens.py',
                ],
        'srcdir': pgm,
        },
    'tree': {
        'subdir': 'util',
        'descr': dedent('''
            Python script to print an ASCII representation of a directory
            tree.  It can optionally decorate the tree with each directory's
            size in MBytes and highlight a regular expression in color.
            '''),
        'files': [
                'tree.py',
                ],
        'srcdir': pgm,
        },
#    'tri': {
#        'subdir': 'math',
#        'descr': 'Python script to solve triangles.',
#        'files': [
#                'tri.py',
#                'tri.odt*',
#                'tri.pdf',
#                ['../sig.py', 'sig.py'],
#                ],
#        'srcdir': pgm,
#        },
    'trigd': {
        'subdir': 'math',
        'descr': dedent('''
            Gives some algebraic expressions for a few special values
            of trigonometric functions in degrees.
            '''),
        'files': [
                'TrigDegrees.odt*',
                'TrigDegrees.pdf',
                ],
        'srcdir': '/math/herman',
        },
    'triguc': {
        'subdir': 'math',
        'descr': dedent('''
            Contains a vector drawing of the trig functions on the unit
            circle.  The python script used to generate the graphics is
            included, so you can tweak it to your tastes.
            '''),
        'files': [
                'trig_functions.py',
                ['images/trig_functions.pdf', 'trig_functions.pdf'],
                'TrigUnitCircle.odt*',
                'TrigUnitCircle.pdf',
                'images/trig_functions.jpg*',
                ],
        'srcdir': '/math/elementary_functions',
        },
    'ts': {
        'subdir': 'prog',
        'descr': dedent('''
            The ts.py script provides facilities for text substitution
            in text files.  It has only 3 basic commands (define a substitution,
            turn  the output on/off, and include a file) and the ability
            to include blocks of python code in the text file.  Though
            it's relatively simple to use, it can provide a fair bit
            of power.
            '''),
        'files': [
                'ts.py',
                'ts.ts',
                'ts.html',
                'manpage',
                'ts_test.py',
                'color_example.ts',
                'makefile',
                'ts.css',
                ],
        'srcdir': '/pylib/pgm/ts',
        },
    'u': {
        'subdir': 'science',
        'descr': dedent('''
            A lightweight python library module that provides conversion
            factors for various physical units.  An experienced scientist or
            engineer will be using it in a few minutes after seeing an example.
            '''),
        'files': [
                'u.odt*',
                'u.pdf',
                'u.py',
                ],
        'srcdir': plib,
        },
#    'uni': {
#        'subdir': 'util',
#        'descr': dedent('''
#            Python script to find Unicode characters.  You'll need to download
#            the relevant files from the Unicode website.  This script was
#            written in 2014 and I based it on the information from The
#            Unicode 7 standard; version 12 is current in 2019 and it's on my
#            todo list to upgrade this script.  Yet I still use this script
#            every day when working on my computer.
#            '''),
#        'files': [
#                'unicode.py',
#                ],
#        'srcdir': pgm,
#        },
    'units': {
        'subdir': 'science',
        'descr': dedent('''
            A short blurb on the capabilities of the useful GNU units
            program.
            '''),
        'files': [
                'GNU_units.odt*',
                'GNU_units.pdf',
                ],
        'srcdir': '/doc',
        },
#    'unx': {
#        'subdir': 'util',
#        'descr': dedent('''
#            Produces a list of files that are candidates for turning
#            their execute bit permission off.  This is useful on Windows machines
#            running cygwin to avoid a "sea of green" in an ls listing with
#            colorizing on.
#            '''),
#        'files': [
#                'unx.py',
#                ],
#        'srcdir': pgm,
#        },
#    'url': {
#        'subdir': 'util',
#        'descr': dedent('''
#            Python script that will interpret a URL from a Google search
#            page.
#            '''),
#        'files': [
#                'url.py',
#                ],
#        'srcdir': pgm,
#        },
    'us': {
        'subdir': 'util',
        'descr': dedent('''
            Python script to replace all space characters in file names
            with underscores.
            '''),
        'files': [
                'spc_to_underscore.py',
                ],
        'srcdir': pgm,
        },
    'util': {
        'subdir': 'prog',
        'descr': dedent('''
            Contains a number of miscellaneous python functions I've
            written and collected from the web.
            '''),
        'files': [
                'util.py',
                ],
        'srcdir': plib,
        },
    'vs': {
        'subdir': 'elec',
        'descr': dedent('''
            Simple voltage standard you can make with one resistor, an IC
            that costs about a buck, and three AA batteries.
            '''),
        'files': [
                'PortableVoltageStandard.odt*',
                'PortableVoltageStandard.pdf',
                'pictures/voltage_reference.png*',
                ],
        'srcdir': '/elec/Articles',
        },
#    'wave': {
#        'subdir': 'elec',
#        'descr': dedent('''
#            Provides a python script (uses numpy and scipy) that lets
#            you construct various waveforms used in engineering and science
#            tasks.
#            '''),
#        'files': [
#                'waveform.py',
#                'waveform.odt*',
#                'waveform.pdf',
#                'pictures/waveform_sine.png*',
#                'pictures/waveform_gated.png*',
#                'pictures/waveform_clipping.png*',
#                'pictures/waveform_scr.png*',
#                'pictures/waveform_trapezoid.png*',
#                'pictures/waveform_staircase.png*',
#                'pictures/waveform_modulation.png*',
#                'pictures/waveform_mw.png*',
#                ],
#        'srcdir': pgm,
#        },
    'weigh': {
        'subdir': 'shop',
        'descr': dedent('''
            Demonstrates how I weighed our trailer with a lever. With
            a 12 foot long 4x4, I was able to measure 2500 pounds.
            '''),
        'files': [
                ['weighing_a_trailer.odt*', 'weigh.odt*'],
                ['weighing_a_trailer.pdf', 'weigh.pdf'],
                'weighing1.jpg*',
                'weighing4.jpg*',
                ],
        'srcdir': '/doc/trailer/weighing_trailer',
        },
#    'wordnum': {
#        'subdir': 'prog',
#        'descr': dedent('''
#            A python script that can convert back and forth between
#            numbers and their word forms.  Handles short and long scales,
#            ordinals, integers, floats (normal and exponential notation),
#            and fractions.  Easy interface through an object's function
#            call; wordnum(36) gives 'thirty six'; wordnum('thirty six')
#            returns the integer 36.  Tested on python 2.7.6 and 3.4.0.
#            '''),
#        'files': [
#                'wordnum.py',
#                ['test/wordnum_test.py', 'wordnum_test.py'],
#                ],
#        'srcdir': plib,
#        },
#    'wrap': {
#        'subdir': 'prog',
#        'descr': 'Two python scripts to wrap and unwrap text files.',
#        'files': [
#                'wrap.py',
#                'unwrap.py',
#                ],
#        'srcdir': pgm,
#        },
    'xmastom': {
        'subdir': 'misc',
        'descr': dedent('''
            Using Christmas tree lights to keep tomato plants from freezing
            at night.
            '''),
        'files': [
                'XmasTomatoes.odt*',
                'XmasTomatoes.pdf',
                ],
        'srcdir': '/doc',
        },
#    'xor': {
#        'subdir': 'prog',
#        'descr': dedent('''
#            C++ program to XOR a data file and key file together to
#            encrypt a file.
#            '''),
#        'files': [
#                'xor.cpp',
#                'xor.odt*',
#                'xor.pdf',
#                'otp.py',
#                'mkfile.py',
#                'md5.c',
#                'md5.h',
#                ],
#        'srcdir': '/tools/xor',
#        },
    'xref': {
        'subdir': 'prog',
        'descr': dedent('''
            A program that will cross reference the tokens in a set of
            files -- each token will be listed in alphabetical order with
            the file it occurs in along with the line numbers it's found on.
            A C++ program and a python script (you'll need version 3.7, but
            you can hack on it a bit to get it to run with earlier python 3
            versions) are included that do the same things.
            '''),
        'files': [
                'xref.cpp',
                ['/pylib/pgm/xref.py', 'xref.py'],
                ['/pylib/pgm/xref.readme', 'xref.readme'],
                ],
        'srcdir': '/tools/xref',
        },
#    'xyz': {
#        'subdir': 'math',
#        'descr': dedent('''
#            Python script that provides a mini-language to perform analytical
#            geometry calculations in 2 and 3 dimensions.
#            '''),
#        'files': [
#                'xyz.py',
#                ['../geom_prim.py', 'geom_prim.py'],
#                ['../test/geom_prim_test.py', 'geom_prim_test.py'],
#                ['../sig.py', 'sig.py'],
#                'xyz.odt*',
#                'xyz.pdf',
#                'xyz.area',
#                'xyz.iss',
#                'xyz.shop',
#                'xyz.sphere',
#                'xyz.splice',
#                ],
#        'srcdir': pgm,
#        },
    'yankee': {
        'subdir': 'shop',
        'descr': dedent('''
            Discusses the Yankee screwdriver, a useful tool that has
            been in production for more than 100 years.
            '''),
        'files': [
                'YankeePushDrill.odt*',
                'YankeePushDrill.pdf',
                'pictures/yankee_screwdriver_1.png*',
                'pictures/yankee_screwdriver_2.png*',
                'pictures/yankee_screwdriver_3.png*',
                'pictures/yankee_screwdriver_4.png*',
                'pictures/yankee_screwdriver_5.png*',
                'pictures/yankee_screwdriver_6.png*',
                'pictures/yankee_screwdriver_7.png*',
                'pictures/yankee_screwdriver_8.png*',
                'pictures/yankee_screwdriver_9.png*',
                'pictures/yankee_screwdriver_dims.png*',
                ],
        'srcdir': '/shop/projects'
    },
}

t.wrn = t("brnl")
t.err = t("wht")
def Warn(msg):
    if show_warnings:
        t.print(f"{t.wrn}Warning:  {msg}")
def Error(msg):
    t.print(f"{t.err}Error:  {msg}")
def CheckFiles(di, pr):
    '''pr is the string naming the project.
       di is HU_Projects dictionary for this project.
 
    Each files entry is either a string or a list of two strings.  The
    strings may contain a trailing '*' character, indicating that this file
    shouldn't be part of the project's output.  Rather, it means the file
    is needed to define all of the project's files.
    '''
    def TrimAsterisk(s):
        Assert(s)
        return s[:-1] if s[-1] == "*" else s
    files = di["files"]
    if not ii(files, (list, tuple)):
        Error(f"files is not a sequence for {project}")
    for item in files:
        srcdir = P(di["srcdir"])
        # Make sure the source file exists
        if ii(item, str):
            # This must be an existing file
            p = srcdir/P(TrimAsterisk(item))
        else:
            # It must be a sequence of two strings.  The first is the
            # actual source file and the second is the name it will have in
            # the resulting project's zip file.
            if len(item) != 2 or not all(ii(i, str) for i in item):
                Error(f"{item!r} is an improper sequence")
            first, second = item
            p = srcdir/P(TrimAsterisk(first))
        ignore = bool(di.get("ignore", ""))
        if not p.exists() or not p.is_file():
            if ignore:
                Warn(f"{item!r} can't be found for project {pr}")
            else:
                Error(f"{item!r} can't be found for project {pr}")
                CheckFiles.error = True
def Validate(warn=False):
    global show_warnings
    show_warnings = bool(warn)
    # Validate the dictionary's contents
    CheckFiles.error = False
    for project in HU_Projects:
        di = HU_Projects[project]
        pr = f"{project!r}"
        # Verify mandatory keys are present
        for k in "subdir descr files srcdir".split():
            if k not in di:
                Error(f"Key {k!r} not in dict for project {pr}")
        # If optional keys are present, verify their type
        if "todo" in di and not ii(di["todo"], str):
            Error(f"'todo' in project {pr} must be a string")
        if "ignore" in di and not ii(di["ignore"], str):
            Error(f"'ignore' in project {pr} must be a string")
        if "files" not in di:
            Error("'files' not in {pr}")
        CheckFiles(di, pr)
    if CheckFiles.error:
        raise ValueError("projects.py:  Validate() failed")
if __name__ == "__main__": 
    show_warnings = False
    Validate()
