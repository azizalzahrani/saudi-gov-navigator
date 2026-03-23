"""
Expat Guide Example - دليل الوافد

Example showing services relevant to foreign workers (expatriates).
مثال يوضح الخدمات ذات الصلة بالعمال الأجانب.
"""

import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from saudi_gov.agents.navigator_agent import NavigatorAgent
from saudi_gov.agents.service_finder import ServiceFinder
from saudi_gov.agents.requirements_agent import RequirementsAgent
from saudi_gov.search import SemanticSearch


def main():
    """Run expat guide example."""
    print("=" * 70)
    print("🌍 دليل الوافد في المملكة العربية السعودية")
    print("Expat Guide in Saudi Arabia")
    print("=" * 70)

    # Initialize
    navigator = NavigatorAgent(language="ar")
    service_finder = ServiceFinder(language="ar")
    req_agent = RequirementsAgent(language="ar")
    search = SemanticSearch(language="ar")

    # Scenario: New expat arriving in Saudi Arabia
    print("\n📋 السيناريو: وافد جديد يصل إلى المملكة\n")

    # Step 1: Find services for new expat
    print("=" * 70)
    print("الخطوة 1️⃣: البحث عن خدمات الوافدين الجدد\n")

    expat_services = service_finder.suggest_services("وافد جديد")
    print(f"وجدنا {len(expat_services)} خدمة مناسبة:\n")

    for idx, service in enumerate(expat_services[:5], 1):
        print(f"{idx}. {service.get('name_ar')}")
        print(f"   المنصة: {service.get('id', 'غير محدد')[:20]}")
        print(f"   الفئة: {service.get('category')}\n")

    # Step 2: Iqama services
    print("\n" + "=" * 70)
    print("الخطوة 2️⃣: خدمات الإقامة (الآيكوما)\n")

    iqama_results = search.search("إقامة")
    print(f"خدمات الإقامة المتاحة:\n")

    for result in iqama_results[:3]:
        service = result["service"]
        print(f"• {service.get('name_ar')}")
        print(f"  الوصف: {service.get('description_ar')}\n")

    # Step 3: Detailed guide for Iqama renewal
    print("\n" + "=" * 70)
    print("الخطوة 3️⃣: دليل تفصيلي لتجديد الإقامة\n")

    service_id = "muqeem_iqama_renewal"
    service = service_finder.get_service_by_id(service_id)

    if service:
        print(f"الخدمة: {service.get('name_ar')}\n")

        print("المتطلبات الأساسية:")
        reqs = service.get("requirements", [])
        for req in reqs[:5]:
            print(f"  □ {req}")

        print(f"\nعدد الخطوات: {len(service.get('steps', []))}")
        print("\nأول 3 خطوات:")
        for idx, step in enumerate(service.get("steps", [])[:3], 1):
            print(f"  {idx}. {step}")

        print(f"\nالرسوم: {service.get('fees', {}).get('note')}")
        print(f"وقت المعالجة: {service.get('processing_time')}")

        print("\nنصائح هامة:")
        for tip in service.get("tips", [])[:3]:
            print(f"  ✓ {tip}")

    # Step 4: Work-related services
    print("\n" + "=" * 70)
    print("الخطوة 4️⃣: خدمات العمل والتوظيف\n")

    work_services = search.search("عقد عمل")
    print(f"خدمات العمل المتاحة:\n")

    for result in work_services[:3]:
        service = result["service"]
        print(f"• {service.get('name_ar')}")
        print(f"  المنصة: {result['platform']}\n")

    # Step 5: Social insurance
    print("\n" + "=" * 70)
    print("الخطوة 5️⃣: التأمينات الاجتماعية\n")

    insurance_services = search.search("تسجيل العامل")
    if insurance_services:
        service = insurance_services[0]["service"]
        print(f"الخدمة: {service.get('name_ar')}")
        print(f"الوصف: {service.get('description_ar')}\n")

        print("المتطلبات:")
        for req in service.get("requirements", [])[:4]:
            print(f"  • {req}")

        print(f"\nالرسوم: {service.get('fees', {}).get('note')}")
        print(f"وقت المعالجة: {service.get('processing_time')}")

    # Summary
    print("\n" + "=" * 70)
    print("📌 ملخص الخطوات الأساسية للوافد الجديد:\n")

    summary_steps = [
        "1. الحصول على تأشيرة الدخول",
        "2. تسجيل الإقامة (الآيكوما)",
        "3. توثيق عقد العمل",
        "4. التسجيل في التأمينات الاجتماعية",
        "5. فتح حساب بنكي",
        "6. الحصول على رخصة القيادة (إن لزم)",
    ]

    for step in summary_steps:
        print(f"  {step}")

    print("\n" + "=" * 70)
    print("💡 نصيحة: استخدم منصة أبشر (Absher) للعديد من هذه الخدمات")
    print("=" * 70)

    print("\n\n✅ انتهى دليل الوافد")


if __name__ == "__main__":
    main()
