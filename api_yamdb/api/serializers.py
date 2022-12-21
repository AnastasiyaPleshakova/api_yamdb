import datetime

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from api_yamdb.settings import username_max_length, email_max_length
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id',)


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        slug_field='slug'
    )
    rating = serializers.FloatField(read_only=True, default=None)

    def validate_year(self, value):
        if value > datetime.datetime.now().year:
            raise serializers.ValidationError(
                f'Год выпуска {value} больше текущего'
            )
        return value

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'category', 'genre',
                  'rating')

    def to_representation(self, value):
        representation = super().to_representation(value)
        representation['category'] = CategorySerializer(value.category).data
        representation['genre'] = GenreSerializer(
            value.genre.all(), many=True).data
        return representation


class TitleListRetrieveSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.FloatField(default=0)

    class Meta:
        model = Title
        fields = (
            'id', 'name',
            'year', 'description',
            'category', 'genre', 'rating',
        )
        read_only_fields = (
            'id', 'name', 'year', 'description', 'category', 'genre', 'rating',
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    score = serializers.IntegerField(
        validators=[MinValueValidator(1,
                    message='Оценка не может быть меньше 1'),
                    MaxValueValidator(10,
                    message='Оценка не может быть больше 10')],
        default=5
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('title',)

    def validate(self, data):
        if (self.context['request'].method == 'POST' and Review.objects.filter(
                author=self.context['request'].user,
                title=self.context['request'].parser_context['kwargs'][
                    'title_id'])):
            raise serializers.ValidationError(
                'На одно произведение можно оставить лишь один отзыв!')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('review',)


class UsersSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=username_max_length,
        validators=[
            UnicodeUsernameValidator(),
            UniqueValidator(queryset=User.objects.all())],
    )

    class Meta:
        model = User
        fields = (
            'username', 'email',
            'first_name', 'last_name',
            'bio', 'role',
        )


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UnicodeUsernameValidator()],
        max_length=username_max_length,
    )
    email = serializers.EmailField(
        required=True,
        max_length=email_max_length,
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать "me" в качестве username')
        if value == '':
            raise serializers.ValidationError(
                'Поле "username" не должно быть пустым')
        return value

    def validate(self, data):
        bool_username = User.objects.filter(username=data['username']).exists()
        bool_email = User.objects.filter(email=data['email']).exists()
        if User.objects.filter(username=data['username'], email=data['email']):
            return data
        if (bool_username or bool_email):
            raise serializers.ValidationError(
                'Такое имя или почта уже существуют'
            )
        return data


class GetTokenSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField(required=False)
    username = serializers.CharField(required=True)
