"""
LLM Configuration Module

This module provides centralized configuration for LM Studio integration
across all Graphiti agent components.
"""

import os
from dotenv import load_dotenv
from graphiti_core import Graphiti
from graphiti_core.embedder import OpenAIEmbedderConfig, OpenAIEmbedder
from graphiti_core.llm_client import OpenAIClient, LLMConfig

# Load environment variables
load_dotenv()


def get_lm_studio_config():
    """
    Get LM Studio configuration from environment variables.
    
    Returns:
        tuple: (embedding_model, api_key, base_url, chat_model)
    """
    embedding_model = os.environ.get('OPENAI_EMBEDDING_MODEL', 'text-embedding-nomic-embed-text-v1.5')
    api_key = os.environ.get('OPENAI_API_KEY', 'lm-studio')
    base_url = os.environ.get('OPENAI_BASE_URL', 'http://localhost:1234/v1')
    chat_model = os.environ.get('MODEL_CHOICE', 'llama-3.2-1b-instruct')
    
    return embedding_model, api_key, base_url, chat_model


def create_embedder():
    """
    Create an OpenAI embedder configured for LM Studio.
    
    Returns:
        OpenAIEmbedder: Configured embedder instance
    """
    embedding_model, api_key, base_url, _ = get_lm_studio_config()
    
    embedder_config = OpenAIEmbedderConfig(
        embedding_model=embedding_model,
        embedding_dim=768,
        api_key=api_key,
        base_url=base_url
    )
    
    return OpenAIEmbedder(config=embedder_config)


def create_llm_client():
    """
    Create an OpenAI LLM client configured for LM Studio.
    
    Returns:
        OpenAIClient: Configured LLM client instance
    """
    _, api_key, base_url, chat_model = get_lm_studio_config()
    
    llm_config = LLMConfig(
        model=chat_model,
        small_model=chat_model,  # Use the same model for both normal and small operations
        api_key=api_key,
        base_url=base_url
    )
    
    return OpenAIClient(config=llm_config)


async def initialize_graphiti_with_clean_state(graphiti_client, clear_data_func=None):
    """
    Initialize Graphiti with proper indices and optionally clear data.
    
    This function ensures that entity types are properly set up after clearing data
    to prevent entity_type_id warnings.
    
    Args:
        graphiti_client: The Graphiti client instance
        clear_data_func: Optional function to clear data (should accept driver parameter)
    """
    # First, build indices and constraints
    await graphiti_client.build_indices_and_constraints()
    
    # If data clearing is requested, do it after indices are built
    if clear_data_func:
        print("Clearing existing graph data for clean demo...")
        await clear_data_func(graphiti_client.driver)
        print("Graph data cleared successfully.")
        
        # Rebuild indices and constraints after clearing to ensure clean state
        await graphiti_client.build_indices_and_constraints()


def create_graphiti_client(neo4j_uri=None, neo4j_user=None, neo4j_password=None):
    """
    Create a Graphiti client with LM Studio configuration.
    
    Args:
        neo4j_uri: Neo4j URI (defaults to environment variable)
        neo4j_user: Neo4j username (defaults to environment variable)
        neo4j_password: Neo4j password (defaults to environment variable)
        
    Returns:
        Graphiti: Configured Graphiti client instance
    """
    # Use provided parameters or fall back to environment variables
    neo4j_uri = neo4j_uri or os.environ.get('NEO4J_URI', 'bolt://localhost:7687')
    neo4j_user = neo4j_user or os.environ.get('NEO4J_USER', 'neo4j')
    neo4j_password = neo4j_password or os.environ.get('NEO4J_PASSWORD', 'password')
    
    # Validate required parameters
    if not neo4j_uri or not neo4j_user or not neo4j_password:
        raise ValueError('NEO4J_URI, NEO4J_USER, and NEO4J_PASSWORD must be set')
    
    # Create embedder and LLM client
    embedder = create_embedder()
    llm_client = create_llm_client()
    
    # Create and return Graphiti client
    return Graphiti(neo4j_uri, neo4j_user, neo4j_password, embedder=embedder, llm_client=llm_client)


def get_model_info():
    """
    Get model information for display purposes.
    
    Returns:
        dict: Dictionary containing model configuration info
    """
    embedding_model, api_key, base_url, chat_model = get_lm_studio_config()
    
    return {
        'embedding_model': embedding_model,
        'chat_model': chat_model,
        'base_url': base_url,
        'api_key': api_key
    }
