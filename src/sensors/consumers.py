import json
from datetime import datetime
from dateutil import parser

from channels.consumer import AsyncConsumer
from .models import stargate
from channels.db import database_sync_to_async


class SensorsConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connected", event)
        await self.send({
            "type": "websocket.accept"
        })
        # receive data from group channel named 'sensor-data'
        await self.channel_layer.group_add("sensor-data", self.channel_name)    # channel_name is now member of group sensor-data
        # tell sensor_data.py to start sending updates
        await self.manage_sensor_data(True)

    async def websocket_receive(self, event):
        print("received", event)

        if 'storeNavData' in event['text']:
            json_data = json.loads(event['text'])   # unpack JSON-String as python object (dictionary w key-value-pairs)
            await self.store_nav_data(json_data['nav'])
            print('Store in database:', json_data['nav'])

        if 'storeGPSData' in event['text']:
            json_data = json.loads(event['text'])
            await self.store_gps_data(json_data['gps'])
            print('Store in database:', json_data['gps'])

    async def websocket_disconnect(self, event):
        print("disconnected", event)

        # remove channel_name
        await self.channel_layer.group_discard("sensor-data", self.channel_name)
        # tell sensor_data.py to stop sending updates
        await self.manage_sensor_data(False)

    async def sensor_refresh(self, event):
        await self.send({
            "type": "websocket.send",
            "text": event['text']
        })

    @database_sync_to_async
    def store_nav_data(self, data):
        sg1 = stargate.objects.get(name='sg1')
        sg1.mydata.nmod_nav_ok = True
        sg1.mydata.save()

    @database_sync_to_async
    def store_gps_data(self, data):
        sg1 = stargate.objects.get(name='sg1')
        sg1.mydata.gps_latitude = data['lat']
        sg1.mydata.gps_longitude = data['lon']
        sg1.mydata.gps_altitude = data['alt']
        sg1.mydata.gps_time = parser.isoparse(data['time'])
        sg1.mydata.nmod_gps_ok = True
        sg1.mydata.save()

    @database_sync_to_async
    def manage_sensor_data(self, read_sensor_data):
        sg1 = stargate.objects.get(name='sg1')
        if read_sensor_data:
            sg1.mystatus.read_sensor_data = True
        elif not read_sensor_data:
            sg1.mystatus.read_sensor_data = False
        sg1.mystatus.save()