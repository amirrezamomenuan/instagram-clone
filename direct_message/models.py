from django.db import models
from accounts.models import User, Profile

class Chat(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='is_sender')
    recipient = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='is_recipient')

    def __str__(self):
        name = self.sender.user.username + ' -> '+ self.recipient.user.username
        return name


class Message(models.Model):
    text_content = models.CharField(max_length=256)
    image_content = models.ImageField(blank = True, null=True)
    
    on_chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')

    status = models.BooleanField(default=True)

    def __str__(self):
        return self.text_content[:20]
    
    def delete_message(self):
        self.delete()
    
    def message_seen(self):
        self.seen = True
        self.save()
    
    @property
    def sender(self):
       return self.on_chat.sender

    @property
    def recipient(self):
        return self.on_chat.recipient 


    
