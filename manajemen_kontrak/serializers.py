from rest_framework import serializers
from .models import Kontrak
from penawaran_pengadaan.models import PenawaranPengadaan
from penawaran_pengadaan.serializers import PenawaranPengadaanSerializer


class KontrakSerializer(serializers.ModelSerializer):
    # Untuk Create/Update: hanya menerima ID penawaran
    penawaran = serializers.PrimaryKeyRelatedField(queryset=PenawaranPengadaan.objects.all(), write_only=True)

    # Untuk Read: menampilkan detail PenawaranPengadaan
    penawaran_detail = PenawaranPengadaanSerializer(source='penawaran', read_only=True)

    class Meta:
        model = Kontrak
        fields = ['id', 'penawaran', 'penawaran_detail', 'start_date', 'end_date', 'dokumen_kontrak', 'created_at', 'is_deleted']
        read_only_fields = ['id', 'created_at', 'is_deleted']

    def validate_dokumen_kontrak(self, file):
        if not file.name.lower().endswith('.pdf'):
            raise serializers.ValidationError("Only PDF files are allowed.")
        return file
