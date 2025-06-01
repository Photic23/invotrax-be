from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import ExchangeRequest
from .serializers import ExchangeRequestSerializer 
from rest_framework.exceptions import PermissionDenied
# Create your views here.
class ExchangeRequestViewSet(viewsets.ModelViewSet):
    queryset = ExchangeRequest.objects.filter(is_deleted=False)
    serializer_class = ExchangeRequestSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)           #save who created particular request
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get_queryset(self):              #set only owner user/staff/admin/manager can view certain exchange request
        user = self.request.user
        if not user.is_authenticated:
            return ExchangeRequest.objects.none()
        if user.role in ['staff', 'admin', 'manager', 'owner']:
            return ExchangeRequest.objects.filter(is_deleted=False)
        elif user.role == 'customer':
            return ExchangeRequest.objects.filter(
                is_deleted=False,
                created_by=user
            )
        else:
            return ExchangeRequest.objects.none()
        
        
    def retrieve(self, request, pk=None):
        exchange_request = get_object_or_404(ExchangeRequest, pk=pk, is_deleted=False)
        
        user = request.user
        if user.role in ['staff', 'admin', 'manager', 'owner'] or exchange_request.created_by == user:       #set only owner user/staff/admin/manager can view certain exchange request
            serializer = self.get_serializer(exchange_request)
            return Response(serializer.data)
        raise PermissionDenied("You do not have permission to view this exchange request.")
        
    @action(detail=True, methods=['patch'])
    def update_exchange_request(self, request, pk=None):
        exchange_request = get_object_or_404(ExchangeRequest, pk=pk, is_deleted=False)
        serializer = self.get_serializer(exchange_request, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"], url_path="by_pengajuan/(?P<pengajuan_id>[^/.]+)")
    def by_pengajuan(self, request, pengajuan_id=None):
        try:
            exchange = ExchangeRequest.objects.get(pengajuan_id=pengajuan_id)
            serializer = self.get_serializer(exchange)
            return Response(serializer.data)
        except ExchangeRequest.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)
