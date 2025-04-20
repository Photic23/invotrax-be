from rest_framework import serializers
from pengajuan_layanan_pasca_beli.models import ExchangeRequest

class ExchangeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeRequest
        fields = '__all__'