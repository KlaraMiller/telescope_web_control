from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import django
import json
import time
from evdev import InputDevice
import os
import math
import gpsd


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "telescope_site_config.settings")
django.setup()
from sensors.models import stargate

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
        k = float(self.y_max - self.y_min) / (self.x_max - self.x_min)
        # print((y_max-y_min))
        # print((x_max-x_min))
        # print(format(k, '.12f'))
        d = self.y_min - k * self.x_min
        # print(d)
        y = (k * x) + d
        # print(y)

        if (y >= self.y_max):
            y = self.y_max
        if (y <= self.y_min):
            y = self.y_min

        return y

    def get_value(self):
        os.system("echo 1 > " + self.enable)
        # dev.capabilities()
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


def get_degree(x, y, z):
    xAngle = math.atan2(x, (math.sqrt((y * y) + (z * z))))
    xAngle = xAngle * 180 / 3.141592

    yAngle = math.atan(y / (math.sqrt((x * x) + (z * z))))
    yAngle = yAngle * 180 / 3.141592

    zAngle = math.atan(math.sqrt((x * x) + (y * y)) / z)
    zAngle = zAngle * 180 / 3.141592
    return xAngle, yAngle, zAngle


def get_compass(x, y):
    if x == 0 and y < 0:
        d = 90
    elif x == 0 and y > 0:
        d = 0
    elif x != 0:
        d = math.atan((y), (x)) * 180 / 3.141592
        if d > 360:
            d = d - 360
        elif d < 0:
            d = d + 360
        else:
            d = d
    return d


def get_compass2(y, x):
    if x == 0 and y < 0:
        d = 90
    elif x == 0 and y > 0:
        d = 270
    elif x < 0:
        d = 180 - math.atan((y * 0.48828125) / (x * 0.48828125)) * 180 / 3.141592
    elif x > 0 and y < 0:
        d = (-1) * math.atan((y * 0.48828125) / (x * 0.48828125)) * 180 / 3.141592
    elif x > 0 and y > 0:
        d = 360 - math.atan((y * 0.48828125) / (x * 0.48828125)) * 180 / 3.141592
    return d


def get_compass3(x, y):
    if x == 0 and y < 0:
        d = 90
    elif x == 0 and y > 0:
        d = 0
    elif x != 0:
        d = math.atan2((y), (x)) * 180 / 3.141592 + 180
        if d > 360:
            d = d - 360
        else:
            d = d
    return d


def sensor_read(acc, mag, mode, kill, data):
    while not kill:
        acc_x = acc_y = acc_z = 0
        acc_x, acc_y, acc_z = acc.get_value()
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
            # pass
            time.sleep(0.03)  # set to whatever


def get_gps_data(gps_resp):
    dict = {
        'mode': str(gps_resp.mode or '–'),
        'sats': str(gps_resp.sats or '–')
    }

    if gps_resp.mode >= 2:
        dict['lat'] = str(gps_resp.lat or '–')
        dict['lon'] = str(gps_resp.lon or '–')
        dict['track'] = str(gps_resp.track or '–')
        dict['hspeed'] = str(gps_resp.hspeed or '–')
        dict['time'] = str(gps_resp.time or '–')
        dict['error'] = str(gps_resp.error or '–')
        dict['position'] = str(gps_resp.position() or '–')
        dict['speed'] = str(gps_resp.speed() or '–')
        dict['position_precision'] = str(gps_resp.position_precision() or '–')
        #dict['time_utc'] = str(gps_resp.time_utc())
        #dict['time_local'] = str(gps_resp.time_local())
        dict['map_url'] = str(gps_resp.map_url() or '–')

    if gps_resp.mode >= 3:
        dict['alt'] = str(gps_resp.alt or '–')
        dict['climb'] = str(gps_resp.climb or '–')
        dict['altitude'] = str(gps_resp.altitude() or '–')
        #dict['device'] = str(gps_resp.device())

    return dict


def send_update():
    sensor_read(acc, mag, 'single', kill, nav_data)
    json_data = '{"command": "refreshSensorData", "nav":' + json.dumps(nav_data) + ', "gps":' + json.dumps(
        get_gps_data(gpsd.get_current())) + '}'
    async_to_sync(channel_layer.group_send)(
        "sensor-data", {
            "type": "sensor.refresh",
            "text": json_data
        }
    )


# -----------------------------------------------------------------------------
# ----------------------------  main function ----------------------------
# -----------------------------------------------------------------------------

## MAIN ##

## CHANNELS SETUP ##
channel_layer = get_channel_layer()     # define Channel Layer

## NAV ##
acc = nmod_sensor('acc', '/dev/input/event1',
                              "/sys/class/spi_master/spi32766/spi32766.0/accelerometer/enable_device",
                              -2000000, 2000000, -2, 2)
mag = nmod_sensor('mag', '/dev/input/event0', "/sys/class/spi_master/spi32766/spi32766.1/enable_device",
                              -4000000,
                              4000000, -4, 4)
kill = []
nav_data = {'acc_x': 0.0, 'acc_y': 0.0, 'acc_z': 0.0, 'acc_xAngle': 0.0, 'acc_yAngle': 0.0, 'acc_zAngle': 0.0, 'direction': 0.0, 'mag_x': 0, 'mag_y': 0, 'mag_z': 0}

## GPS ##
gpsd.connect(host="127.0.0.1", port=2947)

while True:
    sg1 = stargate.objects.get(name='sg1')
    if sg1.mystatus.read_sensor_data:
        send_update()
        # print('update sent')
    # else:
        # print('update NOT sent')
    time.sleep(2)
