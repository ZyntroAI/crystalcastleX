yaml  
---
title: "Repair Loop — Troubleshooting & System Recovery Guide"
type: "reference"
status: "active"
created: "2026-10-26"
updated: "2026-10-26"
tags:
  - troubleshooting
  - debugging
  - repair
  - incident-response
  - crystalcastlex
related:
  - "[[Architecture — System Overview]]"
  - "[[Conventions — Coding Standards]]"
  - "[[Providers — LLM Integration & Failover]]"
description: "คู่มือแก้ไขปัญหาที่พบบ่อย ขั้นตอนดีบัก และการกู้คืนระบบสำหรับ CrystalCastle X"
---
 
 
🔧 Repair Loop — Troubleshooting & System Recovery Guide
 
สงบ → ตรวจสอบ → แยกส่วน → แก้ไข → บันทึก ✅
 
 
 
🎯 วัตถุประสงค์เอกสารนี้
 
- มีขั้นตอนปฏิบัติเมื่อเจอปัญหา — ไม่ต้องคิดใหม่ทุกครั้ง
- แยกแยะสาเหตุได้เร็วขึ้น
- กู้คืนระบบได้เร็วที่สุด
- บันทึกสาเหตุและวิธีแก้ — ไม่ให้ปัญหาเดิมกลับมาอีก
 
 
 
📖 สารบัญ
 
- 🚨 ขั้นตอนเมื่อเกิดปัญหา — 5 ขั้นตอน
- 🔍 คู่มือวินิจฉัย — แยกส่วนเพื่อหาสาเหตุ
- 📋 ปัญหาที่พบบ่อย & วิธีแก้ไข
- 🔴 เริ่มระบบไม่ได้
- 🟡 ทดสอบไม่ผ่าน
- 🤖 LLM/Provider มีปัญหา
- ⚡ ประสิทธิภาพช้าผิดปกติ
- 💰 ค่าใช้จ่ายเกินงบ
- 🔄 การกู้คืนระบบ
- 📝 บันทึกหลังแก้ไข — Post-Mortem
 
 
 
🚨 ขั้นตอนเมื่อเกิดปัญหา — 5 ขั้นตอน
 
1️⃣ ยืนยันและจำกัดขอบเขต
 
- ✅ เกิดขึ้นเมื่อไหร่? เริ่มจากตรงไหน?
- ✅ ใครได้รับผลกระทบ? ทุกคนหรือบางกลุ่ม?
- ✅ ยังทำงานส่วนไหนได้บ้าง?
- ✅ มีการเปลี่ยนแปลงอะไรก่อนหน้านี้หรือไม่? (โค้ด, คอนฟิก, เวอร์ชัน)
 
📌 กฎสำคัญ: อย่าเพิ่งแก้ไขก่อนรู้สาเหตุ — บันทึกสถานะปัจจุบันก่อนเสมอ
 
2️⃣ ตรวจสอบ Logs
 
bash  
# Application logs
tail -f logs/app.log

# FastAPI access logs
tail -f logs/access.log

# Error logs เท่านั้น
grep ERROR logs/app.log

# ดู 50 บรรทัดล่าสุดที่มี ERROR
grep ERROR logs/app.log -A 5 -B 5 | tail -50
 
 
3️⃣ แยกส่วน — ปิดทีละส่วน
 
- ❓ ใช้งานได้ในเครื่องหรือไม่? → แยก Environment
- ❓ API ตอบกลับหรือไม่? → แยก Layer
- ❓ ปิด LLM ยังทำงานได้ไหม? → แยก External Service
- ❓ ใช้ Provider อื่นได้ไหม? → แยก Provider
 
4️⃣ แก้ไขแบบควบคุม
 
- ✅ เปลี่ยนอย่างเดียวครั้งเดียว
- ✅ ทดสอบก่อนขยายผล
- ✅ ถ้าไม่ได้ → ย้อนกลับ
 
5️⃣ บันทึกและป้องกัน
 
- ✅ สาเหตุคืออะไร?
- ✅ แก้ไขอย่างไร?
- ✅ จะป้องกันอย่างไรในอนาคต?
- ✅ อัปเดตเอกสารนี้เลย!
 
 
 
🔍 คู่มือวินิจฉัย — แยกส่วนเพื่อหาสาเหตุ
 
🧪 แผนผังวินิจฉัย
 
plaintext  
ระบบมีปัญหา
    │
    ├── ใช้งานในเครื่องได้ไหม?
    │   ├── ✅ ได้ → ปัญหาที่ Environment/Deployment/Config
    │   └── ❌ ไม่ได้ → ปัญหาที่โค้ด/การตั้งค่าพื้นฐาน
    │
    ├── API ตอบสนองไหม?
    │   ├── ❌ ไม่ตอบ → ตรวจสอบ Server/Port/Process
    │   └── ✅ ตอบ แต่ Error → ตรวจสอบ Status Code
    │       ├── 4xx → ข้อมูล/สิทธิ์/คำขอ
    │       ├── 5xx → เซิร์ฟเวอร์/การเชื่อมต่อ
    │       └── 429 → Rate Limit/Quota
    │
    ├── LLM ทำงานไหม?
    │   ├── ❌ ไม่เลย → ตรวจสอบ API Key/Network/Provider Status
    │   ├── ✅ บาง provider ได้ → สลับ Provider ตรวจสอบ failover
    │   └── ⏱️ ช้ามาก → ตรวจสอบ Timeout/Cache/Queue
    │
    └── ทดสอบผ่านไหม?
        ├── ❌ ล้มทุกครั้ง → โค้ด/ตรรกะ
        ├── ⚠️ บางครั้งล้ม → Race Condition/ข้อมูลไม่คงที่/Rate Limit
        └── 🟡 ช้ากว่าปกติ → Performance/Resource/External Service
 
 
 
 
📋 ปัญหาที่พบบ่อย & วิธีแก้ไข
 
🔴 เริ่มระบบไม่ได้
 
อาการ สาเหตุที่เป็นไปได้ วิธีตรวจสอบ วิธีแก้ไข 
ImportError / ModuleNotFoundError Virtual env ไม่ถูกต้อง หรือ dependency หาย  which python  /  pip list  สร้าง venv ใหม่ → ติดตั้งจาก  requirements.txt  
ConfigValidationError Env var หายหรือผิดชื่อ เปรียบเทียบ  .env  กับ  .env.example  คัดลอก  .env.example  → แก้ไขค่าจริง 
Address already in use พอร์ตถูกใช้งานอยู่  lsof -i :8000  ปิด process เดิม หรือเปลี่ยนพอร์ตชั่วคราว 
Redis/DB Connection Error Service ไม่ทำงานหรือผิดค่า  redis-cli ping  /  nc -vz localhost 5432  เริ่ม container/service ที่หายไป ตรวจสอบค่า URL 
 
💡 กฎทอง: ถ้าในเครื่องทำงาน แต่ใน CI/Production ไม่ทำงาน → ปัญหาคือ Environment/Config/Dependency ไม่ใช่โค้ด
 
 
 
🟡 ทดสอบไม่ผ่าน
 
อาการ สาเหตุที่เป็นไปได้ วิธีแก้ไข 
ล้มเฉพาะ Python 3.13 API บางอย่างเปลี่ยนพฤติกรรม ตรวจสอบ Deprecation Warning / Changelog ของไลบรารี 
บางครั้งผ่าน บางครั้งล้ม ข้อมูลทดสอบซ้ำซ้อน, Race condition, Timeout ใช้  pytest-rerunfailures  ชั่วคราว → แก้ไขให้เป็น Deterministic 
Passed locally but Failed in CI Dependency เวอร์ชันต่างกัน / Cache ค้าง ลบ  __pycache__  → รันด้วย  --fresh-env  / ตรวจสอบ  requirements.txt  ล่าสุด 
Too Slow / Timeout เรียก LLM จริงในทดสอบ → ❌ ห้าม ใช้  unittest.mock  /  pytest-mock  แทนการเรียกจริง 
 
 
 
🤖 LLM/Provider มีปัญหา
 
อาการ สาเหตุที่เป็นไปได้ วิธีแก้ไข 
Authentication Error 401 API Key หมดอายุ/ผิด/ไม่ได้ตั้งค่า ตรวจสอบ  echo $OPENAI_API_KEY  → ตั้งค่าใหม่ → หมุน key ถ้าจำเป็น 
Rate Limit 429 เกินโควต้าหรือความถี่ ✅ ตรวจสอบ  retry_after  ใน response header ✅ เพิ่ม  backoff_factor  ✅ สลับ Provider ทันที 
Timeout / No Response อินเทอร์เน็ตหรือปลายทางช้า/ล่ม ✅ เพิ่ม Timeout setting ✅ ตรวจสอบสถานะหน้าเว็บ Provider ✅ ระบบควร Failover เอง — ถ้าไม่ → ตรวจสอบ  router.py  
Circuit Breaker Open Provider ล้มเกิน 3 ครั้งติด → พัก 5 นาที ✅ รอ 5 นาที หรือ Reset ด้วย endpoint/admin ✅ ตรวจสอบว่า Provider นั้นกลับมาแล้วหรือยัง ✅ ถ้าปัญหายาว → สลับลำดับใน  LLM_PROVIDER_PRIORITY  
All Providers Failed ทางออกอินเทอร์เน็ต/ระบบภายนอกล่มหมด ✅ แจ้งผู้ใช้ → "ระบบกำลังยุ่ง โปรดลองใหม่ภายในไม่กี่นาที" ✅ ตรวจสอบสถานะหน้าเว็บแต่ละ Provider ✅ ตรวจสอบ Proxy/VPN 
 
 
 
⚡ ประสิทธิภาพช้าผิดปกติ
 
อาการ สาเหตุที่เป็นไปได้ วิธีตรวจสอบ วิธีแก้ไข 
ทุกคำขอช้าลง 2-3 เท่า Database/Query ไม่มีดัชนี หรือ Cache หาย ดู Log ช้า →  EXPLAIN ANALYZE  เพิ่ม Index / เปิด Redis Cache 
ช้าเฉพาะบางครั้ง LLM Response ไม่คงที่ / คิวงานแออัด เปรียบเทียบเวลาตอบสนองแต่ละ Provider เพิ่ม Worker / ปรับ Priority / เปิด Cache สำหรับ Prompt ซ้ำ 
หน่วยความจำเพิ่มเรื่อยๆ Connection ไม่ปิด / Memory Leak ตรวจสอบจำนวน Connection / GC Stats ปิด Connection ใน  finally:  บล็อก / ใช้ Context Manager 
 
 
 
💰 ค่าใช้จ่ายเกินงบ
 
อาการ สาเหตุที่เป็นไปได้ วิธีแก้ไข 
เกิน Daily Budget งานมากกว่าที่คาด / Loop เรียกซ้ำ ✅ ระบบควรปฏิเสธงานใหม่อัตโนมัติ → ตรวจสอบ  LLM_MAX_COST_PER_DAY  ✅ หยุดงานที่ไม่จำเป็น ✅ ตรวจสอบว่ามี Loop ที่เรียก LLM ซ้ำหรือไม่ 
Token พุ่งผิดปกติ Prompt ยาวเกินไป / Output ไม่ถูกตัด ✅ ตรวจสอบ Prompt Template — ไม่ส่งข้อมูลซ้ำซ้อน ✅ ตั้ง  max_tokens  ที่เหมาะสม ✅ เปิด Truncation อัตโนมัติ 
Provider ใดรายหนึ่งใช้มากผิดปกติ Failover ไม่ทำงาน / อีกตัวล้มนาน ✅ ตรวจสอบ Circuit Breaker ✅ สลับ Priority ชั่วคราว ✅ แจ้งทีมว่า Provider นั้นมีปัญหา 
 
 
 
🔄 การกู้คืนระบบ
 
�️ ขั้นตอนกู้คืนฉุกเฉิน
 
plaintext  
🚨 ระบบล่ม → ปฏิบัติตามลำดับนี้:

1. ยืนยันปัญหา
   ├── ส่งข้อความแจ้งทีม: "ระบบล่ม — กำลังตรวจสอบ"
   ├── บันทึกเวลาที่เริ่มเกิดปัญหา
   └── ระบุสิ่งที่ทำงานไม่ได้

2. ลดผลกระทบก่อน
   ├── หยุดงานใหม่ถ้าจำเป็น
   ├── สลับไปใช้ Provider สำรอง
   ├── เปิดโหมด Maintenance Page
   └── แจ้งผู้ใช้: "กำลังแก้ไข — จะกลับมาใช้งานได้ภายใน X นาที"

3. กู้คืน
   ├── ✅ กลับไปใช้เวอร์ชันล่าสุดที่ทำงานได้ (Git Revert / Rollback Deploy)
   ├── ✅ รีสตาร์ท Service ที่ล้ม
   ├── ✅ ล้าง Cache ที่อาจเสียหาย
   └── ✅ ทดสอบด้วยตัวเองก่อนเปิดให้ทุกคน

4. ยืนยันว่ากลับมาปกติ
   ├── ตรวจสอบ Health Check ✅
   ├── ทดสอบ Endpoint หลัก ✅
   ├── ตรวจสอบ Log ไม่มี Error ใหม่ ✅
   └── แจ้งผู้ใช้: "กลับมาใช้งานได้ปกติแล้ว ขอบคุณที่รอคอย 🙏"
 
 
🔙 ย้อนกลับเวอร์ชัน (Rollback)
 
bash  
# ดูประวัติ commit ล่าสุด
git log --oneline -10

# ย้อนกลับไป commit ก่อนหน้า
git checkout main
git revert <commit-hash-that-broke>
git push origin main

# หรือ reset ไปยังจุดที่ดี
git reset --hard <good-commit-hash>
git push --force-with-lease origin main
# ⚠️ ใช้ --force-with-lease เสมอ — ปลอดภัยกว่า
 
 
🧹 ล้างสถานะเสีย
 
bash  
# ล้าง Redis Cache (ระวัง — ข้อมูลหายหมด)
redis-cli FLUSHDB

# รีสตาร์ท Service
sudo systemctl restart crystalcastlex

# ตรวจสอบสถานะ
sudo systemctl status crystalcastlex
 
 
 
 
📝 บันทึกหลังแก้ไข — Post-Mortem
 
ทุกครั้งที่เกิดปัญหาระดับสำคัญ — กรอกบันทึกนี้ภายใน 24 ชั่วโมง ✅
 
markdown  
# 📝 บันทึกเหตุการณ์: [ชื่อปัญหา]

**วันที่:** YYYY-MM-DD
**เวลาเริ่ม:** HH:MM | **เวลาแก้ไขเสร็จ:** HH:MM
**ผู้บันทึก:** ชื่อ

## 1. เกิดอะไรขึ้น?
สรุปสั้นๆ ชัดเจน

## 2. สาเหตุที่แท้จริงคืออะไร?
- สาเหตุโดยตรง: ...
- ปัจจัยที่ทำให้แย่ลง: ...
- สิ่งที่เราพลาดไป: ...

## 3. ผลกระทบ
- ระยะเวลาที่ใช้งานไม่ได้: ... นาที
- ผู้ใช้ที่ได้รับผลกระทบ: ... คน
- ความเสียหาย/ค่าใช้จ่ายเพิ่ม: ...

## 4. แก้ไขอย่างไร?
- ขั้นตอนที่ทำ: ...
- เวลาที่กลับมาปกติ: ...

## 5. จะป้องกันอย่างไรในอนาคต?
- [ ] เพิ่มการตรวจสอบก่อน Deploy
- [ ] ปรับปรุงเอกสาร
- [ ] เพิ่มการแจ้งเตือนเมื่อใกล้เกินงบ
- [ ] ปรับปรุง Circuit Breaker / Failover logic
- [ ] อัปเดตเอกสาร `repair-loop.md` ด้วยปัญหานี้

> ✅ ปิดเมื่อทำครบทุกข้อ
 
 
 
 
💡 อัปเดตเอกสารนี้: ทุกครั้งที่เจอปัญหาใหม่และแก้ไขสำเร็จ → เพิ่มลงในตารางปัญหาที่พบบ่อย ทันที เพื่อให้ทีมทุกคนได้เรียนรู้จากประสบการณ์เดียวกัน ✅
 
ต้องการสร้างเนื้อหาฉบับเต็มของไฟล์ถัดไปไหมครับ? 😊