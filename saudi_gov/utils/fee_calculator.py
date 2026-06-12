"""
Fee Calculator - حاسبة الرسوم

Utility functions for handling fees and currency calculations.
وظائف مساعدة للتعامل مع الرسوم والعملات.
"""

import re
from typing import Dict, List, Optional, Union


# Exchange rates (as of knowledge cutoff - should be updated regularly)
EXCHANGE_RATES = {
    "SAR": 1.0,
    "USD": 0.266,      # 1 SAR = 0.266 USD
    "EUR": 0.245,      # 1 SAR = 0.245 EUR
    "AED": 0.978,      # 1 SAR = 0.978 AED
    "QAR": 0.973,      # 1 SAR = 0.973 QAR
    "KWD": 0.082,      # 1 SAR = 0.082 KWD
    "OMR": 0.102,      # 1 SAR = 0.102 OMR
}


def format_sar_amount(amount: Union[int, float]) -> str:
    """
    Format an amount in Saudi Riyals for display.

    تنسيق مبلغ بالريال السعودي للعرض.

    Args:
        amount: Amount in SAR

    Returns:
        Formatted string with currency symbol
    """
    if amount == 0:
        return "مجاني (0 ريال سعودي)"

    if isinstance(amount, float):
        if amount.is_integer():
            return f"{int(amount):,} ريال سعودي"
        else:
            return f"{amount:,.2f} ريال سعودي"

    return f"{amount:,} ريال سعودي"


def format_sar_amount_en(amount: Union[int, float]) -> str:
    """
    Format an amount in Saudi Riyals for display (English).

    تنسيق مبلغ بالريال السعودي للعرض (إنجليزي).

    Args:
        amount: Amount in SAR

    Returns:
        Formatted string with currency symbol
    """
    if amount == 0:
        return "Free (0 SAR)"

    if isinstance(amount, float):
        if amount.is_integer():
            return f"{int(amount):,} SAR"
        else:
            return f"{amount:,.2f} SAR"

    return f"{amount:,} SAR"


def convert_currency(
    amount: float,
    from_currency: str = "SAR",
    to_currency: str = "USD"
) -> float:
    """
    Convert amount from one currency to another.

    تحويل مبلغ من عملة إلى أخرى.

    Args:
        amount: Amount to convert
        from_currency: Source currency code
        to_currency: Target currency code

    Returns:
        Converted amount
    """
    if from_currency not in EXCHANGE_RATES or to_currency not in EXCHANGE_RATES:
        return amount

    # Convert to SAR first if needed
    if from_currency != "SAR":
        amount_in_sar = amount / EXCHANGE_RATES[from_currency]
    else:
        amount_in_sar = amount

    # Convert from SAR to target currency
    converted = amount_in_sar * EXCHANGE_RATES[to_currency]

    return round(converted, 2)


def calculate_total_fees(services: List[Dict]) -> Dict[str, Union[float, str]]:
    """
    Calculate total fees from multiple services.

    حساب إجمالي الرسوم من خدمات متعددة.

    Args:
        services: List of service dictionaries with fee information

    Returns:
        Dictionary with total fees and breakdown
    """
    total_sar = 0.0
    fees_breakdown = []
    has_variable = False

    for service in services:
        fees = service.get("fees", {})
        amount = fees.get("amount", 0)

        if isinstance(amount, str) and amount.lower() in ["متغيرة", "varies", "variable"]:
            has_variable = True
            continue

        if isinstance(amount, (int, float)):
            total_sar += float(amount)
            fees_breakdown.append({
                "service": service.get("name_ar", "غير محدد"),
                "amount": amount
            })

    return {
        "total_sar": total_sar,
        "total_formatted": format_sar_amount(total_sar),
        "fees_breakdown": fees_breakdown,
        "has_variable_fees": has_variable,
        "service_count": len(services),
    }


def apply_discount(original_amount: float, discount_percent: float = 0) -> Dict[str, float]:
    """
    Calculate discount on an amount.

    حساب الخصم على مبلغ.

    Args:
        original_amount: Original amount in SAR
        discount_percent: Discount percentage (0-100)

    Returns:
        Dictionary with original, discount, and final amounts
    """
    if discount_percent < 0 or discount_percent > 100:
        discount_percent = 0

    discount_amount = (original_amount * discount_percent) / 100
    final_amount = original_amount - discount_amount

    return {
        "original": original_amount,
        "discount_percent": discount_percent,
        "discount_amount": round(discount_amount, 2),
        "final_amount": round(final_amount, 2),
    }


def estimate_service_cost(
    service: Dict,
    additional_charges: float = 0,
    discount_percent: float = 0
) -> Dict:
    """
    Estimate total cost for a service with optional charges and discounts.

    تقدير التكلفة الإجمالية للخدمة مع الرسوم والخصومات.

    Args:
        service: Service dictionary with fee information
        additional_charges: Additional charges to add
        discount_percent: Discount percentage to apply

    Returns:
        Cost estimation dictionary
    """
    fees = service.get("fees", {})
    base_amount = fees.get("amount", 0)

    # Handle variable fees
    if isinstance(base_amount, str):
        return {
            "base_fee": "متغيرة",
            "note": "لا يمكن حساب التكلفة الدقيقة - تختلف حسب الحالة",
            "additional_charges": additional_charges,
            "total": "متغيرة",
        }

    base_amount = float(base_amount) if isinstance(base_amount, (int, float)) else 0

    # Apply additional charges
    with_charges = base_amount + additional_charges

    # Apply discount
    if discount_percent > 0:
        discount_amount = (with_charges * discount_percent) / 100
        final_amount = with_charges - discount_amount
    else:
        discount_amount = 0
        final_amount = with_charges

    return {
        "base_fee": round(base_amount, 2),
        "additional_charges": round(additional_charges, 2),
        "subtotal": round(with_charges, 2),
        "discount_percent": discount_percent,
        "discount_amount": round(discount_amount, 2),
        "total_amount": round(final_amount, 2),
        "total_formatted": format_sar_amount(final_amount),
    }


def compare_service_costs(services: List[Dict]) -> Dict:
    """
    Compare costs across multiple services.

    مقارنة التكاليف عبر خدمات متعددة.

    Args:
        services: List of service dictionaries

    Returns:
        Cost comparison dictionary
    """
    costs = []

    for service in services:
        fees = service.get("fees", {})
        amount = fees.get("amount", 0)

        costs.append({
            "service_id": service.get("id"),
            "service_name": service.get("name_ar"),
            "fee_amount": amount,
            "fee_formatted": format_sar_amount(amount) if isinstance(amount, (int, float)) else amount,
            "processing_time": service.get("processing_time"),
        })

    # Sort by cost
    costs.sort(key=lambda x: float(x["fee_amount"]) if isinstance(x["fee_amount"], (int, float)) else float("inf"))

    # Calculate statistics
    numeric_costs = [c["fee_amount"] for c in costs if isinstance(c["fee_amount"], (int, float))]

    stats = {
        "services_compared": len(services),
        "costs": costs,
    }

    if numeric_costs:
        stats["cheapest"] = min(numeric_costs)
        stats["most_expensive"] = max(numeric_costs)
        stats["average_cost"] = round(sum(numeric_costs) / len(numeric_costs), 2)
        stats["total_cost"] = round(sum(numeric_costs), 2)

    return stats


def get_processing_time_estimate(services: List[Dict]) -> Dict:
    """
    Estimate total processing time for multiple services.

    تقدير إجمالي وقت المعالجة للخدمات المتعددة.

    Args:
        services: List of service dictionaries

    Returns:
        Processing time estimates dictionary
    """
    estimates = []

    for service in services:
        processing_time = service.get("processing_time", "غير محدد")
        estimates.append({
            "service_name": service.get("name_ar"),
            "processing_time": processing_time,
        })

    # Try to calculate total days
    total_days = 0
    has_variable = False

    for service in services:
        processing_time = service.get("processing_time", "")
        if "يوم" in processing_time:
            # Extract number of days
            match = re.search(r'(\d+)', processing_time)
            if match:
                days = int(match.group(1))
                total_days += days
        else:
            has_variable = True

    return {
        "individual_estimates": estimates,
        "total_estimated_days": total_days if not has_variable else "متغير",
        "has_variable_timing": has_variable,
        "note": "بعض الخدمات قد تتطلب وقتاً أطول حسب الظروف" if has_variable else "",
    }
