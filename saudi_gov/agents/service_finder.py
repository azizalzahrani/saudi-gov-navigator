"""
Service Finder Agent - وكيل البحث عن الخدمات

Identifies the correct government service and platform based on user queries.
يحدد الخدمة الحكومية الصحيحة والمنصة بناءً على استفسارات المستخدم.
"""

from typing import Dict, List, Optional, Any
from saudi_gov.knowledge_base import get_platform_services, search_services, load_all_services
from saudi_gov.config import PLATFORMS, Config
from saudi_gov.search import SemanticSearch

SCENARIO_SERVICE_HINTS = {
    "وافد": [
        "muqeem_iqama_renewal",
        "muqeem_check_status",
        "qiwa_labor_contract",
        "hrsd_worker_registration",
        "tawakkalna_digital_id",
    ],
    "مقيم": [
        "muqeem_iqama_renewal",
        "muqeem_check_status",
        "qiwa_labor_contract",
        "hrsd_worker_registration",
    ],
    "موظف": [
        "qiwa_labor_contract",
        "hrsd_worker_registration",
        "qiwa_wage_protection",
        "muqeem_check_status",
    ],
    "عامل": [
        "qiwa_labor_contract",
        "hrsd_worker_registration",
        "qiwa_worker_transfer",
        "muqeem_iqama_transfer",
    ],
    "تاسيس": [
        "misa_commercial_registration",
        "balady_commercial_license",
        "qiwa_employer_registration",
        "misa_investor_registration",
        "nitaqat_band_calculation",
    ],
    "تأسيس": [
        "misa_commercial_registration",
        "balady_commercial_license",
        "qiwa_employer_registration",
        "misa_investor_registration",
        "nitaqat_band_calculation",
    ],
    "شركة": [
        "misa_commercial_registration",
        "balady_commercial_license",
        "qiwa_employer_registration",
        "nitaqat_band_calculation",
    ],
    "استثمار": [
        "misa_investment_license",
        "misa_investor_registration",
        "misa_commercial_registration",
        "balady_commercial_license",
    ],
    "سجل تجاري": [
        "misa_commercial_registration",
        "balady_commercial_license",
    ],
}


class ServiceFinder:
    """
    Agent responsible for finding the right government service.

    وكيل مسؤول عن إيجاد الخدمة الحكومية الصحيحة.
    """

    def __init__(self, language: str = "ar"):
        """
        Initialize the ServiceFinder agent.

        Parameters:
            language: Language for responses ("ar" for Arabic, "en" for English)
        """
        self.language = language
        self.platforms = load_all_services()
        self.semantic_search = SemanticSearch(language=language)

    def find_service_by_query(self, query: str) -> List[Dict[str, Any]]:
        """
        Find services matching user query using semantic search.

        البحث عن الخدمات المطابقة لاستعلام المستخدم.

        Args:
            query: User's search query in Arabic or English

        Returns:
            List of matching service dictionaries
        """
        ranked_results = self.semantic_search.search(query, max_results=10)
        if ranked_results:
            return [result["service"] for result in ranked_results]

        return search_services(query, language=self.language)

    def find_service_by_platform(
        self, platform_ar: str, service_keywords: Optional[str] = None
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Find services within a specific platform.

        الحصول على الخدمات ضمن منصة محددة.

        Args:
            platform_ar: Arabic name of the platform (e.g., "أبشر")
            service_keywords: Optional keywords to filter services

        Returns:
            List of services from the platform, optionally filtered
        """
        services = get_platform_services(platform_ar)

        if services is None:
            return None

        if service_keywords:
            filtered = [
                s for s in services
                if service_keywords.lower() in s.get("name_ar", "").lower()
                or service_keywords.lower() in s.get("description_ar", "").lower()
            ]
            return filtered if filtered else services

        return services

    def get_all_platforms(self) -> Dict[str, str]:
        """
        Get all available government platforms.

        الحصول على جميع المنصات الحكومية المتاحة.

        Returns:
            Dictionary mapping Arabic names to platform codes
        """
        return PLATFORMS

    def get_platform_info(self, platform_ar: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a platform.

        الحصول على معلومات تفصيلية عن منصة.

        Args:
            platform_ar: Arabic name of the platform

        Returns:
            Platform information dictionary or None if not found
        """
        platform_data = self.platforms.get(platform_ar)
        if platform_data:
            return {
                "name_ar": platform_data.get("platform_ar"),
                "name_en": platform_data.get("platform_en"),
                "url": platform_data.get("platform_url"),
                "description_ar": platform_data.get("platform_description_ar"),
                "description_en": platform_data.get("platform_description_en"),
                "services_count": len(platform_data.get("services", [])),
            }
        return None

    def categorize_services(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Organize all services by category.

        تنظيم جميع الخدمات حسب الفئة.

        Returns:
            Dictionary with categories as keys and service lists as values
        """
        categories = {}

        for platform_name, platform_data in self.platforms.items():
            services = platform_data.get("services", [])
            for service in services:
                category = service.get(
                    "category" if self.language == "ar" else "category_en",
                    "أخرى"
                )
                if category not in categories:
                    categories[category] = []
                categories[category].append(service)

        return categories

    def get_service_by_id(self, service_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific service by its unique ID.

        الحصول على خدمة محددة من خلال معرفها الفريد.

        Args:
            service_id: Unique service identifier

        Returns:
            Service dictionary or None if not found
        """
        for platform_name, platform_data in self.platforms.items():
            services = platform_data.get("services", [])
            for service in services:
                if service.get("id") == service_id:
                    return service
        return None

    def suggest_services(self, user_scenario: str) -> List[Dict[str, Any]]:
        """
        Suggest relevant services based on user scenario.

        اقتراح الخدمات ذات الصلة بناءً على سيناريو المستخدم.

        Args:
            user_scenario: Description of user's situation (e.g., "وافد جديد")

        Returns:
            List of suggested services
        """
        scenario_lower = user_scenario.lower()
        hinted_services = []
        seen_ids = set()

        for keyword, service_ids in SCENARIO_SERVICE_HINTS.items():
            if keyword in scenario_lower:
                for service_id in service_ids:
                    service = self.get_service_by_id(service_id)
                    if service and service_id not in seen_ids:
                        hinted_services.append(service)
                        seen_ids.add(service_id)

        all_services = []

        for platform_name, platform_data in self.platforms.items():
            all_services.extend(platform_data.get("services", []))

        # Score services based on relevance to scenario
        scored_services = []
        for service in all_services:
            score = 0
            name = service.get("name_ar", "").lower()
            desc = service.get("description_ar", "").lower()

            if scenario_lower in name or scenario_lower in desc:
                score += 3

            eligibility = service.get("eligibility", {})
            if scenario_lower in eligibility.get("requirements", "").lower():
                score += 2

            if score > 0:
                scored_services.append((service, score))

        # Sort by score and return services
        scored_services.sort(key=lambda x: x[1], reverse=True)
        if scored_services:
            suggested = hinted_services[:]
            for service, _score in scored_services:
                service_id = service.get("id")
                if service_id not in seen_ids:
                    suggested.append(service)
                    seen_ids.add(service_id)
            return suggested

        semantic_results = self.semantic_search.search(user_scenario, max_results=5)
        suggested = hinted_services[:]
        for result in semantic_results:
            service = result["service"]
            service_id = service.get("id")
            if service_id not in seen_ids:
                suggested.append(service)
                seen_ids.add(service_id)
        return suggested
