import os
import time
import logging
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv, find_dotenv

# logging.basicConfig(level=logging.DEBUG)
load_dotenv(find_dotenv())

def retrieveKey():
    if os.getenv("PINECONE_API_KEY") is None:
        print("KEY NOT RETRIEVED")
    else: return os.getenv("API_KEY")

PINECONE_KEY = retrieveKey()

pc_client = Pinecone(api_key=PINECONE_KEY)

# Define your text data
texts = [
    "The weather is sunny today.",
    "I love going to the beach when it's sunny.",
    "Today's weather is perfect for a hike.",
    "I prefer rainy days over sunny ones.",
    "Hiking is a great activity on a sunny day."
]

# Generate embeddings using the hosted model
embeddings = pc_client.inference.embed(
    model="multilingual-e5-large",
    inputs=texts,
    parameters={"input_type": "passage", "truncate": "END"}
)

# Create an index with the appropriate dimension
index_name = "example-index1"
pc_client.create_index(index_name, dimension=1536, metric="cosine", spec=ServerlessSpec(cloud="aws",region="us-east-1"))  # Dimension should match the model's output
index = pc_client.Index(index_name)

# Prepare data for upsert
vectors = []

# Loop through embeddings and texts with a counter (i)
for i, (embedding, text) in enumerate(zip(embeddings, texts)):
    # Create a dictionary for each vector
    vector = {
        "id": f"sentence-{i}",           # Unique identifier for this vector
        "values": embedding['values'],  # Embedding values
        "metadata": {"text": text}      # Metadata with the original text
    }
    # Add the dictionary to the list
    vectors.append(vector)
    # print(vector)

# print(stats['my-namespace'])
# Upsert vectors into the index
response = index.upsert(vectors=vectors, namespace="my-namespace")

time.sleep(10)

print(index.describe_index_stats())
print("Namespace Stats:", index.describe_index_stats().get('namespaces'))
retrieved_vector = index.fetch(ids=["sentence-1"], namespace="my-namespace")
print(retrieved_vector)

# Generate embedding for the query
query_embedding = pc_client.inference.embed(
    model="multilingual-e5-large",
    inputs=["hiking"],
    parameters={"input_type": "query"}
)[0]['values']

# print(index.describe_index_stats())
# print(len(query_embedding))
# print(index.describe_index_stats()['namespaces'])

# Query the index
results = index.query(vector=query_embedding, top_k=5, include_metadata=True, namespace="my-namespace")

print(results)