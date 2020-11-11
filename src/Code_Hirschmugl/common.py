# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 11:08:21 2019

@author: hirschmu16
@description: common program part

==============================================================================
 LICENCE INFORMATION
==============================================================================
-
==============================================================================

"""
# -----------------------------------------------------------------------------      
# --------------------------------- librarys ----------------------------------
# ----------------------------------------------------------------------------- 

# standard librarys
import tty
import os
import sys
import termios
import datetime
import time
import threading
import mmap
import struct

# downloaded librarys
import numpy as np
from colorama import Fore, Style
from pyfiglet import Figlet

# my librarys
import motor_control


# -----------------------------------------------------------------------------      
# ---------------------------- classes / functions ----------------------------
# -----------------------------------------------------------------------------  
class RegBlock:
    def __init__(self, baseAddress, size):
        self.baseAddress = baseAddress
        self.size = size
        
        with open("/dev/mem", "r+b" ) as f:
            self.mem = mmap.mmap(f.fileno(), size, 
                       offset = baseAddress)
    def close(self):
        self.mem.close()
        
    def set_u32(self, address, val):
        address = address * 4
        self.mem[address:address+4] = struct.pack("<L", val & 0xffffffff)

    def get_u32(self, address):
        address = address * 4
        return struct.unpack("l", self.mem[address:address+4])[0]

class myCalc:
    def __init__(self):
        self.LMST = 0
        self.ra_sv = 0 #start value
        self.ra_sp = 0
        self.ra_av = 0
        self.ra_sp_steps = 0
        self.ra_dir = "None"
        self.dec_sv = 0 #start value
        self.dec_sp = 0
        self.dec_av = 0
        self.dec_sp_steps = 0
        self.dec_dir = "None"
        
        

class myStatus:
    def __init__(self):
        self.observe = None
        
class myTarget:
    def __init__(self):
        self.target = None
        self.star1 = "Star1"
        self.star2 = "Star2"
        self.star3 = "Star3"
        self.star1_ok = "incomplete"
        self.star2_ok = "incomplete"
        self.star3_ok = "incomplete"
        
    #3Star
    def set_star1(self, value):
        self.star1 = value
    def get_star1(self):
        return self.star1
    
    def set_star2(self, value):
        self.star2 = value
    def get_star2(self):
        return self.star2
    
    def set_star3(self, value):
        self.star3 = value
    def get_star3(self):
        return self.star3
        

class myData:
    def __init__(self):
        self.debug_mode = False
        self.nmod_nav_ok = False
        self.nmod_gps_ok = False
        self.set_polaris_ok = False
        self.gps_latitude = 0
        self.gps_longitude = 0
        self.gps_altitude = 0
        self.gps_time = "1970-02-05T08:52:26.000Z"
        # calculations
        self.T_sp = np.array([(1.0,1.0,1.0), (1.0,1.0,1.0), (1.0,1.0,1.0)])
        self.T_av = np.array([(1.0,1.0,1.0), (1.0,1.0,1.0), (1.0,1.0,1.0)])
        self.T_corr = np.array([(1.0,0.0,0.0), (0.0,1.0,0.0), (0.0,0.0,1.0)])
        	   
        
    def set_debug_mode(self, status):
        self.debug_mode = status
    def get_debug_mode(self):
        return self.debug_mode
    
    def set_nmod_nav(self, status):
        self.nmod_nav_ok = status
    def get_nmod_nav(self):
        return self.nmod_nav_ok
		
    def set_nmod_gps(self, status):
        self.nmod_gps_ok = status
    def get_nmod_gps(self):
        return self.nmod_gps_ok

    def set_polaris(self, status):
        self.set_polaris_ok = status
    def get_polaris(self):
        return self.set_polaris_ok

    def set_gps_latitude(self, value):
        self.gps_latitude = value
    def get_gps_latitude(self):
        return self.gps_latitude

    def set_gps_longitude(self, value):
        self.gps_longitude = value
    def get_gps_longitude(self):
        return self.gps_longitude

    def set_gps_altitude(self, value):
        self.gps_altitude = value
    def get_gps_altitude(self):
        return self.gps_altitude
		
    def set_gps_time(self, value):
        self.gps_time = value
    def get_gps_time(self):
        return self.gps_time
	
    def set_motor_dec_diff(self, value):
        self.motor_dec_diff = value
    def get_motor_dec_diff(self):
        return self.motor_dec_diff

    def set_motor_ra_diff(self, value):
        self.motor_ra_diff = value
    def get_motor_ra_diff(self):
        return self.motor_ra_diff
    
    def get_T_sp(self):
        return self.T_sp
    def set_T_sp(self, col, row, value):
        if col == None and row == None:
            self.T_sp = value
        else:
            self.T_sp[row,col] = value
    
    def get_T_av(self):
        return self.T_av
    def set_T_av(self, col, row, value):
        if col == None and row == None:
            self.T_av = value
        else:
            self.T_av[row,col] = value
    
    def get_T_corr(self):
        return self.T_corr
    def set_T_corr(self, col, row, value):
        if col == None and row == None:
            self.T_corr = value
        else:
            self.T_corr[row,col] = value


class stargate:
    def __init__(self):
        self.mydata = myData()
        self.mytarget = myTarget()
        self.mystatus = myStatus()
        self.mycalc = myCalc()
        self.motor_dec = motor_control.motor_dec((0x43c40000 + (0x2000*4)), 0x08, 0x0A)
        self.motor_ra = motor_control.motor_ra((0x43c40000 + (0x2000*4)), 0x09, 0x0B)


# -----------------------------------------------------------------------------      
# --------------------------------- functions ---------------------------------
# -----------------------------------------------------------------------------       

def set_time(mydata):
    # sets system time of linux os
    date_time = mydata.get_gps_time()
    #print(date_time)
    mydate , mytime = date_time.split('T')
    mytime, tmp = mytime.split('.')
    mydate = mydate.replace("-", "")
    #print(mydate)
    #print(mytime)
    print('setting system time ...')    
    os.system('date +%Y%m%d -s '+ str(mydate))
    os.system('date +%T -s ' + str(mytime))
    print('done')
    #print(os.system('date'))
    #print('print python utc')
    print(datetime.datetime.utcnow())
    #read_character()
    time.sleep(1)


def scale(x, x_min, x_max, y_min, y_max):
        k = float(y_max-y_min) / (x_max-x_min)
        #print((y_max-y_min))
        #print((x_max-x_min))
        #print(format(k, '.12f'))
        d = y_min - k * x_min
        #print(d)
        y = (k*x)+d
        #print(y)
        
        if (y >= y_max):
            y = y_max
        if (y <= y_min):
            y = y_min
        
        return y
    
def read_character():
    # Read a single character from the terminal without echoing it.
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch
	
# k Interface
def print_status(status, text = None):
    if type(status) == str and text == None:          
        if status == True or status == "TRUE" or status == "finished":
            print(Fore.GREEN + str(status) + Style.RESET_ALL)
        else:    
            print(Fore.RED + str(status) + Style.RESET_ALL)	
    else:
        if status == True or status == "TRUE" or status == "finished":
            print(text + ': ' + Fore.GREEN + str(status) + Style.RESET_ALL)
        else:    
            print(text + ': ' + Fore.RED + str(status) + Style.RESET_ALL)

# k Interface
def header(sg1 : stargate, name):
    # variables
    f = Figlet(font='slant')   
    os.system('clear')
    print('')
    print('    *             *         *         *   *')
    print('          *                ')
    print(f.renderText('Stargate'))
    print(' *                *                *')
    print('                 *                ')
    print('           *              *           *       *     *')
    print('')
    print('Status')
    print_status(sg1.mydata.get_nmod_nav(), 'nmod nav status')
    print_status(sg1.mydata.get_polaris(), 'Set polaris')
    print("")
    print('***************** Observe *****************')    
    print_status(sg1.mystatus.observe, 'mode')
    print('target: ' + str(sg1.mytarget.target))
    print("")
    print('***************** GPS DATA *****************')
    print_status(sg1.mydata.get_nmod_gps(), 'nmod gps status')
    print('latitude	:' + str(sg1.mydata.get_gps_latitude()))
    print('longitude	:' + str(sg1.mydata.get_gps_longitude()))
    print('altitude	:' + str(sg1.mydata.get_gps_altitude()))
    print('time UTC	:' + str(sg1.mydata.get_gps_time()))
    print("")
    print('***************** SYSTEM *****************') 
    print_status(sg1.mydata.get_debug_mode(), 'debug mode')
    print('activ threads: ' + str(threading.active_count()))  
    print('threads: ' + str(threading.enumerate()))
    print('' )
    print('****************** ' + str(name) + ' ******************')
    print('' )    


# k Interface
def header_move(sg1 : stargate):
    header(sg1, 'MANUEL')
    print('***************** motor *****************')
    print('')
    print('***************** dec *****************')
    print('steps:' + str(sg1.motor_dec.get_steps()))
    print('degree:' + str(sg1.motor_dec.get_degree()))  
    print('***************** ra *****************')
    print('steps:' + str(sg1.motor_ra.get_steps()))
    print('degree:' + str(sg1.motor_ra.get_degree()))  
    print('')
    print( '---------------- OPTIONS -----------------')
    print( 'w ... move dec north')
    print( 's ... move dec south')
    print( 'a ... move ra east ')
    print( 'd ... move ra west') 
    print('')
    print( 'q ... increase pause between steps [s]')
    print( 'e ... decrease pause between steps [s]')   
    print('')
    print( 'x ... exit the MANUEL')    
        