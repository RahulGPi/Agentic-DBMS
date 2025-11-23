from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Any
from fastapi.middleware.cors import CORSMiddleware
import database

app = FastAPI()

# Enable CORS for the React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Models for Request Bodies ---

class SQLRequest(BaseModel):
    sql: str

class DDLRequest(BaseModel):
    action: str  # 'create_table', 'add_column', 'drop_column'
    table_name: str
    column_name: Optional[str] = None
    column_type: Optional[str] = None

# --- Routes ---

@app.on_event("startup")
def startup_event():
    """Initialize DB with sample data on startup"""
    try:
        database.init_db()
        print("Database initialized.")
    except Exception as e:
        print(f"Error connecting to DB: {e}")

@app.get("/schema")
def read_schema():
    """Returns the current database schema in JSON format."""
    try:
        schema = database.get_current_schema()
        return schema
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask")
def execute_agent_sql(request: SQLRequest):
    """
    Endpoint for the Agent to execute generated SQL.
    """
    # SECURITY NOTE: In a real production app, you need strict safeguards here.
    # This is a raw SQL execution endpoint.
    print(f"Executing SQL: {request.sql}")
    result = database.execute_query(request.sql)
    
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
        
    return result

@app.post("/ddl")
def execute_no_code_update(request: DDLRequest):
    """
    Endpoint for the No-Code tool to update schema.
    Constructs SQL based on the structured request.
    """
    sql = ""
    
    try:
        if request.action == "create_table":
            # Simple default table creation
            sql = f"CREATE TABLE {request.table_name} (id SERIAL PRIMARY KEY);"
            
        elif request.action == "add_column":
            if not request.column_name or not request.column_type:
                raise HTTPException(status_code=400, detail="Column name and type required")
            sql = f"ALTER TABLE {request.table_name} ADD COLUMN {request.column_name} {request.column_type};"
            
        elif request.action == "drop_column":
            if not request.column_name:
                raise HTTPException(status_code=400, detail="Column name required")
            sql = f"ALTER TABLE {request.table_name} DROP COLUMN {request.column_name};"
            
        elif request.action == "drop_table":
             sql = f"DROP TABLE {request.table_name};"

        else:
            raise HTTPException(status_code=400, detail="Unknown action")

        print(f"Executing DDL: {sql}")
        result = database.execute_query(sql)
        
        if isinstance(result, dict) and "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
            
        return {"status": "success", "sql_executed": sql}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)