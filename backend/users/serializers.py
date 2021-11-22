from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Follow

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
        )

    def get_is_subscribed(self, obj):
        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj.id).exists()


class CustomUserCreateSerializer(UserCreateSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="Этот адрес почты уже используется",
            )
        ],
    )
    username = serializers.CharField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="Это имя пользователя уже используется",
            )
        ],
    )
    first_name = serializers.CharField(allow_blank=False)
    last_name = serializers.CharField(allow_blank=False)

    class Meta:
        model = User
        fields = ("email", "username", "first_name", "last_name", "password")
