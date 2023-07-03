from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import  Message
from account.models import Account

# Create your views here.
@login_required(login_url='/login')
def index(request):
    return render(request, 'chat/home.html')



def send_message_view(request, *args, **kwargs):
    sender_id = kwargs.get('id1')
    receiver_id = kwargs.get('id2')

    receiver_obj = Account.objects.get(id=receiver_id)

    # chatId = kwargs
  
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
        
        # 'room_name': f'private_chat_{sender_id}_{receiver_id}',
        # 'chatId': chatId,

    }
    return render(request, 'chat/inbox.html', context)