from rest_framework import exceptions, serializers
from rest_framework.validators import UniqueValidator

from api_yamdb.settings import (ATTENTION_RESERVED_NAME, NAME_NOT_FOUND,
                                RESERVED_NAME)

from .models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        fields = (
            'id',
            'role',
            'username',
            'bio',
            'email',
            'first_name',
            'last_name',
        )
        model = User
        read_only_fields = ('role',)

    def validate_username(self, value):
        if value == RESERVED_NAME:
            raise serializers.ValidationError(ATTENTION_RESERVED_NAME)
        return value


class AdminSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = (
            'role',
            'username',
            'bio',
            'email',
            'first_name',
            'last_name',
        )

    def validate_username(self, value):
        if value == RESERVED_NAME:
            raise serializers.ValidationError(ATTENTION_RESERVED_NAME)
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200, required=True)
    confirmation_code = serializers.CharField(max_length=200, required=True)

    def validation(self, value):
        if value == RESERVED_NAME:
            raise serializers.ValidationError(ATTENTION_RESERVED_NAME)
        if not User.objects.filter(username=value).exists():
            raise exceptions.NotFound(NAME_NOT_FOUND)
        return value
