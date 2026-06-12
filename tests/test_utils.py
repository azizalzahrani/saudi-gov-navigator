"""
Utils Tests - اختبارات الأدوات المساعدة

Unit tests for Arabic utilities and the fee calculator.
"""

import unittest

from saudi_gov.utils.arabic_utils import (
    format_phone_number,
    is_arabic_text,
    normalize_arabic_text,
    validate_arabic_phone,
    validate_iqama,
    validate_saudi_id,
)
from saudi_gov.utils.fee_calculator import (
    calculate_total_fees,
    convert_currency,
    format_sar_amount,
)


class TestArabicUtils(unittest.TestCase):
    """Test cases for Arabic text utilities."""

    def test_normalize_removes_diacritics(self):
        self.assertEqual(normalize_arabic_text("مُحَمَّد"), "محمد")

    def test_is_arabic_text(self):
        self.assertTrue(is_arabic_text("جواز السفر"))
        self.assertFalse(is_arabic_text("passport"))

    def test_validate_arabic_phone(self):
        self.assertTrue(validate_arabic_phone("0512345678"))
        self.assertTrue(validate_arabic_phone("+966512345678"))
        self.assertTrue(validate_arabic_phone("00966512345678"))
        self.assertFalse(validate_arabic_phone("12345"))
        self.assertFalse(validate_arabic_phone("0712345678"))


class TestPhoneFormatting(unittest.TestCase):
    """format_phone_number must produce the same output for equivalent inputs."""

    def test_local_number(self):
        self.assertEqual(format_phone_number("0512345678"), "051 234 5678")

    def test_plus_966_number(self):
        self.assertEqual(format_phone_number("+966512345678"), "051 234 5678")

    def test_00966_number(self):
        self.assertEqual(format_phone_number("00966512345678"), "051 234 5678")

    def test_international_format(self):
        self.assertEqual(
            format_phone_number("0512345678", format_type="international"),
            "+966 51 234 5678",
        )

    def test_unrecognized_returns_input(self):
        self.assertEqual(format_phone_number("12345"), "12345")


class TestIdValidation(unittest.TestCase):
    """Saudi ID and Iqama numbers carry a Luhn check digit."""

    VALID_ID = "1045678909"
    VALID_IQAMA = "2345678904"
    INVALID_CHECK_DIGIT = "1045678900"

    def test_valid_saudi_id(self):
        self.assertTrue(validate_saudi_id(self.VALID_ID))

    def test_saudi_id_with_separators(self):
        spaced = f"{self.VALID_ID[:4]} {self.VALID_ID[4:]}"
        self.assertTrue(validate_saudi_id(spaced))

    def test_invalid_check_digit_rejected(self):
        self.assertFalse(validate_saudi_id(self.INVALID_CHECK_DIGIT))

    def test_wrong_prefix_rejected(self):
        self.assertFalse(validate_saudi_id(self.VALID_IQAMA))  # starts with 2
        self.assertFalse(validate_iqama(self.VALID_ID))  # starts with 1

    def test_valid_iqama(self):
        self.assertTrue(validate_iqama(self.VALID_IQAMA))

    def test_wrong_length_rejected(self):
        self.assertFalse(validate_saudi_id("1234"))
        self.assertFalse(validate_iqama("2"))


class TestFeeCalculator(unittest.TestCase):
    """Test cases for fee calculation helpers."""

    def test_format_sar_free(self):
        self.assertIn("مجاني", format_sar_amount(0))

    def test_format_sar_amount(self):
        self.assertEqual(format_sar_amount(300), "300 ريال سعودي")

    def test_convert_currency_identity(self):
        self.assertEqual(convert_currency(100, "SAR", "SAR"), 100)

    def test_calculate_total_fees_skips_variable(self):
        services = [
            {"name_ar": "أ", "fees": {"amount": 100}},
            {"name_ar": "ب", "fees": {"amount": "متغيرة"}},
            {"name_ar": "ج", "fees": {"amount": 50}},
        ]
        totals = calculate_total_fees(services)
        self.assertEqual(totals["total_sar"], 150.0)
        self.assertTrue(totals["has_variable_fees"])
        self.assertEqual(totals["service_count"], 3)


if __name__ == "__main__":
    unittest.main()
