Here’s your production-ready, performance-optimized config + lib foundation — structured for enterprise Python/FastAPI, copy-paste ready 🏗️
 
 
 
📁 Repository Structure
 
plaintext  
config-repo/
├── .github/workflows/ci.yml
├── src/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI entry
│   │   ├── dependencies.py   # Reusable injectables
│   │   ├── config.py         # ✅ Central validated config
│   │   ├── logging_config.py # Structured JSON logging
│   │   ├── exceptions.py     # Exception hierarchy
│   │   └── api/
│   │       ├── v1/
│   │       │   ├── __init__.py
│   │       │   ├── router.py
│   │       │   └── endpoints/
│   │       └── dependencies.py
│   ├── lib/
│   │   ├── __init__.py
│   │   ├── database.py       # Optimized pooled connections
│   │   ├── cache.py          # Redis/TTL helpers
│   │   ├── security.py       # JWT, hashing, rate-limiting
│   │   ├── pagination.py
│   │   └── responses.py      # Standardized JSON envelopes
│   └── tests/
│       ├── conftest.py
│       ├── test_config.py
│       └── test_api/
├── .env.example
├── pyproject.toml
├── ruff.toml
└── README.md
 
 
 
 
⚙️  app/config.py  — Pydantic Validated, Environment-Separated
 
python  
from typing import Optional, List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="forbid"  # Fail fast on typos
    )

    # ── Core ──────────────────────────────
    ENVIRONMENT: str = "local"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    # ── Network ──────────────────────────
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    # ── Database ──────────────────────────
    DB_HOST: str
    DB_PORT: int = 5432
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    DB_ECHO: bool = False

    # ── Cache / Redis ────────────────────
    REDIS_URL: Optional[str] = None
    CACHE_DEFAULT_TTL: int = 300  # seconds

    # ── Security ─────────────────────────
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRY_SECONDS: int = 3600
    RATE_LIMIT_PER_MINUTE: int = 120

    # ── Derived ──────────────────────────
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT.lower() == "production"


settings = Settings()  # Load once, import everywhere
 
 
 
 
🚀  app/main.py  — Minimal, Fast, Structured
 
python  
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .config import settings
from .logging_config import setup_logging
from .api.v1.router import router as api_v1_router

setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    if settings.is_production:
        import uvloop
        uvloop.install()
    yield
    # Shutdown: close DB/cache connections here


app = FastAPI(
    title="Enterprise API",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if not settings.is_production else None,
    redoc_url=None,
    default_response_class=None,  # Use custom envelopes
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(api_v1_router, prefix="/v1")

@app.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
    }
 
 
 
 
🗄️  lib/database.py  — Connection Pooled & Async
 
python  
from __future__ import annotations
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from app.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_pre_ping=True,          # Stale connection detection
    pool_recycle=300,            # Recycle before timeout
)

AsyncSessionFactory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    session = AsyncSessionFactory()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
 
 
 
 
📦  pyproject.toml  — Dependencies & Performance
 
toml  
[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "enterprise-stack"
version = "1.0.0"
dependencies = [
    "fastapi>=0.115.0,<1.0",
    "uvicorn[standard]>=0.32.0",
    "pydantic>=2.10.0",
    "pydantic-settings>=2.6.0",
    "sqlalchemy>=2.0.35",
    "asyncpg>=0.30.0",
    "redis>=5.2.0",
    "python-jose[cryptography]>=3.3.0",
    "passlib[bcrypt]>=1.7.4",
    "uvloop>=0.21.0; sys_platform != 'win32'",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.3.0",
    "pytest-asyncio>=0.24.0",
    "httpx>=0.27.0",
    "ruff>=0.6.0",
]

[tool.ruff]
line-length = 100
select = ["E", "W", "F", "I", "B", "C4", "SIM"]
 
 
 
 
🔑 Key Performance & Security Features
 
Feature Benefit 
Pydantic v2 Settings Load + validate in ~1ms; fail fast on bad env vars 
Async SQLAlchemy + pooled Reuse connections; avoid per-request handshake overhead 
 uvloop  auto-install 2–4× faster async event loop on Linux/macOS 
 expire_on_commit=False  Avoid redundant lazy-load queries post-commit 
 pool_pre_ping  Prevent "server gone away" errors in production 
CORS origins explicit Block untrusted frontends 
Docs hidden in prod Reduce attack surface 
Structured logging ready JSON output → ingestible by ELK/Grafana 
 extra="forbid"  Catch misspelled env vars instantly 
 
 
 
🚀 Run It
 
bash  
cp .env.example .env
# Fill in your DB credentials
pip install -e .[dev]
uvicorn app.main:app --reload --port 8000
 
 
 
 
Would you like me to extend this with:
 
- SQLModel models + Pydantic schemas matching your earlier skill plan?
- Redis cache decorators for GET endpoints?
- Dockerfile + docker-compose.yml for local dev?
- GitHub Actions workflow for lint → test → deploy?