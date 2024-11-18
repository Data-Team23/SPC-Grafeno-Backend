from django.urls import path
from member.views import RFMClusterAPIView,MemberListCreateAPIView, MemberDetailAPIView, MemberLoginView, GoogleLogin, GoogleCallback, ExportCSVAPIView

urlpatterns = [
    path("members/", MemberListCreateAPIView.as_view(), name="member-list-create"),
    path("members/<str:cpf>/", MemberDetailAPIView.as_view(), name="member-detail"),
    path("token/", MemberLoginView.as_view(), name="api_login"),
    path("auth/google/", GoogleLogin.as_view(), name="google_login"),
    path("auth/callback/", GoogleCallback.as_view(), name="google_callback"),
    path("export_csv/<str:_id>/", ExportCSVAPIView.as_view(), name = "export_user_csv"),
    path("rfm-cluster/", RFMClusterAPIView.as_view(), name="rfm-cluster"),
]

