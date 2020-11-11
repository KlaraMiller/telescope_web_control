# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 11:08:21 2019

@author: hirschmu16
@description: reads data from nmodNav

==============================================================================
 LICENCE INFORMATION
==============================================================================
-
==============================================================================

"""

# standard librarys
import threading
import sys
import math
import subprocess
import os
import time

# downloaded librarys
from evdev import InputDevice, categorize, ecodes

# my librarys
import common


# -----------------------------------------------------------------------------      
# ---------------------------- functions / classes ----------------------------
# ----------------------------------------------------------------------------- 

class nmod_sensor:
    def __init__(self, name, dev, enable, x_min, x_max, y_min, y_max):
        self.name = name
        self.dev = InputDevice(dev)
        self.enable = enable
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        
    def scale(self, x):
        k = float(self.y_max-self.y_min) / (self.x_max-self.x_min)
        #print((y_max-y_min))
        #print((x_max-x_min))
        #print(format(k, '.12f'))
        d = self.y_min - k * self.x_min
        #print(d)
        y = (k*x)+d
        #print(y)
        
        if (y >= self.y_max):
            y = self.y_max
        if (y <= self.y_min):
            y = self.y_min
        
        return y
    
    def get_value(self):
        os.system("echo 1 > " + self.enable)
        #dev.capabilities()
        x = y = z = 0
        for event in self.dev.read_loop():
            if event.code == 0:
                x = event.value
            elif event.code == 1:
                y = event.value
            elif event.code == 2:
                z = event.value

            if (x != 0) and (y != 0) and (z != 0):
                break   
        os.system("echo 0 > " + self.enable)
        x_scaled = self.scale(x)
        y_scaled = self.scale(y)
        z_scaled = self.scale(z)
        return x_scaled, y_scaled, z_scaled   
    
def get_degree(x,y,z):
    xAngle = math.atan2(x, (math.sqrt((y*y) + (z*z))))
    xAngle = xAngle * 180 / 3.141592

    yAngle = math.atan( y / (math.sqrt((x*x) + (z*z))))
    yAngle = yAngle * 180 / 3.141592

    zAngle = math.atan( math.sqrt((x*x) + (y*y)) / z)
    zAngle = zAngle * 180 / 3.141592
    return xAngle, yAngle, zAngle

def get_compass(x,y):
    if x == 0 and y < 0:
        d = 90
    elif x == 0 and y > 0:
        d = 0
    elif x != 0:
        d = math.atan((y),(x))* 180 / 3.141592
        if d > 360:
            d = d - 360
        elif d < 0:
            d = d + 360
        else:
            d = d
    return d    

def get_compass2(y,x):
    if x == 0 and y < 0:
        d = 90
    elif x == 0 and y > 0:
        d = 270
    elif x < 0:
        d = 180 - math.atan((y*0.48828125)/(x*0.48828125))* 180 / 3.141592
    elif x > 0 and y < 0:
        d = (-1) * math.atan((y*0.48828125)/(x*0.48828125))* 180 / 3.141592
    elif x > 0 and y > 0:
        d = 360 - math.atan((y*0.48828125)/(x*0.48828125))* 180 / 3.141592
    return d      

def get_compass3(x,y):
    if x == 0 and y < 0:
        d = 90
    elif x == 0 and y > 0:
        d = 0
    elif x != 0:
        d = math.atan2((y),(x))* 180 / 3.141592 +180
        if d > 360:
            d = d - 360
        else:
            d = d
    return d         
        
def print_setup(acc, mag, mode, kill, data):
    while not kill:
        subprocess.call("clear")
        print()
        print( '------------ Nmod reading ------------')
        print( '--------------------------------------')
        print( '---------------- ACC -----------------')
        print( 'x-Achse in degree ' , data['acc_xAngle'])
        print( 'y-Achse in degree ' , data['acc_yAngle'])
        print( 'z-Achse in degree ' , data['acc_zAngle'])
        #print( 'x Mag ' , data['mag_x'])
        #print( 'y Mag ' , data['mag_y'])
        #print( 'z Mag ' , data['mag_z'])
        #print( 'x-Achse in m/s2   ' , data['acc_x'])
        #print( 'y-Achse in m/s2   ' , data['acc_y'])
        #print( 'z-Achse in m/s2   ' , data['acc_z'])
        print()        
        print( '---------------- MAG -----------------')
        print( 'direction   ' , data['direction'])
        print()        
        print( '---------------- OPTIONS -----------------')
        print( 'press x to exit the first setup')
        print( 'press r to exit the first setup')
        
        if mode == 'single':
              break
        else:
            #pass
            time.sleep(0.03) #set to whatever
            

def sensor_read(acc, mag, mode, kill, data):
    while not kill:
        acc_x = acc_y = acc_z = 0
        acc_x, acc_y , acc_z = acc.get_value()
        data['acc_x'] = acc_x
        data['acc_y'] = acc_y
        data['acc_z'] = acc_z
        data['acc_xAngle'], data['acc_yAngle'], data['acc_zAngle'] = get_degree(acc_x, acc_y, acc_z)
        
        mag_x = mag_y = mag_z = 0
        mag_x, mag_y, mag_z = mag.get_value()
        data['mag_x'] = mag_x
        data['mag_y'] = mag_y
        data['mag_z'] = mag_z
        data['direction'] = get_compass3(mag_x, mag_y)        
        if mode == 'single':
              break
        else:
            #pass
            time.sleep(0.03) #set to whatever

            

# =============================================================================      
# ==================================== main ====================================
# ============================================================================= 
                     
def main(sg1 : common.stargate):
    # create sensor objects
    #qm = class_queue.QueueMap()
    acc = nmod_sensor('acc', '/dev/input/event1', "/sys/class/spi_master/spi32766/spi32766.0/accelerometer/enable_device", -2000000, 2000000, -2, 2)
    mag = nmod_sensor('mag', '/dev/input/event0', "/sys/class/spi_master/spi32766/spi32766.1/enable_device", -4000000, 4000000, -4, 4)
    
    # flags
    kill = []    
    first_setup = True
    data = {'acc_x': 0.0, 'acc_y': 0.0, 'acc_z': 0.0, 'acc_xAngle': 0.0, 'acc_yAngle': 0.0, 'acc_zAngle': 0.0, 'direction': 0.0, 'mag_x': 0, 'mag_y': 0 , 'mag_z': 0}
    # start thread
    thread2 = threading.Thread(target=sensor_read, args=(acc, mag, 'continius', kill, data))
    thread2.daemon = True
    thread2.start()
    thread1 = threading.Thread(target=print_setup, args=(acc, mag, 'continius', kill, data))
    thread1.daemon = True
    thread1.start()
    while first_setup:
        cmd_in = common.read_character()
        if cmd_in == 'r':
            print_setup(acc, mag, 'single', kill)
        elif cmd_in == 'x':
            kill.append(True)
            first_setup = False
            print( 'first setup finished? [y/n]')
            print( 'press x to exit the first setup without saving')
            cmd_in = common.read_character()
            if cmd_in == 'y':
                sg1.mydata.set_nmod_nav(True)			
            elif cmd_in == 'n':
                main()
            elif cmd_in == 'x':
                sg1.mydata.set_nmod_nav(False)
            else:
                main()
                
# -----------------------------------------------------------------------------      
# --------------------------------- Test ---------------------------------
# -----------------------------------------------------------------------------                




