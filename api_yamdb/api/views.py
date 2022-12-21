from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .filters import TitleFilter
from .mixins import CreateDestroyList
from .permissions import (IsAdmin, IsAdminOrReadOnly, IsAllowAny,
                          IsAnonymOrCanCorrect)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, GetTokenSerializer,
                          ReviewSerializer, SignUpSerializer,
                          TitleListRetrieveSerializer, TitleSerializer,
                          UsersSerializer)
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


def get_object(self, model, object_id):
    return get_object_or_404(model, id=self.kwargs.get(object_id))


@permission_classes([IsAdminOrReadOnly])
class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg("reviews__score"))
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleListRetrieveSerializer
        return TitleSerializer


@permission_classes([IsAdminOrReadOnly])
class CategoryViewSet(CreateDestroyList):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@permission_classes([IsAdminOrReadOnly])
class GenreViewSet(CreateDestroyList):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


@permission_classes([IsAnonymOrCanCorrect])
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        title = get_object(self, Title, 'title_id')
        serializer.save(title=title,
                        author=self.request.user)

    def get_queryset(self):
        title = get_object(self, Title, 'title_id')
        return title.reviews.all()


@permission_classes([IsAnonymOrCanCorrect])
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        review = get_object(self, Review, 'review_id')
        serializer.save(review=review,
                        author=self.request.user)

    def get_queryset(self):
        review = get_object(self, Review, 'review_id')
        return review.comments.all()


@permission_classes([IsAdmin])
class UsersViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(detail=False,
            methods=['patch', 'get'],
            url_path='me',
            permission_classes=[permissions.IsAuthenticated],
            )
    def me(self, request):
        user = request.user
        if request.method == 'PATCH':
            serializer = UsersSerializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'GET':
            serializer = UsersSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAllowAny])
def signup(request):
    username = request.data.get('username')
    email = request.data.get('email')
    if User.objects.filter(username=username, email=email).exists():
        return Response(status=status.HTTP_200_OK)
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username']
    )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Подтверждение email',
        f'Ваш код подтверждения: {confirmation_code}',
        from_email='YandexTeam@example.com',
        recipient_list=[serializer.data['email']],
        fail_silently=True,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAllowAny])
def get_token_for_user(request):
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User, username=serializer.validated_data['username'])
    if default_token_generator.check_token(
            user, serializer.validated_data['confirmation_code']):
        token = AccessToken.for_user(user)
        return Response({"token": str(token)}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
