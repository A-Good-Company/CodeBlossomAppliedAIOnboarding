import os
from dotenv import load_dotenv
import json
import numpy as np
from openai import OpenAI
from typing import List, Dict
import scipy.spatial.distance as distance
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown

# Load environment variables
load_dotenv()
console = Console()

class ResumeSearchBot:
    def __init__(self, embeddings_file: str = "resume_embeddings.json"):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.embeddings_data = self.load_embeddings(embeddings_file)
        
    def load_embeddings(self, filename: str) -> List[Dict]:
        """Load embeddings from JSON file"""
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            console.print(f"[red]Error: {filename} not found![/red]")
            return []

    def generate_query_embedding(self, query: str) -> List[float]:
        """Generate embedding for the search query"""
        try:
            response = self.client.embeddings.create(
                input=query,
                model="text-embedding-3-small"
            )
            return response.data[0].embedding
        except Exception as e:
            console.print(f"[red]Error generating query embedding: {e}[/red]")
            return None

    def calculate_similarity(self, query_embedding: List[float], 
                           experience_embedding: List[float]) -> float:
        """Calculate cosine similarity between query and experience embeddings"""
        return 1 - distance.cosine(query_embedding, experience_embedding)

    def search_experiences(self, query: str, top_k: int = 4) -> List[Dict]:
        """Search for relevant experiences based on query"""
        query_embedding = self.generate_query_embedding(query)
        if not query_embedding:
            return []

        # Calculate similarities and rank results
        results = []
        for item in self.embeddings_data:
            similarity = self.calculate_similarity(query_embedding, item["embedding"])
            results.append({
                "text": item["text"],
                "similarity": similarity
            })

        # Sort by similarity score
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]

    def display_results(self, results: List[Dict]):
        """Display search results in a formatted table"""
        if not results:
            console.print("[yellow]No relevant experiences found.[/yellow]")
            return

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Rank", style="dim")
        table.add_column("Relevance", style="cyan")
        table.add_column("Experience", style="green")

        for idx, result in enumerate(results, 1):
            relevance = f"{result['similarity']:.2%}"
            table.add_row(
                str(idx),
                relevance,
                result["text"]
            )

        console.print("\n[bold]Search Results:[/bold]")
        console.print(table)

def print_welcome_message():
    welcome_text = """
    # Resume Experience Search Bot 🤖

    Welcome! I can help you find relevant experiences from the resume.
    
    ## Instructions:
    - Type your query to search for relevant experiences
    - Type 'quit' or 'exit' to end the session
    - Type 'help' for instructions
    """
    console.print(Markdown(welcome_text))

def main():
    bot = ResumeSearchBot()
    print_welcome_message()

    while True:
        try:
            console.print("\n[bold cyan]Enter your query:[/bold cyan] ", end="")
            query = input()

            if query.lower() in ['quit', 'exit']:
                console.print("[yellow]Goodbye! 👋[/yellow]")
                break
            
            if query.lower() == 'help':
                print_welcome_message()
                continue

            if not query.strip():
                console.print("[red]Please enter a valid query.[/red]")
                continue

            # Search and display results
            results = bot.search_experiences(query)
            bot.display_results(results)

        except KeyboardInterrupt:
            console.print("\n[yellow]Session terminated by user. Goodbye! 👋[/yellow]")
            break
        except Exception as e:
            console.print(f"[red]An error occurred: {e}[/red]")

if __name__ == "__main__":
    main()