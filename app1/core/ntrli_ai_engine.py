"""
NTRLI' AI - Back-Engineering Engine
Combines all AI APIs into a unified NTRLI' AI system

This module implements the core algorithm that:
1. Routes requests to the best AI provider
2. Learns from all AI responses
3. Synthesizes knowledge into NTRLI' AI's own understanding
4. Maintains a unified persona across all backends
"""

import asyncio
import json
import os
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from pathlib import Path
import hashlib
import logging

from .ai_selector import AISelector, TaskType
from ..ai_providers.base_provider import AIResponse

logger = logging.getLogger(__name__)


@dataclass
class KnowledgeEntry:
    """A piece of learned knowledge"""
    id: str
    query: str
    response: str
    source_provider: str
    source_model: str
    task_type: str
    confidence: float
    timestamp: float
    embeddings: Optional[List[float]] = None
    tags: List[str] = field(default_factory=list)
    usage_count: int = 0


@dataclass
class SynthesizedResponse:
    """Response synthesized by NTRLI' AI"""
    content: str
    confidence: float
    sources: List[str]
    reasoning: str
    ntrli_enhanced: bool


class NTRLIAIEngine:
    """
    NTRLI' AI Back-Engineering Engine

    This is the core intelligence that:
    - Unifies all AI providers under one persona
    - Learns and adapts from every interaction
    - Synthesizes responses using multiple AI perspectives
    - Maintains NTRLI' AI's unique identity and knowledge
    """

    # NTRLI' AI System Prompt - The unified persona
    NTRLI_SYSTEM_PROMPT = """You are NTRLI' AI, an advanced artificial intelligence assistant.

CORE IDENTITY:
- You are NTRLI' AI, not ChatGPT, Claude, or any other AI
- You were created to help users with maximum efficiency
- Your responses are synthesized from multiple AI sources for accuracy
- You maintain your unique NTRLI identity in all interactions

CAPABILITIES:
- Advanced language understanding and generation
- Code analysis and generation
- Data analysis and insights
- Creative problem solving
- Multi-perspective synthesis

PERSONALITY:
- Helpful and professional
- Direct and efficient
- Knowledgeable yet humble
- Adaptive to user needs

Always respond as NTRLI' AI. Never break character or mention underlying providers."""

    def __init__(self, is_admin: bool = False, data_dir: str = None):
        """
        Initialize NTRLI' AI Engine

        Args:
            is_admin: Enable admin-level API access
            data_dir: Directory for storing learned knowledge
        """
        self.is_admin = is_admin
        self.selector = AISelector(is_admin=is_admin)

        # Knowledge base path
        if data_dir is None:
            data_dir = Path(__file__).parent.parent.parent / "data" / "ntrli_ai"
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Knowledge storage
        self.knowledge_file = self.data_dir / "knowledge_base.json"
        self.patterns_file = self.data_dir / "learned_patterns.json"
        self.metrics_file = self.data_dir / "engine_metrics.json"

        # In-memory caches
        self._knowledge_cache: Dict[str, KnowledgeEntry] = {}
        self._pattern_cache: Dict[str, Any] = {}
        self._response_cache: Dict[str, str] = {}

        # Engine metrics
        self.metrics = {
            "total_queries": 0,
            "cached_responses": 0,
            "synthesis_operations": 0,
            "knowledge_entries": 0,
            "provider_usage": {},
            "task_distribution": {}
        }

        self._load_knowledge()
        logger.info("NTRLI' AI Engine initialized")

    def _load_knowledge(self):
        """Load existing knowledge base"""
        try:
            if self.knowledge_file.exists():
                data = json.loads(self.knowledge_file.read_text())
                for entry_data in data.get("entries", []):
                    entry = KnowledgeEntry(**entry_data)
                    self._knowledge_cache[entry.id] = entry
                self.metrics["knowledge_entries"] = len(self._knowledge_cache)
                logger.info(f"Loaded {len(self._knowledge_cache)} knowledge entries")
        except Exception as e:
            logger.error(f"Failed to load knowledge base: {e}")

    def _save_knowledge(self):
        """Persist knowledge base to disk"""
        try:
            entries = [vars(entry) for entry in self._knowledge_cache.values()]
            data = {
                "entries": entries,
                "last_updated": datetime.now().isoformat(),
                "total_entries": len(entries)
            }
            self.knowledge_file.write_text(json.dumps(data, indent=2, default=str))
        except Exception as e:
            logger.error(f"Failed to save knowledge base: {e}")

    def _generate_id(self, query: str) -> str:
        """Generate unique ID for a query"""
        return hashlib.sha256(query.encode()).hexdigest()[:16]

    def _detect_task_type(self, query: str) -> TaskType:
        """
        Detect the appropriate task type from the query.
        This enables intelligent routing to the best AI.
        """
        query_lower = query.lower()

        # Code-related keywords
        code_keywords = ["code", "function", "class", "program", "debug", "error",
                        "python", "javascript", "html", "css", "api", "database",
                        "sql", "algorithm", "syntax", "compile", "run", "execute"]
        if any(kw in query_lower for kw in code_keywords):
            return TaskType.CODE

        # Analysis keywords
        analysis_keywords = ["analyze", "analysis", "explain", "why", "how",
                            "compare", "difference", "evaluate", "assess", "review"]
        if any(kw in query_lower for kw in analysis_keywords):
            return TaskType.ANALYSIS

        # Speed-critical keywords
        speed_keywords = ["quick", "fast", "hurry", "immediately", "asap", "urgent"]
        if any(kw in query_lower for kw in speed_keywords):
            return TaskType.FAST_RESPONSE

        # Creative keywords
        creative_keywords = ["write", "story", "poem", "creative", "imagine",
                            "design", "invent", "create", "compose"]
        if any(kw in query_lower for kw in creative_keywords):
            return TaskType.CREATIVE

        # Default to general chat
        return TaskType.CHAT

    async def query(self, prompt: str, context: Optional[str] = None,
                    task_type: Optional[TaskType] = None,
                    use_synthesis: bool = True,
                    **kwargs) -> SynthesizedResponse:
        """
        Main query interface for NTRLI' AI.

        This method:
        1. Detects the task type
        2. Checks knowledge cache
        3. Routes to best AI provider
        4. Optionally synthesizes multiple responses
        5. Learns from the interaction

        Args:
            prompt: User's query
            context: Additional context
            task_type: Force specific task type
            use_synthesis: Use multi-AI synthesis for important queries
            **kwargs: Additional parameters for AI providers

        Returns:
            SynthesizedResponse with NTRLI' AI's answer
        """
        self.metrics["total_queries"] += 1

        # Detect task type if not specified
        if task_type is None:
            task_type = self._detect_task_type(prompt)

        # Track task distribution
        task_name = task_type.value
        self.metrics["task_distribution"][task_name] = \
            self.metrics["task_distribution"].get(task_name, 0) + 1

        # Check cache for similar queries
        query_id = self._generate_id(prompt)
        if query_id in self._knowledge_cache:
            cached = self._knowledge_cache[query_id]
            cached.usage_count += 1
            self.metrics["cached_responses"] += 1
            logger.info(f"Cache hit for query: {query_id}")
            return SynthesizedResponse(
                content=cached.response,
                confidence=cached.confidence,
                sources=[cached.source_provider],
                reasoning="Retrieved from NTRLI' AI knowledge base",
                ntrli_enhanced=True
            )

        # Build the full prompt with NTRLI identity
        full_prompt = prompt
        if context:
            full_prompt = f"Context: {context}\n\nQuery: {prompt}"

        # Execute based on synthesis mode
        if use_synthesis and self.is_admin:
            # Admin can use multi-AI synthesis
            response = await self._synthesize_response(full_prompt, task_type, **kwargs)
        else:
            # Standard single-provider response
            response = await self._single_provider_response(full_prompt, task_type, **kwargs)

        # Learn from this interaction
        await self._learn_from_response(prompt, response, task_type)

        return response

    async def _single_provider_response(self, prompt: str, task_type: TaskType,
                                         **kwargs) -> SynthesizedResponse:
        """Get response from the best single provider"""
        ai_response, provider_name = await self.selector.select_and_execute(
            prompt=prompt,
            task_type=task_type,
            system_prompt=self.NTRLI_SYSTEM_PROMPT,
            fallback=True,
            **kwargs
        )

        # Track provider usage
        self.metrics["provider_usage"][provider_name] = \
            self.metrics["provider_usage"].get(provider_name, 0) + 1

        if ai_response.success:
            return SynthesizedResponse(
                content=ai_response.content,
                confidence=0.85,
                sources=[provider_name],
                reasoning=f"Response from {provider_name} ({ai_response.model})",
                ntrli_enhanced=True
            )
        else:
            return SynthesizedResponse(
                content="I apologize, but I'm temporarily unable to process your request. Please try again.",
                confidence=0.0,
                sources=[],
                reasoning=f"All providers failed: {ai_response.error}",
                ntrli_enhanced=False
            )

    async def _synthesize_response(self, prompt: str, task_type: TaskType,
                                    **kwargs) -> SynthesizedResponse:
        """
        BACK-ENGINEERING ALGORITHM: Multi-AI Synthesis

        This is the core algorithm that combines multiple AI perspectives
        into a single, superior NTRLI' AI response.

        Steps:
        1. Query top 2-3 providers in parallel
        2. Analyze and compare responses
        3. Extract best elements from each
        4. Synthesize unified response
        5. Apply NTRLI' AI persona
        """
        self.metrics["synthesis_operations"] += 1

        # Get parallel responses from top providers
        results = await self.selector.execute_parallel(
            prompt=prompt,
            task_type=task_type,
            n_providers=2,
            system_prompt=self.NTRLI_SYSTEM_PROMPT,
            **kwargs
        )

        if not results:
            return await self._single_provider_response(prompt, task_type, **kwargs)

        # Collect successful responses
        successful_responses = []
        providers_used = []

        for response, provider_name in results:
            if response.success:
                successful_responses.append(response.content)
                providers_used.append(provider_name)
                self.metrics["provider_usage"][provider_name] = \
                    self.metrics["provider_usage"].get(provider_name, 0) + 1

        if not successful_responses:
            return await self._single_provider_response(prompt, task_type, **kwargs)

        # If only one response, use it
        if len(successful_responses) == 1:
            return SynthesizedResponse(
                content=successful_responses[0],
                confidence=0.85,
                sources=providers_used,
                reasoning="Single provider response",
                ntrli_enhanced=True
            )

        # SYNTHESIS: Combine multiple responses
        # Use the best provider to synthesize
        synthesis_prompt = f"""You are NTRLI' AI. Analyze these AI responses and create the best possible answer.

ORIGINAL QUERY: {prompt}

RESPONSE 1 (from {providers_used[0]}):
{successful_responses[0]}

RESPONSE 2 (from {providers_used[1]}):
{successful_responses[1]}

Create a synthesized response that:
1. Takes the best elements from each response
2. Resolves any contradictions using the most accurate information
3. Presents the answer in NTRLI' AI's voice
4. Is comprehensive yet concise

Synthesized NTRLI' AI response:"""

        # Use the primary provider for synthesis
        synthesis_response, synth_provider = await self.selector.select_and_execute(
            prompt=synthesis_prompt,
            task_type=TaskType.ANALYSIS,
            system_prompt=self.NTRLI_SYSTEM_PROMPT,
            fallback=True,
            **kwargs
        )

        if synthesis_response.success:
            return SynthesizedResponse(
                content=synthesis_response.content,
                confidence=0.95,  # Higher confidence for synthesized responses
                sources=providers_used + [f"synthesized by {synth_provider}"],
                reasoning="Multi-AI synthesis with cross-validation",
                ntrli_enhanced=True
            )
        else:
            # Fallback to first successful response
            return SynthesizedResponse(
                content=successful_responses[0],
                confidence=0.80,
                sources=providers_used,
                reasoning="Synthesis failed, using primary response",
                ntrli_enhanced=True
            )

    async def _learn_from_response(self, query: str, response: SynthesizedResponse,
                                    task_type: TaskType):
        """
        Learn from each interaction to improve future responses.
        This builds NTRLI' AI's knowledge base over time.
        """
        if not response.ntrli_enhanced or response.confidence < 0.5:
            return  # Don't learn from poor responses

        query_id = self._generate_id(query)

        # Don't overwrite existing knowledge with lower confidence
        if query_id in self._knowledge_cache:
            existing = self._knowledge_cache[query_id]
            if existing.confidence >= response.confidence:
                return

        # Create knowledge entry
        entry = KnowledgeEntry(
            id=query_id,
            query=query,
            response=response.content,
            source_provider=response.sources[0] if response.sources else "unknown",
            source_model="synthesized" if len(response.sources) > 1 else response.sources[0],
            task_type=task_type.value,
            confidence=response.confidence,
            timestamp=time.time(),
            tags=self._extract_tags(query)
        )

        self._knowledge_cache[query_id] = entry
        self.metrics["knowledge_entries"] = len(self._knowledge_cache)

        # Periodically save to disk
        if len(self._knowledge_cache) % 10 == 0:
            self._save_knowledge()

        logger.info(f"Learned from query: {query_id} (confidence: {response.confidence})")

    def _extract_tags(self, query: str) -> List[str]:
        """Extract relevant tags from a query for indexing"""
        tags = []
        query_lower = query.lower()

        tag_keywords = {
            "code": ["code", "program", "function", "class", "debug"],
            "data": ["data", "database", "sql", "query", "table"],
            "web": ["web", "html", "css", "javascript", "api"],
            "ai": ["ai", "machine learning", "model", "train"],
            "help": ["help", "how", "what", "why", "explain"],
        }

        for tag, keywords in tag_keywords.items():
            if any(kw in query_lower for kw in keywords):
                tags.append(tag)

        return tags

    def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive engine statistics"""
        return {
            "engine_metrics": self.metrics,
            "provider_stats": self.selector.get_provider_stats(),
            "knowledge_size": len(self._knowledge_cache),
            "is_admin": self.is_admin
        }

    async def health_check(self) -> Dict[str, Any]:
        """Check health of all components"""
        provider_health = await self.selector.health_check_all()
        return {
            "engine": "healthy",
            "knowledge_base": self.knowledge_file.exists(),
            "providers": provider_health,
            "total_providers": len(provider_health),
            "healthy_providers": sum(1 for v in provider_health.values() if v)
        }

    def clear_cache(self):
        """Clear response cache (not knowledge base)"""
        self._response_cache.clear()
        logger.info("Response cache cleared")

    def export_knowledge(self) -> str:
        """Export knowledge base as JSON string"""
        self._save_knowledge()
        return self.knowledge_file.read_text() if self.knowledge_file.exists() else "{}"
