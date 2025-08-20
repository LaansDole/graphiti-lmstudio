#!/usr/bin/env python3
"""
Simple test script to verify LM Studio connection and functionality.
"""

import os
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_lmstudio_sdk():
    """Test LM Studio connection using the lmstudio-python SDK."""
    try:
        import lmstudio as lms
        
        # Get server configuration from environment or use default
        server_host = os.getenv('LMSTUDIO_SERVER_HOST', 'localhost:1234')
        
        print(f"Testing LM Studio connection to: {server_host}")
        
        # Configure the default client (must be first interaction)
        lms.configure_default_client(server_host)
        
        # Get the default client
        client = lms.get_default_client()
        
        print("✓ LM Studio SDK configured successfully")
        
        # Test basic connection by listing models
        try:
            models = client.list_models()
            print(f"✓ Successfully connected to LM Studio server")
            print(f"Available models: {len(models)}")
            
            for i, model in enumerate(models[:3]):  # Show first 3 models
                print(f"  {i+1}. {model.id}")
            
            if len(models) > 3:
                print(f"  ... and {len(models) - 3} more models")
                
            return True
            
        except Exception as e:
            print(f"✗ Failed to list models: {str(e)}")
            return False
            
    except ImportError:
        print("✗ lmstudio-python package not installed")
        print("Install with: pip install lmstudio")
        return False
    except Exception as e:
        print(f"✗ LM Studio SDK error: {str(e)}")
        return False

def test_openai_compatible_api():
    """Test LM Studio connection using OpenAI-compatible API."""
    try:
        from openai import OpenAI
        
        # Get configuration from environment
        base_url = os.getenv('LMSTUDIO_API_HOST', 'http://localhost:1234/v1')
        api_key = os.getenv('LMSTUDIO_API_KEY', 'lm-studio')
        
        print(f"\nTesting OpenAI-compatible API at: {base_url}")
        
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
        print(f"✗ OpenAI-compatible API error: {str(e)}")
        return False

def test_simple_chat():
    """Test a simple chat completion with LM Studio."""
    try:
        from openai import OpenAI
        
        base_url = os.getenv('LMSTUDIO_API_HOST', 'http://localhost:1234/v1')
        api_key = os.getenv('LMSTUDIO_API_KEY', 'lm-studio')
        model_name = os.getenv('MODEL_CHOICE', 'openai/gpt-oss-20b')
        
        print(f"\nTesting chat completion with model: {model_name}")
        
        client = OpenAI(
            base_url=base_url,
            api_key=api_key,
        )
        
        # Simple test message
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say hello and confirm you are working."}
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

def main():
    """Run all connection tests."""
    print("=" * 60)
    print("LM Studio Connection Test")
    print("=" * 60)
    
    # Test 1: LM Studio SDK
    sdk_success = test_lmstudio_sdk()
    
    # Test 2: OpenAI-compatible API
    api_success = test_openai_compatible_api()
    
    # Test 3: Simple chat (only if API connection works)
    chat_success = False
    if api_success:
        chat_success = test_simple_chat()
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary:")
    print(f"LM Studio SDK:           {'✓ PASS' if sdk_success else '✗ FAIL'}")
    print(f"OpenAI-compatible API:   {'✓ PASS' if api_success else '✗ FAIL'}")
    print(f"Chat completion:         {'✓ PASS' if chat_success else '✗ FAIL'}")
    print("=" * 60)
    
    if not any([sdk_success, api_success]):
        print("\nTroubleshooting tips:")
        print("1. Ensure LM Studio is running")
        print("2. Check that the server is started in LM Studio")
        print("3. Verify the server address (default: localhost:1234)")
        print("4. Make sure a model is loaded or just-in-time loading is enabled")
        print("5. Check firewall settings")
        
        # Show current configuration
        print(f"\nCurrent configuration:")
        print(f"  Server Host: {os.getenv('LMSTUDIO_SERVER_HOST', 'localhost:1234')}")
        print(f"  API Host: {os.getenv('LMSTUDIO_API_HOST', 'http://localhost:1234/v1')}")
        print(f"  Model: {os.getenv('MODEL_CHOICE', 'openai/gpt-oss-20b')}")
    
    return all([api_success, chat_success])

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
