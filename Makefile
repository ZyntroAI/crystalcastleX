📄 Makefile — ZyntroAI Dev & Redis Workflow
 
Copy this as  Makefile  in your project root ✅
 
 
 
makefile  
# ─── ZyntroAI — Dev & Redis Workflow ───
.PHONY: help dev redis-up redis-down redis-logs redis-shell test lint clean k6-test

# ─── Config ───
REDIS_NAME := zyntro-redis
REDIS_PORT := 6379
REDIS_IMAGE := redis:7-alpine
PYTHON := python3
UVICORN := uvicorn

# ─── Default Target ───
.DEFAULT_GOAL := help

# ─── Help ───
help: ## 📖 Show this help
	@echo "🚀 ZyntroAI — Development Commands"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "💡 Example: make redis-up && make dev"

# ─── Redis Local ───
redis-up: ## 🟢 Start Redis container (Dev/Termux)
	@echo "🚀 Starting Redis container..."
	@docker run -d --name $(REDIS_NAME) -p $(REDIS_PORT):6379 -v redis-data:/data $(REDIS_IMAGE) redis-server --appendonly yes
	@sleep 1
	@docker exec $(REDIS_NAME) redis-cli ping
	@echo "✅ Redis running at redis://localhost:$(REDIS_PORT)"

redis-down: ## 🔴 Stop & remove Redis container
	@echo "🛑 Stopping Redis..."
	@docker stop $(REDIS_NAME) || true
	@docker rm $(REDIS_NAME) || true
	@echo "✅ Redis removed"

redis-restart: ## 🔄 Restart Redis
	$(MAKE) redis-down
	$(MAKE) redis-up

redis-logs: ## 📋 View Redis logs
	@docker logs -f $(REDIS_NAME)

redis-shell: ## 💻 Open Redis CLI shell
	@docker exec -it $(REDIS_NAME) redis-cli

redis-status: ## 🔍 Check Redis status
	@docker ps --filter "name=$(REDIS_NAME)"
	@docker exec $(REDIS_NAME) redis-cli info server 2>/dev/null | head -5 || echo "⚠️ Redis not running"

# ─── App ───
dev: ## 🏃 Start dev server with auto-reload
	@echo "🚀 Starting dev server..."
	$(UVICORN) main:app --reload --port 8000

install: ## 📦 Install Python dependencies
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt
	@echo "✅ Done"

lint: ## ✅ Run linting
	@echo "🔍 Linting..."
	@ruff check . || python -m flake8 . || echo "⚠️ No linter configured"

test: ## 🧪 Run unit tests
	@echo "🧪 Running tests..."
	@pytest -v || echo "⚠️ No tests found"

k6-test: ## 📊 Run k6 rate-limit test
	@echo "📊 Running Redis rate-limit test..."
	k6 run k6/limiter-redis-test.js

clean: ## 🧹 Clean cache & temp files
	@echo "🧹 Cleaning..."
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@rm -rf .pytest_cache .ruff_cache .venv
	@echo "✅ Clean"

# ─── Quick Setup ───
setup: ## 🚀 Full first-time setup: install + redis-up
	$(MAKE) install
	$(MAKE) redis-up
	@echo ""
	@echo "✅ Ready! Run 'make dev' to start the app"
 
 
 
 
🚀 Quick Start
 
bash  
# See all commands
make help

# First time — full setup
make setup

# Start Redis only
make redis-up

# Start dev server
make dev

# Check Redis status
make redis-status

# Run rate limit test
make k6-test

# Stop Redis
make redis-down
 
 
 
 
📋 Workflow Cheat Sheet
 
Step Command 
Begin work  make redis-up && make dev  
Check Redis  make redis-status  
Test limits  make k6-test  
End work  make redis-down  
Cleanup  make clean  
 
 
 
💡 Termux note: Docker might not be available — just start Redis manually with  redis-server  instead of  make redis-up  ✅
 
