# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 12:46:00 2019

@author: polsterc16

==============================================================================
 LICENCE INFORMATION
==============================================================================
This Software uses Code (spg4) provided by "Brandon Rhodes" under
the "MIT License". For more Information see "licence-info.txt".

Diese Software benutzt Code (spg4), welcher von "Brandon Rhodes" unter
der "MIT License" zur Verfuegung gestellt wird. Fuer weitere Information
siehe "licence-info.txt".
==============================================================================

"""

import math
import numpy as np
import sgp4.ext as sgp4_ext



def Rx(angle=0):
    sin_ = math.sin(angle)
    cos_ = math.cos(angle)
    
    return np.matrix([[1,       0,      0],
                      [0,       +cos_,  +sin_],
                      [0,       -sin_,  +cos_]])


def Ry(angle=0):
    sin_ = math.sin(angle)
    cos_ = math.cos(angle)
    
    return np.matrix([[+cos_,   0,      -sin_],
                      [0,       +1,     0],
                      [+sin_,   -0,     +cos_]])


def Rz(angle=0):
    sin_ = math.sin(angle)
    cos_ = math.cos(angle)
    
    return np.matrix([[+cos_,   +sin_,  0],
                      [-sin_,   +cos_,  0],
                      [0,       0,      1]])

    
def eps_deg(julCty:float):
    ''' Eklipticschiefe Epsilon in degrees '''
    T = julCty
    arg = [23.43929111, 
           -46.8150,
           -0.00059,
           0.001813]
    
    returnVal = arg[0] + (arg[1]+(arg[2]+(arg[3])*T)*T)*T/3600
    return returnVal

    
def eps_rad(julCty:float):
    ''' Eklipticschiefe Epsilon in radianten '''
    import math
    return math.radians( eps_deg(julCty) )
    
    
def Nutation(julCty:float):
    ''' Rotationsmatrix fuer korrektur bzgl Nutation '''
    from math import sin, cos
    
    import EPH_PLANET_Planetlist as Planetlist
    import EPH_MOON_Moonlist as Moonlist
    
    # hole länge des aufsteigenden knoten
    earth = Planetlist.getCurrentKeplerElem("earth",julCty)
    W = earth["W"] # in radianten
    
    
    meanArgRad = Moonlist.mean_args_rad(julCty)
    l_ = meanArgRad["l_"] #in rad
    F =  meanArgRad["F"]  #in rad
    D =  meanArgRad["D"]  #in rad
    
    eps = eps_rad(julCty) # in rad
    
    
    psiArg = [-17.200,  +0.206, +0.143, -1.319, -0.227] # in arcsec
    epsArg = [+9.203,   -0.090, +0,     +0.574, +0.098] # in arcsec
    sin_ = [sin(W), sin(2*W), sin(l_), sin( 2*(F-D+W) ), sin( 2*(F+W) )]
    cos_ = [cos(W), cos(2*W), cos(l_), cos( 2*(F-D+W) ), cos( 2*(F+W) )]
    
    sumPsi,sumEps = [],[]
    for k in range(len(sin_)):
        sumPsi.append(psiArg[k]*sin_[k])
        sumEps.append(epsArg[k]*cos_[k])
    
    # summe entspricht den Delta-Werten von Eps und Psi
    # wandle summe (arcsec) in radianten um
    dPsi = math.radians( sum(sumPsi)/3600 ) # in rad
    dEps = math.radians( sum(sumEps)/3600 ) # in rad
    
    # gebe fertige roationsmatrix für Nutation zurück
    return Rx(-eps-dEps)*Rz(dPsi)*Rx(eps)
            

def vector_add(v1=[0,0,0], v2=[0,0,0]):
    """ v1 + v2 """
    return [v1[0]+v2[0], v1[1]+v2[1], v1[2]+v2[2]]

def vector_sub(v1=[0,0,0], v2=[0,0,0]):
    """ v1 - v2 """
    return [v1[0]-v2[0], v1[1]-v2[1], v1[2]-v2[2]]

def vector_cross(v1=[0,0,0], v2=[0,0,0]):
    """ v1 x v2 """
    temp=[0,0,0]
    sgp4_ext.cross(v1,v2,temp)
    return temp

def vector_dot(v1=[0,0,0], v2=[0,0,0]):
    """ v1 • v2 """
    return sgp4_ext.dot(v1,v2)

def vector_angle(v1=[1,0,0], v2=[1,0,0]):
    return sgp4_ext.angle(v1,v2)

def vector_abs(v=[0,0,0]):
    return sgp4_ext.mag(v)



def sin_deg(angle_deg):
    """ returns sin for angle in degrees """
    return math.sin(math.radians(angle_deg))

def cos_deg(angle_deg):
    """ returns cos for angle in degrees """
    return math.cos(math.radians(angle_deg))

def tan_deg(angle_deg):
    """ returns tan for angle in degrees """
    return math.tan(math.radians(angle_deg))


def asin_deg(value):
    """ returns asin as angle in degrees """
    return math.degrees(math.asin(value) )

def acos_deg(value):
    """ returns acos as angle in degrees """
    return math.degrees(math.acos(value) )

def atan_deg(value):
    """ returns atan as angle in degrees """
    return math.degrees(math.atan(value) )

def atan2_deg(val1,val2):
    """ returns atan2 as angle in degrees """
    return math.degrees(math.atan2(val1,val2) )



def deg_deg2dms(d:float):
    if d<0:
        vz="-"
        d=-d
    else:
        vz="+"
        
    D = int(d)
    m = 60*(d-D)
    M = int(m)
    s = 60*(m-M)
    
    return "{0}{1:02} {2:02} {3:05.2f} dms".format(vz,D,M,s)

    

def deg_deg2hms(d:float):
    d=d%360
    
    h=d/360*24
    H = int(h)
    m = 60*(h-H)
    M = int(m)
    s = 60*(m-M)
    
    return "{0:02} {1:02} {2:05.2f} hms".format(H,M,s)
