"""
Basic Query Example - مثال الاستعلام الأساسي

Example of basic service search using the Saudi Gov Navigator.
مثال على البحث الأساسي عن الخدمات.
"""

import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from saudi_gov.agents.navigator_agent import NavigatorAgent
from saudi_gov.agents.service_finder import ServiceFinder
from saudi_gov.search import SemanticSearch


def main():
    """Run basic query examples."""
    print("=" * 70)
    print("🏛️  مثال 1: البحث الأساسي عن الخدمات")
    print("Basic Query Example")
    print("=" * 70)

    # Initialize agents
    navigator = NavigatorAgent(language="ar")
    service_finder = ServiceFinder(language="ar")
    search = SemanticSearch(language="ar")

    # Example 1: Search for passport services
    print("\n\n📝 مثال 1: البحث عن خدمات جواز السفر\n")
    query = "تجديد جواز السفر"
    results = search.search(query, max_results=3)

    if results:
        print(f"نتائج البحث عن '{query}':\n")
        for idx, result in enumerate(results, 1):
            service = result["service"]
            print(f"{idx}. {service.get('name_ar')}")
            print(f"   الوصف: {service.get('description_ar')}")
            print(f"   المنصة: {result['platform']}")
            print(f"   معرف الخدمة: {service.get('id')}\n")

    # Example 2: Get all platforms
    print("\n" + "=" * 70)
    print("📊 مثال 2: عرض جميع المنصات الحكومية\n")

    platforms = service_finder.get_all_platforms()
    print(f"عدد المنصات: {len(platforms)}\n")

    for platform_ar, code in list(platforms.items())[:5]:
        info = service_finder.get_platform_info(platform_ar)
        if info:
            print(f"• {info['name_ar']} ({info['name_en']})")
            print(f"  عدد الخدمات: {info['services_count']}")
            print(f"  الرابط: {info['url']}\n")

    # Example 3: Get service by ID
    print("\n" + "=" * 70)
    print("🔍 مثال 3: الحصول على تفاصيل خدمة محددة\n")

    service_id = "absher_passport_renewal"
    service = service_finder.get_service_by_id(service_id)

    if service:
        print(f"الخدمة: {service.get('name_ar')}")
        print(f"الفئة: {service.get('category')}")
        print(f"الوصف: {service.get('description_ar')}\n")

        print("المتطلبات:")
        for req in service.get("requirements", []):
            print(f"  • {req}")

        print("\nالخطوات:")
        for idx, step in enumerate(service.get("steps", []), 1):
            print(f"  {idx}. {step}")

        print(f"\nالرسوم: {service.get('fees', {}).get('note')}")
        print(f"وقت المعالجة: {service.get('processing_time')}")

    # Example 4: Get service guidance
    print("\n" + "=" * 70)
    print("📋 مثال 4: الحصول على دليل خدمة كامل\n")

    from saudi_gov.agents.requirements_agent import RequirementsAgent

    req_agent = RequirementsAgent(language="ar")
    guide = req_agent.get_full_service_guide(service_id)

    if guide:
        print(f"الخدمة: {guide.get('name')}")
        print(f"الفئة: {guide.get('category')}\n")

        print("النصائح المهمة:")
        for tip in guide.get("tips", [])[:3]:
            print(f"  ✓ {tip}")

        print("\nالأخطاء الشائعة:")
        for mistake in guide.get("common_mistakes", [])[:3]:
            print(f"  ✗ {mistake}")

    # Example 5: Suggest services based on scenario
    print("\n" + "=" * 70)
    print("💡 مثال 5: اقتراح خدمات بناءً على السيناريو\n")

    scenario = "موظف جديد يريد تسجيل نفسه"
    suggested = service_finder.suggest_services(scenario)

    print(f"السيناريو: {scenario}\n")
    print("الخدمات المقترحة:")
    for idx, service in enumerate(suggested[:3], 1):
        print(f"{idx}. {service.get('name_ar')} - {service.get('description_ar')}\n")

    print("\n" + "=" * 70)
    print("✅ انتهى المثال")
    print("=" * 70)


if __name__ == "__main__":
    main()
