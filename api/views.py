from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['POST'])
    def register(self, request):
        print(request.data)

        username = request.data['username']
        password = request.data['password']
        # email = request.data['email']
        # first_name = request.data['first_name']
        # last_name = request.data['last_name']

        # if not username or not password or not email or not last_name:
        #     message = {'message': "Please Enter All Valid Fields"}
        #     return Response(message, status=status.HTTP_200_OK)

        search_username = User.objects.filter(username=username)

        if search_username:
            message = {'message': "Username Already Exists"}
            return Response(message, status=status.HTTP_200_OK)

        # if len(password) < 8:
        #     message = {'message': "Password Must Be Longer Than 8 Characters"}
        #     return Response(message, status=status.HTTP_200_OK)

        # if "@" not in email or ".com" not in email:
        #     message = {'message': "Enter A Valid Email"}
        #     return Response(message, status=status.HTTP_200_OK)

        user = User.objects.create_user(
            username=username, password=password)
        serializer = UserSerializer(user, many=False)
        token = Token.objects.create(user=user)
        message = {'message': "User Created",
                   'user': serializer.data, 'token': token.key}
        return Response(message, status=status.HTTP_200_OK)
