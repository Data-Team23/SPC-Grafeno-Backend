from django.urls import path
from member.views import MemberListCreateAPIView, MemberDetailAPIView, MemberLoginView

urlpatterns = [
    path("members/", MemberListCreateAPIView.as_view(), name="member-list-create"),
    path("members/<str:pk>/", MemberDetailAPIView.as_view(), name="member-detail"),
    path("token/", MemberLoginView.as_view(), name='api_login'),
]

