from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import MemberSerializer
from rest_framework.generics import RetrieveAPIView
from .serializers import UserDetailSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status

from management.permissions import IsAdminRole, IsMemberRole, IsAdminOrMember

User = get_user_model()

class MemberListView(ListAPIView):
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Ensure only admins can access this view
        if self.request.user.role == 'admin':
            return User.objects.filter(role='member')  # Filter users with role 'member'
        return User.objects.none()

class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only admins can access user details
        if self.request.user.role == 'admin':
            return super().get_queryset()
        return User.objects.none()

User = get_user_model()

class UnbanUserView(APIView):
    permission_classes = [IsAdminRole]

    def post(self, request, pk):
        """Unban a user."""
        try:
            user = User.objects.get(pk=pk)
            if user.is_banned:
                user.is_banned = False
                user.credit = 200.00  # Reset credit
                user.save()
                return Response({"message": f"User {user.username} has been unbanned."}, status=status.HTTP_200_OK)
            else:
                return Response({"message": f"User {user.username} is not banned."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

