from django.conf import settings
from django.db import models

from pengajuan_penawaran_pengadaan.models import PengajuanPenawaranPengadaan

class ExchangeRequest(models.Model):
    STATUS_CHOICES = [
        ('diajukan', 'Diajukan'),
        ('diproses', 'Diproses'),
        ('ditolak', 'Ditolak'),
        ('dikirim', 'Dikirim'),
        ('diterima', 'Diterima'),
    ]

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="exchange_requests"
    )
    pengajuan = models.OneToOneField(PengajuanPenawaranPengadaan, on_delete=models.CASCADE, null=True, blank=True)
    alasan_penukaran = models.TextField(blank=False, null=False)
    url_foto_penukaran = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='diajukan')
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.pengajuan} - {self.created_by} ({self.created_at.date()})"
