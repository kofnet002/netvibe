from django.urls import path
from .views import send_friend_request, friend_requests, accept_friend_request, remove_friend, decline_friend_request, cancel_friend_request, friend_list_view


urlpatterns = [
    path('friend/list/<user_id>', friend_list_view, name='list'),
    path('friend/friend-request/', send_friend_request, name='friend-request'),
    path('friend/friend-request/<user_id>/', friend_requests, name='view-friend-requests'),
    path('friend/accept-friend-request/<friend_request_id>/', accept_friend_request, name='accept-friend-request'),
    path('friend/decline-friend-request/<friend_request_id>/', decline_friend_request, name='decline-friend-request'),
    path('friend/cancel-friend-request/', cancel_friend_request, name='cancel-friend-request'),
    path('friend/remove-friend/', remove_friend, name='remove-friend'),
]