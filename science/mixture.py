'''
Program to calculate mixtures.
 
Adapted from a C program at http://www.geocities.com/mklotz.geo/
'''
# Copyright (C) 2014 Don Peterson
# Contact:  gmail.com@someonesdad1
 
#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#
 
from __future__ import print_function, division
import sys

py3 = True if sys.version_info[0] > 2 else False
input = input if py3 else raw_input

def InputFloat(prompt, default=""):
    val = 0
    while True:
        s = "[%s] -> " % default
        if s == "[]":
            s = " -> "
        s = input(prompt + " " + s)
        if not s:
            return float(default)
        try:
            val = float(s)
            return val
        except:
            print("Bad input -- try again")

def InputConcentration(prompt, default=""):
    val = 0
    while True:
        val = InputFloat(prompt, default)
        if val < 0 or val > 100:
            print("Concentration should be between 0 and 100%.  Try again.")
        else:
            return val

def PrintResults(VolA, VolB, VolMixture, ConcA, ConcB, ConcMixture):
    pa, pb, pm = ConcA/100, ConcB/100, ConcMixture/100
    if VolA and VolB:
        VolMixture = VolA + VolB
        ConcMixture = 100*(VolA*pa + VolB*pb)/(VolA + VolB)
    elif VolA and ConcMixture:
        VolMixture = VolA*(pa - pb)/(pm - pb)
        VolB = VolMixture - VolA
    elif VolA and VolMixture:
        VolB = VolMixture - VolA
        ConcMixture = 100*(VolA*pa + VolB*pb)/(VolA + VolB)
    elif VolB and ConcMixture:
        VolMixture = VolB*(pb - pa)/(pm - pa)
        VolA = VolMixture - VolB
    elif VolB and VolMixture:
        VolA = VolMixture - VolB
        ConcMixture = 100*(VolA*pa + VolB*pb)/VolMixture
    elif VolMixture and ConcMixture:
        VolA = VolMixture*(pm - pb)/(pa - pb)
        VolB = VolMixture - VolA
    else:
        print("Not enough information")
        exit(1)
    # Print results
    fmt = ".4g"
    print('''
Results:
    Amount of solution A          {VolA:{fmt}}
    Amount of solution B          {VolB:{fmt}}
    Amount of mixture             {VolMixture:{fmt}}
    Concentration of solution A   {ConcA:{fmt}}%
    Concentration of solution B   {ConcB:{fmt}}%
    Concentration of mixture      {ConcMixture:{fmt}}%
'''[:-1].format(**locals()))

def Formulas():
    print('''
Assumptions:
    * The solute in both solutions A and B are the same.
    * One or both solutions can be pure solvent.
    * The solute and solvent are mixed well.
    * There are no volume or temperature changes when the solutions are mixed.
    * Works best for dilute solutions.
    * The concentration fractions are volume fractions.  This means both
      the solvent and solute are liquids (example:  water and antifreeze
      for your car).

Symbols (subscript _a means solution A; subscript _b means solution B):
    C = concentration fraction
    V = volume

The six variables in the problem are thus:
    Solution A:  C_a, V_a
    Solution B:  C_b, V_b
    Mixture:     C, V

Solution A has a solute volume of C_a*V_a.
Solution B has a solute volume of C_b*V_b.

After mixing, the resulting solution has a solute volume faction of

    C = (C_a*V_a + C_b*V_b)/(V_a + V_b)

and the volume is

    V = V_a + V_b

Note that this formulation is an approximation; real solutions sometimes
don't satisfy the above assumptions.  Example:  ethanol and water mixed
together will have a lower volume than their component sum because the
water and ethanol molecules "interlock" somewhat.

You can check the following cases for reasonableness:
    * Mix two unit-volume solutions of 0% concentration to get a 0%
      volume of 2 units.
    * Mix two unit-volume solutions of 100% concentration to get a 100%
      volume of 2 units.
    * Mix one unit volume of p% concentration and one unit volume of 0%
      concentration to get 2 units of (p/2)% concentration.
''')
    exit(0)

if __name__ == "__main__":
    print('''
Calculate the resulting concentration of a solution gotten by mixing two
solutions of differing concentrations.  Include any command line
argument to see the formulas used.
'''[1:])
    if len(sys.argv) > 1:
        Formulas()
    print('''
Specify concentrations of both solutions.  If one solution is a
dilutant (e.g., pure water), enter its concentration as 0%.
'''[1:])
    ConcA = InputConcentration("Concentration of solution A in %?", 0)
    ConcB = InputConcentration("Concentration of solution B in %?", 0)
    print('''
Enter what you know; press return if not known.  You must enter two data
items to obtain a solution.
''')
    data_items_entered = 0
    VolA = VolB = VolMixture = ConcMixture = 0
    while 1:
        VolA = InputFloat("Amount of solution A?", VolA)
        if VolA:
            data_items_entered += 1
        VolB = InputFloat("Amount of solution B?", VolB)
        if VolB:
            data_items_entered += 1
        if data_items_entered != 2:
            VolMixture = InputFloat("Amount of mixture?", VolMixture)
            if VolMixture:
                data_items_entered += 1
            if data_items_entered != 2:
                ConcMixture = InputConcentration(
                    "Concentration of mixture in %?", ConcMixture)
                if ConcMixture:
                    data_items_entered += 1
                if data_items_entered != 2:
                    print("Insufficient data.  Try again.")
                break
            else:
                break
        else:
            break
    PrintResults(VolA, VolB, VolMixture, ConcA, ConcB, ConcMixture)
