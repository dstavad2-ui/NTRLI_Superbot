"""
NTRLI' AI - Groq Provider
Handles Groq API interactions - optimized for speed
"""

import aiohttp
import time
from typing import Dict, List, Optional
import logging

from .base_provider import BaseAIProvider, AIResponse

logger = logging.getLogger(__name__)


class GroqProvider(BaseAIProvider):
    """Groq API Provider implementation - fast inference"""

    def __init__(self, api_key: str, base_url: str = "https://api.groq.com/openai/v1",
                 default_model: str = "llama-3.1-70b-versatile", name: str = "Groq",
                 capabilities: List[str] = None):
        if capabilities is None:
            capabilities = ["chat", "code", "analysis", "fast_inference"]

        super().__init__(api_key, base_url, default_model, name, capabilities)

        # Groq-specific capability scores (optimized for speed)
        self.metrics.capability_scores = {
            "chat": 0.88,
            "code": 0.85,
            "analysis": 0.82,
            "vision": 0.0,  # Not supported
            "function_calling": 0.75,
            "embeddings": 0.0,  # Not supported
            "moderation": 0.0,
            "fast_inference": 0.99  # Groq's main strength
        }

    async def generate(self, prompt: str, system_prompt: Optional[str] = None,
                       model: Optional[str] = None, **kwargs) -> AIResponse:
        """Generate a single response from Groq"""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        return await self.chat(messages, model, **kwargs)

    async def chat(self, messages: List[Dict[str, str]],
                   model: Optional[str] = None, **kwargs) -> AIResponse:
        """Multi-turn chat with Groq - ultra fast"""
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
                    timeout=aiohttp.ClientTimeout(total=30)  # Faster timeout for Groq
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
                            metadata={
                                "finish_reason": data["choices"][0].get("finish_reason"),
                                "groq_id": data.get("id")
                            }
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
            logger.error(f"Groq error: {e}")

        self.update_metrics(response)
        return response

    async def health_check(self) -> bool:
        """Check if Groq API is available"""
        try:
            async with aiohttp.ClientSession() as session:
                headers = {"Authorization": f"Bearer {self.api_key}"}
                async with session.get(
                    f"{self.base_url}/models",
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=5)  # Quick check
                ) as resp:
                    return resp.status == 200
        except Exception as e:
            logger.error(f"Groq health check failed: {e}")
            return False
