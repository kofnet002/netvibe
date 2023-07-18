from django.urls import path
from .views import index, save_post


urlpatterns = [
    path('', index, name='home'),
    path('save-post', save_post, name='save-post'),
]
