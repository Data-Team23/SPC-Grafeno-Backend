from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.models import AccessToken, RefreshToken, Application
from oauth2_provider.settings import oauth2_settings
from django.contrib.auth import authenticate, get_user_model
from django.utils import timezone
from datetime import timedelta
from user_management.serializers import UserSerializer
from user_management.models import (
    LGPDTermItem,
    LGPDGeneralTerm,
    LGPDUserTermApproval
)

import random
import string

User = get_user_model()


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
        user.login()
        token = {
            'access_token': access_token.token,
            'token_type': 'Bearer',
            'expires_in': expire_seconds,
            'refresh_token': refresh_token.token,
            'scope': scopes,
            'user': user_info,
        }

        return Response(token, status=status.HTTP_200_OK)


class RegisterUserAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        password = data.get("password")
        general_term_id = data.get("general_term_id")
        optional_terms = data.get("optional_terms", [])

        user = User(
            username=data.get("username"),
            email=data.get("email"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            cpf=data.get("cpf"),
            contato=data.get("contato"),
        )
        user.set_password(password)
        user.save()

        try:
            general_term = LGPDGeneralTerm.objects.get(id=general_term_id)
        except LGPDGeneralTerm.DoesNotExist:
            return Response({"detail": "Termo geral não encontrado."}, status=status.HTTP_400_BAD_REQUEST)

        LGPDUserTermApproval.objects.create(
            user=user,
            general_term=general_term,
            approval_date=timezone.now(),
            logs="Aprovação do termo geral durante o cadastro do usuário.",
        )

        for term in optional_terms:
            term_id = term.get("id")
            try:
                term_item = LGPDTermItem.objects.get(id=term_id)
                LGPDUserTermApproval.objects.create(
                    user=user,
                    general_term=general_term,
                    logs=f"Aprovação do termo opcional: {term_item.title}",
                    items_term=term_item,
                )
            except LGPDTermItem.DoesNotExist:
                continue

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        user = self.request.user
        data = self.request.data
        optional_terms = data.get("optional_terms", [])

        serializer.save()

        general_term_id = data.get("general_term_id")
        if general_term_id:
            try:
                general_term = LGPDGeneralTerm.objects.get(id=general_term_id)
            except LGPDGeneralTerm.DoesNotExist:
                return Response({"detail": "Termo geral não encontrado."}, status=status.HTTP_400_BAD_REQUEST)

            for term in optional_terms:
                term_id = term.get("id")
                approved = term.get("approved", False)

                try:
                    term_item = LGPDTermItem.objects.get(id=term_id)
                except LGPDTermItem.DoesNotExist:
                    continue

                approval, created = LGPDUserTermApproval.objects.update_or_create(
                    user=user,
                    items_term=term_item,
                    defaults={
                        'general_term': general_term,
                        'logs': f"{'Aprovado' if approved else 'Reprovado'} o termo opcional: {term_item.title}",
                        'approval_date': timezone.now(),
                    }
                )

        return Response({"detail": "Usuário e termos atualizados com sucesso."}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        self.perform_destroy(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)
