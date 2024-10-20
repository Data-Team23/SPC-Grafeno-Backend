from django.urls import path
from member.views import MemberListCreateAPIView, MemberDetailAPIView, GoogleLogin, GoogleCallback, LoginView, TwoFactorView

urlpatterns = [
    path("members/", MemberListCreateAPIView.as_view(), name="member-list-create"),
    path("members/<str:cpf>/", MemberDetailAPIView.as_view(), name="member-detail"),
    path("auth/google/", GoogleLogin.as_view(), name="google_login"),
    path("auth/callback/", GoogleCallback.as_view(), name="google_callback"),
    path("token/", LoginView.as_view(), name="login"),
    path("two-factor/", TwoFactorView.as_view(), name="two_factor"),
]
