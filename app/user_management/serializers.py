from rest_framework import serializers
from user_management.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'password',
            'cpf',
            'contato',
            'created_at',
            'updated_at',
            'last_login',
            'is_admin'
        ]
        
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User(**validated_data)
        user.save()
        return user
