from django.urls import path
from .views import send_friend_request


urlpatterns = [
    path('friend/friend_request/', send_friend_request, name='friend-request'),
]