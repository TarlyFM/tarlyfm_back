from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import AsyncToSync
from urllib.parse import parse_qs
from djoser.conf import settings
import json
import random

def make_chat_message(message, username=None, user=None):
    if user:
        type_ = 'user'
    elif username:
        type_ = 'anon'
    else:
        type_ = 'server'
    return json.dumps({
        "action": "chat-message",
        "args": {
            "type": type_,
            "content": message,
            "username": username
        }
    })

def authenticate(token):
    return settings.TOKEN_MODEL.objects.get(key=token).user

class SocketConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        action = data.get('action', 'reject')
        args = data.get('args', {})

        if action == 'chat-join':
            AsyncToSync(self.channel_layer.group_add)("chat", self.channel_name)
            greetings = [
                "Wesh !",
                "Salam !",
                "Bien ou bien ?",
                "C'est comment ?",
                "What up booooooy ?"
            ]
            self.send(make_chat_message(random.choice(greetings)))

        elif action == 'chat-message':
            try:
                user = self.user
                username = self.username
            except:
                user = None
                username = None
            if username:
                content = args.get('content', '')
                AsyncToSync(self.channel_layer.group_send)(
                    "chat",
                    {
                        "type": "text",
                        "text": make_chat_message(content, username, user)
                    }
                )

        elif action == 'chat-anon-name':
            username = args.get('username', None)
            if type(username) == str and username:
                self.username = username
                self.user = None
                self.send(json.dumps({
                    "action": "chat-anon-name",
                    "args": {
                        "username": username
                    }
                }))

        elif action == 'auth':
            try:
                user = authenticate(args.get('token', ''))
                self.user = user.pk
                self.username = user.username
            except:
                self.send(json.dumps({"error": "bad token"}))

        elif action == 'upload-subscribe':
            AsyncToSync(self.channel_layer.group_add)(
                "upload-subscribe",
                self.channel_name
            )
        elif action == 'upload-unsubscribe':
            AsyncToSync(self.channel_layer.group_discard)(
                "upload-subscribe",
                self.channel_name
            )
        else:
            return

    def disconnect(self, close_code):
        AsyncToSync(self.channel_layer.group_discard)("chat", self.channel_name)
        AsyncToSync(self.channel_layer.group_discard)(
                "upload-subscribe",
                self.channel_name
            )
