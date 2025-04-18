from django.db import models
from django.conf import settings

class Kategori(models.Model):
    nama = models.CharField(max_length=255, unique=True)
    batas_stok_kritis = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.nama
    
class Produk(models.Model):
    nama = models.CharField(max_length=255)
    kategori = models.ForeignKey(Kategori, on_delete=models.SET_NULL, null=True)
    vendor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'vendor'}
    )
    kontrak = models.ForeignKey('manajemen_kontrak.Kontrak', on_delete=models.SET_NULL, null=True, blank=True)
    stok = models.PositiveIntegerField()
    deskripsi = models.TextField(blank=True, null=True)
    harga = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.nama