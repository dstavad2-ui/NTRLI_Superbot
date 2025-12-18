"""
NTRLI' AI - Base AI Provider
Abstract base class for all AI providers
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import time
import logging

logger = logging.getLogger(__name__)


@dataclass
class AIResponse:
    """Standardized AI response format"""
    content: str
    provider: str
    model: str
    tokens_used: int
    latency_ms: float
    success: bool
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class ProviderMetrics:
    """Metrics for AI provider performance tracking"""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    total_tokens: int = 0
    avg_latency_ms: float = 0.0
    last_error: Optional[str] = None
    last_success_time: Optional[float] = None
    capability_scores: Dict[str, float] = None

    def __post_init__(self):
        if self.capability_scores is None:
            self.capability_scores = {}


class BaseAIProvider(ABC):
    """
    Abstract base class for AI providers.
    All providers (OpenAI, Groq, Mistral) inherit from this.
    """

    def __init__(self, api_key: str, base_url: str, default_model: str,
                 name: str, capabilities: List[str]):
        self.api_key = api_key
        self.base_url = base_url
        self.default_model = default_model
        self.name = name
        self.capabilities = capabilities
        self.metrics = ProviderMetrics()
        self._initialize_capability_scores()

    def _initialize_capability_scores(self):
        """Initialize capability scores based on provider type"""
        # Default scores - subclasses override with specific values
        base_scores = {
            "chat": 0.8,
            "code": 0.7,
            "analysis": 0.7,
            "vision": 0.0,
            "function_calling": 0.5,
            "embeddings": 0.5,
            "fast_inference": 0.5,
            "moderation": 0.3
        }
        for cap in self.capabilities:
            if cap not in base_scores:
                base_scores[cap] = 0.5
        self.metrics.capability_scores = base_scores

    @abstractmethod
    async def generate(self, prompt: str, system_prompt: Optional[str] = None,
                       model: Optional[str] = None, **kwargs) -> AIResponse:
        """Generate AI response - must be implemented by subclasses"""
        pass

    @abstractmethod
    async def chat(self, messages: List[Dict[str, str]],
                   model: Optional[str] = None, **kwargs) -> AIResponse:
        """Multi-turn chat - must be implemented by subclasses"""
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """Check if the provider is available"""
        pass

    def get_capability_score(self, task_type: str) -> float:
        """Get the score for a specific capability"""
        return self.metrics.capability_scores.get(task_type, 0.0)

    def update_metrics(self, response: AIResponse):
        """Update provider metrics after a request"""
        self.metrics.total_requests += 1
        if response.success:
            self.metrics.successful_requests += 1
            self.metrics.last_success_time = time.time()
            self.metrics.total_tokens += response.tokens_used
            # Update average latency
            n = self.metrics.successful_requests
            self.metrics.avg_latency_ms = (
                (self.metrics.avg_latency_ms * (n - 1) + response.latency_ms) / n
            )
        else:
            self.metrics.failed_requests += 1
            self.metrics.last_error = response.error

    def get_reliability_score(self) -> float:
        """Calculate reliability score based on success rate"""
        if self.metrics.total_requests == 0:
            return 1.0  # New providers start with full trust
        return self.metrics.successful_requests / self.metrics.total_requests

    def get_overall_score(self, task_type: str) -> float:
        """
        Calculate overall score for task assignment.
        Combines capability score, reliability, and latency.
        """
        capability = self.get_capability_score(task_type)
        reliability = self.get_reliability_score()

        # Latency factor (lower is better, normalized to 0-1)
        if self.metrics.avg_latency_ms > 0:
            latency_factor = min(1.0, 1000 / self.metrics.avg_latency_ms)
        else:
            latency_factor = 1.0

        # Weighted combination
        score = (capability * 0.5) + (reliability * 0.3) + (latency_factor * 0.2)
        return score

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}, model={self.default_model})"
