from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'room', 'sender', 'ciphertext', 'timestamp']
        read_only_fields = ['id', 'sender', 'timestamp']
