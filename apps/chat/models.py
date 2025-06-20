from django.db import models
from uuid import uuid4
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class ChatRoom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(_("Room Name"), max_length=255, blank=True, null=True)
    is_group = models.BooleanField(_("Is Group Chat"), default=False)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    class Meta:
        verbose_name = _("Chat Room")
        verbose_name_plural = _("Chat Rooms")

    def __str__(self):
        return self.name or str(self.id)


class GroupMember(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="members", verbose_name=_("Chat Room"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("User"))
    encrypted_key = models.TextField(
        _("Encrypted Group Key"),
        help_text=_("Group key encrypted with this user's public key")
    )
    joined_at = models.DateTimeField(_("Joined At"), auto_now_add=True)

    class Meta:
        unique_together = ("room", "user")
        verbose_name = _("Group Member")
        verbose_name_plural = _("Group Members")

    def __str__(self):
        return f"{self.user.username} in {self.room}"


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages", verbose_name=_("Chat Room"))
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("Sender"))
    ciphertext = models.TextField(_("Ciphertext"))
    timestamp = models.DateTimeField(_("Timestamp"), auto_now_add=True)

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")

    def __str__(self):
        return f"Message from {self.sender.username} @ {self.timestamp}"
