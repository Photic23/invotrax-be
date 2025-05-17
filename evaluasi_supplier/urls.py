from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EvaluasiSupplierViewSet

router = DefaultRouter()
router.register(r'evaluasi-supplier', EvaluasiSupplierViewSet, basename='evaluasisupplier')

urlpatterns = [
    path('', include(router.urls)),
]
