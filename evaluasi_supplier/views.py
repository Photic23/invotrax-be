from django.utils import timezone
from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from operator import itemgetter

from .models import EvaluasiSupplier
from .serializers import EvaluasiSupplierSerializer
from main.permissions import HasRolePermission
from manajemen_kontrak.models import Kontrak

QUARTER_MAP = {
    1: (1, 3),
    2: (4, 6),
    3: (7, 9),
    4: (10, 12),
}

class EvaluasiSupplierViewSet(viewsets.ModelViewSet):
    required_permission = 'staff_permission'
    permission_classes = [HasRolePermission]
    queryset = EvaluasiSupplier.objects.all()
    serializer_class = EvaluasiSupplierSerializer

    def perform_create(self, serializer):
        supplier = serializer.validated_data['supplier_vendor']
        today = timezone.localdate()
        current_year = today.year
        current_month = today.month
        current_quarter = (current_month - 1) // 3 + 1

        start_month, end_month = QUARTER_MAP[current_quarter]

        kontrak = (
            Kontrak.objects
                .filter(
                    penawaran__supplier_vendor=supplier,
                    is_deleted=False,
                    end_date__year=current_year,
                    end_date__month__gte=start_month,
                    end_date__month__lte=end_month,
                )
                .order_by('-end_date')
                .first()
        )

        if not kontrak:
            raise serializers.ValidationError("Supplier tidak memiliki kontrak aktif pada quarter ini.")

        tahun = kontrak.end_date.year
        kuartal = (kontrak.end_date.month - 1) // 3 + 1

        serializer.save(tahun=tahun, kuartal=kuartal)

    @action(detail=False, methods=['get'])
    def daftar_evaluasi(self, request):
        today = timezone.localdate()
        current_year = today.year
        current_month = today.month
        current_quarter = (current_month - 1) // 3 + 1

        try:
            year = int(request.GET.get('year', current_year))
            quarter = int(request.GET.get('quarter', current_quarter))
        except ValueError:
            return Response(
                {"error": "Parameter year atau quarter tidak valid"},
                status=status.HTTP_400_BAD_REQUEST
            )

        start_month, end_month = QUARTER_MAP.get(quarter, (1, 12))

        kontrak_queryset = Kontrak.objects.filter(
            end_date__year=year,
            end_date__month__gte=start_month,
            end_date__month__lte=end_month,
            is_deleted=False,
        )

        suppliers = {}
        for kontrak in kontrak_queryset:
            vendor = kontrak.penawaran.supplier_vendor
            if vendor and vendor.id not in suppliers:
                suppliers[vendor.id] = {
                    'supplier_id': vendor.id,
                    'supplier_company_name': vendor.company_name,
                }

        evaluated = []
        unevaluated = []
        for supplier_data in suppliers.values():
            evaluasi_supplier_queryset = EvaluasiSupplier.objects.filter(
                supplier_vendor_id=supplier_data['supplier_id'],
                tahun=year,
                kuartal=quarter,
            )
            if evaluasi_supplier_queryset.exists():
                evaluasi_supplier = evaluasi_supplier_queryset.first()
                evaluated.append({
                    'supplier_id': supplier_data['supplier_id'],
                    'supplier_company_name': supplier_data['supplier_company_name'],
                    'evaluation_id': evaluasi_supplier.id,
                    'rating': evaluasi_supplier.rating(),
                })
            else:
                unevaluated.append({
                    'supplier_id': supplier_data['supplier_id'],
                    'supplier_company_name': supplier_data['supplier_company_name'],
                })

        is_current = (year == current_year and quarter == current_quarter)

        evaluated.sort(key=itemgetter('rating'), reverse=True)
        for index, item in enumerate(evaluated, start=1):
            item['rank'] = index
            item['evaluation_allowed'] = False
            item['update_allowed'] = is_current

        for item in unevaluated:
            item['rating'] = '-'
            item['rank'] = '-'
            item['evaluation_allowed'] = is_current
            item['update_allowed'] = False

        return Response(evaluated + unevaluated, status=status.HTTP_200_OK)