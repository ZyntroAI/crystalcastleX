# Security Policy

## Supported Versions

| Version | Status | EOL |
|---------|--------|-----|
| 1.x     | ✅ Supported | — |
| < 1.0   | ❌ End-of-life (ไม่ได้รับการแก้ไข) | — |
| `main` branch | ⚠️ Development only — ไม่แนะนำให้ใช้ใน production | — |

> หากคุณใช้ version ที่ไม่ได้รับการสนับสนุน เราอาจไม่สามารถแก้ไขช่องโหว่ให้คุณได้

---

## Reporting a Vulnerability

⚠️ **ห้ามเปิด Public Issue / ห้ามโพสต์ PoC สู่สาธารณะ**

### ช่องทางรายงาน (เรียงลำดับความปลอดภัย)

1. **GitHub Security Advisory** (แนะนำที่สุด):  
   https://github.com/ZyntroAI/crystalcastleX/security/advisories/new
2. **กรณีฉุกเฉิน**: ติดต่อผู้ดูแลผ่าน GitHub DM หรืออีเมล `security@yourdomain.com`
3. **เข้ารหัสข้อมูลละเอียดอ่อน**: PGP key (แนบท้าย profile) หากรายงานมี PoC ที่ละเอียดอ่อน

### สิ่งที่ควรแนบมาพร้อมรายงาน
- Version / commit SHA ที่ทดสอบพบ
- Steps to reproduce ที่ทำซ้ำได้
- Impact assessment (ผู้โจมตีทำอะไรได้บ้าง)
- PoC code / screenshot / video
- Suggested fix (ถ้ามี)
- Severity ที่คุณประเมิน (CVSS v3.1 score)

### นโยบาย Bug Bounty
- **ขณะนี้ยังไม่มีโครงการ bounty เงินสด** แต่จะให้เครดิตใน Security Advisory + Release Notes หากรายงานถูกต้อง
- หากเปิดโปรแกรมในอนาคต จะประกาศที่หน้านี้

---

## Response & Fix SLA (แยกตามความรุนแรง)

| Severity | ตอบรับเริ่มต้น | เป้าหมายแก้ไข |
|----------|---------------|---------------|
| Critical (RCE, secret leak, auth bypass ทั่วระบบ) | 24 ชั่วโมง | 7 วัน |
| High (XSS stored, SQLi, privilege escalation) | 48 ชั่วโมง | 30 วัน |
| Medium | 5 วันทำการ | 90 วัน |
| Low / Info | 10 วันทำการ | Best effort |

- อัปเดตความคืบหน้าทุก **5 วันทำการ** จนกว่าจะแก้เสร็จ
- เราสามารถขอ **CVE ID** ให้ผ่าน GitHub Advisory ได้หากต้องการ
- ให้เครดิตผู้รายงานใน Advisory และ Release Notes (ยกเว้นผู้รายงานไม่ต้องการ)

---

## Coordinated Disclosure Policy

- ยึดหลัก **Coordinated Disclosure ระยะเวลา 90 วัน** นับจากวันรับรายงาน
- หากต้องการเวลาเพิ่ม สามารถตกลงขยายร่วมกันได้
- หากภายใน 90 วันยังไม่แก้ ผู้รายงานมีสิทธิ์เปิดเผยสู่สาธารณะหลังจากแจ้งให้ทราบล่วงหน้า 14 วัน
- **ห้ามเปิดเผยช่องโหว่สู่สาธารณะก่อนที่จะมี patch เผยแพร่แล้ว** เว้นแต่ตกลงกันไว้

---

## CI/CD & Supply-Chain Security Standards

ทุก workflow ใน repo นี้ต้องผ่านมาตรฐานดังต่อไปนี้:

| มาตรฐาน | สถานะ |
|---------|--------|
| **SHA-pinning** — action ทุกตัว pin ด้วย commit SHA 40 ตัว + Dependabot อัปเดตอัตโนมัติ | ⚠️ อยู่ระหว่าง migrate (ปัจจุบันบางตัวยังใช้ @vN) |
| **Least-privilege `permissions:`** — ทุก workflow ระบุขอบเขตชัดเจน; repo default `GITHUB_TOKEN` = read-only | ✅ |
| **Secret scanning** — `gitleaks` ทุก push/PR + GitHub Push Protection; หากพบ key รั่ว → rotate ทันที | ✅ |
| **Dependency audit** — `pnpm audit --audit-level high` + `dependency-review-action` กั้น PR ที่เพิ่ม dependency มีช่องโหว่ | ✅ |
| **CodeQL** — static analysis ทุก PR (ภาษา JS/TS + Python) | ✅ |
| **Trivy image scan** — scan Docker image ทุก build, block ถ้ามี CRITICAL ที่แก้ได้ | ⏳ แนะนำให้เพิ่ม |
| **AI key verification** — ตรวจ `OPENAI_API_KEY`/`GEMINI_API_KEY` ไม่ใช่ placeholder; key มี scope จำกัด + rotate ทุก 90 วัน + budget alert | ✅ |
| **OIDC** — deploy ไป cloud/registry ด้วย OIDC ไม่ใช้ long-lived secret | ⏳ แนะนำให้เพิ่ม |
| **Artifact attestation + SBOM** — ทุก image มี SBOM และ provenance attestation | ⏳ |
| **Branch protection** — `main` ต้องมี required review, ไม่อนุญาติ force push, แนะนำ signed commits | ✅ |
| **Self-hosted runner** — ใช้ ephemeral runner, isolate network, **ห้ามรัน workflow จาก fork PR บน self-hosted runner** | ⚠️ ตรวจสอบ |

---

## Safe Harbor (สิ่งที่อนุญาติ / ห้ามทำ)

### ✅ ถือว่าอนุญาติ (เราจะไม่ดำเนินคดี)
- ทดสอบช่องโหว่เพื่อพิสูจน์แค่ concept (PoC) โดยไม่กระทบข้อมูล/บริการของผู้ใช้อื่น
- รายงานตามช่องทางที่ระบุ และร่วมมือแก้ไขตามกำหนด

### ❌ ห้ามทำเด็ดขาด (ถือว่าผิดนโยบาย อาจถูกดำเนินคดี)
- Social engineering, phishing ผู้ใช้หรือ staff
- DDoS / DoS / spam / brute force ที่กระทบ availability
- เข้าถึง / ดึง / แก้ไขข้อมูลของผู้ใช้อื่นโดยไม่ได้รับอนุญาติ
- ติดตั้ง backdoor / persistence / exfiltrate data
- Physical access, malware, ransomware
- เปิดเผยช่องโหว่สู่สาธารณะก่อนหมด coordinated disclosure window

---

## Out of Scope (ไม่รับรายงาน)

- Rate limiting / DoS ที่ไม่กระทบความลับ/ความถูกต้องของข้อมูล
- Missing security headers / banner disclosure / version disclosure หากไม่มี PoC พิสูจน์ผลกระทบ
- Clickjacking / CSRF บน endpoint ที่ไม่เปลี่ยนแปลง state
- ปัญหาที่ต้องมี physical access หรือ malware อยู่บนเครื่องผู้ใช้แล้ว
- Social engineering / phishing (ดู Safe Harbor)
- ช่องโหว่ใน dependency ที่ upstream ยังไม่มี patch (รายงานได้ แต่จะ track ตาม upstream)
- ข้อเสนอแนะด้าน best practice โดยไม่มี PoC พิสูจน์ว่าใช้โจมตีได้จริง

---

## Acknowledgments (Hall of Fame)

ผู้รายงานช่องโหว่ที่ verified จะได้รับการขอบคุณที่หน้านี้:

| ชื่อ / GitHub | ช่องโหว่ | วันที่ |
|---------------|----------|--------|
| (ยังไม่มี) | — | — |

---

*เอกสารฉบับนี้ปรับปรุงครั้งล่าสุด: 2026-10-22*