from rest_framework import serializers
from custom_auth.models import CustomUser as User


class ReferredUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "referred_by",
            "date_joined",
        )


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "referral_code",
            "referred_by",
        )
        read_only_fields = (
            "id",
            "referral_code",
        )

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "referral_code",
            "referred_by",
            "date_joined",
        )
