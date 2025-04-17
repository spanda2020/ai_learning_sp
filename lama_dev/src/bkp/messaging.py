from typing import Dict, List

class Messaging:
    def __init__(self):
        self.mcp_queue = []

    def log_status(self, status: str):
        self.mcp_queue.append({"component": "status_logger", "data": status})

    def preprocess_input(self, question: str) -> str:
        cleaned_question = question.strip().lower()
        self.mcp_queue.append({
            "component": "preprocessor",
            "data": {"raw_input": question, "cleaned_input": cleaned_question}
        })
        return cleaned_question

    def log_agent_output(self, component: str, data: Dict):
        self.mcp_queue.append({"component": component, "data": data})

    def get_mcp_queue(self):
        return self.mcp_queue