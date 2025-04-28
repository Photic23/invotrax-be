from rest_framework import serializers
from pengajuan_layanan_pasca_beli.models import ExchangeRequest
from pengajuan_penawaran_pengadaan.models import PengajuanPenawaranPengadaan

class ExchangeRequestSerializer(serializers.ModelSerializer):
    #uncomment this if error
    #pengajuan_detail = PengajuanPenawaranPengadaanSerializer(source='pengajuan', read_only=True)

    class PengajuanPenawaranPengadaanSerializer(serializers.ModelSerializer):
        class Meta:
            model = PengajuanPenawaranPengadaan
            fields = ["id", "nama_produk", "jumlah_produk", "deskripsi_produk"]

        
    class Meta:
        model = ExchangeRequest
        fields = '__all__'
        #fields = ['id', 'pengajuan', 'pengajuan_detail', 'alasan_penukaran', 'url_foto_penukaran', 'created_at']
        