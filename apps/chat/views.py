from rest_framework import generics
from .models import Message
from .serializers import MessageSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import views, status
from rest_framework.response import Response
from .models import ChatRoom, GroupMember
from .serializers import GroupMemberSerializer
from django.shortcuts import get_object_or_404

class SendMessageView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

class GroupMemberCreateView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        room_id = request.data.get("room")
        user_id = request.data.get("user")
        encrypted_key = request.data.get("encrypted_key")

        if not room_id or not user_id or not encrypted_key:
            return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

        room = get_object_or_404(ChatRoom, id=room_id)

        if not room.is_group:
            current_member_count = room.members.count()
            if current_member_count >= 2:
                return Response(
                    {"error": "Private rooms can only have 2 members."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        if GroupMember.objects.filter(room=room, user_id=user_id).exists():
            return Response(
                {"error": "User is already a member of this room."},
                status=status.HTTP_400_BAD_REQUEST
            )

        member = GroupMember.objects.create(
            room=room,
            user_id=user_id,
            encrypted_key=encrypted_key
        )
        serializer = GroupMemberSerializer(member)
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_201_CREATED)
