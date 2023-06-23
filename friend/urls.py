from django.urls import path
from .views import send_friend_request, friend_requests, accept_friend_request


urlpatterns = [
    path('friend/friend-request/', send_friend_request, name='friend-request'),
    path('friend/friend-request/<user_id>', friend_requests, name='view-friend-requests'),
    path('friend/accept-friend-request/<friend_request_id>', accept_friend_request, name='accept-friend-request'),
]