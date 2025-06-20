from django.urls import path
from .views import GroupMemberCreateView

urlpatterns = [
    path('group-members/', GroupMemberCreateView.as_view(), name='group-member-create'),
]
