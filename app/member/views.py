from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from member.models import Member, LGPDTerm
from member.serializers import MemberSerializer, MemberLoginSerializer, LGPDTermSerializer, UpdateMemberProfileSerializer
from django.conf import settings
from django.shortcuts import redirect
from urllib.parse import urlencode
from django.views import View
from django.http import HttpResponse
from bson import ObjectId

import requests
import jwt
import datetime
import csv

class ExportCSVAPIView(APIView):
    permission_classes = [AllowAny]  # Defina as permissões conforme necessário

    def get(self, request, *args, **kwargs):
        id_user = kwargs.get('_id')

        # Verifica se id_user é um ObjectId válido
        if not ObjectId.is_valid(id_user):
            return Response({"detail": "ID inválido."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Usa o ObjectId para buscar o membro
            member = Member.objects.get(_id=ObjectId(id_user))
        except Member.DoesNotExist:
            return Response({"detail": "Usuário não encontrado!"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": f"Erro interno: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Converte o objeto em dicionário
        serializer = MemberSerializer(member)
        data = serializer.data

        # Cria uma resposta HTTP com o CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{id_user}_data.csv"'

        # Cria um escritor CSV
        writer = csv.writer(response)

        # Escreve o cabeçalho (nomes das colunas)
        writer.writerow(data.keys())

        # Escreve os dados do membro
        writer.writerow(data.values())

        return response

class MemberListCreateAPIView(APIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [AllowAny]  

    def get(self, request, *args, **kwargs):
        members = Member.objects.all()
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        member_serializer = MemberSerializer(data=request.data)
        
        if member_serializer.is_valid():
            member = member_serializer.save()
            lgpd_data = {
                "user_email": member.email
            }
            lgpd_serializer = LGPDTermSerializer(data=lgpd_data)
            if lgpd_serializer.is_valid():
                lgpd_serializer.save()
            else:
                return Response(lgpd_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(member_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(member_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MemberDetailAPIView(APIView):
    def get_object(self, cpf):
        try:
            return Member.objects.get(cpf=cpf)
        except Member.DoesNotExist:
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

            LGPDTerm.objects.create(
                user_email=member.email,
                acceptance_date=datetime.datetime.utcnow()
            )

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, cpf, *args, **kwargs):
        member = self.get_object(cpf)
        if not member:
            return Response(status=status.HTTP_404_NOT_FOUND)

        LGPDTerm.objects.update_or_create(
            user_email=member.email,
            defaults={
                "acceptance_date": datetime.datetime.utcnow(),
                "update_logs": "Usuário optou por deletar sua conta."
            }
        )

        member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MemberLoginView(APIView):
    def post(self, request):
        serializer = MemberLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        member = serializer.validated_data["member"]
        
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

        refresh_payload = {
            "id": str(member._id),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
            "iat": datetime.datetime.utcnow()
        }
        refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm="HS256")

        return Response({
            "refresh": refresh_token,
            "access": access_token,
        }, status=status.HTTP_200_OK)


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
