from django.urls import path
from .views import InventoryAdjustView, InventoryHistoryView

urlpatterns = [
    path('adjust', InventoryAdjustView.as_view(), name='inventory-adjust'),
    path('history', InventoryHistoryView.as_view(), name='inventory-history'),  
]