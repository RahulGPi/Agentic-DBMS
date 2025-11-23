import requests
import json
import re

# Configuration for Ollama
# If running inside Docker, use "http://host.docker.internal:11434/api/generate"
# If running Python locally (outside Docker), use "http://localhost:11434/api/generate"
OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL_NAME = "qwen2.5-coder:3b"

def _send_to_ollama(prompt):
    """Helper to send raw prompt to Ollama."""
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.1, 
            "num_predict": 250 
        }
    }
    try:
        # Timeout increased to 90s to handle larger RAG contexts
        response = requests.post(OLLAMA_URL, json=payload, timeout=90)
        response.raise_for_status()
        return clean_llm_response(response.json().get("response", "").strip())
    except requests.exceptions.RequestException as e:
        print(f"LLM Connection Error: {e}")
        return f"-- Error connecting to Local LLM: {str(e)}"

def clean_llm_response(text):
    """Removes markdown backticks and extra whitespace."""
    text = re.sub(r'```sql\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'```\s*', '', text)
    return text.strip()

def _build_schema_context(schema_context):
    """Converts JSON schema to DDL for RAG."""
    schema_statements = []
    for table in schema_context:
        col_defs = []
        for c in table['columns']:
            col_def = f"{c['name']} {c['type']}"
            if c['isPk']: col_def += " PRIMARY KEY"
            if c.get('fk'): col_def += f" REFERENCES {c['fk']['table']}({c['fk']['col']})"
            col_defs.append(col_def)
        schema_statements.append(f"CREATE TABLE {table['name']} (\n    {', '.join(col_defs)}\n);")
    return "\n\n".join(schema_statements)

def generate_sql_from_query(user_query: str, schema_context: list):
    """Initial generation pass."""
    schema_text = _build_schema_context(schema_context)
    
    system_prompt = f"""
    You are a PostgreSQL expert. Convert the user's natural language question into a valid SQL query.
    
    ### LIVE DATABASE SCHEMA (RAG CONTEXT) ###
    {schema_text}
    
    ### RULES ###
    1. Return ONLY the raw SQL. No markdown.
    2. Always end with a semicolon (;).
    3. If creating tables, use `IF NOT EXISTS`.
    4. If dropping tables, ALWAYS append `CASCADE`.
    5. Use valid PostgreSQL syntax.
    """
    
    full_prompt = f"{system_prompt}\n\nUser Question: {user_query}\nSQL:"
    return _send_to_ollama(full_prompt)

def fix_generated_sql(user_query: str, failed_sql: str, error_msg: str, schema_context: list):
    """
    Self-Correction pass: Takes the failed SQL and the DB Error to generate a fix.
    """
    schema_text = _build_schema_context(schema_context)
    
    system_prompt = f"""
    You are a PostgreSQL expert debugging a broken query.
    
    ### LIVE DATABASE SCHEMA ###
    {schema_text}
    
    ### ORIGINAL REQUEST ###
    User: "{user_query}"
    
    ### FAILED ATTEMPT ###
    SQL: {failed_sql}
    
    ### DATABASE ERROR ###
    Error: {error_msg}
    
    ### INSTRUCTIONS ###
    1. Analyze the error message (e.g., syntax error, missing column, constraint violation).
    2. Rewrite the SQL to fix the error.
    3. If the error is about dependencies (DROP), ensure CASCADE is used.
    4. Return ONLY the corrected SQL. No explanations.
    """
    
    full_prompt = f"{system_prompt}\n\nCorrected SQL:"
    print(f"--- ATTEMPTING AUTO-REPAIR ---")
    print(f"Error: {error_msg}")
    
    return _send_to_ollama(full_prompt)