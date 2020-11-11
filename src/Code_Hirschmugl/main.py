# standard libraries
import nav
import time
import datetime
import math
import threading
import sys
import common
#tty.setcbreak(sys.stdin)
#import mot_hand

import class_queue

def get_degree_x(x,y,z):
    xAngle = math.atan2(x, (math.sqrt((y*y) + (z*z))))
    xAngle = xAngle * 180 / 3.141592
    return xAngle

def get_degree_y(x,y,z):
    yAngle = math.atan( y / (math.sqrt((x*x) + (z*z))))
    yAngle = yAngle * 180 / 3.141592
    return yAngle

def get_degree_z(x,y,z):
    zAngle = math.atan( math.sqrt((x*x) + (y*y)) / z)
    zAngle = zAngle * 180 / 3.141592
    return zAngle

def get_compass(x,y):
    D = math.atan(y/x)* 180 / 3.141592
    return D

qm = class_queue.QueueMap()

while True:
    cmd_in = common.read_character()
    if cmd_in == 'v':
        print('starting')        
        thread1 = threading.Thread(nav.acc_get_value(qm))
        thread1.daemon = True
        thread1.start()
        print(threading.active_count())
        thread1.join()
        print(threading.active_count())
        print('done')
        print (qm.pop('acc_x'))
        print (qm.pop('acc_y'))
        print (qm.pop('acc_z'))
        time.sleep(3)
    elif cmd_in == 'e':
        sys.exit()
    elif cmd_in == 'm':        
        mot_hand.mode_manuel()
    

    #if __name__ == "__main__":    
    #x, y, z = Nav.acc_get_value()

    
    #print("x-Achse scaled: " + str(x))
    #print("y-Achse scaled: " + str(y))
    #print("z-Achse scaled: " + str(z))

    
    """
    x_deg = get_degree_x(x,y,z)
    y_deg = get_degree_y(x,y,z)
    z_deg = get_degree_z(x,y,z)
    print("x-Achse degree: " + str(x_deg))
    print("y-Achse degree: " + str(y_deg))
    print("z-Achse degree: " + str(z_deg))
    
    mag_x, mag_y, mag_z = Nav.mag_get_value()
    
    print("#### compass ####")
    print("x-Achse scaled: " + str(mag_x))
    print("y-Achse scaled: " + str(mag_y))
    
    comp_angle = get_compass(mag_x,mag_y)
    
    if comp_angle < 0:
        comp_angle = comp_angle +360
    elif comp_angle > 360:
        comp_angle = comp_angle -360        
    print(comp_angle)
    """