from langchain_community.llms import Ollama
from langchain_community.llms import Bedrock  # For Claude (AWS Bedrock)
import os

def get_llm(model_type: str = "ollama"):
    if model_type == "ollama":
        try:
            return Ollama(model="llama3.1", temperature=0)
        except Exception as e:
            raise Exception(f"Error loading Ollama: {e}. Ensure Ollama server is running (ollama run llama3.1).")
    
    elif model_type == "claude":
        try:
            # Requires AWS credentials and Bedrock access
            return Bedrock(
                model_id="anthropic.claude-v2",  # Or claude-3
                region_name=os.getenv("AWS_REGION", "us-east-1"),
                credentials_profile_name=os.getenv("AWS_PROFILE")
            )
        except Exception as e:
            raise Exception(f"Error loading Claude: {e}. Ensure AWS credentials are set.")
    
    else:
        raise ValueError(f"Unsupported model type: {model_type}")