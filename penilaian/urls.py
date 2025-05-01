from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PenilaianViewSet

router = DefaultRouter()
router.register(r"rating", PenilaianViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
