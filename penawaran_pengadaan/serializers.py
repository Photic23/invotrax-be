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
    display_label = serializers.SerializerMethodField()

    kategori_produk = serializers.PrimaryKeyRelatedField(queryset=Kategori.objects.all(), write_only=True)
    supplier_vendor = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), write_only=True)

    kategori_produk_detail = KategoriSerializer(source='kategori_produk', read_only=True)
    supplier_vendor_detail = VendorSerializer(source='supplier_vendor', read_only=True)

    class Meta:
        model = PenawaranPengadaan
        fields = ['id', 'nama_produk', 'kategori_produk', 'jumlah_produk', 'deskripsi_produk', 'url_foto_produk', 'harga_diajukan', 'tanggal_estimasi', 'tanggal_diterima_dikirim', 'status', 'created_at', 'is_deleted', 'kategori_produk_detail', 'supplier_vendor_detail', 'supplier_vendor', 'display_label']
    
    def get_display_label(self, obj):
        produk = obj.nama_produk or "-"
        qty = (
            obj.jumlah_produk
            if obj.jumlah_produk is not None
            else 0
        )
        vendor = (
            obj.supplier_vendor.company_name
            if obj.supplier_vendor and obj.supplier_vendor.company_name
            else "-"
        )
        return f"{produk} (Jumlah: {qty}) – {vendor} [ID {obj.id}]"