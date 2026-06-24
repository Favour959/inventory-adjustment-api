from rest_framework import serializers
from .models import Product, InventoryAdjustment


class InventoryAdjustmentRequestSerializer(serializers.Serializer):
    """
    Validates the INCOMING request body for POST /inventory/adjust.

    We deliberately use a plain Serializer (not a ModelSerializer) here
    because this object does not map 1:1 to a model -- it represents
    a *request* to make a change, not the change record itself.
    The view will use this validated data to perform the actual
    business logic (checking stock, creating records, etc).
    """
    product_id = serializers.IntegerField()
    adjustment = serializers.IntegerField()
    reason = serializers.CharField(max_length=255, allow_blank=False)

    def validate_adjustment(self, value):
        if value == 0:
            raise serializers.ValidationError(
                "Adjustment cannot be zero -- it must increase or decrease stock."
            )
        return value

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError(
                f"Product with id {value} does not exist."
            )
        return value


class InventoryAdjustmentSerializer(serializers.ModelSerializer):
    """
    Serializes InventoryAdjustment MODEL INSTANCES for output.
    Used by:
      - GET /inventory/history (list of past adjustments)
      - the success response of POST /inventory/adjust

    This IS a ModelSerializer because it maps directly onto the
    InventoryAdjustment model -- one field per database column.

    Note the `product_id` field below: the model's actual field is
    called `product` and is a ForeignKey. DRF auto-generates a
    "product" field that outputs the related object's primary key.
    We rename it to `product_id` in the JSON output (via `source=`)
    so the API response matches the project spec exactly.
    """
    product_id = serializers.IntegerField(source='product.id', read_only=True)

    class Meta:
        model = InventoryAdjustment
        fields = ['id', 'product_id', 'adjustment', 'reason', 'created_at']
        read_only_fields = fields


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'stock']