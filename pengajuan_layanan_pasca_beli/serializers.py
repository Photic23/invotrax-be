from rest_framework import serializers
from pengajuan_layanan_pasca_beli.models import ExchangeRequest
from pengajuan_penawaran_pengadaan.models import PengajuanPenawaranPengadaan
from pengajuan_penawaran_pengadaan.serializers import *
from django.contrib.auth import get_user_model

User = get_user_model()

class ExchangeRequestSerializer(serializers.ModelSerializer):
    pengajuan_detail = PengajuanPenawaranPengadaanSerializer(source='pengajuan', read_only=True)
    created_by_username = serializers.SerializerMethodField()
    
    class PengajuanPenawaranPengadaanSerializer(serializers.ModelSerializer):
        class Meta:
            model = PengajuanPenawaranPengadaan
            fields = ["id", "nama_produk", "kategori_produk", "jumlah_produk", "deskripsi_produk"]
    
    def get_created_by_username(self, obj):
        if obj.created_by:
            return obj.created_by.username
        return None
        
    class Meta:
        model = ExchangeRequest
        fields = '__all__'  # This includes the original created_by field with the ID