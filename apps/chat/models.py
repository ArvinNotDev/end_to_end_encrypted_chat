from django.db import models
from uuid import uuid4
from django.conf import settings


class ChatRoom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255, blank=True, null=True)
    is_group = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name or str(self.id)


class GroupMember(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="members")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    encrypted_key = models.TextField(help_text="Encrypted group key with this user's public key")
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("room", "user")  # Prevent duplicate memberships

    def __str__(self):
        return f"{self.user.username} in {self.room}"


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ciphertext = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} @ {self.timestamp}"
