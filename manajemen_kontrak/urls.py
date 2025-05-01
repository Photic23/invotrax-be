from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import KontrakViewSet

router = DefaultRouter()
router.register(r'kontrak', KontrakViewSet, basename='kontrak')

urlpatterns = [
    path('', include(router.urls)),
]
