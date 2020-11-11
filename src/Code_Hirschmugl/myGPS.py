# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 11:08:21 2019

@author: hirschmu16
@description: top level of the program

==============================================================================
 LICENCE INFORMATION
==============================================================================
-
==============================================================================

"""

# standard librarys
import time
import threading
import subprocess

# downloaded librarys
import gpsd

# my librarys
import common

'''
class nmod_gps:
    def __init__(self):
        gpsd.connect()
        gpsd.connect(host="127.0.0.1", port=2947)
'''       
         
def print_setup(sg1, mode, kill):
    gpsd.connect()
    gpsd.connect(host="127.0.0.1", port=2947)
    while not kill:
        #os.system('clear')
        subprocess.call("clear")
        packet = gpsd.get_current()
        print(" ************ PROPERTIES ************* ")
        print("  Mode: " + str(packet.mode))
        print("Satellites: " + str(packet.sats))
        if packet.mode >= 2:
          print("  Latitude: " + str(packet.lat))
          print(" Longitude: " + str(packet.lon))
          print(" Track: " + str(packet.track))
          print("  Horizontal Speed: " + str(packet.hspeed))
          print(" Time: " + str(packet.time))
          print(" Error: " + str(packet.error))
        else:
          print("  Latitude: NOT AVAILABLE")
          print(" Longitude: NOT AVAILABLE")
          print(" Track: NOT AVAILABLE")
          print("  Horizontal Speed: NOT AVAILABLE")
          print(" Error: NOT AVAILABLE")

        if packet.mode >= 3:
          print("  Altitude: " + str(packet.alt))
          print(" Climb: " + str(packet.climb))
        else:
          print("  Altitude: NOT AVAILABLE")
          print(" Climb: NOT AVAILABLE")

        print(" ************** METHODS ************** ")
        if packet.mode >= 2:
          print("  Location: " + str(packet.position()))
          print(" Speed: " + str(packet.speed()))
          print("Position Precision: " + str(packet.position_precision()))
          #print("  Time UTC: " + str(packet.time_utc()))
          #print("Time Local: " + str(packet.time_local()))
          #print("   Map URL: " + str(packet.map_url()))
        else:
          print("  Location: NOT AVAILABLE")
          print(" Speed: NOT AVAILABLE")
          print("Position Precision: NOT AVAILABLE")
          print("  Time UTC: NOT AVAILABLE")
          print("Time Local: NOT AVAILABLE")
          print("   Map URL: NOT AVAILABLE")

        if packet.mode >= 3:
          print("  Altitude: " + str(packet.altitude()))
          # print("  Movement: " + str(packet.movement()))
          # print("  Speed Vertical: " + str(packet.speed_vertical()))
        else:
          print("  Altitude: NOT AVAILABLE")
          # print("  Movement: NOT AVAILABLE")
          # print(" Speed Vertical: NOT AVAILABLE")

        print(" ************* FUNCTIONS ************* ")
        print("Device: " + str(gpsd.device()))
        print( '---------------- OPTIONS -----------------')
        print( 'press x to exit the gps setup')
        sg1.mydata.set_gps_latitude(packet.lat)
        sg1.mydata.set_gps_longitude(packet.lon)
        sg1.mydata.set_gps_altitude(packet.alt)
        sg1.mydata.set_gps_time(packet.time)
        if mode == 'single':
              break
        else:
            time.sleep(1) #set to whatever
                      
def main(sg1):
    # flags
    kill = []    
    gps_setup = True
    
    # start thread
    thread1 = threading.Thread(target=print_setup, args=(sg1, 'continius', kill))
    thread1.daemon = True
    thread1.start()
    while gps_setup:
        cmd_in = common.read_character()
        if cmd_in == 'x':
            kill.append(True)
            gps_setup = False
            print( 'gps setup finished? [y/n]')
            print( 'press x to exit gps setup without saving')
            cmd_in = common.read_character()
            if cmd_in == 'y':
                sg1.mydata.set_nmod_gps(True)
                common
            elif cmd_in == 'n':
                main()
            elif cmd_in == 'x':
                sg1.mydata.set_nmod_gps(False)
            else:
                main()
            print( 'set system date and time to: ' +  str(sg1.mydata.get_gps_time()) + ' [y/n]')
            print( 'press x to exit without seting date and time')
            cmd_in = common.read_character()
            if cmd_in == 'y':
                common.set_time(sg1.mydata)
            elif cmd_in == 'n':
                main()
            elif cmd_in == 'x':
                gps_setup = False
            else:
                main()
                