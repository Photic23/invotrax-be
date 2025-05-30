import datetime
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from manajemen_stok.models import Kategori

class PengajuanPenawaranPengadaan(models.Model):
    STATUS_CHOICES = [
        ('diajukan', 'Diajukan'),
        ('diproses', 'Diproses'),
        ('ditolak', 'Ditolak'),
        ('dikirim', 'Dikirim'),
        ('diterima', 'Diterima'),
    ]

    # to save who is the owner
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pengajuan_requests"
    )

    supplier_vendor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'vendor'}
    )
    nama_produk = models.CharField(max_length=255)
    kategori_produk = models.ForeignKey(Kategori, on_delete=models.SET_NULL, null=True)
    jumlah_produk = models.PositiveIntegerField()
    deskripsi_produk = models.TextField(blank=True, null=True)
    url_foto_produk = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='diajukan')
    created_at = models.DateTimeField(auto_now_add=True)
    harga_diajukan = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    tanggal_estimasi = models.DateField(null=True, blank=True)
    tanggal_diterima_dikirim = models.DateField(null=True, blank=True)      #Variabel untuk pencatatan historis proses pengiriman dan penerimaan
    tanggal_garansi = models.DateField(null=True, blank=True)
    durasi_garansi = models.PositiveIntegerField(null=True, blank=True, help_text="Durasi garansi dalam hari")
    is_deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # When status changes to 'diterima', calculate tanggal_garansi
        if self.status == 'diterima' and not self.tanggal_garansi and self.durasi_garansi:
            # Use tanggal_diterima_dikirim as the base date, not current date
            if self.tanggal_diterima_dikirim:
                self.tanggal_garansi = self.tanggal_diterima_dikirim + datetime.timedelta(days=self.durasi_garansi)
            else:
                # Fallback to current date if tanggal_diterima_dikirim is not set
                self.tanggal_garansi = timezone.now().date() + datetime.timedelta(days=self.durasi_garansi)
        super().save(*args, **kwargs)
        
    @property
    def status_garansi(self):
        if self.tanggal_garansi and self.tanggal_garansi < timezone.now().date():           # check and update when accessed  
            return "Habis"
        return "Berlaku"
