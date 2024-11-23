from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import MemberListView, UserDetailView, UnbanUserView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('members/', MemberListView.as_view(), name='member-list'),
    path('members/<int:pk>/', UserDetailView.as_view(), name='member-detail'),
    path('unban/<int:pk>/', UnbanUserView.as_view(), name='unban-user'),
]
