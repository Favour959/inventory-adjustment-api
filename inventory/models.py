from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} (stock: {self.stock})"


class InventoryAdjustment(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='adjustments'
    )
    adjustment = models.IntegerField()
    reason = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.product_id}: {self.adjustment:+d} ({self.reason})"