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
    
    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return PenawaranPengadaan.objects.none()
        if user.role in ['staff', 'admin']:
            return PenawaranPengadaan.objects.filter(is_deleted=False)
        elif user.role == 'vendor':
            return PenawaranPengadaan.objects.filter(
                is_deleted=False,
                supplier_vendor=user
            )
        else:
            return PenawaranPengadaan.objects.none()

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
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user 
        if user.role in ['staff', 'admin']:     # all staff allowed
            pass
        elif user.role == 'vendor' and instance.supplier_vendor == user:    # only allow owned
            pass
        elif instance.supplier_vendor is None and user.role in ['staff', 'admin']:
            pass
        else:
            return Response(
                {"error": "Not authorized to view this request."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

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