# Graphiti Agent Demo with LM Studio

Here we demonstrate the power of Graphiti, a temporal knowledge graph solution that enables AI agents to maintain and query evolving knowledge over time. This implementation showcases how to use Graphiti with Pydantic AI and **LM Studio** to build intelligent agents that can reason about changing facts using local LLMs.

## Overview

This demo includes four main components:

1. **Quickstart Example**: A comprehensive tutorial demonstrating Graphiti's core features including hybrid search, center node search, and node retrieval.
2. **Agent Interface**: A conversational agent powered by Pydantic AI that can search and query the Graphiti knowledge graph using LM Studio models.
3. **LLM Evolution Demo**: A simulation showing how knowledge evolves over time, with three phases of LLM development that update the knowledge graph.
4. **Connection Tests**: Utility scripts to verify LM Studio connection and test basic functionality.

## Prerequisites

- Python 3.10 or higher
- Neo4j 5.26 or higher (for storing the knowledge graph)
- **LM Studio** (for local LLM inference and embedding)

## Installation

### 1. Install uv (recommended)

[uv](https://docs.astral.sh/uv/) is a fast Python package installer and resolver:

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh  # Unix/macOS
# or
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"  # Windows
```

### 2. Set up the project

```bash
# Clone the repository
git clone https://github.com/LaansDole/graphiti-lmstudio.git
cd graphiti-lmstudio

# Install dependencies and create virtual environment
uv sync

# Activate the virtual environment
source .venv/bin/activate  # Unix/macOS
# or
.venv\Scripts\activate     # Windows
```

### 3. Set up LM Studio

Download and install [LM Studio](https://lmstudio.ai/) to run local LLMs:

1. Download and install LM Studio from the official website
2. Launch LM Studio and download a model (recommended: any OpenAI-compatible model)
3. Start the local server by going to the "Local Server" tab
4. Configure the server settings and start it (default: `http://localhost:1234`)
5. Make sure to enable CORS if needed for your setup

### 4. Set up Neo4j

1. Download and install [Neo4j Desktop](https://neo4j.com/download/)
2. Create a new project and add a local DBMS
3. Start the DBMS and set a password
4. Note the connection details (URI, username, password)

### 5. Configure environment variables

Create a `.env` file in the project root with the following variables:

```bash
# Neo4j Connection
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password

# LM Studio Configuration
LMSTUDIO_API_HOST=http://127.0.0.1:1234/v1
LMSTUDIO_API_KEY=lm-studio
MODEL_CHOICE=llama-3.2-1b-instruct

# Configure LM Studio as OpenAI-compatible API for Graphiti
OPENAI_API_KEY=lm-studio
OPENAI_BASE_URL=http://localhost:1234/v1

# Configure embedding model for LM Studio
OPENAI_EMBEDDING_MODEL=text-embedding-nomic-embed-text-v1.5
```

## Running the Demo

### Quick Start with Makefile

This project includes a Makefile for easy command execution:

```bash
# View all available commands
make help

# Install dependencies
make install

# Test LM Studio connection (recommended first step)
make test-connection

# Run the quickstart tutorial
make demo-quickstart

# Run the evolution demo (WARNING: clears Neo4j database)
make demo-evolution

# Run the conversational agent
make demo-agent
```

## Demo Workflow

For the best demonstration experience:

1. **Setup**: `make install` and ensure LM Studio is running
2. **Test**: `make test-connection` to verify everything works
3. **Terminal 1**: `make demo-evolution` and complete Phase 1
4. **Terminal 2**: `make demo-agent` and ask "Which is the best LLM?"
5. **Terminal 1**: Continue to Phase 2 by typing "continue"
6. **Terminal 2**: Ask the same question again to see updated knowledge
7. **Terminal 1**: Continue to Phase 3
8. **Terminal 2**: Ask "Are LLMs still relevant?" to see the final evolution

This workflow demonstrates how Graphiti maintains temporal knowledge and how the agent's responses adapt to the changing knowledge graph.

## Key Features

- **Local LLM Integration**: Uses LM Studio for private, local LLM inference
- **Temporal Knowledge**: Graphiti tracks when facts become valid and invalid
- **Hybrid Search**: Combines semantic similarity and BM25 text retrieval
- **Context-Aware Queries**: Reranks results based on graph distance
- **Structured Data Support**: Works with both text and JSON episodes
- **Easy Integration**: Seamlessly works with Pydantic AI for agent development
- **Connection Testing**: Built-in utilities to verify LM Studio connectivity

## Troubleshooting

### LM Studio Issues

If you encounter connection issues with LM Studio:

1. **Server not running**: Ensure LM Studio is open and the server is started
2. **Model not loaded**: Load a model in LM Studio or enable just-in-time loading
3. **Port conflicts**: Check if port 1234 is available or change the port in settings
4. **CORS issues**: Enable CORS in LM Studio server settings if needed
5. **Model compatibility**: Ensure the model supports chat completions

### Neo4j Issues

If you encounter Neo4j connection issues:

1. **Database not running**: Ensure Neo4j Desktop is running with an active database
2. **Connection refused**: Check the URI, username, and password in your `.env` file
3. **Authentication failed**: Verify your Neo4j credentials
4. **Memory issues**: Increase Neo4j memory allocation if working with large datasets

## Additional Resources

- [Graphiti Documentation](https://help.getzep.com/graphiti/graphiti/overview)
- [Pydantic AI Documentation](https://ai.pydantic.dev/)
- [LM Studio Documentation](https://lmstudio.ai/docs)
- [Neo4j Documentation](https://neo4j.com/docs/)

## License

This project includes code from Zep Software, Inc. under the Apache License 2.0.
