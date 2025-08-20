# Graphiti LM Studio Demo Makefile

.PHONY: help install test test-connection demo-quickstart demo-evolution demo-agent clean

help:  ## Show this help message
	@echo "Graphiti LM Studio Demo Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "Demo Workflow:"
	@echo "  1. make install           # Set up the project"
	@echo "  2. make test-connection   # Test LM Studio connection"
	@echo "  3. make demo-evolution    # Run evolution demo (Terminal 1)"
	@echo "  4. make demo-agent        # Run agent interface (Terminal 2)"

install:  ## Install dependencies using uv
	uv sync
	@echo "✅ Installation complete! Activate the virtual environment:"
	@echo "   source .venv/bin/activate  # Unix/macOS"
	@echo "   .venv\\Scripts\\activate     # Windows"

test:  ## Run all tests
	python -m pytest src/graphiti_agent/tests/ -v

test-connection:  ## Test LM Studio connection
	python -c "from graphiti_agent.tests.test_lmstudio_connection import main; main()"

demo-quickstart:  ## Run the Graphiti quickstart tutorial
	cd src && python -m graphiti_agent.quickstart

demo-evolution:  ## Run the LLM evolution demo (WARNING: clears Neo4j database)
	cd src && python -m graphiti_agent.evolution

demo-agent: demo-quickstart ## Run the conversational agent interface
	cd src && python -m graphiti_agent.agent

clean:  ## Clean up temporary files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

dev-install:  ## Install in development mode (editable)
	uv pip install -e .

# Windows-compatible versions
install-win:  ## Install dependencies using uv (Windows)
	uv sync
	@echo "✅ Installation complete! Activate the virtual environment:"
	@echo "   .venv\\Scripts\\activate"

clean-win:  ## Clean up temporary files (Windows)
	@for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
	@del /s /q *.pyc 2>nul
	@for /d /r . %%d in (*.egg-info) do @if exist "%%d" rd /s /q "%%d" 2>nul
