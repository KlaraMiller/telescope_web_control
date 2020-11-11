# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 11:08:21 2019

@author: hirschmu16
@description: set polaris ra = 0, dec = 0

==============================================================================
 LICENCE INFORMATION
==============================================================================
-
==============================================================================

"""

# standard librarys
import time

# downloaded librarys


# my librarys
import common
import threading


def main(sg1 : common.stargate):
    # flags

    print()
    print( '------------ Set polaris ------------')
    print( '--------------------------------------')
    print("  motor ra: " + str(sg1.motor_ra.get_steps()))
    print("  motor dec: " + str(sg1.motor_dec.get_steps())) 
    print( '--------------------------------------')    
    print( 'please aligne the telescope to the northstar')
    print( 'press x to exit')
    cmd_in = common.read_character()
    if cmd_in == 'x':
        print( 'aligment finished, set step to ra=0 und dec=0? [y/n]')
        print( 'press x to exit without setting steps')
        cmd_in = common.read_character()
        if cmd_in == 'y':
            threading_decS = threading.Thread(target=sg1.motor_dec.move_steps(1,0,5,1))
            threading_decS.daemon = True
            threading_decS.start()
            threading_raS = threading.Thread(target=sg1.motor_ra.move_steps(1,0,5,1))
            threading_raS.daemon = True
            threading_raS.start()
            sg1.mydata.set_polaris(True)
            sg1.motor_ra.set_degree(90*(-1))
            sg1.motor_dec.set_degree(90*(-1))            
            print( '--------------------------------------')
            print("  motor1 ra: " + str(sg1.motor_ra.get_steps()))
            print("  motor1 dec: " + str(sg1.motor_dec.get_steps())) 
            print( '--------------------------------------')		
            time.sleep(1)
        elif cmd_in == 'n': #HIR vll gef
            main(sg1)
        elif cmd_in == 'x':
            sg1.mydata.set_polaris(False)
        else:
            main(sg1)