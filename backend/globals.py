import os
from pinecone import Pinecone
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

#Index being referred
INDEX_NAME = "response-informatics-index"
namespace = "response-informatics"
# Initialize Pinecone client
pinecone_client = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))