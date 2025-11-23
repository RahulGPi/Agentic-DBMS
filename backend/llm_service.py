import requests
import json
import re

# Configuration for Ollama
# OLLAMA_URL = "http://host.docker.internal:11434/api/generate" # Use host.docker.internal if running backend in Docker
OLLAMA_URL = "http://localhost:11434/api/generate"
# If running backend locally (not in Docker), use: "http://localhost:11434/api/generate"

MODEL_NAME = "qwen2.5-coder:1.5b"

def generate_sql_from_query(user_query: str, schema_context: list):
    """
    Constructs the prompt and calls the local Qwen model.
    """
    
    # 1. Format the schema into a readable string for the LLM
    schema_text = ""
    for table in schema_context:
        columns = ", ".join([f"{c['name']} ({c['type']})" for c in table['columns']])
        schema_text += f"Table: {table['name']}\nColumns: {columns}\n\n"

    # 2. Strict Prompt Engineering for the 1.5B model
    # Smaller models need very specific instructions to avoid chatting.
    system_prompt = f"""
    You are a PostgreSQL expert. Convert the user's natural language question into a valid SQL query.
    
    Database Schema:
    {schema_text}
    
    Rules:
    1. Return ONLY the raw SQL. 
    2. Do NOT use markdown code blocks (```sql). 
    3. Do NOT add explanations.
    4. Always end with a semicolon (;).
    5. Use valid PostgreSQL syntax.
    """

    full_prompt = f"{system_prompt}\n\nUser Question: {user_query}\nSQL:"

    payload = {
        "model": MODEL_NAME,
        "prompt": full_prompt,
        "stream": False,
        "options": {
            "temperature": 0.1, # Keep it deterministic
            "num_predict": 150  # Short output (SQL is rarely long)
        }
    }

    try:
        # Note: If running backend in Docker, ensure Ollama allows external connections
        # or use host networking. 
        response = requests.post(OLLAMA_URL, json=payload, timeout=10)
        response.raise_for_status()
        
        result_json = response.json()
        raw_response = result_json.get("response", "").strip()
        
        # 3. Clean the output (Post-processing)
        # Sometimes models still wrap code in markdown despite instructions
        clean_sql = clean_llm_response(raw_response)
        
        return clean_sql

    except requests.exceptions.RequestException as e:
        print(f"LLM Connection Error: {e}")
        return f"-- Error connecting to Local LLM: {str(e)}"

def clean_llm_response(text):
    """Removes markdown backticks and extra whitespace."""
    # Remove ```sql ... ``` or just ``` ... ```
    text = re.sub(r'```sql\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'```\s*', '', text)
    # Remove leading/trailing whitespace
    text = text.strip()
    return text