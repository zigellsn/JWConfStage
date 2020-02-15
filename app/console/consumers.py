#  Copyright 2019 Simon Zigelli
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# from datetime import date

from channels.db import database_sync_to_async
from channels.exceptions import StopConsumer
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from console.models import Audit
# from get_times import extract
from stage.consumers import generate_channel_group_name


class ConsoleConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        # times = await extract(date.today(), date.today())
        await self.channel_layer.group_add(
            generate_channel_group_name("console", self.scope["url_route"]["kwargs"]["congregation"]),
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            generate_channel_group_name("console", self.scope["url_route"]["kwargs"]["congregation"]),
            self.channel_name
        )
        raise StopConsumer()

    async def receive_json(self, text_data, **kwargs):
        congregation_group_name = generate_channel_group_name("console",
                                                              self.scope["url_route"]["kwargs"]["congregation"])
        if text_data["alert"] == "message":
            await database_sync_to_async(self.get_name)(text_data)
        await self.channel_layer.group_send(congregation_group_name, {"type": "alert", "alert": text_data})

    async def exit(self, event):
        await self.send_json(event)

    async def alert(self, event):
        await self.send_json(event)

    def get_name(self, text_data):
        return Audit.objects.create_audit(self.scope["url_route"]["kwargs"]["congregation"],
                                          self.scope["user"].username, text_data["value"])
