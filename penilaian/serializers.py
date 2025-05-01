# penilaian/serializers.py
from rest_framework import serializers
from .models import Penilaian

class PenilaianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Penilaian
        fields = '__all__'
