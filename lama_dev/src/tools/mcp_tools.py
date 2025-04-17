"""
src/tools/mcp_tools.py: Defines tools for text-to-SQL operations.
- Uses direct function calls instead of fastmcp for simplicity.
- Includes a LangChain-compatible SchemaRetrievalTool with Pydantic fields.
"""

from langchain_core.tools import BaseTool
from pydantic import Field
from src.config.config import CONFIG
from src.core import schema_retrieval
from src.utils.logging import setup_logging

logger = setup_logging(__name__)

def execute_sql_query(query: str, db) -> str:
    """Execute a SQL query and return results or error message."""
    try:
        result = db.run(query)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

def list_tables(db) -> str:
    """List available tables in the database."""
    return str(db.get_usable_table_names())

def retrieve_schema_tool(query: str, vector_store) -> str:
    """Retrieve relevant schema from ChromaDB."""
    if vector_store is None:
        # Fallback: Use schema from config if vector_store is not provided
        logger.info("Using fallback schema from CONFIG")
        return CONFIG["schema"]
    return schema_retrieval.retrieve_schema(vector_store, query)

class MCPClient:
    def call_tool(self, tool_name: str, args: dict):
        """Mock MCP client to call tools directly."""
        if tool_name == "execute_sql_query":
            return execute_sql_query(args["query"], args["db"])
        elif tool_name == "list_tables":
            return list_tables(args["db"])
        elif tool_name == "retrieve_schema":
            return retrieve_schema_tool(args["query"], args.get("vector_store"))
        raise ValueError(f"Unknown tool: {tool_name}")

def initialize_mcp_tools(db, vector_store):
    """Initialize mock MCP client."""
    return MCPClient()

class SchemaRetrievalTool(BaseTool):
    name: str = "schema_retrieval"
    description: str = "Retrieve relevant database schema for a given query."
    mcp_client: object = Field(description="MCP client for schema retrieval")

    def __init__(self, mcp_client):
        super().__init__(mcp_client=mcp_client)

    def _run(self, query: str) -> str:
        """Synchronous execution of schema retrieval."""
        return self.mcp_client.call_tool("retrieve_schema", {"query": query, "vector_store": None})

    async def _arun(self, query: str) -> str:
        """Asynchronous execution (not used, but required by BaseTool)."""
        return self._run(query)