.PHONY: dev up down api-test api-lint web-install web-dev web-build

up:
	docker compose up --build

down:
	docker compose down

api-test:
	cd apps/api && python -m pytest

api-lint:
	cd apps/api && ruff check app tests && mypy app

web-install:
	cd apps/web && npm install

web-dev:
	cd apps/web && npm run dev

web-build:
	cd apps/web && npm run build
