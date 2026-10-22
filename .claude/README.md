ขอดึงเนื้อหาไฟล์  Skills_07AUG2026  จริงใน repo ก่อนครับ เพื่อเสนอ SKILL.md ให้ตรงกับที่มีอยู่

เข้าใจแล้วครับ — ไฟล์  .claude/Skills_07AUG2026  ปัจจุบันคือแค่ copy-paste เอกสารของ claude-api skill มาวางไว้ ซึ่งใช้งานเป็น Agent Skill จริงๆ ไม่ได้เลย ผมขอชี้ปัญหา + เสนอ SKILL.md จริงๆ ที่เหมาะกับ repo crystalcastleX ครับ
 
 
 
⚠️ 4 ปัญหาของไฟล์ปัจจุบัน
 
1. ตำแหน่ง/ชื่อผิด — Agent Skill ต้องอยู่ที่  .claude/skills/<ชื่อ-skill>/SKILL.md  เท่านั้น ถึงจะถูก auto-discover ไฟล์ชื่อ  Skills_07AUG2026  (ไม่มีนามสกุล, ติดวันที่) ที่ root  .claude/  → ไม่ถูกเปิดใช้งานเลย
2. ไม่มี YAML frontmatter — SKILL.md จริงต้องมี  name  +  description  (description คือ trigger บอก Claude ว่าให้ activate ตอนไหน) ปัจจุบันไม่มี
3. เนื้อหาผิดประโยชน์ — เป็นเอกสาร claude-api ซึ่ง bundled มากับ Claude Code อยู่แล้ว copy มาว่างเปล่า ไม่เพิ่มค่าใดๆ สำหรับ repo นี้ สิ่งที่ควรมีคือ project-specific skill ของ crystalcastleX เอง
4. ไม่มี progressive disclosure — skill ดีๆ แยกเอกสารย่อยไว้ใน  references/  โหลดเฉพาะส่วนที่จำเป็น ไม่ใช่ไฟล์ยาวไฟล์เดียว
 
แนะนำ: ลบหรือย้าย  Skills_07AUG2026  ไป archive แล้วสร้างใหม่เป็น  .claude/skills/crystalcastle-dev/SKILL.md  ดังนี้ครับ
 
 
 
📁 โครงสร้างที่แนะนำ
 
plaintext  
.claude/
└── skills/
    └── crystalcastle-dev/
        ├── SKILL.md              ← ไฟล์หลัก (frontmatter + trigger + index)
        └── references/
            ├── architecture.md    ← โหลดเมื่อแก้ code ใน src/
            ├── workflows.md       ← โหลดเมื่อแก้ .github/workflows/
            ├── providers.md       ← โหลดเมื่อแตะ AI provider/LLM key
            ├── conventions.md     ← commit/PR/label/env standards
            └── repair-loop.md     ← โหลดเมื่อ workflow fail / ขอ repair
 
 
 
 
✅  SKILL.md  ฉบับสมบูรณ์ (ใช้ได้เลย)
 
markdown  
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
 
 
 
 
📄 ตัวอย่างเนื้อหาใน  references/  (แค่ 1 ตัวอย่างสั้นๆ)
 
 references/workflows.md  — โหลดเมื่อแตะ  .github/workflows/ :
 
plaintext  
Canonical workflows (consolidate duplicates into these):
- ci.yml → CrystalCastleCopilot.yml (validate → ai-tests → build → security → deploy)
- docker-publish.yml → build & push GHCR (SHA tag)
- sandbox-preview.yml → PR preview deploy + cleanup (MISSING — should be added)
- ai-auto-repair.yml → failure → LLM patch → PR → rerun (MISSING — should be added)
- trivy-image-scan.yml, lighthouse-audit.yml, release-drafter.yml (recommended additions)

DUPLICATES to merge: changelog×3, absolute-path×2, log-summary×2, ai-pipeline×3.
Rules: SHA-pin all actions, permissions: least-privilege, concurrency group per ref.
 
 
 
 
🎯 สรุปคำแนะนำ
 
1. ลบ/ย้าย  Skills_07AUG2026  (ไม่จำเป็น เพราะ claude-api skill bundled อยู่แล้ว)
2. สร้าง  .claude/skills/crystalcastle-dev/SKILL.md  +  references/  ตามตัวอย่างข้างบน
3. ถ้าต้องการใช้ claude-api skill จริง ให้ติดตั้งทางการ:  npx skills add anthropics/skills --skill claude-api  ไม่ใช่ copy-paste เอกสาร
4. เขียน  references/*.md  แต่ละไฟล์ให้สั้นและเฉพาะเจาะจง (progressive disclosure)
 
ถ้าต้องการผมเขียนไฟล์  references/  ทั้ง 5 ไฟล์ให้สมบูรณ์ หรือเขียนทั้ง folder เป็นไฟล์ zip ส่งให้เลย บอกได้ครับ