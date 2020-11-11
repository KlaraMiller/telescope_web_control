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
# -----------------------------------------------------------------------------      
# --------------------------------- librarys ----------------------------------
# ----------------------------------------------------------------------------- 

# standard librarys
from __future__ import print_function, unicode_literals
from pprint import pprint
import time
import threading
import datetime
import os

# downloaded librarys
from PyInquirer import style_from_dict, Token, prompt, Separator
from examples import custom_style_2

# my librarys
import common
import magic
import motor_control

# -----------------------------------------------------------------------------      
# ---------------------------- classes / functions ----------------------------
# -----------------------------------------------------------------------------  

def header(sg1 : common.stargate, target):
    while(sg1.mystatus.observe == "TRUE"):
        common.header(sg1, 'OBSERVE')
        print(datetime.datetime.utcnow())
        print('' )
        print('target: ' + str(target))
        #calculations
        print('LMST: ' + str(sg1.mycalc.LMST))
        print('****************** RA ******************' )        
        print('setpoint: ' + str(sg1.mycalc.ra_sp))
        print('actual value: ' + str(sg1.motor_ra.get_degree()))
        print('setpoint steps: ' + str(sg1.mycalc.ra_sp_steps))
        print('actual value steps: ' + str(sg1.motor_ra.get_steps()))
        print('direction: ' + str(sg1.mycalc.ra_dir))        
        print('****************** DEC ******************' )        
        print('setpoint: ' + str(sg1.mycalc.dec_sp))
        print('actual value: ' + str(sg1.motor_dec.get_degree()))
        print('setpoint steps: ' + str(sg1.mycalc.dec_sp_steps))
        print('actual value steps: ' + str(sg1.motor_dec.get_steps()))
        print('direction: ' + str(sg1.mycalc.dec_dir)) 
        print('')
        print( '---------------- OPTIONS -----------------')
        print( 'x ... exit')
        print( 's ... stop the motors')
        print( 'm ... manual mode')
        time.sleep(0.1)
        
        
        

# =============================================================================      
# ================================== observe ==================================
# ============================================================================= 
       
def main(sg1 : common.stargate, target = None):
    if target == None and sg1.mytarget.target == None:
        print('no target selected')
        sg1.mystatus.observe = "False"
        time.sleep(1)
    else:
        print('start')
        # creating an target object
        sg1.mystatus.observe = "TRUE"
        eph = magic.ephemeris_calculations(None, sg1.mydata.gps_latitude, sg1.mydata.gps_longitude, sg1.mydata.gps_altitude)
        eph.make_new_objekt("star", str(target))
        print('start calculations ... ') 
        print('thread')
        # calculation the angles of the target
        threading_calc = threading.Thread(name='calc', target=eph.get_pos_spherical, args=(sg1, ))
        threading_calc.daemon = True
        threading_calc.start()
        #threading6 = threading.Thread(target=sg1.motor_ra.move_steps(64836,0,2,0))
        #threading6.daemon = True
        #threading6.start()
        
        # starting the motors
        threading_ra = threading.Thread(name='ra', target=sg1.motor_ra.move_degree, args=(sg1.mycalc.ra_sp, 2,sg1))
        threading_ra.daemon = True
        threading_ra.start()
        threading_dec = threading.Thread(name='dec', target=sg1.motor_dec.move_degree, args=(sg1.mycalc.dec_sp, 2, sg1))
        threading_dec.daemon = True
        threading_dec.start()
        
        # header
        threading_header = threading.Thread(name='header', target=header, args=(sg1,sg1.mytarget.target))
        threading_header.daemon = True
        threading_header.start()
    
    # keyboard input
    while(sg1.mystatus.observe == "TRUE"):
        cmd_in = common.read_character()
        if cmd_in == 'x':
            sg1.mystatus.observe = False
            os.system('clear')
        elif cmd_in == 'g':
            threading6 = threading.Thread(target=sg1.motor_dec.move_steps(10,0,5,1))
            threading6.daemon = True
            threading6.start()
        elif cmd_in == 's':
            threading_decS = threading.Thread(target=sg1.motor_dec.move_steps(0,0,5,1))
            threading_decS.daemon = True
            threading_decS.start()
            threading_raS = threading.Thread(target=sg1.motor_ra.move_steps(0,0,5,1))
            threading_raS.daemon = True
            threading_raS.start()
        elif cmd_in == 'm':
            sg1.mystatus.observe = "MANUAL"
            motor_control.mode_manual(sg1)
        elif cmd_in == 'y':
            sg1.mystatus.observe = "MANUAL"
            motor_control.mode_manual(sg1)                 






# -----------------------------------------------------------------------------      
# --------------------------------- OLD / TEST --------------------------------
# -----------------------------------------------------------------------------         
        
def test(sg1 : common.stargate):
    print('start') 
    sg1.mystatus.observe = "TRUE"
    eph = magic.ephemeris_calculations(None, sg1.mydata.gps_latitude, sg1.mydata.gps_longitude, sg1.mydata.gps_altitude)
    eph.make_new_objekt("star", "Vega")
    #eph.get_pos_spherical(dict1)
    #print(dict1)
    print('thread')    
    threadingc = threading.Thread(target=eph.get_pos_spherical, args=(sg1, ))
    threadingc.daemon = True
    threadingc.start()
    print(sg1.mycalc.ra_sp) 
    print(sg1.mycalc.dec_sp)  
    print('ra')
    sg1.motor_ra.move_degree(sg1.mycalc.ra_sp, 2,sg1)
    print('dec')
    sg1.motor_dec.move_degree(sg1.mycalc.dec_sp, 2, sg1)

    common.read_character()
    
def test2(sg1 : common.stargate):
    print('create object of observation ... ')
    sg1.mystatus.observe = "TRUE"
    eph = magic.ephemeris_calculations(None, sg1.mydata.gps_latitude, sg1.mydata.gps_longitude, sg1.mydata.gps_altitude)
    eph.make_new_objekt("star", "Vega")
    print('start calculations ... ') 
    print('thread') 
    threading1 = threading.Thread(name='calc', target=eph.get_pos_spherical, args=(sg1, ))
    threading1.daemon = True
    threading1.start()
    print('start observation ... ') 
    time.sleep(2)
    threading3 = threading.Thread(name='header', target=header, args=(sg1,"Vega"))
    threading3.daemon = True
    threading3.start()
    while(sg1.mystatus.observe == "TRUE"):
        cmd_in = common.read_character()
        if cmd_in == 'x':
            sg1.mystatus.observe = "False"
        elif cmd_in == 's':
            threading4 = threading.Thread(target=sg1.motor_dec.move_steps(10,0,5,1))
            threading4.daemon = True
            threading4.start()
            threading5 = threading.Thread(target=sg1.motor_ra.move_steps(10,0,5,1))
            threading5.daemon = True
            threading5.start()
        elif cmd_in == 'g':
            threading6 = threading.Thread(target=sg1.motor_ra.move_degree, args=(sg1.mycalc.ra_sp, 5))
            threading6.daemon = True
            threading6.start()
        elif cmd_in == 'm':
            sg1.mystatus.observe = "MANUAL"
            motor_control.mode_manual(sg1)    



# -----------------------------------------------------------------------------      
# --------------------------------- OLD / TEST --------------------------------
# ----------------------------------------------------------------------------- 

   
''' OLD
    else:
        
        MOTOR_BASEADDR = 0x43c40000 + (0x2000*4)
        motor_config = class_RegBlock.RegBlock(MOTOR_BASEADDR, 0x1000)
        motor_speed = 5
        manuel_on = True
        Motor_1_steps = 0x0A
        Motor_2_steps = 0x0B
        motor_config.set_u32(Motor_1_steps, 0)
        motor_config.set_u32(Motor_2_steps, 0)
        mot1_pos_start = motor_config.get_u32(Motor_1_steps)
        mot2_pos_start = motor_config.get_u32(Motor_2_steps)
        print ("manuel mode start")
        print ("Motor 1 steps\t  %.8x" % mot1_pos_start)
        print (int(mot1_pos_start))
        print ("Motor 2 steps\t  %.8x" % mot2_pos_start)
        print (int(mot2_pos_start))
    
        cord = class_steps.hl_goto_koord(0,0,5,15)
        print(cord.get_rektanzension())
        print(cord.get_deklination())
        threading2 = threading.Thread(target=motor_control.motor_move('mot1',cord.get_rektanzension(),0,motor_speed,1 ,motor_config))
        threading2.daemon = True
        threading2.start()
        threading1 = threading.Thread(target=motor_control.motor_move('mot2',cord.get_deklination(),0,motor_speed,1 ,motor_config))
        threading1.daemon = True
        threading1.start()
        print (threading.active_count())
        threading2.join()
        threading1.join()
        print (threading.active_count())
        print ('done')
    	
        while manuel_on:
            #time.sleep(0.1)
            cmd_in = common.read_character()
            if cmd_in == 'x':
                mot1_pos_diff = motor_config.get_u32(Motor_1_steps) - mot1_pos_start
                mot2_pos_diff = motor_config.get_u32(Motor_2_steps) - mot1_pos_start
                mydata.set_motor1_diff(mot1_pos_diff)
                mydata.set_motor2_diff(mot2_pos_diff)
                manuel_on = False
                '''