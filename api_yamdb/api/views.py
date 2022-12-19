from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, mixins, generics, status
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

import datetime

from .filters import TitleFilter
from .permissions import IsAnonym
from .serializers import (
    CommentSerializer
    CategorySerializer,
    GenreSerializer,
    GetTokenSerializer,
    ReviewSerializer,
    TitleListRetrieveSerializer,
    TitleSerializer,
    SignUpSerializer,
    
)
from reviews.models import Category, Genre, Title, Review, Comment
from users.models import User

class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleListRetrieveSerializer
        return TitleSerializer


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

  
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        print(self.request.user)
        serializer.save(title=title,
                        author=self.request.user)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()  
      
      
  class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        print(self.request.user)
        serializer.save(review=review,
                        author=self.request.user)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()
    

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
