yaml  
---
title: "📚 CrystalCastleX References — Complete Overview & Guide"
type: "guide"
status: "active"
created: "2026-10-26"
updated: "2026-10-26"
tags:
  - crystalcastlex
  - claude-skills
  - references
  - architecture
  - workflows
  - best-practices
related:
  - "[[AI Providers Reference — CrystalCastle X]]"
description: "แนะนำภาพรวมและจุดประสงค์ของไฟล์อ้างอิงทั้ง 5 ฉบับใน .claude/references/"
---
 
 
📚 คู่มือภาพรวม — ไฟล์อ้างอิงทั้ง 5 ฉบับ
 
โฟลเดอร์  .claude/references/  คือ แหล่งความรู้กลาง ที่ AI จะอ้างอิงอัตโนมัติเมื่อทำงานกับโปรเจกต์นี้ ✅
 
 
 
📋 รายการไฟล์และจุดประสงค์
 
# ไฟล์ หน้าที่ เมื่อควรอ่าน/แก้ไข 
🏗️  architecture.md  แผนภาพรวมระบบ, โครงสร้างโฟลเดอร์, เทคสแต็กหลัก เริ่มโปรเจกต์, เปลี่ยนแปลงโครงสร้าง, อธิบายระบบให้คนใหม่ 
📏  conventions.md  กฎการเขียนโค้ด, ชื่อตัวแปร, รูปแบบไฟล์, มารยาททีม ก่อนเขียนโค้ดใหม่, ตรวจสอบโค้ด, ตั้งค่า linter/formatter 
🤖  providers.md  การจัดการ LLM provider, failover, API key, ค่าใช้จ่าย เพิ่ม/เปลี่ยนโมเดล AI, ตั้งค่า API key, ตรวจสอบงบประมาณ 
🔧  repair-loop.md  วิธีแก้ไขปัญหาที่พบบ่อย, ขั้นตอนดีบัก, คู่มือกู้คืนระบบ เจอปัญหา, ระบบล่ม, ทดสอบไม่ผ่าน, ตรวจสอบสาเหตุ 
🔄  workflows.md  ขั้นตอนการทำงาน, PR, ทดสอบ, Deploy, กระบวนการทีม ส่งงาน, เปลี่ยนกระบวนการ, อัปเดต CI/CD 
 
 
 
💡 คำแนะนำการใช้งาน
 
✅ ควรทำ
 
- ✅ อ่านก่อนแก้ — เปิดไฟล์ที่เกี่ยวข้องก่อนเขียน/แก้โค้ด เพื่อให้ตรงกับมาตรฐาน
- ✅ อัปเดตพร้อมโค้ด — ถ้าเปลี่ยนแปลงระบบสำคัญ → อัปเดตเอกสารนี้ทันที
- ✅ ใช้อ้างอิงร่วมกันในทีม — ทุกคนอ่านจากจุดเดียว → ไม่มี "ทำตามความเข้าใจส่วนตัว"
- ✅ ให้ AI อ้างอิงอัตโนมัติ — วางใน  .claude/references/  AI จะโหลดเองเมื่อเปิดโปรเจกต์
 
📖 เส้นทางการอ่านแนะนำ
 
สถานการณ์ อ่านลำดับนี้ 
🆓 สมาชิกใหม่เข้าทีม  architecture  →  conventions  →  workflows  
💻 จะเขียนโค้ดใหม่  conventions  →  architecture  
🤖 จะทำงานส่วน AI/LLM  providers  →  architecture  
❌ เจอปัญหา/ระบบผิดปกติ  repair-loop  →  architecture  
🚀 จะส่งงาน/Deploy  workflows  →  conventions  
 
 
 
🗺️ ตัวอย่างการอ่านร่วมกัน
 
ต้องการเพิ่ม Provider AI ใหม่ → อ่าน  providers.md  เพื่อทำตามขั้นตอนที่กำหนด → ดู  architecture.md  วางไฟล์ตรงไหน → เช็ค  conventions.md  วิธีเขียนโค้ดให้ถูกต้อง → ปฏิบัติตาม  workflows.md  ตอนส่ง PR ✅
 
 
 
ต้องการให้สร้างเนื้อหาฉบับเต็มของไฟล์ไหนไหมครับ? 😊