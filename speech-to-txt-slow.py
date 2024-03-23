from dotenv import find_dotenv, load_dotenv
from transformers import pipeline
import requests
import os 

# Load environment variables from .env file
load_dotenv(find_dotenv())

# Retrieve the API token from environment variables
HUGGINGFACEHUB_API_TOKENS = os.getenv("HUGGINGFACEHUB_API_TOKENS")

# Define the API endpoint
API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v2"

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    
    headers = {"Authorization": f"Bearer {HUGGINGFACEHUB_API_TOKENS}"}
    
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()

output = query("sample2.flac")

print(output)
