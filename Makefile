.PHONY: all start_api start_frontend start_main

all: start_api start_frontend start_main

start_api:
	@echo "Starting API..."
	cd src/api_system && del logs.json && start cmd /k "uvicorn api:app --reload --host 0.0.0.0 --port 8000"

start_frontend:
	@echo "Starting JS Frontend..."
	cd frontend && start cmd /k "npm run dev"

start_main:
	@echo "Starting Main Project..."
	python -m src.main