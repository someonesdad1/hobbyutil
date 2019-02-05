'''

Print a report on when you'll run out of pills.  This script is handy when
you take a number of pills and their exhaustion dates get out of phase.
Run the script with no datafile to get a sample datafile and a report from
this sample data.  Your pill data must be in the text file
pills_remaining.data (you can change the name in a global variable).  

One line in the datafile must be
    
    Inventory_date = <last inventory date string>

The remaining lines must be as follows:

    Drug name, num_pills_daily, pill_mg, remaining_count

The fields must be separated by the character in the global variable
sep_char (a comma is the default).

Blank lines and lines starting with # are ignored.  
'''
 
# Copyright (C) 2018 Don Peterson
# Contact:  gmail.com@someonesdad1
 
#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#
 
from __future__ import division, print_function
import sys
import os
from fractions import Fraction
from datetime import date, timedelta

datafile = "pills_remaining.data"
sepchar = ","   # Used to separate fields in the datafile

def GetDummyData(file):
    '''The datafile doesn't exist, so print a message to this effect,
    construct an example datafile, and run the report from these data.
    '''
    sep = "-"*60
    print("Missing datafile '{}'".format(file))
    print("The following sample datafile will be used:")
    print(sep)
    data = '''
    # Drug name, num_pills_daily, pill_mg, remaining_count
    Aspirin,            2,           20,         30
    Vitamin B,          1,          100,          5
    Positronium,       1/2,          40,         22
 
    Inventory_date = 4 Feb 2019'''[1:]
    print(data)
    print(sep)
    return data.split("\n")

def ReadDatafile():
    '''Read in the data from the indicated datafile, which must be in the
    same directory as this script.
    '''
    d, inventory_date = {}, ""
    dir = os.path.abspath(os.path.split(sys.argv[0])[0])
    file = os.path.join(dir, datafile)
    try:
        lines = open(file).readlines()
    except Exception:
        lines = GetDummyData(file)
    for i, line in enumerate(lines):
        ln = line.strip()
        if not ln or ln[0] == "#":
            continue
        if ln.startswith("Inventory_date"):
            inventory_date = ln.split("=")[1].strip()
            continue
        try:
            drug_name, num_pills_daily, pill_mg, remaining_count = \
                ln.split(sepchar)
            num_pills_daily = float(eval(num_pills_daily))
            pill_mg = float(pill_mg)
            remaining_count = float(eval(remaining_count))
            d[drug_name] = (num_pills_daily, pill_mg, remaining_count)
        except Exception as e:
            print("Line {} in {} is bad:\n  '{}'".format(
                i + 1, file, ln))
            print("Exception = '{}'".format(e))
            exit(1)
    if not inventory_date:
        print("Datafile '{}' is missing a line of the form:")
        print("  Inventory_date = <last inventory date string>".format(file))
        exit(1)
    maxlen = max([len(i) for i in d.keys()])
    return maxlen, d, inventory_date

def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)

def ds(dt, dayname=False):
    '''Return a date string as 'Day dd MMM yyyy' where MMM is "Jan", etc.
    dt is a date object.
    '''
    months = {1 : "Jan", 2 : "Feb", 3 : "Mar", 4 : "Apr", 5 : "May",
              6 : "Jun", 7 : "Jul", 8 : "Aug", 9 : "Sep", 10 : "Oct",
              11 : "Nov", 12 : "Dec"}
    if dayname:
        return "{} {:2d} {} {}".format(dow(dt), dt.day, months[dt.month],
                                       dt.year)
    else:
        return "{:2d} {} {}".format(dt.day, months[dt.month], dt.year)

def dow(dt):
    '''Return day of week for date object dt as "Mon", "Tue", etc.
    '''
    return "Mon Tue Wed Thu Fri Sat Sun".split()[dt.weekday()]

def P(x):
    '''Formatting aid for pill numbers and dosages in mg.  If the number is
    an integer, return it as an integer string.  Otherwise, round it to 1
    decimal place.
    '''
    s = str(round(float(x), 1))
    if s.endswith(".0"):
        return s[:-2]
    return str(Fraction(s).limit_denominator(10))

def PrintDailyDoses(daily_doses):
    print("Daily doses:       Num_pills    Pill_mg     Dose_mg")
    for drug, val in daily_doses.items():
        num_pills_daily, pill_mg, remaining_count = val
        print("    {:{}s}      {:^6s}    {:^9s}  {:^11s}".format(drug, maxlen, 
                P(num_pills_daily), P(pill_mg), P(pill_mg*num_pills_daily)))
    print()

def PrintDatesOut(daily_doses):
    today = date.today()
    print("Date pills run out:")
    for drug, val in daily_doses.items():
        num_pills_daily, pill_mg, remaining_count = val
        days_left = remaining_count/num_pills_daily
        date_out = today + timedelta(float(days_left))
        print("    {:{}s}      {:s}".format(drug, maxlen, ds(date_out, False)))
    print("\nReport printed", ds(today).strip())

if __name__ == "__main__": 
    maxlen, daily_doses, inventory_date = ReadDatafile()
    print("Inventory date =", inventory_date)
    print()
    PrintDailyDoses(daily_doses)
    PrintDatesOut(daily_doses)
