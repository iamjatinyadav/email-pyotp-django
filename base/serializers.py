from rest_framework import serializers

from django.contrib.auth import get_user_model
from .otp import *
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=True)
    is_verified = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "password2", "is_verified"]
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "password field didn't match"})
        return attrs

    def create(self, validated_data):
        email = validated_data['email']

        # verified = validated_data['is_verified']
        # print(email)
        generate_otp(email)
        return {'email': email}





class VerifyAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()