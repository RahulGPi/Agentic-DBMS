import psycopg
from psycopg.rows import dict_row
import os

# Configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "agentic_db")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASS = os.getenv("DB_PASS", "password123")
DB_PORT = os.getenv("DB_PORT", "5432")

def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    conn = psycopg.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )
    conn.autocommit = True
    return conn

def execute_query(sql: str):
    """Executes a raw SQL query and returns the results (if any)."""
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=dict_row)
    try:
        cursor.execute(sql)
        # If the query returns rows (like SELECT), fetch them
        if cursor.description:
            result = cursor.fetchall()
            return result
        return {"status": "success", "message": "Query executed successfully"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        conn.close()

def get_current_schema():
    """
    Introspects the PostgreSQL database to build a JSON schema 
    compatible with the React frontend.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Get all table names in the public schema
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
    """)
    tables = cursor.fetchall()
    
    schema_output = []
    
    for (table_name,) in tables:
        # 2. Get columns for each table
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name = %s
        """, (table_name,))
        columns_data = cursor.fetchall()
        
        # 3. Check for Primary Keys
        cursor.execute("""
            SELECT c.column_name
            FROM information_schema.table_constraints tc 
            JOIN information_schema.constraint_column_usage ccu ON tc.constraint_name = ccu.constraint_name
            JOIN information_schema.columns c ON c.table_name = tc.table_name AND c.column_name = ccu.column_name
            WHERE constraint_type = 'PRIMARY KEY' AND tc.table_name = %s
        """, (table_name,))
        pks = [r[0] for r in cursor.fetchall()]
        
        formatted_columns = []
        for col_name, dtype, is_null in columns_data:
            formatted_columns.append({
                "name": col_name,
                "type": dtype.upper(), #// Postgres types (integer, character varying)
                "isPk": col_name in pks
            })
            
        schema_output.append({
            "id": f"tbl_{table_name}",
            "name": table_name,
            "columns": formatted_columns
        })
        
    cursor.close()
    conn.close()
    return schema_output

def init_db():
    """Creates a sample table if none exist, just for testing."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            email VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.close()