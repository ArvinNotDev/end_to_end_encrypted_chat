from django.contrib import admin
from .models import ChatRoom, GroupMember, Message

admin.site.register(ChatRoom)
admin.site.register(GroupMember)
admin.site.register(Message)
