from __future__ import annotations
from typing import Dict, List, Optional
from dataclasses import dataclass
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from rich.markdown import Markdown
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
import asyncio
import os
import logging

from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai import Agent, RunContext
from graphiti_core import Graphiti

load_dotenv()

# Configure logging to be less verbose unless there are errors
logging.basicConfig(level=logging.WARNING)
# Suppress specific noisy loggers
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('httpcore').setLevel(logging.WARNING)
logging.getLogger('openai').setLevel(logging.WARNING)

# ========== Define dependencies ==========
@dataclass
class GraphitiDependencies:
    """Dependencies for the Graphiti agent."""
    graphiti_client: Graphiti

# ========== Helper function to get model configuration ==========
def get_model():
    """Configure and return the LLM model to use."""
    # LM Studio configuration
    model_choice = os.getenv('MODEL_CHOICE', 'openai/gpt-oss-20b')
    base_url = os.getenv('LMSTUDIO_API_HOST', 'http://127.0.0.1:1234/v1')
    api_key = os.getenv('LMSTUDIO_API_KEY', 'lm-studio')

    # Create OpenAI provider with LM Studio base URL
    provider = OpenAIProvider(
        api_key=api_key,
        base_url=base_url
    )
    
    return OpenAIModel(model_choice, provider=provider)

# ========== Create the Graphiti agent ==========
graphiti_agent = Agent(
    get_model(),
    system_prompt="""You are a helpful assistant with access to a knowledge graph filled with temporal data about LLMs.
    
    When the user asks you a question, you should:
    1. Use your search tool to query the knowledge graph for relevant information
    2. If the search returns results, use that information to answer the question
    3. If the search returns no results or fails, acknowledge that you don't have specific information about that topic in the knowledge graph
    4. Always be honest about what information you found or didn't find
    5. You can still provide general knowledge if the knowledge graph doesn't contain specific information
    
    Be conversational and helpful, but always be clear about what information comes from the knowledge graph versus your general knowledge.""",
    deps_type=GraphitiDependencies,
    retries=1  # Limit retries to prevent loops
)

# ========== Define a result model for Graphiti search ==========
class GraphitiSearchResult(BaseModel):
    """Model representing a search result from Graphiti."""
    uuid: str = Field(description="The unique identifier for this fact")
    fact: str = Field(description="The factual statement retrieved from the knowledge graph")
    valid_at: Optional[str] = Field(None, description="When this fact became valid (if known)")
    invalid_at: Optional[str] = Field(None, description="When this fact became invalid (if known)")
    source_node_uuid: Optional[str] = Field(None, description="UUID of the source node")

# ========== Graphiti search tool ==========
@graphiti_agent.tool
async def search_graphiti(ctx: RunContext[GraphitiDependencies], query: str) -> List[GraphitiSearchResult]:
    """Search the Graphiti knowledge graph with the given query.
    
    Args:
        ctx: The run context containing dependencies
        query: The search query to find information in the knowledge graph
        
    Returns:
        A list of search results containing facts that match the query
    """
    # Access the Graphiti client from dependencies
    graphiti = ctx.deps.graphiti_client
    
    try:
        # Perform the search
        logging.info(f"Searching Graphiti with query: {query}")
        results = await graphiti.search(query)
        logging.info(f"Found {len(results)} results")
        
        # Format the results
        formatted_results = []
        for result in results:
            formatted_result = GraphitiSearchResult(
                uuid=result.uuid,
                fact=result.fact,
                source_node_uuid=result.source_node_uuid if hasattr(result, 'source_node_uuid') else None
            )
            
            # Add temporal information if available
            if hasattr(result, 'valid_at') and result.valid_at:
                formatted_result.valid_at = str(result.valid_at)
            if hasattr(result, 'invalid_at') and result.invalid_at:
                formatted_result.invalid_at = str(result.invalid_at)
            
            formatted_results.append(formatted_result)
        
        return formatted_results
    except Exception as e:
        # Log the error with more detail
        logging.error(f"Error searching Graphiti: {type(e).__name__}: {str(e)}")
        # Return empty results instead of raising to prevent tool retry loops
        return []

# ========== Main execution function ==========
async def main():
    """Run the Graphiti agent with user queries."""
    console = Console()
    
    # Create a nice welcome banner
    welcome_table = Table.grid(padding=1)
    welcome_table.add_column(style="cyan bold", justify="center")
    welcome_table.add_row("🤖 Graphiti AI Agent")
    welcome_table.add_row("[dim]Powered by Pydantic AI, Graphiti, Neo4j, and LM Studio[/dim]")
    
    console.print(Panel(welcome_table, title="[bold blue]Welcome[/bold blue]", border_style="blue"))
    
    # Display configuration info
    lm_studio_host = os.getenv('LMSTUDIO_API_HOST', 'http://127.0.0.1:1234/v1')
    model_choice = os.getenv('MODEL_CHOICE', 'openai/gpt-oss-20b')
    
    config_table = Table(show_header=False, box=None)
    config_table.add_column("Key", style="cyan")
    config_table.add_column("Value", style="white")
    config_table.add_row("🌐 LM Studio Host:", lm_studio_host)
    config_table.add_row("🧠 Model:", model_choice)
    config_table.add_row("💬 Commands:", "[dim]Type 'exit' to quit[/dim]")
    
    console.print(Panel(config_table, title="[bold green]Configuration[/bold green]", border_style="green"))

    # Neo4j connection parameters
    neo4j_uri = os.environ.get('NEO4J_URI', 'bolt://localhost:7687')
    neo4j_user = os.environ.get('NEO4J_USER', 'neo4j')
    neo4j_password = os.environ.get('NEO4J_PASSWORD', 'password')
    
    # Initialize Graphiti with LM Studio configuration
    from .llm_config import create_graphiti_client
    
    graphiti_client = create_graphiti_client(neo4j_uri, neo4j_user, neo4j_password)
    
    # Initialize the graph database with graphiti's indices if needed
    try:
        await graphiti_client.build_indices_and_constraints()
        console.print("✅ [green]Graphiti indices built successfully[/green]")
        
        # Optional: Clear any inconsistent entity type data
        # This helps resolve entity_type_id warnings
        from graphiti_core.utils.maintenance.graph_data_operations import clear_data
        # Uncomment the next line if you want to start with a completely fresh database
        await clear_data(graphiti_client.driver)
        
    except Exception as e:
        console.print(f"ℹ️  [yellow]Using existing indices: {str(e)}[/yellow]")

    messages = []
    
    try:
        while True:
            # Get user input with emoji
            console.print("\n👤 ", style="bold blue", end="")
            user_input = input()
            
            # Check if user wants to exit
            if user_input.lower() in ['exit', 'quit', 'bye', 'goodbye']:
                console.print("👋 [bold cyan]Goodbye![/bold cyan]")
                break
            
            try:
                # Process the user input and output the response
                console.print("🤖 ", style="bold green", end="")
                with Live('', console=console, vertical_overflow='visible') as live:
                    # Pass the Graphiti client as a dependency
                    deps = GraphitiDependencies(graphiti_client=graphiti_client)
                    
                    async with graphiti_agent.run_stream(
                        user_input, message_history=messages, deps=deps
                    ) as result:
                        curr_message = ""
                        async for message in result.stream_text(delta=True):
                            curr_message += message
                            live.update(Markdown(curr_message))
                    
                    # Add the new messages to the chat history
                    messages.extend(result.all_messages())
                
            except Exception as e:
                error_msg = str(e)
                console.print(f"\n❌ [bold red]Error:[/bold red] {error_msg}")
                
                # Provide helpful LM Studio troubleshooting tips
                if "connection" in error_msg.lower() or "refused" in error_msg.lower():
                    troubleshoot_table = Table(show_header=False, box=None)
                    troubleshoot_table.add_column("Step", style="cyan")
                    troubleshoot_table.add_column("Description", style="white")
                    troubleshoot_table.add_row("1.", "Ensure LM Studio server is running")
                    troubleshoot_table.add_row("2.", f"Check server accessibility: {os.getenv('LMSTUDIO_API_HOST', 'http://127.0.0.1:1234/v1')}")
                    troubleshoot_table.add_row("3.", f"Verify model is loaded: '{os.getenv('MODEL_CHOICE', 'openai/gpt-oss-20b')}'")
                    troubleshoot_table.add_row("4.", "Enable just-in-time model loading if needed")
                    troubleshoot_table.add_row("5.", "Visit: https://lmstudio.ai/docs/basics/server")
                    
                    console.print(Panel(troubleshoot_table, title="[bold yellow]🔧 LM Studio Troubleshooting[/bold yellow]", border_style="yellow"))
    finally:
        # Close the Graphiti connection when done
        await graphiti_client.close()
        console.print("\n🔌 [dim]Graphiti connection closed.[/dim]")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console = Console()
        console.print("\n⏹️  [bold yellow]Program terminated by user.[/bold yellow]")
    except Exception as e:
        console = Console()
        console.print(f"\n💥 [bold red]Unexpected error:[/bold red] {str(e)}")
        raise
