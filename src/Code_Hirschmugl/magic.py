# -*- coding: utf-8 -*-
"""
Created on Tue Feb  13 11:10:21 2019

@author: hirschmu16
@description: observation

==============================================================================
 LICENCE INFORMATION
==============================================================================
-
==============================================================================

"""

# standard librarys
from __future__ import print_function, unicode_literals
import math
import datetime
import time
import threading

# downloaded librarys
import numpy as np

# my librarys
import common

# librarys Christoph Polster
import EPH_CORE_SkyObjectMgr as SOMgr
import EPH_CORE_TimeSpaceMgr as TSMgr

# Schnittstelle 
class ephemeris_calculations:
    def __init__(self, utcDateTime, lat, lon, alti):
        self.data = {'Ra': 0.0, 'De': 0.0, 'Success': None}
        self.timeSpaceMgr = TSMgr.TimeSpaceMgr(None, lat, lon, alti)
        self.currentObjekt = None
        self.make_new_objekt("star", "polaris")
        
    def make_new_objekt(self, type, ID):
        self.currentObjekt = SOMgr.SkyObjectMgr(self.timeSpaceMgr, type, ID)                                   
	
    def get_pos_spherical(self, sg1):
        while(sg1.mystatus.observe == "TRUE"):
            #print(self.data)
            self.data = {'Ra': 0.0, 'De': 0.0, 'Success': None}
            #print(self.data)
            #print('start')
            #print(datetime.datetime.utcnow())
            self.currentObjekt.write_pos_to_dict(self.data)
            self.timeSpaceMgr.time_set_utcNow()
            sg1.mycalc.LMST = self.timeSpaceMgr.sidereal_get_LMST()
            #print(datetime.datetime.utcnow())
            #print(self.data)
            if self.data['Success'] == True:
                sg1.mycalc.ra_sp = self.data['Ra'] - sg1.mycalc.LMST
                sg1.mycalc.dec_sp = self.data['De']
                self.data['Success'] = False
            else:
                print('calculation not successful')
            time.sleep(0.5)

    def get_pos_spherical_test(self, sg1):
        #print(self.data)
        self.data = {'Ra': 0.0, 'De': 0.0, 'Success': None}
        #print(self.data)
        #print('start')
        #print(datetime.datetime.utcnow())
        start = time.time()
        self.currentObjekt.write_pos_to_dict(self.data)
        self.timeSpaceMgr.time_set_utcNow()
        sg1.mycalc.LMST = self.timeSpaceMgr.sidereal_get_LMST()
        end = time.time()
        print(end -start)
        #print(datetime.datetime.utcnow())
        #print(self.data)
        print(self.data)
        if self.data['Success'] == True:
            sg1.mycalc.ra_sp = self.data['Ra'] - sg1.mycalc.LMST
            sg1.mycalc.dec_sp = self.data['De']
            self.data['Success'] = False
        else:
            print('calculation not successful')


def calc_spherical_to_cartesian(myData, star_nr, LST, ra_sp, dec_sp, ra_av, dec_av):
    # Setpoints
    tel_ra_deg = (LST - ra_sp) * math.pi / 180
    dec_deg = dec_sp * math.pi / 180
    
    x = math.cos(dec_deg) * math.cos(tel_ra_deg)
    print(x)
    myData.set_T_sp(star_nr,0,x)
    
    y = math.cos(dec_deg) * math.sin(tel_ra_deg)
    myData.set_T_sp(star_nr,1,y)
    
    z = math.sin(dec_deg)
    myData.set_T_sp(star_nr,2,z)
    
    # Actual values
    ra_av_deg = ra_av * math.pi / 180
    dec_av_deg = dec_av * math.pi / 180
    
    x = math.cos(dec_av_deg) * math.cos(ra_av_deg)
    print(x)
    myData.set_T_av(star_nr,0,x)
    
    y = math.cos(dec_av_deg) * math.sin(ra_av_deg)
    myData.set_T_av(star_nr,1,y)
    
    z = math.sin(dec_av_deg)
    myData.set_T_av(star_nr,2,z)
    
def calc_T_corr(myData):
    print("start corr")
    print(myData.get_T_sp())
    print("inv T setpoint")    
    T_sp_inv = np.linalg.inv(myData.get_T_sp())
    print(T_sp_inv)
    print("T_av*T_sp_inv")  
    T = myData.get_T_av() * T_sp_inv
    print(T)
    print("inv T")
    T_inv = np.linalg.inv(T)
    print(T_inv)    
    print("saved in T_corr") 
    myData.set_T_corr(None,None,T_inv)
    print(myData.get_T_corr())
    
def calc_sp_corr(myData, LST, ra_sp, dec_sp):
    # Setpoints
    tel_ra_deg = (LST - ra_sp) * math.pi / 180
    dec_deg = dec_sp * math.pi / 180
    
    x = math.cos(dec_deg) * math.cos(tel_ra_deg)   
    y = math.cos(dec_deg) * math.sin(tel_ra_deg)   
    z = math.sin(dec_deg)
    T = myData.get_T_sp()
    x_corr = x * T[0,0] + x * T[0,1] + x * T[0,2]
    y_corr = y * T[1,0] + y * T[1,1] + y * T[1,2]
    z_corr = z * T[2,0] + z * T[2,1] + z * T[2,2]
    print("xtest")
    print(x_corr)
    print(y_corr)    
    print(z_corr)
    print("angle")
    ra = math.atan2(y_corr, x_corr) * 180 / math.pi
    dec = 0 #math.asin(z_corr) * 180 / math.pi
    print(ra)
    print(dec)    
    
    
def test(myData):
    print("star1")
    print(myData.get_T_sp())
    calc_spherical_to_cartesian(myData, 0, 10.1, 20.3, 30.5, 19.9, 29.6)
    calc_spherical_to_cartesian(myData, 1, 10.1, 50.3, 80.5, 50.3, 80.5)
    calc_spherical_to_cartesian(myData, 2, 10.1, 70.3, 110.5, 70.3, 110.5)
    print(myData.get_T_sp())        
    calc_T_corr(myData)
    print("start2")
    calc_sp_corr(myData, 10.1, 20.3, 30.5)
    '''
    print("TEST vektor")
    mat = np.array([(1,-1,2), (0,-3,1)])
    vec = np.array([(2),(1),(0)])
    vec_sp = mat * vec
    print(mat)
    print("*")
    print(vec)
    print("=")
    print(vec_sp)
    '''
    common.read_character()
    
    
def test_runtime_star(sg1):
    print(' Anlegen Stern ')
    start = time.time()
    eph = ephemeris_calculations(None, sg1.mydata.gps_latitude, sg1.mydata.gps_longitude, sg1.mydata.gps_altitude)
    eph.make_new_objekt("star", "Vega")
    end = time.time()
    print(end - start)
    
    print(' abfragen Stern ')
    eph.get_pos_spherical_test(sg1, )
    
    
def test_runtime_planet(sg1):
    
    print(' Anlegen Planet ')
    start = time.time()
    eph = ephemeris_calculations(None, sg1.mydata.gps_latitude, sg1.mydata.gps_longitude, sg1.mydata.gps_altitude)
    eph.make_new_objekt("planet", "mars")
    end = time.time()
    print(end - start)
    
    print(' abfragen Planet ')
    eph.get_pos_spherical_test(sg1, )

    
def test_runtime_moon(sg1):    
    print(' Anlegen Mond ')
    start = time.time()
    eph = ephemeris_calculations(None, sg1.mydata.gps_latitude, sg1.mydata.gps_longitude, sg1.mydata.gps_altitude)
    eph.make_new_objekt("moon", "moon")
    end = time.time()
    print(end - start)
 
    print(' abfragen moon ')
    eph.get_pos_spherical_test(sg1, )

def test_runtime_sat(sg1):    
    print(' Anlegen Sat ')
    start = time.time()
    eph = ephemeris_calculations(None, sg1.mydata.gps_latitude, sg1.mydata.gps_longitude, sg1.mydata.gps_altitude)
    eph.make_new_objekt("sat", "25544")
    end = time.time()
    print(end - start)
    
    print(' abfragen sat ')
    eph.get_pos_spherical_test(sg1, )      
    
    
