from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TitleViewSet


router_v1 = DefaultRouter()
router_v1.register('titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
