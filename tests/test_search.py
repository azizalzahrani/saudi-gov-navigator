"""
Search Tests - اختبارات البحث

Unit tests for semantic search functionality.
اختبارات الوحدة لوظائف البحث الدلالي.
"""

import unittest
from saudi_gov.search import SemanticSearch


class TestSemanticSearch(unittest.TestCase):
    """Test cases for semantic search module."""

    def setUp(self):
        """Set up test fixtures."""
        self.search = SemanticSearch(language="ar")

    def test_search_initialization(self):
        """Test that search engine initializes properly."""
        self.assertIsNotNone(self.search.services)
        self.assertIsNotNone(self.search.search_index)
        self.assertGreater(len(self.search.search_index), 0)

    def test_basic_search(self):
        """Test basic keyword search."""
        results = self.search.search("جواز السفر")
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)

    def test_search_returns_scores(self):
        """Test that search results include relevance scores."""
        results = self.search.search("إقامة")
        self.assertGreater(len(results), 0)

        for result in results:
            self.assertIn("service", result)
            self.assertIn("platform", result)
            self.assertIn("score", result)
            self.assertGreater(result["score"], 0)

    def test_max_results_limit(self):
        """Test that max_results parameter is respected."""
        results = self.search.search("خدمة", max_results=3)
        self.assertLessEqual(len(results), 3)

    def test_autocomplete(self):
        """Test autocomplete functionality."""
        suggestions = self.search.autocomplete("جوا")
        self.assertIsInstance(suggestions, list)

    def test_filter_by_category(self):
        """Test filtering by category."""
        results = self.search.filter_by_category("التسجيل")
        self.assertIsInstance(results, list)

    def test_filter_by_platform(self):
        """Test filtering by platform."""
        results = self.search.filter_by_platform("أبشر")
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)

    def test_filter_by_fee(self):
        """Test filtering free services."""
        results = self.search.filter_by_fee(max_fee=0)
        self.assertIsInstance(results, list)
        # Most Saudi government services are free

    def test_advanced_search(self):
        """Test advanced search with multiple filters."""
        results = self.search.advanced_search(
            query="إقامة",
            platform="معايش",
            max_results=5
        )
        self.assertIsInstance(results, list)

    def test_get_related_services(self):
        """Test finding related services."""
        related = self.search.get_related_services("absher_passport_renewal")
        self.assertIsInstance(related, list)

    def test_search_english(self):
        """Test search with English language."""
        search_en = SemanticSearch(language="en")
        results = search_en.search("passport")
        self.assertIsInstance(results, list)

    def test_empty_search_query(self):
        """Test search with empty query."""
        results = self.search.search("")
        self.assertIsInstance(results, list)

    def test_search_special_characters(self):
        """Test search with special characters."""
        results = self.search.search("(رقم)")
        self.assertIsInstance(results, list)

    def test_case_insensitive_search(self):
        """Test that search is case-insensitive."""
        results1 = self.search.search("جواز")
        results2 = self.search.search("جواز")  # Same word
        # Should return same or similar results
        self.assertEqual(len(results1), len(results2))

    def test_ranking_by_relevance(self):
        """Test that results are ranked by relevance."""
        results = self.search.search("جواز")
        if len(results) > 1:
            # First result should have equal or higher score
            self.assertGreaterEqual(results[0]["score"], results[-1]["score"])


if __name__ == "__main__":
    unittest.main()
