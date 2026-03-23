"""
Business Setup Example - مثال إعداد العمل التجاري

Example showing services relevant to business owners starting a company.
مثال يوضح الخدمات المتعلقة بأصحاب الأعمال الذين يريدون تأسيس شركة.
"""

import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from saudi_gov.agents.navigator_agent import NavigatorAgent
from saudi_gov.agents.service_finder import ServiceFinder
from saudi_gov.search import SemanticSearch
from saudi_gov.utils.fee_calculator import calculate_total_fees, compare_service_costs


def main():
    """Run business setup example."""
    print("=" * 70)
    print("🏢 دليل تأسيس عمل تجاري في المملكة")
    print("Business Setup Guide in Saudi Arabia")
    print("=" * 70)

    # Initialize
    navigator = NavigatorAgent(language="ar")
    service_finder = ServiceFinder(language="ar")
    search = SemanticSearch(language="ar")

    # Scenario: Entrepreneur wants to start a business
    print("\n📋 السيناريو: رجل أعمال يريد تأسيس شركة جديدة\n")

    # Step 1: Find business-related services
    print("=" * 70)
    print("الخطوة 1️⃣: البحث عن خدمات تأسيس العمل\n")

    business_services = service_finder.suggest_services("تأسيس شركة")
    print(f"وجدنا {len(business_services)} خدمة متعلقة بتأسيس الأعمال:\n")

    for idx, service in enumerate(business_services[:6], 1):
        print(f"{idx}. {service.get('name_ar')}")
        print(f"   الفئة: {service.get('category')}\n")

    # Step 2: Commercial registration
    print("\n" + "=" * 70)
    print("الخطوة 2️⃣: التسجيل التجاري\n")

    commercial_results = search.search("تسجيل تجاري")
    print("خدمات التسجيل التجاري:\n")

    commercial_services = []
    for result in commercial_results[:3]:
        service = result["service"]
        commercial_services.append(service)
        print(f"• {service.get('name_ar')}")
        print(f"  المنصة: {result['platform']}")
        print(f"  الرسوم: {service.get('fees', {}).get('note')}\n")

    # Step 3: Investment services (MISA)
    print("\n" + "=" * 70)
    print("الخطوة 3️⃣: خدمات الاستثمار والترخيص\n")

    investment_results = search.search("استثمار")
    print("خدمات الاستثمار:\n")

    investment_services = []
    for result in investment_results[:3]:
        service = result["service"]
        investment_services.append(service)
        print(f"• {service.get('name_ar')}")
        print(f"  الوصف: {service.get('description_ar')}\n")

    # Step 4: Saudization compliance (Nitaqat)
    print("\n" + "=" * 70)
    print("الخطوة 4️⃣: متطلبات السعودة (نطاقات)\n")

    nitaqat_results = search.search("نطاقات سعودة")
    print("خدمات السعودة:\n")

    if nitaqat_results:
        for result in nitaqat_results[:3]:
            service = result["service"]
            print(f"• {service.get('name_ar')}")
            print(f"  الفئة: {service.get('category')}")
            print(f"  المتطلبات: {', '.join(service.get('requirements', [])[:2])}\n")

    # Step 5: Labor compliance
    print("\n" + "=" * 70)
    print("الخطوة 5️⃣: الامتثال لقوانين العمل\n")

    labor_results = search.search("عقد عمل الكتروني")
    print("خدمات العمل والتوظيف:\n")

    labor_services = []
    for result in labor_results[:2]:
        service = result["service"]
        labor_services.append(service)
        print(f"• {service.get('name_ar')}")
        print(f"  الوصف: {service.get('description_ar')}\n")

    # Step 6: Licenses and permits
    print("\n" + "=" * 70)
    print("الخطوة 6️⃣: الرخص والتصاريح\n")

    license_results = search.search("رخصة نشاط تجاري")
    print("خدمات الرخص والتصاريح:\n")

    license_services = []
    for result in license_results[:3]:
        service = result["service"]
        license_services.append(service)
        print(f"• {service.get('name_ar')}")
        print(f"  الفئة: {service.get('category')}\n")

    # Cost analysis
    print("\n" + "=" * 70)
    print("💰 تحليل التكاليف\n")

    all_business_services = (commercial_services + investment_services +
                            labor_services + license_services)

    if all_business_services:
        cost_comparison = compare_service_costs(all_business_services[:8])

        print("تكاليف الخدمات الأساسية:\n")
        for cost_item in cost_comparison["costs"][:5]:
            print(f"• {cost_item['service_name']}")
            print(f"  الرسوم: {cost_item['fee_formatted']}\n")

        if "total_cost" in cost_comparison:
            print(f"إجمالي التكاليف: {cost_comparison['total_cost']} ريال سعودي\n")

    # Key requirements summary
    print("\n" + "=" * 70)
    print("📋 المتطلبات الأساسية لتأسيس شركة:\n")

    requirements = [
        "✓ البطاقة الهوية الوطنية الصحيحة",
        "✓ عنوان مقر الشركة",
        "✓ رأس المال المطلوب",
        "✓ اسم الشركة المختار",
        "✓ نوع النشاط التجاري",
        "✓ الشركاء والمساهمين (إن وجدوا)",
        "✓ حساب بنكي للشركة",
        "✓ رقم الضريبة (VAT)",
    ]

    for req in requirements:
        print(f"  {req}")

    # Timeline
    print("\n\n" + "=" * 70)
    print("⏱️  الجدول الزمني المتوقع:\n")

    timeline = [
        ("التسجيل التجاري", "1-2 أيام"),
        ("ترخيص النشاط", "3-5 أيام"),
        ("التسجيل الضريبي", "2-3 أيام"),
        ("التأمينات الاجتماعية", "1-2 أيام"),
        ("الإجمالي", "7-12 يوم عمل"),
    ]

    for task, duration in timeline:
        print(f"  • {task}: {duration}")

    # Helpful tips
    print("\n\n" + "=" * 70)
    print("💡 نصائح مهمة:\n")

    tips = [
        "استخدم منصة MISA (هيئة الاستثمار) للخدمات الاستثمارية",
        "تأكد من استيفاء متطلبات السعودة (نطاقات)",
        "وثق جميع العقود والاتفاقيات",
        "انتظر تأكيد جميع الترخيصات قبل بدء العمليات",
        "استشر محامياً متخصصاً في القانون التجاري السعودي",
        "احتفظ بجميع الأوراق والشهادات",
    ]

    for tip in tips:
        print(f"  • {tip}")

    print("\n" + "=" * 70)
    print("✅ انتهى دليل تأسيس العمل التجاري")
    print("=" * 70)


if __name__ == "__main__":
    main()
