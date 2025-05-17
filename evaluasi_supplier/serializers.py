from rest_framework import serializers
from .models import EvaluasiSupplier
from main.models import CustomUser

class EvaluasiSupplierSerializer(serializers.ModelSerializer):
    # Untuk Create/Update: hanya ID supplier
    supplier_vendor = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(role='vendor')
    )

    # Untuk output: tampilkan company name supplier
    supplier_company_name = serializers.SerializerMethodField(read_only=True)

    # Untuk output: hasil perhitungan rata-rata skor
    rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = EvaluasiSupplier
        fields = [
            'id', 'supplier_vendor', 'supplier_company_name',
            'created_at', 'updated_at',
            'kualitas_1', 'kualitas_2', 'kualitas_3', 'kualitas_4', 'kualitas_5',
            'harga_1', 'harga_2', 'harga_3',
            'pengiriman_1', 'pengiriman_2', 'pengiriman_3',
            'fleksibilitas_1', 'fleksibilitas_2', 'fleksibilitas_3',
            'responsif_1', 'responsif_2',
            'rating',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'supplier_company_name', 'rating']

    def get_supplier_company_name(self, obj):
        if obj.supplier_vendor:
            return obj.supplier_vendor.company_name
        return None

    def get_rating(self, obj):
        return obj.rating()