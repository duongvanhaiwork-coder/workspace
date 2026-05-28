.PHONY: setup up down logs health index ide-config sync-ide verify engine-dev worker-dev mcp-dev format

setup:
	./scripts/setup.sh

ide-config:
	./scripts/install-ide-config.sh

link-global:
	./scripts/link-global-ide.sh

sync-ide:
	./scripts/sync-ide.sh

up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f

health:
	@echo "Engine:" && curl -sf http://localhost:8000/api/health | python3 -m json.tool || echo "FAIL"
	@echo "MCP:" && curl -sf http://localhost:3000/health | python3 -m json.tool || echo "FAIL"

index:
	./scripts/index-all.sh

verify:
	./scripts/verify.sh

mcp-dev:
	cd mcp-server && npm run dev

engine-dev:
	cd intelligence-engine && uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

worker-dev:
	cd intelligence-engine && python -m src.tasks.worker

format:
	cd intelligence-engine && python -m ruff check src --fix || true
	cd mcp-server && npm run build
