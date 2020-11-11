# standard librarys

# classes / functions copied from magic.py and adapted
from __future__ import print_function, unicode_literals
import math
import datetime
import time
import threading

# downloaded librarys
import numpy as np

# librarys Christoph Polster
# OCC: changed import statements for all imports in folder src.EPH
import src.EPH.EPH_CORE_SkyObjectMgr as SOMgr
import src.EPH.EPH_CORE_TimeSpaceMgr as TSMgr

# interface (Schnittstelle)
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
            print(self.data)
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