import sqlite3
from sqlalchemy import create_engine, MetaData
from langchain_community.utilities import SQLDatabase
from typing import Dict, List

class DatabaseManager:
    def __init__(self, db_path: str = "sqlite:///example.db"):
        try:
            self.engine = create_engine(db_path)
            self.metadata = MetaData()
            self.metadata.reflect(bind=self.engine)
            self.db = SQLDatabase.from_uri(db_path)
        except Exception as e:
            raise Exception(f"Database error: {e}. Ensure {db_path} exists.")

    def get_schema(self) -> Dict[str, List[str]]:
        return {
            table: [col.name for col in self.metadata.tables[table].columns]
            for table in self.metadata.tables
        }

    def execute_query(self, query: str) -> bool:
        try:
            self.db.run(query)
            return True
        except Exception as e:
            return False, str(e)

    @staticmethod
    def setup_example_db(db_path: str = "example.db"):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS Customers (id INTEGER PRIMARY KEY, name TEXT, city TEXT)")
            cursor.execute("CREATE TABLE IF NOT EXISTS Orders (order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER)")
            cursor.execute("INSERT OR IGNORE INTO Customers (id, name, city) VALUES (1, 'Alice', 'New York'), (2, 'Bob', 'Chicago')")
            cursor.execute("INSERT OR IGNORE INTO Orders (order_id, customer_id, amount) VALUES (1, 1, 150), (2, 2, 50)")
            conn.commit()
            conn.close()
        except Exception as e:
            raise Exception(f"Error setting up database: {e}")