
# -----------------------------------------------------------------------------
# --------------------------------- librarys ----------------------------------
# -----------------------------------------------------------------------------

import math
import mmap
import struct

# -----------------------------------------------------------------------------
# ---------------------------- classes / functions ----------------------------
# -----------------------------------------------------------------------------


class motor:
    def __init__(self, baseaddr, command, read_steps):
        self.baseaddr = baseaddr
        self.read_steps = read_steps
        self.command = command
        self.register = RegBlock(self.baseaddr, 0x1000)
        self.const_full_step = 360 / (200 * 705)

    def control_input(self, steps, micro_steps, step_periode, direction):
        steps_bin = bin(steps)[2:].zfill(16)
        micro_steps_bin = bin(micro_steps)[2:].zfill(16)
        step_periode_bin = bin(step_periode)[2:].zfill(12)
        step_mode = bin(0)[2:].zfill(3)
        direction_bin = bin(direction)[2:].zfill(1)

        tmp = (str(direction_bin) + str(step_mode) + str(step_periode_bin) + str(steps_bin))
        # print(tmp)
        return int(tmp, 2)

    def move(self, steps, micro_steps, step_periode, direction):
        # print("start motor")
        # print(steps)
        # print(micro_steps)
        # print(direction)
        bitstream = self.control_input(steps, micro_steps, step_periode, direction)

        try:
            # print(self.command)
            # print(bitstream)
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
        return (self.register.get_u32(self.read_steps) * self.const_full_step) * (-1)



class motor_ra(motor):

    def __init__(self, baseaddr, command, read_steps):
        motor.__init__(self, baseaddr, command, read_steps)

    def get_rektanzension(self, rektazension_sp, rektazension_av):
        temp = 0
        # print("start get setpoint")
        # print("setpoint =" + str(rektazension_sp))
        # print("actual value =" + str(rektazension_av))
        temp = (rektazension_sp - rektazension_av)
        # print("setpoint degree =" + (temp))
        step = "FULL_STEP"
        if (temp > 0):
            # MOT1_RIGHT
            dir_mot1 = "EAST"
        else:
            # MOT1_LEFT
            dir_mot1 = "WEST"
            temp = temp * (-1)
        if (temp > 180):
            temp = 360 - temp
            if (dir_mot1 == "EAST"):
                # MOT1_LEFT
                dir_mot1 = "WEST"
            else:
                # MOT1_RIGHT
                dir_mot1 = "EAST"
        if (step == "FULL_STEP"):
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
        motor.move(self, ra["steps"], ra["micro_steps"], step_periode, direction)

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
        if (temp > 0):
            # MOT2_UP
            dir_mot2 = "NORTH"
        else:
            # MOT2_DOWN
            dir_mot2 = "SOUTH"
            temp = temp * (-1)
        if (temp > 180):
            temp = 360 - temp
            if (dir_mot2 == "NORTH"):
                # MOT2_DOWN
                dir_mot2 = "SOUTH"
            else:
                # MOT2_UP
                dir_mot2 = "NORTH"
        if (step == "FULL_STEP"):
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
        motor.move(self, dec["steps"], dec["micro_steps"], step_periode, direction)

    def move_steps(self, steps, micro_steps, step_periode, direction):
        motor.move(self, steps, micro_steps, step_periode, direction)




class RegBlock:
    def __init__(self, baseAddress, size):
        self.baseAddress = baseAddress
        self.size = size

        with open("/dev/mem", "r+b") as f:
            self.mem = mmap.mmap(f.fileno(), size, offset=baseAddress)

    def close(self):
        self.mem.close()

    def set_u32(self, address, val):
        address = address * 4
        self.mem[address:address + 4] = struct.pack("<L", val & 0xffffffff)

    def get_u32(self, address):
        address = address * 4
        return struct.unpack("l", self.mem[address:address + 4])[0]