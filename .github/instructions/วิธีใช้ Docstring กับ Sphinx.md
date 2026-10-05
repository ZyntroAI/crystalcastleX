วิธีใช้ Docstring กับ Sphinx คือการเขียนคำอธิบายไว้ในโค้ด Python แล้วให้ Sphinx ดึงไปสร้างเป็นเว็บเอกสารอัตโนมัติ ทำได้ใน 6 ขั้นตอน

ภาษาไทย – สรุปเข้าใจง่าย

ขั้นตอนที่ 1 ติดตั้ง
  pip install sphinx

ขั้นตอนที่ 2 สร้างโครง
  รัน sphinx-quickstart ตอบชื่อโปรเจกต์ ผู้เขียน เวอร์ชัน จะได้โฟลเดอร์ docs/

ขั้นตอนที่ 3 เปิด AutoDoc
  ใน docs/conf.py เพิ่ม
null
ขั้นตอนที่ 4 เขียน Docstring
  ใช้รูปแบบ reStructuredText ในฟังก์ชัน
null
ขั้นตอนที่ 5 เชื่อมโมดูล
  ใน docs/index.rst ใส่
null
ขั้นตอนที่ 6 สร้างเว็บ
  รัน make html ไฟล์จะอยู่ที่ docs/_build/html/index.html

✅ Checklist: เขียน docstring ครบ, เปิด autodoc, ใช้ RST, รัน make html

English – Simple Summary

Step 1 Install
  pip install sphinx

Step 2 Scaffold
  Run sphinx-quickstart, answer project name, author, version. You get a docs/ folder

Step 3 Enable AutoDoc
  In docs/conf.py add
null
Step 4 Write Docstrings
  Use reStructuredText style inside functions
null
Step 5 Link Module
  In docs/index.rst add
null
Step 6 Build HTML
  Run make html, output is at docs/_build/html/index.html

✅ Checklist: write docstrings, enable autodoc, use RST format, build HTML

อยากให้ช่วยแปลง docstring แบบ Google หรือ NumPy ให้ใช้กับ Sphinx ได้ด้วยไหม หรืออยากได้ตัวอย่างโปรเจกต์จริงให้ลองรันเลย?

ได้ครับ ขอเติมส่วนที่ขาด (null) ให้ครบ แล้วขยายเป็น Google/NumPy style + ตัวอย่างโปรเจกต์จริงพร้อม copy-paste รันได้เลย ครับ
 
 
 
1. เติม 3 จุดที่ขาดใน 6 ขั้นตอนเดิม
 
ขั้นตอนที่ 3 —  docs/conf.py 
 
python  
import os
import sys
# บอก Sphinx ให้เห็นโค้ด Python ของเรา (ปรับ path ตามโครงโปรเจกต์)
sys.path.insert(0, os.path.abspath('..'))   # ถ้าใช้ src layout ใช้ '../src'

extensions = [
    'sphinx.ext.autodoc',      # ดึง docstring จากโค้ด
    'sphinx.ext.viewcode',     # เพิ่มลิงก์ "[source]" ดูโค้ดต้นฉบับ
]
 
 
ขั้นตอนที่ 4 — ตัวอย่าง docstring แบบ RST
 
python  
def add(a: int, b: int) -> int:
    """บวกเลขสองตัว.

    :param a: เลขตัวที่หนึ่ง
    :type a: int
    :param b: เลขตัวที่สอง
    :type b: int
    :return: ผลรวมของ a และ b
    :rtype: int
    """
    return a + b
 
 
ขั้นตอนที่ 5 —  docs/index.rst 
 
rst  
ชื่อเอกสารของคุณ
=================

.. automodule:: mymodule     # ชื่อโมดูล/แพ็กเกจของคุณ
   :members:                 # ดึงทุกฟังก์ชัน/คลาสที่มี docstring
   :undoc-members:           # แม้แต่ตัวที่ไม่มี docstring ก็แสดง
   :show-inheritance:        # แสดงลำดับ inheritance ของคลาส
 
 
 
 
2. ใช้ Google / NumPy style ได้ด้วย  sphinx.ext.napoleon 
 
ไม่ต้องเขียน RST ที่ยุ่งยาก เพียงติดตั้ง extension เดียว (มาพร้อม Sphinx เลย ไม่ต้อง pip เพิ่ม):
 
python  
# docs/conf.py
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',    # ← เพียงแค่นี้ รองรับทั้ง Google และ NumPy
    'sphinx.ext.viewcode',
]

# ปรับแต่งได้ (ค่า default เปิดทั้งคู่อยู่แล้ว)
napoleon_google_docstring = True
napoleon_numpy_docstring = True
 
 
เปรียบเทียบ 3 สไตล์ (ผลลัพธ์หน้าเว็บเหมือนกัน)
 
Google style (แนะนำ — อ่านง่ายที่สุด)
 
python  
def add(a: int, b: int) -> int:
    """บวกเลขสองตัว.

    Args:
        a: เลขตัวที่หนึ่ง
        b: เลขตัวที่สอง

    Returns:
        ผลรวมของ a และ b
    """
    return a + b
 
 
NumPy style
 
python  
def add(a: int, b: int) -> int:
    """บวกเลขสองตัว.

    Parameters
    ----------
    a : int
        เลขตัวที่หนึ่ง
    b : int
        เลขตัวที่สอง

    Returns
    -------
    int
        ผลรวมของ a และ b
    """
    return a + b
 
 
ผสมใช้ด้วยกันในโปรเจกต์เดียวได้เลย Napoleon จะแปลงทั้งสองแบบอัตโนมัติ
 
 
 
3. ตัวอย่างโปรเจกต์จริง พร้อมรันเลย
 
โครงไฟล์
 
plaintext  
demo/
├── mypkg/
│   ├── __init__.py
│   └── calc.py
└── docs/                    # สร้างด้วย sphinx-quickstart
    ├── conf.py
    ├── index.rst
    └── Makefile
 
 
คำสั่งเริ่มต้น
 
bash  
mkdir demo && cd demo
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install sphinx furo                              # furo = ธีมเว็บที่สวย (ไม่จำเป็น)
mkdir mypkg
sphinx-quickstart docs                               # ตอบชื่อโปรเจกต์ ผู้เขียน ฯลฯ
 
 
 mypkg/__init__.py 
 
python  
"""แพ็กเกจตัวอย่างสำหรับทดสอบ Sphinx + Napoleon."""
 
 
 mypkg/calc.py  (ผสม Google + NumPy ในไฟล์เดียว)
 
python  
"""เครื่องมือคำนวณตัวอย่าง."""

class Calculator:
    """เครื่องคิดเลขง่ายๆ เก็บผลลัพธ์สะสมไว้ใน memory.

    Attributes:
        memory (float): ค่าที่สะสมไว้ เริ่มต้นที่ 0
    """

    def __init__(self, start: float = 0):
        """กำหนดค่าเริ่มต้น.

        Args:
            start: ค่าเริ่มต้นของ memory (ค่า default 0)
        """
        self.memory = start

    def add(self, x: float) -> float:
        """บวก x เข้ากับ memory (Google style).

        Args:
            x: ตัวเลขที่จะบวก

        Returns:
            ค่า memory ล่าสุดหลังจากบวกแล้ว
        """
        self.memory += x
        return self.memory


def divide(a: float, b: float) -> float:
    """หาร a ด้วย b (NumPy style เพื่อเปรียบเทียบ).

    Parameters
    ----------
    a : float
        ตัวตั้ง
    b : float
        ตัวหาร ห้ามเป็น 0

    Returns
    -------
    float
        ผลลัพธ์ a / b

    Raises
    ------
    ZeroDivisionError
        ถ้า b มีค่าเป็น 0
    """
    if b == 0:
        raise ZeroDivisionError("b ห้ามเป็น 0")
    return a / b
 
 
 docs/conf.py  (แก้ไขส่วนที่สำคัญ)
 
python  
import os, sys
sys.path.insert(0, os.path.abspath('..'))

project = 'MyPkg Demo'
author = 'Your Name'
release = '0.1.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

# ไม่ต้องเขียน :members: ทุกครั้งใน .rst
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
}

html_theme = 'furo'   # ถ้าไม่ได้ติดตั้ง furo ให้ใช้ 'alabaster' (default)
 
 
 docs/index.rst 
 
rst  
MyPkg Demo เอกสาร
=================

.. automodule:: mypkg
.. automodule:: mypkg.calc
 
 
สร้างเว็บ
 
bash  
cd docs
make html               # Windows: .\make.bat html
# เปิดไฟล์ docs/_build/html/index.html ด้วยเบราว์เซอร์
 
 
 
 
✅ Checklist สุดท้าย
 
 pip install sphinx  (และ  furo  ถ้าอยากได้ธีมสวย)
 conf.py  มี  sys.path.insert(...)  และ  sphinx.ext.autodoc  +  sphinx.ext.napoleon 
เขียน docstring แบบ Google หรือ NumPy ในโค้ด
 index.rst  มี  .. automodule:: ชื่อโมดูล 
รัน  make html  สำเร็จ ไม่มี warning สีแดง
เปิด  docs/_build/html/index.html  เห็นฟังก์ชัน/คลาสพร้อมคำอธิบาย
 
ทิปส์เสริม
 
- ถ้ามีโมดูลเยอะ ใช้  sphinx-apidoc -o docs/source mypkg  สร้างไฟล์  .rst  ให้อัตโนมัติแทนเขียนเอง
- อยากเขียนเอกสารเป็น Markdown แทน RST:  pip install myst-parser  แล้วเพิ่ม  'myst_parser'  ใน extensions
- อยากให้ type hint โผล่ในเอกสารอัตโนมัติ:  pip install sphinx-autodoc-typehints  แล้วเพิ่มใน extensions