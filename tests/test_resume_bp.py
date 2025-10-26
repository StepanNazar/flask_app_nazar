import unittest
from tests import FlaskAppTestCase

class ResumeBlueprintTestCase(FlaskAppTestCase):
    def test_resume_page(self):
        """Тест маршруту /resume."""
        response = self.client.get("/resume")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Resume", response.data)

    def test_contact_page(self):
        """Тест маршруту /contact."""
        response = self.client.get("/contact")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Contact", response.data)

if __name__ == "__main__":
    unittest.main()
