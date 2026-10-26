yaml  
---
title: "Conventions — Coding Standards & Team Guidelines"
type: "reference"
status: "active"
created: "2026-10-26"
updated: "2026-10-26"
tags:
  - conventions
  - coding-standards
  - best-practices
  - team-guidelines
  - crystalcastlex
related:
  - "[[Architecture — System Overview]]"
  - "[[Workflows — Team Processes]]"
description: "มาตรฐานการเขียนโค้ด กฎการตั้งชื่อ รูปแบบไฟล์ และมารยาททีมงาน CrystalCastle X"
---
 
 
📏 Conventions — Coding Standards & Team Guidelines
 
โค้ดที่อ่านง่าย = โค้ดที่ดีที่สุด — กฎเหล็กของทีม ✅
 
 
 
🎯 วัตถุประสงค์เอกสารนี้
 
- ให้ทุกคนเขียนโค้ดใน ภาษาเดียวกัน
- ลดเวลาที่ใช้ถาม "ทำไมเขียนแบบนี้?"
- ให้การตรวจสอบโค้ดเน้นที่ ตรรกะและคุณภาพ ไม่ใช่รูปแบบ
- AI ทุกคน (Copilot, Claude, Cursor) ปฏิบัติตามกฎเดียวกัน
 
 
 
📖 สารบัญ
 
- 🐍 Python Style Guide
- 📁 การตั้งชื่อไฟล์และโฟลเดอร์
- 🔤 กฎการตั้งชื่อ
- 📝 รูปแบบโค้ด
- 📦 การนำเข้าโมดูล
- ✅ การเขียนทดสอบ
- 📄 เอกสารและความคิดเห็น
- 🛠️ เครื่องมือที่ใช้ตรวจสอบ
- ⚠️ สิ่งที่ห้ามทำอย่างเด็ดขาด
 
 
 
🐍 Python Style Guide
 
พื้นฐาน
 
- ปฏิบัติตาม PEP 8 เป็นหลัก
- ใช้ Ruff เป็น linter + formatter
- ความยาวบรรทัดสูงสุด: 100 ตัวอักษร
- ใช้ 4 ช่องว่าง ย่อหน้า — ห้ามใช้ Tab
- ไฟล์ทุกไฟล์ต้องมี UTF-8 encoding
 
เวอร์ชัน Python
 
- พัฒนาด้วย Python 3.12+
- เขียนให้เข้ากับ 3.12 ขึ้นไป — ไม่ต้องรองรับเวอร์ชันเก่า
 
 
 
📁 การตั้งชื่อไฟล์และโฟลเดอร์
 
สิ่งที่ตั้งชื่อ รูปแบบ ตัวอย่าง 
ไฟล์ Python  snake_case.py   api_client.py  ✅ /  ApiClient.py  ❌ 
โฟลเดอร์  snake_case/   utils/  ✅ /  Utils/  ❌ 
ไฟล์ทดสอบ  test_<module>.py   test_auth.py  ✅ 
คอนฟิก/สคริปต์  snake_case   ci-config.yml  ✅ 
Markdown เอกสาร  kebab-case.md   api-design.md  ✅ 
 
❌ ห้ามใช้ชื่อภาษาไทยหรืออักขระพิเศษในชื่อไฟล์
 
 
 
🔤 กฎการตั้งชื่อ
 
ประเภท รูปแบบ ตัวอย่าง 
ตัวแปร / ฟังก์ชัน  snake_case   user_name ,  calculate_cost()  
คลาส  PascalCase   LLMProvider ,  TaskService  
ค่าคงที่  UPPER_CASE   MAX_RETRIES = 5  
ตัวแปรส่วนตัว  _leading_underscore   _internal_state ,  validate_token()  
ตัวแปรที่ไม่ได้ใช้  _   for _ in range(3):  
 
ความชัดเจน > ความสั้น
 
python  
# ✅ ดี
number_of_tokens = 1024
is_payment_successful = True
calculate_total_cost()

# ❌ ไม่ดี
cnt = 1024
ok = True
calc()
 
 
คำย่อที่ยอมรับได้
 
-  api ,  id ,  url ,  db ,  ctx  — ใช้ได้
- คำย่ออื่นๆ ต้องอธิบาย หรือใช้ชื่อเต็ม
 
 
 
📝 รูปแบบโค้ด
 
ไฟล์เริ่มต้น — ทุกไฟล์ .py ควรมี
 
python  
"""สั้นๆ อธิบายว่าไฟล์นี้ทำอะไร"""
from __future__ import annotations

# Standard library imports
import os
from typing import Optional

# Third-party imports
from pydantic import BaseModel

# Local imports
from .config import settings
 
 
Import Order — เสมอ
 
1. 📦 Standard library →  import os ,  from typing import... 
2. 📦 Third-party packages →  from fastapi import... 
3. 📁 โมดูลภายในโปรเจกต์ →  from .utils import... 
4. เว้นบรรทัดระหว่างกลุ่ม
 
Type Hints — บังคับใช้
 
python  
# ✅ ดี
def calculate_cost(tokens: int, rate: float) -> float:
    return tokens * rate

# ❌ ไม่ดี — ไม่ระบุประเภท
def calculate_cost(tokens, rate):
    return tokens * rate
 
 
Docstrings
 
ใช้สไตล์ Google style:
 
python  
def calculate_cost(tokens: int, rate: float) -> float:
    """คำนวณค่าใช้จ่ายจากจำนวน token

    Args:
        tokens: จำนวน token ที่ใช้
        rate: อัตราค่าต่อ 1,000 token

    Returns:
        ค่าใช้จ่ายเป็นหน่วยดอลลาร์

    Raises:
        ValueError: ถ้า tokens หรือ rate เป็นค่าลบ
    """
    if tokens < 0 or rate < 0:
        raise ValueError("Tokens และ rate ต้องเป็นค่าบวก")
    return (tokens / 1000) * rate
 
 
ความคิดเห็น
 
- ความคิดเห็นอธิบาย ทำไม ไม่ใช่ ทำอะไร
- ความคิดเห็นภาษาไทยได้ แต่ต้องชัดเจน
- ลบความคิดเห็นที่ไม่ได้ใช้แล้ว — อย่าปล่อยทิ้งไว้
 
 
 
📦 การนำเข้าโมดูล
 
Absolute Import (แนะนำ)
 
python  
# ✅ จากรากโปรเจกต์
from src.ai.providers.router import get_provider

# ✅ สัมพัทธ์ภายในแพ็กเกจ
from .base import BaseProvider
 
 
❌ ห้ามทำ
 
python  
# ❌ นำเข้าทุกอย่างแบบนี้
from utils import *

# ❌ ใช้ฟังก์ชันโดยตรงจากภายนอก
import openai
client = openai.OpenAI()  # ❌ ห้าม — ต้องผ่าน providers.router
 
 
วงเล็บยาวเกินไป → ขึ้นบรรทัดใหม่
 
python  
# ✅ ดี
provider = get_provider(
    task="document_summary",
    priority=["openai", "gemini"],
    max_tokens=1024,
)
 
 
 
 
✅ การเขียนทดสอบ
 
ชื่อฟังก์ชันทดสอบ
 
python  
def test_calculate_cost_with_valid_input():
    pass

def test_calculate_cost_raises_for_negative_tokens():
    pass
 
 
จัดเรียงเนื้อหา
 
python  
# Arrange — เตรียมข้อมูล
tokens = 1000
rate = 0.015

# Act — ทำการทดสอบ
result = calculate_cost(tokens, rate)

# Assert — ตรวจสอบผลลัพธ์
assert result == 0.015
 
 
สิ่งที่ควรทดสอบ
 
- ✅ กรณีปกติ
- ✅ ค่าขอบเขต (ค่าต่ำสุด/สูงสุด)
- ✅ ข้อมูลไม่ถูกต้อง / ข้อมูลว่าง
- ❌ ไม่ต้องทดสอบไลบรารีภายนอก — ทดสอบแค่ตรรกะของเรา
 
 
 
📄 เอกสารและความคิดเห็น
 
- ทุกไฟล์หลักควรมี docstring บอกว่าไฟล์นี้ทำอะไร
- เมื่อแก้ไขสิ่งที่สำคัญ → อัปเดตเอกสารด้วย
- ใช้ภาษาไทยหรืออังกฤษให้สอดคล้องกับส่วนที่เหลือของไฟล์
- เอกสารใน  .claude/references/  เป็นแหล่งความจริงสุดท้าย — โค้ดต้องสอดคล้องกับเอกสาร
 
 
 
🛠️ เครื่องมือที่ใช้ตรวจสอบ
 
pyproject.toml — ตัวอย่างคอนฟิก
 
toml  
[tool.ruff]
line-length = 100
indent-width = 4
src = ["src"]

[tool.ruff.lint]
select = [
  "E",      # pycodestyle errors
  "W",      # pycodestyle warnings
  "F",      # pyflakes
  "I",      # isort
  "UP",     # pyupgrade
  "B",      # flake8-bugbear
  "C4",     # flake8-comprehensions
  "SIM",    # flake8-simplify
]
ignore = ["E501"]  # Handled by formatter

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401"]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
 
 
คำสั่งตรวจสอบก่อนส่ง PR
 
bash  
# จัดรูปแบบโค้ด
ruff format src/

# ตรวจสอบกฎ
ruff check src/

# ตรวจสอบและแก้ไขอัตโนมัติ
ruff check src/ --fix

# รันทดสอบ
pytest tests/ -v
 
 
💡 ตั้งค่า VS Code: บันทึกไฟล์แล้วจัดรูปแบบอัตโนมัติ — ไม่ต้องทำด้วยตัวเองอีกต่อไป ✅
 
 
 
⚠️ สิ่งที่ห้ามทำอย่างเด็ดขาด
 
❌ ห้ามทำ เหตุผล 
Hard-code API key หรือความลับในโค้ด ความปลอดภัย — ใช้ Environment Variable แทน 
เรียก LLM SDK โดยตรงใน business logic ต้องผ่าน  providers.router  เพื่อจัดการ failover + cost 
Commit ไฟล์ที่มีข้อมูลส่วนตัว ตรวจสอบ  .gitignore  ก่อน commit เสมอ 
ปิดการทำงานของ linter โดยไม่มีเหตุผลอันควร รักษาคุณภาพโค้ด 
เขียนโค้ดที่อ่านไม่ออกเพื่อ "ทำให้สั้น" โค้ดอ่านซ้ำบ่อยกว่าเขียนครั้งเดียว 
ปรับแก้เอกสารอ้างอิงโดยไม่แจ้งทีม เอกสารกลางต้องตรงกับความจริงเสมอ 
 
 
 
✅ กฎทอง: "ถ้าโค้ดของคุณทำให้คนอื่นต้องถามว่า 'ทำไมถึงเขียนแบบนี้?' แสดงว่าคุณเขียนผิดแบบแล้ว"
 
ต้องการสร้างเนื้อหาฉบับเต็มของไฟล์ถัดไปไหมครับ? 😊