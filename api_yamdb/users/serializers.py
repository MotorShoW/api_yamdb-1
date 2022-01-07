from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username',
            'id',
            'first_name',
            'last_name',
            'email',
            'role',
            'bio',
        )
        model = User


class TokenSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)


class SignUpSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ('email',)
