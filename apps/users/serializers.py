from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from apps.users.models import User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class VerificationEmailSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'verification_code']
        extra_kwargs = {"password": {"write_only": True}}


class ForgotPasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(max_length=120)
    confirm_password = serializers.CharField(max_length=120)

    class Meta:
        model = User
        fields = ['email', 'new_password', 'confirm_password', 'verification_code']
        extra_kwargs = {"new_password": {"write_only": True},
                        "confirm_password": {"write_only": True},
                        "verification_code": {"write_only": True}}


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']


class ForgotChangePasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(max_length=120)
    confirm_password = serializers.CharField(max_length=120)

    class Meta:
        model = User
        fields = ['email', 'new_password', 'confirm_password', 'verification_code']
        extra_kwargs = {"new_password": {"write_only": True},
                        "confirm_password": {"write_only": True},
                        "verification_code": {"write_only": True}}


class ChangePasswordSerializers(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=55)

    class Meta:
        model = User
        fields = ['password', 'confirm_password']
        extra_kwargs = {
            'password': {"write_only": True},
            'confirm_password': {"write_only": True}
        }


class ForgotPasswordModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']
