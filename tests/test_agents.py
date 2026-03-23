"""
Agents Tests - اختبارات الوكلاء

Unit tests for AI agents.
اختبارات الوحدة للوكلاء الذكية.
"""

import unittest
from saudi_gov.agents.navigator_agent import NavigatorAgent
from saudi_gov.agents.service_finder import ServiceFinder
from saudi_gov.agents.requirements_agent import RequirementsAgent


class TestNavigatorAgent(unittest.TestCase):
    """Test cases for NavigatorAgent."""

    def setUp(self):
        """Set up test fixtures."""
        self.agent = NavigatorAgent(language="ar")

    def test_agent_initialization(self):
        """Test that agent initializes properly."""
        self.assertIsNotNone(self.agent.service_finder)
        self.assertIsNotNone(self.agent.requirements_agent)

    def test_process_user_query(self):
        """Test processing a user query."""
        result = self.agent.process_user_query("جواز السفر")
        self.assertIsInstance(result, dict)
        self.assertIn("query", result)
        self.assertIn("matching_services", result)
        self.assertIn("suggested_services", result)

    def test_get_service_guidance(self):
        """Test getting service guidance."""
        guidance = self.agent.get_service_guidance("absher_passport_renewal")
        self.assertIsNotNone(guidance)
        self.assertIn("name", guidance)
        self.assertIn("requirements", guidance)

    def test_get_quick_answer(self):
        """Test getting quick answer."""
        answer = self.agent.get_quick_answer("absher_passport_renewal")
        self.assertIsInstance(answer, str)
        self.assertGreater(len(answer), 0)

    def test_compare_services(self):
        """Test comparing multiple services."""
        service_ids = ["absher_passport_renewal", "muqeem_iqama_renewal"]
        comparison = self.agent.compare_services(service_ids)
        self.assertIsNotNone(comparison)
        self.assertIn("service_count", comparison)

    def test_get_service_by_category(self):
        """Test getting services by category."""
        services = self.agent.get_service_by_category("التسجيل")
        self.assertIsInstance(services, list)

    def test_get_all_platforms_info(self):
        """Test getting all platforms information."""
        platforms = self.agent.get_all_platforms_info()
        self.assertIsInstance(platforms, dict)
        self.assertGreater(len(platforms), 0)

    def test_format_response_text(self):
        """Test formatting response as text."""
        data = {"name": "خدمة", "fee": "مجاني"}
        response = self.agent.format_response(data, format_type="text")
        self.assertIsInstance(response, str)
        self.assertIn("name", response)

    def test_format_response_json(self):
        """Test formatting response as JSON."""
        data = {"name": "خدمة", "fee": "مجاني"}
        response = self.agent.format_response(data, format_type="json")
        self.assertIsInstance(response, str)

    def test_suggest_next_steps(self):
        """Test suggesting next steps."""
        steps = self.agent.suggest_next_steps("absher_passport_renewal")
        self.assertIsInstance(steps, list)
        self.assertGreater(len(steps), 0)

    def test_answer_formats_natural_language_query(self):
        """Test README-style natural language query handling."""
        answer = self.agent.answer("أنا أريد تجديد جواز سفري، ما الخطوات؟")
        self.assertIsInstance(answer, str)
        self.assertIn("absher_passport_renewal", answer)
        self.assertIn("تجديد جواز السفر", answer)

    def test_answer_prefers_suggestions_for_broad_guidance(self):
        """Test scenario-style guidance queries use suggested services."""
        answer = self.agent.answer("أنا وافد جديد، ما الخدمات التي أحتاجها؟")
        self.assertIsInstance(answer, str)
        self.assertIn("muqeem_iqama_renewal", answer)


class TestServiceFinder(unittest.TestCase):
    """Test cases for ServiceFinder."""

    def setUp(self):
        """Set up test fixtures."""
        self.finder = ServiceFinder(language="ar")

    def test_finder_initialization(self):
        """Test that finder initializes properly."""
        self.assertIsNotNone(self.finder.platforms)
        self.assertGreater(len(self.finder.platforms), 0)

    def test_find_service_by_query(self):
        """Test finding service by query."""
        results = self.finder.find_service_by_query("إقامة")
        self.assertIsInstance(results, list)

    def test_find_service_by_platform(self):
        """Test finding services by platform."""
        services = self.finder.find_service_by_platform("أبشر")
        self.assertIsNotNone(services)
        self.assertIsInstance(services, list)

    def test_get_all_platforms(self):
        """Test getting all platforms."""
        platforms = self.finder.get_all_platforms()
        self.assertIsInstance(platforms, dict)
        self.assertGreater(len(platforms), 0)

    def test_get_platform_info(self):
        """Test getting platform info."""
        info = self.finder.get_platform_info("أبشر")
        self.assertIsNotNone(info)
        self.assertIn("name_ar", info)
        self.assertIn("url", info)

    def test_categorize_services(self):
        """Test categorizing services."""
        categories = self.finder.categorize_services()
        self.assertIsInstance(categories, dict)
        self.assertGreater(len(categories), 0)

    def test_get_service_by_id(self):
        """Test getting service by ID."""
        service = self.finder.get_service_by_id("absher_passport_renewal")
        self.assertIsNotNone(service)
        self.assertEqual(service.get("id"), "absher_passport_renewal")

    def test_suggest_services(self):
        """Test suggesting services."""
        suggestions = self.finder.suggest_services("وافد جديد")
        self.assertIsInstance(suggestions, list)
        self.assertGreater(len(suggestions), 0)


class TestRequirementsAgent(unittest.TestCase):
    """Test cases for RequirementsAgent."""

    def setUp(self):
        """Set up test fixtures."""
        self.agent = RequirementsAgent(language="ar")

    def test_agent_initialization(self):
        """Test that agent initializes properly."""
        self.assertIsNotNone(self.agent.service_finder)

    def test_get_requirements(self):
        """Test getting requirements."""
        reqs = self.agent.get_requirements("absher_passport_renewal")
        self.assertIsNotNone(reqs)
        self.assertIn("requirements", reqs)
        self.assertIsInstance(reqs["requirements"], list)

    def test_get_steps(self):
        """Test getting service steps."""
        steps = self.agent.get_steps("absher_passport_renewal")
        self.assertIsNotNone(steps)
        self.assertIn("steps", steps)
        self.assertIsInstance(steps["steps"], list)
        self.assertGreater(len(steps["steps"]), 0)

    def test_get_fees(self):
        """Test getting fee information."""
        fees = self.agent.get_fees("absher_passport_renewal")
        self.assertIsNotNone(fees)
        self.assertIn("fees", fees)
        self.assertIsInstance(fees["fees"], dict)

    def test_get_common_mistakes(self):
        """Test getting common mistakes."""
        mistakes = self.agent.get_common_mistakes("absher_passport_renewal")
        self.assertIsNotNone(mistakes)
        self.assertIn("mistakes", mistakes)

    def test_get_tips(self):
        """Test getting helpful tips."""
        tips = self.agent.get_tips("absher_passport_renewal")
        self.assertIsNotNone(tips)
        self.assertIn("tips", tips)

    def test_get_full_service_guide(self):
        """Test getting full service guide."""
        guide = self.agent.get_full_service_guide("absher_passport_renewal")
        self.assertIsNotNone(guide)
        self.assertIn("name", guide)
        self.assertIn("requirements", guide)
        self.assertIn("steps", guide)

    def test_format_requirements_for_display(self):
        """Test formatting requirements for display."""
        formatted = self.agent.format_requirements_for_display("absher_passport_renewal")
        self.assertIsInstance(formatted, str)
        self.assertGreater(len(formatted), 0)

    def test_format_steps_for_display(self):
        """Test formatting steps for display."""
        formatted = self.agent.format_steps_for_display("absher_passport_renewal")
        self.assertIsInstance(formatted, str)
        self.assertGreater(len(formatted), 0)

    def test_nonexistent_service(self):
        """Test with non-existent service."""
        result = self.agent.get_requirements("nonexistent_id")
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
