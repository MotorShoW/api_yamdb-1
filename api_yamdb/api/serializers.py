from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from .models import Category, Genre, Titles, User
from django.utils import timezone


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'


class TitlesSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    score = SerializerMethodField()

    class Meta:
        model = Titles
        fields = '__all__'

    def get_score(self, obj):
        """Тут надо переход на рейтинг оформить, но часть B у нас пока в тумане где-то, думаю, лучше оставить на потом"""
        pass


class TitleCreateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )

    class Meta:
        model = Titles
        fields = '__all__'

    def validate_year(self, obj):
        year = timezone.now().year
        if not 0 <= obj <= year:
            raise serializers.ValidationError(
                'Ошибка валидации года'
            )
        return obj


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username',
            'email',
            'role',
            'first_name',
            'last_name',
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
