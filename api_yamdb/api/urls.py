from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, TitleViewSet, ReviewViewSet, CommentViewSet


router_v1 = DefaultRouter()
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', CategoryViewSet, basename='genres')
router_v1.register(
    r'titles/(?P<title_id>.+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>.+)/reviews/(?P<review_id>.+)/comments',
    CommentViewSet,
    basename='comments')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
