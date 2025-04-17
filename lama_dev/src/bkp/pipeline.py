from typing import Dict
from .agents import TextToSQLAgents
from .database import DatabaseManager
from .messaging import Messaging

class TextToSQLPipeline:
    def __init__(self, llm, db_path: str = "sqlite:///example.db"):
        self.db_manager = DatabaseManager(db_path)
        self.agents = TextToSQLAgents(llm)
        self.messaging = Messaging()

    def run(self, question: str, max_attempts: int = 3) -> str:
        self.messaging.log_status("Starting Text-to-SQL pipeline")
        
        cleaned_question = self.messaging.preprocess_input(question)
        schema = self.db_manager.get_schema()
        self.messaging.log_agent_output("schema_retriever", schema)
        
        parsed = self.agents.parser_agent(cleaned_question, schema)
        self.messaging.log_agent_output("parser", parsed)
        self.messaging.log_status("Parsed question successfully")
        
        attempt = 0
        query = None
        while attempt < max_attempts:
            query = self.agents.sql_generator_agent(parsed, schema)
            self.messaging.log_agent_output("generator", query)
            
            is_valid, reason = self.agents.validator_agent(query, schema, cleaned_question, self.db_manager)
            self.messaging.log_agent_output("validator", {"is_valid": is_valid, "reason": reason})
            
            if is_valid:
                self.messaging.log_status("Generated valid query")
                break
            
            query = self.agents.corrector_agent(query, reason, parsed, schema)
            self.messaging.log_agent_output("corrector", query)
            self.messaging.log_status(f"Attempt {attempt + 1} failed, correcting query")
            attempt += 1
        
        if not is_valid:
            self.messaging.log_status(f"Failed after {max_attempts} attempts")
            raise Exception(f"Failed after {max_attempts} attempts: {reason}")
        
        return query

    def get_logs(self):
        return {
            "acp_queue": self.agents.get_acp_queue(),
            "mcp_queue": self.messaging.get_mcp_queue()
        }