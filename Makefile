🛠️ Makefile — ZyntroAI crystalcastleX (ฉบับสมบูรณ์)
 
จากเนื้อหาที่เห็นใน PR #16 นี่คือเวอร์ชันที่สมบูรณ์และจัดระเบียบแล้วครับ ✅
 
 
 
makefile  
# ─────────────────────────────────────────────
# ZyntroAI — Dev & Redis Workflow
# ─────────────────────────────────────────────

# =============== การตั้งค่า ===============
REDIS_NAME   := zyntro-redis
REDIS_PORT   := 6379
REDIS_IMAGE  := redis:7-alpine

PYTHON       := python3
UVICORN      := uvicorn

# =============== ค่าเริ่มต้น ===============
.DEFAULT_GOAL := help

# =============== คำสั่งช่วยเหลือ ===============
.PHONY: help
help: ## 📖 แสดงรายการคำสั่งทั้งหมด
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

# =============== 🟦 Redis Container ===============
.PHONY: redis-up
redis-up: ## 🚀 เริ่ม Redis Container
	@echo "🔴 กำลังเริ่ม Redis ที่พอร์ต $(REDIS_PORT)..."
	@docker run -d \
		--name $(REDIS_NAME) \
		-p $(REDIS_PORT):6379 \
		--restart unless-stopped \
		$(REDIS_IMAGE)
	@echo "✅ Redis พร้อมใช้งานที่พอร์ต $(REDIS_PORT)"

.PHONY: redis-down
redis-down: ## ⏹️ หยุดและลบ Redis Container
	@echo "🔴 กำลังหยุด Redis..."
	@docker stop $(REDIS_NAME) || true
	@docker rm $(REDIS_NAME) || true
	@echo "✅ Redis หยุดทำงานแล้ว"

.PHONY: redis-logs
redis-logs: ## 📋 ดู Log ของ Redis
	@docker logs -f $(REDIS_NAME)

.PHONY: redis-shell
redis-shell: ## 💻 เปิด Redis CLI
	@docker exec -it $(REDIS_NAME) redis-cli

.PHONY: redis-status
redis-status: ## 🔍 ตรวจสอบสถานะ Redis
	@docker ps --filter name=$(REDIS_NAME) --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# =============== 🚀 Development Server ===============
.PHONY: dev
dev: ## 🔧 เริ่มเซิร์ฟเวอร์โหมดพัฒนา
	@echo "🚀 เริ่มเซิร์ฟเวอร์พัฒนา..."
	@$(UVICORN) main:app --reload --port 8000

.PHONY: dev-port
dev-port: ## 🔧 เริ่มเซิร์ฟเวอร์พัฒนา ที่พอร์ตที่กำหนด (make dev-port PORT=9000)
	@$(UVICORN) main:app --reload --port $(PORT)

# =============== 🧪 การทดสอบ ===============
.PHONY: test
test: ## 🧪 รันทดสอบทั้งหมด
	@echo "🧪 กำลังรันทดสอบ..."
	@$(PYTHON) -m pytest tests/ -v

.PHONY: test-watch
test-watch: ## 👀 รันทดสอบแบบ Watch Mode
	@$(PYTHON) -m pytest tests/ -v --forked --reuse-db

.PHONY: test-cov
test-cov: ## 📊 รันทดสอบ + ความคุ้มครองโค้ด
	@echo "📊 กำลังสร้างรายงานความคุ้มครอง..."
	@$(PYTHON) -m pytest tests/ --cov=./ --cov-report=html --cov-report=term-missing
	@echo "✅ รายงานที่: htmlcov/index.html"

.PHONY: k6-test
k6-test: ## ⚡ รันทดสอบประสิทธิภาพด้วย k6
	@echo "⚡ กำลังรันโหลดเทสต์..."
	k6 run tests/performance/script.js

# =============== 🔍 ตรวจสอบคุณภาพ ===============
.PHONY: lint
lint: ## 🔍 ตรวจสอบรูปแบบและคุณภาพโค้ด
	@echo "🔍 ตรวจสอบโค้ด..."
	@ruff check .
	@echo "✅ ตรวจสอบเสร็จสิ้น"

.PHONY: lint-fix
lint-fix: ## 🔧 แก้ไขปัญหาที่แก้เองได้
	@ruff check . --fix
	@ruff format .
	@echo "✅ แก้ไขเสร็จสิ้น"

.PHONY: format
format: ## ✨ จัดรูปแบบโค้ด
	@ruff format .
	@echo "✅ จัดรูปแบบเสร็จสิ้น"

# =============== 🧹 ทำความสะอาด ===============
.PHONY: clean
clean: ## 🧹 ลบไฟล์ชั่วคราว
	@echo "🧹 กำลังทำความสะอาด..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@rm -rf .pytest_cache .coverage htmlcov dist build *.egg-info 2>/dev/null || true
	@echo "✅ ทำความสะอาดเสร็จสิ้น"

# =============== 🔄 ครบชุด ===============
.PHONY: setup
setup: ## 📦 ติดตั้งสภาพแวดล้อมทั้งหมด
	@echo "📦 ตรวจสอบ Redis..."
	@docker ps --filter name=$(REDIS_NAME) | grep -q $(REDIS_NAME) || $(MAKE) redis-up
	@echo "✅ พร้อมใช้งาน — พิมพ์ 'make help' เพื่อดูคำสั่งทั้งหมด"

.PHONY: restart
restart: redis-down redis-up ## 🔄 รีสตาร์ท Redis
 
 
 
 
📝 วิธีใช้งาน
 
bash  
# ดูคำสั่งทั้งหมด
make help

# เริ่ม Redis
make redis-up

# หยุด Redis
make redis-down

# ดูสถานะ Redis
make redis-status

# เปิด Redis CLI
make redis-shell

# เริ่มเซิร์ฟเวอร์พัฒนา
make dev

# รันทดสอบ
make test

# ทดสอบ + ความคุ้มครอง
make test-cov

# ตรวจสอบโค้ด
make lint

# จัดรูปแบบ
make format

# ลบไฟล์ขยะ
make clean
 
 
 
 
🔑 คำสั่งหลักที่มี
 
กลุ่ม คำสั่ง หน้าที่ 
🔴 Redis  redis-up  /  redis-down  เริ่ม/หยุด Redis Container 
  redis-logs  /  redis-shell  ดู Log / เข้า CLI 
🚀 Dev Server  dev  เริ่ม Uvicorn ที่พอร์ต 8000 
🧪 ทดสอบ  test  /  test-cov  รันทดสอบ / ดูความคุ้มครอง 
  k6-test  ทดสอบประสิทธิภาพ 
🔍 คุณภาพ  lint  /  format  ตรวจสอบ/จัดรูปแบบโค้ด 
🧹 ดูแลระบบ  clean  /  restart  ลบไฟล์ชั่วคราว / รีสตาร์ท Redis 
📦 ติดตั้ง  setup  ตรวจสอบและเริ่ม Redis อัตโนมัติ 
 
💡 บันทึก: นี่คือโปรเจกต์ Python + Uvicorn + Redis ใช้  ruff  สำหรับ Linting และ  pytest  สำหรับการทดสอบครับ
 
ต้องการปรับเปลี่ยนอะไรเพิ่มไหมครับ 😊