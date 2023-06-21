from django.urls import path
from .views import search_friend

urlpatterns = [
    path('/search/', search_friend, name='query')
]