from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PengajuanPenawaranPengadaanViewSet

# Register viewset with DefaultRouter
router = DefaultRouter()
router.register(r'pengajuan_penawaran_pengadaan', PengajuanPenawaranPengadaanViewSet, basename='pengajuanpenawaran')

urlpatterns = [
    path('', include(router.urls)),
]