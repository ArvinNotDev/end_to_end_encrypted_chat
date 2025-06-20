from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Message, GroupMember

User = get_user_model()

# Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'room', 'sender', 'ciphertext', 'timestamp']
        read_only_fields = ['id', 'sender', 'timestamp']

# Group Member Serializer
class GroupMemberSerializer(serializers.ModelSerializer):
    user = MinimalUserSerializer(read_only=True)

    class Meta:
        model = GroupMember
        fields = ['id', 'room', 'user', 'encrypted_key', 'joined_at']
        read_only_fields = ['id', 'joined_at']
