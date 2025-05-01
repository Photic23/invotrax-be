import datetime
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# class Supplier(models.Model):
#     nama = models.CharField(max_length=255, unique=True)
#     kontak = models.CharField(max_length=255, blank=True, null=True)
#     email = models.EmailField(blank=True, null=True)
#     alamat = models.TextField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.nama

# class Kategori(models.Model):
#     nama = models.CharField(max_length=255, unique=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     is_deleted = models.BooleanField(default=False)

#     def __str__(self):
#         return self.nama

class PengajuanPenawaranPengadaan(models.Model):
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
        related_name="pengajuan_requests"
    )
    # supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    nama_produk = models.CharField(max_length=255)
    # kategori_produk = models.ForeignKey(Kategori, on_delete=models.SET_NULL, null=True)
    jumlah_produk = models.PositiveIntegerField()
    deskripsi_produk = models.TextField(blank=True, null=True)
    url_foto_produk = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='diajukan')
    created_at = models.DateTimeField(auto_now_add=True)
    harga_diajukan = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    tanggal_estimasi = models.DateField(default=datetime.date.today)
    tanggal_diterima_dikirim = models.DateField(default=datetime.date.today)
    tanggal_garansi = models.DateField(null=True, blank=True)
    # updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.status == 'diterima' and not self.tanggal_garansi:
            self.tanggal_garansi = timezone.now().date() + datetime.timedelta(days=30)
        super().save(*args, **kwargs)

    @property
    def status_garansi(self):
        if self.tanggal_garansi and self.tanggal_garansi < timezone.now().date():
            return "Habis"
        return "Berlaku"
