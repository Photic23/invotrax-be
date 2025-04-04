from rest_framework import serializers
from manajemen_stok.models import Kategori
from .models import PenawaranPengadaan
from main.models import CustomUser

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'company_name']

class KategoriSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kategori
        fields = ['id', 'nama']

class PenawaranPengadaanSerializer(serializers.ModelSerializer):
    kategori_produk = KategoriSerializer(read_only=True)
    supplier_vendor = VendorSerializer(read_only=True)

    class Meta:
        model = PenawaranPengadaan
        fields = '__all__'