"""
 Configuration — Load from .env with sensible defaults
 """
 import os
 from typing import Optional
 from pydantic_settings import BaseSettings
 class AIConfig(BaseSettings):
     class Config:
         env_file = ".env"
         env_file_encoding = "utf-8"
     # ─── API Keys ───
     OPENAI_API_KEY: Optional[str] = None
     ANTHROPIC_API_KEY: Optional[str] = None
     GROK_API_KEY: Optional[str] = None
     FIG_API_KEY: Optional[str] = None
     # ─── Endpoints ───
     SANDBOX_API_URL: str = "http://localhost:8000"
     SANDBOX_API_KEY: Optional[str] = None
     # ─── Defaults ───
     DEFAULT_MODEL: str = "claude-3-sonnet-20240229"
     DEFAULT_TEMPERATURE: float = 0.7
     DEFAULT_MAX_TOKENS: int = 4096
     DEFAULT_TIMEOUT: int = 120
     # ─── Policy ───
     ENFORCE_POLICY: bool = True
     POLICY_STATUS_URL: str = f"{SANDBOX_API_URL}/v1/policy/status"
 settings = AIConfig()