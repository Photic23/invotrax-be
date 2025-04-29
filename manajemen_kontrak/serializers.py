from rest_framework import serializers
from .models import Kontrak
from penawaran_pengadaan.models import PenawaranPengadaan
from penawaran_pengadaan.serializers import PenawaranPengadaanSerializer


class KontrakSerializer(serializers.ModelSerializer):
    # Untuk Create/Update: hanya menerima ID penawaran
    penawaran = serializers.PrimaryKeyRelatedField(queryset=PenawaranPengadaan.objects.all(), write_only=True)

    # Untuk Read: menampilkan detail PenawaranPengadaan
    penawaran_detail = PenawaranPengadaanSerializer(source='penawaran', read_only=True)
    supplier_company_name = serializers.SerializerMethodField()

    class Meta:
        model = Kontrak
        fields = ['id', 'penawaran', 'penawaran_detail', 'supplier_company_name', 'start_date', 'end_date', 'dokumen_kontrak', 'created_at', 'is_deleted', 'status']
        read_only_fields = ['id', 'created_at', 'is_deleted']

    def validate_dokumen_kontrak(self, file):
        if not file.name.lower().endswith('.pdf'):
            raise serializers.ValidationError("Only PDF files are allowed.")
        return file

    def get_supplier_company_name(self, obj):
        if obj.penawaran and obj.penawaran.supplier_vendor:
            return obj.penawaran.supplier_vendor.company_name
        return None