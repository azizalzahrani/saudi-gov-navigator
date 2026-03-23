"""
Knowledge Base Module - قاعدة المعرفة

Loads and manages Saudi government service data from JSON files.
يحمل ويدير بيانات الخدمات الحكومية السعودية من ملفات JSON.
"""

import json
import os
from typing import Dict, List, Any, Optional

__all__ = ["load_all_services", "get_platform_services", "get_service_by_id"]


def _get_kb_dir() -> str:
    """Get the knowledge base directory path."""
    return os.path.dirname(os.path.abspath(__file__))


def load_json_file(filename: str) -> Dict[str, Any]:
    """
    Load a JSON knowledge base file.

    تحميل ملف قاعدة معرفة JSON.

    Args:
        filename: Name of the JSON file (without directory path)

    Returns:
        Dictionary containing the JSON data
    """
    kb_path = os.path.join(_get_kb_dir(), filename)
    try:
        with open(kb_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Knowledge base file not found: {kb_path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {filename}: {str(e)}")


def load_all_services() -> Dict[str, Dict[str, Any]]:
    """
    Load all services from all platform knowledge base files.

    تحميل جميع الخدمات من ملفات قاعدة المعرفة لجميع المنصات.

    Returns:
        Dictionary with platform names as keys and service data as values
    """
    platforms = [
        "absher.json",
        "muqeem.json",
        "qiwa.json",
        "tawakkalna.json",
        "balady.json",
        "misa.json",
        "hrsd.json",
        "nitaqat.json",
    ]

    all_services = {}
    for platform_file in platforms:
        try:
            data = load_json_file(platform_file)
            platform_name = data.get("platform_ar", platform_file.replace(".json", ""))
            all_services[platform_name] = data
        except (FileNotFoundError, ValueError) as e:
            print(f"Warning: Could not load {platform_file}: {str(e)}")

    return all_services


def get_platform_services(platform_name_ar: str) -> Optional[List[Dict[str, Any]]]:
    """
    Get all services for a specific platform.

    الحصول على جميع الخدمات لمنصة معينة.

    Args:
        platform_name_ar: Arabic name of the platform (e.g., "أبشر")

    Returns:
        List of service dictionaries or None if platform not found
    """
    all_services = load_all_services()
    platform_data = all_services.get(platform_name_ar)

    if platform_data:
        return platform_data.get("services", [])
    return None


def get_service_by_id(service_id: str) -> Optional[Dict[str, Any]]:
    """
    Find a service by its unique ID across all platforms.

    البحث عن خدمة من خلال معرفها الفريد عبر جميع المنصات.

    Args:
        service_id: Unique service identifier (e.g., "absher_passport_renewal")

    Returns:
        Service dictionary or None if not found
    """
    all_services = load_all_services()

    for platform_name, platform_data in all_services.items():
        services = platform_data.get("services", [])
        for service in services:
            if service.get("id") == service_id:
                return service

    return None


def search_services(query: str, language: str = "ar") -> List[Dict[str, Any]]:
    """
    Search services by keywords in name or description.

    البحث عن الخدمات باستخدام الكلمات الرئيسية في الاسم أو الوصف.

    Args:
        query: Search query string
        language: Language for search ("ar" for Arabic, "en" for English)

    Returns:
        List of matching services
    """
    all_services = load_all_services()
    results = []

    query_lower = query.lower()

    for platform_name, platform_data in all_services.items():
        services = platform_data.get("services", [])
        for service in services:
            name_key = "name_ar" if language == "ar" else "name_en"
            desc_key = "description_ar" if language == "ar" else "description_en"

            name = service.get(name_key, "").lower()
            description = service.get(desc_key, "").lower()

            if query_lower in name or query_lower in description:
                results.append(service)

    return results
