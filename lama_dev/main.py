"""
main.py: Entry point for the text-to-SQL application.
- Initializes LLM, database, vector store, MCP tools, and agent.
- Runs a sample query to demonstrate functionality.
"""

from src.core.llm import initialize_llm
from src.core.database import initialize_database
from src.core.schema_retrieval import initialize_vector_store
from src.tools.mcp_tools import initialize_mcp_tools
from src.agents.agent import initialize_agent, process_text_to_sql
from src.utils.logging import setup_logging

logger = setup_logging(__name__)

def main():
    # Initialize components
    llm = initialize_llm()
    db = initialize_database()
    vector_store = initialize_vector_store()
    mcp_client = initialize_mcp_tools(db, vector_store)
    executor = initialize_agent(llm, db, mcp_client)

    # Example query
    question = "How many unique airplane producers are there?"
    response = process_text_to_sql(executor, mcp_client, question)
    
    print("Question:", response["question"])
    print("SQL Query/Result:", response.get("sql_query", response.get("error")))

if __name__ == "__main__":
    main()