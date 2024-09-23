from rest_framework import serializers
from member.models import Member, LGPDTerm

class MemberSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="_id", read_only=True)

    class Meta:
        model = Member
        fields = ["id", "email", "first_name", "last_name", "password", "created_at", "updated_at"]
        extra_kwargs = {
            "password": {"write_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }

    def create(self, validated_data):
        user = Member(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get("email", instance.email)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        if "password" in validated_data:
            instance.set_password(validated_data["password"])
        instance.save()
        return instance


class MemberLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            member = Member.objects.get(email=email)
            
            if member.password:
                if not member.check_password(password):
                    raise serializers.ValidationError("Credenciais inválidas.")
            else:
                raise serializers.ValidationError(
                    "Este usuário pode ter se registrado usando o login do Google. Tente fazer login com Google."
                )

        except Member.DoesNotExist:
            raise serializers.ValidationError("Usuário não encontrado.")

        attrs["member"] = member
        return attrs


class LGPDTermSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="_id", read_only=True)

    class Meta:
        model = LGPDTerm
        fields = ["id", "user_email", "acceptance_date", "update_logs", "created_at"]
        extra_kwargs = {
            "acceptance_date": {"read_only": True},
            "created_at": {"read_only": True},
        }

    def create(self, validated_data):
        lgpd_term = LGPDTerm(**validated_data)
        lgpd_term.save()
        return lgpd_term

    def update(self, instance, validated_data):
        instance.user_email = validated_data.get("user_email", instance.user_email)
        instance.update_logs = validated_data.get("update_logs", instance.update_logs)
        instance.save()
        return instance