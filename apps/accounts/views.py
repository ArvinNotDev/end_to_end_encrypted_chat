from rest_framework import views, status, permissions, pagination
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from . import models, serializers


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.CustomTokenObtainPairSerializer


class UploadPublicKeyView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        public_key = request.data.get("public_key")
        if not public_key:
            return Response({"error": "Public key not provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        request.user.public_key = public_key
        request.user.save()
        return Response({"success": True, "message": "Public key uploaded."}, status=status.HTTP_200_OK)


class UserListView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    class CustomPagination(pagination.PageNumberPagination):
        page_size = 10
        page_size_query_param = 'page_size'

    def get(self, request):
        users = models.User.objects.all().order_by("-created_at")
        paginator = self.CustomPagination()
        paginated_users = paginator.paginate_queryset(users, request)
        serializer = serializers.UserSerializer(paginated_users, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_user(self, pk):
        try:
            return models.User.objects.get(id=pk)
        except models.User.DoesNotExist:
            return None

    def get(self, request, pk):
        user = self.get_user(pk)
        if not user:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.UserSerializer(user)
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        user = self.get_user(pk)
        if not user:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.UserViewSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_user(pk)
        if not user:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response({"success": True, "message": "User deleted successfully"}, status=status.HTTP_200_OK)
