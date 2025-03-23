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
    

    #TODO: OKE GW MAKIN STRES I DON'T THINK THIS IS HOW IT'S SUPPOSED TO BE... I think for updating overall i can use... update method above?
    # @action(detail=True, methods=['patch'])
    # def update_detail(self, request, pk=None):
    #     penawaran_pengadaan = get_object_or_404(PenawaranPengadaan, pk=pk, is_delete=False)
    #     user_role = request.user.role
    #     current_status = penawaran_pengadaan.status
    #     new_status = request.data.get('status')

    #     if user_role == 'vendor':
    #         if current_status.status == 'diajukan' and new_status in ['diproses', 'ditolak']:
    #             if new_status == 'diproses' and not request.data.get('tanggal_estimasi'):
    #                 return Response({'error':'Estimasi tanggal pengiriman produk butuh diisi untuk menyetujui request'}, status=status.HTTP_400_BAD_REQUEST)
    #             if new_status == 'diproses':
    #                 penawaran_pengadaan.tanggal_estimasi = request.data.get('tanggal_estimasi')     
    #         elif current_status == 'diproses' and new_status == 'dikirim':
    #             penawaran_pengadaan.tanggal_diterima_dikirim = timezone.now()
    #     elif user_role in ['manager', 'staff']:
    #         if current_status == 'dikirim' and new_status == 'diterima':
    #             penawaran_pengadaan.tanggal_diterima_dikirim = timezone.now()
    #     penawaran_pengadaan.status = new_status
    #     serializer = self.get_serializer(penawaran_pengadaan, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({'status': 'Request telah ' + new_status}, serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_penawaran_pengadaan(self, request, pk=None):
        penawaran_pengadaan = get_object_or_404(PenawaranPengadaan, pk=pk, is_deleted=False)
        penawaran_pengadaan.is_deleted = True
        penawaran_pengadaan.save()    
        return Response(status=status.HTTP_204_NO_CONTENT)