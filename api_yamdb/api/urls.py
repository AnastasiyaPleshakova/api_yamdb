from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet, TitleViewSet, SignupViewSet, GetTokenViewSet
)


router_v1 = DefaultRouter()
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', CategoryViewSet, basename='genres')
router_v1.register('auth/signup', SignupViewSet, basename='signup')
router_v1.register('auth/token', GetTokenViewSet, basename='token')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
