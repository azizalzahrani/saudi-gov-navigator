"""
Arabic Text Utilities - مساعدات النصوص العربية

Functions for processing and normalizing Arabic text.
وظائف لمعالجة وتطبيع النصوص العربية.
"""

import re
from typing import Optional


def normalize_arabic_text(text: str) -> str:
    """
    Normalize Arabic text by removing diacritics and standardizing characters.

    تطبيع النص العربي بإزالة التشكيل وتوحيد الأحرف.

    Args:
        text: Arabic text to normalize

    Returns:
        Normalized Arabic text
    """
    if not text:
        return text

    # Remove diacritical marks
    diacritics = [
        '\u064B',  # FATHATAN
        '\u064C',  # DAMMATAN
        '\u064D',  # KASRATAN
        '\u064E',  # FATHA
        '\u064F',  # DAMMA
        '\u0650',  # KASRA
        '\u0651',  # SHADDA
        '\u0652',  # SUKUN
    ]

    normalized = text
    for diacritic in diacritics:
        normalized = normalized.replace(diacritic, '')

    # Normalize various forms of alef
    normalized = normalized.replace('\u0649', '\u064A')  # Alef maksura to ya
    normalized = normalized.replace('\u0671', '\u0627')  # Alef wasla to alef

    # Normalize teh marbuta
    normalized = normalized.replace('\u0629', '\u0647')  # Teh marbuta to hah

    # Remove extra whitespace
    normalized = ' '.join(normalized.split())

    return normalized


def remove_diacritics(text: str) -> str:
    """
    Remove all diacritical marks from Arabic text.

    إزالة جميع علامات التشكيل من النص العربي.

    Args:
        text: Arabic text

    Returns:
        Text without diacritics
    """
    if not text:
        return text

    diacritics = re.compile(r'[\u064B-\u0652\u0640]')
    return diacritics.sub('', text)


def is_arabic_text(text: str) -> bool:
    """
    Check if text contains Arabic characters.

    التحقق من وجود أحرف عربية في النص.

    Args:
        text: Text to check

    Returns:
        True if text contains Arabic characters, False otherwise
    """
    if not text:
        return False

    arabic_pattern = re.compile(r'[\u0600-\u06FF]')
    return bool(arabic_pattern.search(text))


def transliterate_arabic(text: str) -> str:
    """
    Basic transliteration of Arabic to Latin characters.

    تحويل بسيط من العربية إلى أحرف لاتينية.

    Args:
        text: Arabic text to transliterate

    Returns:
        Transliterated text
    """
    # Common Arabic to Latin mappings
    arabic_to_latin = {
        'ا': 'a',
        'ب': 'b',
        'ت': 't',
        'ث': 'th',
        'ج': 'j',
        'ح': 'h',
        'خ': 'kh',
        'د': 'd',
        'ذ': 'dh',
        'ر': 'r',
        'ز': 'z',
        'س': 's',
        'ش': 'sh',
        'ص': 's',
        'ض': 'd',
        'ط': 't',
        'ظ': 'z',
        'ع': 'a',
        'غ': 'gh',
        'ف': 'f',
        'ق': 'q',
        'ك': 'k',
        'ل': 'l',
        'م': 'm',
        'ن': 'n',
        'ه': 'h',
        'و': 'w',
        'ي': 'y',
        'ة': 'h',
        'ئ': 'y',
        'ؤ': 'w',
        'أ': 'a',
        'إ': 'i',
        'آ': 'aa',
        'ى': 'a',
    }

    transliterated = ""
    for char in text:
        transliterated += arabic_to_latin.get(char, char)

    return transliterated


def count_arabic_words(text: str) -> int:
    """
    Count the number of Arabic words in text.

    عد عدد الكلمات العربية في النص.

    Args:
        text: Text to count

    Returns:
        Number of Arabic words
    """
    if not text:
        return 0

    words = text.split()
    arabic_words = sum(1 for word in words if is_arabic_text(word))
    return arabic_words


def split_arabic_text(text: str, max_chars: int = 100) -> list:
    """
    Split Arabic text into chunks of maximum character length.

    تقسيم النص العربي إلى أجزاء بحد أقصى من الأحرف.

    Args:
        text: Text to split
        max_chars: Maximum characters per chunk

    Returns:
        List of text chunks
    """
    if not text:
        return []

    chunks = []
    current_chunk = ""

    words = text.split()
    for word in words:
        if len(current_chunk) + len(word) + 1 <= max_chars:
            if current_chunk:
                current_chunk += " " + word
            else:
                current_chunk = word
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = word

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def reverse_arabic_string(text: str) -> str:
    """
    Reverse an Arabic string while preserving character direction.

    عكس سلسلة عربية مع الحفاظ على اتجاه الأحرف.

    Args:
        text: Arabic text to reverse

    Returns:
        Reversed text
    """
    if not text:
        return text

    # Reverse the string
    reversed_text = text[::-1]

    # Handle combining characters if needed
    # For most cases, simple reversal works
    return reversed_text


def validate_arabic_phone(phone: str) -> bool:
    """
    Validate a Saudi Arabian phone number.

    التحقق من رقم هاتف سعودي.

    Args:
        phone: Phone number to validate

    Returns:
        True if valid Saudi phone number, False otherwise
    """
    # Remove common separators
    cleaned = re.sub(r'[\s\-()]+', '', phone)

    # Saudi phone patterns
    # +966XXXXXXXXX, 00966XXXXXXXXX, or 05XXXXXXXXX
    patterns = [
        r'^\+966\d{9}$',      # +966 format
        r'^00966\d{9}$',      # 00966 format
        r'^05\d{8}$',         # 05 format
    ]

    return any(re.match(pattern, cleaned) for pattern in patterns)


def _luhn_checksum_valid(digits: str) -> bool:
    """
    Validate a digit string with the Luhn algorithm.

    Saudi national ID and Iqama numbers use a Luhn check digit.
    """
    total = 0
    # Process from the rightmost digit; double every second digit.
    for index, char in enumerate(reversed(digits)):
        digit = int(char)
        if index % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit
    return total % 10 == 0


def validate_saudi_id(id_number: str) -> bool:
    """
    Validate a Saudi Arabian National ID number (رقم الهوية الوطنية).

    التحقق من رقم الهوية الوطنية السعودية.

    Args:
        id_number: ID number to validate

    Returns:
        True if valid Saudi ID, False otherwise
    """
    # Remove spaces and dashes
    cleaned = re.sub(r'[\s\-]+', '', id_number)

    # Saudi ID should be 10 digits, starting with 1
    if not re.match(r'^1\d{9}$', cleaned):
        return False

    return _luhn_checksum_valid(cleaned)


def validate_iqama(iqama_number: str) -> bool:
    """
    Validate a Resident Identity Card (Iqama) number.

    التحقق من رقم الإقامة.

    Args:
        iqama_number: Iqama number to validate

    Returns:
        True if valid Iqama, False otherwise
    """
    # Remove spaces and dashes
    cleaned = re.sub(r'[\s\-]+', '', iqama_number)

    # Iqama should be 10 digits, starting with 2
    if not re.match(r'^2\d{9}$', cleaned):
        return False

    return _luhn_checksum_valid(cleaned)


def format_phone_number(phone: str, format_type: str = "saudi") -> str:
    """
    Format a phone number for display.

    تنسيق رقم هاتف للعرض.

    Args:
        phone: Phone number to format
        format_type: Format type ("saudi", "international")

    Returns:
        Formatted phone number
    """
    # Remove all non-digit characters except +
    cleaned = re.sub(r'[^\d+]', '', phone)

    # Normalize to the 9-digit national number (5XXXXXXXX)
    national = cleaned
    for prefix in ('+966', '00966', '966'):
        if national.startswith(prefix):
            national = national[len(prefix):]
            break
    national = national.lstrip('0') if national.startswith('0') else national

    if not re.match(r'^5\d{8}$', national):
        return phone  # Not a recognizable Saudi mobile number

    if format_type == "international":
        # Format as +966 5X XXX XXXX
        return f"+966 {national[:2]} {national[2:5]} {national[5:]}"

    # Saudi local format: 05X XXX XXXX
    local = f"0{national}"
    return f"{local[:3]} {local[3:6]} {local[6:]}"
