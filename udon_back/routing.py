from django.conf.urls import url

from channels.routing import ProtocolTypeRouter, URLRouter
from udon_back.consumers import SocketConsumer


application = ProtocolTypeRouter({

    'websocket': URLRouter([
        url("^ws/$", SocketConsumer),
    ]),
})
