from rest_framework.routers import DefaultRouter
from django.urls import path, include
from pengajuan_layanan_pasca_beli.views import ExchangeRequestViewSet

router = DefaultRouter()
router.register(r'exchange-request', ExchangeRequestViewSet, basename='exchangerequest')

urlpatterns = [
    path('', include(router.urls)),
]
