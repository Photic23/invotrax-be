from rest_framework import serializers
from .models import PengajuanPenawaranPengadaan

class PengajuanPenawaranPengadaanSerializer(serializers.ModelSerializer):
    status_garansi = serializers.SerializerMethodField()

    class Meta:
        model = PengajuanPenawaranPengadaan
        fields = '__all__'

    def get_status_garansi(self, obj):
        return obj.status_garansi  # This calls your @property
