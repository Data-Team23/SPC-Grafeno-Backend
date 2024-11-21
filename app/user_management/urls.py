from django.urls import path
from user_management.views import (
    LoginAPIView,
    RegisterUserAPIView,
    UserRetrieveUpdateDestroyAPIView,
    GeneralAndTermItemsAPIView,
    UserExportCSVAPIView,
    UserExportPDFAPIView,
)

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('register/', RegisterUserAPIView.as_view(), name='register'),
    path('me/', UserRetrieveUpdateDestroyAPIView.as_view(), name='user-detail'),
    path('term/', GeneralAndTermItemsAPIView.as_view(), name='term'),
    path('export-csv/', UserExportCSVAPIView.as_view(), name='export-csv'),
    path('export-pdf/', UserExportPDFAPIView.as_view(), name='export-pdf'),
]
