import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .models import Message
from account.models import Account
from asgiref.sync import sync_to_async


# class ChatConsumer(AsyncJsonWebsocketConsumer):

#     async def connect(self):
#         # Get the user IDs from the URL
#         sender_id = self.scope['url_route']['kwargs']['auth_user_id']
#         receiver_id = self.scope['url_route']['kwargs']['receiver_id']

#         # Check if the users are friends or have a chat history
#         if not self.check_chat_history(sender_id, receiver_id):
#             # If they are not friends or have no chat history, close the connection
#             await self.close()
#             return

#         # Create a unique room name based on the user IDs
#         self.room_name = f'private_chat_{sender_id}__{receiver_id}'


#         # Join the room group
#         await self.channel_layer.group_add(
#             self.room_name,
#             self.channel_name
#         )

#         await self.accept()
        

#     async def disconnect(self, close_code):
#         # Leave the room group when the WebSocket closes
#         await self.channel_layer.group_discard(
#             self.room_name,
#             self.channel_name
#         )

#     async def receive_json(self, content):
#         # Handle incoming messages
#         command = content.get('command')
#         if command == 'send_message':
#             await self.send_message(content)

#     @sync_to_async
#     def get_account_instance(self, account_id):
#         # Retrieve the Account instance asynchronously
#         return Account.objects.get(id=account_id)

#     @sync_to_async
#     def save_message(self, sender, receiver, message):
#         # Save the message to the database asynchronously
#         return Message.objects.create(sent_by=sender, receiver=receiver, body=message)

#     @sync_to_async
#     def check_chat_history(self, sender_id, receiver_id):
#         # Implement your logic to check if the users have a chat history
#         # Return True if they have a chat history, otherwise False
#         # For example, you can check if there are any messages exchanged between the sender and receiver
#         return Message.objects.filter(sent_by_id=sender_id, receiver_id=receiver_id).exists()

#     @sync_to_async
#     def broadcast_message(self, message, sender_id, sender_username):
#         # Broadcast the message to the room group
#         self.channel_layer.group_send(
#             self.room_name,
#             {
#                 'type': 'chat_message',
#                 'message': message,
#                 'sender_id': str(sender_id),
#                 'sender_username': sender_username,
#             }
#         )

#     async def send_message(self, content):
#         message = content['message']
#         sender_id = content['sender_id']
#         receiver_id = content['receiver_id']

#         # Get the sender and receiver instances from the Account model asynchronously
#         sender = await self.get_account_instance(sender_id)
#         receiver = await self.get_account_instance(receiver_id)

#         # Save the message to the database
#         message = await self.save_message(sender, receiver, message)

#         # Broadcast the message to the room group
#         await self.broadcast_message(message.body, sender_id, sender.username)

#     async def chat_message(self, event):
#         # Send the message to the WebSocket
#         await self.send_json(event)


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        sender_id = self.scope['url_route']['kwargs']['auth_user_id']
        receiver_id = self.scope['url_route']['kwargs']['receiver_id']

        if sender_id > receiver_id:
            self.room_name = f"{sender_id}-{receiver_id}"
        else:
            self.room_name = f"{receiver_id}-{sender_id}"

        self.room_group_name = f'chat-{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
    

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data['message']
        sender_id = data['sender_id']
        receiver_id = data['receiver_id']


        # Get the sender and receiver instances from the Account model asynchronously
        sender = await self.get_account_instance(sender_id)
        receiver = await self.get_account_instance(receiver_id)

        # save messages to database
        await self.save_message(sender, message, receiver)


        await self.channel_layer.group_send(
            self.room_group_name,{
                'type': 'chat_message',
                'message': message,
                'sender_id': sender_id,
                'receiver_id': receiver_id
            }
        )
        

    # send message to friend
    async def chat_message(self, event):
        typing_status = event['type']
        message = event['message']
        sender_id = event['sender_id']
        receiver_id = event['receiver_id']

        await self.send(text_data=json.dumps({
            'typing_status': typing_status,
            'message': message,
            'sender_id': sender_id,
            'receiver_id': receiver_id
        }))

    async def disconnect(self, code):
        print(f"Disconnecting with code: {code}")
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_layer
        )
    

    @sync_to_async
    def save_message(self, sent_by, body, receiver):
        Message.objects.create(
            sent_by=sent_by,
            body=body,
            receiver=receiver,
        )
    

    @sync_to_async
    def get_account_instance(self, account_id):
        # Retrieve the Account instance asynchronously
        return Account.objects.get(id=account_id)


class OnlineStatusConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        # common/static group to allow users connected to it to know the 
        # online status of other users connected to this group
        self.room_group_name = 'user'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name    
        )
    
        await self.accept()


    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        data = json.loads(text_data)
        user_id = data['userId']
        connection_type = data['type']

        # save the necessary change to the database
        await self.change_online_status(user_id, connection_type)


    async def send_onlineStatus(self, event):
        data = json.loads(event.get('value'))
        user_id = str(data['user_id'])  # Convert UUID to string
        online_status = data['online_status']

        await self.send(text_data=json.dumps({
            'user_id': user_id,
            'online_status': online_status
        }))


    async def disconnect(self, message):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )
    

    @sync_to_async
    def change_online_status(self, use_id, connection_type):
        user = Account.objects.get(id=use_id)
        if connection_type == 'open':
            user.is_online = True
            user.save()
        else:
            user.is_online = False
            user.save()


class TypingStatusConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        # common/static group to allow users connected to it to know the 
        # typing status of other users connected to this group
        self.room_group_name = 'typing_status'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name    
        )
    
        await self.accept()


    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        data = json.loads(text_data)
        user_id = data['userId']
        connection_type = data['type']

        # save the necessary change to the database
        await self.change_typing_status(user_id, connection_type)


    async def send_is_typing_status(self, event):
        data = json.loads(event.get('value'))
        user_id = str(data['user_id'])  # Convert UUID to string
        typing_status = data['typing_status']

        await self.send(text_data=json.dumps({
            'user_id': user_id,
            'typing_status': typing_status
        }))


    async def disconnect(self, message):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )
    

    @sync_to_async
    def change_typing_status(self, use_id, connection_type):
        user = Account.objects.get(id=use_id)
        if connection_type == 'typing':
            user.is_typing = True
            user.save()
        else:
            user.is_typing = False
            user.save()