import unittest
from tests import FlaskAppTestCase

class ProductsBlueprintTestCase(FlaskAppTestCase):
    def test_products_page(self):
        """Тест маршруту /products."""
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Laptop", response.data)

    def test_product_details_page(self):
        """Тест маршруту /products/1."""
        response = self.client.get("/products/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Laptop", response.data)

    def test_product_details_page_not_found(self):
        """Тест маршруту /products/999."""
        response = self.client.get("/products/4")
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()
