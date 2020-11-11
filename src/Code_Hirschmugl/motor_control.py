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
# -----------------------------------------------------------------------------      
# --------------------------------- librarys ----------------------------------
# ----------------------------------------------------------------------------- 

# standard librarys
import threading
import time
import math

# downloaded librarys

# my librarys
import common
import class_steps
import observe
import star3_verification


# -----------------------------------------------------------------------------      
# ---------------------------- classes / functions ----------------------------
# -----------------------------------------------------------------------------  

class motor:
    def __init__(self, baseaddr, command, read_steps):
        self.baseaddr = baseaddr
        self.read_steps = read_steps
        self.command = command
        self.register = common.RegBlock(self.baseaddr, 0x1000)
        self.const_full_step = 360 / (200 * 705)
                        
    def control_input(self, steps, micro_steps, step_periode, direction):
        steps_bin = bin(steps)[2:].zfill(16)  
        micro_steps_bin = bin(micro_steps)[2:].zfill(16)    
        step_periode_bin = bin(step_periode)[2:].zfill(12)
        step_mode = bin(0)[2:].zfill(3)
        direction_bin = bin(direction)[2:].zfill(1)
        
        tmp =  (str(direction_bin) + str(step_mode) + str(step_periode_bin) + str(steps_bin))
        #print(tmp)
        return int(tmp, 2)
    
    def move(self, steps, micro_steps, step_periode, direction): 
        #print("start motor")
        #print(steps)      
        #print(micro_steps) 
        #print(direction) 
        bitstream = self.control_input(steps ,micro_steps, step_periode, direction)

        try:
            #print(self.command)
            #print(bitstream)
            self.register.set_u32(self.command, bitstream) 
            print('--- setpoint written to register ---')
        except KeyboardInterrupt:
            print('wrong motor selected')

    def set_steps(self, steps):
        self.register.set_u32(self.read_steps, steps)
        
    def set_degree(self, steps):
        self.register.set_u32(self.read_steps, math.floor(steps / self.const_full_step))
    
    def get_steps(self):
        return self.register.get_u32(self.read_steps)
    def get_degree(self):
        return (self.register.get_u32(self.read_steps) * self.const_full_step)*(-1)


class motor_ra(motor):
    
    def __init__(self, baseaddr, command, read_steps):
        motor.__init__(self, baseaddr, command, read_steps)

    def get_rektanzension(self, rektazension_sp, rektazension_av):
            temp = 0
            #print("start get setpoint")
            #print("setpoint =" + str(rektazension_sp))
            #print("actual value =" + str(rektazension_av))           
            temp = (rektazension_sp - rektazension_av)
            #print("setpoint degree =" + (temp))
            step = "FULL_STEP"
            if(temp > 0):
                #MOT1_RIGHT
                dir_mot1 = "EAST"
            else:
                #MOT1_LEFT
                dir_mot1 = "WEST"
                temp = temp * (-1)
            if(temp > 180):
                temp = 360 - temp
                if(dir_mot1 == "EAST"):
                    #MOT1_LEFT
                    dir_mot1 = "WEST"
                else:
                    #MOT1_RIGHT
                    dir_mot1 = "EAST"
            if(step == "FULL_STEP"):
                temp = math.floor((temp / self.const_full_step))
            else:
                temp = math.floor((temp / self.const_half_step))
            print(temp)
            print(dir_mot1)
            return {"steps": temp, "micro_steps": 0, "direction": dir_mot1}

    def move_degree(self, degree, step_periode, sg1):        
        ra = self.get_rektanzension(degree, self.get_degree())
        if ra["direction"] == "EAST":
            direction = 0
        elif ra["direction"] == "WEST":
            direction = 1
        sg1.mycalc.ra_sp_steps = ra["steps"]
        sg1.mycalc.ra_dir = ra["direction"]        
        motor.move(self, ra["steps"] , ra["micro_steps"], step_periode, direction)
        
    def move_steps(self, steps, micro_steps, step_periode, direction):
        motor.move(self, steps, micro_steps, step_periode, direction)


class motor_dec(motor):
    
    def __init__(self, baseaddr, command, read_steps):
        motor.__init__(self, baseaddr, command, read_steps)

    def get_deklination(self, deklination_sp, deklination_av):
        temp = deklination_sp - deklination_av
        
        print("--- get setpoint ---")
        print("setpoint = " + str(deklination_sp))
        print("current degrees = " + str(deklination_av))           
        print("setpoint degree = " + str(temp))
    
        step = "FULL_STEP"
        if(temp > 0):
            #MOT2_UP
            dir_mot2 = "NORTH"
        else:
            #MOT2_DOWN
            dir_mot2 = "SOUTH"
            temp = temp * (-1)
        if(temp > 180):
            temp = 360 - temp
            if(dir_mot2 == "NORTH"):
                #MOT2_DOWN
                dir_mot2 = "SOUTH"
            else:
                #MOT2_UP
                dir_mot2 = "NORTH"
        if(step == "FULL_STEP"):
            temp = math.floor((temp / self.const_full_step))
        else:
            temp = math.floor((temp / self.const_full_step))
        return {"steps": temp, "micro_steps": 0, "direction": dir_mot2}
        
    def move_degree(self, degree, step_periode, sg1):
        dec = self.get_deklination(degree, self.get_degree())
        if dec["direction"] == "NORTH":
            direction = 0
        elif dec["direction"] == "SOUTH":
            direction = 1
        sg1.mycalc.dec_sp_steps = dec["steps"]
        sg1.mycalc.dec_dir = dec["direction"]
        print("setpoint steps = " + str(dec["steps"]))
        print("setpoint direction = " + str(dec["direction"]))
        motor.move(self, dec["steps"] , dec["micro_steps"], step_periode, direction)
        
    def move_steps(self, steps, micro_steps, step_periode, direction):
        motor.move(self, steps, micro_steps, step_periode, direction)


# =============================================================================      
# =================================== manual ==================================
# ============================================================================= 

def mode_manual(sg1 : common.stargate):
    manual_on = True
    motor_speed = 5
    mot_dec_pos_start = sg1.motor_dec.get_steps()
    mot_ra_pos_start = sg1.motor_ra.get_steps()
    while manual_on:
        common.header_move(sg1)
        print('speed: ' + str(motor_speed))
        cmd_in = common.read_character()
        if cmd_in == 'w':
            # move dec north
            threading2 = threading.Thread(target=sg1.motor_dec.move_steps(100,0,motor_speed,1))
            threading2.daemon = True
            threading2.start()
            threading2.join()
        elif cmd_in == 's':
            # move dec south
            threading2 = threading.Thread(target=sg1.motor_dec.move_steps(100,0,motor_speed,0))
            threading2.daemon = True
            threading2.start()
            threading2.join()
        elif cmd_in == 'a':
            # move ra east
            threading2 = threading.Thread(target=sg1.motor_ra.move_steps(100,0,motor_speed,1))
            threading2.daemon = True
            threading2.start()
            threading2.join()
        elif cmd_in == 'd':
            # move ra west
            threading2 = threading.Thread(target=sg1.motor_ra.move_steps(100,0,motor_speed,0))
            threading2.daemon = True
            threading2.start()
            threading2.join()
        elif cmd_in == 'q':
            # increase pause between steps
            motor_speed = motor_speed + 1
            if motor_speed > 10:
                motor_speed = 10
            print(motor_speed)
        elif cmd_in == 'e':
            # decrease pause between steps            
            motor_speed = motor_speed - 1
            if motor_speed < 1:
                motor_speed = 1
            print(motor_speed) 
        elif cmd_in == 'x':
            # exit
            mot_dec_pos_diff = sg1.motor_dec.get_steps() - mot_dec_pos_start
            mot_ra_pos_diff = sg1.motor_ra.get_steps() - mot_ra_pos_start
            sg1.mydata.set_motor_dec_diff(mot_dec_pos_diff)
            sg1.mydata.set_motor_ra_diff(mot_ra_pos_diff)
            manual_on = False
            if sg1.mystatus.observe == "MANUAL":
                if sg1.mytarget.target == sg1.mytarget.star1:
                    sg1.mytarget.star1_ok = "finished"
                elif sg1.mytarget.target == sg1.mytarget.star2:
                    sg1.mytarget.star2_ok = "finished"
                elif sg1.mytarget.target == sg1.mytarget.star3:
                    sg1.mytarget.star3_ok = "finished"
                star3_verification.select(sg1)
                

# -----------------------------------------------------------------------------      
# --------------------------------- OLD / TEST --------------------------------
# -----------------------------------------------------------------------------    


def test(sg1 : common.stargate):

    print("--- read current degrees ---")
    print("current degrees = " + str(sg1.motor_dec.get_degree()))
    print("--- set degree to 0 ---")
    sg1.motor_dec.set_degree(0)
    print("current degrees = " + str(sg1.motor_dec.get_degree()))
    print("--- call move_degree ---")
    threading2 = threading.Thread(target=sg1.motor_dec.move_degree(10,5,sg1))
    threading2.daemon = True
    threading2.start()
    threading2.join()
    print("---start ---")
    time.sleep(1)
    print("---after 1sec ---")
    print("current steps = " + str(sg1.motor_dec.get_steps())) 
    print("current degrees = " + str(sg1.motor_dec.get_degree()))
    time.sleep(5)
    print("--- after 5sec ---")
    print("current steps = " + str(sg1.motor_dec.get_steps()))  
    print("current degrees = " + str(sg1.motor_dec.get_degree()))
    time.sleep(10)
    print("--- after 10sec ---")
    print("current steps = " + str(sg1.motor_dec.get_steps())) 
    print("current degrees = " + str(sg1.motor_dec.get_degree()))
    time.sleep(20)
    print("--- after 20sec ---")
    print("current steps = " + str(sg1.motor_dec.get_steps()))  
    print("current degrees = " + str(sg1.motor_dec.get_degree()))
    print("--- END ---")
    common.read_character()
    

def mode_test(sg1):
    MOTOR_BASEADDR = 0x43c40000 + (0x2000*4)
    Motor_1_steps = 0x0A
    Motor_1_command = 0x08
    
    motor1 = motor(MOTOR_BASEADDR, Motor_1_command, Motor_1_steps, 5)
    print(motor1.get_steps())
    motor1.set_steps(33)
    print(motor1.get_steps())
    thread1 = threading.Thread(target=motor1.set_steps(66))
    thread1.daemon = True
    thread1.start()
    thread1.join()
    print(motor1.get_steps())
    
    cord = class_steps.hl_goto_koord(0,0,5,15)
    print(cord.get_rektanzension())
    print(cord.get_deklination())
    threading2 = threading.Thread(target=motor1.move(200,0,1))
    threading2.daemon = True
    threading2.start()
    threading2.join()
    print("ok")
    time.sleep(1)
    print(motor1.get_steps())  
    print(motor1.get_degree())
    
    cmd_in = common.read_character()




        
        
        
        
        
        