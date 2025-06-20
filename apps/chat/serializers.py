from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Message, GroupMember, ChatRoom

User = get_user_model()

# Minimal user representation
class MinimalUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# Group Member Serializer
class GroupMemberSerializer(serializers.ModelSerializer):
    user = MinimalUserSerializer(read_only=True)

    class Meta:
        model = GroupMember
        fields = ['id', 'room', 'user', 'encrypted_key', 'joined_at']
        read_only_fields = ['id', 'joined_at']

# Optional: ChatRoom with nested members
class ChatRoomDetailSerializer(serializers.ModelSerializer):
    admin = MinimalUserSerializer(read_only=True)
    members = GroupMemberSerializer(many=True, read_only=True)

    class Meta:
        model = ChatRoom
        fields = ['id', 'name', 'is_group', 'admin', 'created_at', 'members']

# Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    sender = MinimalUserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'room', 'sender', 'ciphertext', 'timestamp']
        read_only_fields = ['id', 'sender', 'timestamp']

# Chat Room Serializer
class ChatRoomSerializer(serializers.ModelSerializer):
    admin = MinimalUserSerializer(read_only=True)

    class Meta:
        model = ChatRoom
        fields = ['id', 'name', 'is_group', 'admin', 'created_at']
        read_only_fields = ['id', 'admin', 'created_at']

