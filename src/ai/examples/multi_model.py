"""
Example 2: Compare Output Across All Models
"""
import asyncio
from src.ai import LLMClient, ModelType

async def main():
    task = "Explain what an isolated sandbox environment is in one sentence."

    for model in [ModelType.CLAUDE, ModelType.CHATGPT, ModelType.GROK]:
        ai = LLMClient(model=model)
        try:
            resp = await ai.chat(task)
            print(f"\n🤖 {model.value.upper()}:\n{resp['content']}")
        except Exception as e:
            print(f"\n⚠️ {model.value.upper()}: {e}")
        finally:
            await ai.close()

asyncio.run(main())
