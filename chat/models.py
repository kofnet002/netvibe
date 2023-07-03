from django.db import models
import uuid
from account.models import Account

# Create your models here.
class Message(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField()
    sent_by = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='msg_sender')
    receiver = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='msg_receiver')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created_at',)
    
    def __str__(self):
        return f"{self.sent_by}"
