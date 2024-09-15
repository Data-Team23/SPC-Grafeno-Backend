from rest_framework import serializers
from .models import Member

class MemberSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="_id", read_only=True)

    class Meta:
        model = Member
        fields = ["id", "username", "email", "first_name", "last_name", "password", "created_at", "updated_at"]
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
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        if "password" in validated_data:
            instance.set_password(validated_data["password"])
        instance.save()
        return instance
