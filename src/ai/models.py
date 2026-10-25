"""
Multi-Model LLM Client — Unified interface for FIG/Claude/GPT/Grok
"""
import os
import httpx
from enum import Enum
from typing import Optional, Dict, Any, List
from .config import settings


class ModelType(str, Enum):
    FIG = "fig"
    CLAUDE = "claude"
    CHATGPT = "chatgpt"
    GROK = "grok"


class LLMClient:
    """
    Universal LLM Client
    
    Usage:
        ai = LLMClient(model=ModelType.CLAUDE)
        response = await ai.chat("Hello world")
    """

    def __init__(
        self,
        model: ModelType = ModelType.CLAUDE,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ):
        self.model_type = model
        self.api_key = api_key or self._get_default_key()
        self.base_url = base_url or self._get_default_url()
        self._client = httpx.AsyncClient(timeout=settings.DEFAULT_TIMEOUT)

    def _get_default_key(self) -> str:
        key_map = {
            ModelType.FIG: settings.FIG_API_KEY,
            ModelType.CLAUDE: settings.ANTHROPIC_API_KEY,
            ModelType.CHATGPT: settings.OPENAI_API_KEY,
            ModelType.GROK: settings.GROK_API_KEY,
        }
        return key_map.get(self.model_type) or ""

    def _get_default_url(self) -> str:
        url_map = {
            ModelType.FIG: "https://api.fig.ai/v1",
            ModelType.CLAUDE: "https://api.anthropic.com/v1",
            ModelType.CHATGPT: "https://api.openai.com/v1",
            ModelType.GROK: "https://api.x.ai/v1",
        }
        return url_map.get(self.model_type, "")

    async def chat(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        temperature: float = settings.DEFAULT_TEMPERATURE,
        max_tokens: int = settings.DEFAULT_MAX_TOKENS,
        **kwargs
    ) -> Dict[str, Any]:
        """Send chat completion request"""
        
        if isinstance(messages, str):
            messages = [{"role": "user", "content": messages}]

        if system_prompt:
            messages.insert(0, {"role": "system", "content": system_prompt})

        headers = self._get_headers()
        payload = self._build_payload(messages, temperature, max_tokens, **kwargs)

        resp = await self._client.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload
        )
        resp.raise_for_status()
        return self._parse_response(resp.json())

    def _get_headers(self) -> Dict[str, str]:
        common = {"Content-Type": "application/json"}
        if self.model_type == ModelType.CLAUDE:
            return {**common, "x-api-key": self.api_key, "anthropic-version": "2023-06-01"}
        return {**common, "Authorization": f"Bearer {self.api_key}"}

    def _build_payload(self, messages, temp, max_tok, **kw) -> Dict[str, Any]:
        model_name = {
            ModelType.FIG: "fig-pro",
            ModelType.CLAUDE: "claude-3-sonnet-20240229",
            ModelType.CHATGPT: "gpt-4o",
            ModelType.GROK: "grok-2-latest",
        }[self.model_type]

        payload = {
            "model": model_name,
            "messages": messages,
            "temperature": temp,
            "max_tokens": max_tok,
            **kw
        }
        if self.model_type == ModelType.CLAUDE:
            payload["system"] = messages.pop(0)["content"] if messages[0]["role"] == "system" else None
        return payload

    def _parse_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "content": data["choices"][0]["message"]["content"],
            "model": data.get("model", ""),
            "usage": data.get("usage", {}),
            "finish_reason": data["choices"][0].get("finish_reason")
        }

    async def close(self):
        await self._client.aclose()
