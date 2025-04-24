from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Kontrak
from .serializers import KontrakSerializer
from main.permissions import HasRolePermission


class KontrakViewSet(viewsets.ModelViewSet):
    required_permission = 'staff_permission'
    permission_classes = [HasRolePermission]

    queryset = Kontrak.objects.filter(is_deleted=False)
    serializer_class = KontrakSerializer

    def perform_create(self, serializer):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['patch'])
    def update_kontrak(self, request, pk=None):
        kontrak = get_object_or_404(Kontrak, pk=pk, is_deleted=False)
        serializer = self.get_serializer(kontrak, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def daftar_kontrak(self, request):
        kontrak_list = self.get_queryset()
        serializer = self.get_serializer(kontrak_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)