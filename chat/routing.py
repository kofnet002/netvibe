from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path('ws/chat/<str:auth_user_id>__<str:receiver_id>/', consumers.ChatConsumer.as_asgi()),
    path('ws/online/', consumers.OnlineStatusConsumer.as_asgi()),
    path('ws/typing/', consumers.TypingStatusConsumer.as_asgi()),
]