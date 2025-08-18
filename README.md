# Graphiti Agent Demo with LM Studio

Here we demonstrate the power of Graphiti, a temporal knowledge graph solution that enables AI agents to maintain and query evolving knowledge over time. This implementation showcases how to use Graphiti with Pydantic AI and **LM Studio** to build intelligent agents that can reason about changing facts using local LLMs.

## Overview

This demo includes four main components:

1. **Quickstart Example (`quickstart.py`)**: A comprehensive tutorial demonstrating Graphiti's core features including hybrid search, center node search, and node retrieval.
2. **Agent Interface (`agent.py`)**: A conversational agent powered by Pydantic AI that can search and query the Graphiti knowledge graph using LM Studio models.
3. **LLM Evolution Demo (`llm_evolution.py`)**: A simulation showing how knowledge evolves over time, with three phases of LLM development that update the knowledge graph.
4. **Connection Test (`test_lmstudio_connection.py`)**: A utility script to verify LM Studio connection and test basic functionality.

## Prerequisites

- Python 3.10 or higher
- Neo4j 5.26 or higher (for storing the knowledge graph)
- **LM Studio** (for local LLM inference and embedding)
- **OpenAI API key** (for Graphiti's embedding functionality)

## Installation

### 1. Set up a virtual environment

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up LM Studio

Download and install [LM Studio](https://lmstudio.ai/) to run local LLMs:

1. Download and install LM Studio from the official website
2. Launch LM Studio and download a model (recommended: any OpenAI-compatible model)
3. Start the local server by going to the "Local Server" tab
4. Configure the server settings and start it (default: `http://localhost:1234`)
5. Make sure to enable CORS if needed for your setup

### 4. Set up Neo4j

You have a couple easy options for setting up Neo4j:

#### Option A: Using Local-AI-Packaged (Simplified setup)
1. Clone the repository: `git clone https://github.com/coleam00/local-ai-packaged`
2. Follow the installation instructions to set up Neo4j through the package
3. Note the username and password you set in .env and the URI will be bolt://localhost:7687

#### Option B: Using Neo4j Desktop
1. Download and install [Neo4j Desktop](https://neo4j.com/download/)
2. Create a new project and add a local DBMS
3. Start the DBMS and set a password
4. Note the connection details (URI, username, password)

### 5. Configure environment variables

Create a `.env` file in the project root with the following variables:

```
# Neo4j Connection
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password

# LM Studio Configuration
LMSTUDIO_API_HOST=http://127.0.0.1:1234/v1
LMSTUDIO_API_KEY=lm-studio
MODEL_CHOICE=openai/gpt-oss-20b

# OpenAI API (required for Graphiti embeddings)
OPENAI_API_KEY=your_openai_api_key
```

## Running the Demo

### 0. Test LM Studio Connection (Recommended First Step)

Before running the main demos, test your LM Studio connection:

```bash
python test_lmstudio_connection.py
```

This will verify:
- LM Studio server is running and accessible
- Models are available
- Basic chat completion functionality works

### 1. Run the Quickstart Example

To get familiar with Graphiti's core features:

```bash
python quickstart.py
```

This will demonstrate:
- Adding episodes to the knowledge graph
- Performing hybrid searches (semantic + BM25)
- Using center node search for context-aware results
- Utilizing search recipes for node retrieval

### 3. Experience the Power of Temporal Knowledge

To see how knowledge evolves over time, run the LLM evolution demo in one terminal:

```bash
python llm_evolution.py
```

**⚠️ WARNING: Running this script will clear all existing data in your Neo4j database!**

This interactive demo will:
1. Add information about current top LLMs (Gemini, Claude, GPT-4.1)
2. Update the knowledge graph when Claude 4 emerges as the best LLM
3. Update again when MLMs make traditional LLMs obsolete

The script will pause between phases, allowing you to interact with the agent to see how its knowledge changes.

### 4. Interact with the Agent

In a separate terminal, run the agent interface:

```bash
python agent.py
```

This will start a conversational interface where you can:
1. Ask questions about LLMs using natural language
2. See the agent retrieve information from the knowledge graph
3. Experience how the agent's responses change as the knowledge graph evolves
4. Interact with local LLMs through LM Studio

## Demo Workflow

For the best demonstration experience:

1. Start with a fresh Neo4j database
2. Test LM Studio connection: `python test_lmstudio_connection.py`
3. In Terminal 1: Run `python llm_evolution.py` and complete Phase 1
4. In Terminal 2: Run `python agent.py` and ask "Which is the best LLM?"
5. In Terminal 1: Continue to Phase 2 by typing "continue"
6. In Terminal 2: Ask the same question again to see the updated knowledge
7. In Terminal 1: Continue to Phase 3
8. In Terminal 2: Ask "Are LLMs still relevant?" to see the final evolution

This workflow demonstrates how Graphiti maintains temporal knowledge and how the agent's responses adapt to the changing knowledge graph.

## Key Features

- **Local LLM Integration**: Uses LM Studio for private, local LLM inference
- **Temporal Knowledge**: Graphiti tracks when facts become valid and invalid
- **Hybrid Search**: Combines semantic similarity and BM25 text retrieval
- **Context-Aware Queries**: Reranks results based on graph distance
- **Structured Data Support**: Works with both text and JSON episodes
- **Easy Integration**: Seamlessly works with Pydantic AI for agent development
- **Connection Testing**: Built-in utilities to verify LM Studio connectivity

## Project Structure

- `agent.py`: Pydantic AI agent with Graphiti search capabilities using LM Studio
- `quickstart.py`: Tutorial demonstrating core Graphiti features
- `llm_evolution.py`: Demo showing how knowledge evolves over time
- `test_lmstudio_connection.py`: Connection testing utility for LM Studio
- `requirements.txt`: Project dependencies
- `pyproject.toml`: Project configuration with all dependencies
- `.env`: Configuration for API keys, LM Studio, and Neo4j connection

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
