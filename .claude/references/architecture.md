yaml  
---
title: "Architecture — CrystalCastle X System Overview"
type: "reference"
status: "active"
created: "2026-10-26"
updated: "2026-10-26"
tags:
  - architecture
  - overview
  - project-structure
  - tech-stack
  - crystalcastlex
related:
  - "[[Conventions — Coding Standards]]"
  - "[[AI Providers Reference — CrystalCastle X]]"
description: "แผนภาพรวมระบบ โครงสร้างโฟลเดอร์ และเทคสแต็กหลักของ CrystalCastle X"
---
 
 
🏗️ Architecture — CrystalCastle X
 
ภาพรวมระบบสำหรับสมาชิกใหม่ การออกแบบ และการตัดสินใจเกี่ยวกับโครงสร้าง ✅
 
 
 
🎯 วัตถุประสงค์เอกสารนี้
 
- เข้าใจภาพรวมระบบได้ใน 5 นาที
- รู้ว่าโค้ดส่วนไหนอยู่ที่ไหน
- ทราบเหตุผลที่เลือกแต่ละเทคโนโลยี
- อ้างอิงเมื่อตัดสินใจเปลี่ยนแปลงโครงสร้าง
 
 
 
📖 สารบัญ
 
- 📋 ภาพรวมระบบ
- 📁 โครงสร้างโฟลเดอร์
- 🛠️ เทคสแต็กหลัก
- 🔄 ขั้นตอนการทำงานหลัก
- 📐 หลักการออกแบบ
- ⚠️ ข้อผิดพลาดที่ควรหลีกเลี่ยง
 
 
 
📋 ภาพรวมระบบ
 
CrystalCastle X เป็นแพลตฟอร์มประมวลผลเนื้อหาและสร้างเนื้อหาด้วย AI ที่ออกแบบมาเพื่อ:
 
- 📥 รับไฟล์/เนื้อหาจากหลายแหล่ง
- 🤖 ประมวลผลด้วย LLM หลายผู้ให้บริการ (พร้อม failover อัตโนมัติ)
- 📤 ส่งผลลัพธ์กลับไปยังผู้ใช้หรือระบบอื่น
- 💰 ติดตามและควบคุมค่าใช้จ่ายการใช้ AI
 
plaintext  
┌─────────────────┐     ┌──────────────────────┐     ┌──────────────────┐
│  ผู้ใช้ / ระบบ   │────▶│  API Gateway / Layer  │────▶│  Task Router     │
│  ภายนอก         │     │  การตรวจสอบสิทธิ์     │     │  คิวงาน + กฎ   │
└─────────────────┘     └──────────────────────┘     └────────┬───────┘
                                                              │
                     ┌──────────────────┬─────────────────────┼──────────────────┐
                     ▼                  ▼                     ▼                  ▼
          ┌──────────────────┐ ┌──────────────┐  ┌──────────────────┐ ┌───────────────┐
          │  OpenAI Provider │ │ Gemini Prov. │  │  Mistral Prov.   │ │  Cache Layer   │
          │  (gpt-4o-mini)   │ │ (gemini-1.5) │  │  (mistral-large) │ │  Redis / DB    │
          └──────────────────┘ └──────────────┘  └──────────────────┘ └───────────────┘
 
 
 
 
📁 โครงสร้างโฟลเดอร์
 
plaintext  
crystalcastlex/
├── .claude/                     # 🤖 AI Assistant Skills
│   └── references/              #   → ไฟล์อ้างอิงทั้งหมด (ที่คุณกำลังอ่าน)
│
├── src/
│   ├── ai/
│   │   ├── providers/           # ⚡ LLM Provider Abstraction Layer
│   │   │   ├── base.py         #    — Interface มาตรฐาน
│   │   │   ├── openai_provider.py
│   │   │   ├── gemini_provider.py
│   │   │   ├── mistral_provider.py
│   │   │   └── router.py       #    — เลือก provider + failover + circuit breaker
│   │   ├── prompts/             # 📝 Prompt Templates (.md, versioned)
│   │   └── tasks/               # 📋 Task Definitions & Business Logic
│   │
│   ├── api/                     # 🌐 REST API Layer
│   │   ├── routes/             #    — Endpoints
│   │   ├── middleware/         #    — Auth, Logging, Rate Limit
│   │   └── main.py             #    — App Entry Point
│   │
│   ├── core/                    # ⚙️ Core Utilities
│   │   ├── config.py           #    — Settings & Environment Variables
│   │   ├── logging.py          #    — Structured Logging
│   │   └── exceptions.py       #    — Custom Exceptions
│   │
│   ├── db/                      # 🗄️ Database Layer
│   │   ├── redis.py            #    — Cache & Queue
│   │   └── postgres.py         #    — Persistent Storage
│   │
│   └── utils/                   # 🔧 Shared Helpers
│       ├── cost_tracker.py     #    — คำนวณค่าใช้จ่าย AI
│       └── validators.py       #    — Input Validation
│
├── tests/                       # 🧪 Tests
│   ├── unit/
│   └── integration/
│
├── .github/workflows/           # 🔄 CI/CD
│   ├── ci.yml
│   └── ai-cost-monitor.yml
│
├── .env.example                # 🔑 Environment Variables Template
├── pyproject.toml              # 📦 Dependencies & Metadata
└── README.md                   # 👋 Project Introduction
 
 
📌 กฎสำคัญเกี่ยวกับโครงสร้าง
 
- Business Logic → อยู่ใน  src/ai/tasks/  เท่านั้น — ไม่ปะปนกับ API layer
- LLM Calls → ผ่าน  src/ai/providers/router.py  เท่านั้น — ห้ามเรียก SDK โดยตรง
- Prompts → แยกไฟล์ที่  src/ai/prompts/  — ไม่ hardcode ในโค้ด
- Config → อ่านผ่าน  src/core/config.py  — ไม่อ่าน  os.environ  โดยตรง
 
 
 
🛠️ เทคสแต็กหลัก
 
ชั้น/ส่วน เทคโนโลยี เหตุผลที่เลือก ทางเลือกที่พิจารณา 
ภาษา Python 3.12+ ยืดหยุ่น, ชุมชน AI ใหญ่, ecosystem ครบถ้วน — 
API Framework FastAPI Async รองรับ, ประเภทชัดเจน, docs อัตโนมัติ Flask, Starlette 
LLM Providers OpenAI, Gemini, Mistral ครอบคลุม, หลากหลาย, failover ได้ Anthropic, Groq 
Cache / Queue Redis คิวงาน, แคช, ตัวนับ — ที่เดียวครบ RabbitMQ, Memcached 
Database PostgreSQL คงที่, เชื่อมโยงข้อมูลได้ดี, มีมาตรฐาน SQLite (dev-only) 
Configuration Pydantic Settings ตรวจสอบประเภท, env auto-load python-dotenv 
Testing pytest ยืดหยุ่น, plugin เยอะ unittest 
CI/CD GitHub Actions รวมอยู่ในแพลตฟอร์ม, ไม่ต้องเซิร์ฟเวอร์เพิ่ม GitLab CI 
 
 
 
🔄 ขั้นตอนการทำงานหลัก
 
plaintext  
1. รับคำขอ → POST /api/v1/task
   ├── ตรวจสอบสิทธิ์ + Validate Input
   └── บันทึกลงคิว

2. ประมวลผล
   ├── Router เลือก Provider ที่เหมาะสม + พร้อมใช้งาน
   ├── โหลด Prompt Template + ใส่ค่า
   ├── เรียก LLM (มี retry + timeout + fallback)
   ├── บันทึกการใช้งาน (token, cost, latency)

3. ส่งคืน
   ├── จัดรูปแบบผลลัพธ์
   └── ส่งกลับ + สถานะ
 
 
 
 
📐 หลักการออกแบบ
 
หลักการ ความหมาย 
🧱 Separation of Concerns API, Business Logic, LLM Integration — แยกกันอย่างชัดเจน เปลี่ยนส่วนหนึ่งไม่กระทบส่วนอื่น 
🛡️ Abstraction First ไม่ผูกติดกับผู้ให้บริการรายใดรายหนึ่ง — สลับได้ทันทีถ้ามีปัญหา 
💰 Cost Visibility รู้ต้นทุนทุกคำขอ — ป้องกันความประหลาดใจเมื่อใบเสร็จมาถึง 
🔁 Resilience by Design ระบบไม่ล้มเมื่อ service ภายนอกล้ม — มีทางเลือกเสมอ 
📝 Explicit over Implicit โค้ดอ่านง่าย กฎชัดเจน ไม่มี "เวทมนตร์" ที่ซ่อนอยู่ 
 
 
 
⚠️ ข้อผิดพลาดที่ควรหลีกเลี่ยง
 
❌ อย่าทำ ✅ ให้ทำแทน เหตุผล 
เรียก OpenAI SDK โดยตรงใน route ผ่าน  providers.router  เสมอ จัดการ failover + cost tracking ที่จุดเดียว 
เขียน prompt ยาวๆ ในโค้ด เก็บที่  src/ai/prompts/  เป็นไฟล์ .md Version control + review ได้ 
อ่าน  os.environ  โดยตรง ใช้  src/core/config.py  ตรวจสอบค่าที่ขาดหายไปตอนเริ่มระบบ 
สร้างการเชื่อมต่อ DB ในแต่ละไฟล์ ใช้ singleton จาก  db/postgres.py  จัดการ connection pool อย่างถูกต้อง 
บันทึก API key ใน log ใช้ filter — เซนซิทีฟข้อมูลต้องถูกซ่อน ความปลอดภัยและกฎหมาย 
 
 
 
💡 อัปเดตล่าสุด: หากคุณเปลี่ยนแปลงโครงสร้างสำคัญในโค้ด — อัปเดตไฟล์นี้ทันที เพื่อให้ทีมทุกคนเห็นภาพเดียวกัน ✅
 
ต้องการสร้างเนื้อหาฉบับเต็มของไฟล์ถัดไปไหมครับ? 😊