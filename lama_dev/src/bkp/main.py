import json
from pipeline import TextToSQLPipeline
from database import DatabaseManager
from llm_config import get_llm

def main():
    # Setup database
    DatabaseManager.setup_example_db()

    # Initialize LLM and pipeline
    llm = get_llm(model_type="ollama")  # Change to "claude" for Claude
    pipeline = TextToSQLPipeline(llm)

    # Run pipeline
    question = "Find customers in New York with orders over $100"
    try:
        final_query = pipeline.run(question)
        print("Final SQL Query:", final_query)
        logs = pipeline.get_logs()
        print("\nACP Message Log:", json.dumps(logs["acp_queue"], indent=2))
        print("\nMCP Message Log:", json.dumps(logs["mcp_queue"], indent=2))
    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    main()