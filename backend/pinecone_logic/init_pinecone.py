import os
import pinecone

# Hardcoded Pinecone credentials
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")

def initialize_pinecone():
    """
    Initializes the Pinecone client with the API key and environment.
    """
    try:
        pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)
        print("Pinecone initialized successfully!")
        return pinecone
    except Exception as e:
        print(f"Failed to initialize Pinecone: {e}")
        raise

# Export the Pinecone client
pinecone_client = initialize_pinecone()