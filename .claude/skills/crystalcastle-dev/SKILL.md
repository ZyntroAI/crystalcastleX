---
name: crystalcastle-dev
description: >
  CrystalCastle X (ZyntroAI/crystalcastleX) project skill — AI video/content pipeline
  (Next.js frontend + Python FastAPI backend, multi-LLM providers: OpenAI/Gemini/Mistral,
  Docker deploy, sandbox preview per PR, AI auto-repair loop, 40+ GitHub Actions workflows).
  ACTIVATE when: editing files under src/ai/, src/core/, app/, .github/workflows/,
  docker-compose*.yml, Dockerfile, or when asked about CrystalCastle, ZyntroAI,
  AI provider failover, sandbox preview deploy, auto-repair, workflow consolidation,
  or conventional commits in this repo. DO NOT activate for generic programming or
  other repos. Manual invocation: /crystalcastle <subcommand>.
---

# CrystalCastle X — Developer Skill

Progressive disclosure: load only the relevant reference file from `references/`
based on the task. Do not load all references at once.

## When to use / not use

**Use** when working in this repo (architecture, providers, workflows, deploy, repair, conventions).
**Do NOT use** for generic coding questions, other repos, or pure Claude API integration
(use the built-in `claude-api` skill for that).

## Project at a glance

- **Monorepo (pnpm, Node 22)**: Next.js frontend (`src/`), Python FastAPI backend (`app/`)
- **AI layer** (`src/ai/`): `prompts/` (prompt templates), `pipelines/` (orchestration),
  `providers/` (OpenAI / Gemini / Mistral abstraction + failover)
- **Core** (`src/core/`): `video/`, `render/`, `captions/`
- **Deploy**: Docker → GHCR → sandbox host (preview per PR) + Vercel (production, `main`)
- **CI/CD**: 40+ workflows in `.github/workflows/` — many are DUPLICATED; consolidate before adding new ones
- **Auto-repair**: failed workflow → collect logs → `scripts/ai_repair.py` (LLM patch) → PR → rerun (max 3 attempts, then rollback)

## Hard rules (never violate)

1. **Never call an LLM SDK directly** — always go through `src/ai/providers/` abstraction (handles failover + key rotation + cost tracking)
2. **Never add a new workflow file without checking for duplicates** — see `references/workflows.md` for canonical list
3. **Actions must be SHA-pinned** (not `@vN`) + `permissions:` least-privilege — enforced by SECURITY.md
4. **Secrets**: never log API keys; keys are in GitHub Environment `sandbox`/`production`, never in `.env` committed
5. **Commits**: Conventional Commits (`feat:`, `fix:`, `chore:`, `ci:`) — `commit-lint.yml` enforces
6. **Preview deploys** are ephemeral per PR — always clean up on PR close

## Subcommands (manual invocation)

| Command | Action | Reference loaded |
|---|---|---|
| `/crystalcastle onboard` | Interview-style walkthrough of repo architecture + how to run locally | architecture.md |
| `/crystalcastle add-workflow <purpose>` | Scaffold a new workflow, checking for duplicates + SHA-pinning | workflows.md |
| `/crystalcastle repair <run-id>` | Run the auto-repair flow: fetch logs → analyze → patch → PR | repair-loop.md |
| `/crystalcastle provider <task>` | Add/modify an AI provider with failover + budget guard | providers.md |
| `/crystalcastle deploy-preview` | Wire up PR preview deploy + cleanup + comment URL | workflows.md |
| `/crystalcastle conventions` | Print commit/label/env/secret naming standards | conventions.md |

## Quick reference (always available)

- **Env vars**: `OPENAI_API_KEY`, `GEMINI_API_KEY`, `MISTRAL_API_KEY`, `REDIS_URL`, `DB_*`, `SANDBOX_HOST`, `VERCEL_TOKEN`
- **Test**: `pnpm test` (unit), `pnpm exec playwright test` (e2e against preview)
- **Build**: `pnpm build` (Next.js); `docker build -t api .` (backend)
- **Health endpoint**: `GET /health` (used by every deploy + health-check workflow)
- **Default ports**: frontend 3000, api 8000, postgres 5432, redis 6379

## If something is unclear

- Check `references/` first
- If still ambiguous, ask the user which area applies (frontend / backend / AI providers / workflows / deploy)
  before making changes — do not guess across layers.
