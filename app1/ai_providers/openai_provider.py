"""
NTRLI' AI - OpenAI Provider
Handles OpenAI API interactions
"""

import aiohttp
import time
import json
from typing import Dict, List, Optional
import logging

from .base_provider import BaseAIProvider, AIResponse

logger = logging.getLogger(__name__)


class OpenAIProvider(BaseAIProvider):
    """OpenAI API Provider implementation"""

    def __init__(self, api_key: str, base_url: str = "https://api.openai.com/v1",
                 default_model: str = "gpt-4o-mini", name: str = "OpenAI",
                 capabilities: List[str] = None):
        if capabilities is None:
            capabilities = ["chat", "code", "analysis", "vision", "function_calling", "embeddings"]

        super().__init__(api_key, base_url, default_model, name, capabilities)

        # OpenAI-specific capability scores (high quality)
        self.metrics.capability_scores = {
            "chat": 0.95,
            "code": 0.92,
            "analysis": 0.93,
            "vision": 0.90,
            "function_calling": 0.95,
            "embeddings": 0.90,
            "moderation": 0.85,
            "fast_inference": 0.70
        }

    async def generate(self, prompt: str, system_prompt: Optional[str] = None,
                       model: Optional[str] = None, **kwargs) -> AIResponse:
        """Generate a single response from OpenAI"""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        return await self.chat(messages, model, **kwargs)

    async def chat(self, messages: List[Dict[str, str]],
                   model: Optional[str] = None, **kwargs) -> AIResponse:
        """Multi-turn chat with OpenAI"""
        model = model or self.default_model
        start_time = time.time()

        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }

                payload = {
                    "model": model,
                    "messages": messages,
                    "max_tokens": kwargs.get("max_tokens", 2048),
                    "temperature": kwargs.get("temperature", 0.7)
                }

                async with session.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as resp:
                    latency_ms = (time.time() - start_time) * 1000

                    if resp.status == 200:
                        data = await resp.json()
                        content = data["choices"][0]["message"]["content"]
                        tokens = data.get("usage", {}).get("total_tokens", 0)

                        response = AIResponse(
                            content=content,
                            provider=self.name,
                            model=model,
                            tokens_used=tokens,
                            latency_ms=latency_ms,
                            success=True,
                            metadata={"finish_reason": data["choices"][0].get("finish_reason")}
                        )
                    else:
                        error_text = await resp.text()
                        response = AIResponse(
                            content="",
                            provider=self.name,
                            model=model,
                            tokens_used=0,
                            latency_ms=latency_ms,
                            success=False,
                            error=f"HTTP {resp.status}: {error_text}"
                        )

        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            response = AIResponse(
                content="",
                provider=self.name,
                model=model,
                tokens_used=0,
                latency_ms=latency_ms,
                success=False,
                error=str(e)
            )
            logger.error(f"OpenAI error: {e}")

        self.update_metrics(response)
        return response

    async def health_check(self) -> bool:
        """Check if OpenAI API is available"""
        try:
            async with aiohttp.ClientSession() as session:
                headers = {"Authorization": f"Bearer {self.api_key}"}
                async with session.get(
                    f"{self.base_url}/models",
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as resp:
                    return resp.status == 200
        except Exception as e:
            logger.error(f"OpenAI health check failed: {e}")
            return False

    async def create_embedding(self, text: str, model: str = "text-embedding-3-small") -> Optional[List[float]]:
        """Create text embedding for NTRLI AI learning"""
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": model,
                    "input": text
                }
                async with session.post(
                    f"{self.base_url}/embeddings",
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data["data"][0]["embedding"]
        except Exception as e:
            logger.error(f"Embedding creation failed: {e}")
        return None
