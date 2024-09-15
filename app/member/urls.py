from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from .views import MemberListCreateAPIView, MemberDetailAPIView

urlpatterns = [
    path("members/", MemberListCreateAPIView.as_view(), name="member-list-create"),
    path("members/<str:pk>/", MemberDetailAPIView.as_view(), name="member-detail"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
