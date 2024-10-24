from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from member.models import Member
from member.serializers import MemberSerializer, MemberLoginSerializer
from django.conf import settings
from django.shortcuts import redirect
from urllib.parse import urlencode
from django.views import View
from django.contrib.auth import login
from member.utils.email import send_email
from bson import ObjectId

import requests
import jwt
import datetime
import random


class MemberListCreateAPIView(APIView):
    permission_classes = [AllowAny]  

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        otp_code = str(random.randint(100000, 999999))
        member_serializer = MemberSerializer(data=request.data)
        if member_serializer.is_valid():
            member = member_serializer.save(otp=otp_code)
            send_email(member.email, f"Seu código de verificação é: {otp_code}")
            
            return Response({
                "message": "Código de verificação enviado para o e-mail.",
                "member_id": member.id
            }, status=status.HTTP_200_OK)
        
        return Response(member_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        member_id = request.data.get("member_id")
        obj_id = ObjectId(member_id)
        otp_code = request.data.get("otp_code")
        
        try:
            member = Member.objects.get(_id=obj_id)
        except Member.DoesNotExist:
            return Response({"error": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        
        if member.otp != otp_code:
            return Response({"error": "Código OTP incorreto."}, status=status.HTTP_400_BAD_REQUEST)
        
        member.otp = None
        member.save()

        return Response({"message": "Verificação concluída. Usuário registrado com sucesso."}, status=status.HTTP_201_CREATED)


class MemberDetailAPIView(APIView):
    def get_object(self, cpf):
        queryset = Member.objects.filter(cpf=cpf)

        if queryset.exists():
            return queryset.first()
        return None

    def get(self, request, cpf, *args, **kwargs):
        member = self.get_object(cpf)
        if not member:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MemberSerializer(member)
        return Response(serializer.data)

    def put(self, request, cpf, *args, **kwargs):
        member = self.get_object(cpf)
        if not member:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateMemberProfileSerializer(member, data=request.data)
        if serializer.is_valid():
            member = serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, cpf, *args, **kwargs):
        member = self.get_object(cpf)
        if not member:
            return Response(status=status.HTTP_404_NOT_FOUND)

        member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GoogleLogin(View):
    def get(self, request):
        google_auth_url = "https://accounts.google.com/o/oauth2/auth"
        params = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "response_type": "code",
            "scope": "openid email profile",
            "access_type": "offline",
            "prompt": "consent",
        }
        return redirect(f"{google_auth_url}?{urlencode(params)}")


class GoogleCallback(View):
    def get(self, request):
        code = request.GET.get("code")
        token_url = "https://oauth2.googleapis.com/token"
        token_data = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
            "code": code,
        }

        response = requests.post(token_url, data=token_data)
        token_json = response.json()
        access_token = token_json.get("access_token")

        user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        user_info_response = requests.get(user_info_url, headers={"Authorization": f"Bearer {access_token}"})
        user_info = user_info_response.json()

        member, created = Member.objects.get_or_create(
            username=user_info["email"],
            defaults={
                "first_name": user_info.get("given_name", ""),
                "last_name": user_info.get("family_name", ""),
                "email": user_info["email"],
            }
        )

        access_payload = {
            "id": str(member._id),
            "username": member.username,
            "email": member.email,
            "first_name": member.first_name,
            "last_name": member.last_name,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
            "iat": datetime.datetime.utcnow()
        }
        access_token_jwt = jwt.encode(access_payload, settings.SECRET_KEY, algorithm="HS256")

        refresh_payload = {
            "id": str(member._id),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
            "iat": datetime.datetime.utcnow()
        }
        refresh_token_jwt = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm="HS256")

        redirect_url = f"http://localhost:5173/?access={access_token_jwt}&refresh={refresh_token_jwt}"
        return redirect(redirect_url)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        member = Member.objects.filter(email=email).first()

        if member is None or not member.check_password(password):
            return Response({"error": "Usuário não encontrado ou senha incorreta."}, status=status.HTTP_404_NOT_FOUND)

        otp_code = str(random.randint(100000, 999999))
        member.otp = otp_code
        member.save()

        send_email(member.email, f"Seu código 2FA é: {otp_code}")

        return Response({"message": "Código de autenticação enviado."}, status=status.HTTP_200_OK)


class TwoFactorView(APIView):
    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("otp_code")
        member = Member.objects.filter(email=email).first()

        if member is None:
            return Response({"error": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        if code != member.otp:
            return Response({"message": "OTP inválido."}, status=status.HTTP_400_BAD_REQUEST)

        access_payload = {
            "id": str(member._id),
            "email": member.email,
            "first_name": member.first_name,
            "cpf": member.cpf,
            "contato": member.contato,
            "last_name": member.last_name,
            "is_admin": member.is_admin,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
            "iat": datetime.datetime.utcnow()
        }
        access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm="HS256")

        return Response({
            "access": access_token,
            "message": "Login bem-sucedido com autenticação de dois fatores."
        }, status=status.HTTP_200_OK)