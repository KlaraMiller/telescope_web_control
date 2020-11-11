# -*- coding: utf-8 -*-
"""
Created on Sun Feb 24 10:05:35 2019

@author: polsterc16

"""


#moon_L0        # mittlere Laenge des Mondes
#moon_l         # mittlere Anomalie des Mondes
#moon_lApos     # mittlere Anomalie der Sonne
#moon_F         # mittlerer Winkelbstand des Mondes vom aufsteigenden Knoten
#moon_D         # mittlere Elongation des Mondes 


#""" Mittlere Winkel fuer Mondberechnung
# Daten kommen von "Astronomie mit dem Personal Computer", 
#   beziehen sich auf J2000 (JD:2451545)

# Format: |a0|a1|a2| mit x = a0 + a1*T + a2*T*T     
#   (T = julianische jahrhunderte seit J2000 - alle angaben in Grad!!!)
# MOON_MEAN_ARGUMENTS_CALC 

# mittlere Argumente in deg
mean_args_deg = {
        "L0":   [218.31617, 481267.88088, -4.06/3600.0], 
        "l":    [134.96292, 477198.86753, 33.25/3600.0],
        "l_":   [357.52543, 35999.04944,  -0.58/3600.0],
        "F":    [93.27283,  483202.01873, -11.56/3600.0],
        "D":    [297.85027, 445267.11135, -5.15/3600.0]}

# mittlere argumente: langperiodische schwankungen in arcsec
mean_args_long_periodic_arcsec = {
        "L0":   [0.84, 0.31, 14.27, 7.26,  0.28,  0.24,  0], 
        "l":    [2.94, 0.31, 14.27, 9.34,  1.12,  0.83,  0], 
        "l_":   [-6.4, 0,    0,     0,     0,     -1.89, 0],
        "F":    [0.21, 0.31, 14.27, -88.7, -15.3, 0.24,  -1.86],
        "D":    [7.24, 0.31, 14.27, 7.26,  0.28,  2.13,  0],
        
        "sArg1": [0.19833, 0.27869,  0.16827,  0.34734,  0.10498,  0.42681,  0.14943],
        "sArg2": [0.05611, 0.04508, -0.36903, -5.37261, -5.37899, -0.41855, -5.37511]}


def get_mean_args_deg(julianCty:float):
    T = julianCty
    returnDict = {}
    
    for key in mean_args_deg:
        # mittlere argumente
        meanArg = mean_args_deg[key]
        mean = (meanArg[0] + meanArg[1]*T + meanArg[2]*T*T )
        
        returnDict[key] = mean 
    
    return returnDict


def get_mean_args_rad(julianCty:float):
    import math
    
    meanArgsDeg = get_mean_args_deg(julianCty)
    returnDict = {}
    
    for key in meanArgsDeg:
        returnDict[key] = math.radians(meanArgsDeg[key])
    
    return returnDict





def get_mean_args_long_deg(julianCty:float):
    import math
    T = julianCty
    
    mean = get_mean_args_deg(T)
    
    sinArg1 = mean_args_long_periodic_arcsec['sArg1']
    sinArg2 = mean_args_long_periodic_arcsec['sArg2']
    sinList = [0]*len(sinArg1)
    returnDict = {}
    
    for i,v in enumerate(sinArg1):
        # berechne sin für langperiodische schwankungen
        # sin = sin( 2*pi * (arg1 + arg2*T) )
        sinList[i] = math.sin(2*math.pi * (sinArg1[i] + sinArg2[i]*T))
    
    
    for key in mean_args_deg:
        
        # langperiodische schwankungen
        longPerArg = mean_args_long_periodic_arcsec[key]
        
        longPerSum = []
        for i,v in enumerate(longPerArg):
            # alle deltaWerte mit sin mulitpliziert und in liste geschrieben
            longPerSum.append(sinList[i]*longPerArg[i])
        
        # liste aufaddiert
        longPer = sum(longPerSum)/3600
        
        # schreibe ergebnis der argumente in returnDict
        returnDict[key] = mean[key] + longPer
    
    return returnDict



def addThe(c1,s1,c2,s2,cs:dict):
    cs["c"] = c1*c2 - s1*s2
    cs["s"] = s1*c2 + c1*s2

def cosSum(a1,a2):
    import math
    c1 = math.cos(a1)
    s1 = math.sin(a1)
    c2 = math.cos(a2)
    s2 = math.sin(a2)
    
    myDict={}
    
    addThe(c1,s1,c2,s2,myDict)
    
    return myDict["c"]









