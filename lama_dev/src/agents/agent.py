"""
src/agents/agent.py: Initializes and runs the LangChain ReAct agent for text-to-SQL.
- Uses tools for SQL execution, table listing, and schema retrieval.
- Executes generated queries and returns accurate results.
- Supports self-correction via error analysis and retries.
"""

from langchain.agents import create_react_agent, AgentExecutor
from langchain_community.tools.sql_database.tool import (
    QuerySQLDataBaseTool,
    ListSQLDatabaseTool,
)
from langchain_core.prompts import PromptTemplate
from src.tools.mcp_tools import SchemaRetrievalTool
from src.utils.logging import setup_logging
from src.config.config import CONFIG
from langchain_community.utilities import SQLDatabase

logger = setup_logging(__name__)

def initialize_agent(llm, db, mcp_client):
    """Initialize LangChain ReAct agent."""
    # LangChain tools
    query_tool = QuerySQLDataBaseTool(db=db)
    list_tables_tool = ListSQLDatabaseTool(db=db)
    schema_tool = SchemaRetrievalTool(mcp_client)

    # ReAct-compatible prompt template
    SQL_PROMPT = PromptTemplate.from_template(
        """
        You are an expert SQL assistant tasked with answering user questions by generating and executing SQL queries based on the provided database schema.
        Your goal is to:
        1. Generate a syntactically correct SQL query to answer the question.
        2. Execute the query using the sql_db_query tool to retrieve the result.
        3. Verify the result makes sense given the schema and question.
        If the query fails or the result seems incorrect, analyze the error, correct the query, and retry.
        
        Question: {question}
        Schema: {schema}
        
        Available tools:
        {tools}
        
        Tool names: {tool_names}
        
        Follow this process:
        Thought: [Explain your reasoning for the query]
        Action: sql_db_query
        Input: [The SQL query to execute]
        
        After execution:
        Observation: [The result returned by the tool]
        Thought: [Verify if the result answers the question correctly]
        Final Answer: [The query result, e.g., [(3)]]
        
        If the question explicitly asks for only the query, return:
        Final Answer: [SQL query]
        
        Scratchpad for intermediate steps:
        {agent_scratchpad}
        """
    )

    # Create agent
    agent = create_react_agent(
        llm=llm,
        tools=[query_tool, list_tables_tool, schema_tool],
        prompt=SQL_PROMPT,
    )

    # Create executor
    executor = AgentExecutor(
        agent=agent,
        tools=[query_tool, list_tables_tool, schema_tool],
        verbose=True,
        max_iterations=5,
        handle_parsing_errors=True,
    )
    
    logger.info("Initialized LangChain agent")
    return executor

def process_text_to_sql(executor, mcp_client, question: str) -> dict:
    """Process a user query and return SQL query/result."""
    try:
        schema = mcp_client.call_tool("retrieve_schema", {"query": question, "vector_store": None})
        logger.info(f"Retrieved schema: {schema}")

        result = executor.invoke({"question": question, "schema": schema})
        logger.info(f"Agent result: {result}")

        output = result.get("output", "No result returned.")
        # Extract query and result from output
        query = None
        query_result = output

        # If output contains a query, extract it
        if "SELECT" in output:
            # Try to find the query in the agent's reasoning steps
            for step in result.get("intermediate_steps", []):
                if step[0].tool == "sql_db_query":
                    query = step[0].tool_input
                    query_result = step[1] if step[1] else output
                    break

        # Verify result by re-executing the query
        if query and query_result and query_result != "No result returned.":
            db = SQLDatabase.from_uri(CONFIG["database_uri"])
            try:
                verified_result = db.run(query)
                if verified_result != query_result:
                    logger.warning(f"Agent result {query_result} differs from verified result {verified_result}")
                    query_result = verified_result
            except Exception as e:
                logger.error(f"Verification failed: {str(e)}")
                query_result = f"Error verifying result: {str(e)}"

        return {
            "question": question,
            "sql_query": query,
            "result": query_result
        }
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        return {"question": question, "error": str(e)}