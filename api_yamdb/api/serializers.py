from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Genre, Review, Title, User
from django.utils import timezone


YEAR_VALIDATION_ERROR = 'Ошибка валидации года'
CREATE_DIFFERENT_NAME = 'Создайте другое имя'
SCORE_OUT_OF_RANGE = 'Оценка должна быть между 1 и 10'
ONE_REVIEW_ALLOWED = 'Разрешен только один отзыв на одно произведение'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('slug', 'name')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitlesSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = ('name', 'year', 'category',
                  'genre', 'id', 'description', 'rating')

    def get_score(self, obj):
        pass


class TitleCreateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )

    class Meta:
        model = Title
        fields = ('name', 'year', 'category', 'genre', 'id', 'description')

    def validate_year(self, obj):
        year = timezone.now().year
        if not 0 <= obj <= year:
            raise serializers.ValidationError(YEAR_VALIDATION_ERROR)
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
    confirmation_code = serializers.CharField(required=True)
    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('confirmation_code', 'username',)


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username',)

    def validate_username(self, name):
        if name == 'me':
            raise serializers.ValidationError(CREATE_DIFFERENT_NAME)
        return name

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        many=False,
    )
    title = serializers.PrimaryKeyRelatedField(read_only=True)


    def validate(self, data):
        if (data.get('score') > 10 or data.get('score') < 1):
            raise serializers.ValidationError(SCORE_OUT_OF_RANGE)
        author = self.context['request'].user
        title = get_object_or_404(
            Title,
            id=self.context['request'].parser_context['kwargs'].get('title_id')
        )
        if (self.context['request'].method == 'POST'
                and title.reviews.filter(author=author).exists()):
            raise serializers.ValidationError(
                f'Отзыв на произведение {title.name} уже существует'
            )
        return data

    class Meta:
        fields = '__all__'
        model = Review
