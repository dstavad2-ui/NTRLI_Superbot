"""
NTRLI' AI - Mistral Provider
Handles Mistral AI API interactions
"""

import aiohttp
import time
from typing import Dict, List, Optional
import logging

from .base_provider import BaseAIProvider, AIResponse

logger = logging.getLogger(__name__)


class MistralProvider(BaseAIProvider):
    """Mistral AI API Provider implementation"""

    def __init__(self, api_key: str, base_url: str = "https://api.mistral.ai/v1",
                 default_model: str = "mistral-large-latest", name: str = "Mistral",
                 capabilities: List[str] = None):
        if capabilities is None:
            capabilities = ["chat", "code", "analysis", "function_calling", "embeddings"]

        super().__init__(api_key, base_url, default_model, name, capabilities)

        # Mistral-specific capability scores
        self.metrics.capability_scores = {
            "chat": 0.90,
            "code": 0.88,
            "analysis": 0.87,
            "vision": 0.0,  # Limited support
            "function_calling": 0.85,
            "embeddings": 0.82,
            "moderation": 0.70,
            "fast_inference": 0.80
        }

    async def generate(self, prompt: str, system_prompt: Optional[str] = None,
                       model: Optional[str] = None, **kwargs) -> AIResponse:
        """Generate a single response from Mistral"""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        return await self.chat(messages, model, **kwargs)

    async def chat(self, messages: List[Dict[str, str]],
                   model: Optional[str] = None, **kwargs) -> AIResponse:
        """Multi-turn chat with Mistral"""
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
            logger.error(f"Mistral error: {e}")

        self.update_metrics(response)
        return response

    async def health_check(self) -> bool:
        """Check if Mistral API is available"""
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
            logger.error(f"Mistral health check failed: {e}")
            return False

    async def create_embedding(self, text: str, model: str = "mistral-embed") -> Optional[List[float]]:
        """Create text embedding for NTRLI AI learning"""
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": model,
                    "input": [text]
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
            logger.error(f"Mistral embedding creation failed: {e}")
        return None
