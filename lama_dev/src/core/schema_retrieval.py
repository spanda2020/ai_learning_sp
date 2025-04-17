"""
src/core/schema_retrieval.py: Handles schema storage and retrieval using ChromaDB.
- Uses Ollama embeddings (e.g., nomic-embed-text) for semantic search.
- Stores database schema from config.py and retrieves relevant schema for queries.
"""

from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from src.config.config import CONFIG
from src.utils.logging import setup_logging

logger = setup_logging(__name__)

def initialize_vector_store():
    """Initialize ChromaDB with schema embeddings using Ollama."""
    embeddings = OllamaEmbeddings(model=CONFIG["ollama_embedding_model"])
    vector_store = Chroma.from_texts(
        texts=[CONFIG["schema"]],
        embedding=embeddings,
        collection_name=CONFIG["chroma_collection"],
    )
    logger.info("Initialized ChromaDB vector store with Ollama embeddings")
    return vector_store

def retrieve_schema(vector_store, query: str) -> str:
    """Retrieve relevant schema from ChromaDB."""
    results = vector_store.similarity_search(query, k=1)
    return results[0].page_content if results else "No relevant schema found."