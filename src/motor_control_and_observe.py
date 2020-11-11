from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import django
import json
import time
import os
import math
import threading
from django.forms.models import model_to_dict


# calculations and motors
from src.telescope.motors import motor_dec, motor_ra
from src.telescope.calculations import ephemeris_calculations, calc_spherical_to_cartesian, calc_sp_corr, calc_T_corr

# set up channel layer
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "telescope_site_config.settings")
django.setup()
channel_layer = get_channel_layer()

from sensors.models import stargate

# set up motors
motor_speed = 5


# functions
def calculate_eph(target):
    # create eph object with data from db
    eph = ephemeris_calculations(None, sg1.mydata.gps_latitude, sg1.mydata.gps_longitude, sg1.mydata.gps_altitude)
    # set target
    eph.make_new_objekt("star", str(target))
    # get spherical position once, other method runs in a loop
    eph.get_pos_spherical_test(sg1)
    print(sg1.mycalc.ra_sp)
    print(sg1.mycalc.dec_sp)


def update_target():
    # gets current values of target and observe from db and sets them in local sg1
    new_sg1 = stargate.objects.get(name='sg1')
    sg1.mystatus.observe = new_sg1.mystatus.observe
    sg1.mytarget.target = new_sg1.mytarget.target


def clear_mycalc():
    # clears mycalc values from local sg1 object, we don't want to send these to the browser in manual mode
    sg1.mycalc.ra_sp = 0.0
    sg1.mycalc.ra_sp_steps = 0.0
    sg1.mycalc.ra_dir = '–'
    sg1.mycalc.dec_sp = 0.0
    sg1.mycalc.dec_sp_steps = 0.0
    sg1.mycalc.dec_dir = '–'


def store_and_send_data(save_to_db=False):
    # write current motor data to object
    sg1.mycalc.ra_av = sg1.motor_ra.get_steps()
    sg1.mycalc.dec_av = sg1.motor_dec.get_steps()
    sg1.mycalc.ra_deg = sg1.motor_ra.get_degree()
    sg1.mycalc.dec_deg = sg1.motor_dec.get_degree()

    #save in db only if save flag is true
    if save_to_db:
        sg1.mycalc.save()

    # send current motor data via channels
    # serialize mycalc object
    mycalc_dict = model_to_dict(sg1.mycalc)
    async_to_sync(channel_layer.group_send)(
        "motor-data", {
            "type": "motors.refresh",
            "text": json.dumps(mycalc_dict)
        })


###     MAIN    ###
## get sg1 object from db
sg1 = stargate.objects.get(name='sg1')
sg1.motor_dec = motor_dec((0x43c40000 + (0x2000 * 4)), 0x08, 0x0A)
sg1.motor_ra = motor_ra((0x43c40000 + (0x2000 * 4)), 0x09, 0x0B)

while True:
    update_target()

    ## OBSERVE MODE ##
    if sg1.mystatus.observe == "TRUE" and sg1.mytarget.target != "None":
        print('observe true, target set')
        eph = ephemeris_calculations(None, sg1.mydata.gps_latitude, sg1.mydata.gps_longitude, sg1.mydata.gps_altitude)
        eph.make_new_objekt("star", str(sg1.mytarget.target))


        print('starting threads')
        # calculation of the angles of the target
        threading_calc = threading.Thread(name='calc', target=eph.get_pos_spherical, args=(sg1, ))
        threading_calc.start()

        # starting the motors
        threading_ra = threading.Thread(name='ra', target=sg1.motor_ra.move_degree, args=(sg1.mycalc.ra_sp, 2,sg1))
        threading_ra.start()
        threading_dec = threading.Thread(name='dec', target=sg1.motor_dec.move_degree, args=(sg1.mycalc.dec_sp, 2, sg1))
        threading_dec.start()

        current_target = sg1.mytarget.target

        while sg1.mystatus.observe == "TRUE" and sg1.mytarget.target == current_target:
            print('observe true, target set')
            # check if status has changed in db
            update_target()

            # store calculations and send update via channels
            store_and_send_data(save_to_db=True)
            time.sleep(0.5)

        print('done observing, joining threads')
        threading_calc.join()
        threading_dec.join()
        threading_ra.join()
        time.sleep(0.5)

    ## MANUAL MODE ##
    elif sg1.mystatus.observe == "MANUAL":
        print('Manual mode')
        # clear mycalc values we don't want to send to the browser
        clear_mycalc()
        # check for manual motor control
        new_sg1 = stargate.objects.get(name='sg1')
        # set target values to current steps for while loop at the end
        if sg1.motor_ra.get_steps() != new_sg1.mycalc.ra_av:
            ra_target = new_sg1.mycalc.ra_av
            ra_current = sg1.motor_ra.get_steps()
            if ra_current < ra_target:
                direction = 1
                diff = ra_target - ra_current
            else:
                direction = 0
                diff = ra_current - ra_target
            sg1.motor_ra.move_steps(int(diff), 0, motor_speed, direction)
            time.sleep(0.7)

            store_and_send_data(save_to_db=False)

        if sg1.motor_dec.get_steps() != new_sg1.mycalc.dec_av:
            dec_target = new_sg1.mycalc.dec_av
            dec_current = sg1.motor_dec.get_steps()
            if dec_current < dec_target:
                direction = 1
                diff = dec_target - dec_current
            else:
                direction = 0
                diff = dec_current - dec_target
            sg1.motor_dec.move_steps(int(diff), 0, motor_speed, direction)
            time.sleep(0.7)

            store_and_send_data(save_to_db=False)

    ## STANDBY MODE ##
    else:
        # observe is neither MANUAL nor TRUE
        # print('waiting for command')
        pass

    time.sleep(0.5)