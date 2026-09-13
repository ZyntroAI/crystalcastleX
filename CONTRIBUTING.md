# Contributing to Crystal Castle X

ขอบคุณที่สนใจร่วมพัฒนา 🙏 คู่มือนี้ครอบคลุมขั้นตอนการตั้งค่า การทดสอบ และ CI/CD

## สิ่งที่ต้องมี

| เครื่องมือ | เวอร์ชัน |
| --- | --- |
| Node.js | 22 (ดู [`.nvmrc`](.nvmrc)) |
| PNPM | 9 (`packageManager` ใน `package.json` กำหนดไว้แล้ว) |
| Python | 3.11+ (เฉพาะงาน Backend) |

```bash
corepack enable          # ให้ pnpm ใช้เวอร์ชันจาก packageManager
pnpm install             # ติดตั้ง dependencies
cp .env.example .env     # แล้วเติมค่าจริง (ห้าม commit .env)
```

## ขั้นตอนการพัฒนา

1. **แตก branch** จาก `main` — ใช้ชื่อสื่อความหมาย เช่น `feat/…`, `fix/…`, `docs/…`
   ```bash
   git checkout -b feat/my-change
   ```
2. **แก้โค้ด** ให้สอดคล้องกับสไตล์เดิมของโปรเจกต์
3. **รันการตรวจสอบในเครื่อง** ก่อน push (ดูหัวข้อถัดไป)
4. **Commit** ด้วยข้อความที่ชัดเจน — repo ใช้ Conventional Commits (`commitlint.config.js`)
   ```bash
   git commit -m "feat(ai): add gemini provider fallback"
   ```
5. **Push และเปิด Pull Request** เข้า `main`

> ⚠️ ห้าม push ตรงเข้า `main` — ทุกการเปลี่ยนแปลงต้องผ่าน Pull Request

## การทดสอบ (Testing)

```bash
pnpm lint            # next lint / ESLint
pnpm type-check      # tsc --noEmit
pnpm test            # vitest run
pnpm coverage        # vitest run --coverage
pnpm build           # ตรวจว่า build ผ่านจริง
```

ถ้ามีการเพิ่มฟีเจอร์ใหม่ ควรมีเทสต์ประกอบด้วย (ดูตัวอย่างใน `__tests__/`)

## CI/CD Pipeline

workflow หลักคือ [`.github/workflows/CrystalCastleCopilot.yml`](.github/workflows/CrystalCastleCopilot.yml)
ทำงานตามลำดับ job ต่อไปนี้:

| Job | หน้าที่ | เงื่อนไข |
| --- | --- | --- |
| `validate` | ตรวจโครงสร้าง repo + lint + type check | ทุก push / PR |
| `ai-tests` | ตรวจคีย์ AI ว่ามีจริง + รัน unit test | หลัง `validate` ผ่าน |
| `build` | build แอปและอัปโหลด artifact | หลัง `validate` + `ai-tests` ผ่าน |
| `security` | `pnpm audit --audit-level high` + gitleaks secret scan | ขนานกัน |
| `deploy-preview` | deploy preview | Pull Request เท่านั้น |
| `deploy-production` | deploy production | push เข้า `main` เท่านั้น + `security` ผ่าน |

### Secrets ที่ต้องตั้งค่าใน repo

| Secret | ใช้ทำอะไร |
| --- | --- |
| `OPENAI_API_KEY` | AI provider หลัก |
| `GEMINI_API_KEY` | AI provider สำรอง |
| `VERCEL_TOKEN` | deploy production |

> ⚠️ `ai-tests` จะ **ล้มเหลว** ถ้าคีย์ AI ไม่ได้ตั้งค่า หรือตั้งเป็นค่า placeholder
> (`your_…_here`, `sk-xxx`, `changeme` ฯลฯ)

### มาตรฐานความปลอดภัยของ Workflow

ทุก workflow ต้องปฏิบัติตามกฎเหล่านี้ (ตรวจในรีวิว PR):

1. **SHA-pin ทุก action** — ใช้ commit SHA 40 ตัว ห้ามใช้แท็ก `@vN` เด็ดขาด
   ```yaml
   uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262 # v4.2.2
   ```
2. **ระบุ `permissions:` เสมอ** — ใช้ least-privilege (ค่าเริ่มต้น `contents: read`)
3. **ห้าม hardcode ความลับ** — ใช้ `${{ secrets.* }}` เท่านั้น
4. **Secret scan** — gitleaks จะสแกนทุก PR ถ้าเจอความลับ CI จะแดง

รายละเอียดนโยบายความปลอดภัยดูที่ [`SECURITY.md`](SECURITY.md)

## Pull Request Checklist

- [ ] รัน `pnpm lint`, `pnpm type-check`, `pnpm test` ผ่านในเครื่องแล้ว
- [ ] ไม่มี action ที่ยังใช้แท็ก `@vN` (ถ้าแก้ workflow)
- [ ] มี `permissions:` ระบุชัดเจน (ถ้าแก้ workflow)
- [ ] ไม่มีคีย์/ความลับในโค้ดที่ commit
- [ ] อัปเดตเอกสารที่เกี่ยวข้อง (README / docs) ถ้าพฤติกรรมเปลี่ยน

## โครงสร้างโปรเจกต์ (ย่อ)

```
CrystalCastleX/
├── app/            # Next.js App Router (api, components, core, studio, dashboard)
├── Backend/        # บริการฝั่งเซิร์ฟเวอร์
├── Package/        # แพ็กเกจ Node (install-crystal action)
├── agent-hub/      # คอนฟิกของ agent
├── docs/           # เอกสารความรู้และสถาปัตยกรรม
└── .github/        # workflows, dependabot, templates
```

## License

ผลงานที่ส่งเข้ามาถือว่าเผยแพร่ภายใต้สัญญาอนุญาต MIT ของโปรเจกต์
