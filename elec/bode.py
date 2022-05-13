if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2011 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Make a Bode plot of a transfer function
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
    import getopt
    from pylab import *
def Usage(d, status=1):
    name = sys.argv[0]
    lower = d["-l"]
    upper = d["-u"]
    s = '''Usage:  {name} [options] xfr_fn_file
  Generates a Bode plot for a transfer function defined in a file called
  xfr_fn_file.  This file must contain a python function of the form

    def H(s):
        Define function here

  This code is then executed to make a plot.

  Example:  to plot the transfer function H = 2*s/(s^2 - 4*s + 3), define H
  to be

    def H(s):
        return 2*s/(s**2 - 4*s + 3)

Options:
    -l dec
        Lower frequency of the plot; defaults to {lower}.  The frequency is
        10^dec Hz.  dec must be a number that can have the integer part taken.
    -L
        Make the vertical axis linear instead of logarithmic.
    -u dec
        Upper frequency of the plot; defaults to {upper}.  The frequency is
        10^dec Hz.  dec must be a number that can have the integer part taken.
    -t title
        String to use for the plot's title
'''
    print(s.format(**locals()))
    exit(status)
def ParseCommandLine(d):
    d["-l"] = 0
    d["-L"] = False
    d["-t"] = ""
    d["-u"] = 5
    if len(sys.argv) < 2:
        Usage(d)
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "Ll:u:t:")
    except getopt.GetoptError as str:
        msg, option = str
        sys.stdout.write(msg + "\n")
        sys.exit(1)
    for opt in optlist:
        if opt[0] == "-L":
            d["-L"] = True
        if opt[0] == "-l":
            d["-l"] = int(opt[1])
        if opt[0] == "-t":
            d["-t"] = opt[1]
        if opt[0] == "-u":
            d["-u"] = int(opt[1])
    if len(args) != 1:
        Usage(d)
    return args
def Plot(file, d):
    n, R = 1000, d["-u"] - d["-l"]
    f = 10**arange(d["-l"], d["-u"], R/n)
    w = 2*pi*f
    s = w*1j
    # Read in the function
    with open(file) as source_file:
        exec(source_file.read(), globals(), globals())
    # Make the plot
    response = H(s)
    subplot(211)
    if d["-L"]:
        semilogx(f, abs(response))
        ys = "Response"
    else:
        semilogx(f, 20*log10(abs(response)))
        ys = "Response, dB"
    if d["-t"]:
        t = d["-t"] + "\nMagnitude"
    else:
        t = "Magnitude"
    title(t)
    ylabel(ys)
    grid()
    subplot(212)
    title("Phase")
    phase = arctan2(imag(response), real(response))*180/pi   # In degrees
    semilogx(f, phase)
    grid()
    xlabel("Frequency, Hz")
    ylabel("Phase, degrees")
    show()
if __name__ == "__main__": 
    d = {}   # Options dictionary
    args = ParseCommandLine(d)
    Plot(args[0], d)
