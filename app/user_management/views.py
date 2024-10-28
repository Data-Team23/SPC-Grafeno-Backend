from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from oauth2_provider.models import AccessToken, RefreshToken, Application
from oauth2_provider.settings import oauth2_settings
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import datetime, timedelta
import random
import string


def random_token_generator(request, length=40):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):        
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if not user:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        expire_seconds = oauth2_settings.user_settings['ACCESS_TOKEN_EXPIRE_SECONDS']
        scopes = ' '.join(oauth2_settings.user_settings['SCOPES'].keys())

        application = Application.objects.get(name="ApplicationName")

        expires = timezone.now() + timedelta(seconds=expire_seconds)
        access_token = AccessToken.objects.create(
            user=user,
            application=application,
            token=random_token_generator(request),
            expires=expires,
            scope=scopes
        )

        refresh_token = RefreshToken.objects.create(
            user=user,
            token=random_token_generator(request),
            access_token=access_token,
            application=application
        )

        user_info = user.decrypt_data()
        token = {
            'access_token': access_token.token,
            'token_type': 'Bearer',
            'expires_in': expire_seconds,
            'refresh_token': refresh_token.token,
            'scope': scopes,
            'user': user_info,
        }

        return Response(token, status=status.HTTP_200_OK)
