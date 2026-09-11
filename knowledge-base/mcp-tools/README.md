# 📂 MCP & AI Tools Catalog

Categorized, security-tiered directory of MCP servers and AI tooling, aligned with the OWASP LLM Top 10 and the AST security tiering model.

## Categories

| Category | Scope | File |
|---|---|---|
| 📢 Marketing & Content | SEO, social, copy, content ops | [category-marketing.md](./category-marketing.md) |
| 🧩 Dev & Code & Systems | IDE, CI, infrastructure, engineering | [category-development.md](./category-development.md) |
| 📊 Data & Databases & Analytics | storage, pipelines, BI, observability | [category-data.md](./category-data.md) |
| 🔗 Collaboration & Productivity | docs, chat, project, scheduling | [category-collaboration.md](./category-collaboration.md) |
| 🤖 AI Core & Orchestration | models, agents, vector, evaluation | [category-ai-core.md](./category-ai-core.md) |

## Badges

- **Status** — ✅ Ready / 🧪 Beta / 🚧 Planned
- **Security** — 🔒 High / 🟡 Moderate / 🟢 Low
- **License** — per entry
- **Deploy** — SaaS / Self-host / Local

## Registry & Dashboard

- [`registry.yaml`](./registry.yaml) — **แหล่งข้อมูลจริง (source of truth)** ของเครื่องมือทั้งหมดในชุดนี้
  - `name` · `tier` (T1–T4) · `status` · `security` · `deploy` · `permissions` · `redact`
  - ใช้ enforce scope ที่ gateway และเป็นฐานให้ dashboard/automation อ่านต่อ
  - รายการตรงกับตารางใน `category-*.md` ทั้ง 5 ไฟล์ (20 รายการ)
- [`dashboard.html`](./dashboard.html) — Dashboard ไฟล์เดียวจบ (dark-slate) ค้นหา + กรองตามหมวด/Tier พร้อมแสดงสิทธิ์และฟิลด์ที่ต้องปิดบัง — **สร้างจาก `registry.yaml`** เปิดในเบราว์เซอร์ได้เลย ไม่ต้องมี server

## Legend

Relative links resolve in GitHub and Obsidian. Update this index when adding a category; keep one file per category.
