import os
from dotenv import load_dotenv
import json
from openai import OpenAI
from typing import List, Dict

# Ensure your environment variables are properly loaded
load_dotenv()

class ExperienceEmbeddingGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def get_embedding(self, text: str) -> List[float]:
        """Generate an embedding for a given piece of text."""
        try:
            response = self.client.embeddings.create(
                input=text,
                model="text-embedding-3-small"
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return []

    def save_embeddings_to_file(self, experiences: List[Dict[str, any]], filename: str):
        """Save experiences and their embeddings to a file."""
        with open(filename, 'w') as f:
            json.dump(experiences, f, ensure_ascii=False, indent=4)

    def collect_experiences_from_file(self, filename: str) -> List[Dict[str, any]]:
        """Collect experiences from a file returning a list of experiences."""
        experiences = []
        try:
            with open(filename, 'r') as file:
                for line in file:
                    embedding = self.get_embedding(line)
                    print(embedding)
                    columns = line.strip().split(' | ')
                    if embedding:
                        experiences.append({
                            "company": columns[0],
                            "period": columns[1],
                            "skills": columns[2],
                            "project": columns[3],
                            "embedding": embedding
                        })
        except FileNotFoundError:
            print(f"File {filename} not found.")
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")

        return experiences

def main():
    generator = ExperienceEmbeddingGenerator()
    experiences = generator.collect_experiences_from_file('embeddings/munk_resume.psv')
    generator.save_embeddings_to_file(experiences, 'resume_embeddings.json')
    print(f"Embeddings for {len(experiences)} experiences have been saved to resume_embeddings.json.")

if __name__ == "__main__":
    main()