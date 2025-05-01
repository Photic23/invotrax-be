# penilaian/views.py
from rest_framework import viewsets
from .models import Penilaian
from .serializers import PenilaianSerializer

class PenilaianViewSet(viewsets.ModelViewSet):
    queryset = Penilaian.objects.all()
    serializer_class = PenilaianSerializer
