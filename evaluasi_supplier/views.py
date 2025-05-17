from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import EvaluasiSupplierSerializer
from main.permissions import HasRolePermission

class EvaluasiSupplierViewSet(viewsets.ModelViewSet):
    required_permission = 'staff_permission'
    permission_classes = [HasRolePermission]
    serializer_class = EvaluasiSupplierSerializer

    def perform_create(self, serializer):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)