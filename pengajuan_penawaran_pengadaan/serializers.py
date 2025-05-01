from rest_framework import serializers
from .models import PengajuanPenawaranPengadaan

class PengajuanPenawaranPengadaanSerializer(serializers.ModelSerializer):
    status_garansi = serializers.SerializerMethodField()

    class Meta:
        model = PengajuanPenawaranPengadaan
        fields = '__all__'

    # Make these fields optional in the serializer
    tanggal_estimasi = serializers.DateField(required=False)
    tanggal_diterima_dikirim = serializers.DateField(required=False)
    def get_status_garansi(self, obj):
        return obj.status_garansi  # This calls your @property
