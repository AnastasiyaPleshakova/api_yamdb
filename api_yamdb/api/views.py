from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework_simplejwt.tokens import Token
from django.core.mail import send_mail

from rest_framework import status
from rest_framework.response import Response

from .filters import TitleFilter
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    SignUpSerializer,
    GetTokenSerializer,
)
from .permissions import IsAnonym
from reviews.models import Category, Genre, Title
from users.models import User

from random import randint


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
    lookup_field = 'slug'


def send_message():
    global confirmation_code
    confirmation_code = randint(1000, 9999)
    send_mail(
        'Подтверждение email',
        f'Ваш код подтверждения: {confirmation_code}',
        'from@example.com',  # Это поле "От кого"
        ['to@exmaple.com'],  # Это поле "Кому"
        fail_silently=True,  # Сообщать об ошибках
    )
    return confirmation_code


class SignupViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [IsAnonym, ]

    def perform_create(self, serializer):
        send_message()
        serializer.save()


def get_tokens_for_user(user):
    token = Token.for_user(user)
    print(token)
    return {
        'token': str(token),
    }


class GetTokenViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = GetTokenSerializer
    permission_classes = [IsAnonym, ]
