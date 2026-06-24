from django.db import transaction
from django.shortcuts import get_object_or_404
from django.views import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, InventoryAdjustment
from .serializers import (
    InventoryAdjustmentRequestSerializer,
    InventoryAdjustmentSerializer,
)


class InventoryAdjustView(APIView):
    """
    POST /inventory/adjust

    Adjusts a product's stock up or down and records the change
    in the audit history table.
    """

    def post(self, request):
        request_serializer = InventoryAdjustmentRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        product_id = request_serializer.validated_data['product_id']
        adjustment = request_serializer.validated_data['adjustment']
        reason = request_serializer.validated_data['reason']

        with transaction.atomic():
            product = get_object_or_404(
                Product.objects.select_for_update(), id=product_id
            )

            new_stock = product.stock + adjustment
            if new_stock < 0:
                return Response(
                    {
                        "error": "Adjustment would result in negative stock.",
                        "current_stock": product.stock,
                        "requested_adjustment": adjustment,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            product.stock = new_stock
            product.save()

            record = InventoryAdjustment.objects.create(
                product=product,
                adjustment=adjustment,
                reason=reason,
            )

        output_serializer = InventoryAdjustmentSerializer(record)
        return Response(
            {
                "message": "Stock adjusted successfully.",
                "new_stock": product.stock,
                "adjustment": output_serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


class InventoryHistoryView(APIView):
    """
    GET /inventory/history

    Returns every adjustment ever made, newest first (see
    Meta.ordering on the model). Read-only by design -- this view
    only implements `get`, so POST/PUT/DELETE on this URL will
    automatically return 405 Method Not Allowed, courtesy of DRF.
    """

    def get(self, request):
        records = InventoryAdjustment.objects.select_related('product').all()
        serializer = InventoryAdjustmentSerializer(records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

