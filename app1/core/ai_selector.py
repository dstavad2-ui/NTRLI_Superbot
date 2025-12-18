"""
NTRLI' AI - AI Selector & Ranking System
Pre-prompt ranking algorithm to select the best AI for each task
"""

import asyncio
from enum import Enum
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import logging

from ..config.api_config import APIConfig, APIType, AIProviderConfig
from ..ai_providers.base_provider import BaseAIProvider, AIResponse
from ..ai_providers.openai_provider import OpenAIProvider
from ..ai_providers.groq_provider import GroqProvider
from ..ai_providers.mistral_provider import MistralProvider

logger = logging.getLogger(__name__)


class TaskType(Enum):
    """Types of tasks for AI selection"""
    CHAT = "chat"                    # General conversation
    CODE = "code"                    # Code generation/analysis
    ANALYSIS = "analysis"            # Data/text analysis
    VISION = "vision"                # Image understanding
    FUNCTION_CALLING = "function_calling"  # Tool use
    EMBEDDINGS = "embeddings"        # Vector embeddings
    FAST_RESPONSE = "fast_inference" # Speed-critical tasks
    MODERATION = "moderation"        # Content moderation
    CREATIVE = "creative"            # Creative writing


@dataclass
class RankedProvider:
    """Provider with calculated ranking score"""
    provider: BaseAIProvider
    config: AIProviderConfig
    score: float
    task_type: TaskType
    is_available: bool = True


class AISelector:
    """
    AI Selection and Ranking System
    Selects the best qualified AI for each action using pre-prompt ranking
    """

    def __init__(self, is_admin: bool = False):
        """
        Initialize AI Selector

        Args:
            is_admin: If True, enables access to ADMIN APIs
        """
        self.is_admin = is_admin
        self.config = APIConfig()
        self._providers: Dict[str, BaseAIProvider] = {}
        self._provider_configs: Dict[str, AIProviderConfig] = {}
        self._initialize_providers()

    def _initialize_providers(self):
        """Initialize all available AI providers based on access level"""
        if self.is_admin:
            api_configs = self.config.get_all_apis_for_admin()
        else:
            api_configs = self.config.get_all_apis_for_user()

        for name, config in api_configs.items():
            provider = self._create_provider(config)
            if provider:
                self._providers[name] = provider
                self._provider_configs[name] = config
                logger.info(f"Initialized provider: {name} ({config.provider})")

    def _create_provider(self, config: AIProviderConfig) -> Optional[BaseAIProvider]:
        """Create provider instance based on config"""
        try:
            if config.provider == "openai":
                return OpenAIProvider(
                    api_key=config.api_key,
                    base_url=config.base_url,
                    default_model=config.default_model,
                    name=config.name,
                    capabilities=config.capabilities
                )
            elif config.provider == "groq":
                return GroqProvider(
                    api_key=config.api_key,
                    base_url=config.base_url,
                    default_model=config.default_model,
                    name=config.name,
                    capabilities=config.capabilities
                )
            elif config.provider == "mistral":
                return MistralProvider(
                    api_key=config.api_key,
                    base_url=config.base_url,
                    default_model=config.default_model,
                    name=config.name,
                    capabilities=config.capabilities
                )
            else:
                logger.warning(f"Unknown provider type: {config.provider}")
                return None
        except Exception as e:
            logger.error(f"Failed to create provider {config.name}: {e}")
            return None

    def rank_providers(self, task_type: TaskType) -> List[RankedProvider]:
        """
        Rank all available providers for a specific task type.
        This is the PRE-PROMPT RANKING algorithm.

        Returns list sorted by score (highest first)
        """
        ranked = []

        for name, provider in self._providers.items():
            config = self._provider_configs[name]

            # Calculate composite score
            score = self._calculate_ranking_score(provider, config, task_type)

            ranked.append(RankedProvider(
                provider=provider,
                config=config,
                score=score,
                task_type=task_type
            ))

        # Sort by score descending
        ranked.sort(key=lambda x: x.score, reverse=True)

        logger.info(f"Ranked providers for {task_type.value}:")
        for i, r in enumerate(ranked):
            logger.info(f"  {i+1}. {r.config.name}: {r.score:.3f}")

        return ranked

    def _calculate_ranking_score(self, provider: BaseAIProvider,
                                  config: AIProviderConfig,
                                  task_type: TaskType) -> float:
        """
        Calculate ranking score for a provider on a specific task.

        Scoring factors:
        - Capability score (40%): How well the AI handles this task type
        - Priority score (25%): Configured priority from API config
        - Reliability (20%): Historical success rate
        - Latency (15%): Response speed
        """
        # Task capability score
        capability_score = provider.get_capability_score(task_type.value)

        # Configured priority (normalized to 0-1)
        priority_score = config.priority_score / 10.0

        # Historical reliability
        reliability_score = provider.get_reliability_score()

        # Latency factor (normalized, lower is better)
        avg_latency = provider.metrics.avg_latency_ms
        if avg_latency > 0:
            latency_score = min(1.0, 2000 / avg_latency)  # 2s baseline
        else:
            latency_score = 1.0  # New providers get full score

        # Weighted combination
        final_score = (
            capability_score * 0.40 +
            priority_score * 0.25 +
            reliability_score * 0.20 +
            latency_score * 0.15
        )

        return final_score

    def get_best_provider(self, task_type: TaskType) -> Optional[RankedProvider]:
        """Get the single best provider for a task"""
        ranked = self.rank_providers(task_type)
        return ranked[0] if ranked else None

    def get_top_providers(self, task_type: TaskType, n: int = 3) -> List[RankedProvider]:
        """Get top N providers for a task (for fallback strategies)"""
        ranked = self.rank_providers(task_type)
        return ranked[:n]

    async def select_and_execute(self, prompt: str, task_type: TaskType,
                                  system_prompt: Optional[str] = None,
                                  fallback: bool = True,
                                  **kwargs) -> Tuple[AIResponse, str]:
        """
        Select the best AI and execute the request.
        Automatically falls back to next best if primary fails.

        Returns:
            Tuple of (AIResponse, provider_name)
        """
        ranked = self.rank_providers(task_type)

        if not ranked:
            return AIResponse(
                content="No AI providers available",
                provider="none",
                model="none",
                tokens_used=0,
                latency_ms=0,
                success=False,
                error="No providers configured for this access level"
            ), "none"

        # Try providers in order until one succeeds
        max_attempts = len(ranked) if fallback else 1

        for i, ranked_provider in enumerate(ranked[:max_attempts]):
            provider = ranked_provider.provider
            config = ranked_provider.config

            logger.info(f"Attempting {config.name} (rank {i+1}, score {ranked_provider.score:.3f})")

            response = await provider.generate(
                prompt=prompt,
                system_prompt=system_prompt,
                **kwargs
            )

            if response.success:
                logger.info(f"Success with {config.name}")
                return response, config.name
            else:
                logger.warning(f"Failed with {config.name}: {response.error}")

        # All providers failed
        return AIResponse(
            content="All AI providers failed",
            provider="none",
            model="none",
            tokens_used=0,
            latency_ms=0,
            success=False,
            error="All providers exhausted"
        ), "none"

    async def execute_parallel(self, prompt: str, task_type: TaskType,
                                n_providers: int = 2,
                                system_prompt: Optional[str] = None,
                                **kwargs) -> List[Tuple[AIResponse, str]]:
        """
        Execute request on top N providers in parallel.
        Returns all responses for comparison or consensus.
        """
        ranked = self.get_top_providers(task_type, n_providers)

        if not ranked:
            return []

        tasks = []
        for ranked_provider in ranked:
            provider = ranked_provider.provider
            config = ranked_provider.config

            task = asyncio.create_task(
                provider.generate(prompt=prompt, system_prompt=system_prompt, **kwargs)
            )
            tasks.append((task, config.name))

        results = []
        for task, name in tasks:
            try:
                response = await task
                results.append((response, name))
            except Exception as e:
                logger.error(f"Parallel execution error for {name}: {e}")

        return results

    async def health_check_all(self) -> Dict[str, bool]:
        """Check health of all providers"""
        results = {}
        for name, provider in self._providers.items():
            try:
                results[name] = await provider.health_check()
            except Exception as e:
                logger.error(f"Health check failed for {name}: {e}")
                results[name] = False
        return results

    def get_provider_stats(self) -> Dict[str, dict]:
        """Get statistics for all providers"""
        stats = {}
        for name, provider in self._providers.items():
            config = self._provider_configs[name]
            stats[name] = {
                "provider_type": config.provider,
                "api_type": config.api_type.value,
                "owner": config.owner,
                "default_model": config.default_model,
                "total_requests": provider.metrics.total_requests,
                "success_rate": provider.get_reliability_score(),
                "avg_latency_ms": provider.metrics.avg_latency_ms,
                "total_tokens": provider.metrics.total_tokens,
                "capabilities": config.capabilities
            }
        return stats
