"""
src/core/database.py: Initializes SQLite database for text-to-SQL queries.
- Creates a sample database with schema if it doesn't exist.
- Checks for existing tables to avoid duplication errors.
- Populates with sample data if the table is empty.
- Returns a LangChain SQLDatabase object.
"""

from langchain_community.utilities import SQLDatabase
from src.config.config import CONFIG
import sqlite3
from src.utils.logging import setup_logging

logger = setup_logging(__name__)

def initialize_database():
    """Initialize SQLite database and return SQLDatabase object."""
    db_uri = CONFIG["database_uri"]
    
    # Connect to the database
    conn = sqlite3.connect("sample.db")
    cursor = conn.cursor()
    
    # Check if the airplanes table exists
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='airplanes';
    """)
    table_exists = cursor.fetchone()
    
    if not table_exists:
        # Create the table if it doesn't exist
        logger.info("Creating airplanes table")
        conn.executescript(CONFIG["schema"])
    
    # Check if the table is empty and populate if needed
    cursor.execute("SELECT COUNT(*) FROM airplanes")
    row_count = cursor.fetchone()[0]
    if row_count == 0:
        logger.info("Populating airplanes table with sample data")
        conn.executescript("""
            INSERT INTO airplanes (Airplane_id, Producer, Type) VALUES
            (1, 'Boeing', 'Jet'),
            (2, 'Airbus', 'Jet'),
            (3, 'Boeing', 'Prop'),
            (4, 'Embraer', 'Jet');
        """)
    
    conn.commit()
    conn.close()
    
    logger.info(f"Connecting to database: {db_uri}")
    return SQLDatabase.from_uri(db_uri)