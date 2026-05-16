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


class AdvancedProductCategoryIdsFilterTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="cat_ids_tester", password="testpass123")
        self.client.force_authenticate(user=self.user)
        self.cat1 = Category.objects.create(name="Cat ids 1", slug="cat-ids-1")
        self.cat2 = Category.objects.create(name="Cat ids 2", slug="cat-ids-2")
        self.cat3 = Category.objects.create(name="Cat ids 3", slug="cat-ids-3")
        self.cat4 = Category.objects.create(name="Cat ids 4", slug="cat-ids-4")
        for index, category in enumerate((self.cat1, self.cat2, self.cat3, self.cat4), start=1):
            Product.objects.create(
                name=f"Category ids product {index}",
                slug=f"cat-ids-product-{index}",
                sku=f"CAT-IDS-{index}",
                price=Decimal("10.00"),
                stock=index,
                category=category,
                is_active=True,
            )

    def assert_category_ids_filter(self, query_string):
        r = self.client.get(f"/api/products/?{query_string}")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        category_ids = {row["category"] for row in _rows(r.json())}
        self.assertEqual(category_ids, {self.cat1.pk, self.cat2.pk, self.cat3.pk})

    def test_repeated_category_id_filter(self):
        self.assert_category_ids_filter(
            f"categoryId={self.cat1.pk}&categoryId={self.cat2.pk}&categoryId={self.cat3.pk}"
        )

    def test_comma_separated_category_ids_filter(self):
        self.assert_category_ids_filter(f"categoryIds={self.cat1.pk},{self.cat2.pk},{self.cat3.pk}")

    def test_bracket_category_ids_filter(self):
        self.assert_category_ids_filter(
            f"categoryIds[]={self.cat1.pk}&categoryIds[]={self.cat2.pk}&categoryIds[]={self.cat3.pk}"
        )

    def test_indexed_category_ids_filter(self):
        self.assert_category_ids_filter(
            f"categoryIds[0]={self.cat1.pk}&categoryIds[1]={self.cat2.pk}&categoryIds[2]={self.cat3.pk}"
        )

    def test_json_array_category_ids_filter(self):
        self.assert_category_ids_filter(f"categoryIds=[{self.cat1.pk},{self.cat2.pk},{self.cat3.pk}]")
