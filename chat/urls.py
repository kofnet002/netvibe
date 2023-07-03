from django.urls import path
from .views import index, send_message_view


urlpatterns = [
    path('', index, name='home'),
    path('chat/<str:id1>__<str:id2>/', send_message_view, name='send-msg-view'),
]