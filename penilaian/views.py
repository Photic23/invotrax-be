# penilaian/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Penilaian
from .serializers import PenilaianSerializer

class PenilaianViewSet(viewsets.ModelViewSet):
    queryset = Penilaian.objects.all()
    serializer_class = PenilaianSerializer

    @action(detail=False, methods=["get"], url_path="by_pengajuan/(?P<pengajuan_id>[^/.]+)")
    def by_pengajuan(self, request, pengajuan_id=None):
        try:
            penilaian = Penilaian.objects.get(pengajuan_id=pengajuan_id)
            serializer = self.get_serializer(penilaian)
            return Response(serializer.data)
        except Penilaian.DoesNotExist:
            return Response(None, status=status.HTTP_200_OK)
