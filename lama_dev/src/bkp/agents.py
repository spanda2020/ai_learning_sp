import json
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from typing import Dict, Tuple

class TextToSQLAgents:
    def __init__(self, llm):
        self.llm = llm
        self.acp_queue = []

        # Parser Agent
        parser_prompt = PromptTemplate(
            input_variables=["question", "schema"],
            template="""
            Schema: {schema}
            Question: {question}
            Extract as JSON:
            - Entities (tables)
            - Conditions (filters)
            - Aggregations (e.g., COUNT)
            - Relationships (e.g., joins)
            """
        )
        self.parser_chain = LLMChain(llm=llm, prompt=parser_prompt)

        # Generator Agent
        generator_prompt = PromptTemplate(
            input_variables=["schema", "parsed"],
            template="""
            Schema: {schema}
            Parsed Input: {parsed}
            Generate a SQL query.
            """
        )
        self.generator_chain = LLMChain(llm=llm, prompt=generator_prompt)

        # Corrector Agent
        corrector_prompt = PromptTemplate(
            input_variables=["schema", "query", "error", "parsed"],
            template="""
            Schema: {schema}
            Original Query: {query}
            Error: {error}
            Parsed Input: {parsed}
            Suggest a corrected SQL query.
            """
        )
        self.corrector_chain = LLMChain(llm=llm, prompt=corrector_prompt)

    def parser_agent(self, question: str, schema: Dict) -> Dict:
        schema_json = json.dumps(schema, indent=2)
        response = self.parser_chain.run(question=question, schema=schema_json)
        # Mock parsing (replace with LLM output parsing)
        parsed = {
            "entities": ["Customers", "Orders"],
            "conditions": ["city = 'New York'", "amount > 100"],
            "aggregations": [],
            "relationships": [{"table1": "Customers", "table2": "Orders", "join": "customer_id = id"}]
        }
        self.acp_queue.append({
            "agent": "parser",
            "action": "parse",
            "input": question,
            "output": parsed
        })
        return parsed

    def sql_generator_agent(self, parsed: Dict, schema: Dict) -> str:
        schema_json = json.dumps(schema, indent=2)
        parsed_json = json.dumps(parsed, indent=2)
        query = self.generator_chain.run(schema=schema_json, parsed=parsed_json).strip()
        # Mock query
        query = "SELECT c.name FROM Customers c JOIN Orders o ON c.id = o.customer_id WHERE c.city = 'New York' AND o.amount > 100"
        self.acp_queue.append({
            "agent": "sql_generator",
            "action": "generate",
            "input": parsed,
            "output": query
        })
        return query

    def validator_agent(self, query: str, schema: Dict, question: str, db_manager) -> Tuple[bool, str]:
        # Syntax check
        result = db_manager.execute_query(query)
        if result is not True:
            self.acp_queue.append({
                "agent": "validator",
                "action": "validate",
                "input": query,
                "output": {"is_valid": False, "reason": f"Syntax error: {result[1]}"}
            })
            return False, f"Syntax error: {result[1]}"
        
        # Schema check
        for table in schema:
            if table.lower() in query.lower():
                for col in schema[table]:
                    if col.lower() in question.lower() and col.lower() not in query.lower():
                        self.acp_queue.append({
                            "agent": "validator",
                            "action": "validate",
                            "input": query,
                            "output": {"is_valid": False, "reason": f"Missing column: {col}"}
                        })
                        return False, f"Missing column: {col}"
        
        # Semantic check
        for condition in question.lower().split():
            if condition in ["new york", "100"] and condition.lower() not in query.lower():
                self.acp_queue.append({
                    "agent": "validator",
                    "action": "validate",
                    "input": query,
                    "output": {"is_valid": False, "reason": f"Missing condition: {condition}"}
                })
                return False, f"Missing condition: {condition}"
        
        self.acp_queue.append({
            "agent": "validator",
            "action": "validate",
            "input": query,
            "output": {"is_valid": True, "reason": "Valid"}
        })
        return True, "Valid"

    def corrector_agent(self, query: str, error: str, parsed: Dict, schema: Dict) -> str:
        schema_json = json.dumps(schema, indent=2)
        parsed_json = json.dumps(parsed, indent=2)
        corrected_query = self.corrector_chain.run(
            schema=schema_json, query=query, error=error, parsed=parsed_json
        ).strip()
        # Mock correction
        corrected_query = query
        self.acp_queue.append({
            "agent": "corrector",
            "action": "correct",
            "input": {"query": query, "error": error},
            "output": corrected_query
        })
        return corrected_query

    def get_acp_queue(self):
        return self.acp_queue