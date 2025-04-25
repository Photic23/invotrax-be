from django.conf import settings
from django.db import models

from manajemen_stok.models import Kategori

# Create your models here.
class ExchangeRequest(models.Model):
    created_by = models.ForeignKey(         #to help identify the owner of each request 
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="exchange_requests"
    )

    nama_produk = models.CharField(max_length=255)
    # kategori_produk = models.ForeignKey(Kategori, on_delete=models.SET_NULL, null=True)
    jumlah_produk = models.PositiveIntegerField()
    deskripsi_produk = models.TextField(blank=True, null=True)
    alasan_penukaran = models.TextField(blank=False, null=False)
    url_foto_penukaran = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nama_produk} - {self.created_by} ({self.created_at.date()})"