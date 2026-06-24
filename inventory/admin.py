from django.contrib import admin
from .models import Product, InventoryAdjustment


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'stock')
    search_fields = ('name',)


@admin.register(InventoryAdjustment)
class InventoryAdjustmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'adjustment', 'reason', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('reason',)
    # This table is an audit log -- nobody should edit or delete
    # history through the admin. It should only ever be appended to.
    readonly_fields = ('product', 'adjustment', 'reason', 'created_at')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False