"""
NTRLI' AI - User Controller
Provides USER-level AI access for app customers

IMPORTANT: This controller does NOT have access to ADMIN APIs.
Users can only access USER and GENERAL APIs.
"""

import asyncio
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime

from ..core.ntrli_ai_engine import NTRLIAIEngine, SynthesizedResponse
from ..core.ai_selector import AISelector, TaskType
from ..config.api_config import APIConfig, APIType

logger = logging.getLogger(__name__)


class UserController:
    """
    User Controller for App Customers

    SECURITY: This controller is RESTRICTED to USER and GENERAL APIs only.
    ADMIN APIs are NOT accessible through this controller.

    Features:
    - Access to USER APIs
    - Access to GENERAL APIs
    - NO access to ADMIN APIs
    - Rate limiting support
    - Usage tracking
    """

    def __init__(self, user_id: int, username: str = None):
        """
        Initialize User Controller

        Args:
            user_id: The user's unique ID
            username: Optional username for logging
        """
        self.user_id = user_id
        self.username = username or f"user_{user_id}"
        self._session_start = datetime.now()

        # User-level access only (is_admin=False)
        self._engine = NTRLIAIEngine(is_admin=False)
        self._selector = AISelector(is_admin=False)

        # Usage tracking
        self._query_count = 0
        self._token_count = 0
        self._last_query_time: Optional[datetime] = None

        # Rate limiting (configurable)
        self.rate_limit_queries_per_minute = 20
        self.rate_limit_tokens_per_day = 100000

        logger.info(f"UserController initialized for user: {self.username}")

    def _check_rate_limit(self) -> bool:
        """Check if user has exceeded rate limits"""
        # Simple rate limiting - can be enhanced
        if self._last_query_time:
            time_diff = (datetime.now() - self._last_query_time).total_seconds()
            if time_diff < 3:  # Minimum 3 seconds between queries
                return False
        return True

    def _can_access_api(self, api_name: str) -> bool:
        """
        Check if user can access a specific API.
        Users CANNOT access ADMIN APIs.
        """
        if "ADMIN" in api_name.upper():
            logger.warning(f"User {self.username} attempted to access ADMIN API: {api_name}")
            return False
        return True

    # ========================================
    # User AI Access Methods
    # ========================================

    async def query(self, prompt: str, task_type: TaskType = None,
                    **kwargs) -> SynthesizedResponse:
        """
        Query NTRLI' AI using USER-level APIs

        Args:
            prompt: The user's query
            task_type: Type of task (auto-detected if None)
            **kwargs: Additional parameters

        Returns:
            SynthesizedResponse from NTRLI' AI
        """
        # Rate limiting check
        if not self._check_rate_limit():
            return SynthesizedResponse(
                content="Please wait a moment before sending another message.",
                confidence=1.0,
                sources=["rate_limiter"],
                reasoning="Rate limit exceeded",
                ntrli_enhanced=False
            )

        self._query_count += 1
        self._last_query_time = datetime.now()

        # User queries don't use synthesis (simpler, faster)
        response = await self._engine.query(
            prompt=prompt,
            task_type=task_type,
            use_synthesis=False,  # Users get single-provider responses
            **kwargs
        )

        return response

    async def chat(self, message: str, conversation_history: List[Dict[str, str]] = None,
                   **kwargs) -> SynthesizedResponse:
        """
        Chat with NTRLI' AI (conversational mode)

        Args:
            message: User's message
            conversation_history: Previous messages for context
            **kwargs: Additional parameters

        Returns:
            SynthesizedResponse
        """
        if not self._check_rate_limit():
            return SynthesizedResponse(
                content="Please wait a moment before sending another message.",
                confidence=1.0,
                sources=["rate_limiter"],
                reasoning="Rate limit exceeded",
                ntrli_enhanced=False
            )

        # Build context from history
        context = None
        if conversation_history:
            context = "\n".join([
                f"{msg['role']}: {msg['content']}"
                for msg in conversation_history[-5:]  # Last 5 messages
            ])

        return await self._engine.query(
            prompt=message,
            context=context,
            task_type=TaskType.CHAT,
            use_synthesis=False,
            **kwargs
        )

    async def ask_code_help(self, question: str, code_snippet: str = None,
                             language: str = None, **kwargs) -> SynthesizedResponse:
        """
        Get coding help from NTRLI' AI

        Args:
            question: The coding question
            code_snippet: Optional code to analyze
            language: Programming language
            **kwargs: Additional parameters

        Returns:
            SynthesizedResponse with code help
        """
        prompt = question
        if code_snippet:
            prompt = f"""Question: {question}

Code ({language or 'unknown language'}):
```
{code_snippet}
```

Please help with this code."""

        return await self._engine.query(
            prompt=prompt,
            task_type=TaskType.CODE,
            use_synthesis=False,
            **kwargs
        )

    async def analyze_text(self, text: str, analysis_type: str = "general",
                            **kwargs) -> SynthesizedResponse:
        """
        Analyze text using NTRLI' AI

        Args:
            text: Text to analyze
            analysis_type: Type of analysis (general, sentiment, summary, etc.)
            **kwargs: Additional parameters

        Returns:
            SynthesizedResponse with analysis
        """
        prompt = f"""Analyze the following text.
Analysis type: {analysis_type}

Text to analyze:
{text}

Provide a clear, structured analysis."""

        return await self._engine.query(
            prompt=prompt,
            task_type=TaskType.ANALYSIS,
            use_synthesis=False,
            **kwargs
        )

    # ========================================
    # User Information Methods
    # ========================================

    def get_available_capabilities(self) -> List[str]:
        """Get list of capabilities available to this user"""
        # Users have access to USER and GENERAL APIs only
        config = APIConfig()
        user_apis = config.get_all_apis_for_user()

        capabilities = set()
        for api_config in user_apis.values():
            capabilities.update(api_config.capabilities or [])

        return list(capabilities)

    def get_usage_stats(self) -> Dict[str, Any]:
        """Get user's usage statistics"""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "session_start": self._session_start.isoformat(),
            "query_count": self._query_count,
            "token_count": self._token_count,
            "last_query": self._last_query_time.isoformat() if self._last_query_time else None
        }

    def get_available_apis(self) -> List[Dict[str, Any]]:
        """
        Get list of APIs available to this user.
        NOTE: ADMIN APIs are NOT included.
        """
        config = APIConfig()
        user_apis = config.get_all_apis_for_user()

        return [
            {
                "name": name,
                "provider": cfg.provider,
                "capabilities": cfg.capabilities,
                # Don't expose API keys to users
            }
            for name, cfg in user_apis.items()
        ]

    async def health_check(self) -> Dict[str, Any]:
        """Check health of USER-accessible APIs only"""
        health = await self._selector.health_check_all()

        # Filter to only show USER-accessible APIs
        config = APIConfig()
        user_api_names = set(config.get_all_apis_for_user().keys())

        return {
            name: status
            for name, status in health.items()
            if name in user_api_names
        }

    def reset_session(self):
        """Reset user session statistics"""
        self._query_count = 0
        self._token_count = 0
        self._last_query_time = None
        self._session_start = datetime.now()
        logger.info(f"Session reset for user: {self.username}")
