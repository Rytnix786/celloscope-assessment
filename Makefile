.PHONY: test docker-up docker-down lint help

help:
	@echo "Available commands:"
	@echo "  make test       - Run unit and integration test suite"
	@echo "  make docker-up  - Start service via Docker Compose in mock mode"
	@echo "  make docker-down- Stop Docker Compose services"
	@echo "  make lint       - Run layer separation AST audit test"

test:
	python -m pytest tests/ -v

docker-up:
	docker compose up -d --build

docker-down:
	docker compose down

lint:
	python -m pytest tests/test_layer_separation.py -v
