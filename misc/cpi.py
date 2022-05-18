'''
Consumer price index utility.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2017 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Program description string
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import getopt
    import os
    import sys
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    from f import flt
    from columnize import Columnize
if 1:   # Global variables
    # The following CPI data came from the cpi_data.py script.
    CPI = { # Integers need to be divided by 1000 to get CPI
        2021: 265144, 2020: 258810, 2019: 255657, 2018: 251107, 2017:
        245120, 2016: 240008, 2015: 237017, 2014: 236736, 2013: 232957,
        2012: 229594, 2011: 224939, 2010: 218056, 2009: 214537, 2008:
        215303, 2007: 207342, 2006: 201600, 2005: 195300, 2004: 188900,
        2003: 183960, 2002: 179880, 2001: 177100, 2000: 172200, 1999:
        166600, 1998: 163000, 1997: 160500, 1996: 156900, 1995: 152400,
        1994: 148200, 1993: 144500, 1992: 140300, 1991: 136200, 1990:
        130699, 1989: 124000, 1988: 118300, 1987: 113600, 1986: 109600,
        1985: 107600, 1984: 103900, 1983: 99600, 1982: 96500, 1981:
        90900, 1980: 82400, 1979: 72600, 1978: 65200, 1977: 60600, 1976:
        56900, 1975: 53800, 1974: 49300, 1973: 44400, 1972: 41800, 1971:
        40500, 1970: 38800, 1969: 36700, 1968: 34800, 1967: 33400, 1966:
        32400, 1965: 31500, 1964: 31000, 1963: 30600, 1962: 30200, 1961:
        29900, 1960: 29600, 1959: 29100, 1958: 28900, 1957: 28100, 1956:
        27200, 1955: 26800, 1954: 26900, 1953: 26700, 1952: 26500, 1951:
        26000, 1950: 24100, 1949: 23800, 1948: 24100, 1947: 22300, 1946:
        19500, 1945: 18000, 1944: 17600, 1943: 17300, 1942: 16300, 1941:
        14700, 1940: 14000, 1939: 13900, 1938: 14100, 1937: 14400, 1936:
        13900, 1935: 13700, 1934: 13400, 1933: 13000, 1932: 13700, 1931:
        15200, 1930: 16700, 1929: 17100, 1928: 17100, 1927: 17400, 1926:
        17700, 1925: 17500, 1924: 17100, 1923: 17100, 1922: 16800, 1921:
        17900, 1920: 20000, 1919: 17300, 1918: 15100, 1917: 12800, 1916:
        10900, 1915: 10100, 1914: 10000, 1913: 9900,
    }
    for y in CPI:
        CPI[y] = flt(CPI[y])/1000
    ref_year = max(CPI)
    min_year = min(CPI)
    min_digits, max_digits = 1, 8
def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)
def Usage(d, status=1):
    name = sys.argv[0]
    print(dedent(f'''
    Usage:  {name} [options] yr [amount1 amount2 ...]
      Print approximately what something cost in year yr compared to
      today ({ref_year}).  If amounts are included, they are scaled to
      both years.  Based on the consumer price index.
    Options:
      -d n      Set the number of significant digits.  [{d["-d"]}]
      -t        Print a CPI table relative to the reference year
      -y yr     Define the reference year.  [{ref_year}]
    '''))
    exit(status)
def GetYear(s):
    try:
        y = int(s)
        if not (min_year <= y <= ref_year):
            raise ValueError()
        return y
    except ValueError:
        msg = f"A year must be between {min_year} and {ref_year}"
        Error(msg)
def ParseCommandLine(d):
    d["-d"] = 3         # Number of significant digits
    d["-p"] = False     # If True, plot the data
    d["-t"] = False     # If True, print table
    d["-y"] = ref_year  # Today reference year
    if len(sys.argv) < 2:
        Usage(d)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:pty:")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o[1] in "pt":
            d[o] = not d[o]
        elif o in ("-d",):
            try:
                d["-d"] = int(a)
                if not (min_digits <= d["-d"] <= max_digits):
                    raise ValueError()
            except ValueError:
                Error("-d option's argument must be an integer between "
                      f"{min_digits} and {max_digits}")
        elif o in ("-y",):
            d["-y"] = GetYear(a)
    if d["-p"]:
        PlotTable(args, d)
    elif d["-t"]:
        PrintTable(args, d)
    if not args:
        Usage(d)
    flt(0).n = d["-d"]
    return args
def PlotTable(args, d):
    from pylab import plot, show, grid, title, xlabel, ylabel, text
    years, cpi = CPI.keys(), CPI.values()
    ref_year = years[-1]
    if args:
        # First item is reference year
        ref_year = GetYear(args[0])
    ref_cpi = CPI[ref_year]
    cpi_rel = [i/ref_cpi for i in cpi]
    plot(years, cpi_rel)
    grid()
    title("Relative US Consumer Price Index 1913-2021\n"
          "(Relative to {}, CPI = {})".format(ref_year, round(ref_cpi, 2)))
    xlabel("Year")
    ylabel("Consumer Price Index")
    show()
def PrintTable(args, d):
    ref_year = d["-y"]
    print(f"$1 in {ref_year} is equivalent to about how much in other years?")
    ref_cpi = CPI[ref_year]
    out = []
    for yr, cpi in sorted(CPI.items()):
        out.append(f"{yr}   ${cpi/ref_cpi}")
    for i in Columnize(out, columns=4, sep=" "*4):
        print(i)
    exit(0)
def rdp(x):
    '''If x is a flt with str interpolation with a trailing decimal point,
    remove the decimal point.
    '''
    s = str(x)
    if s[-1] == ".":
        return s[:-1]
    return s
if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    ref_year = d["-y"]
    # Print percentages
    year = GetYear(args[0])
    cpi, ref_cpi = CPI[year], CPI[ref_year]
    print("Year = {}, reference year = {}, difference = {} years".format(
          year, ref_year, abs(year - ref_year)))
    ratio = ref_cpi/cpi
    print(f"Ratio for year/ref = {ratio}") 
    print(f"Ratio for ref/year = {1/ratio}")
    if len(args) > 1:
        s = "Amounts" if len(args[1:]) > 1 else "Amount"
        a = f"in {year}"
        b = f"in {ref_year}"
        m, n = 12, 20
        print(f"{s:^{m}s}   {a:^{n}s}   {b:^{n}s}")
        print(f"{'-'*m:^{m}s}   {'-'*n:^{n}s}   {'-'*n:^{n}s}")
        for x in [float(j) for j in args[1:]]:
            a = f"${rdp(x*ratio)} in {ref_year}"
            b = f"${rdp(x/ratio)} in {year}"
            print(f"{rdp(x):^{m}s}   {a:^{n}s}   {b:^{n}s}")
