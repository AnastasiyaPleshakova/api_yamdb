from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken


from .filters import TitleFilter
from .permissions import (
    IsAdmin,
    IsAdminOrReadOnly,
    IsAllowAny,
    IsAnonymOrCanCorrect,
    IsUser,
)
from .serializers import (
    CommentSerializer
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    GetTokenSerializer,
    ReviewSerializer,
    SignUpSerializer,
    TitleListRetrieveSerializer,
    TitleSerializer,
    UsersSerializer,
)
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class CreateDestroyList(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    pass


@permission_classes([IsAdminOrReadOnly])
class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
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
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
    lookup_field = 'slug'


@permission_classes([IsAdminOrReadOnly])
class GenreViewSet(CreateDestroyList):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
    lookup_field = 'slug'


@permission_classes([IsAnonymOrCanCorrect])
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
        serializer.save(review=review,
                        author=self.request.user)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()


@permission_classes([IsAdmin])
class UsersViewSet(viewsets.ModelViewSet):
    # http_method_names = ['get', 'post', 'patch', 'del']
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(detail=False,
            methods=['patch', 'get'],
            url_path='me',
            permission_classes=[IsUser],
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
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        user = get_object_or_404(
            User, username=serializer.validated_data["username"])
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
@permission_classes([IsAllowAny])
def get_token_for_user(request):
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User, username=serializer.validated_data["username"])
    if default_token_generator.check_token(
            user, serializer.validated_data["confirmation_code"]):
        token = AccessToken.for_user(user)
        return Response({"token": str(token)}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
