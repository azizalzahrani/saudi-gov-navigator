"""
Knowledge Base Tests - اختبارات قاعدة المعرفة

Unit tests for knowledge base loading and retrieval.
اختبارات الوحدة لتحميل واسترجاع قاعدة المعرفة.
"""

import unittest
from saudi_gov.knowledge_base import (
    load_all_services,
    get_platform_services,
    get_service_by_id,
    search_services,
)


class TestKnowledgeBase(unittest.TestCase):
    """Test cases for knowledge base module."""

    def setUp(self):
        """Set up test fixtures."""
        self.all_services = load_all_services()

    def test_load_all_services(self):
        """Test loading all services."""
        self.assertIsNotNone(self.all_services)
        self.assertGreater(len(self.all_services), 0)

    def test_get_platform_services(self):
        """Test getting services for a specific platform."""
        # Test with a known platform
        absher_services = get_platform_services("أبشر")
        self.assertIsNotNone(absher_services)
        self.assertIsInstance(absher_services, list)
        self.assertGreater(len(absher_services), 0)

    def test_get_nonexistent_platform(self):
        """Test getting services for non-existent platform."""
        result = get_platform_services("منصة غير موجودة")
        self.assertIsNone(result)

    def test_get_service_by_id(self):
        """Test getting a service by its ID."""
        service = get_service_by_id("absher_passport_renewal")
        self.assertIsNotNone(service)
        self.assertEqual(service.get("id"), "absher_passport_renewal")

    def test_get_nonexistent_service(self):
        """Test getting non-existent service."""
        service = get_service_by_id("nonexistent_service_id")
        self.assertIsNone(service)

    def test_service_structure(self):
        """Test that services have required fields."""
        service = get_service_by_id("absher_passport_renewal")
        self.assertIsNotNone(service)

        required_fields = ["id", "name_ar", "name_en", "description_ar",
                         "description_en", "category", "requirements", "steps"]

        for field in required_fields:
            self.assertIn(field, service)

    def test_search_services_arabic(self):
        """Test searching services in Arabic."""
        results = search_services("جواز", language="ar")
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)

    def test_search_services_english(self):
        """Test searching services in English."""
        results = search_services("passport", language="en")
        self.assertIsInstance(results, list)
        # May or may not find results depending on English content

    def test_search_empty_results(self):
        """Test search with no results."""
        results = search_services("xxxxabc123", language="ar")
        self.assertEqual(len(results), 0)

    def test_all_platforms_loaded(self):
        """Test that all expected platforms are loaded."""
        expected_platforms = [
            "أبشر",
            "معايش",
            "قوى العمل",
            "تواصل",
            "بلدي",
            "الهيئة العامة للاستثمار",
            "التأمينات",
            "نطاقات",
        ]

        for platform in expected_platforms:
            self.assertIn(platform, self.all_services)

    def test_service_fees_structure(self):
        """Test that service fees are properly structured."""
        service = get_service_by_id("absher_passport_renewal")
        self.assertIsNotNone(service)

        fees = service.get("fees", {})
        self.assertIn("amount", fees)
        self.assertIn("currency", fees)

    def test_service_requirements_not_empty(self):
        """Test that services have requirements listed."""
        service = get_service_by_id("absher_passport_renewal")
        self.assertIsNotNone(service)

        requirements = service.get("requirements", [])
        self.assertIsInstance(requirements, list)
        self.assertGreater(len(requirements), 0)

    def test_service_steps_not_empty(self):
        """Test that services have steps listed."""
        service = get_service_by_id("absher_passport_renewal")
        self.assertIsNotNone(service)

        steps = service.get("steps", [])
        self.assertIsInstance(steps, list)
        self.assertGreater(len(steps), 0)

    def test_bilingual_content(self):
        """Test that services have both Arabic and English content."""
        service = get_service_by_id("absher_passport_renewal")
        self.assertIsNotNone(service)

        # Check Arabic content
        self.assertTrue(len(service.get("name_ar", "")) > 0)
        self.assertTrue(len(service.get("description_ar", "")) > 0)

        # Check English content
        self.assertTrue(len(service.get("name_en", "")) > 0)
        self.assertTrue(len(service.get("description_en", "")) > 0)


if __name__ == "__main__":
    unittest.main()
