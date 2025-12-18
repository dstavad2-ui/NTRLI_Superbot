"""
NTRLI' AI - API Configuration
Manages all AI API keys with Admin/User separation

IMPORTANT: All API keys must be set via environment variables.
See env.example for required environment variable names.
"""

import os
from pathlib import Path
from enum import Enum

# Load encrypted secrets (decrypts using ADMIN_ID)
try:
    from .secrets import load_encrypted_secrets
    load_encrypted_secrets()
except ImportError:
    pass  # Fallback to environment variables
from dataclasses import dataclass
from typing import Dict, List, Optional

class APIType(Enum):
    """API access type classification"""
    ADMIN = "admin"      # Only accessible by admin in Admin Panel
    USER = "user"        # Accessible by app customers
    GENERAL = "general"  # Accessible by both (based on context)


@dataclass
class AIProviderConfig:
    """Configuration for a single AI provider"""
    name: str
    api_key: str
    api_type: APIType
    provider: str  # openai, groq, mistral
    owner: str
    base_url: Optional[str] = None
    default_model: Optional[str] = None
    capabilities: List[str] = None
    priority_score: float = 1.0  # Higher = more preferred

    def __post_init__(self):
        if self.capabilities is None:
            self.capabilities = []

    def is_configured(self) -> bool:
        """Check if API key is properly configured"""
        return bool(self.api_key and not self.api_key.startswith("YOUR_"))


class APIConfig:
    """
    Central API Configuration Manager
    Separates ADMIN and USER APIs strictly

    API Keys must be set via environment variables:
    - ADMIN_OPENAI_API_KEY: Admin OpenAI API key
    - ADMIN_MISTRAL_API_KEY: Admin Mistral API key
    - USER_OPENAI_API_KEY: User OpenAI API key
    - USER_MISTRAL_API_KEY: User Mistral API key
    - GROQ_API_KEY: Groq API key (general purpose)
    """

    def __init__(self):
        self._admin_apis: Dict[str, AIProviderConfig] = {}
        self._user_apis: Dict[str, AIProviderConfig] = {}
        self._general_apis: Dict[str, AIProviderConfig] = {}
        self._load_apis()

    def _load_apis(self):
        """Load all configured AI APIs from environment variables"""

        # ========================================
        # ADMIN APIs - ONLY for Admin Panel
        # ========================================

        # ADMIN OpenAI - Full unrestricted access for admin
        admin_openai_key = os.getenv("ADMIN_OPENAI_API_KEY", "")
        if admin_openai_key:
            self._admin_apis["ADMIN_OPEN-AI_Super_APK"] = AIProviderConfig(
                name="ADMIN_OPEN-AI_Super_APK",
                api_key=admin_openai_key,
                api_type=APIType.ADMIN,
                provider="openai",
                owner="Dennis",
                base_url="https://api.openai.com/v1",
                default_model="gpt-4o",
                capabilities=["chat", "vision", "code", "analysis", "function_calling", "embeddings", "moderation"],
                priority_score=10.0  # Highest priority for admin
            )

        # ADMIN Mistral AI - Full unrestricted access for admin
        admin_mistral_key = os.getenv("ADMIN_MISTRAL_API_KEY", "")
        if admin_mistral_key:
            self._admin_apis["ADMIN_mistral-AI_API"] = AIProviderConfig(
                name="ADMIN_mistral-AI_API",
                api_key=admin_mistral_key,
                api_type=APIType.ADMIN,
                provider="mistral",
                owner="Dennis",
                base_url="https://api.mistral.ai/v1",
                default_model="mistral-large-latest",
                capabilities=["chat", "code", "analysis", "function_calling", "embeddings"],
                priority_score=9.0
            )

        # ========================================
        # USER APIs - For App Customers
        # ========================================

        # USER OpenAI - For customer interactions
        user_openai_key = os.getenv("USER_OPENAI_API_KEY", "")
        if user_openai_key:
            self._user_apis["USER_OPEN-AI_Super_APK"] = AIProviderConfig(
                name="USER_OPEN-AI_Super_APK",
                api_key=user_openai_key,
                api_type=APIType.USER,
                provider="openai",
                owner="Dennis",
                base_url="https://api.openai.com/v1",
                default_model="gpt-4o-mini",
                capabilities=["chat", "code", "analysis"],
                priority_score=8.0
            )

        # USER Mistral AI - For customer interactions
        user_mistral_key = os.getenv("USER_MISTRAL_API_KEY", "")
        if user_mistral_key:
            self._user_apis["USERS_mistral-AI_Super_APK"] = AIProviderConfig(
                name="USERS_mistral-AI_Super_APK",
                api_key=user_mistral_key,
                api_type=APIType.USER,
                provider="mistral",
                owner="Dennis",
                base_url="https://api.mistral.ai/v1",
                default_model="mistral-small-latest",
                capabilities=["chat", "code", "analysis"],
                priority_score=7.0
            )

        # ========================================
        # GENERAL APIs - Context-dependent access
        # ========================================

        # Groq AI - Fast inference, general purpose
        groq_key = os.getenv("GROQ_API_KEY", "")
        if groq_key:
            self._general_apis["Groq-AI_API"] = AIProviderConfig(
                name="Groq-AI_API",
                api_key=groq_key,
                api_type=APIType.GENERAL,
                provider="groq",
                owner="Y ki mail",
                base_url="https://api.groq.com/openai/v1",
                default_model="llama-3.1-70b-versatile",
                capabilities=["chat", "code", "fast_inference"],
                priority_score=7.5  # Good balance of speed and capability
            )

    def get_admin_apis(self) -> Dict[str, AIProviderConfig]:
        """Get all ADMIN-only APIs - restricted to Admin Panel"""
        return self._admin_apis.copy()

    def get_user_apis(self) -> Dict[str, AIProviderConfig]:
        """Get all USER APIs - for customer use"""
        return self._user_apis.copy()

    def get_general_apis(self) -> Dict[str, AIProviderConfig]:
        """Get general purpose APIs"""
        return self._general_apis.copy()

    def get_all_apis_for_admin(self) -> Dict[str, AIProviderConfig]:
        """Admin gets access to ALL APIs without restrictions"""
        all_apis = {}
        all_apis.update(self._admin_apis)
        all_apis.update(self._user_apis)
        all_apis.update(self._general_apis)
        return all_apis

    def get_all_apis_for_user(self) -> Dict[str, AIProviderConfig]:
        """Users only get USER and GENERAL APIs"""
        user_accessible = {}
        user_accessible.update(self._user_apis)
        user_accessible.update(self._general_apis)
        return user_accessible

    def get_api_by_name(self, name: str, is_admin: bool = False) -> Optional[AIProviderConfig]:
        """Get specific API by name, respecting access control"""
        if is_admin:
            all_apis = self.get_all_apis_for_admin()
        else:
            all_apis = self.get_all_apis_for_user()

        return all_apis.get(name)

    def validate_admin_access(self, api_name: str) -> bool:
        """Check if an API requires admin access"""
        return api_name in self._admin_apis or "ADMIN" in api_name.upper()

    def get_configured_count(self) -> Dict[str, int]:
        """Get count of configured APIs by type"""
        return {
            "admin": len(self._admin_apis),
            "user": len(self._user_apis),
            "general": len(self._general_apis),
            "total": len(self._admin_apis) + len(self._user_apis) + len(self._general_apis)
        }
