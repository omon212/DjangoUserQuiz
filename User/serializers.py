from rest_framework import serializers
from .models import UserModel
from .utils import validate_password_length


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['email', 'password']

    def validate_password(self, value):
        return validate_password_length(value)


class OTPCheckSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp_code = serializers.CharField(max_length=6)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
