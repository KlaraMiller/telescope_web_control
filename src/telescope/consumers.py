# this script is asynchron
import json
import time
import os
from PIL import Image
import base64
from django.forms.models import model_to_dict

from channels.consumer import AsyncConsumer
from asgiref.sync import sync_to_async
from .motors import motor_dec, motor_ra
from channels.db import database_sync_to_async
from sensors.models import stargate
# calculations
from .calculations import ephemeris_calculations, calc_spherical_to_cartesian, calc_sp_corr, calc_T_corr

motor_speed = 5
motor_dec = motor_dec((0x43c40000 + (0x2000 * 4)), 0x08, 0x0A)  # motors are not part of the sg1 object
motor_ra = motor_ra((0x43c40000 + (0x2000 * 4)), 0x09, 0x0B)


class TelescopeConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connected", event)
        await self.send({
            "type": "websocket.accept"
        })

        placeholder_motor_data = await self.get_placeholder_motor_data()
        print(placeholder_motor_data)
        await self.send({
            "type": "websocket.send",
            "text": '{"command": "placeholder_motor_data", "motorData": ' + str(placeholder_motor_data) + '}'
        })

        await self.channel_layer.group_add("camera-data", self.channel_name)
        await self.channel_layer.group_add("motor-data", self.channel_name)

    async def websocket_receive(self, event):
        print("received", event)
        data = json.loads(event['text'])  # parses (extracts) text value of event into dictionary (key value pairs)
        # print(data['command'])
        if data['command'] == 'move_motor':
            await self.switch_observe_mode('MANUAL')
            await self.move_motor(data['direction'], 100)

        if data['command'] == 'set_polaris':
            # save to database
            await self.set_polaris()

        if data['command'] == 'alignment':
            # save to database
            await self.store_target(data)

        if data['command'] == 'observation':
            # save to database
            await self.store_target(data)

        if data['command'] == 'stop_observation':
            # clear target and observe status
            await self.switch_observe_mode('None')

        if data['command'] == 'refresh_image':
            await self.refresh_camera_image()

    async def websocket_disconnect(self, event):
        print("disconnected", event)
        await self.switch_observe_mode('None')
        await self.channel_layer.group_discard("camera-data", self.channel_name)
        await self.channel_layer.group_discard("motor-data", self.channel_name)

    async def camera_refresh(self, event):
        await self.refresh_camera_image()

    async def motors_refresh(self, event):
        print("Motor data received", event)
        await self.send({
            "type": "websocket.send",
            "text": '{"command": "refresh_motor_data", "motorData": ' + json.dumps(event['text']) + '}'
        })

    # updates camera image
    async def refresh_camera_image(self):
        print('refreshing camera image')
        image_string = await self.get_current_image_string()
        await self.send ({
            "type": "websocket.send",
            "text": '{"command": "refresh_image", "imageDataAsString": "' + image_string + '"}'
        })

    @sync_to_async
    def get_current_image_string(self):
        orig_image = Image.open('image.jpg')
        resized_image = orig_image.resize((640, 480))
        resized_image.save('image_small.jpg')

        with open('image_small.jpg', "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        return encoded_string.decode('ascii')

    @database_sync_to_async
    def move_motor(self, direction, steps):
        sg1 = stargate.objects.get(name='sg1')
        if direction == 'west':
            sg1.mycalc.ra_av -= steps
        if direction == 'north':
            sg1.mycalc.dec_av += steps
        if direction == 'south':
            sg1.mycalc.dec_av -= steps
        if direction == 'east':
            sg1.mycalc.ra_av += steps
        sg1.mycalc.save()

    @database_sync_to_async
    def store_target(self, data):
        sg1 = stargate.objects.get(name='sg1')
        sg1.mytarget.target = data['target']
        sg1.mystatus.observe = "TRUE"
        # if we are doing 3 star alignment, save star_nr as well
        if data['star_nr'] == 'star1':
            sg1.mytarget.star1 = data['target']
        if data['star_nr'] == 'star2':
            sg1.mytarget.star2 = data['target']
        if data['star_nr'] == 'star3':
            sg1.mytarget.star3 = data['target']
        sg1.mytarget.save()
        sg1.mystatus.save()

    @database_sync_to_async
    def set_polaris(self):
        sg1 = stargate.objects.get(name='sg1')
        sg1.mydata.set_polaris_ok = True
        sg1.mydata.save()

    @database_sync_to_async
    def switch_observe_mode(self, mode):
        sg1 = stargate.objects.get(name='sg1')
        sg1.mystatus.observe = mode
        sg1.mystatus.save()

        if mode == 'None':
            sg1.mytarget.target = "None"
            sg1.mytarget.save()

    @database_sync_to_async
    def get_placeholder_motor_data(self):
        sg1 = stargate.objects.get(name='sg1')
        sg1.mycalc.ra_sp = 0.0
        sg1.mycalc.ra_sp_steps = 0.0
        sg1.mycalc.ra_dir = '–'
        sg1.mycalc.dec_sp = 0.0
        sg1.mycalc.dec_sp_steps = 0.0
        sg1.mycalc.dec_dir = '–'
        return json.dumps(model_to_dict(sg1.mycalc))