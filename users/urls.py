from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import MemberListView, UserDetailView, UnbanUserView, MemberRegistrationView, AdminRegistrationView

urlpatterns = [
    path('register/member/', MemberRegistrationView.as_view(), name='register-member'),
    path('register/admin/', AdminRegistrationView.as_view(), name='register-admin'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('members/', MemberListView.as_view(), name='member-list'),
    path('members/<int:pk>/', UserDetailView.as_view(), name='member-detail'),
    path('unban/<int:pk>/', UnbanUserView.as_view(), name='unban-user'),
]
