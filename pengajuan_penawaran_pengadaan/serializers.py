from rest_framework import serializers
from .models import PengajuanPenawaranPengadaan
from main.models import CustomUser
from manajemen_stok.models import Kategori


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'company_name']

class KategoriSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kategori
        fields = ['id', 'nama']

class PengajuanPenawaranPengadaanSerializer(serializers.ModelSerializer):
    status_garansi = serializers.SerializerMethodField()
    kategori_produk = serializers.PrimaryKeyRelatedField(queryset=Kategori.objects.all(), write_only=True)
    supplier_vendor = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), write_only=True)

    kategori_produk_detail = KategoriSerializer(source='kategori_produk', read_only=True)
    supplier_vendor_detail = VendorSerializer(source='supplier_vendor', read_only=True)


    class Meta:
        model = PengajuanPenawaranPengadaan
        fields = '__all__'

    # Make these fields optional in the serializer
    tanggal_estimasi = serializers.DateField(required=False)
    tanggal_diterima_dikirim = serializers.DateField(required=False)
    def get_status_garansi(self, obj):
        return obj.status_garansi  # This calls your @property
