from django.contrib import admin
from .models import Message
from django.contrib.auth.admin import UserAdmin



# Register your models here.
# class ChatAdmin(UserAdmin):
#     list_display=('sent_by', 'body', 'receiver', 'created_at')
#     search_fields=('body','sent_by', 'receiver')

#     filter_horizontal = ()
#     list_filter = ()
#     fieldsets = ()
#     ordering = ('uuid',)

    
admin.site.register(Message)
