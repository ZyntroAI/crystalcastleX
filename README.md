# 🔮 Crystal Castle X

> Runner AI powered by Zyntro-Media-AI

[![CI](https://github.com/ZyntroAI/crystalcastleX/actions/workflows/ci.yml/badge.svg)](https://github.com/ZyntroAI/crystalcastleX/actions/workflows/ci.yml)
[![CrystalCastle AI Pipeline](https://github.com/ZyntroAI/crystalcastleX/actions/workflows/CrystalCastleCopilot.yml/badge.svg)](https://github.com/ZyntroAI/crystalcastleX/actions/workflows/CrystalCastleCopilot.yml)
[![Update README from docs/knowledge](https://github.com/ZyntroAI/crystalcastleX/actions/workflows/update-readme.yml/badge.svg?branch=main)](https://github.com/ZyntroAI/crystalcastleX/actions/workflows/update-readme.yml)
[![License](https://img.shields.io/badge/license-MIT-1f6feb?style=flat-square)](LICENSE)
[![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat-square&logo=next.js&logoColor=white)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)](https://www.docker.com/)

[![GitHub Stars](https://img.shields.io/github/stars/ZyntroAI/crystalcastleX?style=flat-square)](https://github.com/ZyntroAI/crystalcastleX/stargazers)
[![GitHub Issues](https://img.shields.io/github/issues/ZyntroAI/crystalcastleX?style=flat-square)](https://github.com/ZyntroAI/crystalcastleX/issues)
[![Last Commit](https://img.shields.io/github/last-commit/ZyntroAI/crystalcastleX?style=flat-square)](https://github.com/ZyntroAI/crystalcastleX/commits/main)

## ✨ ภาพรวม

Crystal Castle X คือระบบ AI Video Studio ที่รวม pipeline การสร้างวิดีโอ
พร้อม abstraction ของ AI provider หลายเจ้า (OpenAI, Gemini, Groq, FAL, RunwayML ฯลฯ)

## 🚀 เริ่มต้นใช้งาน (Getting Started)

### สิ่งที่ต้องมี

| เครื่องมือ | เวอร์ชัน |
| --- | --- |
| Node.js | 22 (ดู [`.nvmrc`](.nvmrc)) |
| PNPM | 9 |
| Python | 3.11+ (สำหรับ Backend) |
| Docker | ล่าสุด (ถ้ารันแบบ container) |

### ขั้นตอน

```bash
# 1. โคลนโปรเจกต์
git clone https://github.com/ZyntroAI/crystalcastleX.git
cd crystalcastleX

# 2. เปิดใช้ pnpm เวอร์ชันที่โปรเจกต์กำหนด แล้วติดตั้ง dependencies
corepack enable
pnpm install

# 3. ตั้งค่าตัวแปรสภาพแวดล้อม
cp .env.example .env
#    แล้วเติมค่าจริงในไฟล์ .env (ห้าม commit ไฟล์ .env)

# 4. เริ่ม dev server
pnpm dev
```

> ⚠️ **สำคัญ:** ไฟล์ `.env` ถูกกันไว้ใน `.gitignore` แล้ว ห้าม commit คีย์จริงขึ้น GitHub เด็ดขาด
> ตั้งค่า `NEXT_PUBLIC_USE_MOCK=true` เพื่อทดสอบโดยไม่เสียเครดิตจริง

### คำสั่งที่ใช้บ่อย

```bash
pnpm dev          # dev server
pnpm build        # production build
pnpm lint         # ESLint
pnpm type-check   # tsc --noEmit
pnpm test         # vitest
pnpm coverage     # vitest + coverage
```

## 🧠 สถาปัตยกรรม AI

ระบบออกแบบเป็น **provider-neutral** — โค้ดธุรกิจไม่ผูกกับเจ้าของโมเดลรายใด
สลับผู้ให้บริการได้โดยแก้ที่ชั้น provider เท่านั้น

```
AI Layer
├── Prompts      — เทมเพลต prompt ที่ใช้ซ้ำได้
├── Pipelines    — ลำดับขั้นการประมวลผล (เช่น สร้างวิดีโอจาก storyboard)
└── Providers    — adapter ต่อผู้ให้บริการ (OpenAI / Gemini / Groq / FAL / …)

Core Layer
├── Video        — ประกอบและเข้ารหัสวิดีโอ
├── Render       — ประมวลผลภาพ/เฟรม
└── Captions     — สร้างและซิงก์คำบรรยาย
```

> 📌 **หมายเหตุ:** โฟลเดอร์มาตรฐาน `src/ai/prompts`, `src/ai/pipelines`, `src/ai/providers`,
> `src/core/video`, `src/core/render`, `src/core/captions` ถูกกำหนดเป็นเป้าหมายเชิงสถาปัตยกรรมแล้ว
> แต่ยังไม่ได้ย้ายโค้ดจริงเข้าไป — งานย้ายโค้ดอยู่ในแผนถัดไป (ดูรายละเอียดใน [`docs/`](docs/))

## 🔐 ความปลอดภัย & CI/CD

ทุก workflow ใน `.github/workflows/` ต้องผ่านมาตรฐานเหล่านี้:

- **SHA-pinned actions** — pin กับ commit SHA 40 ตัวทุกตัว (ไม่มี `@vN`)
- **Least-privilege `permissions:`** — ระบุขอบเขตสิทธิ์ทุก workflow
- **gitleaks secret scan** — สแกนความลับทุก push / pull request
- **`pnpm audit --audit-level high`** — กั้น dependency ที่มีช่องโหว่ระดับสูง
- **AI key verification** — ตรวจ `OPENAI_API_KEY` / `GEMINI_API_KEY` ว่ามีจริงและไม่ใช่ placeholder

อ่านนโยบายฉบับเต็มได้ที่ [`SECURITY.md`](SECURITY.md)

### Deployment Flow

| เป้าหมาย | Trigger | Environment |
| --- | --- | --- |
| Preview | Pull Request | `preview` |
| Production | push เข้า `main` | `production` |

## 🤝 การมีส่วนร่วม

อ่านขั้นตอนการทดสอบและ CI/CD ได้ที่ [`CONTRIBUTING.md`](CONTRIBUTING.md)

## 📄 License

MIT — ดูรายละเอียดใน [LICENSE](LICENSE)
