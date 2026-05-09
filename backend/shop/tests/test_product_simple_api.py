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


class SimpleProductListTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="prod_tester", password="testpass123")
        self.client.force_authenticate(user=self.user)
        self.cat = Category.objects.create(name="Test cat", slug="test-cat-sp")
        Product.objects.create(
            name="Xüsusi axtarış məhsulu",
            slug="sp-search-1",
            sku="SKU-SP-1",
            price=Decimal("10.00"),
            stock=1,
            category=self.cat,
            is_active=True,
            description="unikal tesvir xyz",
        )
        Product.objects.create(
            name="Başqa məhsul",
            slug="sp-other",
            sku="SKU-SP-2",
            price=Decimal("5.00"),
            stock=2,
            category=self.cat,
            is_active=True,
        )

    def test_search_finds_by_name_or_description(self):
        r = self.client.get("/api/products/simple/", {"search": "Xüsusi"})
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        names = {p["name"] for p in _rows(r.json())}
        self.assertEqual(names, {"Xüsusi axtarış məhsulu"})

    def test_search_finds_by_sku(self):
        r = self.client.get("/api/products/simple/", {"search": "SKU-SP-2"})
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(_rows(r.json())), 1)
        self.assertEqual(_rows(r.json())[0]["sku"], "SKU-SP-2")

    def test_category_filter(self):
        r = self.client.get("/api/products/simple/", {"category": self.cat.pk})
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(_rows(r.json())), 2)
