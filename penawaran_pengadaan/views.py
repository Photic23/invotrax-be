from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import PenawaranPengadaan
from .serializers import PenawaranPengadaanSerializer
from main.permissions import HasRolePermission

class PenawaranPengadaanViewSet(viewsets.ModelViewSet):
    # required_permission = 'vendor_permission'
    # permission_classes = [HasRolePermission]

    queryset = PenawaranPengadaan.objects.filter(is_deleted=False)
    serializer_class = PenawaranPengadaanSerializer

    def perform_create(self, serializer):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def daftar_penawaran_pengadaan(self, request): 
        penawaran_pengadaan_list = self.get_queryset()
        serializer = self.get_serializer(penawaran_pengadaan_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['patch'])
    def update_penawaran_pengadaan(self, request, pk=None):
        penawaran_pengadaan = get_object_or_404(PenawaranPengadaan, pk=pk, is_deleted=False)
        serializer = self.get_serializer(penawaran_pengadaan, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def detail_penawaran_pengadaan(self, request, pk=None):
        penawaran_pengadaan = get_object_or_404(PenawaranPengadaan, pk=pk, is_deleted=False)    
        serializer = self.get_serializer(penawaran_pengadaan)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)