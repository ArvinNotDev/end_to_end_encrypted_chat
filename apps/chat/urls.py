from django.urls import path
from .views import (
    ChatRoomCreateView, ChatRoomListView,
    MessageListView, SendMessageView,
    GroupMemberCreateView, GroupMemberListView, GroupMemberDeleteView
)

urlpatterns = [
    path('group-members/', GroupMemberCreateView.as_view(), name='group-member-create'),
    path('chatrooms/', ChatRoomListView.as_view(), name='chatroom-list'),
    path('chatrooms/create/', ChatRoomCreateView.as_view(), name='chatroom-create'),
    path('chatrooms/<uuid:room_id>/messages/', MessageListView.as_view(), name='message-list'),
    path('chatrooms/<uuid:room_id>/members/', GroupMemberListView.as_view(), name='member-list'),
    path('chatrooms/<uuid:room_id>/members/add/', GroupMemberCreateView.as_view(), name='member-add'),
    path('chatrooms/<uuid:room_id>/messages/send/', SendMessageView.as_view(), name='message-send'),
    path('chatrooms/<uuid:room_id>/members/<uuid:user_id>/remove/', GroupMemberDeleteView.as_view(), name='member-remove'),
    path('messages/send/', SendMessageView.as_view(), name='message-send'),
]
