import json
import os
import time
from pinecone import Pinecone, ServerlessSpec
import functions as fs
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

#Load .env file
load_dotenv(find_dotenv())
pc_client = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
openai_client = OpenAI(api_key = os.getenv("OPEN_AI_API_KEY"))

# Define your Pinecone index name
INDEX_NAME = "response-informatics-index"

#TO-DO edit this out
input_file = "output.json"
namespace = "response-informatics"

if not fs.check_index_exists(pc_client, INDEX_NAME):
    index = pc_client.Index(INDEX_NAME)
else: 
    fs.create_pinecone_index(pc_client, INDEX_NAME)
    index = pc_client.Index(INDEX_NAME)

print("INDEXES", pc_client.list_indexes())
# index = fs.fetch_pinecone_index(pc_client, INDEX_NAME)

print("Reading data")
# Step 2: Read JSON data
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Extract texts and URLs
urls = [block["url"] for block in data]
texts = [block["text"] for block in data]

embeddings = [
    openai_client.embeddings.create(input=text, model="text-embedding-ada-002").data[0].embedding
    for text in texts
]

vectors = [
    {"id": url, "values": embedding, "metadata": {"text": text}}
    for url, embedding, text in zip(urls, embeddings, texts)
]

response = index.upsert(vectors=vectors, namespace=namespace)

time.sleep(10)