from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import django

import argparse
import os
import sys
import time
import zwoasi as asi
#import Pillow

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "telescope_site_config.settings")
django.setup()
from sensors.models import stargate

## CHANNELS SETUP ##
channel_layer = get_channel_layer()

## CAMERA LIBRARY SETUP ##

## initialize camera library
def initialize_zwoasi():
    env_filename = '/usr/local/lib/libASICamera2.so'

    asi.init(env_filename)
    num_cameras = asi.get_num_cameras()

    if num_cameras == 0:
        print('No cameras found')
        sys.exit(0)

    cameras_found = asi.list_cameras()  # Models names of the connected cameras

    if num_cameras == 1:
        camera_id = 0
        print('Found one camera: %s' % cameras_found[0])
    else:
        print('Found %d cameras' % num_cameras)
        for n in range(num_cameras):
            print('    %d: %s' % (n, cameras_found[n]))
        # TO DO: allow user to select a camera
        camera_id = 0
        print('Using #%d: %s' % (camera_id, cameras_found[camera_id]))

    return camera_id

## CAMERA SETUP ##
def setup_camera(camera_id):
    camera = asi.Camera(camera_id)
    camera_info = camera.get_camera_property()

    # Get all of the camera controls
    print('')
    print('Camera controls:')
    controls = camera.get_controls()
    for cn in sorted(controls.keys()):
        print('    %s:' % cn)
        for k in sorted(controls[cn].keys()):
            print('        %s: %s' % (k, repr(controls[cn][k])))


    # Use minimum USB bandwidth permitted
    camera.set_control_value(asi.ASI_BANDWIDTHOVERLOAD, camera.get_controls()['BandWidth']['MinValue'])

    # Set some sensible defaults. They will need adjusting depending upon
    # the sensitivity, lens and lighting conditions used.
    camera.disable_dark_subtract()

    camera.set_control_value(asi.ASI_GAIN, 150)
    camera.set_control_value(asi.ASI_EXPOSURE, 30000)
    camera.set_control_value(asi.ASI_WB_B, 99)
    camera.set_control_value(asi.ASI_WB_R, 75)
    camera.set_control_value(asi.ASI_GAMMA, 50)
    camera.set_control_value(asi.ASI_BRIGHTNESS, 50)
    camera.set_control_value(asi.ASI_FLIP, 0)



    print('Enabling stills mode')
    try:
        # Force any single exposure to be halted
        camera.stop_video_capture()
        camera.stop_exposure()
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        pass

    # turn on high speed mode
    # camera.set_control_value(asi.ASI_HIGH_SPEED_MODE, 1)

    return camera


## MAIN ##
camera_id = initialize_zwoasi()
camera = setup_camera(camera_id)
camera.set_image_type(asi.ASI_IMG_RAW8)

while True:
    filename = 'image.jpg'
    try:
        camera.capture(filename=filename)
        async_to_sync(channel_layer.group_send)(
            "camera-data", {
                "type": "camera.refresh",
                "text": '{"image_file": "' + filename + '"}'
        })
        time.sleep(0.2)
    except asi.ZWO_CaptureError:
        print('Capture error')
        break
    except asi.ZWO_IOError:
        print('IO error')
        break

print('Shutting everything down')
try:
    # Force any single exposure to be halted
    camera.stop_video_capture()
    camera.stop_exposure()
except (KeyboardInterrupt, SystemExit):
    raise
except:
    pass

camera.close()
time.sleep(3)
sys.exit(1)