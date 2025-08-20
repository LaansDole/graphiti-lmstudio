#!/usr/bin/env python3
"""
Test script to verify Neo4j and LM Studio connections.
"""

import os
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_neo4j_connection():
    """Test Neo4j connection."""
    print("=" * 60)
    print("Testing Neo4j Connection")
    print("=" * 60)
    
    try:
        from neo4j import GraphDatabase
        
        # Get Neo4j configuration
        neo4j_uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
        neo4j_user = os.getenv('NEO4J_USER', 'neo4j')
        neo4j_password = os.getenv('NEO4J_PASSWORD', 'password')
        
        print(f"Connecting to: {neo4j_uri}")
        print(f"Username: {neo4j_user}")
        
        # Create driver and test connection
        driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
        
        # Test the connection
        driver.verify_connectivity()
        print("✓ Neo4j connection successful")
        
        # Test a simple query
        with driver.session() as session:
            result = session.run("RETURN 'Hello Neo4j!' as message")
            record = result.single()
            print(f"✓ Query test successful: {record['message']}")
            
        # Get Neo4j version
        with driver.session() as session:
            result = session.run("CALL dbms.components() YIELD name, versions")
            for record in result:
                if record['name'] == 'Neo4j Kernel':
                    print(f"✓ Neo4j version: {record['versions'][0]}")
                    break
        
        driver.close()
        return True
        
    except ImportError:
        print("✗ neo4j package not installed")
        print("Install with: pip install neo4j")
        return False
    except Exception as e:
        print(f"✗ Neo4j connection failed: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Ensure Neo4j is running (check Neo4j Desktop)")
        print("2. Verify connection details in .env file")
        print("3. Check username and password")
        print(f"   Current config: {neo4j_uri}, user: {neo4j_user}")
        return False

async def test_lmstudio_connection():
    """Test LM Studio connection using OpenAI-compatible API."""
    print("\n" + "=" * 60)
    print("Testing LM Studio Connection (OpenAI-compatible)")
    print("=" * 60)
    
    try:
        from openai import OpenAI
        
        # Get configuration from environment
        base_url = os.getenv('OPENAI_BASE_URL', 'http://localhost:1234/v1')
        api_key = os.getenv('OPENAI_API_KEY', 'lm-studio')
        
        print(f"Base URL: {base_url}")
        print(f"API Key: {api_key}")
        
        # Create OpenAI client with LM Studio configuration
        client = OpenAI(
            base_url=base_url,
            api_key=api_key,
        )
        
        # Test by listing models
        models = client.models.list()
        print("✓ Successfully connected via OpenAI-compatible API")
        print(f"Available models: {len(models.data)}")
        
        for i, model in enumerate(models.data[:3]):  # Show first 3 models
            print(f"  {i+1}. {model.id}")
            
        if len(models.data) > 3:
            print(f"  ... and {len(models.data) - 3} more models")
            
        return True
        
    except ImportError:
        print("✗ openai package not installed")
        print("Install with: pip install openai")
        return False
    except Exception as e:
        print(f"✗ LM Studio connection failed: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Ensure LM Studio is running")
        print("2. Start the local server in LM Studio")
        print("3. Check server URL and port")
        print(f"   Current config: {base_url}")
        return False

async def test_simple_chat():
    """Test a simple chat completion with LM Studio."""
    print("\n" + "=" * 60)
    print("Testing Simple Chat Completion")
    print("=" * 60)
    
    try:
        from openai import OpenAI
        
        base_url = os.getenv('OPENAI_BASE_URL', 'http://localhost:1234/v1')
        api_key = os.getenv('OPENAI_API_KEY', 'lm-studio')
        
        client = OpenAI(
            base_url=base_url,
            api_key=api_key,
        )
        
        # Get available models
        models = client.models.list()
        if not models.data:
            print("✗ No models available")
            return False
            
        # Use the first available model
        model_name = models.data[0].id
        print(f"Using model: {model_name}")
        
        # Simple test message
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say hello and confirm you are working. Keep it short."}
            ],
            max_tokens=50,
            temperature=0.7
        )
        
        print("✓ Chat completion successful")
        print(f"Response: {response.choices[0].message.content.strip()}")
        return True
        
    except Exception as e:
        print(f"✗ Chat completion failed: {str(e)}")
        return False

async def test_graphiti_basic():
    """Test basic Graphiti initialization."""
    print("\n" + "=" * 60)
    print("Testing Graphiti Basic Initialization")
    print("=" * 60)
    
    try:
        from graphiti_core import Graphiti
        
        # Get Neo4j configuration
        neo4j_uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
        neo4j_user = os.getenv('NEO4J_USER', 'neo4j')
        neo4j_password = os.getenv('NEO4J_PASSWORD', 'password')
        
        print("Initializing Graphiti...")
        
        # Initialize Graphiti
        graphiti = Graphiti(neo4j_uri, neo4j_user, neo4j_password)
        
        print("✓ Graphiti initialized successfully")
        
        # Test building indices
        print("Building indices and constraints...")
        await graphiti.build_indices_and_constraints()
        print("✓ Indices and constraints built successfully")
        
        # Close connection
        await graphiti.close()
        print("✓ Graphiti connection closed successfully")
        
        return True
        
    except Exception as e:
        print(f"✗ Graphiti initialization failed: {str(e)}")
        print("\nThis might be due to:")
        print("1. Missing OpenAI API configuration")
        print("2. Neo4j connection issues")
        print("3. LM Studio not responding correctly")
        return False

async def main():
    """Run all connection tests."""
    print("Connection Test Suite for Graphiti + LM Studio")
    print("=" * 60)
    
    # Display current configuration
    print("Current Configuration:")
    print(f"  Neo4j URI: {os.getenv('NEO4J_URI', 'bolt://localhost:7687')}")
    print(f"  Neo4j User: {os.getenv('NEO4J_USER', 'neo4j')}")
    print(f"  OpenAI Base URL: {os.getenv('OPENAI_BASE_URL', 'http://localhost:1234/v1')}")
    print(f"  OpenAI API Key: {os.getenv('OPENAI_API_KEY', 'lm-studio')}")
    
    # Run tests
    neo4j_ok = await test_neo4j_connection()
    lmstudio_ok = await test_lmstudio_connection()
    
    chat_ok = False
    if lmstudio_ok:
        chat_ok = await test_simple_chat()
    
    graphiti_ok = False
    if neo4j_ok and lmstudio_ok:
        graphiti_ok = await test_graphiti_basic()
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary:")
    print(f"Neo4j Connection:        {'✓ PASS' if neo4j_ok else '✗ FAIL'}")
    print(f"LM Studio Connection:    {'✓ PASS' if lmstudio_ok else '✗ FAIL'}")
    print(f"Chat Completion:         {'✓ PASS' if chat_ok else '✗ FAIL'}")
    print(f"Graphiti Initialization: {'✓ PASS' if graphiti_ok else '✗ FAIL'}")
    print("=" * 60)
    
    if all([neo4j_ok, lmstudio_ok, chat_ok, graphiti_ok]):
        print("🎉 All tests passed! You're ready to run the demos.")
    else:
        print("❌ Some tests failed. Please address the issues above before proceeding.")
    
    return all([neo4j_ok, lmstudio_ok, chat_ok, graphiti_ok])

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
