"""
Configuration Module - وحدة الإعدادات

Manages application configuration from environment variables and defaults.
يدير إعدادات التطبيق من متغيرات البيئة والقيم الافتراضية.
"""

import os
from typing import Optional

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - optional dependency
    def load_dotenv(*args, **kwargs) -> bool:
        """Gracefully skip .env loading when python-dotenv is unavailable."""
        return False

# Load environment variables from .env file
load_dotenv()


class Config:
    """
    Application configuration class.

    فئة إعدادات التطبيق.
    """

    # Language and Localization
    LANGUAGE: str = os.getenv("LANGUAGE", "ar")
    """
    Default language for the application.
    اللغة الافتراضية للتطبيق (ar=العربية، en=الإنجليزية)
    """

    # LLM Configuration
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openai")
    """LLM provider: openai or anthropic"""

    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4-turbo")

    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    ANTHROPIC_MODEL: str = os.getenv("ANTHROPIC_MODEL", "claude-opus")

    # Logging Configuration
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Service Endpoints
    ABSHER_API_ENDPOINT: str = os.getenv(
        "ABSHER_API_ENDPOINT", "https://www.absher.sa"
    )
    MUQEEM_API_ENDPOINT: str = os.getenv("MUQEEM_API_ENDPOINT", "https://muqeem.sa")
    QIWA_API_ENDPOINT: str = os.getenv("QIWA_API_ENDPOINT", "https://qiwa.sa")
    TAWAKKALNA_API_ENDPOINT: str = os.getenv(
        "TAWAKKALNA_API_ENDPOINT", "https://tawakkalna.sa"
    )
    BALADY_API_ENDPOINT: str = os.getenv("BALADY_API_ENDPOINT", "https://balady.gov.sa")
    MISA_API_ENDPOINT: str = os.getenv("MISA_API_ENDPOINT", "https://misa.gov.sa")
    HRSD_API_ENDPOINT: str = os.getenv("HRSD_API_ENDPOINT", "https://hrsd.org.sa")

    # Application Metadata
    VERSION: str = "0.1.0"
    APP_NAME: str = "دليل الخدمات الحكومية السعودية"
    APP_NAME_EN: str = "Saudi Gov Navigator"

    @classmethod
    def validate(cls) -> None:
        """
        Validate that required configuration is set.

        التحقق من أن الإعدادات المطلوبة مضبوطة.

        Raises:
            ValueError: If required config is missing
        """
        if cls.LLM_PROVIDER == "openai" and not cls.OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY environment variable is required when using OpenAI"
            )

        if cls.LLM_PROVIDER == "anthropic" and not cls.ANTHROPIC_API_KEY:
            raise ValueError(
                "ANTHROPIC_API_KEY environment variable is required when using Anthropic"
            )

    @classmethod
    def get_language_config(cls) -> dict:
        """
        Get language-specific configuration.

        الحصول على إعدادات محددة للغة.

        Returns:
            Dictionary with language-specific settings
        """
        return {
            "language": cls.LANGUAGE,
            "is_arabic": cls.LANGUAGE == "ar",
            "is_english": cls.LANGUAGE == "en",
        }

    @classmethod
    def get_llm_config(cls) -> dict:
        """
        Get LLM configuration.

        الحصول على إعدادات نموذج اللغة.

        Returns:
            Dictionary with LLM settings
        """
        if cls.LLM_PROVIDER == "openai":
            return {
                "provider": "openai",
                "model": cls.OPENAI_MODEL,
                "api_key": cls.OPENAI_API_KEY,
            }
        else:
            return {
                "provider": "anthropic",
                "model": cls.ANTHROPIC_MODEL,
                "api_key": cls.ANTHROPIC_API_KEY,
            }


# Export common patterns
PLATFORMS = {
    "أبشر": "absher",
    "معايش": "muqeem",
    "قوى العمل": "qiwa",
    "تواصل": "tawakkalna",
    "بلدي": "balady",
    "الهيئة العامة للاستثمار": "misa",
    "التأمينات": "hrsd",
    "نطاقات": "nitaqat",
}

# Common SAR currency format
CURRENCY = "ريال سعودي"  # Saudi Riyal
CURRENCY_CODE = "SAR"
