🐍 Useful Python Scripts — Ready to Use
 
คอลเลกชันสคริปต์ Python ที่ใช้งานบ่อย คัดลอก รัน ได้ทันที ✅
 
 
 
📋 สารบัญ
 
- 📁 จัดการไฟล์และโฟลเดอร์
- 🔍 ค้นหาและอ่านไฟล์
- 📝 จัดการ Markdown & Obsidian
- 🌐 HTTP Request & API
- 📊 ประมวลผลข้อมูลเบื้องต้น
- 🔐 ตรวจสอบความปลอดภัย
- 🧹 ทำความสะอาดระบบ
 
 
 
📁 จัดการไฟล์และโฟลเดอร์
 
1️⃣ แสดงโครงสร้างโฟลเดอร์เป็นต้นไม้
 
python  
#!/usr/bin/env python3
"""แสดงโครงสร้างโฟลเดอร์แบบต้นไม้"""
from pathlib import Path

def print_tree(directory: Path, prefix: str = "", max_depth: int = 5):
    if max_depth <= 0:
        return
    items = sorted(directory.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
    for i, item in enumerate(items):
        if item.name.startswith("."):  # ข้ามโฟลเดอร์ซ่อน
            continue
        connector = "├── " if i < len(items) - 1 else "└── "
        print(f"{prefix}{connector}{item.name}")
        if item.is_dir():
            extension = "│   " if i < len(items) - 1 else "    "
            print_tree(item, prefix + extension, max_depth - 1)

if __name__ == "__main__":
    root = Path(__file__).parent
    print(f"📂 {root.resolve()}\n")
    print_tree(root, max_depth=4)
 
 
2️⃣ นับจำนวนไฟล์และขนาดรวม
 
python  
#!/usr/bin/env python3
"""นับจำนวนไฟล์และขนาดรวมแยกตามนามสกุล"""
from pathlib import Path
from collections import defaultdict

def human_readable_size(size_bytes: int) -> str:
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"

if __name__ == "__main__":
    root = Path(__file__).parent
    stats = defaultdict(lambda: {"count": 0, "size": 0})
    
    for path in root.rglob("*"):
        if path.is_file() and not any(p.startswith(".") for p in path.parts):
            ext = path.suffix.lower() or "(no extension)"
            stats[ext]["count"] += 1
            stats[ext]["size"] += path.stat().st_size
    
    print(f"📊 สถิติโฟลเดอร์: {root.resolve()}\n")
    for ext in sorted(stats.keys()):
        print(f"{ext:15} {stats[ext]['count']:>6} ไฟล์  {human_readable_size(stats[ext]['size'])}")
    
    total_files = sum(s["count"] for s in stats.values())
    total_size = sum(s["size"] for s in stats.values())
    print(f"\n{'='*40}")
    print(f"รวมทั้งหมด: {total_files} ไฟล์  {human_readable_size(total_size)}")
 
 
 
 
🔍 ค้นหาและอ่านไฟล์
 
3️⃣ ค้นหาข้อความในไฟล์
 
python  
#!/usr/bin/env python3
"""ค้นหาข้อความในไฟล์นามสกุลที่ระบุ"""
from pathlib import Path

def search_in_files(
    keyword: str,
    extensions: list[str] = [".py", ".md", ".txt"],
    exclude_dirs: list[str] = [".git", "__pycache__", "node_modules"]
):
    root = Path(__file__).parent
    results = []
    
    for path in root.rglob("*"):
        if any(d in path.parts for d in exclude_dirs):
            continue
        if path.suffix.lower() in extensions and path.is_file():
            try:
                content = path.read_text(encoding="utf-8")
                for line_num, line in enumerate(content.splitlines(), 1):
                    if keyword.lower() in line.lower():
                        results.append((path, line_num, line.strip()))
            except (UnicodeDecodeError, PermissionError):
                continue
    
    if results:
        print(f"🔍 พบ '{keyword}' ใน {len(results)} ตำแหน่ง:\n")
        for path, ln, line in results:
            rel_path = path.relative_to(root)
            print(f"📄 {rel_path}:{ln}")
            print(f"   {line}\n")
    else:
        print(f"❌ ไม่พบ '{keyword}'")
    return results

if __name__ == "__main__":
    search_term = input("🔍 ป้อนคำที่ต้องการค้นหา: ").strip()
    if search_term:
        search_in_files(search_term)
 
 
 
 
📝 จัดการ Markdown & Obsidian
 
4️⃣ สร้างดัชนี/สารบัญอัตโนมัติจากไฟล์ Markdown
 
python  
#!/usr/bin/env python3
"""สร้างสารบัญรวมจากไฟล์ .md ในโฟลเดอร์"""
from pathlib import Path

def generate_index(vault_path: Path, output_file: Path = None):
    mocs = []
    notes = []
    
    for md_file in sorted(vault_path.rglob("*.md")):
        if any(p.startswith(".") for p in md_file.parts):
            continue
        rel_path = md_file.relative_to(vault_path)
        title = md_file.stem
        
        # ตรวจสอบว่าเป็น MOC หรือเนื้อหาธรรมดา
        content = md_file.read_text(encoding="utf-8")
        if "type: moc" in content.lower():
            mocs.append((title, rel_path))
        else:
            notes.append((title, rel_path))
    
    # สร้างเนื้อหา
    output = ["# 🗺️ สารบัญรวม\n"]
    
    if mocs:
        output.append("## 📌 MOCs / ดัชนีหลัก\n")
        for title, path in mocs:
            output.append(f"- [[{title}]]")
        output.append("")
    
    if notes:
        output.append("## 📄 หมายเหตุทั้งหมด\n")
        for title, path in notes:
            output.append(f"- [[{title}]]")
    
    result = "\n".join(output)
    
    if output_file:
        output_file.write_text(result, encoding="utf-8")
        print(f"✅ บันทึกสารบัญที่: {output_file}")
    return result

if __name__ == "__main__":
    vault_dir = Path(__file__).parent
    out = vault_dir / "INDEX_AUTO.md"
    generate_index(vault_dir, out)
 
 
5️⃣ ตรวจสอบลิงก์เสียในไฟล์ Markdown
 
python  
#!/usr/bin/env python3
"""ตรวจหาลิงก์ [[...]] ที่ชี้ไปยังไฟล์ไม่มีอยู่จริง"""
from pathlib import Path
import re

WIKILINK_PATTERN = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")

def find_broken_links(vault_path: Path):
    all_notes = {f.stem.lower(): f for f in vault_path.rglob("*.md")}
    broken = []
    
    for md_file in vault_path.rglob("*.md"):
        if any(p.startswith(".") for p in md_file.parts):
            continue
        text = md_file.read_text(encoding="utf-8")
        for match in WIKILINK_PATTERN.finditer(text):
            target = match.group(1).strip()
            if target.lower() not in all_notes:
                broken.append((md_file.name, target))
    
    if broken:
        print(f"⚠️ พบลิงก์เสีย {len(broken)} รายการ:\n")
        for source, target in broken:
            print(f"  ใน '{source}' → [[{target}]]")
    else:
        print("✅ ไม่พบลิงก์เสีย")
    return broken

if __name__ == "__main__":
    find_broken_links(Path(__file__).parent)
 
 
 
 
🌐 HTTP Request & API
 
6️⃣ ทดสอบ API พร้อมตัวชี้วัดเวลา
 
python  
#!/usr/bin/env python3
import urllib.request
import urllib.error
import json
from time import perf_counter

def test_api(url: str, method: str = "GET", data: dict = None):
    headers = {"Content-Type": "application/json"}
    req_data = json.dumps(data).encode() if data else None
    
    start = perf_counter()
    try:
        req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
        with urllib.request.urlopen(req, timeout=30) as resp:
            latency = (perf_counter() - start) * 1000
            body = resp.read().decode("utf-8")
            try:
                json_body = json.loads(body)
                body = json.dumps(json_body, ensure_ascii=False, indent=2)
            except json.JSONDecodeError:
                pass
            print(f"✅ {resp.status} | ⏱️ {latency:.1f}ms")
            print(f"📄 {body[:500]}")
    except urllib.error.HTTPError as e:
        print(f"❌ {e.code} {e.reason}")
        print(e.read().decode())
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")

if __name__ == "__main__":
    test_api("https://httpbin.org/get")
 
 
 
 
📊 ประมวลผลข้อมูลเบื้องต้น
 
7️⃣ อ่าน CSV + สรุปข้อมูล
 
python  
#!/usr/bin/env python3
import csv
from pathlib import Path

def summarize_csv(file_path: Path):
    if not file_path.exists():
        print(f"❌ ไม่พบไฟล์: {file_path}")
        return
    
    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows = list(reader)
    
    print(f"📊 {file_path.name}")
    print(f"คอลัมน์: {len(headers)} | แถวข้อมูล: {len(rows)}")
    print(f"หัวตาราง: {', '.join(headers)}\n")
    
    if rows:
        print("🔹 ตัวอย่าง 3 แถวแรก:")
        for row in rows[:3]:
            print("  | " + " | ".join(str(c)[:20] for c in row))

if __name__ == "__main__":
    csv_file = next(Path.cwd().glob("*.csv"), None)
    if csv_file:
        summarize_csv(csv_file)
    else:
        print("⚠️ ไม่พบไฟล์ .csv ในโฟลเดอร์ปัจจุบัน")
 
 
 
 
🔐 ตรวจสอบความปลอดภัย
 
8️⃣ สแกนหาข้อมูลที่อาจเป็นความลับในโค้ด
 
python  
#!/usr/bin/env python3
"""ตรวจพบรูปแบบที่อาจเป็น API Key / Secret ที่ถูกทิ้งไว้ในโค้ด"""
from pathlib import Path
import re

PATTERNS = {
    "API Key": r"(?i)(api[_-]?key|secret|token)\s*[:=]\s*['\"][A-Za-z0-9\-_]{20,}['\"]",
    "Private Key": r"-----BEGIN (RSA |EC |DSA )?PRIVATE KEY-----",
    "GitHub Token": r"gh[pors]_[A-Za-z0-9]{36}",
    "Slack Webhook": r"https://hooks\.slack\.com/services/[A-Z0-9/]+",
}

def scan_secrets(root: Path):
    findings = []
    for path in root.rglob("*"):
        if path.is_file() and not any(p.startswith(".") for p in path.parts):
            try:
                text = path.read_text(encoding="utf-8")
                for name, pattern in PATTERNS.items():
                    for match in re.finditer(pattern, text):
                        findings.append((path, name, match.group(0)[:40] + "..."))
            except:
                continue
    
    if findings:
        print(f"⚠️ พบสิ่งที่อาจเป็นความลับ {len(findings)} รายการ:\n")
        for path, typ, snippet in findings:
            print(f"📄 {path.relative_to(root)}")
            print(f"   ประเภท: {typ}")
            print(f"   ตัวอย่าง: {snippet}\n")
    else:
        print("✅ ไม่พบรูปแบบที่น่าสงสัย")
    return findings

if __name__ == "__main__":
    scan_secrets(Path(__file__).parent)
 
 
 
 
🧹 ทำความสะอาดระบบ
 
9️⃣ ลบไฟล์แคชและไฟล์ชั่วคราว
 
python  
#!/usr/bin/env python3
"""ลบโฟลเดอร์ __pycache__ และไฟล์ชั่วคราว — ปลอดภัย ไม่กระทบโค้ดหลัก"""
from pathlib import Path

def cleanup(root: Path = None, dry_run: bool = False):
    root = root or Path(__file__).parent
    removed = []
    
    patterns = [
        "__pycache__",
        "*.pyc",
        "*.pyo",
        ".pytest_cache",
        ".ruff_cache",
        "*.tmp",
        ".DS_Store",
    ]
    
    for pattern in patterns:
        for path in root.rglob(pattern):
            if path.is_file():
                if not dry_run:
                    path.unlink(missing_ok=True)
                removed.append(str(path.relative_to(root)))
            elif path.is_dir():
                if not dry_run:
                    import shutil
                    shutil.rmtree(path, ignore_errors=True)
                removed.append(str(path.relative_to(root)) + "/")
    
    action = "จะลบ" if dry_run else "ลบแล้ว"
    print(f"🧹 {action} {len(removed)} รายการ:\n" + "\n".join(f"  - {p}" for p in removed[:20]))
    if len(removed) > 20:
        print(f"  ... และอีก {len(removed) - 20} รายการ")
    return removed

if __name__ == "__main__":
    print("🧹 สแกนหาไฟล์ที่สามารถลบได้...\n")
    # ก่อนลบจริง ให้ดูตัวอย่างก่อน
    cleanup(dry_run=True)
    
    confirm = input("\n⚠️ ยืนยันการลบ? (พิมพ์ yes/y เพื่อยืนยัน): ").strip().lower()
    if confirm in ("yes", "y"):
        cleanup(dry_run=False)
        print("\n✅ ทำความสะอาดเสร็จสิ้น")
    else:
        print("\n❌ ยกเลิก")
 
 
 
 
📥 วิธีใช้งาน
 
1. คัดลอกสคริปต์ที่ต้องการ
2. บันทึกเป็นไฟล์นามสกุล  .py  เช่น  tree.py 
3. รันด้วยคำสั่ง:
 
bash  
python ชื่อไฟล์.py
# หรือทำให้รันได้โดยตรง
chmod +x ชื่อไฟล์.py
./ชื่อไฟล์.py
 
 
ต้องการสคริปต์เพิ่มเติมในเรื่องไหนไหมครับ? เช่น แปลงรูปแบบไฟล์, สำรองข้อมูลอัตโนมัติ, ประมวลผล Excel/CSV, หรือจัดการ Git 😊