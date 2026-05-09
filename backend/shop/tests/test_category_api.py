from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from shop.models import Category

User = get_user_model()


def _rows(response_data):
    """Səhifələnmiş və ya düz siyahı."""
    if isinstance(response_data, dict) and "results" in response_data:
        return response_data["results"]
    return response_data


class CategoryListFilterTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="api_tester", password="testpass123")
        self.client.force_authenticate(user=self.user)

        Category.objects.create(
            name="Tikinti materialları",
            slug="cat-tikinti-test",
            description="Test tikinti",
        )
        Category.objects.create(
            name="Elektronika",
            slug="cat-elek-test",
            description="Başqa kateqoriya",
        )
        Category.objects.create(
            name="Kosmetika",
            slug="cat-kosm-test",
            description="",
        )

    def test_search_tikinti_returns_only_matches(self):
        response = self.client.get("/api/categories/", {"search": "Tikinti"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = _rows(response.json())
        self.assertEqual(len(data), 1, data)
        self.assertIn("Tikinti", data[0]["name"])

    def test_search_slug_partial(self):
        response = self.client.get("/api/categories/", {"search": "elek"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        names = {row["name"] for row in _rows(response.json())}
        self.assertEqual(names, {"Elektronika"})

    def test_filter_name_param(self):
        response = self.client.get("/api/categories/", {"name": "Elek"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = _rows(response.json())
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "Elektronika")

    def test_without_search_returns_all_in_results(self):
        response = self.client.get("/api/categories/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertIn("count", body)
        self.assertIn("results", body)
        self.assertEqual(body["count"], 3)
        self.assertEqual(len(body["results"]), 3)

    def test_ordering_by_created_at_desc(self):
        response = self.client.get("/api/categories/", {"ordering": "-created_at"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = _rows(response.json())
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0]["slug"], "cat-kosm-test")

    def test_pagination_page_size(self):
        response = self.client.get("/api/categories/", {"page_size": "2", "page": "1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertEqual(len(body["results"]), 2)
        self.assertEqual(body["count"], 3)

    def test_requires_auth(self):
        self.client.force_authenticate(user=None)
        response = self.client.get("/api/categories/", {"search": "x"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
