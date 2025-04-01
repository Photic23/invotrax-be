from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import PengajuanPenawaranPengadaan
from .serializers import PengajuanPenawaranPengadaanSerializer

class PengajuanPenawaranPengadaanViewSet(viewsets.ModelViewSet):
    queryset = PengajuanPenawaranPengadaan.objects.filter(is_deleted=False)
    serializer_class = PengajuanPenawaranPengadaanSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

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
    
    @action(detail=True, methods=['get'])
    def detail_pengajuan(self, request, pk=None):
        pengajuan_penawaran = get_object_or_404(PengajuanPenawaranPengadaan, pk=pk, is_deleted=False)
        serializer = self.get_serializer(pengajuan_penawaran)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)