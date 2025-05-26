from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Produk, Kategori
from .serializers import ProdukSerializer, KategoriSerializer
from main.permissions import HasRolePermission
from django.db.models import Sum

class ProdukViewSet(viewsets.ModelViewSet):
    required_permission = 'staff_permission'
    permission_classes = [HasRolePermission]

    queryset = Produk.objects.filter(is_deleted=False)
    serializer_class = ProdukSerializer

    def perform_create(self, serializer):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def total_stok(self, request):
        total = self.get_queryset().aggregate(total_stok=Sum('stok'))['total_stok'] or 0
        return Response({
            'total_stok': total,
            'jumlah_produk': self.get_queryset().count()
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def daftar_produk(self, request):
        produk_list = self.get_queryset()
        serializer = self.get_serializer(produk_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['patch'])
    def update_produk(self, request, pk=None):
        produk = get_object_or_404(Produk, pk=pk, is_deleted=False)
        serializer = self.get_serializer(produk, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def detail_produk(self, request, pk=None):
        produk = get_object_or_404(Produk, pk=pk, is_deleted=False)
        serializer = self.get_serializer(produk)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'])
    def hapus_produk(self, request, pk=None):
        produk = get_object_or_404(Produk, pk=pk, is_deleted=False)
        produk.is_deleted = True
        produk.save()
        return Response(status=status.HTTP_200_OK)

class KategoriViewSet(viewsets.ModelViewSet):
    required_permission = 'staff_permission'
    permission_classes = [HasRolePermission]

    queryset = Kategori.objects.filter(is_deleted=False)
    serializer_class = KategoriSerializer

    def perform_create(self, serializer):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:  # Jika hanya ingin mengizinkan view list atau retrieve
            self.required_permission = 'view_own_profile'
        return super().get_permissions()

    @action(detail=True, methods=['patch'])
    def update_kategori(self, request, pk=None):
        kategori = get_object_or_404(Kategori, pk=pk, is_deleted=False)
        serializer = self.get_serializer(kategori, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def daftar_kategori(self, request):
        kategori_list = self.get_queryset()
        serializer = self.get_serializer(kategori_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)