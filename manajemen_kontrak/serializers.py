from rest_framework import serializers
from .models import Kontrak
from penawaran_pengadaan.models import PenawaranPengadaan
from penawaran_pengadaan.serializers import PenawaranPengadaanSerializer

MAX_FILE_SIZE = 10 * 1024 * 1024

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

    def validate(self, attrs):
        start = attrs.get("start_date", getattr(self.instance, "start_date", None))
        end   = attrs.get("end_date",   getattr(self.instance, "end_date",   None))
        if start and end and start >= end:
            raise serializers.ValidationError(
                {"end_date": "Tanggal berakhir harus lebih besar dari tanggal mulai."}
            )
        return attrs
    
    def validate_dokumen_kontrak(self, file):
        if not file.name.lower().endswith(".pdf"):
            raise serializers.ValidationError("Hanya file PDF yang diperbolehkan.")
        if file.size > MAX_FILE_SIZE:
            raise serializers.ValidationError("File terlalu besar, maksimum 10 MB.")
        return file

    def get_supplier_company_name(self, obj):
        if obj.penawaran and obj.penawaran.supplier_vendor:
            return obj.penawaran.supplier_vendor.company_name
        return None