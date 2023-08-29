from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    dark = models.BooleanField(verbose_name="is_dark_theme", default=True)
    def __str__(self) -> str:
        return self.username

class Chat(models.Model):
    participants = models.ManyToManyField(User, related_name='users_in_chat')
    

class Message(models.Model):
    chat = models.ForeignKey(Chat, models.CASCADE, related_name='message_in')
    sender = models.ForeignKey(User, models.CASCADE, related_name='message_sender')
    message = models.CharField(max_length=5000)

    def __str__(self) -> str:
        return self.message[:20]
