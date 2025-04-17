"""
src/core/llm.py: Initializes the LLM for text-to-SQL generation.
- Supports Ollama (local LLaMA) and AWS Bedrock (Claude).
- Uses configuration from config.py.
"""

from langchain_ollama import OllamaLLM
from langchain_community.chat_models.bedrock import BedrockChat
from src.config.config import CONFIG, AWS_REGION, AWS_ACCESS_KEY, AWS_SECRET_KEY
from src.utils.logging import setup_logging


logger = setup_logging(__name__)

def initialize_llm():
    """Initialize the LLM based on config."""
    provider = CONFIG["llm_provider"].lower()
    
    if provider == "ollama":
        logger.info(f"Initializing Ollama with model: {CONFIG['ollama_model']}")
        return OllamaLLM(model=CONFIG["ollama_model"], temperature=0.7)
    
    elif provider == "bedrock":
        logger.info(f"Initializing Bedrock with model: {CONFIG['bedrock_model']}")
        return BedrockChat(
            model_id=CONFIG["bedrock_model"],
            region_name=AWS_REGION,
            credentials_profile_name=None,
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
            model_kwargs={"temperature": 0.7}
        )
    
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")