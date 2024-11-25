from rest_framework import serializers
from django.contrib.auth import get_user_model
from user_management.models import LGPDGeneralTerm, LGPDTermItem, LGPDUserTermApproval

User = get_user_model()


class TermApprovalSerializer(serializers.ModelSerializer):
    term_id = serializers.IntegerField(source='general_term.id')
    approved = serializers.SerializerMethodField()
    logs = serializers.CharField()

    class Meta:
        model = LGPDUserTermApproval
        fields = ['term_id', 'approved', 'approval_date', 'logs']

    def get_approved(self, obj):
        return 'Aprovação' in obj.logs


class UserSerializer(serializers.ModelSerializer):
    terms_approval = serializers.SerializerMethodField()
    decrypted_data = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'terms_approval',
            'decrypted_data',
        ]

    def get_terms_approval(self, obj):
        approvals = LGPDUserTermApproval.objects.filter(user=obj)
        return TermApprovalSerializer(approvals, many=True).data
    
    def get_decrypted_data(self, obj):
        return obj.decrypt_data()


class LGPDTermItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LGPDTermItem
        fields = ['id', 'title', 'content']


class LGPDGeneralTermSerializer(serializers.ModelSerializer):
    term_itens = LGPDTermItemSerializer(many=True)

    class Meta:
        model = LGPDGeneralTerm
        fields = ['id', 'title', 'content', 'term_itens']
