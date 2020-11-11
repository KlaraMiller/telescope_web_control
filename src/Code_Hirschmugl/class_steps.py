#
# hl_goto_koord
#
# Schrittberechnung für beide Motoren und starten dieser
#
# IN: rektazension - Rektaszensions Koordinate in Grad
# deklination - Deklination Koordinate in Grad
# OUT: void
#
#
#!/usr/bin/python
# -*- coding: <encoding name> -*-

import math
import motor_control


class hl_goto_koord:
    
    def __init__(self, rektazension_av, deklination_av, rektazension_sp, deklination_sp):
        self.rektazension_av = rektazension_av
        self.deklination_av = deklination_av
        self.rektazension_sp = rektazension_sp
        self.deklination_sp = deklination_sp
        self.const_full_step = 0.002553191489 #(360 / (200 * 705))
        self.const_half_step = 0.002553191489 / 2
        self.const_quater_step = 0.002553191489 / 4
        
        
    def get_rektanzension(self):
        temp = 0
        temp = (self.rektazension_sp - self.rektazension_av)
        step = "FULL_STEP"
        if(temp > 0):
            #MOT1_RIGHT
            dir_mot1 = "RIGHT"
        else:
            #MOT1_LEFT
            dir_mot1 = "LEFT"
            temp = temp * (-1)
        if(temp > 180):
            temp = 360 - temp
            if(dir_mot1 == "RIGHT"):
                #MOT1_LEFT
                dir_mot1 = "LEFT"
            else:
                #MOT1_RIGHT
                dir_mot1 = "RIGHT"
        if(step == "FULL_STEP"):
            temp = math.floor((temp / self.const_full_step))
        else:
            temp = math.floor((temp / self.const_half_step))
        #hl_make_steps((uint32_t)temp, MOT1)
        return temp

    def get_deklination(self):
        temp = self.deklination_sp - self.deklination_av
        step = "FULL_STEP"
        if(temp > 0):
            #MOT2_UP
            dir_mot2 = "UP"
        else:
            #MOT2_DOWN
            dir_mot2 = "DOWN"
            temp = temp * (-1)
        if(temp > 180):
            temp = 360 - temp
            if(dir_mot2 == "UP"):
                #MOT2_DOWN
                dir_mot2 = "DOWN"
            else:
                #MOT2_UP
                dir_mot2 = "UP"
        if(step == "FULL_STEP"):
            temp = math.floor((temp / self.const_full_step))
        else:
            temp = math.floor((temp / self.const_full_step))
        return temp
    
    
if __name__ == '__main__':
    a = hl_goto_koord(0,0,10,15)
    print(a.get_deklination())
    print(a.get_rektanzension())
    
    