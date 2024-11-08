from rest_framework import serializers
from django.contrib.auth import get_user_model
from user_management.models import LGPDGeneralTerm, LGPDTermItem

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'cpf',
            'contato'
        ]


class LGPDTermItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LGPDTermItem
        fields = ['id', 'title', 'content']


class LGPDGeneralTermSerializer(serializers.ModelSerializer):
    term_itens = LGPDTermItemSerializer(many=True)

    class Meta:
        model = LGPDGeneralTerm
        fields = ['id', 'title', 'content', 'term_itens']
