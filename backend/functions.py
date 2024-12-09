import time
from pinecone import ServerlessSpec

def create_pinecone_index(pinecone_client, index_name, dimension=1536, metric="cosine", cloud="aws", region="us-east-1"):
    """
    Creates a Pinecone index if it doesn't already exist.

    Args:
        pinecone_client: The initialized Pinecone client.
        index_name (str): Name of the index.
        dimension (int): Dimensionality of the vectors.
        metric (str): Similarity metric.
        cloud (str): Cloud provider.
        region (str): Region for hosting the index.

    Returns:
        pinecone.Index: The created or retrieved index.
    """
    if index_name not in pinecone_client.list_indexes():
        print(f"Creating index '{index_name}'...")
        pinecone_client.create_index(
            index_name,
            dimension=dimension,
            metric=metric,
            spec=ServerlessSpec(cloud=cloud, region=region)
        )
        time.sleep(10)
    else:
        print(f"Index '{index_name}' already exists.")

    return pinecone_client.Index(index_name)

def fetch_pinecone_index(client, index_name):
    """
    Fetches a Pinecone index by name.

    Args:
        client (pinecone.Pinecone): The initialized Pinecone client.
        index_name (str): The name of the Pinecone index to fetch.

    Returns:
        pinecone.Index: The Pinecone index object.

    Raises:
        ValueError: If the index does not exist.
    """
    # Check if the index exists
    if index_name not in client.list_indexes():
        raise ValueError(f"Index '{index_name}' does not exist.")
    
    # Return the index object
    return client.Index(index_name)

def check_index_exists(client, index_name):
    if index_name not in client.list_indexes():
        return False
    else: return True


def generateEmbeddings( pinecone_client, inputs=None, model="multilingual-e5-large", input_type="passage", truncate="END" ):
    """
    Generates embeddings using Pinecone's Inference API.

    Args:
        pinecone_client: The initialized Pinecone client or inference object.
        inputs (str or list): Input text to generate embeddings for.
        model (str): The embedding model to use (default: multilingual-e5-large).
        input_type (str): The type of input ("query" or "passage", default: "passage").
        truncate (str): Truncation behavior for long inputs ("END" or "START", default: "END").

    Returns:
        list: A list of embedding vectors.
    """
    if not inputs:
        raise ValueError("Input text cannot be None or empty.")

    try:
        # Generate embeddings using Pinecone's inference API
        embeddings = pinecone_client.inference.embed(
            model=model,
            inputs=inputs,
            parameters={"input_type": input_type, "truncate": truncate}
        )
        return [embedding["values"] for embedding in embeddings]  # Extract embedding values
    except Exception as e:
        print(f"An error occurred while generating embeddings: {e}")
        return None

def queryForMatch( query_embedding=None, index=None, top_k=5, namespace="my-namespace" ):
    """
    Queries the Pinecone database for matches to the input text which is passed as a vector embedding.

    Args:
        query_embedding (list): Embedding vector for the query.
        index (pinecone.Index): The Pinecone index to query (must be provided).
        top_k (int): Number of top results to return (default: 3).
        namespace (str): The namespace to query within (default: "my-namespace").

    Returns:
        dict: Query results from the Pinecone index.
    """
    if not index:
        raise ValueError("Index must be provided.")

    try:

        # Query Pinecone index
        results = index.query(
            vector=query_embedding,
            top_k=top_k,
            namespace=namespace,
            include_metadata=True
        )

        return results

    except Exception as e:
        print(f"An error occurred during the query: {e}")
        return None