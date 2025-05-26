from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import PengajuanPenawaranPengadaan
from .serializers import PengajuanPenawaranPengadaanSerializer

class PengajuanPenawaranPengadaanViewSet(viewsets.ModelViewSet):
    queryset = PengajuanPenawaranPengadaan.objects.filter(is_deleted=False)
    serializer_class = PengajuanPenawaranPengadaanSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return PengajuanPenawaranPengadaan.objects.none()
        if user.role in ['staff', 'admin', 'manager']:          # staff/manager/admin allowed access all
            return PengajuanPenawaranPengadaan.objects.filter(is_deleted=False)
        elif user.role == 'customer':           # allow customer to view only owned object
            return PengajuanPenawaranPengadaan.objects.filter(
                is_deleted=False,
                created_by=user
            )
        else:
            return PengajuanPenawaranPengadaan.objects.none()

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def daftar_pengajuan_penawaran_pengadaan(self, request):
        pengajuan_penawaran_list = self.get_queryset()
        serializer = self.get_serializer(pengajuan_penawaran_list, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'], permission_classes=[permissions.AllowAny])
    def update_pengajuan_penawaran_pengadaan(self, request, pk=None):
        pengajuan_penawaran = get_object_or_404(PengajuanPenawaranPengadaan, pk=pk, is_deleted=False)
        serializer = self.get_serializer(pengajuan_penawaran, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user 
        if user.role in ['staff', 'admin', 'manager']:     # staff/admin/manager allowed to access all
            pass
        elif user.role == 'customer' and instance.created_by == user:    # allow customer to access only owned
            pass
        elif instance.created_by is None and user.role in ['staff', 'admin', 'manager']:        # in case no customer related
            pass
        else:
            return Response(
                {"error": "Not authorized to view this request."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def detail_pengajuan(self, request, pk=None):
        pengajuan_penawaran = get_object_or_404(PengajuanPenawaranPengadaan, pk=pk, is_deleted=False)
        user = request.user
        created_by = pengajuan_penawaran.created_by
        if user.role in ['staff', 'admin', 'manager']:     # staff/manager/admin allowed all
            pass
        elif user.role == 'customer' and created_by == user:    # allow customer to access only owned
            pass
        else:
            return Response(
                {"error": "Not authorized to view this request."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.get_serializer(pengajuan_penawaran)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)