"""
src/config/config.py: Configuration for text-to-SQL application.
- Defines LLM provider (Ollama or Bedrock), models, database URI, schema, and embedding model.
- Supports environment variables for AWS credentials.
"""

import os

# Configuration dictionary
CONFIG = {
    "llm_provider": "ollama",  # Options: "ollama", "bedrock"
    "ollama_model": "llama3",  # Ollama model for text-to-SQL
    "ollama_embedding_model": "nomic-embed-text",  # Ollama model for embeddings
    "bedrock_model": "anthropic.claude-3-sonnet-20240229-v1:0",  # Claude model ID
    "database_uri": "sqlite:///sample.db",
    "schema": """
CREATE TABLE airplanes (
    Airplane_id INT(10) PRIMARY KEY,
    Producer VARCHAR(20),
    Type VARCHAR(10)
);
""",
    "chroma_collection": "schema_store",
    "log_level": "INFO",
}

# AWS Bedrock credentials (if using Bedrock)
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")