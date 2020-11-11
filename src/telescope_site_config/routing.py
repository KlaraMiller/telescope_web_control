from django.conf.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

from sensors.consumers import SensorsConsumer   # NEVER ADD src. !!!
from telescope.consumers import TelescopeConsumer
# from sensors.consumers import NavConsumer

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    url('sensors/', SensorsConsumer),
                    url('telescope/', TelescopeConsumer),
                ]
            )
        )
    ),
    # 'channel': ChannelNameRouter({
    #     'nav-data': NavConsumer,
    # })
})