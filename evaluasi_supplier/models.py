from django.db import models
from django.conf import settings

QUARTER_CHOICES = [
    (1, "Q1"), (2, "Q2"),
    (3, "Q3"), (4, "Q4"),
]

LIKERT_CHOICES = [(i, str(i)) for i in range(1, 6)]

class EvaluasiSupplier(models.Model):
    supplier_vendor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'vendor'}
    )
    tahun = models.PositiveIntegerField(null=True, editable=False)
    kuartal = models.PositiveIntegerField(
        choices=QUARTER_CHOICES,
        null=True,
        editable=False
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Skor Penilaian (Likert 1–5)
    # A. Kualitas
    kualitas_1 = models.IntegerField(choices=LIKERT_CHOICES)
    kualitas_2 = models.IntegerField(choices=LIKERT_CHOICES)
    kualitas_3 = models.IntegerField(choices=LIKERT_CHOICES)
    kualitas_4 = models.IntegerField(choices=LIKERT_CHOICES)
    kualitas_5 = models.IntegerField(choices=LIKERT_CHOICES)

    # B. Harga
    harga_1 = models.IntegerField(choices=LIKERT_CHOICES)
    harga_2 = models.IntegerField(choices=LIKERT_CHOICES)
    harga_3 = models.IntegerField(choices=LIKERT_CHOICES)

    # C. Pengiriman
    pengiriman_1 = models.IntegerField(choices=LIKERT_CHOICES)
    pengiriman_2 = models.IntegerField(choices=LIKERT_CHOICES)
    pengiriman_3 = models.IntegerField(choices=LIKERT_CHOICES)

    # D. Fleksibilitas
    fleksibilitas_1 = models.IntegerField(choices=LIKERT_CHOICES)
    fleksibilitas_2 = models.IntegerField(choices=LIKERT_CHOICES)
    fleksibilitas_3 = models.IntegerField(choices=LIKERT_CHOICES)

    # E. Responsif
    responsif_1 = models.IntegerField(choices=LIKERT_CHOICES)
    responsif_2 = models.IntegerField(choices=LIKERT_CHOICES)

    def __str__(self):
        return f"Evaluasi Supplier {self.supplier_vendor}"

    def rating(self):
        # Rata-rata semua score pada Likert Scale
        fields = [
            self.kualitas_1, self.kualitas_2, self.kualitas_3, self.kualitas_4, self.kualitas_5,
            self.harga_1, self.harga_2, self.harga_3,
            self.pengiriman_1, self.pengiriman_2, self.pengiriman_3,
            self.fleksibilitas_1, self.fleksibilitas_2, self.fleksibilitas_3,
            self.responsif_1, self.responsif_2,
        ]
        return round(sum(fields) / len(fields), 2)

    class Meta:
        unique_together = ['supplier_vendor', 'tahun', 'kuartal']
