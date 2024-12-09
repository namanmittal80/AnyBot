import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv, find_dotenv
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from globals import pinecone_client, openai_client, INDEX_NAME, namespace

def initialize_services():
    load_dotenv(find_dotenv())
    OPENAI_KEY = os.getenv("OPEN_AI_API_KEY")

    embedding_model = OpenAIEmbeddings(
        openai_api_key=os.getenv("OPEN_AI_API_KEY")
    )

    index = pinecone_client.Index(INDEX_NAME)

    llm = ChatOpenAI(api_key=OPENAI_KEY)

    return index, embedding_model, llm

# Create the RAG chain
def create_rag_chain(index, embedding_model, llm):
    prompt = ChatPromptTemplate.from_template("""
    Answer the following question based only on the provided context as a chatbot. Only use below context if it is relevant to the question.

    <context>
    {context}
    </context>

    Question: {input}
    """)

    document_chain = create_stuff_documents_chain(llm, prompt)
    vectorstore = Pinecone(index, embedding_model, "text", "response-informatics")
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

    return create_retrieval_chain(
        retriever=retriever,
        combine_docs_chain=document_chain
    )
    
def process_query(rag_chain, user_input):
    response = rag_chain.invoke({"input": user_input})
    print(response["answer"])
    return response["answer"]


