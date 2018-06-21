'''Calculate the integrated irradiance from one or more  StellarNet
irradiance files.  The integral is calculated using the trapezoidal
rule.
 
Also use matplot to plot spectra.
'''
 
from __future__ import print_function, division
import getopt
import sys
from math import log10
from pdb import set_trace as xx

# Copyright (C) 2014 Don Peterson
# Contact:  gmail.com@someonesdad1

#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#
try:
    from pylab import *
except:
    pass

# The following weighting curve came from Appendix B of
# http://www.hpa.org.uk/radiation/publications/documents_of_nrpb/abstracts/absd13-3.htm
#
# It is used to calculate the effective irradiance of UV radiation
# (see paragraph 33, page 7 in the paper):
#
# "The basic exposure limit value (ELV) for both general public and
# occupational exposure to UVR (ultraviolet radiation) incident
# perpendicular to the skin or eye is an effective radiant exposure of
# 30 J m^(-2) within any 8-hour period (ICNIRP, 1999).  This assumes
# that the exposure is delivered during any period of 8 successive
# hours, even where such a period overlaps work shifts or calendar
# days.  Effective radiant exposure (J m^(-2)) is the product of
# exposure duration (s) and effective irradiance (W m^(-2)).
# Effective irradiance is the spectral irradiance Elambda at the eye
# or skin surface, mathematically weighted with the hazard relative
# spectral effectiveness factor s(lambda) and summed from 180 to 400
# nm, as follows:
#
# Eeff = SUM[Elambda*s(lambda)*delta_lambda]
#
# where
#   Eeff = effective irradiance in W m^(-2)
#   Elambda = spectral irradiance from measurements in W m^-2 nm^-1
#   s(lambda) = relative spectral effectiveness factor
#   delta_lambda = bandwidth of the calculation or measurement in nm"
#
# The relative spectral effectiveness factor is given in the following
# array.  The first number is wavelength in nm, the second is the
# relative spectral effectiveness, and the third is the TLV in J/m^2.
#----------------------------------------------------------------------
#
# This table is identical to that given in "2006 TLVs and BEIs",
# ACGIH (American Conference of Government Industrial Hygienists),
# 2006.
#
# Ultraviolet Radiation
# ---------------------
#
# These TLVs refer to ultraviolet (UV) radiation with wavelengths in
# air between 180 and 400 nm and represent conditions under which it
# is believed that nearly all healthy workers may be repeatedly
# exposed without acute adverse health effects such as erythema and
# photokeratitis.  These values for exposure of the eye or the skin
# apply to UV radiation from arcs, gas and vapor discharges,
# fluorescent and incandescent sources, and solar radiation, but they
# do not apply to UV lasers.  They also do not apply to photosensitive
# individuals or individuals taking photosensitizing agents, nor
# aphakes (persons who have the lens of the eye removed).  These
# values should be used as guides in the control of exposure to
# continuous sources for exposure durations >= 0.1 s.
#
# These values should be used as guides in the control of UV exposure
# and should not be regarded as fine lines between safe and dangerous
# levels.
#
# TLVs
# ----
#
# 1.  The UV radiant exposure upon the unprotected skin or eye(s)
#     should not exceed the values in the weighting curve array in an
#     8 hour period.
#
# 2.  The exposure time tmax in seconds to reach the TLV for UV
#     radiation incident upon the unprotected skin or eye may be
#     computed by dividing 0.003 J/cm^2 by the effective irradiance
#     Eeff in W/cm^2 where Eeff = effective irradiance relative to a
#     monochromatic source at 270 nm in W/cm^2.
#
# 3.  To determine Eeff for a broad-band source weighted against the
#     peak of the spectral effectiveness curve (270 nm), the following
#     formula should be used:
#
#       Eeff = [Sum from 180 to 400][Elambda*S(lambda) delta_lambda
#
#       where
#           Eeff = effective irradiance relative to a monochromatic
#                  source at 270 nm in W/cm^2
#           Elambda = spectral irradiance in W/(cm^2*nm)
#           S(lambda) = relative spectral effectiveness
#           delta_lambda = band width in nm
#
# UV-A Spectral Region (315-400 nm)
# ---------------------------------
#
# In addition to the above TLV, exposure of the unprotected eye(s) to
# UV-A should not exceed the following unweighted values:
#
#   1.  A radiant exposure of 1.0 J/cm^2 for periods lasting less than
#       1000 seconds.
#   2.  An irradiance of 1.0 mW/cm^2 for periods lasting 1000 seconds
#       or more.
#
# All preceding TLVs for UV radiation apply to sources that subtend an
# angle less than 80 degrees at the detector.  Sources that subtend a
# greater angle need to be measured only over an angle of 80 degrees.
#
# Table 2:  Exposure Durations for Given Actinic UV Radiation
# Effective Irradiances
#
# Duration of Exposure        Effective Irradiance
#     Per Day                    Eeff (uW/cm^2)
# --------------------        --------------------
#       8 hrs                           0.1
#       4 hrs                           0.2
#       2 hrs                           0.4
#       1 hr                            0.8
#       30 min                          1.7
#       15 min                          3.3
#       10 min                          5
#       5 min                          10
#       1 min                          50
#       30 sec                        100
#       10 sec                        300
#       1 sec                        3000
#       0.5 sec                      6000
#       0.1 sec                     30000
#
# Notes:
#
# 1.  The probability of developing skin cancer depends on a variety
#     of factors such as skin pigmentation, a history of blistering
#     sunburns, and the accumulated UV dose.
#
# 2.  Outdoor workers in latitudes within 40 degrees of the equator
#     can be exposed to levels above the TLVs in as little as 5
#     minutes around noontime during the summer.
#
# 3.  Exposure to ultraviolet radiation concurrently with tropical or
#     systemic exposure to a variety of chemicals, including some
#     prescription drugs, can result in skin erythema at sub-TLV
#     exposures.  Hypersensitivity should be suspected if workers
#     present skin reactions when exposed to sub-TLV doses or when
#     exposed to levels that did not cause a noticeable erythema in
#     the same individual in the past.  Among the hundreds of agents
#     that can cause hypersensitivity to ultraviolet radiation are
#     certain plants and chemicals such as some antibiotics (e.g.,
#     tetracycline and sulphathiazole), some antidepressants (e.g.,
#     imipramine and sinequan), as well as some diuretics, cosmetics,
#     antipsychotic drugs, coal tar distillates, some dyes, or lime
#     oil.
#
# 4.  Ozone is produced in air by sources emitting UV radiation at
#     wavelengths below 250 nm.  Refer to the Chemical Substances TLV
#     for ozone.

#----------------------------------------------------------------------
#
# Column 1 = wavelength in nm
# Column 2 = Slambda, relative spectral weighting factor
# Column 3 = TLV in J/m^2

weighting_curve = (
    (180, 0.012, 2500),
    (190, 0.019, 1600),
    (200, 0.030, 1000),
    (205, 0.051, 590),
    (210, 0.075, 400),
    (215, 0.095, 320),
    (220, 0.120, 250),
    (225, 0.150, 200),
    (230, 0.190, 160),
    (235, 0.240, 130),
    (240, 0.300, 100),
    (245, 0.360, 83),
    (250, 0.430, 70),
    (254, 0.500, 60),                # Hg spectrum
    (255, 0.520, 58),
    (260, 0.650, 46),
    (265, 0.810, 37),
    (270, 1.000, 30),
    (275, 0.960, 31),
    (280, 0.880, 34),                # Hg spectrum
    (285, 0.770, 39),
    (290, 0.640, 47),
    (295, 0.540, 56),
    (297, 0.460, 65),                # Hg spectrum
    (300, 0.300, 100),
    (303, 0.120, 250),               # Hg spectrum
    (305, 0.060, 500),
    (308, 0.026, 1200),
    (310, 0.015, 2000),
    (313, 0.006, 5000),              # Hg spectrum
    (315, 0.003, 1.0e4),
    (316, 0.0024, 1.3e4),
    (317, 0.0020, 1.5e4),
    (318, 0.0016, 1.9e4),
    (319, 0.0012, 2.5e4),
    (320, 0.0010, 2.9e4),
    (322, 0.00067, 4.5e4),
    (323, 0.00054, 5.6e4),
    (325, 0.00050, 6.0e4),
    (328, 0.00044, 6.8e4),
    (330, 0.00041, 7.3e4),
    (333, 0.00037, 8.1e4),
    (335, 0.00034, 8.8e4),
    (340, 0.00028, 1.1e5),
    (345, 0.00024, 1.3e5),
    (350, 0.00020, 1.5e5),
    (355, 0.00016, 1.9e5),
    (360, 0.00013, 2.3e5),
    (365, 0.00011, 2.7e5),           # Hg spectrum
    (370, 0.000093, 3.2e5),
    (375, 0.000077, 3.9e5),
    (380, 0.000064, 4.7e5),
    (385, 0.000053, 5.7e5),
    (390, 0.000044, 6.8e5),
    (395, 0.000036, 8.3e5),
    (400, 0.000030, 1.0e6),
)

# These are numpy arrays containing the data.
Wavelength = None
Weighting = None
def InitializeWeightingData():
    wl = []
    we = []
    for l, e, ignore in weighting_curve:
        wl.append(l)
        we.append(e)
    global Wavelength, Weighting
    Wavelength = array(wl)
    Weighting = array(we)
InitializeWeightingData()


# I fitted straight lines to the above curve to allow analytical
# evaluation.  The lines are between the following points and
# undefined outside of them.  Note the y values need to be the log, as
# the lines are for a semilog plot.

weighting_points = (
    (180, 0.012, 200, 0.03),
    (200, 0.030, 210, 0.075),
    (210, 0.075, 270, 1.000),
    (270, 1.000, 295, 0.600),
    (295, 0.600, 323, 5.4e-4),
    (323, 5.4e-4, 400, 3e-5)
)
weighting = None         # Will contain linear approximation constants
calculate_weighted = 0   # Use weighting for irr if true
short_output = 0         # Only print irradiance if true for 'int'
legend_loc = "best"      # Where to put the legend

def Weighting(lambda1):
    '''Return the weighting factor for wavelengths between 180 nm and
    400 nm.  Return 1e-99 if outside this range.
    '''
    global weighting
    if weighting is None:
        weighting = []
        for la1, w1, la2, w2 in weighting_points:
            slope = (log10(w2) - log10(w1))/(la2 - la1)
            intercept = log10(w1) - slope*la1
            weighting.append((la1, la2, slope, intercept))
        weighting = tuple(weighting)
    for la1, la2, slope, intercept in weighting:
        if la1 <= lambda1 <= la2:
            y = slope*lambda1 + intercept
            return 10**y
    return 1e-99

def TestWeighting():
    '''Print out the ratio of the calculated vs actual.  Around 300-320 nm,
    there are 20-30% deviations, but these aren't important for my uses
    as my practical needs are for the SAM UVa lamps that have little output
    in these regions.
    '''
    for lambda1, weight, ignore in weighting_curve:
        w = Weighting(lambda1)
        ratio = w/weight
        print("%d  %.2f" % (lambda1, ratio), end=" ")
        if 0.8 < ratio < 1.2:
            print()
        else:
            print(" *")

def err(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)

def Usage():
    print('''
Usage:  %s op parameters
  Operates on StellarNet spectrum files.

  int[egrate] [-w] [-s] lambda1 lambda2 file1 [file2...]
    Prints the integrated irradiance for a StellarNet irradiance file
    integrated over the indicated wavelengths.  If the -w option is
    given, the effective irradiance over the UV band is printed.  If
    -s is used, just the calculated integrated irradiance is printed.

  dif[ference] file1 file2 output_file
    Calculates the difference between two spectra and writes it to the
    output file.

  plot [-l loc] plot_title lambda1 lambda2 file1 [file2...]
    Plots the indicated files between the indicated wavelengths.  The
    -l option lets you specify where the legend should be.  Set it to
    "none" for no legend.  Defaults to "best".
'''[1:-1] % sys.argv[0])
    sys.exit(1)


def StellarNet(file):
    '''Return (w, s) where w is the array of wavelengths and s is the array
    of spectral irradiances.
    '''
    lines = open(file).readlines()
    # Remove lines from front of file beginning with '"' and from end of
    # file beginning with ':'.
    while lines[0][0] == '"' or lines[0][0] == '#':
        lines = lines[1:]
    while lines[-1][0] == ':':
        lines = lines[0:-1]
    wavelength = []
    spectral_irradiance = []
    for line in lines:
        x, y = line.split()
        wavelength.append(float(x))
        spectral_irradiance.append(float(y))
    return array(wavelength), array(spectral_irradiance)

def ReadLines(file):
    lines = open(file).readlines()
    # Remove lines from front of file beginning with '"' and from end of
    # file beginning with ':'.
    while lines[0][0] == '"' or lines[0][0] == '#':
        lines = lines[1:]
    while lines[-1][0] == ':':
        lines = lines[0:-1]
    lines = [s.split() for s in lines]
    for ix in xrange(len(lines)):
        lines[ix] = (float(lines[ix][0]), float(lines[ix][1]))
    assert(len(lines) > 2)
    return lines

def SelectSubset(lines, lambda1, lambda2):
    '''Return all lines with wavelengths between lambda1 and lambda2
    inclusive.
    '''
    return [x for x in lines if lambda1 <= x[0] <= lambda2]

def Integrate(Lines, lambda1, lambda2):
    '''Use the trapezoidal rule.  From Bartsch, "Handbook of Mathematical
    Formulas", Academic Press, 1974, page 361.
    '''
    assert(lambda1 < lambda2)
    lines = SelectSubset(Lines, lambda1, lambda2)
    assert(len(lines) > 1)
    a = lines[0][0]
    b = lines[-1][0]
    ya = lines[0][1]
    yb = lines[-1][1]
    n = len(lines) - 1  # Number of intervals
    interior = lines[1:-1]
    def weight(lambda1):
        if calculate_weighted:
            return Weighting(lambda1)
        else:
            return 1.0
    interior_sum = sum([x[1]*weight(x[0]) for x in interior])
    power = (ya + yb + 2*interior_sum) * ((b - a)/(2*n))
    return power

def PrintResults(lambda1, lambda2, file, short=0):
    power = Integrate(ReadLines(file), lambda1, lambda2)
    if short:
        print("%14.6f" % power)
    else:
        print("%14.6f  %s" % (power, file))

def Test():
    '''We should get 5.7411 for the band [300, 400] nm for the
    following data: '''
    data = [
        [298.50, 1.840E-004],
        [299.00, 5.888E-005],
        [299.50, 8.308E-005],
        [300.00, 9.661E-005],
        [300.50, 8.834E-005],
        [301.00, 6.585E-005],
        [301.50, 5.899E-006],
        [302.00, 0.000E+000],
        [302.50, 0.000E+000],
        [303.00, 0.000E+000],
        [303.50, 2.206E-005],
        [304.00, 5.637E-005],
        [304.50, 6.309E-005],
        [305.00, 2.241E-005],
        [305.50, 1.310E-004],
        [306.00, 2.665E-004],
        [306.50, 3.427E-004],
        [307.00, 3.719E-004],
        [307.50, 3.749E-004],
        [308.00, 3.189E-004],
        [308.50, 2.610E-004],
        [309.00, 1.326E-004],
        [309.50, 7.072E-006],
        [310.00, 0.000E+000],
        [310.50, 0.000E+000],
        [311.00, 0.000E+000],
        [311.50, 3.437E-005],
        [312.00, 2.718E-004],
        [312.50, 5.712E-004],
        [313.00, 7.039E-004],
        [313.50, 6.865E-004],
        [314.00, 5.482E-004],
        [314.50, 3.919E-004],
        [315.00, 2.656E-004],
        [315.50, 1.799E-004],
        [316.00, 1.537E-004],
        [316.50, 1.633E-004],
        [317.00, 1.537E-004],
        [317.50, 1.630E-004],
        [318.00, 8.804E-005],
        [318.50, 4.805E-005],
        [319.00, 3.060E-005],
        [319.50, 2.281E-006],
        [320.00, 1.373E-006],
        [320.50, 5.559E-005],
        [321.00, 1.739E-004],
        [321.50, 3.332E-004],
        [322.00, 4.217E-004],
        [322.50, 3.234E-004],
        [323.00, 3.017E-004],
        [323.50, 3.125E-004],
        [324.00, 3.208E-004],
        [324.50, 4.403E-004],
        [325.00, 4.846E-004],
        [325.50, 5.226E-004],
        [326.00, 5.530E-004],
        [326.50, 5.528E-004],
        [327.00, 5.726E-004],
        [327.50, 6.793E-004],
        [328.00, 7.918E-004],
        [328.50, 9.023E-004],
        [329.00, 9.472E-004],
        [329.50, 1.030E-003],
        [330.00, 1.184E-003],
        [330.50, 1.249E-003],
        [331.00, 1.325E-003],
        [331.50, 1.316E-003],
        [332.00, 1.389E-003],
        [332.50, 1.599E-003],
        [333.00, 1.905E-003],
        [333.50, 2.236E-003],
        [334.00, 2.581E-003],
        [334.50, 2.905E-003],
        [335.00, 3.114E-003],
        [335.50, 3.244E-003],
        [336.00, 3.290E-003],
        [336.50, 3.308E-003],
        [337.00, 3.351E-003],
        [337.50, 3.435E-003],
        [338.00, 3.580E-003],
        [338.50, 3.784E-003],
        [339.00, 4.050E-003],
        [339.50, 4.402E-003],
        [340.00, 4.688E-003],
        [340.50, 4.878E-003],
        [341.00, 5.013E-003],
        [341.50, 5.173E-003],
        [342.00, 5.453E-003],
        [342.50, 5.842E-003],
        [343.00, 6.195E-003],
        [343.50, 6.531E-003],
        [344.00, 6.784E-003],
        [344.50, 7.021E-003],
        [345.00, 7.290E-003],
        [345.50, 7.487E-003],
        [346.00, 7.778E-003],
        [346.50, 8.180E-003],
        [347.00, 8.650E-003],
        [347.50, 9.202E-003],
        [348.00, 9.782E-003],
        [348.50, 1.032E-002],
        [349.00, 1.093E-002],
        [349.50, 1.160E-002],
        [350.00, 1.239E-002],
        [350.50, 1.331E-002],
        [351.00, 1.435E-002],
        [351.50, 1.556E-002],
        [352.00, 1.699E-002],
        [352.50, 1.881E-002],
        [353.00, 2.085E-002],
        [353.50, 2.313E-002],
        [354.00, 2.571E-002],
        [354.50, 2.872E-002],
        [355.00, 3.236E-002],
        [355.50, 3.653E-002],
        [356.00, 4.121E-002],
        [356.50, 4.643E-002],
        [357.00, 5.242E-002],
        [357.50, 5.937E-002],
        [358.00, 6.705E-002],
        [358.50, 7.526E-002],
        [359.00, 8.417E-002],
        [359.50, 9.391E-002],
        [360.00, 1.043E-001],
        [360.50, 1.157E-001],
        [361.00, 1.276E-001],
        [361.50, 1.406E-001],
        [362.00, 1.556E-001],
        [362.50, 1.716E-001],
        [363.00, 1.878E-001],
        [363.50, 2.027E-001],
        [364.00, 2.160E-001],
        [364.50, 2.297E-001],
        [365.00, 2.464E-001],
        [365.50, 2.644E-001],
        [366.00, 2.798E-001],
        [366.50, 2.890E-001],
        [367.00, 2.919E-001],
        [367.50, 2.907E-001],
        [368.00, 2.887E-001],
        [368.50, 2.868E-001],
        [369.00, 2.850E-001],
        [369.50, 2.830E-001],
        [370.00, 2.808E-001],
        [370.50, 2.779E-001],
        [371.00, 2.742E-001],
        [371.50, 2.698E-001],
        [372.00, 2.639E-001],
        [372.50, 2.568E-001],
        [373.00, 2.487E-001],
        [373.50, 2.407E-001],
        [374.00, 2.326E-001],
        [374.50, 2.243E-001],
        [375.00, 2.154E-001],
        [375.50, 2.056E-001],
        [376.00, 1.954E-001],
        [376.50, 1.851E-001],
        [377.00, 1.753E-001],
        [377.50, 1.662E-001],
        [378.00, 1.577E-001],
        [378.50, 1.495E-001],
        [379.00, 1.413E-001],
        [379.50, 1.331E-001],
        [380.00, 1.248E-001],
        [380.50, 1.168E-001],
        [381.00, 1.093E-001],
        [381.50, 1.024E-001],
        [382.00, 9.622E-002],
        [382.50, 9.050E-002],
        [383.00, 8.499E-002],
        [383.50, 7.968E-002],
        [384.00, 7.463E-002],
        [384.50, 6.979E-002],
        [385.00, 6.524E-002],
        [385.50, 6.072E-002],
        [386.00, 5.622E-002],
        [386.50, 5.195E-002],
        [387.00, 4.800E-002],
        [387.50, 4.451E-002],
        [388.00, 4.151E-002],
        [388.50, 3.867E-002],
        [389.00, 3.583E-002],
        [389.50, 3.303E-002],
        [390.00, 3.017E-002],
        [390.50, 2.768E-002],
        [391.00, 2.548E-002],
        [391.50, 2.350E-002],
        [392.00, 2.180E-002],
        [392.50, 2.016E-002],
        [393.00, 1.869E-002],
        [393.50, 1.726E-002],
        [394.00, 1.584E-002],
        [394.50, 1.453E-002],
        [395.00, 1.330E-002],
        [395.50, 1.210E-002],
        [396.00, 1.105E-002],
        [396.50, 1.004E-002],
        [397.00, 9.152E-003],
        [397.50, 8.383E-003],
        [398.00, 7.629E-003],
        [398.50, 7.000E-003],
        [399.00, 6.375E-003],
        [399.50, 5.734E-003],
        [400.00, 5.214E-003],
        [400.50, 4.736E-003],
        [401.00, 4.320E-003],
        [401.50, 3.992E-003],
        [402.00, 3.689E-003],
    ]
    irradiance = Integrate(data, 300, 400)
    expected = 5.7411   # W/m^2
    assert(abs(irradiance - expected) < 1e-4)
    print("Test passed")

def ProcessCommandLine():
    global legend_loc
    if len(sys.argv) < 2:
        Usage()
    command = sys.argv[1][:3]
    if command == "int":
        try:
            optlist, args = getopt.getopt(sys.argv[2:], "l:stw")
        except getopt.error as str:
            print("getopt error:  %s" % str)
            sys.exit(1)
        for opt in optlist:
            if opt[0] == "-l":
                legend_loc = opt[1]
            if opt[0] == "-s":
                global short_output
                short_output = 1
            if opt[0] == "-w":
                global calculate_weighted
                calculate_weighted = 1
            if opt[0] == "-t":
                global Title
                Title = opt[1]
        if len(args) < 3:
            Usage()
        try:
            lambda1 = float(args[0])
            lambda2 = float(args[1])
            if lambda1 >= lambda2:
                err("lambda1 must be < lambda2\n")
            if lambda1 <= 0:
                err("lambda1 must be > 0\n")
            if lambda2 <= 0:
                err("lambda2 must be > 0\n")
        except:
            Usage()
    elif command == "dif":
        # Need dif file1 file2 output_file
        if len(sys.argv) < 5:
            Usage()
        else:
            args = sys.argv[2:]
    elif command == "plo":
        # Need plot plot_title lambda1 lambda2 file1 [file2...]
        try:
            optlist, args = getopt.getopt(sys.argv[2:], "l:")
        except getopt.error as str:
            print("getopt error:  %s" % str)
            sys.exit(1)
        for opt in optlist:
            if opt[0] == "-l":
                legend_loc = opt[1]
        if len(args) < 4:
            Usage()
    else:
        Usage()
    args = [command] + args
    return args

def CalculateIrradiance(args):
    lambda1 = float(args[1])
    lambda2 = float(args[2])
    if short_output:
        for file in args[3:]:
            PrintResults(lambda1, lambda2, file, 1)
    else:
        print("Irradiance in W/m^2 over [%.1f, %.1f] nm for the "
              "following files:" % (lambda1, lambda2))
        for file in args[3:]:
            PrintResults(lambda1, lambda2, file)

def CalculateDifference(args):
    # Put spectra into dictionary keyed by wavelength
    wavelength1 = {}
    wavelength2 = {}
    for wavelength, signal in ReadLines(args[1]):
        wavelength1[wavelength] = signal
    for wavelength, signal in ReadLines(args[2]):
        wavelength2[wavelength] = signal
    # Calculate difference
    diff = {}
    for wavelength in wavelength1:
        if wavelength in wavelength2.:
            diff[wavelength] = wavelength1[wavelength] - wavelength2[wavelength]
        else:
            diff[wavelength] = wavelength1[wavelength]
    # Change difference dictionary back into a list
    list = diff.keys()
    list.sort()
    for ix in xrange(len(list)):
        list[ix] = (list[ix], diff[list[ix]])
    # Write to output file
    ofp = open(args[3], "wb")
    for item in list:
        ofp.write("%.1f %.4e\n" % item)

def GetSpectrum(file):
    '''Process a StellarNet type spectrum.  Return two tuples:  the first
    is the wavelengths and the second is the spectral irradiance.
    '''
    lines = ReadLines(file)
    wavelengths = []
    spectral_irradiance = []
    for wl, sir in lines:
        wavelengths.append(wl)
        spectral_irradiance.append(sir)
    return tuple(wavelengths), tuple(spectral_irradiance)

def Truncate(wl, sir, lambda1, lambda2):
    '''Remove any values in wl and corresponding values in sir that are
    outside of the indicated wavelength band.  Return the modified (wl, sir).
    '''
    wlnew, sirnew = [], []
    if lambda1 > lambda2:
        lambda1, lambda2 = lambda2, lambda1
    for i in xrange(len(wl)):
        if lambda1 <= wl[i] <= lambda2:
            wlnew.append(wl[i])
            sirnew.append(sir[i])
    return array(wlnew), array(sirnew)


def Plot(args):
    plot_title = args[1]
    lambda1 = float(args[2])
    lambda2 = float(args[3])
    for file in args[4:]:
        wavelengths, spectral_irradiance = GetSpectrum(file)
        wl = array(wavelengths)
        sir = array(spectral_irradiance)
        wl, sir = Truncate(wl, sir, lambda1, lambda2)
        plot(wl, sir, label=file)
    xlabel('Wavelength, nm')
    ylabel('Spectral Irradiance, (W/m^2)/nm')
    axis(xmin=lambda1, xmax=lambda2)
    if legend_loc != "none":
        legend(loc=legend_loc)
    title(plot_title)
    grid(True)
    show()

def main():
    args = ProcessCommandLine()
    if args[0] == "int":
        CalculateIrradiance(args)
    elif args[0] == "dif":
        CalculateDifference(args)
    elif args[0] == "plo":
        Plot(args)

if __name__ == "__main__":
    main()
