"""
NTRLI' AI - Admin Panel Controller
Provides UNRESTRICTED access to all AI APIs for administrators
"""

import asyncio
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime

from ..core.ntrli_ai_engine import NTRLIAIEngine, SynthesizedResponse
from ..core.ai_selector import AISelector, TaskType
from ..config.api_config import APIConfig, APIType

logger = logging.getLogger(__name__)


class AdminController:
    """
    Admin Panel Controller

    IMPORTANT: This controller provides UNRESTRICTED access to ALL AI APIs.
    Only authenticated administrators should use this controller.

    Features:
    - Access to ADMIN-only APIs (no restrictions)
    - Access to USER APIs
    - Access to GENERAL APIs
    - Full synthesis capabilities
    - System management functions
    """

    def __init__(self, admin_id: int):
        """
        Initialize Admin Controller

        Args:
            admin_id: The admin's user ID for verification
        """
        self.admin_id = admin_id
        self._is_verified = False
        self._engine: Optional[NTRLIAIEngine] = None
        self._selector: Optional[AISelector] = None
        self._session_start = datetime.now()
        self._action_log: List[Dict[str, Any]] = []

        logger.info(f"AdminController initialized for admin_id: {admin_id}")

    def verify_admin(self, provided_id: int, admin_ids: List[int] = None) -> bool:
        """
        Verify administrator access

        Args:
            provided_id: ID to verify
            admin_ids: List of valid admin IDs (from config if not provided)
        """
        if admin_ids is None:
            # Default admin ID from environment
            import os
            config_admin = os.getenv("ADMIN_ID", "8467779489")
            admin_ids = [int(config_admin)]

        if provided_id in admin_ids:
            self._is_verified = True
            self._initialize_admin_access()
            self._log_action("admin_verified", {"admin_id": provided_id})
            logger.info(f"Admin verified: {provided_id}")
            return True

        logger.warning(f"Admin verification failed for: {provided_id}")
        return False

    def _initialize_admin_access(self):
        """Initialize full admin access to all APIs"""
        if self._is_verified:
            # Admin gets access to ALL APIs
            self._engine = NTRLIAIEngine(is_admin=True)
            self._selector = AISelector(is_admin=True)
            logger.info("Admin-level AI access initialized")

    def _require_verification(self):
        """Decorator helper to require admin verification"""
        if not self._is_verified:
            raise PermissionError("Admin verification required. Call verify_admin() first.")

    def _log_action(self, action: str, details: Dict[str, Any]):
        """Log admin actions for audit"""
        self._action_log.append({
            "action": action,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "admin_id": self.admin_id
        })

    # ========================================
    # ADMIN-ONLY AI Access Methods
    # ========================================

    async def query_admin_ai(self, prompt: str, task_type: TaskType = None,
                              use_synthesis: bool = True,
                              specific_api: str = None,
                              **kwargs) -> SynthesizedResponse:
        """
        Query AI using ADMIN-level APIs (unrestricted)

        Args:
            prompt: The query
            task_type: Type of task (auto-detected if None)
            use_synthesis: Use multi-AI synthesis
            specific_api: Force specific API by name
            **kwargs: Additional parameters

        Returns:
            SynthesizedResponse from NTRLI' AI
        """
        self._require_verification()
        self._log_action("query_admin_ai", {
            "prompt_length": len(prompt),
            "task_type": task_type.value if task_type else "auto",
            "specific_api": specific_api
        })

        return await self._engine.query(
            prompt=prompt,
            task_type=task_type,
            use_synthesis=use_synthesis,
            **kwargs
        )

    async def query_specific_admin_api(self, api_name: str, prompt: str,
                                        **kwargs) -> Dict[str, Any]:
        """
        Directly query a specific ADMIN API (bypass ranking)

        Args:
            api_name: Exact API name (e.g., "ADMIN_OPEN-AI_Super_APK")
            prompt: The query
            **kwargs: Additional parameters

        Returns:
            Raw response from the specific API
        """
        self._require_verification()

        config = APIConfig()
        api_config = config.get_api_by_name(api_name, is_admin=True)

        if not api_config:
            raise ValueError(f"API not found: {api_name}")

        if api_config.api_type == APIType.ADMIN or "ADMIN" in api_name.upper():
            self._log_action("direct_admin_api_call", {"api": api_name})
        else:
            self._log_action("direct_api_call", {"api": api_name})

        # Get the specific provider
        providers = self._selector._providers
        if api_name in providers:
            response = await providers[api_name].generate(
                prompt=prompt,
                system_prompt=self._engine.NTRLI_SYSTEM_PROMPT,
                **kwargs
            )
            return {
                "success": response.success,
                "content": response.content,
                "provider": response.provider,
                "model": response.model,
                "tokens": response.tokens_used,
                "latency_ms": response.latency_ms,
                "error": response.error
            }

        raise ValueError(f"Provider not initialized: {api_name}")

    # ========================================
    # System Management (Admin Only)
    # ========================================

    async def get_all_provider_stats(self) -> Dict[str, Any]:
        """Get detailed statistics for ALL providers"""
        self._require_verification()
        self._log_action("view_provider_stats", {})

        return {
            "engine_stats": self._engine.get_stats(),
            "selector_stats": self._selector.get_provider_stats(),
            "session_info": {
                "session_start": self._session_start.isoformat(),
                "admin_id": self.admin_id,
                "actions_count": len(self._action_log)
            }
        }

    async def health_check_all_apis(self) -> Dict[str, bool]:
        """Check health of ALL APIs (including ADMIN-only)"""
        self._require_verification()
        self._log_action("health_check", {})

        return await self._selector.health_check_all()

    def get_admin_api_list(self) -> List[Dict[str, Any]]:
        """Get list of ADMIN-only APIs"""
        self._require_verification()

        config = APIConfig()
        admin_apis = config.get_admin_apis()

        return [
            {
                "name": name,
                "provider": cfg.provider,
                "owner": cfg.owner,
                "capabilities": cfg.capabilities,
                "priority_score": cfg.priority_score
            }
            for name, cfg in admin_apis.items()
        ]

    def get_all_api_list(self) -> List[Dict[str, Any]]:
        """Get list of ALL APIs (admin has full visibility)"""
        self._require_verification()

        config = APIConfig()
        all_apis = config.get_all_apis_for_admin()

        return [
            {
                "name": name,
                "provider": cfg.provider,
                "api_type": cfg.api_type.value,
                "owner": cfg.owner,
                "capabilities": cfg.capabilities,
                "priority_score": cfg.priority_score
            }
            for name, cfg in all_apis.items()
        ]

    def get_action_log(self) -> List[Dict[str, Any]]:
        """Get admin action audit log"""
        self._require_verification()
        return self._action_log.copy()

    async def test_all_apis(self) -> Dict[str, Dict[str, Any]]:
        """Test all APIs with a simple query"""
        self._require_verification()
        self._log_action("test_all_apis", {})

        test_prompt = "Say 'API test successful' in exactly those words."
        results = {}

        for api_name, provider in self._selector._providers.items():
            try:
                response = await provider.generate(test_prompt)
                results[api_name] = {
                    "success": response.success,
                    "latency_ms": response.latency_ms,
                    "error": response.error
                }
            except Exception as e:
                results[api_name] = {
                    "success": False,
                    "latency_ms": 0,
                    "error": str(e)
                }

        return results

    def export_knowledge_base(self) -> str:
        """Export the NTRLI' AI knowledge base"""
        self._require_verification()
        self._log_action("export_knowledge", {})
        return self._engine.export_knowledge()

    def clear_response_cache(self):
        """Clear the response cache"""
        self._require_verification()
        self._log_action("clear_cache", {})
        self._engine.clear_cache()

    def get_ranking_for_task(self, task_type: TaskType) -> List[Dict[str, Any]]:
        """Get current AI ranking for a specific task type"""
        self._require_verification()

        ranked = self._selector.rank_providers(task_type)
        return [
            {
                "rank": i + 1,
                "name": r.config.name,
                "score": r.score,
                "provider": r.config.provider,
                "api_type": r.config.api_type.value
            }
            for i, r in enumerate(ranked)
        ]
