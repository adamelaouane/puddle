from django.db import models
from item.models import Item
from django.contrib.auth.models import User 

from django.contrib.auth.models import User
from django.db import models

from item.models import Item


class Conversation(models.Model):
    item = models.ForeignKey(
        Item,
        related_name='conversations',
        on_delete=models.CASCADE
    )

    members = models.ManyToManyField(
        User,
        related_name='conversations'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-modified_at',)

    def __str__(self):
        return f"Conversation about {self.item.name}"


class ConversationMessage(models.Model):
    conversation = models.ForeignKey(
        Conversation,
        related_name='message',
        on_delete=models.CASCADE
    )

    content = models.TextField()

    # الوقت كيتسجل غير ملي كتتخلق الرسالة
    created_at = models.DateTimeField(auto_now_add=True)

    created_by = models.ForeignKey(
        User,
        related_name='created_message',
        on_delete=models.CASCADE
    )

    # المستخدمين اللي قراو هاد الرسالة
    read_by = models.ManyToManyField(
        User,
        related_name='read_conversation_messages',
        blank=True
    )

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return f"Message by {self.created_by.username}"