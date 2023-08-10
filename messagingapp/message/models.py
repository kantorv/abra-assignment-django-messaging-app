from django.db import models
from core.models import User
import uuid
# Create your models here.



class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject = models.CharField(max_length = 255, default="New message")
    message = models.TextField(default="")
    created = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True)
    sender = models.ForeignKey(User, on_delete = models.SET_NULL, blank = True, null = True, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="received_messages")
    hide_for_sender = models.BooleanField(default=False)
    hide_for_receiver = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ["-created"]
