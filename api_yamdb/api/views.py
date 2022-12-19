from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, mixins, generics, status
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
import datetime

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


@api_view(['POST'])
@permission_classes([IsAnonym])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        user = get_object_or_404(User, username=serializer.validated_data["username"])
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            'Подтверждение email',
            f'Ваш код подтверждения: {confirmation_code}',
            'from@example.com',  # Это поле "От кого"
            ['to@exmaple.com'],  # Это поле "Кому"
            fail_silently=True,  # Сообщать об ошибках
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAnonym])
def get_token_for_user(request):
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User, username=serializer.validated_data["username"])
    if default_token_generator.check_token(user, serializer.validated_data["confirmation_code"]):
        token = AccessToken.for_user(user)
        return Response({"token": str(token)}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
