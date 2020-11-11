# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 10:25:49 2019

@author: polsterc16

information taken from NASA JPL
https://ssd.jpl.nasa.gov/txt/aprx_pos_planets.pdf
["Grundlagen der Ephemeridenrechung", O. Montenbruck]

"""
def keplerEquation2(m, e, tol=1e-12):
    import math
    
    E = m
    z = 0
    while (m - z) > tol:
        z = E - e * math.sin(E)
        E = E + (m - z)
        

    return E

def keplerEquation(m, e, tol=1e-12, iterMax=8):
    ''' Kepler Equation for mean anomaly M in rad and eccentricity e 
        returns E in rad '''
    
    #auflösung der keplergleichung nach newtonverfahren
    #siehe ["Grundlagen der Ephemeridenrechung", O. Montenbruck] p 56
    
    import math
    
    E = m  # E0 zu beginn (gilt nur für i<0.8, immer erfüllt)
    
    for k in range(iterMax):
        dE = (m - ( E - e*math.sin(E) ) ) / ( 1 - e*math.cos(E) )
        E = E + dE
        if (dE <= tol) and (dE >= -tol): 
            # abbrechen, wenn änderung innerhalb von toleranz
            break
    
    return E #eccentric anomaly in rad


def getCurrentKeplerElem(planet:str, julianCty:float):
    ''' get Kepler elements for given planet and julian date '''
    
    import math
    
    if not(planet in Planetlist):
        # nur für gültige planetennamen
        return None
    
    temp = Keplerelements[planet]
    
    returnDict = {}
    
    # a: semi major axis in au
    returnDict['a'] = (temp['a1'] + temp['a2']*julianCty) 
    
    # e: eccentricity
    returnDict['e'] = (temp['e1'] + temp['e2']*julianCty) 
    
    # I: inclination in degrees (conv to rad)
    returnDict['i'] = math.radians(temp['i1'] + temp['i2']*julianCty)
    
    # L: mean longitude in degrees (conv to rad)
    returnDict['L'] = math.radians(temp['L1'] + temp['L2']*julianCty)
    
    # \omega_: longitude of perihelion in degrees (conv to rad)
    returnDict['w_'] = math.radians(temp['w_1'] + temp['w_2']*julianCty)
    
    # \OMEGA: longitude of ascending node in degrees (conv to rad)
    returnDict['W'] = math.radians(temp['W1'] + temp['W2']*julianCty)
    
    # \omega: argument of perihelion in degrees (conv to rad)
    returnDict['w'] = returnDict['w_'] - returnDict['W']
    
    # \omega: mean anomaly in degrees (conv to rad)
    returnDict['M'] = returnDict['L'] - returnDict['w_']
    returnDict['M'] = (returnDict['M'])%(2*math.pi)
    
    
    return returnDict



Planetlist = [
        'mercury', 'venus', 'earth', 'mars', 'jupiter', 
        'saturn', 'uranus', 'neptune', 'pluto']


Keplerelements = {}
# Kepler elements are given in value at J2000 and rate of change over 
# a century (cty). A cty is 100 years or 36525 days long.
#     elem(today) = elem(J2000) + elem_dot * T
#     with T = ( julianDate(today) - julianDate(J2000) )/36525
#     julianDate(J2000) = 2451545.0
Keplerelements['mercury'] = {
        'a1':       0.38709927, # semi major axis in au
        'a2':       0.00000037, # rate of major axis in au/cty
        'e1':       0.20563593, # eccentricity
        'e2':       0.00001906, # rate of eccentricity in 1/cty
        'i1':       7.00497902, # inclination in degrees
        'i2':      -0.00594749, # rate of inclination in degrees/cty
        'L1':     252.25032350, # mean longitude in degrees
        'L2':  149472.67411175, # rate of mean longitude in degrees/cty
        'w_1':     77.45779628, # longitude of perihelion in degrees
        'w_2':      0.16047689, # rate of longitude of perihel. in degrees/cty
        'W1':      48.33076593, # longitude of ascending node in degrees
        'W2':      -0.12534081} # rate of longitude of AN in degrees/cty

Keplerelements['venus'] = {
        'a1':       0.72333566,
        'a2':       0.00000390,
        'e1':       0.00677672,
        'e2':      -0.00004107,
        'i1':       3.39467605,
        'i2':      -0.00078890,
        'L1':     181.97909950,
        'L2':   58517.81538729,
        'w_1':    131.60246718,
        'w_2':      0.00268329,
        'W1':      76.67984255,
        'W2':      -0.27769418}

Keplerelements['earth'] = {
        'a1':       1.00000261,
        'a2':       0.00000562,
        'e1':       0.01671123,
        'e2':      -0.00004392,
        'i1':      -0.00001531,
        'i2':      -0.01294668,
        'L1':     100.46457166,
        'L2':   35999.37244981,
        'w_1':    102.93768193,
        'w_2':      0.32327364,
        'W1':       0.00000000,
        'W2':       0.00000000}

Keplerelements['mars'] = {
        'a1':       1.52371034,
        'a2':       0.00001847,
        'e1':       0.09339410,
        'e2':       0.00007882,
        'i1':       1.84969142,
        'i2':      -0.00813131,
        'L1':      -4.55343205,
        'L2':   19140.30268499,
        'w_1':    -23.94362959,
        'w_2':      0.44441088,
        'W1':      49.55953891,
        'W2':      -0.29257343}

Keplerelements['jupiter'] = {
        'a1':       5.20288700,
        'a2':      -0.00011607,
        'e1':       0.04838624,
        'e2':      -0.00013253,
        'i1':       1.30439695,
        'i2':      -0.00183714,
        'L1':      34.39644051,
        'L2':    3034.74612775,
        'w_1':     14.72847983,
        'w_2':      0.21252668,
        'W1':     100.47390909,
        'W2':       0.20469106}

Keplerelements['saturn'] = {
        'a1':       9.53667594,
        'a2':      -0.00125060,
        'e1':       0.05386179,
        'e2':      -0.00050991,
        'i1':       2.48599187,
        'i2':       0.00193609,
        'L1':      49.95424423,
        'L2':    1222.49362201,
        'w_1':     92.59887831,
        'w_2':     -0.41897216,
        'W1':     113.66242448,
        'W2':      -0.28867794}

Keplerelements['uranus'] = {
        'a1':      19.18916464,
        'a2':      -0.00196176,
        'e1':       0.04725744,
        'e2':      -0.00004397,
        'i1':       0.77263783,
        'i2':      -0.00242939,
        'L1':     313.23810451,
        'L2':     428.48202785,
        'w_1':    170.95427630,
        'w_2':      0.40805281,
        'W1':      74.01692503,
        'W2':       0.04240589}

Keplerelements['neptune'] = {
        'a1':      30.06992276,
        'a2':       0.00026291,
        'e1':       0.00859048,
        'e2':       0.00005105,
        'i1':       1.77004347,
        'i2':       0.00035372,
        'L1':     -55.12002969,
        'L2':     218.45945325,
        'w_1':     44.96476227,
        'w_2':     -0.32241464,
        'W1':     131.78422574,
        'W2':      -0.00508664}

Keplerelements['pluto'] = {
        'a1':      39.48211675,
        'a2':      -0.00031596,
        'e1':       0.24882730,
        'e2':       0.00005170,
        'i1':      17.14001206,
        'i2':       0.00004818,
        'L1':     238.92903833,
        'L2':     145.20780515,
        'w_1':    224.06891629,
        'w_2':     -0.04062942,
        'W1':     110.30393684,
        'W2':      -0.01183482}

