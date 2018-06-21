'''
This script is a python translation of the NOVAS-C 2.0.1 software in C
from the U.S. Naval Observatory.  See
http://aa.usno.navy.mil/software/novas/novas_c/novasc_info.html.
 
*****************************************************************
* PLEASE NOTE:  this software is not a product of the people at *
* the U.S. Naval Observatory and is not supported by them.      *
*****************************************************************
 
Run this script as 'python novas.py' to perform the same testing as
done by the checkout-st.c program in the NOVAS package.  You should
see the identical results.
 
I wrote some python scripts to perform the translation from the C
code.  This did about 90% of the work; the remaining stuff I
translated by hand.  In particular, I stripped all of the comments out
of the C code.  If you're interested in understanding the code, see
the comments in the C source.
 
The only hacks I added were in precession() and proper_motion(), where
I had to check the type of an incoming parameter.  Where variables
were passed by reference, I had to use a python list as the variable,
since that would be the only way a change in the parameter would get
back to the calling context.  Thus, if you want to use these routines,
you'll have to look at the C code and find where the addresses are
passed; where they are, make sure you pass in a list.  '''
 
# Copyright (C) 2003 Don Peterson
# Contact:  gmail.com@someonesdad1
 
#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#
 
from __future__ import division
from math import pi, fabs, fmod, sin, cos, atan2, asin, sqrt

ii = isinstance

PSI_COR = 0.0
EPS_COR = 0.0

# Constants from novascon.c
FN1 = 1
FN0 = 0
T0 = 2451545.00000000
KMAU = 1.49597870e+8
MAU = 1.49597870e+11
C = 173.14463348
GS = 1.32712438e+20
EARTHRAD = 6378.140
F = 0.00335281
OMEGA = 7.292115e-5
TWOPI = 2*pi
RAD2SEC = 3600*180/pi
DEG2RAD = pi/180
RAD2DEG = 180/pi


# The following three dictionaries are used to represent the structures
# that were in novas.h.

#   body: designates a celestial object.
#
#   type              = type of body
#                     = 0 ... major planet, Sun, or Moon
#                     = 1 ... minor planet
#   number            = body number
#                       For 'type' = 0: Mercury = 1, ..., Pluto = 9,
#                                       Sun = 10, Moon = 11
#                       For 'type' = 1: minor planet number
#   name              = name of the body (limited to 99 characters)

body = {
    "type"   : 0,
    "number" : 0,
    "name"   : "",
}


#   site_info: data for the observer's location.  The atmospheric
#                     parameters are used only by the refraction
#                     function called from function 'equ_to_hor'.
#                     Additional parameters can be added to this
#                     structure if a more sophisticated refraction model
#                     is employed.
#
#   latitude           = geodetic latitude in degrees; north positive.
#   longitude          = geodetic longitude in degrees; east positive.
#   height             = height of the observer in meters.
#   temperature        = temperature (degrees Celsius).
#   pressure           = atmospheric pressure (millibars)

site_info = {
    "latitude"    : 0.0,
    "longitude"   : 0.0,
    "height"      : 0.0,
    "temperature" : 0.0,
    "pressure"    : 0.0,
}

#
#   cat_entry: the astrometric catalog data for a star; equator
#                     and equinox and units will depend on the catalog.
#                     While this structure can be used as a generic
#                     container for catalog data, all high-level
#                     NOVAS-C functions require J2000.0 catalog data
#                     with FK5-type units (shown in square brackets
#                     below).
#
#   catalog[4]         = 3-character catalog designator.
#   starname[51]       = name of star.
#   starnumber         = integer identifier assigned to star.
#   ra                 = mean right ascension [hours].
#   dec                = mean declination [degrees].
#   promora            = proper motion in RA [seconds of time per
#                        century].
#   promodec           = proper motion in declination [arcseconds per
#                        century].
#   parallax           = parallax [arcseconds].
#   radialvelocity     = radial velocity [kilometers per second].

cat_entry = {
    "catalog"        : "",
    "starname"       : "",
    "starnumber"     : 0,
    "ra"             : 0.0,
    "dec"            : 0.0,
    "promora"        : 0.0,
    "promodec"       : 0.0,
    "parallax"       : 0.0,
    "radialvelocity" : 0.0,
}

BARYC = 0
HELIOC = 1

#----------------------------------------------------------------------
# Added utility functions

def mag3vec(x):
    return x[0]*x[0] + x[1]*x[1] + x[2]*x[2]

def DumpLocals(msg, vars, names=[]):
    '''Print the message in msg, then the alphabetized list of variables
    in the vars dictionary.
    '''
    print(msg)
    if len(names) == 0:
        names = vars.keys()
    names.sort()
    g = globals()
    for var in names:
        try:
            print("   ", var, "=", vars[var])
        except:
            print("   ", var, "=", g[var])
    print()

#----------------------------------------------------------------------
# The following two functions were translated from the solsys3.c file.

# These were static double variables in solarsystem()
tlast_ss = 0.0
sine_ss = 0.0
cose_ss = 0.0
tmass_ss = 0.0
pbary_ss = [0.0, 0.0, 0.0]
vbary_ss = [0.0, 0.0, 0.0]

def solarsystem(tjd, body, origin, pos, vel):
    global tlast_ss
    global sine_ss
    global cose_ss
    global tmass_ss
    global pbary_ss
    global vbary_ss
    pm = [1047.349, 3497.898, 22903.0, 19412.2]
    pa = [5.203363, 9.537070, 19.191264, 30.068963]
    pl = [0.600470, 0.871693, 5.466933, 5.321160]
    pn = [1.450138e-3, 5.841727e-4, 2.047497e-4, 1.043891e-4]
    obl = 23.43929111
    oblr = 0.0
    qjd = 0.0
    ras = [0.0]
    decs = [0.0]
    diss = [0.0]
    dlon = 0.0
    sinl = 0.0
    cosl = 0.0
    x = 0.0
    y = 0.0
    z = 0.0
    xdot = 0.0
    ydot = 0.0
    zdot = 0.0
    f = 0.0
    pos1 = [0.0, 0.0, 0.0]
    p = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
    if tlast_ss == 0.0:
        oblr = obl*TWOPI/360.0
        sine_ss = sin(oblr)
        cose_ss = cos(oblr)
        tmass_ss = 1.0
        for i in range(4):
            tmass_ss += 1.0/pm[i]
        tlast_ss = 1.0
    if tjd < 2340000.5 or tjd > 2560000.5:
        return 1
    if body == 0 or body == 1 or body == 10:
        for i in range(3):
            pos[i] = vel[i] = 0.0
    elif body == 2 or body == 3:
        for i in range(3):
            qjd = tjd + (i - 1)*0.1
            sun_eph(qjd, ras, decs, diss)
            radec2vector(ras, decs, diss, pos1)
            precession(qjd, pos1, T0, pos)
            p[i][0] = -pos[0]
            p[i][1] = -pos[1]
            p[i][2] = -pos[2]
        for i in range(3):
            pos[i] = p[1][i]
            vel[i] = (p[2][i] - p[0][i])/0.2
    else:
        return 2
    if origin == 0:
        if fabs(tjd - tlast_ss) >= 1.0e-06:
            for i in range(3):
                pbary_ss[i] = vbary_ss[i] = 0.0
            for i in range(4):
                dlon = pl[i] + pn[i]*(tjd - T0)
                dlon = fmod(dlon, TWOPI)
                sinl = sin(dlon)
                cosl = cos(dlon)
                x = pa[i]*cosl
                y = pa[i]*sinl*cose_ss
                z = pa[i]*sinl*sine_ss
                xdot = -pa[i]*pn[i]*sinl
                ydot = pa[i]*pn[i]*cosl*cose_ss
                zdot = pa[i]*pn[i]*cosl*sine_ss
                f = 1.0/(pm[i]*tmass_ss)
                pbary_ss[0] += x*f
                pbary_ss[1] += y*f
                pbary_ss[2] += z*f
                vbary_ss[0] += xdot*f
                vbary_ss[1] += ydot*f
                vbary_ss[2] += zdot*f
            tlast_ss = tjd
        for i in range(3):
            pos[i] -= pbary_ss[i]
            vel[i] -= vbary_ss[i]
    return 0

sun_con_data = [
    (403406.0, 0.0, 4.721964, 1.621043),
    (195207.0, -97597.0, 5.937458, 62830.348067),
    (119433.0, -59715.0, 1.115589, 62830.821524),
    (112392.0, -56188.0, 5.781616, 62829.634302),
    (3891.0, -1556.0, 5.5474, 125660.5691),
    (2819.0, -1126.0, 1.5120, 125660.9845),
    (1721.0, -861.0, 4.1897, 62832.4766),
    (0.0, 941.0, 1.163, 0.813),
    (660.0, -264.0, 5.415, 125659.310),
    (350.0, -163.0, 4.315, 57533.850),
    (334.0, 0.0, 4.553, -33.931),
    (314.0, 309.0, 5.198, 777137.715),
    (268.0, -158.0, 5.989, 78604.191),
    (242.0, 0.0, 2.911, 5.412),
    (234.0, -54.0, 1.423, 39302.098),
    (158.0, 0.0, 0.061, -34.861),
    (132.0, -93.0, 2.317, 115067.698),
    (129.0, -20.0, 3.193, 15774.337),
    (114.0, 0.0, 2.828, 5296.670),
    (99.0, -47.0, 0.52, 58849.27),
    (93.0, 0.0, 4.65, 5296.11),
    (86.0, 0.0, 4.35, -3980.70),
    (78.0, -33.0, 2.75, 52237.69),
    (72.0, -32.0, 4.50, 55076.47),
    (68.0, 0.0, 3.23, 261.08),
    (64.0, -10.0, 1.22, 15773.85),
    (46.0, -16.0, 0.14, 188491.03),
    (38.0, 0.0, 3.44, -7756.55),
    (37.0, 0.0, 4.37, 264.89),
    (32.0, -24.0, 1.14, 117906.27),
    (29.0, -13.0, 2.84, 55075.75),
    (28.0, 0.0, 5.96, -7961.39),
    (27.0, -9.0, 5.09, 188489.81),
    (27.0, 0.0, 1.72, 2132.19),
    (25.0, -17.0, 2.56, 109771.03),
    (24.0, -11.0, 1.92, 54868.56),
    (21.0, 0.0, 0.09, 25443.93),
    (21.0, 31.0, 5.98, -55731.43),
    (20.0, -10.0, 4.03, 60697.74),
    (18.0, 0.0, 4.27, 2132.79),
    (17.0, -12.0, 0.79, 109771.63),
    (14.0, 0.0, 4.24, -7752.82),
    (13.0, -5.0, 2.01, 188491.91),
    (13.0, 0.0, 2.65, 207.81),
    (13.0, 0.0, 4.98, 29424.63),
    (12.0, 0.0, 0.93, -7.99),
    (10.0, 0.0, 2.21, 46941.14),
    (10.0, 0.0, 3.59, -68.29),
    (10.0, 0.0, 1.50, 21463.25),
    (10.0, -9.0, 2.55, 157208.40)
]

# Make an array of dictionaries to simulate an array of structs
sun_con = []
for item in sun_con_data:
    d = {}
    d["l"] = item[0]
    d["r"] = item[1]
    d["alpha"] = item[2]
    d["nu"] = item[3]
    sun_con.append(d)

def sun_eph(jd, ra, dec, dis):
    sum_lon = 0.0
    sum_r = 0.0
    factor = 1.0e-07
    u = 0.0
    arg = 0.0
    lon = 0.0
    lat = 0.0
    t = 0.0
    t2 = 0.0
    emean = 0.0
    sin_lon = 0.0

    u = (jd - T0)/3652500.0
    for i in range(50):
        arg = sun_con[i]["alpha"] + sun_con[i]["nu"]*u
        sum_lon += sun_con[i]["l"]*sin(arg)
        sum_r += sun_con[i]["r"]*cos(arg)
    lon = 4.9353929 + 62833.1961680*u + factor*sum_lon
    lon = fmod(lon, TWOPI)
    while lon < 0.0:
        lon += TWOPI
    lat = 0.0
    dis[0] = 1.0001026 + factor*sum_r
    t = u*100.0
    t2 = t*t
    emean = (0.001813*t2*t - 0.00059*t2 - 46.8150*t +
             84381.448)/RAD2SEC
    sin_lon = sin(lon)
    ra[0] = atan2((cos(emean)*sin_lon), cos(lon))*RAD2DEG
    ra[0] = fmod(ra[0], 360.0)
    if ra[0] < 0.0:
        ra[0] += 360.0
    ra[0] = ra[0]/15.0
    dec[0] = asin(sin(emean)*sin_lon)*RAD2DEG
    return

#----------------------------------------------------------------------
# The remainder of the file came from the novas.c file translation.

def app_star(tjd, earth, star, ra, dec):
    error = 0
    tdb = [0.0]
    time2 = [0.0]
    peb = [0.0, 0.0, 0.0, ]
    veb = [0.0, 0.0, 0.0, ]
    pes = [0.0, 0.0, 0.0, ]
    ves = [0.0, 0.0, 0.0, ]
    pos1 = [0.0, 0.0, 0.0, ]
    pos2 = [0.0, 0.0, 0.0, ]
    pos3 = [0.0, 0.0, 0.0, ]
    pos4 = [0.0, 0.0, 0.0, ]
    pos5 = [0.0, 0.0, 0.0, ]
    pos6 = [0.0, 0.0, 0.0, ]
    pos7 = [0.0, 0.0, 0.0, ]
    vel1 = [0.0, 0.0, 0.0, ]
    error = get_earth(tjd, earth, tdb, peb, veb, pes, ves)
    if error:
        ra[0] = 0.0
        dec[0] = 0.0
        return error
    starvectors(star, pos1, vel1)
    proper_motion(T0, pos1, vel1, tdb, pos2)
    bary_to_geo(pos2, peb, pos3, time2)
    sun_field(pos3, pes, pos4)
    aberration(pos4, veb, time2, pos5)
    precession(T0, pos5, tdb, pos6)
    nutate(tdb, FN0, pos6, pos7)
    vector2radec(pos7, ra, dec)
    return 0

def app_planet(tjd, ss_object, earth, ra, dec, dis):
    error = 0
    tdb = [0.0]
    peb = [0.0, 0.0, 0.0, ]
    veb = [0.0, 0.0, 0.0, ]
    pes = [0.0, 0.0, 0.0, ]
    ves = [0.0, 0.0, 0.0, ]
    t2 = [0.0]
    t3 = [0.0]
    lighttime = [0.0]
    pos1 = [0.0, 0.0, 0.0, ]
    vel1 = [0.0, 0.0, 0.0, ]
    pos2 = [0.0, 0.0, 0.0, ]
    pos3 = [0.0, 0.0, 0.0, ]
    pos4 = [0.0, 0.0, 0.0, ]
    pos5 = [0.0, 0.0, 0.0, ]
    pos6 = [0.0, 0.0, 0.0, ]
    error = get_earth(tjd, earth, tdb, peb, veb, pes, ves)
    if error:
        ra[0] = 0.0
        dec[0] = 0.0
        return error + 10
    error = ephemeris(tdb, ss_object, BARYC, pos1, vel1)
    if error:
        ra[0] = 0.0
        dec[0] = 0.0
        dis[0] = 0.0
        return error
    bary_to_geo(pos1, peb, pos2, lighttime)
    dis[0] = lighttime*C
    t3 = tdb - lighttime
    # Do-while
    t2 = t3
    error = ephemeris(t2, ss_object, BARYC, pos1, vel1)
    if error:
        ra[0] = 0.0
        dec[0] = 0.0
        dis[0] = 0.0
        return error
    bary_to_geo(pos1, peb, pos2, lighttime)
    t3 = tdb - lighttime
    while fabs(t3 - t2) > 1.0e-8:
        t2 = t3
        error = ephemeris(t2, ss_object, BARYC, pos1, vel1)
        if error:
            ra[0] = 0.0
            dec[0] = 0.0
            dis[0] = 0.0
            return error
        bary_to_geo(pos1, peb, pos2, lighttime)
        t3 = tdb - lighttime
    # End do-while
    sun_field(pos2, pes, pos3)
    aberration(pos3, veb, lighttime, pos4)
    precession(T0, pos4, tdb, pos5)
    nutate(tdb, FN0, pos5, pos6)
    vector2radec(pos6, ra, dec)
    return 0

def topo_star(tjd, earth, deltat, star, location, ra, dec):
    error = 0
    lighttime = [0.0]
    ujd = [0.0]
    pob = [0.0, 0.0, 0.0, ]
    pog = [0.0, 0.0, 0.0, ]
    vob = [0.0, 0.0, 0.0, ]
    vog = [0.0, 0.0, 0.0, ]
    pos = [0.0, 0.0, 0.0, ]
    gast = [0.0]
    pos1 = [0.0, 0.0, 0.0, ]
    pos2 = [0.0, 0.0, 0.0, ]
    pos3 = [0.0, 0.0, 0.0, ]
    pos4 = [0.0, 0.0, 0.0, ]
    pos5 = [0.0, 0.0, 0.0, ]
    pos6 = [0.0, 0.0, 0.0, ]
    pos7 = [0.0, 0.0, 0.0, ]
    vel1 = [0.0, 0.0, 0.0, ]
    vel2 = [0.0, 0.0, 0.0, ]
    tdb = [0.0]
    peb = [0.0, 0.0, 0.0, ]
    veb = [0.0, 0.0, 0.0, ]
    pes = [0.0, 0.0, 0.0, ]
    ves = [0.0, 0.0, 0.0, ]
    oblm = [0.0]
    oblt = [0.0]
    eqeq = [0.0]
    psi = [0.0]
    eps = [0.0]
    ujd = tjd - (deltat/86400.0)
    error = get_earth(tjd, earth, tdb, peb, veb, pes, ves)
    if error:
        ra[0] = 0.0
        dec[0] = 0.0
        return error
    earthtilt(tdb, oblm, oblt, eqeq, psi, eps)
    sidereal_time(ujd, 0.0, eqeq, gast)
    terra(location, gast, pos1, vel1)
    nutate(tdb, FN1, pos1, pos2)
    precession(tdb, pos2, T0, pog)
    nutate(tdb, FN1, vel1, vel2)
    precession(tdb, vel2, T0, vog)
    for j in range(3):
        pob[j] = peb[j] + pog[j]
        vob[j] = veb[j] + vog[j]
        pos[j] = pes[j] + pog[j]
    starvectors(star, pos1, vel1)
    proper_motion(T0, pos1, vel1, tdb, pos2)
    bary_to_geo(pos2, pob, pos3, lighttime)
    sun_field(pos3, pos, pos4)
    aberration(pos4, vob, lighttime, pos5)
    precession(T0, pos5, tdb, pos6)
    nutate(tdb, FN0, pos6, pos7)
    vector2radec(pos7, ra, dec)
    return 0

def topo_planet(tjd, ss_object, earth, deltat, location, ra, dec, dis):
    error = 0
    ujd = [0.0]
    t2 = [0.0]
    t3 = [0.0]
    gast = [0.0]
    pos1 = [0.0, 0.0, 0.0, ]
    pos2 = [0.0, 0.0, 0.0, ]
    pos4 = [0.0, 0.0, 0.0, ]
    pos5 = [0.0, 0.0, 0.0, ]
    pos6 = [0.0, 0.0, 0.0, ]
    pos7 = [0.0, 0.0, 0.0, ]
    vel1 = [0.0, 0.0, 0.0, ]
    vel2 = [0.0, 0.0, 0.0, ]
    pog = [0.0, 0.0, 0.0, ]
    vog = [0.0, 0.0, 0.0, ]
    pob = [0.0, 0.0, 0.0, ]
    vob = [0.0, 0.0, 0.0, ]
    pos = [0.0, 0.0, 0.0, ]
    lighttime = [0.0]
    tdb = [0.0]
    peb = [0.0, 0.0, 0.0, ]
    veb = [0.0, 0.0, 0.0, ]
    pes = [0.0, 0.0, 0.0, ]
    ves = [0.0, 0.0, 0.0, ]
    oblm = [0.0]
    oblt = [0.0]
    eqeq = [0.0]
    psi = [0.0]
    eps = [0.0]
    ujd = tjd - (deltat/86400.0)
    error = get_earth(tjd, earth, tdb, peb, veb, pes, ves)
    if error:
        ra[0] = 0.0
        dec[0] = 0.0
        dis[0] = 0.0
        return error + 10
    earthtilt(tdb, oblm, oblt, eqeq, psi, eps)
    sidereal_time(ujd, 0.0, eqeq, gast)
    terra(location, gast, pos1, vel1)
    nutate(tdb, FN1, pos1, pos2)
    precession(tdb, pos2, T0, pog)
    nutate(tdb, FN1, vel1, vel2)
    precession(tdb, vel2, T0, vog)
    for j in range(3):
        pob[j] = peb[j] + pog[j]
        vob[j] = veb[j] + vog[j]
        pos[j] = pes[j] + pog[j]
    error = ephemeris(tdb, ss_object, BARYC, pos1, vel1)
    if error:
        ra[0] = 0.0
        dec[0] = 0.0
        dis[0] = 0.0
        return error
    bary_to_geo(pos1, pob, pos2, lighttime)
    dis[0] = lighttime*C
    t3 = tdb - lighttime
    # Do-while
    t2 = t3
    error = ephemeris(t2, ss_object, BARYC, pos1, vel1)
    if error:
        ra[0] = 0.0
        dec[0] = 0.0
        dis[0] = 0.0
        return error
    bary_to_geo(pos1, pob, pos2, lighttime)
    t3 = tdb - lighttime
    while fabs(t3 - t2) > 1.0e-8:
        t2 = t3
        error = ephemeris(t2, ss_object, BARYC, pos1, vel1)
        if error:
            ra[0] = 0.0
            dec[0] = 0.0
            dis[0] = 0.0
            return error
        bary_to_geo(pos1, pob, pos2, lighttime)
        t3 = tdb - lighttime
    # End do-while
    sun_field(pos2, pos, pos4)
    aberration(pos4, vob, lighttime, pos5)
    precession(T0, pos5, tdb, pos6)
    nutate(tdb, FN0, pos6, pos7)
    vector2radec(pos7, ra, dec)
    return error

def virtual_star(tjd, earth, star, ra, dec):
    error = 0
    pos1 = [0.0, 0.0, 0.0, ]
    vel1 = [0.0, 0.0, 0.0, ]
    pos2 = [0.0, 0.0, 0.0, ]
    pos3 = [0.0, 0.0, 0.0, ]
    pos4 = [0.0, 0.0, 0.0, ]
    pos5 = [0.0, 0.0, 0.0, ]
    tdb = [0.0]
    peb = [0.0, 0.0, 0.0, ]
    veb = [0.0, 0.0, 0.0, ]
    pes = [0.0, 0.0, 0.0, ]
    ves = [0.0, 0.0, 0.0, ]
    lighttime = [0.0]
    error = get_earth(tjd, earth, tdb, peb, veb, pes, ves)
    if error:
        ra[0] = 0.0
        dec[0] = 0.0
        return error
    starvectors(star, pos1, vel1)
    proper_motion(T0, pos1, vel1, tdb, pos2)
    bary_to_geo(pos2, peb, pos3, lighttime)
    sun_field(pos3, pes, pos4)
    aberration(pos4, veb, lighttime, pos5)
    vector2radec(pos5, ra, dec)
    return 0

def virtual_planet(tjd, ss_object, earth, ra, dec, dis):
    error = 0
    t2 = 0.0
    t3 = 0.0
    lighttime = [0.0]
    pos1 = [0.0, 0.0, 0.0, ]
    vel1 = [0.0, 0.0, 0.0, ]
    pos2 = [0.0, 0.0, 0.0, ]
    pos3 = [0.0, 0.0, 0.0, ]
    pos4 = [0.0, 0.0, 0.0, ]
    tdb = [0.0]
    peb = [0.0, 0.0, 0.0, ]
    veb = [0.0, 0.0, 0.0, ]
    pes = [0.0, 0.0, 0.0, ]
    ves = [0.0, 0.0, 0.0, ]
    oblm = [0.0]
    oblt = [0.0]
    eqeq = [0.0]
    psi = [0.0]
    eps = [0.0]
    error = get_earth(tjd, earth, tdb, peb, veb, pes, ves)
    if error:
        ra[0] = 0.0
        dec[0] = 0.0
        return error + 10
    earthtilt(tdb, oblm, oblt, eqeq, psi, eps)
    error = ephemeris(tdb, ss_object, BARYC, pos1, vel1)
    if error:
        ra[0] = 0.0
        dec[0] = 0.0
        return error
    bary_to_geo(pos1, peb, pos2, lighttime)
    dis[0] = lighttime*C
    t3 = tdb - lighttime
    # Do-while
    t2 = t3
    error = ephemeris(t2, ss_object, BARYC, pos1, vel1)
    if error:
        ra[0] = 0.0
        dec[0] = 0.0
        return error
    bary_to_geo(pos1, peb, pos2, lighttime)
    t3 = tdb - lighttime
    while fabs(t3 - t2) > 1.0e-8:
        t2 = t3
        error = ephemeris(t2, ss_object, BARYC, pos1, vel1)
        if error:
            ra[0] = 0.0
            dec[0] = 0.0
            return error
        bary_to_geo(pos1, peb, pos2, lighttime)
        t3 = tdb - lighttime
    # End do-while
    sun_field(pos2, pes, pos3)
    aberration(pos3, veb, lighttime, pos4)
    vector2radec(pos4, ra, dec)
    return 0

def local_star(tjd, earth, deltat, star, location, ra, dec):
    error = 0
    gast = [0.0]
    lighttime = [0.0]
    ujd = [0.0]
    pog = [0.0, 0.0, 0.0, ]
    vog = [0.0, 0.0, 0.0, ]
    pb = [0.0, 0.0, 0.0, ]
    vb = [0.0, 0.0, 0.0, ]
    ps = [0.0, 0.0, 0.0, ]
    vs = [0.0, 0.0, 0.0, ]
    pos1 = [0.0, 0.0, 0.0, ]
    vel1 = [0.0, 0.0, 0.0, ]
    pos2 = [0.0, 0.0, 0.0, ]
    vel2 = [0.0, 0.0, 0.0, ]
    pos3 = [0.0, 0.0, 0.0, ]
    pos4 = [0.0, 0.0, 0.0, ]
    pos5 = [0.0, 0.0, 0.0, ]
    tdb = [0.0]
    peb = [0.0, 0.0, 0.0, ]
    veb = [0.0, 0.0, 0.0, ]
    pes = [0.0, 0.0, 0.0, ]
    ves = [0.0, 0.0, 0.0, ]
    oblm = [0.0]
    oblt = [0.0]
    eqeq = [0.0]
    psi = [0.0]
    eps = [0.0]
    ujd = tjd - (deltat/86400.0)
    error = get_earth(tjd, earth, tdb, peb, veb, pes, ves)
    if error:
        ra[0] = 0.0
        dec[0] = 0.0
        return error
    earthtilt(tdb, oblm, oblt, eqeq, psi, eps)
    sidereal_time(ujd, 0.0, eqeq, gast)
    terra(location, gast, pos1, vel1)
    nutate(tdb, FN1, pos1, pos2)
    precession(tdb, pos2, T0, pog)
    nutate(tdb, FN1, vel1, vel2)
    precession(tdb, vel2, T0, vog)
    for j in range(3):
        pb[j] = peb[j] + pog[j]
        vb[j] = veb[j] + vog[j]
        ps[j] = pes[j] + pog[j]
        vs[j] = ves[j] + vog[j]
    starvectors(star, pos1, vel1)
    proper_motion(T0, pos1, vel1, tdb, pos2)
    bary_to_geo(pos2, pb, pos3, lighttime)
    sun_field(pos3, ps, pos4)
    aberration(pos4, vb, lighttime, pos5)
    vector2radec(pos5, ra, dec)
    return 0

def local_planet(tjd, ss_object, earth, deltat, location, ra, dec, dis):
    error = 0
    t2 = 0.0
    t3 = 0.0
    gast = [0.0]
    lighttime = [0.0]
    ujd = [0.0]
    pog = [0.0, 0.0, 0.0, ]
    vog = [0.0, 0.0, 0.0, ]
    pb = [0.0, 0.0, 0.0, ]
    vb = [0.0, 0.0, 0.0, ]
    ps = [0.0, 0.0, 0.0, ]
    vs = [0.0, 0.0, 0.0, ]
    pos1 = [0.0, 0.0, 0.0, ]
    vel1 = [0.0, 0.0, 0.0, ]
    pos2 = [0.0, 0.0, 0.0, ]
    vel2 = [0.0, 0.0, 0.0, ]
    pos3 = [0.0, 0.0, 0.0, ]
    pos4 = [0.0, 0.0, 0.0, ]
    tdb = [0.0]
    peb = [0.0, 0.0, 0.0, ]
    veb = [0.0, 0.0, 0.0, ]
    pes = [0.0, 0.0, 0.0, ]
    ves = [0.0, 0.0, 0.0, ]
    oblm = [0.0]
    oblt = [0.0]
    eqeq = [0.0]
    psi = [0.0]
    eps = [0.0]
    ujd = tjd - (deltat/86400.0)
    error = get_earth(tjd, earth, tdb, peb, veb, pes, ves)
    if error:
        ra[0] = 0.0
        dec[0] = 0.0
        return error + 10
    earthtilt(tdb, oblm, oblt, eqeq, psi, eps)
    sidereal_time(ujd, 0.0, eqeq, gast)
    terra(location, gast, pos1, vel1)
    nutate(tdb, FN1, pos1, pos2)
    precession(tdb, pos2, T0, pog)
    nutate(tdb, FN1, vel1, vel2)
    precession(tdb, vel2, T0, vog)
    for j in range(3):
        pb[j] = peb[j] + pog[j]
        vb[j] = veb[j] + vog[j]
        ps[j] = pes[j] + pog[j]
        vs[j] = ves[j] + vog[j]
    error = ephemeris(tdb, ss_object, BARYC, pos1, vel1)
    if error:
        ra[0] = 0.0
        dec[0] = 0.0
        dis[0] = 0.0
        return error
    bary_to_geo(pos1, pb, pos2, lighttime)
    dis[0] = lighttime*C
    t3 = tdb - lighttime
    # Do-while
    t2 = t3
    error = ephemeris(t2, ss_object, BARYC, pos1, vel1)
    if error:
        ra[0] = 0.0
        dec[0] = 0.0
        return error
    bary_to_geo(pos1, pb, pos2, lighttime)
    t3 = tdb - lighttime
    while fabs(t3 - t2) > 1.0e-8:
        t2 = t3
        error = ephemeris(t2, ss_object, BARYC, pos1, vel1)
        if error:
            ra[0] = 0.0
            dec[0] = 0.0
            return error
        bary_to_geo(pos1, pb, pos2, lighttime)
        t3 = tdb - lighttime
    # End do-while
    sun_field(pos2, ps, pos3)
    aberration(pos3, vb, lighttime, pos4)
    vector2radec(pos4, ra, dec)
    return 0

def astro_star(tjd, earth, star, ra, dec):
    error = 0
    lighttime = [0.0]
    pos1 = [0.0, 0.0, 0.0, ]
    vel1 = [0.0, 0.0, 0.0, ]
    pos2 = [0.0, 0.0, 0.0, ]
    pos3 = [0.0, 0.0, 0.0, ]
    tdb = [0.0]
    peb = [0.0, 0.0, 0.0, ]
    veb = [0.0, 0.0, 0.0, ]
    pes = [0.0, 0.0, 0.0, ]
    ves = [0.0, 0.0, 0.0, ]
    error = get_earth(tjd, earth, tdb, peb, veb, pes, ves)
    if error:
        ra[0] = 0.0
        dec[0] = 0.0
        return error
    starvectors(star, pos1, vel1)
    proper_motion(T0, pos1, vel1, tdb, pos2)
    bary_to_geo(pos2, peb, pos3, lighttime)
    vector2radec(pos3, ra, dec)
    return 0

def astro_planet(tjd, ss_object, earth, ra, dec, dis):
    error = 0
    t2 = 0.0
    t3 = 0.0
    lighttime = [0.0]
    pos1 = [0.0, 0.0, 0.0, ]
    vel1 = [0.0, 0.0, 0.0, ]
    pos2 = [0.0, 0.0, 0.0, ]
    tdb = [0.0]
    peb = [0.0, 0.0, 0.0, ]
    veb = [0.0, 0.0, 0.0, ]
    pes = [0.0, 0.0, 0.0, ]
    ves = [0.0, 0.0, 0.0, ]
    error = get_earth(tjd, earth, tdb, peb, veb, pes, ves)
    if error:
        ra[0] = 0.0
        dec[0] = 0.0
        return error + 10
    error = ephemeris(tdb, ss_object, BARYC, pos1, vel1)
    if error:
        ra[0] = 0.0
        dec[0] = 0.0
        dis[0] = 0.0
        return error
    bary_to_geo(pos1, peb, pos2, lighttime)
    dis[0] = lighttime*C
    t3 = tdb - lighttime
    # Do-while
    t2 = t3
    error = ephemeris(t2, ss_object, BARYC, pos1, vel1)
    if error:
        ra[0] = 0.0
        dec[0] = 0.0
        dis[0] = 0.0
        return error
    bary_to_geo(pos1, peb, pos2, lighttime)
    t3 = tdb - lighttime
    while fabs(t3 - t2) > 1.0e-8:
        t2 = t3
        error = ephemeris(t2, ss_object, BARYC, pos1, vel1)
        if error:
            ra[0] = 0.0
            dec[0] = 0.0
            dis[0] = 0.0
            return error
        bary_to_geo(pos1, peb, pos2, lighttime)
        t3 = tdb - lighttime
    # End do-while
    vector2radec(pos2, ra, dec)
    return 0

def mean_star(tjd, earth, ra, dec, mra, mdec):
    iter = 0
    newmra = [0.0]
    newdec = [0.0]
    oldmra = [0.0]
    olddec = [0.0]
    ra2 = [0.0]
    dec2 = [0.0]
    deltara = [0.0]
    deltadec = [0.0]
    tempstar = {
        "catalog"        : "CAT",
        "starname"       : "dummy",
        "starnumber"     : 0,
        "ra"             : 0.0,
        "dec"            : 0.0,
        "promora"        : 0.0,
        "promodec"       : 0.0,
        "parallax"       : 0.0,
        "radialvelocity" : 0.0,
    }
    newmra = fmod(ra, 24.0)
    if newmra < 0.0:
        newmra += 24.0
    newdec = dec
    # Do-while
    oldmra = newmra
    olddec = newdec
    tempstar["ra"] = oldmra
    tempstar["dec"] = olddec
    error = app_star(tjd, earth, tempstar, ra2, dec2)
    if error:
        mra[0] = 0.0
        mdec[0] = 0.0
        return error + 10
    deltara = ra2 - oldmra
    deltadec = dec2 - olddec
    if deltara < -12.0:
        deltara += 24.0
    if deltara > 12.0:
        deltara -= 24.0
    newmra = ra - deltara
    newdec = dec - deltadec
    if iter >= 20:
        mra[0] = 0.0
        mdec[0] = 0.0
        return 1
    else:
        iter += 1
    while (fabs(newmra - oldmra) > 1.0e-10) and \
          (fabs(newdec - olddec) > 1.0e-9):
        oldmra = newmra
        olddec = newdec
        tempstar["ra"] = oldmra
        tempstar["dec"] = olddec
        error = app_star(tjd, earth, tempstar, ra2, dec2)
        if error:
            mra[0] = 0.0
            mdec[0] = 0.0
            return error + 10
        deltara = ra2 - oldmra
        deltadec = dec2 - olddec
        if deltara < -12.0:
            deltara += 24.0
        if deltara > 12.0:
            deltara -= 24.0
        newmra = ra - deltara
        newdec = dec - deltadec
        if iter >= 20:
            mra[0] = 0.0
            mdec[0] = 0.0
            return 1
        else:
            iter += 1
    # End do-while
    mra[0] = newmra
    mdec[0] = newdec
    if mra[0] < 0.0:
        mra[0] += 24.0
    if mra[0] >= 24.0:
        mra[0] -= 24.0
    return 0

def sidereal_time(jd_high, jd_low, ee, gst):
    t_hi = 0.0
    t_lo = 0.0
    t = 0.0
    t2 = 0.0
    t3 = 0.0
    st = 0.0
    t_hi = (jd_high - T0)/36525.0
    t_lo = jd_low/36525.0
    t = t_hi + t_lo
    t2 = t*t
    t3 = t2*t
    st = (ee[0] - 6.2e-6*t3 + 0.093104*t2 + 67310.54841 +
          8640184.812866*t_lo + 3155760000.0*t_lo +
          8640184.812866*t_hi + 3155760000.0*t_hi)
    gst[0] = fmod((st/3600.0), 24.0)
    if gst[0] < 0.0:
        gst[0] += 24.0
    return

def pnsw(tjd, gast, x, y, vece, vecs):
    dummy = [0.0]
    secdiff = [0.0]
    v1 = [0.0, 0.0, 0.0, ]
    v2 = [0.0, 0.0, 0.0, ]
    v3 = [0.0, 0.0, 0.0, ]
    tdb = [0.0]
    if tjd != 0.0:
        tdb2tdt(tjd, dummy, secdiff)
        tdb = tjd + secdiff/86400.0
    if x == 0.0 and y == 0.0:
        for j in range(3):
            v1[j] = vece[j]
    else:
        wobble(x, y, vece, v1)
    if gast == 0.0:
        for j in range(3):
            v2[j] = v1[j]
    else:
        spin(gast, v1, v2)
    if tjd == 0.0:
        for j in range(3):
            vecs[j] = v2[j]
    else:
        nutate(tdb, FN1, v2, v3)
        precession(tdb, v3, T0, vecs)
    return

def spin(st, pos1, pos2):
    str = [0.0]
    cosst = [0.0]
    sinst = [0.0]
    XX = [0.0]
    yx = [0.0]
    xy = [0.0]
    YY = [0.0]
    str = st*15.0*DEG2RAD
    cosst = cos(str)
    sinst = sin(str)
    XX = cosst
    yx = -sinst
    xy = sinst
    YY = cosst
    pos2[0] = XX*pos1[0] + yx*pos1[1]
    pos2[1] = xy*pos1[0] + YY*pos1[1]
    pos2[2] = pos1[2]
    return

def wobble(x, y, pos1, pos2):
    xpole = [0.0]
    ypole = [0.0]
    zx = [0.0]
    zy = [0.0]
    xz = [0.0]
    yz = [0.0]
    xpole = x/RAD2SEC
    ypole = y/RAD2SEC
    zx = -xpole
    zy = ypole
    xz = xpole
    yz = -ypole
    pos2[0] = pos1[0] + zx*pos1[2]
    pos2[1] = pos1[1] + zy*pos1[2]
    pos2[2] = xz*pos1[0] + yz*pos1[1] + pos1[2]
    return

def terra(locale, st, pos, vel):
    df2 = [0.0]
    sinphi = [0.0]
    cosphi = [0.0]
    c = [0.0]
    s = [0.0]
    ach = [0.0]
    ash = [0.0]
    stlocl = [0.0]
    sinst = [0.0]
    cosst = [0.0]
    df2 = (1.0 - F)*(1.0 - F)
    sinphi = sin(locale["latitude"]*DEG2RAD)
    cosphi = cos(locale["latitude"]*DEG2RAD)
    c = 1.0/sqrt(cosphi*cosphi + df2*sinphi*sinphi)
    s = df2*c
    ach = EARTHRAD*c + (locale["height"]/1000.0)
    ash = EARTHRAD*s + (locale["height"]/1000.0)
    stlocl = (st[0]*15.0 + locale["longitude"])*DEG2RAD
    sinst = sin(stlocl)
    cosst = cos(stlocl)
    pos[0] = ach*cosphi*cosst
    pos[1] = ach*cosphi*sinst
    pos[2] = ash*sinphi
    vel[0] = -OMEGA*ach*cosphi*sinst
    vel[1] = OMEGA*ach*cosphi*cosst
    vel[2] = 0.0
    for j in range(3):
        pos[j] /= KMAU
        vel[j] /= KMAU
        vel[j] *= 86400.0
    return

# These variables were static doubles in earthtilt()
tjd_last_earthtilt = 0.0
t_earthtilt = 0.0
dp_earthtilt = [0.0]
de_earthtilt = [0.0]

def earthtilt(tjd, mobl, tobl, eq, dpsi, deps):
    global tjd_last_earthtilt
    global t_earthtilt
    global dp_earthtilt
    global de_earthtilt
    d_psi = [0.0]
    d_eps = [0.0]
    mean_obliq = [0.0]
    true_obliq = [0.0]
    eq_eq = [0.0]
    args = [0.0, 0.0, 0.0, 0.0, 0.0, ]
    t_earthtilt = (tjd[0] - T0)/36525.0
    if fabs(tjd[0] - tjd_last_earthtilt) > 1.0e-6:
        nutation_angles(t_earthtilt, dp_earthtilt, de_earthtilt)
    #  de_earthtilt = [-8.9202358306507428] -8.73336
    #  dp_earthtilt = [4.9305120849267148] 3.65856
    #   t_earthtilt = -0.0367282683089   OK
    d_psi = dp_earthtilt[0] + PSI_COR
    d_eps = de_earthtilt[0] + EPS_COR
    mean_obliq = (84381.4480 - 46.8150*t_earthtilt -
                  0.00059*t_earthtilt*t_earthtilt +
                  0.001813*t_earthtilt*t_earthtilt*t_earthtilt)
    true_obliq = mean_obliq + d_eps
    mean_obliq /= 3600.0
    true_obliq /= 3600.0
    fund_args(t_earthtilt, args)
    eq_eq = (d_psi*cos(mean_obliq*DEG2RAD) +
             (0.00264*sin(args[4]) + 0.000063*sin(2.0*args[4])))
    eq_eq /= 15.0
    tjd_last_earthtilt = tjd[0]
    dpsi[0] = d_psi
    deps[0] = d_eps
    eq[0] = eq_eq
    mobl[0] = mean_obliq
    tobl[0] = true_obliq
    return

def cel_pole(del_dpsi, del_deps):
    PSI_COR = del_dpsi
    EPS_COR = del_deps
    return

# These variables were static doubles in get_earth()
tjd_last_get_earth = 0.0
time1_get_earth = 0.0
peb_get_earth = [0.0, 0.0, 0.0]
veb_get_earth = [0.0, 0.0, 0.0]
pes_get_earth = [0.0, 0.0, 0.0]
ves_get_earth = [0.0, 0.0, 0.0]

def get_earth(tjd, earth, tdb, bary_earthp, bary_earthv,
              helio_earthp, helio_earthv):
    global tjd_last_get_earth
    global time1_get_earth
    global peb_get_earth
    global veb_get_earth
    global pes_get_earth
    global ves_get_earth
    error = 0
    earth_num = 0
    dummy = [0.0]
    secdiff = [0.0]
    if fabs(tjd - tjd_last_get_earth) > 1.0e-6:
        tdb2tdt(tjd, dummy, secdiff)
        time1_get_earth = tjd + secdiff[0]/86400.0
        earth_num = earth["number"]
        error = solarsystem(time1_get_earth, earth_num, BARYC,
                            peb_get_earth, veb_get_earth)
        if error:
            tjd_last_get_earth = 0.0
            return error
        error = solarsystem(time1_get_earth, earth_num, HELIOC,
                            pes_get_earth, ves_get_earth)
        if error:
            tjd_last_get_earth = 0.0
            return error
        tjd_last_get_earth = tjd
    tdb[0] = time1_get_earth
    for i in range(3):
        bary_earthp[i] = peb_get_earth[i]
        bary_earthv[i] = veb_get_earth[i]
        helio_earthp[i] = pes_get_earth[i]
        helio_earthv[i] = ves_get_earth[i]
    return error

def proper_motion(tjd1, pos, vel, tjd2, pos2):
    if ii(tjd1, list):
        TJD1 = tjd1[0]
    else:
        TJD1 = tjd1
    if ii(tjd2, list):
        TJD2 = tjd2[0]
    else:
        TJD2 = tjd2
    for j in range(3):
        pos2[j] = pos[j] + (vel[j]*(TJD2 - TJD1))
    return

def bary_to_geo(pos, earthvector, pos2, lighttime):
    sum_of_squares = [0.0]
    for j in range(3):
        pos2[j] = pos[j] - earthvector[j]
    sum_of_squares = pos2[0]*pos2[0] + pos2[1]*pos2[1] + pos2[2]*pos2[2]
    lighttime[0] = sqrt(sum_of_squares)/C
    return

def sun_field(pos, earthvector, pos2):
    f = 0.0
    p1mag = [0.0]
    pemag = [0.0]
    cosd = [0.0]
    sind = [0.0]
    b = [0.0]
    bm = [0.0]
    pqmag = [0.0]
    zfinl = [0.0]
    zinit = [0.0]
    xifinl = [0.0]
    xiinit = [0.0]
    delphi = [0.0]
    delphp = 0.0
    delp = [0.0]
    p1hat = [0.0, 0.0, 0.0, ]
    pehat = [0.0, 0.0, 0.0, ]
    c = (C*MAU)/86400.0
    p1mag = sqrt(pos[0]*pos[0] + pos[1]*pos[1] + + pos[2]*pos[2])
    pemag = sqrt(earthvector[0]*earthvector[0] +
                 earthvector[1]*earthvector[1] +
                 earthvector[2]*earthvector[2])
    for j in range(3):
        p1hat[j] = pos[j]/p1mag
        pehat[j] = earthvector[j]/pemag
    cosd = -pehat[0]*p1hat[0] - pehat[1]*p1hat[1] - pehat[2]*p1hat[2]
    if fabs(cosd) > 0.9999999999:
        for j in range(3):
            pos2[j] = pos[j]
    else:
        sind = sqrt(1.0 - cosd*cosd)
        b = pemag*sind
        bm = b*MAU
        pqmag = sqrt(p1mag*p1mag + pemag*pemag - 2.0*p1mag*pemag*cosd)
        zfinl = pemag*cosd
        zinit = -p1mag + zfinl
        xifinl = zfinl/b
        xiinit = zinit/b
        delphi = (2.0*GS/(bm*c*c)*(xifinl/sqrt(1.0 + pow(xifinl, 2.0))
                  - xiinit/sqrt(1.0 + pow(xiinit, 2.0))))
        delphp = delphi/(1.0 + (pemag/pqmag))
        f = delphp*p1mag/sind
        for j in range(3):
            delp = f*(cosd*p1hat[j] + pehat[j])
            pos2[j] = pos[j] + delp
    return 0

def aberration(pos, ve, lighttime, pos2):
    p1mag = [0.0]
    vemag = [0.0]
    beta = [0.0]
    dot = [0.0]
    cosd = [0.0]
    gammai = [0.0]
    p = [0.0]
    q = [0.0]
    r = [0.0]
    if lighttime == 0.0:
        p1mag = sqrt(mag3vec(pos))
        lighttime = p1mag/C
    else:
        p1mag = lighttime[0]*C
    vemag = sqrt(mag3vec(ve))
    beta = vemag/C
    dot = pos[0]*ve[0] + pos[1]*ve[1] + pos[2]*ve[2]
    cosd = dot/(p1mag*vemag)
    gammai = sqrt(1.0 - beta*beta)
    p = beta*cosd
    q = (1.0 + p/(1.0 + gammai))*lighttime[0]
    r = 1.0 + p
    for j in range(3):
        pos2[j] = (gammai*pos[j] + q*ve[j])/r
    return 0

def precession(tjd1, pos, tjd2, pos2):
    XX = 0.0
    yx = 0.0
    zx = 0.0
    xy = 0.0
    YY = 0.0
    zy = 0.0
    xz = 0.0
    yz = 0.0
    zz = 0.0
    t = 0.0
    t1 = 0.0
    t02 = 0.0
    t2 = 0.0
    t3 = 0.0
    zeta0 = 0.0
    zee = 0.0
    theta = 0.0
    cz0 = 0.0
    sz0 = 0.0
    ct = 0.0
    st = 0.0
    cz = 0.0
    sz = 0.0
    if ii(tjd1, list):
        TJD1 = tjd1[0]
    else:
        TJD1 = tjd1
    if ii(tjd2, list):
        TJD2 = tjd2[0]
    else:
        TJD2 = tjd2
    t = (TJD1 - T0)/36525.0
    t1 = (TJD2 - TJD1)/36525.0
    t02 = t*t
    t2 = t1*t1
    t3 = t2*t1
    zeta0 = ((2306.2181 + 1.39656*t - 0.000139*t02)*t1 + (0.30188 -
             0.000344*t)*t2 + 0.017998*t3)
    zee = ((2306.2181 + 1.39656*t - 0.000139*t02)*t1 + (1.09468 +
           0.000066*t)*t2 + 0.018203*t3)
    theta = ((2004.3109 - 0.85330*t - 0.000217*t02)*t1 +
             (-0.42665 - 0.000217*t)*t2 - 0.041833*t3)
    zeta0 /= RAD2SEC
    zee /= RAD2SEC
    theta /= RAD2SEC
    cz0 = cos(zeta0)
    sz0 = sin(zeta0)
    ct = cos(theta)
    st = sin(theta)
    cz = cos(zee)
    sz = sin(zee)
    XX = cz0*ct*cz - sz0*sz
    yx = -sz0*ct*cz - cz0*sz
    zx = -st*cz
    xy = cz0*ct*sz + sz0*cz
    YY = -sz0*ct*sz + cz0*cz
    zy = -st*sz
    xz = cz0*st
    yz = -sz0*st
    zz = ct
    pos2[0] = XX*pos[0] + yx*pos[1] + zx*pos[2]
    pos2[1] = xy*pos[0] + YY*pos[1] + zy*pos[2]
    pos2[2] = xz*pos[0] + yz*pos[1] + zz*pos[2]
    return

def nutate(tjd, fn, pos, pos2):
    cobm = 0.0
    sobm = 0.0
    cobt = 0.0
    sobt = 0.0
    cpsi = 0.0
    spsi = 0.0
    XX = 0.0
    yx = 0.0
    zx = 0.0
    xy = 0.0
    YY = 0.0
    zy = 0.0
    xz = 0.0
    yz = 0.0
    zz = 0.0
    oblm = [0.0]
    oblt = [0.0]
    eqeq = [0.0]
    psi = [0.0]
    eps = [0.0]
    earthtilt(tjd, oblm, oblt, eqeq, psi, eps)
    cobm = cos(oblm[0]*DEG2RAD)
    sobm = sin(oblm[0]*DEG2RAD)
    cobt = cos(oblt[0]*DEG2RAD)
    sobt = sin(oblt[0]*DEG2RAD)
    cpsi = cos(psi[0]/RAD2SEC)
    spsi = sin(psi[0]/RAD2SEC)
    XX = cpsi
    yx = -spsi*cobm
    zx = -spsi*sobm
    xy = spsi*cobt
    YY = cpsi*cobm*cobt + sobm*sobt
    zy = cpsi*sobm*cobt - cobm*sobt
    xz = spsi*sobt
    yz = cpsi*cobm*sobt - sobm*cobt
    zz = cpsi*sobm*sobt + cobm*cobt
    if not fn:
        pos2[0] = XX*pos[0] + yx*pos[1] + zx*pos[2]
        pos2[1] = xy*pos[0] + YY*pos[1] + zy*pos[2]
        pos2[2] = xz*pos[0] + yz*pos[1] + zz*pos[2]
    else:
        pos2[0] = XX*pos[0] + xy*pos[1] + xz*pos[2]
        pos2[1] = yx*pos[0] + YY*pos[1] + yz*pos[2]
        pos2[2] = zx*pos[0] + zy*pos[1] + zz*pos[2]
    return 0

def nutation_angles(t, longnutation, obliqnutation):
    clng = [1.0, 1.0, -1.0, -1.0, 1.0, -1.0, -1.0, -1.0, -1.0, -1.0,
            -1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, -1.0, 1.0, 1.0,
            -1.0, 1.0, -1.0, 1.0, -1.0, -1.0, -1.0, 1.0, -1.0, -1.0,
            1.0, -1.0, 1.0, 2.0, 2.0, 2.0, 2.0, 2.0, -2.0, 2.0, 2.0,
            2.0, 3.0, -3.0, -3.0, 3.0, -3.0, 3.0, -3.0, 3.0, 4.0, 4.0,
            -4.0, -4.0, 4.0, -4.0, 5.0, 5.0, 5.0, -5.0, 6.0, 6.0, 6.0,
            -6.0, 6.0, -7.0, 7.0, 7.0, -7.0, -8.0, 10.0, 11.0, 12.0,
            -13.0, -15.0, -16.0, -16.0, 17.0, -21.0, -22.0, 26.0, 29.0,
            29.0, -31.0, -38.0, -46.0, 48.0, -51.0, 58.0, 59.0, 63.0,
            63.0, -123.0, 129.0, -158.0, -217.0, -301.0, -386.0,
            -517.0, 712.0, 1426.0, 2062.0, -2274.0, -13187.0, -171996.0]
    clngx = [0.1, -0.1, 0.1, 0.1, 0.1, 0.1, 0.2, -0.2, -0.4, 0.5, 1.2,
             -1.6, -3.4, -174.2]
    cobl = [1.0, 1.0, 1.0, -1.0, -1.0, -1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
            -1.0, 1.0, -1.0, 1.0, -1.0, -1.0, -1.0, 1.0, -1.0, 1.0,
            1.0, -1.0, -2.0, -2.0, -2.0, 3.0, 3.0, -3.0, 3.0, 3.0,
            -3.0, 3.0, 3.0, -3.0, 3.0, 3.0, 5.0, 6.0, 7.0, -7.0, 7.0,
            -8.0, 9.0, -10.0, -12.0, 13.0, 16.0, -24.0, 26.0, 27.0,
            32.0, -33.0, -53.0, 54.0, -70.0, -95.0, 129.0, 200.0,
            224.0, -895.0, 977.0, 5736.0, 92025.0]
    coblx = [-0.1, -0.1, 0.3, 0.5, -0.5, -0.6, -3.1, 8.9]
    nav1 = [0, 0, 1, 0, 2, 1, 3, 0, 4, 0]
    nav2 = [0, 0, 0, 5, 1, 1, 3, 3, 4, 4]
    nav = [2, 0, 1, 1, 5, 2, 2, 0, 2, 1, 0, 3, 2, 5, 8, 1, 17, 8, 1,
           18, 0, 2, 0, 8, 0, 1, 3, 2, 1, 8, 0, 17, 1, 1, 15, 1, 2,
           21, 1, 1, 2, 8, 2, 0, 29, 1, 21, 2, 2, 1, 29, 2, 0, 9, 2,
           5, 4, 2, 0, 4, 0, 1, 9, 2, 1, 4, 0, 2, 9, 2, 2, 4, 1, 14,
           44, 2, 0, 45, 2, 5, 44, 2, 50, 0, 1, 36, 2, 2, 5, 45, 1,
           37, 2, 2, 1, 45, 2, 1, 44, 2, 53, 1, 2, 8, 4, 1, 40, 3, 2,
           17, 4, 2, 0, 64, 1, 39, 8, 2, 27, 4, 1, 50, 18, 1, 21, 47,
           2, 44, 3, 2, 44, 8, 2, 45, 8, 1, 46, 8, 0, 67, 2, 1, 5, 74,
           1, 0, 74, 2, 50, 8, 1, 5, 78, 2, 17, 53, 2, 53, 8, 2, 0,
           80, 2, 0, 81, 0, 7, 79, 1, 7, 81, 2, 1, 81, 2, 24, 44, 1,
           1, 79, 2, 27, 44]
    llng = [57, 25, 82, 34, 41, 66, 33, 36, 19, 88, 18, 104, 93, 84, 47,
            28, 83, 86, 69, 75, 89, 30, 58, 73, 46, 77, 23, 32, 59, 72,
            31, 16, 74, 22, 98, 38, 62, 96, 37, 35, 6, 76, 85, 51, 26,
            10, 13, 63, 105, 52, 102, 67, 99, 15, 24, 14, 3, 100, 65,
            11, 55, 68, 20, 87, 64, 95, 27, 60, 61, 80, 91, 94, 12, 43,
            71, 42, 97, 70, 7, 49, 29, 2, 5, 92, 50, 78, 56, 17, 48, 40,
            90, 8, 39, 54, 81, 21, 103, 53, 45, 101, 0, 1, 9, 44, 79, 4]
    llngx = [81, 7, 97, 0, 39, 40, 9, 44, 45, 103, 101, 79, 1, 4]
    lobl = [51, 98, 17, 21, 5, 2, 63, 105, 38, 52, 102, 62, 96, 37, 35,
            76, 36, 88, 85, 104, 93, 84, 83, 67, 99, 8, 68, 100, 60, 61,
            91, 87, 64, 80, 95, 65, 55, 94, 43, 97, 0, 71, 70, 42, 49,
            92, 50, 78, 56, 90, 48, 40, 39, 54, 1, 81, 103, 53, 45, 101,
            9, 44, 79, 4]
    loblx = [53, 1, 103, 9, 44, 101, 79, 4]
    a = [0.0, 0.0, 0.0, 0.0, 0.0, ]
    angle = 0.0
    cc = 0.0
    ss1 = 0.0
    cs = 0.0
    sc = 0.0
    c = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
         0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
         0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
         0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
         0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
         0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
         0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
         0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
         0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    s = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
         0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
         0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
         0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
         0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
         0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
         0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
         0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
         0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    lng = 0.0
    lngx = 0.0
    obl = 0.0
    oblx = 0.0
    fund_args(t, a)
    i = 0
    for ii in range(0, 10, 2):
        angle = a[nav1[ii]]*(nav1[1 + ii] + 1)
        c[i] = cos(angle)
        s[i] = sin(angle)
        i += 1
    i = 5
    for ii in range(0, 10, 2):
        i1 = nav2[ii]
        i2 = nav2[1 + ii]
        c[i] = c[i1]*c[i2] - s[i1]*s[i2]
        s[i] = s[i1]*c[i2] + c[i1]*s[i2]
        i += 1
    i = 10
    for ii in range(0, 183, 3):
        iop = nav[ii]
        i1 = nav[1 + ii]
        i2 = nav[2 + ii]
        if iop == 0:
            c[i] = c[i1]*c[i2] - s[i1]*s[i2]
            s[i] = s[i1]*c[i2] + c[i1]*s[i2]
            i += 1
        elif iop == 1:
            c[i] = c[i1]*c[i2] + s[i1]*s[i2]
            s[i] = s[i1]*c[i2] - c[i1]*s[i2]
            i += 1
        elif iop == 2:
            cc = c[i1]*c[i2]
            ss1 = s[i1]*s[i2]
            sc = s[i1]*c[i2]
            cs = c[i1]*s[i2]
            c[i] = cc - ss1
            s[i] = sc + cs
            i += 1
            c[i] = cc + ss1
            s[i] = sc - cs
            i += 1
        if iop == 3:
            break
    lng = 0.0
    for i in range(0, 106):
        lng += clng[i]*s[llng[i]]
    lngx = 0.0
    for i in range(0, 14):
        lngx += clngx[i]*s[llngx[i]]
    obl = 0.0
    for i in range(0, 64):
        obl += cobl[i]*c[lobl[i]]
    oblx = 0.0
    for i in range(0, 8):
        oblx += coblx[i]*c[loblx[i]]
    longnutation[0] = (lng + t*lngx)/10000.0
    obliqnutation[0] = (obl + t*oblx)/10000.0
    return 0

def fund_args(t, a):
    a[0] = (2.3555483935439407 + t*(8328.691422883896 + t *
            (1.517951635553957e-4 + 3.1028075591010306e-7*t)))
    a[1] = (6.240035939326023 + t*(628.3019560241842 + t *
            (-2.7973749400020225e-6 - 5.817764173314431e-8*t)))
    a[2] = (1.6279019339719611 + t*(8433.466158318453 + t *
            (-6.427174970469119e-5 + 5.332950492204896e-8*t)))
    a[3] = (5.198469513579922 + t*(7771.377146170642 + t *
            (-3.340851076525812e-5 + 9.211459941081184e-8*t)))
    a[4] = (2.1824386243609943 + t*(-33.75704593375351 + t *
            (3.614285992671591e-5 + 3.878509448876288e-8*t)))
    for i in range(5):
        a[i] = fmod(a[i], TWOPI)
        if a[i] < 0.0:
            a[i] += TWOPI
    return

def vector2radec(pos, ra, dec):
    xyproj = [0.0]
    xyproj = sqrt(pos[0]*pos[0] + pos[1]*pos[1])
    if xyproj == 0.0 and pos[2] == 0:
        ra[0] = 0.0
        dec[0] = 0.0
        return 1
    elif xyproj == 0.0:
        ra[0] = 0.0
        if pos[2] < 0.0:
            dec[0] = -90.0
        else:
            dec[0] = 90.0
        return 2
    else:
        ra[0] = atan2(pos[1], pos[0])*RAD2SEC/54000.0
        dec[0] = atan2(pos[2], xyproj)*RAD2SEC/3600.0
        if ra[0] < 0.0:
            ra[0] += 24.0
    return 0

def radec2vector(ra, dec, dist, vector):
    vector[0] = dist[0]*cos(DEG2RAD*dec[0])*cos(DEG2RAD*15.0*ra[0])
    vector[1] = dist[0]*cos(DEG2RAD*dec[0])*sin(DEG2RAD*15.0*ra[0])
    vector[2] = dist[0]*sin(DEG2RAD*dec[0])
    return

def starvectors(star, pos, vel):
    paralx = [0.0]
    dist = [0.0]
    r = [0.0]
    d = [0.0]
    cra = [0.0]
    sra = [0.0]
    cdc = [0.0]
    sdc = [0.0]
    pmr = [0.0]
    pmd = [0.0]
    rvl = [0.0]
    paralx = star["parallax"]
    if star["parallax"] <= 0.0:
        paralx = 1.0e-7
    dist = RAD2SEC/paralx
    r = (star["ra"])*15.0*DEG2RAD
    d = (star["dec"])*DEG2RAD
    cra = cos(r)
    sra = sin(r)
    cdc = cos(d)
    sdc = sin(d)
    pos[0] = dist*cdc*cra
    pos[1] = dist*cdc*sra
    pos[2] = dist*sdc
    pmr = star["promora"]*15.0*cdc/(paralx*36525.0)
    pmd = star["promodec"]/(paralx*36525.0)
    rvl = star["radialvelocity"]*86400.0/KMAU
    vel[0] = -pmr*sra - pmd*sdc*cra + rvl*cdc*cra
    vel[1] = pmr*cra - pmd*sdc*sra + rvl*cdc*sra
    vel[2] = pmd*cdc + rvl*sdc
    return

def tdb2tdt(tdb, tdtjd, secdiff):
    ecc = 0.01671022
    rev = 1296000.0
    tdays = [0.0]
    m = [0.0]
    l = [0.0]
    lj = [0.0]
    e = [0.0]
    tdays = tdb - T0
    m = (357.51716 + 0.985599987*tdays)*3600.0
    l = (280.46435 + 0.985609100*tdays)*3600.0
    lj = (34.40438 + 0.083086762*tdays)*3600.0
    m = fmod(m, rev)/RAD2SEC
    l = fmod(l, rev)/RAD2SEC
    lj = fmod(lj, rev)/RAD2SEC
    e = m + ecc*sin(m) + 0.5*ecc*ecc*sin(2.0*m)
    secdiff[0] = 1.658e-3*sin(e) + 20.73e-6*sin(l - lj)
    tdtjd[0] = tdb - secdiff[0]/86400.0
    return

def set_body(Type, number, name, cel_obj):
    error = 0
    cel_obj["type"] = 0
    cel_obj["number"] = 0
    cel_obj["name"] = "  "
    if Type < 0 or Type > 1:
        return 1
    else:
        cel_obj["type"] = Type
    if Type == 0:
        if number <= 0 or number > 11:
            return 2
        elif number <= 0:
            return 2
    cel_obj["number"] = number
    cel_obj["name"] = name
    return error

def ephemeris(tjd, cel_obj, origin, pos, vel):
    mp_name = ""
    err = [0]
    mp_number = 0
    error = 0
    ss_number = 0
    i = 0
    posvel = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    sun_pos = [0.0, 0.0, 0.0]
    sun_vel = [0.0, 0.0, 0.0]
    if origin < 0 or origin > 1:
        return 1
    if cel_obj["type"] == 0:
        ss_number = cel_obj["number"]
        error = solarsystem(tjd, ss_number, origin, pos, vel)
        if error:
            error += 10
    elif cel_obj["type"] == 1:
        mp_number = cel_obj["number"]
        name_len = len(cel_obj["name"])
        mp_name = cel_obj["name"]
        posvel = readeph(mp_number, mp_name, tjd, err)
        if err[0]:
            return 20 + err[0]
        if origin == 0:
            error = solarsystem(tjd, 10, 0, sun_pos, sun_vel)
            if error:
                return 10 + err[0]
            for i in range(3):
                posvel[i] += sun_pos[i]
                posvel[i + 3] += sun_vel[i]
        for i in range(3):
            pos[i] = posvel[i]
            vel[i] = posvel[i + 3]
    else:
        error = 2
    return error

def make_cat_entry(catalog, star_name, star_num, ra, dec, pm_ra,
                   pm_dec, parallax, rad_vel, star):
    for i in range(4):
        star["catalog"][i] = catalog[i]
        if catalog[i] == '':
            break
    star["catalog"][i] = ''
    for i in range(51):
        star["starname"][i] = star_name[i]
        if star_name[i] == '':
            break
    star["starname"][i] = ''
    star["starnumber"] = star_num
    star["ra"] = ra
    star["dec"] = dec
    star["promora"] = pm_ra
    star["promodec"] = pm_dec
    star["parallax"] = parallax
    star["radialvelocity"] = rad_vel
    return

def transform_hip(hipparcos, fk5):
    epoch_hip = 2448349.0625
    epoch_fk5 = 2451545.0000
    scratch = {  # Create an empty catalog entry
        "catalog"        : "",
        "starname"       : "",
        "starnumber"     : 0,
        "ra"             : 0.0,
        "dec"            : 0.0,
        "promora"        : 0.0,
        "promodec"       : 0.0,
        "parallax"       : 0.0,
        "radialvelocity" : 0.0,
    }
    scratch["starname"] = hipparcos["starname"]
    scratch["starnumber"] = hipparcos["starnumber"]
    scratch["dec"] = hipparcos["dec"]
    scratch["radialvelocity"] = hipparcos["radialvelocity"]
    scratch["catalog"] = "SCR"
    scratch["ra"] = hipparcos["ra"]/15.0
    scratch["promora"] = \
        hipparcos["promora"]/(150.0*cos(hipparcos["dec"]*DEG2RAD))
    scratch["promodec"] = hipparcos["promodec"]/10.0
    scratch["parallax"] = hipparcos["parallax"]/1000.0
    transform_cat(1, epoch_hip, scratch, epoch_fk5, "FK5", fk5)
    return

def transform_cat(option, date_incat, incat, date_newcat, newcat_id, newcat):
    jd_incat = [0.0]
    jd_newcat = [0.0]
    paralx = [0.0]
    dist = [0.0]
    r = [0.0]
    d = [0.0]
    cra = [0.0]
    sra = [0.0]
    cdc = [0.0]
    sdc = [0.0]
    pos1 = [0.0, 0.0, 0.0, ]
    term1 = [0.0]
    pmr = [0.0]
    pmd = [0.0]
    rvl = [0.0]
    vel1 = [0.0, 0.0, 0.0, ]
    pos2 = [0.0, 0.0, 0.0, ]
    vel2 = [0.0, 0.0, 0.0, ]
    xyproj = [0.0]
    if date_incat < 10000.0:
        jd_incat = T0 + (date_incat - 2000.0)*365.25
    else:
        jd_incat = date_incat
    if date_newcat < 10000.0:
        jd_newcat = T0 + (date_newcat - 2000.0)*365.25
    else:
        jd_newcat = date_newcat
    paralx = incat["parallax"]
    if paralx <= 0.0:
        paralx = 1.0e-7
    dist = RAD2SEC/paralx
    r = incat["ra"]*54000.0/RAD2SEC
    d = incat["dec"]*3600.0/RAD2SEC
    cra = cos(r)
    sra = sin(r)
    cdc = cos(d)
    sdc = sin(d)
    pos1[0] = dist*cdc*cra
    pos1[1] = dist*cdc*sra
    pos1[2] = dist*sdc
    term1 = paralx*36525.0
    pmr = incat["promora"]*15.0*cdc/term1
    pmd = incat["promodec"]/term1
    rvl = incat["radialvelocity"]*86400.0/KMAU
    vel1[0] = -pmr*sra - pmd*sdc*cra + rvl*cdc*cra
    vel1[1] = pmr*cra - pmd*sdc*sra + rvl*cdc*sra
    vel1[2] = pmd*cdc + rvl*sdc
    if option == 1 or option == 3:
        for j in range(3):
            pos2[j] = pos1[j] + vel1[j]*(jd_newcat - jd_incat)
            vel2[j] = vel1[j]
    else:
        for j in range(3):
            pos2[j] = pos1[j]
            vel2[j] = vel1[j]
    if option == 2 or option == 3:
        for j in range(3):
            pos1[j] = pos2[j]
            vel1[j] = vel2[j]
        precession(jd_incat, pos1, jd_newcat, pos2)
        precession(jd_incat, vel1, jd_newcat, vel2)
    xyproj = sqrt(pos2[0]*pos2[0] + pos2[1]*pos2[1])
    r = atan2(pos2[1], pos2[0])
    d = atan2(pos2[2], xyproj)
    newcat["ra"] = r*RAD2SEC/54000.0
    newcat["dec"] = d*RAD2SEC/3600.0
    if newcat["ra"] < 0.0:
        newcat["ra"] += 24.0
    dist = sqrt(pos2[0]*pos2[0] + pos2[1]*pos2[1] + pos2[2]*pos2[2])
    paralx = RAD2SEC/dist
    newcat["parallax"] = paralx
    cra = cos(r)
    sra = sin(r)
    cdc = cos(d)
    sdc = sin(d)
    pmr = -vel2[0]*sra + vel2[1]*cra
    pmd = -vel2[0]*cra*sdc - vel2[1]*sra*sdc + vel2[2]*cdc
    rvl = vel2[0]*cra*cdc + vel2[1]*sra*cdc + vel2[2]*sdc
    newcat["promora"] = pmr*paralx*36525.0/(15.0*cdc)
    newcat["promodec"] = pmd*paralx*36525.0
    newcat["radialvelocity"] = rvl*KMAU/86400.0
    if newcat["parallax"] <= 1.01e-7:
        newcat["parallax"] = 0.0
        newcat["radialvelocity"] = incat["radialvelocity"]
    strcpy(newcat["catalog"], newcat_id)
    strcpy(newcat["starname"], incat["starname"])
    newcat["starnumber"] = incat["starnumber"]
    return

def equ2hor(tjd, deltat, x, y, location, ra, dec, ref_option,
            zd, az, rar, decr):
    ujd = [0.0]
    dummy = [0.0]
    secdiff = [0.0]
    tdb = [0.0]
    mobl = [0.0]
    tobl = [0.0]
    ee = [0.0]
    dpsi = [0.0]
    deps = [0.0]
    gast = [0.0]
    sinlat = [0.0]
    coslat = [0.0]
    sinlon = [0.0]
    coslon = [0.0]
    sindc = [0.0]
    cosdc = [0.0]
    sinra = [0.0]
    cosra = [0.0]
    uze = [0.0, 0.0, 0.0, ]
    une = [0.0, 0.0, 0.0, ]
    uwe = [0.0, 0.0, 0.0, ]
    uz = [0.0, 0.0, 0.0, ]
    un = [0.0, 0.0, 0.0, ]
    uw = [0.0, 0.0, 0.0, ]
    p = [0.0, 0.0, 0.0, ]
    pz = [0.0]
    pn = [0.0]
    pw = [0.0]
    proj = [0.0]
    zd0 = [0.0]
    zd1 = [0.0]
    refr = [0.0]
    cosr = [0.0]
    prlen = [0.0]
    rlen = [0.0]
    pr = [0.0, 0.0, 0.0, ]
    ujd = tjd - (deltat/86400.0)
    tdb2tdt(tjd, dummy, secdiff)
    tdb = tjd + secdiff/86400.0
    earthtilt(tdb, mobl, tobl, ee, dpsi, deps)
    sidereal_time(ujd, 0.0, ee, gast)
    rar[0] = ra
    decr[0] = dec
    sinlat = sin(location["latitude"]*DEG2RAD)
    coslat = cos(location["latitude"]*DEG2RAD)
    sinlon = sin(location["longitude"]*DEG2RAD)
    coslon = cos(location["longitude"]*DEG2RAD)
    sindc = sin(dec*DEG2RAD)
    cosdc = cos(dec*DEG2RAD)
    sinra = sin(ra*15.0*DEG2RAD)
    cosra = cos(ra*15.0*DEG2RAD)
    uze[0] = coslat*coslon
    uze[1] = coslat*sinlon
    uze[2] = sinlat
    une[0] = -sinlat*coslon
    une[1] = -sinlat*sinlon
    une[2] = coslat
    uwe[0] = sinlon
    uwe[1] = -coslon
    uwe[2] = 0.0
    pnsw(0.0, gast, x, y, uze, uz)
    pnsw(0.0, gast, x, y, une, un)
    pnsw(0.0, gast, x, y, uwe, uw)
    p[0] = cosdc*cosra
    p[1] = cosdc*sinra
    p[2] = sindc
    pz = p[0]*uz[0] + p[1]*uz[1] + p[2]*uz[2]
    pn = p[0]*un[0] + p[1]*un[1] + p[2]*un[2]
    pw = p[0]*uw[0] + p[1]*uw[1] + p[2]*uw[2]
    proj = sqrt(pn*pn + pw*pw)
    if proj > 0.0:
        az[0] = -atan2(pw, pn)*RAD2DEG
    if az[0] < 0.0:
        az[0] += 360.0
    if az[0] >= 360.0:
        az[0] -= 360.0
    zd[0] = atan2(proj, pz)*RAD2DEG
    if ref_option != 0:
        zd0 = zd[0]
        # Do-while
        zd1 = zd[0]
        refr = refract(location, ref_option, zd[0])
        zd[0] = zd0 - refr
        while fabs(zd[0] - zd1) > 5.0e-5:
            zd1 = zd[0]
            refr = refract(location, ref_option, zd[0])
            zd[0] = zd0 - refr
        # End do-while
        if refr > 0.0 and zd[0] > 0.01:
            cosr = cos(refr*DEG2RAD)
            prlen = sin(zd0*DEG2RAD)/sin(zd[0]*DEG2RAD)
            rlen = sqrt(1.0 + prlen*prlen - 2.0*prlen*cosr)
            for j in range(3):
                pr[j] = (p[j] + rlen*uz[j])/prlen
            proj = sqrt(pr[0]*pr[0] + pr[1]*pr[1])
            if proj > 0.0:
                rar[0] = atan2(pr[1], pr[0])*RAD2DEG/15.0
            if rar[0] < 0.0:
                rar[0] += 24.0
            if rar[0] >= 24.0:
                rar[0] -= 24.0
            decr[0] = atan2(pr[2], proj)*RAD2DEG
    return

def refract(location, ref_option, zd_obs):
    s = 9.1e3
    refr = [0.0]
    p = [0.0]
    t = [0.0]
    h = [0.0]
    r = [0.0]
    if zd_obs < 0.1 or zd_obs > 91.0:
        refr = 0.0
    else:
        if ref_option == 2:
            p = location["pressure"]
            t = location["temperature"]
        else:
            p = 1010.0*exp(-location["height"]/s)
            t = 10.0
        h = 90.0 - zd_obs
        r = 0.016667/tan((h + 7.31/(h + 4.4))*DEG2RAD)
        refr = r*(0.28*p/(t + 273.0))
    return refr

def julian_date(year, month, day, hour):
    jd12h = (day - 32075 + 1461*(year + 4800 + (month - 14)/12)/4 +
             367*(month - 2 - (month - 14)/12*12)/12 -
             3*((year + 4900 + (month - 14)/12)/100)/4)
    return jd12h - 0.5 + hour/24.0

def cal_date(tjd, year, month, day, hour):
    djd = [0.0]
    djd = tjd + 0.5
    jd = djd
    hour[0] = fmod(djd, 1.0)*24.0
    k = jd + 68569
    n = 4*k/146097
    k = k - (146097*n + 3)/4
    m = 4000*(k + 1)/1461001
    k = k - 1461*m/4 + 31
    month[0] = (80*k/2447)
    day[0] = (k - 2447*month[0]/80)
    k = month[0]/11
    month[0] = month[0] + 2 - 12*k
    year[0] = (100*(n - 49) + m + k)
    return
