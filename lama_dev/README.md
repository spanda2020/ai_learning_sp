# Text-to-SQL Application using MCP
This project implements a robust text-to-SQL solution that converts natural language questions into SQL queries, executes them against a SQLite database, and returns the results. It uses a LangChain ReAct agent with tools for query execution, table listing, and schema retrieval, supporting self-correction for complex queries. The application is built with Ollama (LLaMA) for local LLM inference and is compatible with AWS Bedrock (Claude) for cloud-based LLM inference, aligning with the AWS blog on text-to-SQL solutions.

## Features
Natural Language to SQL: Converts questions like "How many unique airplane producers are there?" into SQL queries (e.g., SELECT COUNT(DISTINCT Producer) FROM airplanes;).

Query Execution: Executes generated queries against a SQLite database and returns results (e.g., [(3)]).

Self-Correction: Uses a ReAct agent to analyze errors, correct queries, and retry up to 5 iterations.

Schema Retrieval: Retrieves relevant database schema using a mock MCP client or ChromaDB with Ollama embeddings (nomic-embed-text).

LLM Support: Supports local inference with Ollama (llama3) and cloud inference with AWS Bedrock (Claude).

Sample Database: Includes a SQLite database (sample.db) with an airplanes table for demonstration.

```markdown
## Project Structure

lama_dev/
├── src/
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── config.py          # Configuration for LLM, database, and schema
│   ├── core/
│   │   ├── __init__.py
│   │   ├── llm.py             # Initializes Ollama or Bedrock LLM
│   │   ├── database.py        # Sets up SQLite database with sample data
│   │   └── schema_retrieval.py # Initializes ChromaDB vector store
│   ├── tools/
│   │   ├── __init__.py
│   │   └── mcp_tools.py       # Defines SQL tools (query, list tables, schema retrieval)
│   ├── agents/
│   │   ├── __init__.py
│   │   └── agent.py           # ReAct agent for query generation and execution
│   └── utils/
│       ├── __init__.py
│       └── logging.py         # Logging setup
├── tests/
│   ├── __init__.py
│   └── test_agent.py          # Placeholder for tests
├── main.py                    # Entry point to run the application
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
└── sample.db                  # SQLite database with airplanes table

```

## Prerequisites
Python: 3.11 or higher

Ollama: For local LLM inference (install from Ollama)

AWS CLI: Optional, for Bedrock integration (configure with aws configure)

SQLite: For database operations (included with Python)

