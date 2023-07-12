from django.shortcuts import render
from .models import  Message
from account.models import Account

# Create your views here.
def send_message_view(request, *args, **kwargs):
    sender_id = kwargs.get('id1')
    receiver_id = kwargs.get('id2')

    receiver_obj = Account.objects.get(id=receiver_id)

    messages = Message.objects.all()

    # Filter the messages queryset to include only the relevant messages
    messages_queryset = messages.filter(
        sent_by_id=sender_id, receiver_id=receiver_id) | \
        messages.filter(sent_by_id=receiver_id, receiver_id=sender_id).order_by('created_at')
   
    context = {
        'receiver_id': receiver_id,
        'sender_id': sender_id,
        'messages_queryset': messages_queryset,
        'receiver_obj': receiver_obj,
    }
    return render(request, 'chat/inbox.html', context)