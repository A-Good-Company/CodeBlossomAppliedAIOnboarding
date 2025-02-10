import os
from dotenv import load_dotenv
import json
from openai import OpenAI
import numpy as np

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
api_key = os.getenv('OPENAI_API_KEY')

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Resume experiences
resume_experiences = [
    {
        "company": "Amazon Music",
        "period": "2017-2018",
        "location": "Bengaluru",
        "details": [
            "Back-end developer for Live Audio Platform's Delivery service",
            "Developed workflows in Python for iOS subscription events routing",
            "Technologies used: AWS Services, Java, Python, DynamoDB, S3, Lambda"
        ]
    },
    {
        "company": "Amazon Web Services",
        "period": "2016",
        "location": "Bengaluru",
        "details": [
            "Implemented email parser module for procurement system",
            "Technologies used: Ruby on Rails, Java Spring"
        ]
    },
    {
        "company": "Amazon Magazines",
        "period": "2015-2016",
        "location": "Chennai",
        "details": [
            "Implemented serverless AWS architecture",
            "Migrated Magazines Retail page to modern Java-based platform"
        ]
    },
    {
        "company": "BitSavvy Solutions",
        "period": "2024-Present",
        "location": "Present",
        "details": [
            "Designed vector database architecture with MongoDB Atlas",
            "AWS backend development for multi-modal chat agent"
        ]
    }
]

def generate_embedding(text):
    """Generate embedding for a given text using OpenAI API"""
    try:
        response = client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None

def process_resume():
    """Process resume experiences and generate embeddings"""
    embeddings_data = []
    
    for experience in resume_experiences:
        # Combine all details into a single text
        experience_text = f"{experience['company']} - {experience['location']} ({experience['period']}): "
        experience_text += " ".join(experience['details'])
        
        # Generate embedding
        embedding = generate_embedding(experience_text)
        
        if embedding:
            embeddings_data.append({
                "text": experience_text,
                "embedding": embedding
            })
    
    return embeddings_data

def save_embeddings(embeddings_data, filename="resume_embeddings.json"):
    """Save embeddings to a JSON file"""
    # Convert numpy arrays to lists for JSON serialization
    serializable_data = []
    for item in embeddings_data:
        serializable_data.append({
            "text": item["text"],
            "embedding": list(map(float, item["embedding"]))
        })
    
    with open(filename, 'w') as f:
        json.dump(serializable_data, f, indent=2)
    
    print(f"Embeddings saved to {filename}")

def main():
    # Generate embeddings for resume experiences
    embeddings_data = process_resume()
    
    # Save embeddings to file
    save_embeddings(embeddings_data)

if __name__ == "__main__":
    main()