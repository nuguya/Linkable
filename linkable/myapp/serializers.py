from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from .models import Book,Recommend

User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "password","name","email")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["username"], validated_data["password"],validated_data["email"],validated_data["name"]
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "name")


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'autor', 'location', 'sellnum', 'description','node','imagesource')


class RecommendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommend
        fields = ('id', 'books', 'username')