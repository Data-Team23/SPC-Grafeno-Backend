from django.urls import path
from member.views import MemberListCreateAPIView, MemberDetailAPIView, MemberLoginView, GoogleLogin, GoogleCallback

urlpatterns = [
    path("members/", MemberListCreateAPIView.as_view(), name="member-list-create"),
    path("members/<str:pk>/", MemberDetailAPIView.as_view(), name="member-detail"),
    path("token/", MemberLoginView.as_view(), name="api_login"),
    path("auth/google/", GoogleLogin.as_view(), name="google_login"),
    path("auth/callback/", GoogleCallback.as_view(), name="google_callback"),
]

