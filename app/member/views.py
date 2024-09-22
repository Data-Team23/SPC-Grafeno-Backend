from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from member.models import Member
from member.serializers import MemberSerializer, MemberLoginSerializer
from django.conf import settings

import jwt
import datetime


class MemberListCreateAPIView(APIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [AllowAny]  

    def get(self, request, *args, **kwargs):
        members = Member.objects.all()
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MemberDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Member.objects.get(pk=pk)
        except Member.DoesNotExist:
            return None

    def get(self, request, pk, *args, **kwargs):
        member = self.get_object(pk)
        if not member:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MemberSerializer(member)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        member = self.get_object(pk)
        if not member:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MemberSerializer(member, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        member = self.get_object(pk)
        if not member:
            return Response(status=status.HTTP_404_NOT_FOUND)
        member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MemberLoginView(APIView):
    def post(self, request):
        serializer = MemberLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        member = serializer.validated_data["member"]
        
        access_payload = {
            "id": str(member._id),
            "username": member.username,
            "email": member.email,
            "first_name": member.first_name,
            "last_name": member.last_name,
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
