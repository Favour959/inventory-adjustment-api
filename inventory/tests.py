from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from .models import Product, InventoryAdjustment


class InventoryAdjustTests(APITestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Blue Widget", stock=20)
        self.adjust_url = reverse('inventory-adjust')
        self.history_url = reverse('inventory-history')

    def test_positive_adjustment_increases_stock(self):
        response = self.client.post(self.adjust_url, {
            "product_id": self.product.id, "adjustment": 10, "reason": "New stock received",
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 30)

    def test_negative_adjustment_decreases_stock(self):
        response = self.client.post(self.adjust_url, {
            "product_id": self.product.id, "adjustment": -5, "reason": "Sold to customer",
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 15)

    def test_adjustment_cannot_make_stock_negative(self):
        response = self.client.post(self.adjust_url, {
            "product_id": self.product.id, "adjustment": -100, "reason": "Too much",
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 20)

    def test_reason_is_required(self):
        response = self.client.post(self.adjust_url, {
            "product_id": self.product.id, "adjustment": 5,
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('reason', response.data)

    def test_adjustment_cannot_be_zero(self):
        response = self.client.post(self.adjust_url, {
            "product_id": self.product.id, "adjustment": 0, "reason": "no-op",
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nonexistent_product_returns_400(self):
        response = self.client.post(self.adjust_url, {
            "product_id": 9999, "adjustment": 5, "reason": "test",
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_successful_adjustment_creates_history_record(self):
        self.assertEqual(InventoryAdjustment.objects.count(), 0)
        self.client.post(self.adjust_url, {
            "product_id": self.product.id, "adjustment": 10, "reason": "New stock received",
        }, format='json')
        self.assertEqual(InventoryAdjustment.objects.count(), 1)

    def test_failed_adjustment_does_not_create_history_record(self):
        self.client.post(self.adjust_url, {
            "product_id": self.product.id, "adjustment": -100, "reason": "Too much",
        }, format='json')
        self.assertEqual(InventoryAdjustment.objects.count(), 0)

    def test_history_endpoint_returns_all_adjustments(self):
        InventoryAdjustment.objects.create(product=self.product, adjustment=10, reason="First")
        InventoryAdjustment.objects.create(product=self.product, adjustment=-3, reason="Second")
        response = self.client.get(self.history_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_history_endpoint_rejects_post(self):
        response = self.client.post(self.history_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
