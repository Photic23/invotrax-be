# penilaian/serializers.py
from rest_framework import serializers
from .models import Penilaian

class PenilaianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Penilaian
        fields = '__all__'

    def validate_penilaian(self, value):
        if Penilaian.objects.filter(pengajuan=value).exists():
            raise serializers.ValidationError("Penilaian for this pengajuan already exists.")
        return value
