import base64

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
        # extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "password field didn't match"})
        return attrs

    def create(self, validated_data):
        email = validated_data['email']
        user = User.objects.create(email=email,)
        user.set_password(validated_data['password'])
        generate_otp(email)
        user.save()
        return user


class VerifyAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

    class Meta:
        model = User
        fields = ['email', 'otp']

    def validate(self, attrs):
        val = generate_verify_otp(attrs['email'])
        # token = val['token']
        # secret = base64.b32decode(token)
        # get_email = secret.decode()

        get_otp = val['OTP']
        user = User.objects.filter(email = attrs['email']).exists()
        if not user:
            raise serializers.ValidationError({"email": "User not register"})

        if get_otp != attrs['otp']:
            raise serializers.ValidationError({'otp': "Wrong Otp"})

        return attrs

    # def update(self, validated_data):
    #     email = validated_data["email"]
    #     user = User.objects.filter()



