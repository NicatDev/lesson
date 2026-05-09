from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from shop.models import Category, Product

User = get_user_model()


def _rows(body):
    if isinstance(body, dict) and "results" in body:
        return body["results"]
    return body


class AdvancedProductSearchTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="adv_tester", password="testpass123")
        self.client.force_authenticate(user=self.user)
        self.cat = Category.objects.create(name="Adv cat", slug="adv-cat")
        Product.objects.create(
            name="Alpha unique adv",
            slug="adv-alpha",
            sku="ADV-ALPHA-1",
            price=Decimal("1.00"),
            stock=1,
            category=self.cat,
            is_active=True,
            description="foo",
        )
        Product.objects.create(
            name="Beta",
            slug="adv-beta",
            sku="ADV-BETA-2",
            price=Decimal("2.00"),
            stock=2,
            category=self.cat,
            is_active=False,
        )

    def test_search_param(self):
        r = self.client.get("/api/products/", {"search": "unique"})
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        rows = _rows(r.json())
        self.assertEqual(len(rows), 1)
        self.assertIn("Alpha", rows[0]["name"])

    def test_filter_is_active_and_ordering(self):
        r = self.client.get("/api/products/", {"is_active": "false", "ordering": "sku"})
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        rows = _rows(r.json())
        self.assertTrue(all(not x["is_active"] for x in rows))
