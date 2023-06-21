from django.db import models
from django.conf import settings
from django.utils import timezone


# Create your models here.
class FriendList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='friends')


    def add_friend(self, account):
        if not account in self.friends.all():
            self.friends.add(account)
            self.save()


    def remove_friend(self, account):
        if account in self.friends.all():
            self.friends.remove(account)
            self.save()
    

    def unfriend(self, removee):
        # initiate the action of unfriending someone
        remover_friends_list = self # person terminating the friendship

        # remove friend from remover friend list
        remover_friends_list.remove_friend(removee)

        # remove friend from removee friend list
        friends_list = FriendList.objects.get(user=removee)
        friends_list.remove_friend(self.user)


    def is_mutual_friend(self, friend):
        # is this a friend
        if friend in self.friends.all():
            return True
        return False
    

    def __str__(self):
        return self.username


class FriendRequest(models.Model):
    # friend request consists of two parts: sender & receiver
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="receiver")
    is_active = models.BooleanField(blank=True, null=False, default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def accept(self):
        # accept and update both sender & receiver
        receiver_friend_list = FriendList.objects.get(user=self.receiver)

        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            sender_friend_list = FriendList.objects.get(user=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                self.is_active = False
                self.save()


    def decline(self):
        self.is_active = False
        self.save()


    def cancel(self):
        self.is_active = False
        self.save()


    def __str__(self):
        return self.username