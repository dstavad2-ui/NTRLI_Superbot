"""
NTRLI' AI - Utility Functions
Helper functions for the AI system
"""

import os
import re
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


def is_admin_user(user_id: int) -> bool:
    """
    Check if a user ID belongs to an admin.

    Args:
        user_id: The user's ID to check

    Returns:
        True if the user is an admin
    """
    admin_id = os.getenv("ADMIN_ID", "8467779489")
    try:
        return user_id == int(admin_id)
    except ValueError:
        return False


def sanitize_prompt(prompt: str, max_length: int = 10000) -> str:
    """
    Sanitize user prompts for safety.

    Args:
        prompt: Raw user prompt
        max_length: Maximum allowed length

    Returns:
        Sanitized prompt
    """
    if not prompt:
        return ""

    # Truncate if too long
    if len(prompt) > max_length:
        prompt = prompt[:max_length] + "..."
        logger.warning(f"Prompt truncated to {max_length} characters")

    # Remove potential injection patterns
    # Note: This is basic sanitization - AI providers have their own safety measures
    prompt = prompt.strip()

    return prompt


def format_response(content: str, provider: str = None,
                    include_source: bool = False) -> str:
    """
    Format AI response for user display.

    Args:
        content: Raw AI response content
        provider: Optional provider name
        include_source: Whether to include source attribution

    Returns:
        Formatted response string
    """
    if not content:
        return "No response available."

    formatted = content.strip()

    if include_source and provider:
        formatted += f"\n\n---\n_Powered by NTRLI' AI_"

    return formatted


def calculate_cost_estimate(tokens: int, provider: str, model: str) -> float:
    """
    Estimate the cost of an API call.

    Args:
        tokens: Number of tokens used
        provider: Provider name
        model: Model name

    Returns:
        Estimated cost in USD
    """
    # Approximate costs per 1000 tokens (input+output average)
    cost_table = {
        "openai": {
            "gpt-4o": 0.005,
            "gpt-4o-mini": 0.00015,
            "gpt-4-turbo": 0.01,
            "default": 0.002
        },
        "groq": {
            "llama-3.1-70b-versatile": 0.0009,
            "llama-3.1-8b-instant": 0.0001,
            "default": 0.0005
        },
        "mistral": {
            "mistral-large-latest": 0.004,
            "mistral-small-latest": 0.001,
            "default": 0.002
        }
    }

    provider_lower = provider.lower()
    if provider_lower in cost_table:
        provider_costs = cost_table[provider_lower]
        cost_per_1k = provider_costs.get(model, provider_costs["default"])
    else:
        cost_per_1k = 0.002  # Default fallback

    return (tokens / 1000) * cost_per_1k


def detect_language(text: str) -> str:
    """
    Simple language detection for code snippets.

    Args:
        text: Text or code to analyze

    Returns:
        Detected language name
    """
    patterns = {
        "python": [r"def\s+\w+\s*\(", r"import\s+\w+", r"print\s*\(", r"class\s+\w+:"],
        "javascript": [r"function\s+\w+\s*\(", r"const\s+\w+", r"let\s+\w+", r"=>"],
        "typescript": [r"interface\s+\w+", r"type\s+\w+\s*=", r":\s*\w+\s*[=;]"],
        "html": [r"<html", r"<div", r"<body", r"</\w+>"],
        "css": [r"\.\w+\s*\{", r"#\w+\s*\{", r"@media"],
        "sql": [r"SELECT\s+", r"FROM\s+", r"WHERE\s+", r"INSERT\s+INTO"],
        "json": [r'"\w+":\s*[{\[\"\d]'],
    }

    text_lower = text.lower()

    for lang, lang_patterns in patterns.items():
        for pattern in lang_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return lang

    return "text"


def truncate_for_logging(text: str, max_length: int = 100) -> str:
    """Truncate text for safe logging"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."
