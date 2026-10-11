#!/usr/bin/env bash
set -euo pipefail

# 📝 AI Commit — Generate Diff & Message

# 1. แสดงการเปลี่ยนแปลง
echo "🔍 กำลังรวบรวมการเปลี่ยนแปลง..."
git status --short

# 2. สร้าง Diff
echo ""
echo "📄 สร้าง Diff..."
git diff --staged > .git/ai-staged.diff
git diff >> .git/ai-unstaged.diff

# 3. แสดงสรุป
echo ""
echo "📊 สรุปการเปลี่ยนแปลง:"
echo "  ไฟล์ที่เปลี่ยน: $(git diff --staged --name-only | wc -l)"
echo "  บรรทัดเพิ่ม:    $(git diff --staged --numstat | awk '{sum += $1} END {print sum}')"
echo "  บรรทัดลบ:    $(git diff --staged --numstat | awk '{sum += $2} END {print sum}')"

# 4. ตัวอย่าง Prompt ส่งให้ AI
cat << 'PROMPT'

══════════════════════════════════════════
🤖 ส่งข้อความนี้ให้ AI เพื่อสร้างข้อความ Commit
══════════════════════════════════════════

ฉันมีการเปลี่ยนแปลงดังนี้:

---
\`\`\`diff
PROMPT
cat .git/ai-staged.diff
cat << 'PROMPT'
\`\`\`

กรุณาสร้างข้อความ Commit ตามรูปแบบ Conventional Commits:

<ประเภท>: <หัวข้อสั้นๆ ไม่เกิน 50 ตัวอักษร>

- รายละเอียดการเปลี่ยนแปลงที่ 1
- รายละเอียดการเปลี่ยนแปลงที่ 2

ประเภท: feat, fix, docs, style, refactor, test, chore, ci, perf
PROMPT

echo ""
echo "✅ Diff บันทึกที่: .git/ai-staged.diff"
