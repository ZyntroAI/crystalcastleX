#!/usr/bin/env python3
"""
เพิ่มข้อความลิขสิทธิ์ที่ส่วนบนของไฟล์โค้ด
ข้ามไฟล์ที่มีหัวข้อนี้อยู่แล้วโดยอัตโนมัติ
"""
from __future__ import annotations
from pathlib import Path
import sys

# ========== CONFIGURATION ==========
COPYRIGHT_TEXT = """Copyright (c) 2026 ZyntroAI
Licensed under the MIT License.
See LICENSE file in the project root for full license information.
"""

TARGET_EXTENSIONS = [".py", ".ts", ".tsx", ".js", ".jsx", ".md"]
EXCLUDE_DIRS = {".git", "__pycache__", "node_modules", "venv", ".venv", "dist", "build"}
# ===================================

HEADER_LINES = COPYRIGHT_TEXT.strip().splitlines()

def make_comment(line: str, ext: str) -> str:
    """แปลงข้อความเป็นรูปแบบความคิดเห็นตามนามสกุลไฟล์"""
    if ext in {".py", ".ts", ".tsx", ".js", ".jsx"}:
        return f"# {line}"
    if ext in {".md"}:
        return f"<!-- {line} -->"
    return f"# {line}"

HEADER = "\n".join(make_comment(line, ext=".py") for line in HEADER_LINES) + "\n\n"

def has_license_header(content: str) -> bool:
    """ตรวจสอบว่าไฟล์มีหัวข้ออยู่แล้วหรือไม่"""
    return "Copyright" in content[:1000] and "MIT License" in content[:1000]

def add_header(file_path: Path, dry_run: bool = False) -> bool:
    """เพิ่มหัวข้อลิขสิทธิ์ให้ไฟล์เดียว"""
    content = file_path.read_text(encoding="utf-8")
    
    if has_license_header(content):
        return False  # มีอยู่แล้ว ข้ามไป
    
    new_content = HEADER + content
    
    if not dry_run:
        file_path.write_text(new_content, encoding="utf-8")
    return True

def process_directory(root: Path, dry_run: bool = False) -> int:
    """ดำเนินการทุกไฟล์ในโฟลเดอร์"""
    count = 0
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(d in path.parts for d in EXCLUDE_DIRS):
            continue
        if path.suffix in TARGET_EXTENSIONS:
            if add_header(path, dry_run=dry_run):
                print(f"✅ เพิ่มลิขสิทธิ์: {path.relative_to(root)}")
                count += 1
    return count

if __name__ == "__main__":
    root = Path(__file__).parent.parent
    dry_run = "--dry-run" in sys.argv
    
    mode = "📋 [ทดสอบ] จะเพิ่ม" if dry_run else "⚡ เพิ่ม"
    print(f"{mode} หัวข้อลิขสิทธิ์ให้ไฟล์ใน: {root.resolve()}\n")
    
    count = process_directory(root, dry_run=dry_run)
    
    print(f"\nเสร็จสิ้น: {count} ไฟล์ได้รับการอัปเดต")
    if dry_run:
        print("นี่เป็นการทดสอบ — ไม่มีการเปลี่ยนแปลงไฟล์จริง")
        print("รันโดยไม่มี --dry-run เพื่อดำเนินการจริง")
