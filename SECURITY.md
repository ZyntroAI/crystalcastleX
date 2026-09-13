# Security Policy

## Supported Versions

| Version | Supported |
| --- | --- |
| main | ✅ |
| < 1.0 | ❌ |

## Reporting a Vulnerability

หากคุณพบช่องโหว่ด้านความปลอดภัย กรุณา **อย่าเปิดเป็น Public Issue**

**ช่องทางรายงานที่แนะนำ:**
1. เปิดผ่าน [GitHub Security Advisory](../../security/advisories/new) — วิธีที่ปลอดภัยที่สุด
2. หากฉุกเฉินมาก ติดต่อผู้ดูแล repo โดยตรงผ่าน GitHub

**สิ่งที่ควรรายงาน:** XSS, SQL Injection, ข้อมูลรั่วไหล, API Key/Token หลุด, RCE, Auth Bypass, Supply-chain (unpinned action)

**กระบวนการของเรา:**
1. ตอบรับรายงานภายใน **48 ชั่วโมง**
2. อัปเดตความคืบหน้าให้คุณทุก 5 วันทำการ จนกว่าแก้จะเสร็จ
3. เมื่อแก้เสร็จ จะให้เครดิตคุณใน release notes หากต้องการ

## CI/CD Security Standards

Repo นี้บังคับใช้มาตรฐานความปลอดภัยกับทุก workflow:

- **SHA-pinning** — action ทุกตัวต้อง pin กับ commit SHA 40 ตัว ห้ามใช้แท็ก `@vN` โดยเด็ดขาด
- **Least-privilege permissions** — ทุก workflow ต้องมี `permissions:` ระบุขอบเขตชัดเจน
- **Secret scanning** — ใช้ `gitleaks` สแกนทุก push และ pull request
- **Dependency audit** — `pnpm audit --audit-level high` กั้น dependency ที่มีช่องโหว่ระดับสูงขึ้นไป
- **AI key verification** — ตรวจว่าคีย์ `OPENAI_API_KEY` / `GEMINI_API_KEY` มีอยู่จริงและไม่ใช่ค่า placeholder

## Disclosure Policy

เรายึดหลัก Coordinated Disclosure ขอเวลา 90 วันในการแก้ไขก่อนเปิดเผยสู่สาธารณะ

## Out of Scope

- Rate limiting หรือ DoS ที่ไม่กระทบข้อมูล
- ปัญหาที่ต้องเข้าถึงเครื่องของ user โดยตรง (Physical access)
- Social engineering, Phishing
