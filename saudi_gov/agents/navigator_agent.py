"""
Navigator Agent - وكيل الملاح

Main agent that understands user queries in Arabic and orchestrates responses.
وكيل رئيسي يفهم استفسارات المستخدم باللغة العربية ويقدم التوجيهات.
"""

from typing import Dict, List, Optional, Any
from saudi_gov.agents.service_finder import ServiceFinder
from saudi_gov.agents.requirements_agent import RequirementsAgent
from saudi_gov.config import Config


def _localized_key(base_key: str, language: str) -> str:
    """Map a logical field name to the dataset's localized key."""
    return f"{base_key}_en" if language == "en" else f"{base_key}_ar"


class NavigatorAgent:
    """
    Main agent that understands user queries and provides service guidance.

    وكيل رئيسي يفهم الاستفسارات ويقدم توجيهات الخدمات.
    """

    def __init__(self, language: str = "ar"):
        """
        Initialize the NavigatorAgent.

        Parameters:
            language: Language for responses ("ar" for Arabic, "en" for English)
        """
        self.language = language
        self.service_finder = ServiceFinder(language=language)
        self.requirements_agent = RequirementsAgent(language=language)
        self.config = Config()

    def process_user_query(self, query: str) -> Dict[str, Any]:
        """
        Process a user query and return relevant government services.

        معالجة استفسار المستخدم وإرجاع الخدمات الحكومية ذات الصلة.

        Args:
            query: User's question or request in Arabic or English

        Returns:
            Dictionary with search results and recommendations
        """
        # Search for matching services
        matching_services = self.service_finder.find_service_by_query(query)

        # Suggest services based on scenario
        suggested_services = self.service_finder.suggest_services(query)

        return {
            "query": query,
            "matching_services": matching_services,
            "suggested_services": suggested_services,
            "total_matches": len(matching_services),
        }

    def answer(self, query: str, max_results: int = 3) -> str:
        """
        Return a concise, human-readable answer for README/examples usage.

        Args:
            query: User query in Arabic or English
            max_results: Maximum services to include in the response

        Returns:
            Formatted answer string
        """
        result = self.process_user_query(query)
        matches = result["matching_services"]
        suggestions = result["suggested_services"]

        if self._is_broad_guidance_query(query):
            selected_services = suggestions or matches
        else:
            selected_services = matches[:]
            seen_ids = {service.get("id") for service in selected_services}
            for service in suggestions:
                if service.get("id") not in seen_ids:
                    selected_services.append(service)
                    seen_ids.add(service.get("id"))

        matches = selected_services[:max_results]

        if not matches:
            return (
                "لم أجد خدمة مطابقة. جرّب كلمات مفتاحية مختلفة أو اسم المنصة."
                if self.language == "ar"
                else "I could not find a matching service. Try different keywords or the platform name."
            )

        lines = [
            "وجدت الخدمات التالية:" if self.language == "ar" else "I found these services:"
        ]
        name_key = _localized_key("name", self.language)
        description_key = _localized_key("description", self.language)

        for service in matches:
            lines.append(f"- {service.get(name_key)}")
            lines.append(f"  {service.get(description_key)}")
            lines.append(f"  ID: {service.get('id')}")

        return "\n".join(lines)

    def _is_broad_guidance_query(self, query: str) -> bool:
        """Detect when the user is asking for a workflow or bundle of services."""
        query_lower = query.lower()
        scenario_markers = [
            "ما الخدمات",
            "ماذا احتاج",
            "ماذا أحتاج",
            "ايش احتاج",
            "وش احتاج",
            "وافد جديد",
            "new expat",
            "what services",
            "what do i need",
        ]
        return any(marker in query_lower for marker in scenario_markers)

    def get_service_guidance(self, service_id: str) -> Dict[str, Any]:
        """
        Get complete guidance for a specific service.

        الحصول على التوجيهات الكاملة لخدمة محددة.

        Args:
            service_id: Unique service identifier

        Returns:
            Complete service guide with all information
        """
        full_guide = self.requirements_agent.get_full_service_guide(service_id)

        if not full_guide:
            return {"error": "الخدمة غير موجودة" if self.language == "ar" else "Service not found"}

        return full_guide

    def get_quick_answer(self, service_id: str) -> str:
        """
        Get a quick answer with the most important information for a service.

        الحصول على إجابة سريعة بأهم المعلومات.

        Args:
            service_id: Unique service identifier

        Returns:
            Formatted string with key information
        """
        service = self.service_finder.get_service_by_id(service_id)

        if not service:
            return "الخدمة غير موجودة" if self.language == "ar" else "Service not found"

        name_key = _localized_key("name", self.language)
        description_key = _localized_key("description", self.language)
        fees_key = "fees_en" if self.language == "en" else "fees"
        processing_time_key = (
            "processing_time_en" if self.language == "en" else "processing_time"
        )

        lines = []
        lines.append(f"🏛️ {service.get(name_key)}\n")
        lines.append(f"📝 {service.get(description_key)}\n")

        fees = service.get(fees_key, {})
        lines.append(f"💰 {fees.get('note', 'رسوم غير محددة')}\n")

        processing = service.get(processing_time_key, "غير محدد")
        lines.append(f"⏱️ {processing}\n")

        return "".join(lines)

    def compare_services(self, service_ids: List[str]) -> Dict[str, Any]:
        """
        Compare multiple services side by side.

        مقارنة عدة خدمات جنباً إلى جنب.

        Args:
            service_ids: List of service identifiers to compare

        Returns:
            Comparison dictionary
        """
        services = []
        for sid in service_ids:
            service = self.service_finder.get_service_by_id(sid)
            if service:
                services.append(service)

        if not services:
            return {"error": "لم يتم العثور على خدمات" if self.language == "ar" else "No services found"}

        name_key = _localized_key("name", self.language)
        category_key = "category_en" if self.language == "en" else "category"
        fees_key = "fees_en" if self.language == "en" else "fees"
        processing_time_key = (
            "processing_time_en" if self.language == "en" else "processing_time"
        )

        comparison = {
            "service_count": len(services),
            "services": []
        }

        for service in services:
            comparison["services"].append({
                "id": service.get("id"),
                "name": service.get(name_key),
                "category": service.get(category_key),
                "fees": service.get(fees_key, {}).get("amount", 0),
                "processing_time": service.get(processing_time_key),
            })

        return comparison

    def get_service_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        Get all services in a specific category.

        الحصول على جميع الخدمات في فئة محددة.

        Args:
            category: Service category name

        Returns:
            List of services in the category
        """
        categorized = self.service_finder.categorize_services()
        return categorized.get(category, [])

    def get_all_platforms_info(self) -> Dict[str, Dict[str, Any]]:
        """
        Get information about all government platforms.

        الحصول على معلومات عن جميع المنصات الحكومية.

        Returns:
            Dictionary of platform information
        """
        platforms = self.service_finder.get_all_platforms()
        platform_info = {}

        for platform_ar, platform_code in platforms.items():
            info = self.service_finder.get_platform_info(platform_ar)
            if info:
                platform_info[platform_code] = info

        return platform_info

    def format_response(
        self, data: Dict[str, Any], format_type: str = "text"
    ) -> str:
        """
        Format response data for display.

        تنسيق بيانات الاستجابة للعرض.

        Args:
            data: Data dictionary to format
            format_type: Format type ("text", "json", "html")

        Returns:
            Formatted string
        """
        if format_type == "json":
            import json
            return json.dumps(data, ensure_ascii=False, indent=2)
        elif format_type == "html":
            return self._format_as_html(data)
        else:
            return self._format_as_text(data)

    def _format_as_text(self, data: Dict[str, Any]) -> str:
        """Format data as plain text."""
        lines = []
        for key, value in data.items():
            if isinstance(value, list):
                lines.append(f"{key}:")
                for item in value:
                    lines.append(f"  - {item}")
            elif isinstance(value, dict):
                lines.append(f"{key}:")
                for k, v in value.items():
                    lines.append(f"  {k}: {v}")
            else:
                lines.append(f"{key}: {value}")
        return "\n".join(lines)

    def _format_as_html(self, data: Dict[str, Any]) -> str:
        """Format data as HTML."""
        html = "<div class='service-guide'>\n"
        for key, value in data.items():
            if isinstance(value, list):
                html += f"<h3>{key}</h3>\n<ul>\n"
                for item in value:
                    html += f"<li>{item}</li>\n"
                html += "</ul>\n"
            elif isinstance(value, dict):
                html += f"<h3>{key}</h3>\n<dl>\n"
                for k, v in value.items():
                    html += f"<dt>{k}</dt><dd>{v}</dd>\n"
                html += "</dl>\n"
            else:
                html += f"<p><strong>{key}:</strong> {value}</p>\n"
        html += "</div>"
        return html

    def suggest_next_steps(self, service_id: str) -> List[str]:
        """
        Suggest next steps after selecting a service.

        اقتراح الخطوات التالية بعد اختيار الخدمة.

        Args:
            service_id: Selected service identifier

        Returns:
            List of suggested next steps
        """
        requirements = self.requirements_agent.get_requirements(service_id)

        if not requirements:
            return []

        steps = [
            "جمع المتطلبات المذكورة أعلاه" if self.language == "ar" else "Gather the requirements listed above",
            "زيارة المنصة الرسمية للخدمة" if self.language == "ar" else "Visit the official service platform",
            "اتبع الخطوات المفصلة خطوة بخطوة" if self.language == "ar" else "Follow the detailed steps",
            "احتفظ برقم الطلب أو التسجيل" if self.language == "ar" else "Keep your application reference number",
            "تابع حالة الطلب إن أمكن" if self.language == "ar" else "Track your application status if available",
        ]

        return steps
