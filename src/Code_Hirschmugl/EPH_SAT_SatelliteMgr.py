# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 10:49:27 2019

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


# ---------------------------------------------------
# IMPORTS


import sys
import os
import datetime
import math


import EPH_CORE_TimeSpaceMgr as TSMgr
import EPH_ADD_math_helper as math_helper
from EPH_ADD_wgs72_complete import wgs72_complete

import sgp4.earth_gravity as sgp4_earth_gravity
import sgp4.io as sgp4_io

from EPH_SAT_norad_lists import sat_list
from EPH_SAT_norad_lists import __relative_path as sat_rel_path
#import norad_lists



# ---------------------------------------------------
# ---------------------------------------------------
# VARIABLES



# ---------------------------------------------------
# ---------------------------------------------------
# CLASSES

class SatelliteMgr:
    ''' Encapsulation of sap4 class for satellites.
        provides additional functinos '''

    def __init__(self, TSMgrObj, sat_id):
        ''' Create a satellite by its ID,
            with reference to a TimeSpaceMgr object
            (preferably one for all satellites). '''
        
        # default values
        self._successID =       False
        self._successTSMgr =    False
        

        self._TSMgr = TSMgrObj   # reference to the global TSMgr
        # check if the TimeSpaceMgrObj is a TSMgr object
        self._successTSMgr = (type(self._TSMgr)==TSMgr.TimeSpaceMgr)
        

        self._sat = self._createSatByID(sat_id)
        
        # indicator for successful extraction of TLE
        # returns true, if the "_sat" attribute/member variable is NOT "None"
        #   or to put it another way:
        #   "True, if the satellite (corresponding to the ID) was found"
        self._successID = (self._sat != None)
        
        # "_time_previous"
        #   Purpose: keep track, whether sat position has to be recalculated
        tnow = self._TSMgr.time_get_utcDateTime()   #utctime from TSMgr
        tdelta = datetime.timedelta(1)              # 1 day
        # previous time is initialized as one day in the past
        self._time_previous = tnow - tdelta


        # inital values
        self._geocentr_equator = {}
        self._geocentr_equator["cartesian"] = {
                "pos":[0,0,0],"vel":[0,0,0]}
        self._geocentr_equator["spherical"] = {
                "pos":{"Ra":0,"De":0,"R":0},
                "vel":{"Ra":0,"De":0} }
        
        self._topocentr_equator = {}
        self._topocentr_equator["cartesian"] = {
                "pos":[0,0,0],"vel":[0,0,0]}
        self._topocentr_equator["spherical"] = {
                "pos":{"Ra":0,"De":0,"R":0},
                "vel":{"Ra":0,"De":0} }
        
        
    # ---------------------------------------------------

    def __get_successID(self):
        ''' returns whether the Satellite was created successfully '''
        return self._successID;

    def __get_successTSMgr(self):
        ''' returns whether the Satellite has valid TSMgr member  variable '''
        return self._successTSMgr;

    def get_success(self):
        ''' returns whether all init actions were successful '''
        return all(
                [self.__get_successID(), 
                 self.__get_successTSMgr()]
                );
    # ---------------------------------------------------



    # ---------------------------------------------------
    # CALCULATIONS

    def _check_time_for_calc(self, utcTime):
        
        # check TIME
        if(utcTime==None):
            # if None given, then use utcNow
            self._TSMgr.time_set_utcNow()
        else:
            # otherwise use given time and update TSMgr to it
            self._TSMgr.time_set_utcDateTime(utcTime)
            
        
        time_now = self._TSMgr.time_get_utcDateTime()
        
        
        # check for time difference
        if(time_now != self._time_previous):
            # time difference: calculate everything for new time
            self._calc_all()    # start new calculation
            self._time_previous = time_now  # update time_prev
    # -------------






    def _calc_all(self):
        """ calculates everything from TSMgr utctime. 
            To be called by '_check_time_for_calc' """
        
        self._propagate()
        self._calc_geoc_equator_spherical()
        self._calc_topoc_equator_spherical()
    
    # -------------
    
    
    
    
    
    
    def _calc_topoc_equator_spherical(self):
        ''' computes [Position Angles] and [Angular Velocities] 
            ([Right Ascencion] and [Declination]) 
            in [TOPOcentric Equatorial Coordinate System] of the Sat
            relavtive to the telescope.
            (Center = [surface position],
            References: [Earth axis] / [Equatorial plane] and
                the direction to the [Vernal equinox].) '''
        
        # Berechnung is aehnlich zu GEOzentrisch spherical,
        #   JEDOCH ist (x,y,z) der vektor vom telescop zum satelliten
        #   und fuer (x',y',z') muss x',y' vom teleskop berechnet werden
        
        
        # -------------
        # get cartesian corrdinates
        xp,yp,zp =  self._topocentr_equator["cartesian"]["vel"]
        x,y,z =     self._topocentr_equator["cartesian"]["pos"]
        r =         math_helper.vector_abs((x,y,z))
        
        
        # -------------
        # calc spherical coordinates
        
        # -------------
        # ANGULAR POSITION
        
        Ra = math_helper.atan2_deg(y,x)
        De = math_helper.asin_deg(z/r)

        self._topocentr_equator["spherical"]["pos"]["Ra"] = Ra
        self._topocentr_equator["spherical"]["pos"]["De"] = De
        self._topocentr_equator["spherical"]["pos"]["R"] =  r
        
        # -------------
        # ANGULAR VELOCITY
        
        # x,y,z = f(t)
        # r = f(t) = sqrt(x^2+y^2+z^2)
        
        # Ra = atan(y/x)
        # d( atan(y(t)/x(t)) )/dt = (x*y' - y*x')/(x^2+y^2)   in rad/s
        Ra_dot = math.degrees( (x*yp - y*xp)/(x**2+y**2) )
        
        # De = asin(z/r)
        # d( asin(z(t)/r(t)) )/dt = 
        #       z' - z/(r^2) * (x*x'+y*y'+z*z')
        #   = ------------------------------    in rad/s
        #           sqrt(r^2 - z^2)
        De_dot = math.degrees(
                ( zp - z/(r**2)*(x*xp+y*yp+z*zp) ) / math.sqrt(r**2 - z**2)
                ) 
        
        self._topocentr_equator["spherical"]["vel"]["Ra"] = Ra_dot
        self._topocentr_equator["spherical"]["vel"]["De"] = De_dot
    # -------------
    
    
    def _calc_geoc_equator_spherical(self):
        ''' computes [Position Angles] and [Angular Velocities] 
            ([Right Ascencion] and [Declination]) 
            in [GEOcentric Equatorial Coordinate System] of the Sat
            relavtive to the telescope.
            (Center = [Earth Center],
            References: [Earth axis] / [Equatorial plane] and
                the direction to the [Vernal equinox].) '''
        
        # -------------
        # get cartesian corrdinates
        xp,yp,zp =  self._geocentr_equator["cartesian"]["vel"]
        x,y,z =     self._geocentr_equator["cartesian"]["pos"]
        r =         math_helper.vector_abs((x,y,z))
        
        
        # -------------
        # calc spherical coordinates
        
        # -------------
        # ANGULAR POSITION
        
        Ra = math_helper.atan2_deg(y,x)
        De = math_helper.asin_deg(z/r)

        self._geocentr_equator["spherical"]["pos"]["Ra"] = Ra
        self._geocentr_equator["spherical"]["pos"]["De"] = De
        self._geocentr_equator["spherical"]["pos"]["R"] =  r
        
        # -------------
        # ANGULAR VELOCITY
        
        # x,y,z = f(t)
        # r = f(t) = sqrt(x^2+y^2+z^2)
        
        # Ra = atan(y/x)
        # d( atan(y(t)/x(t)) )/dt = (x*y' - y*x')/(x^2+y^2)   in rad/s
        Ra_dot = math.degrees( (x*yp - y*xp)/(x**2+y**2) )
        
        # De = asin(z/r)
        # d( asin(z(t)/r(t)) )/dt = 
        #       z' - z/(r^2) * (x*x'+y*y'+z*z')
        #   = ------------------------------    in rad/s
        #           sqrt(r^2 - z^2)
        De_dot = math.degrees(
                ( zp - z/(r**2)*(x*xp+y*yp+z*zp) ) / math.sqrt(r**2 - z**2)
                )
        
        self._geocentr_equator["spherical"]["vel"]["Ra"] = Ra_dot
        self._geocentr_equator["spherical"]["vel"]["De"] = De_dot
    # -------------
    
    
    
    def _propagate(self):
        ''' Calculates [Position] and [Velocity] in [Cartesian Coordinate 
            System] for the [GEOcentric AND TOPOcentric Equatorial System] 
            for the statet utc time.
            (Center = [Earth Center], [Surface position],
            References: [Earth axis] / [Equatorial plane] and
                the direction to the [Vernal equinox].) '''

        # get utc time of TSMgr object
        t = self._TSMgr.time_get_utcDateTime()


        # -------------
        # calc pos and vel for GEOcentr cartesian coordins of SAT
        
        pos_sat, vel_sat = self._sat.propagate(t.year, t.month, t.day, 
                                               t.hour, t.minute,
                                               t.second + t.microsecond*1e-6)
        
        self._geocentr_equator["cartesian"]["pos"] = pos_sat
        self._geocentr_equator["cartesian"]["vel"] = vel_sat
    
    
        # -------------
        # calc pos and vel for GEOcentr cartesian coordins of TELE
        
        #get geocentr pos of tele
        pos_tele =  self._TSMgr.pos_get_ECI()  
        
        #calc geocentr vel of tele
        # Formel fuer kartesiches koordinatensystem: 
        #   drehender pfeil in xy ebene mit w = winkelgeschw.
        w = wgs72_complete["omega_RadPerSec"]   # winkelgeschw in xy ebene
        vel_tele=[0,0,0]
        vel_tele[0] =  w * pos_tele[1]  # x' =   w*y
        vel_tele[1] = -w * pos_tele[0]  # y' = - w*x
        vel_tele[2] = 0                 # z' = 0    # (erdrotation in z) = 0
        
        
        # -------------
        # calc pos and vel for TOPOcentr cartesian coordins of SAT(fromTELE)
        
        #topocentr pos of sat = [geocentr pos of sat] - [geocentr pos of tele]
        pos_topo = math_helper.vector_sub(pos_sat, pos_tele)
        vel_topo = math_helper.vector_sub(vel_sat, vel_tele)
        
        self._topocentr_equator["cartesian"]["pos"] = tuple(pos_topo)
        self._topocentr_equator["cartesian"]["vel"] = tuple(vel_topo)
    # -------------
    
    
    # ---------------------------------------------------
    # GET FUNCTIONS
    
    # simplified get functions for telescope
    
#        self._topocentr_equator["spherical"] = {
#                "pos":{"Ra":0,"De":0,"R":0},
#                "vel":{"Ra":0,"De":0} }
#        
    
    def getPos(self):
        ''' returns dict of {'Ra', 'De'} in degrees (or None if error) '''
        if self.get_success():
            self._check_time_for_calc(None)
            return {"Ra": self._topocentr_equator["spherical"]["pos"]["Ra"], 
                    "De": self._topocentr_equator["spherical"]["pos"]["De"]}
        else:
            return None
    
    def getPosRa(self):
        ''' returns number of 'Ra' in degrees (or None if error) '''
        if self.get_success():
            self._check_time_for_calc(None)
            return self._topocentr_equator["spherical"]["pos"]["Ra"]
        else:
            return None
    
    def getPosDe(self):
        ''' returns number of 'De' in degrees (or None if error) '''
        if self.get_success():
            self._check_time_for_calc(None)
            return self._topocentr_equator["spherical"]["pos"]["De"]
        else:
            return None
    
    
    # Geocentr equator
    
    #   Cartesian
    
    def get_pos_geoc_equator_cartesian(self, utcTimeDate=None):
        ''' returns position in km in [Cartesian Coordinates] in the 
            [GEOcentric Equatorial Coordinate System] of the Sat. '''

        self._check_time_for_calc(utcTimeDate)
        return self._geocentr_equator["cartesian"]["pos"]
    
    def get_vel_geoc_equator_cartesian(self, utcTimeDate=None):
        ''' returns velocity in km/sec [Cartesian Coordinates] in the 
            [GEOcentric Equatorial Coordinate System] of the Sat. '''

        self._check_time_for_calc(utcTimeDate)
        return self._geocentr_equator["cartesian"]["vel"]    
    
    def get_all_geoc_equator_cartesian(self, utcTimeDate=None):
        ''' returns position and velocity in [Cartesian Coordinates] 
            in the [GEOcentric Equatorial Coordinate System] of the Sat. '''

        self._check_time_for_calc(utcTimeDate)
        return self._geocentr_equator["cartesian"]
    
    #   spherical
    
    def get_pos_geoc_equator_spherical(self, utcTimeDate=None):
        ''' returns [Angle Position] in degrees and [Radius] in km 
            in [Spherical Coordinates] 
            in the [GEOcentric Equatorial Coordinate System] of the Sat. '''

        self._check_time_for_calc(utcTimeDate)
        return self._geocentr_equator["spherical"]["pos"]
    
    def get_vel_geoc_equator_spherical(self, utcTimeDate=None):
        ''' returns [Angule Speeds] in degrees/sec in [Spherical Coordinates] 
            in the [GEOcentric Equatorial Coordinate System] of the Sat. '''

        self._check_time_for_calc(utcTimeDate)
        return self._geocentr_equator["spherical"]["vel"]
    
    def get_all_geoc_equator_spherical(self, utcTimeDate=None):
        ''' returns [Angle Position] and [Angule Speeds] in 
            [Spherical Coordinates] in the [GEOcentric Equatorial 
            Coordinate System] of the Sat. '''

        self._check_time_for_calc(utcTimeDate)
        return self._geocentr_equator["spherical"]
    
    #   ALL
    
    def get_all_geoc_equator(self, utcTimeDate=None):
        ''' returns cartesian and spherical coordinates in the
            [GEOcentric Equatorial Coordinate System] of the Sat. '''

        self._check_time_for_calc(utcTimeDate)
        return self._geocentr_equator
    
    
    
    # TOPOcentric Equatorial
    
    #   Cartesian
    
    def get_pos_topoc_equator_cartesian(self, utcTimeDate=None):
        ''' returns position in km in [Cartesian Coordinates] in the 
            [TOPOcentric Equatorial Coordinate System] of the Sat. '''

        self._check_time_for_calc(utcTimeDate)
        return self._topocentr_equator["cartesian"]["pos"]
    
    def get_vel_topoc_equator_cartesian(self, utcTimeDate=None):
        ''' returns velocity in km/sec [Cartesian Coordinates] in the 
            [TOPOcentric Equatorial Coordinate System] of the Sat. '''

        self._check_time_for_calc(utcTimeDate)
        return self._topocentr_equator["cartesian"]["vel"]    
    
    def get_all_topoc_equator_cartesian(self, utcTimeDate=None):
        ''' returns position and velocity in [Cartesian Coordinates] 
            in the [TOPOcentric Equatorial Coordinate System] of the Sat. '''

        self._check_time_for_calc(utcTimeDate)
        return self._topocentr_equator["cartesian"]
    
    #   spherical
    
    def get_pos_topoc_equator_spherical(self, utcTimeDate=None):
        ''' returns [Angle Position] in degrees and [Radius] in km 
            in [Spherical Coordinates] 
            in the [TOPOcentric Equatorial Coordinate System] of the Sat. '''

        self._check_time_for_calc(utcTimeDate)
        return self._topocentr_equator["spherical"]["pos"]
    
    def get_vel_topoc_equator_spherical(self, utcTimeDate=None):
        ''' returns [Angule Speeds] in degrees/sec in [Spherical Coordinates] 
            in the [TOPOcentric Equatorial Coordinate System] of the Sat. '''

        self._check_time_for_calc(utcTimeDate)
        return self._topocentr_equator["spherical"]["vel"]
    
    def get_all_topoc_equator_spherical(self, utcTimeDate=None):
        ''' returns [Angle Position] and [Angule Speeds] in 
            [Spherical Coordinates] in the [TOPOcentric Equatorial 
            Coordinate System] of the Sat. '''

        self._check_time_for_calc(utcTimeDate)
        return self._topocentr_equator["spherical"]
    
    #   ALL
    
    def get_all_topoc_equator(self, utcTimeDate=None):
        ''' returns cartesian and spherical coordinates in the
            [TOPOcentric Equatorial Coordinate System] of the Sat. '''

        self._check_time_for_calc(utcTimeDate)
        return self._topocentr_equator
    
    
    


        







    def _createSatByID(self,identifier,file=None):
        ''' creates a satellite by its ID
            code provided by david vallado (twoline2rv) '''

        n,l1,l2 = getSatTLE(identifier,file)

        if(l1==None):
            # If no TLE with that ID is found
            self._successID = False
            return None
        else:
            sat = sgp4_io.twoline2rv(l1,l2,sgp4_earth_gravity.wgs72)
            sat.satname = n
        return sat



    def get_str_satname(self):
        # returns ID and name of sat as string
        return "Satellite: ["+str(self.get_satnum())+"] - "+str(
                self.get_satname())

    def get_str_epoch(self):
        # returns epoch in "year days"
        return "Epoch: "+str(self.get_epochyr())+" "+str(self.get_epochdays())



    def get_satname(self):
        # Name of Satellite given in the TLE file.
        return self._sat.satname

    def get_satnum(self):
        #'satnum'
        #Unique satellite number given in the TLE file.
        return self._sat.satnum

    def get_epochyr(self):
        #'epochyr'
        #Full four-digit year of this element set's epoch moment.
        return self._sat.epochyr

    def get_epochdays(self):
        #'epochdays'
        #Fractional days into the year of the epoch moment.
        return self._sat.epochdays

    def get_jdsatepoch(self):
        #'jdsatepoch'
        #Julian date of the epoch (computed from 'epochyr' and 'epochdays').
        return self._sat.jdsatepoch

    def get_ndot(self):
        #'ndot'
        #First time derivative of the mean motion (ignored by SGP4).
        return self._sat.ndot

    def get_nddot(self):
        #'nddot'
        #Second time derivative of the mean motion (ignored by SGP4).
        return self._sat.nddot

    def get_bstar(self):
        #'bstar'
        #Ballistic drag coefficient B* in inverse earth radii.
        return self._sat.bstar

    def get_inclo(self):
        #'inclo'
        #Inclination in radians.
        return self._sat.inclo

    def get_nodeo(self):
        #'nodeo'
        #Right ascension of ascending node in radians.
        return self._sat.nodeo

    def get_ecco(self):
        #'ecco'
        #Eccentricity.
        return self._sat.ecco

    def get_argpo(self):
        #'argpo'
        #Argument of perigee in radians.
        return self._sat.argpo

    def get_mo(self):
        #'mo'
        #Mean anomaly in radians.
        return self._sat.mo

    def get_no(self):
        #'no'
        #Mean motion in radians per minute.
        return self._sat.no




# ---------------------------------------------------
# ---------------------------------------------------
# FUNCTIONS


def getSatTLE(identifier, file=None):
    tle = None,None,None

    if(file != None):
        #wenn file name explizit angegeben
        tle = getSatTLE_File(identifier, file)

    if (tle[0] != None):
        # wenn TLE bereits gefunden: gib zurueck
        return tle
    else:
        # durchsuch alle verzeichnisse

        for entry in sat_list:
            tle = getSatTLE_File(identifier, entry)
            if (tle[0] != None):
                # wenn TLE gefunden: gib zurueck
                return tle
    print("No TLE element found")
    return tle

    # example code
    # test = getSatTLE("07646")

# end FUNCTION ---------------------------------------------------



def getSatTLE_File(identifier, file="stations.txt"):
    default_return = None, None, None

    if (identifier==None):
        raise NameError('Missing inputs for function [getSatById].')

    filename = __getAbsFilePathTo(sat_rel_path+"/"+file)

    line_number=None

    f = open(filename)
    linecntr = 0
    for line in f:
        linecntr = linecntr+1   #increment linecounter

        if (linecntr%3 == 2):
            # jede dritte zeile mit offset 1 (line 1 TLE)
            if(line[2:2+5] == str(identifier)):
                line_number = linecntr-1
                # wenn identifier gefunden, gib linenumber zurueck
                break
    # end FOR ----------------
    f.close()

    if (line_number==None):
        ## wenn nichts gefunden wurde
        return default_return
    else:
        # (1) wenn identifier gefunden wurde,
        f = open(filename)
        linecntr = 0

        # (2) dann lies das file erneut fuer die entsprechenden TLEs
        for line in f:
            linecntr = linecntr+1   #increment linecounter

            if (linecntr == line_number):
                ## die entsprechende line wurde gefunden
                n = line[0:-1]  # [0:-1] = entferne "\n" am Ende
                l1 = f.readline()[0:-1]
                l2 = f.readline()[0:-1]
        # end FOR ----------------

        f.close()
        # (3) und gib diese TLEs zurueck
        return n, l1, l2

    # end ELSE ----------------

# end FUNCTION ---------------------------------------------------






def listSats(file='stations.txt', maxNum=10):

    filename = __getAbsFilePathTo(sat_rel_path+"/"+file)


    print("---------------------------------------------------")
    print("The first "+str(maxNum)+" satellites in '"+file+"':")
    print("---------------------------------------------------")
    #      25544: ISS (ZARYA)              (2019 023.26903142)
    print("ID     Name                      TLE Epoch")

    f = open(filename)

    for i in range(maxNum):
        n_ = f.readline()[0:-1]
        l1_ = f.readline()[0:-1]
        l2_ = f.readline()[0:1]
        del l2_

        if n_ =="":
            print("---------------------------------------------------")
            print("'"+file+"' contains only "+str(i)+" Satellite(s).")
            break

        id_ = l1_[2:2+5]
        Y_ = int(l1_[18:18+2])
        D_ = (l1_[20:20+12])

        if Y_>=57:
            y_=1900+Y_
        else:
            y_=2000+Y_



        text_ = id_+": "+n_+" ("+str(y_)+" "+str(D_)+")"
        print(text_)
    print("---------------------------------------------------")
    f.close()

    #    ISS (ZARYA)
    #1 25544U 98067A   19023.26903142  .00000178  00000-0  10220-4 0  9997
    #2 25544  51.6427   1.9875 0004758 301.9446  19.2970 15.53166446152735

    # example code:
    # listSats("stations.txt",60)

# end of FUNCTION ---------------------------------------------------


def __getAbsFilePathTo(relPath):
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    #rel_path = sat_rel_path+"/"+file

    try:
        absPath = os.path.join(fileDir, relPath)
    except:
        raise NameError('Error at "__getAbsFilePathTo(relPath)".')
    return absPath

# end FUNCTION ---------------------------------------------------
