"""
Sandbox API Client — Execute tasks in isolated environment
"""
import httpx
from typing import Optional, Dict, Any
from .config import settings


class SandboxClient:
    """
    Interact with ZyntroAI Sandbox API
    
    Usage:
        async with SandboxClient() as sb:
            result = await sb.execute("print('Hello')", timeout=30)
    """

    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        self.base_url = (base_url or settings.SANDBOX_API_URL).rstrip("/")
        self.api_key = api_key or settings.SANDBOX_API_KEY
        self._client = httpx.AsyncClient(timeout=60)

    @property
    def headers(self) -> Dict[str, str]:
        h = {"Content-Type": "application/json"}
        if self.api_key:
            h["Authorization"] = f"Bearer {self.api_key}"
        return h

    async def policy_status(self) -> Dict[str, Any]:
        """Check system authorization"""
        r = await self._client.get(f"{self.base_url}/v1/policy/status")
        r.raise_for_status()
        return r.json()

    async def execute(
        self,
        code: str,
        session_id: Optional[str] = None,
        tools: Optional[list] = None,
        timeout: int = 30,
    ) -> Dict[str, Any]:
        """Run code in sandbox — auto-destroys on completion"""
        payload = {
            "session_id": session_id,
            "prompt": code,
            "tools": tools or [],
            "timeout": timeout,
        }
        r = await self._client.post(
            f"{self.base_url}/v1/agent/execute",
            headers=self.headers,
            json=payload
        )
        r.raise_for_status()
        return r.json()

    async def destroy(self, session_id: str) -> bool:
        """Manually terminate sandbox"""
        r = await self._client.delete(
            f"{self.base_url}/v1/sandbox/{session_id}",
            headers=self.headers
        )
        return r.json().get("destroyed", False)

    async def close(self):
        await self._client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.close()
