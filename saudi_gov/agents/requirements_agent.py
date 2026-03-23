"""
Requirements Agent - وكيل المتطلبات

Extracts and presents service requirements and step-by-step procedures.
يستخرج ويقدم متطلبات الخدمات والإجراءات خطوة بخطوة.
"""

from typing import Dict, List, Optional, Any
from saudi_gov.agents.service_finder import ServiceFinder


def _localized_key(base_key: str, language: str) -> str:
    """Map a logical field name to the dataset's localized key."""
    return f"{base_key}_en" if language == "en" else f"{base_key}_ar"


class RequirementsAgent:
    """
    Agent responsible for extracting and presenting service requirements.

    وكيل مسؤول عن استخراج وعرض متطلبات الخدمة.
    """

    def __init__(self, language: str = "ar"):
        """
        Initialize the RequirementsAgent.

        Parameters:
            language: Language for responses ("ar" for Arabic, "en" for English)
        """
        self.language = language
        self.service_finder = ServiceFinder(language=language)

    def get_requirements(self, service_id: str) -> Optional[Dict[str, Any]]:
        """
        Get all requirements for a specific service.

        الحصول على جميع المتطلبات لخدمة محددة.

        Args:
            service_id: Unique service identifier

        Returns:
            Dictionary with requirements or None if service not found
        """
        service = self.service_finder.get_service_by_id(service_id)

        if not service:
            return None

        name_key = _localized_key("name", self.language)
        req_key = "requirements_en" if self.language == "en" else "requirements"

        return {
            "service_id": service_id,
            "service_name": service.get(name_key),
            "requirements": service.get(req_key, []),
            "eligibility": service.get("eligibility", {}),
        }

    def get_steps(self, service_id: str) -> Optional[Dict[str, Any]]:
        """
        Get step-by-step procedure for a service.

        الحصول على خطوات الإجراء خطوة بخطوة.

        Args:
            service_id: Unique service identifier

        Returns:
            Dictionary with procedure steps or None if service not found
        """
        service = self.service_finder.get_service_by_id(service_id)

        if not service:
            return None

        name_key = _localized_key("name", self.language)
        steps_key = "steps_en" if self.language == "en" else "steps"

        return {
            "service_id": service_id,
            "service_name": service.get(name_key),
            "steps": service.get(steps_key, []),
        }

    def get_fees(self, service_id: str) -> Optional[Dict[str, Any]]:
        """
        Get fee information for a service.

        الحصول على معلومات الرسوم للخدمة.

        Args:
            service_id: Unique service identifier

        Returns:
            Dictionary with fee information or None if service not found
        """
        service = self.service_finder.get_service_by_id(service_id)

        if not service:
            return None

        name_key = _localized_key("name", self.language)
        fees_key = "fees_en" if self.language == "en" else "fees"
        time_key = "processing_time_en" if self.language == "en" else "processing_time"

        return {
            "service_id": service_id,
            "service_name": service.get(name_key),
            "fees": service.get(fees_key, {}),
            "processing_time": service.get(time_key, "غير محدد"),
        }

    def get_common_mistakes(self, service_id: str) -> Optional[Dict[str, Any]]:
        """
        Get common mistakes to avoid for a service.

        الحصول على الأخطاء الشائعة الواجب تجنبها.

        Args:
            service_id: Unique service identifier

        Returns:
            Dictionary with common mistakes or None if service not found
        """
        service = self.service_finder.get_service_by_id(service_id)

        if not service:
            return None

        name_key = _localized_key("name", self.language)
        mistakes_key = (
            "common_mistakes_en" if self.language == "en" else "common_mistakes"
        )

        return {
            "service_id": service_id,
            "service_name": service.get(name_key),
            "mistakes": service.get(mistakes_key, []),
        }

    def get_tips(self, service_id: str) -> Optional[Dict[str, Any]]:
        """
        Get helpful tips for using a service successfully.

        الحصول على نصائح مفيدة للاستخدام الناجح.

        Args:
            service_id: Unique service identifier

        Returns:
            Dictionary with tips or None if service not found
        """
        service = self.service_finder.get_service_by_id(service_id)

        if not service:
            return None

        name_key = _localized_key("name", self.language)
        tips_key = "tips_en" if self.language == "en" else "tips"

        return {
            "service_id": service_id,
            "service_name": service.get(name_key),
            "tips": service.get(tips_key, []),
        }

    def get_full_service_guide(self, service_id: str) -> Optional[Dict[str, Any]]:
        """
        Get complete guide for a service with all information.

        الحصول على دليل كامل للخدمة.

        Args:
            service_id: Unique service identifier

        Returns:
            Complete service guide or None if service not found
        """
        service = self.service_finder.get_service_by_id(service_id)

        if not service:
            return None

        name_key = _localized_key("name", self.language)
        description_key = _localized_key("description", self.language)
        category_key = "category_en" if self.language == "en" else "category"
        requirements_key = "requirements_en" if self.language == "en" else "requirements"
        steps_key = "steps_en" if self.language == "en" else "steps"
        fees_key = "fees_en" if self.language == "en" else "fees"
        processing_time_key = (
            "processing_time_en" if self.language == "en" else "processing_time"
        )
        common_mistakes_key = (
            "common_mistakes_en" if self.language == "en" else "common_mistakes"
        )
        tips_key = "tips_en" if self.language == "en" else "tips"

        return {
            "service_id": service_id,
            "name": service.get(name_key),
            "description": service.get(description_key),
            "category": service.get(category_key),
            "requirements": service.get(requirements_key, []),
            "steps": service.get(steps_key, []),
            "fees": service.get(fees_key, {}),
            "processing_time": service.get(processing_time_key),
            "common_mistakes": service.get(common_mistakes_key, []),
            "tips": service.get(tips_key, []),
            "eligibility": service.get("eligibility", {}),
        }

    def format_requirements_for_display(
        self, service_id: str
    ) -> Optional[str]:
        """
        Format requirements as a human-readable string.

        تنسيق المتطلبات كنص قابل للقراءة.

        Args:
            service_id: Unique service identifier

        Returns:
            Formatted string or None if service not found
        """
        req_info = self.get_requirements(service_id)

        if not req_info:
            return None

        lines = [f"🏛️ {req_info['service_name']}\n"]
        lines.append("📋 المتطلبات المطلوبة:\n" if self.language == "ar" else "📋 Requirements:\n")

        for idx, req in enumerate(req_info["requirements"], 1):
            lines.append(f"  {idx}. {req}\n")

        return "".join(lines)

    def format_steps_for_display(self, service_id: str) -> Optional[str]:
        """
        Format steps as a human-readable instruction guide.

        تنسيق الخطوات كدليل التعليمات.

        Args:
            service_id: Unique service identifier

        Returns:
            Formatted string or None if service not found
        """
        steps_info = self.get_steps(service_id)

        if not steps_info:
            return None

        lines = [f"🏛️ {steps_info['service_name']}\n"]
        lines.append("📝 الخطوات:\n" if self.language == "ar" else "📝 Steps:\n")

        for idx, step in enumerate(steps_info["steps"], 1):
            lines.append(f"  {idx}. {step}\n")

        return "".join(lines)
