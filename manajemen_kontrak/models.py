from django.db import models
from penawaran_pengadaan.models import PenawaranPengadaan

class Kontrak(models.Model):
    STATUS_CHOICES = [
        ('Aktif', 'Aktif'),
        ('Nonaktif', 'Nonaktif'),
    ]

    penawaran = models.ForeignKey(
        PenawaranPengadaan,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    start_date = models.DateField()
    end_date = models.DateField()
    dokumen_kontrak = models.FileField(upload_to='dokumen_kontrak/')
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Aktif'
    )

    def __str__(self):
        return f"Kontrak {self.id}"
