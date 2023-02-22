from django.shortcuts import render
from rest_framework import generics
from .serializers import *
from .models import *
# Create your views here.
from rest_framework.response import Response
from rest_framework import status


class Register(generics.CreateAPIView):
    serializer_class = UserSerializer


class Varify(generics.GenericAPIView):
    serializer_class = VerifyAccountSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data['email']

            user = User.objects.get(email=email)
            print("views", user)
            user.is_verified = True
            user.save()
            return Response({
                'status': 200,
                'message': 'account verified',
                'data': {},
            })
        return Response({'data': serializer.errors})












