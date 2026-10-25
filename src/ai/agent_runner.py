"""
Agent Orchestrator — End-to-end workflow:
Policy Check → Build Prompt → Call LLM → Run in Sandbox → Return Result
"""
import uuid
from typing import Optional, List, Dict, Any
from .models import LLMClient, ModelType
from .prompt_builder import PromptBuilder
from .sandbox_client import SandboxClient


class AgentRunner:
    """
    High-level agent workflow orchestration
    
    Flow:
        Policy Verify → Build Prompt → Call LLM → Execute in Sandbox → Cleanup → Result
    """

    def __init__(
        self,
        model: ModelType = ModelType.CLAUDE,
        template_dir: str = "prompts/",
    ):
        self.model_type = model
        self.llm = LLMClient(model=model)
        self.builder = PromptBuilder(template_dir=template_dir)
        self.sandbox = SandboxClient()

    async def run(
        self,
        user_task: str,
        tools: Optional[List[str]] = None,
        verify_first: bool = True,
    ) -> Dict[str, Any]:
        """Complete end-to-end execution"""
        session_id = str(uuid.uuid4())
        tools = tools or []

        # Step 1: Policy verification
        policy_ok = await self.builder.verify_policy() if verify_first else True
        if not policy_ok:
            return {
                "session_id": session_id,
                "status": "blocked",
                "error": "POLICY_NOT_VERIFIED",
                "message": "Agent halted: /v1/policy/status not approved by Project Owner"
            }

        # Step 2: Build compliant prompt
        built = await self.builder.build(
            model=self.model_type,
            task=user_task,
            tools=tools,
            session_id=session_id,
            verify_policy=False,
        )

        # Step 3: Call LLM
        llm_resp = await self.llm.chat(
            messages=[{"role": "user", "content": user_task}],
            system_prompt=built["system_prompt"],
        )
        generated_code = llm_resp["content"]

        # Step 4: Execute in sandbox
        try:
            result = await self.sandbox.execute(
                code=generated_code,
                session_id=session_id,
                tools=tools,
                timeout=30,
            )
            status = "completed"
        except Exception as e:
            result = {"error": str(e)}
            status = "failed"
        finally:
            await self.sandbox.destroy(session_id)

        return {
            "session_id": session_id,
            "status": status,
            "model": llm_resp["model"],
            "llm_output": generated_code,
            "sandbox_result": result,
            "policy_verified": policy_ok,
        }

    async def close(self):
        await self.llm.close()
        await self.sandbox.close()
