from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('user', 'title', 'author')


class UserSerializer(serializers.ModelSerializer):
    books = BookSerializer(read_only=True, many=True)

    class Meta:
        model = User

        fields = ('id', 'username', 'password', 'books')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}
