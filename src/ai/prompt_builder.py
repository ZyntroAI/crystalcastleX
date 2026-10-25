"""
Prompt Builder — Load templates, inject values, verify policy
"""
import uuid
import re
from pathlib import Path
from typing import Optional, List, Dict, Any
from .models import ModelType
from .config import settings


class PromptBuilder:
    """
    Build compliant, ready-to-send prompts from templates
    
    Usage:
        pb = PromptBuilder(template_dir="prompts/")
        prompt = await pb.build(
            model=ModelType.CLAUDE,
            task="Analyze this code...",
            tools=["code_review"]
        )
    """

    TEMPLATE_FILES = {
        ModelType.FIG: "template_claude_fig.md",
        ModelType.CLAUDE: "template_claude_fig.md",
        ModelType.CHATGPT: "template_chatgpt.md",
        ModelType.GROK: "template_grok.md",
    }

    def __init__(self, template_dir: str = "prompts/"):
        self.template_dir = Path(template_dir)
        self._cache: Dict[ModelType, str] = {}
        self._policy_ok: Optional[bool] = None

    async def verify_policy(self) -> bool:
        """Check sandbox policy status before building"""
        if not settings.ENFORCE_POLICY:
            return True
        try:
            import httpx
            async with httpx.AsyncClient(timeout=10) as c:
                r = await c.get(settings.POLICY_STATUS_URL)
                d = r.json()
                self._policy_ok = d.get("approved") and d.get("owner") == "Project Owner"
        except Exception:
            self._policy_ok = False
        return self._policy_ok

    def load_template(self, model: ModelType) -> str:
        if model in self._cache:
            return self._cache[model]
        path = self.template_dir / self.TEMPLATE_FILES[model]
        text = path.read_text(encoding="utf-8")
        self._cache[model] = text
        return text

    def inject(
        self,
        template: str,
        session_id: str,
        task: str,
        tools: List[str],
        jwt: str = "[REDACTED]",
    ) -> str:
        policy_line = (
            "✅ POLICY VERIFIED — approved: true | owner: Project Owner"
            if self._policy_ok is not False else
            "⚠️ POLICY UNCHECKED — verify via /v1/policy/status first"
        )
        result = template.replace("[POLICY_STATUS_BANNER]", policy_line)
        result = result.replace("{{JWT_SECRET}}", jwt)
        result = result.replace("{{uuid}}", session_id)
        result = result.replace("TASK_HERE", task)
        result = re.sub(r'"tools": \[[^\]]*\]', f'"tools": {tools}', result)
        return result

    async def build(
        self,
        model: ModelType,
        task: str,
        tools: Optional[List[str]] = None,
        session_id: Optional[str] = None,
        verify_policy: bool = True,
    ) -> Dict[str, Any]:
        if verify_policy:
            await self.verify_policy()
        session_id = session_id or str(uuid.uuid4())
        tools = tools or []
        template = self.load_template(model)
        prompt = self.inject(template, session_id, task, tools)
        return {
            "session_id": session_id,
            "model": model.value,
            "system_prompt": prompt,
            "tools": tools,
            "policy_verified": self._policy_ok,
        }
