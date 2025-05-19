from rest_framework import serializers
from .models import Produk, Kategori
from main.models import CustomUser
from manajemen_kontrak.models import Kontrak
from manajemen_kontrak.serializers import KontrakSerializer

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'company_name']

class KategoriSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kategori
        fields = ['id', 'nama', 'batas_stok_kritis']

class ProdukSerializer(serializers.ModelSerializer):
    # Untuk Create: hanya menerima ID
    kategori = serializers.PrimaryKeyRelatedField(queryset=Kategori.objects.all(), write_only=True)
    vendor = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), write_only=True)
    kontrak = serializers.PrimaryKeyRelatedField(queryset=Kontrak.objects.all(), write_only=True)

    # Untuk Read: menampilkan ID & Nama
    kategori_detail = KategoriSerializer(source='kategori', read_only=True)
    vendor_detail = VendorSerializer(source='vendor', read_only=True)
    kontrak_detail = KontrakSerializer(source='kontrak',  read_only=True)

    class Meta:
        model = Produk
        fields = ['id', 'nama', 'kategori', 'vendor', 'kategori_detail', 'vendor_detail', 'kontrak', 'kontrak_detail', 'stok', 'harga', 'deskripsi']