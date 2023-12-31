from django.db.models.signals import post_save
from django.dispatch import receiver
from account.models import Account
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

@receiver(post_save, sender=Account)
def send_onlineStatus(sender, instance, created, **kwargs):
    if not created:
        channel_layer = get_channel_layer()
        user_id = str(instance.id) # to serialize the uuid of the instance id / user id
        user_status = instance.is_online

        data = {
            'user_id': user_id,
            'online_status': user_status
        }

        async_to_sync(channel_layer.group_send)(
            # group room name for consumer
            'user',{
                'type': 'send_onlineStatus',
                'value': json.dumps(data)
            }
        )


@receiver(post_save, sender=Account)
def send_is_typing_status(sender, instance, created, **kwargs):
    if not created:
        channel_layer = get_channel_layer()
        user_id = str(instance.id)
        typing_status = instance.is_typing

        data = {
            'user_id': user_id,
            'typing_status': typing_status
        }

        async_to_sync(channel_layer.group_send)(
            'typing_status', {
                'type': 'send_is_typing_status',
                'value': json.dumps(data)
            }
        )