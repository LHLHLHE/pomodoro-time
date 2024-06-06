DEFAULT_GOAL := help

HOST ?= 127.0.0.1
PORT ?= 8000

run: ## Run the app
	uvicorn main:app --reload --host ${HOST} --port ${PORT} --env-file .env

install: ## Install dependency by poetry
	poetry add ${LIBRARY}

uninstall: ## Uninstall dependency by poetry
	poetry remove ${LIBRARY}

update: ## Update dependency by poetry
	poetry update ${LIBRARY}

help: ## Show this help message
	@echo "Usage: make [command]"
	@echo ""
	@echo "Commands:"
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'