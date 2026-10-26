#!/usr/bin/env python3
"""
ตรวจสอบไฟล์โค้ดที่ยังไม่มีหัวข้อลิขสิทธิ์
ใช้ใน CI/CD เพื่อป้องกันไฟล์ใหม่ที่ลืมใส่ลิขสิทธิ์
"""
from __future__ import annotations
from pathlib import Path
import sys

# ========== CONFIGURATION ==========
TARGET_EXTENSIONS = [".py", ".ts", ".tsx", ".js", ".jsx"]
EXCLUDE_DIRS = {".git", "__pycache__", "node_modules", "venv", ".venv", "dist", "build"}
CHECK_KEYWORDS = ["Copyright", "License"]
# ===================================

def missing_license(file_path: Path) -> bool:
    """ตรวจสอบว่าไฟล์ขาดหัวข้อลิขสิทธิ์หรือไม่"""
    try:
        content = file_path.read_text(encoding="utf-8")[:1500]
        return not all(keyword in content for keyword in CHECK_KEYWORDS)
    except (UnicodeDecodeError, PermissionError):
        return False  # ข้ามไฟล์ที่อ่านไม่ได้

def scan_directory(root: Path) -> list[Path]:
    """สแกนทั้งโฟลเดอร์ คืนรายการไฟล์ที่ขาดลิขสิทธิ์"""
    missing = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(d in path.parts for d in EXCLUDE_DIRS):
            continue
        if path.suffix in TARGET_EXTENSIONS and missing_license(path):
            missing.append(path.relative_to(root))
    return missing

if __name__ == "__main__":
    root = Path(__file__).parent.parent
    missing_files = scan_directory(root)
    
    if missing_files:
        print(f"⚠️ พบ {len(missing_files)} ไฟล์ที่ยังไม่มีหัวข้อลิขสิทธิ์:\n")
        for f in missing_files:
            print(f"  ❌ {f}")
        print(f"\n💡 รัน 'python scripts/add_license_header.py' เพื่อเพิ่มให้อัตโนมัติ")
        sys.exit(1)  # ไม่ผ่าน — สำหรับ CI/CD
    else:
        print("✅ ทุกไฟล์มีหัวข้อลิขสิทธิ์ครบถ้วน")
        sys.exit(0)
