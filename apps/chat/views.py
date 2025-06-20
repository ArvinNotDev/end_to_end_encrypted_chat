from rest_framework import generics
from .models import Message
from .serializers import MessageSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import views, status
from rest_framework.response import Response
from .models import ChatRoom, GroupMember
from .serializers import GroupMemberSerializer, ChatRoomDetailSerializer, ChatRoomSerializer
from django.shortcuts import get_object_or_404

class SendMessageView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, room_id):
        room = get_object_or_404(ChatRoom, id=room_id)

        # Optional: Check if user is member of this room
        if not room.members.filter(user=request.user).exists():
            return Response({"error": "You are not a member of this room."}, status=status.HTTP_403_FORBIDDEN)

        # Add room field to data because serializer requires it
        data = request.data.copy()
        data['room'] = str(room_id)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(sender=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class GroupMemberCreateView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, room_id):
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


class ChatRoomCreateView(generics.CreateAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(admin=self.request.user)

class ChatRoomListView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rooms = ChatRoom.objects.filter(members__user=request.user).distinct()
        serializer = ChatRoomSerializer(rooms, many=True)
        return Response(serializer.data)
    
class ChatRoomDetailView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, room_id):
        room = get_object_or_404(ChatRoom, id=room_id)
        if not room.members.filter(user=request.user).exists():
            return Response({"error": "Access denied."}, status=403)
        serializer = ChatRoomDetailSerializer(room)
        return Response(serializer.data)
    
class MessageListView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, room_id):
        room = get_object_or_404(ChatRoom, id=room_id)
        if not room.members.filter(user=request.user).exists():
            return Response({"error": "Access denied"}, status=403)

        messages = room.messages.order_by('timestamp')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

class GroupMemberListView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, room_id):
        room = get_object_or_404(ChatRoom, id=room_id)
        if not room.members.filter(user=request.user).exists():
            return Response({"error": "Access denied."}, status=403)
        members = room.members.select_related('user')
        serializer = GroupMemberSerializer(members, many=True)
        return Response(serializer.data)
    

class GroupMemberDeleteView(views.APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, room_id, user_id):
        room = get_object_or_404(ChatRoom, id=room_id)
        if room.admin != request.user:
            return Response({"error": "Only admin can remove members."}, status=403)

        if str(room.admin_id) == str(user_id):
            return Response({"error": "Admin cannot remove themselves."}, status=400)

        member = GroupMember.objects.filter(room=room, user_id=user_id).first()
        if not member:
            return Response({"error": "User is not a member of this room."}, status=404)

        member.delete()
        return Response({"success": True, "message": "Member removed."}, status=200)
