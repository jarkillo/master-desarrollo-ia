"""Internationalization module for AI Dev Academy backend."""

from typing import Any

from .bug_templates_en import BUG_TEMPLATES_EN
from .bug_templates_es import BUG_TEMPLATES_ES


def get_bug_template_i18n(template_id: str, language: str = "es") -> dict[str, Any]:
    """
    Get translated bug template metadata.

    Args:
        template_id: The bug template ID (e.g., "bug_001")
        language: Language code ("es" or "en")

    Returns:
        Dictionary with translated title, description, and bug details
    """
    translations = BUG_TEMPLATES_ES if language == "es" else BUG_TEMPLATES_EN

    if template_id not in translations:
        raise ValueError(f"Translation not found for template: {template_id}")

    return translations[template_id]


__all__ = [
    "get_bug_template_i18n",
    "BUG_TEMPLATES_ES",
    "BUG_TEMPLATES_EN",
]
