# penilaian/models.py

from django.db import models
from pengajuan_penawaran_pengadaan.models import PengajuanPenawaranPengadaan  
from pengajuan_layanan_pasca_beli.models import ExchangeRequest    

class Penilaian(models.Model):
    pengajuan = models.ForeignKey(
        PengajuanPenawaranPengadaan,
        on_delete=models.CASCADE,
        related_name="penilaian"
    )
    exchange_request = models.OneToOneField(
        ExchangeRequest,
        on_delete=models.CASCADE,
        related_name="penilaian"
    )
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    deskripsi = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Penilaian #{self.id} - Rating: {self.rating}"
