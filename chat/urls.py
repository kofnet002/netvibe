from django.urls import path
from .views import index, create_room, send_message_view


urlpatterns = [
    path('', index, name='home'),
    path('chat/<str:id1>__<str:id2>/', send_message_view, name='send-msg-view'),
    # path('online/', send_message_view, name='online-status'),
    # path('api/create-room/<str:uuid>/', create_room, name='create-room'),
]